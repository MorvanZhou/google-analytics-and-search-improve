#!/usr/bin/env python3
"""Google Search Console API data extraction tool.

Usage:
    python gsc_query.py --site-url "https://example.com" --mode search_analytics \
        --start-date 2025-01-01 --end-date 2025-03-01 --dimensions query,page --limit 100

    python gsc_query.py --site-url "https://example.com" --mode sitemaps

    python gsc_query.py --site-url "https://example.com" --mode inspect \
        --inspect-url "https://example.com/page"

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env vars: GSC_SITE_URL
Credentials: auto-discovered from .skills-data/google-analytics-and-search-improve/configs/*.json
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime, timedelta
from pathlib import Path

# Suppress FutureWarning (Python 3.9 EOL notices from google libs)
# and NotOpenSSLWarning (urllib3 v2 + LibreSSL) so they don't pollute output.
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*urllib3.*OpenSSL.*")

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


def _find_data_dir():
    """Walk up from script dir to find .skills-data/google-analytics-and-search-improve/."""
    d = Path(__file__).resolve().parent
    while d != d.parent:
        candidate = d / ".skills-data" / "google-analytics-and-search-improve"
        if candidate.is_dir():
            return candidate
        d = d.parent
    return None


_data_dir = _find_data_dir()
if _data_dir:
    env_path = _data_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def _find_credentials():
    """Auto-discover Service Account JSON key from configs/ directory."""
    # 1. Explicit env var takes priority (backward compatible)
    explicit = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if explicit and Path(explicit).is_file():
        return explicit
    # 2. Auto-discover from configs/ directory
    if _data_dir:
        configs_dir = _data_dir / "configs"
        if configs_dir.is_dir():
            json_files = sorted(configs_dir.glob("*.json"))
            if json_files:
                # Set env var so GA4 client libs also pick it up
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(json_files[0])
                return str(json_files[0])
    return None


SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def get_credentials():
    creds_path = _find_credentials()
    if not creds_path:
        print("Error: No Service Account JSON key found in configs/ directory", file=sys.stderr)
        sys.exit(1)
    return service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )


def build_service():
    credentials = get_credentials()
    return build("searchconsole", "v1", credentials=credentials)


def query_search_analytics(service, site_url, start_date, end_date, dimensions, limit, start_row=0):
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": limit,
        "startRow": start_row,
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    return response


def fetch_all_search_analytics(service, site_url, start_date, end_date, dimensions, limit):
    """Paginate through all results up to `limit` rows."""
    all_rows = []
    start_row = 0
    page_size = min(limit, 25000)

    while len(all_rows) < limit:
        response = query_search_analytics(
            service, site_url, start_date, end_date, dimensions, page_size, start_row
        )
        rows = response.get("rows", [])
        if not rows:
            break
        all_rows.extend(rows)
        start_row += len(rows)
        if len(rows) < page_size:
            break

    return all_rows[:limit]


def list_sitemaps(service, site_url):
    response = service.sitemaps().list(siteUrl=site_url).execute()
    return response.get("sitemap", [])


def inspect_url(service, site_url, inspect_url_str):
    body = {
        "inspectionUrl": inspect_url_str,
        "siteUrl": site_url,
    }
    response = service.urlInspection().index().inspect(body=body).execute()
    return response


def main():
    parser = argparse.ArgumentParser(description="Google Search Console API query tool")
    parser.add_argument("--site-url", default=os.environ.get("GSC_SITE_URL"),
                        help="Site URL (or set GSC_SITE_URL env)")
    parser.add_argument("--mode", choices=["search_analytics", "sitemaps", "inspect"],
                        default="search_analytics")
    parser.add_argument("--start-date", default=(datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d"))
    parser.add_argument("--end-date", default=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
    parser.add_argument("--dimensions", default="query,page",
                        help="Comma-separated: query,page,country,device,date,searchAppearance")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--inspect-url", help="URL to inspect (for inspect mode)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.site_url:
        print("Error: --site-url required or set GSC_SITE_URL", file=sys.stderr)
        sys.exit(1)

    service = build_service()
    result = None

    if args.mode == "search_analytics":
        dims = [d.strip() for d in args.dimensions.split(",")]
        rows = fetch_all_search_analytics(
            service, args.site_url, args.start_date, args.end_date, dims, args.limit
        )
        result = {
            "mode": "search_analytics",
            "site_url": args.site_url,
            "date_range": {"start": args.start_date, "end": args.end_date},
            "dimensions": dims,
            "total_rows": len(rows),
            "rows": rows,
        }
    elif args.mode == "sitemaps":
        sitemaps = list_sitemaps(service, args.site_url)
        result = {
            "mode": "sitemaps",
            "site_url": args.site_url,
            "sitemaps": sitemaps,
        }
    elif args.mode == "inspect":
        if not args.inspect_url:
            print("Error: --inspect-url required for inspect mode", file=sys.stderr)
            sys.exit(1)
        inspection = inspect_url(service, args.site_url, args.inspect_url)
        result = {
            "mode": "inspect",
            "site_url": args.site_url,
            "inspect_url": args.inspect_url,
            "result": inspection,
        }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
