# Bing Webmaster Tools API Reference

## Authentication Setup

### Step 1: Sign in to Bing Webmaster Tools

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters/)
2. Sign in with your Microsoft, Google, or Facebook account
3. Add your site if not already added, and complete site verification

### Step 2: Generate API Key

1. After signing in, click the **gear icon** (Settings) in the top-right
2. Go to **"API Access"**
3. Accept the Terms & Conditions
4. Click **"Generate API Key"**
5. Copy and save the generated API key

> **Note**: Only one API key per user account. If compromised, delete and regenerate (all apps using the old key will break).

### Step 3: Write to .env

Write the following values to `$DATA_DIR/.env`:

```
BING_WEBMASTER_API_KEY=your_api_key_here
```

> **Note**: The site URL is read from `SITE_URL` (the same variable used for GSC and other tools). No separate Bing site URL variable is needed.

## API Overview

| Item | Details |
|------|---------|
| **Base URL** | `https://ssl.bing.com/webmaster/api.svc/json/` |
| **Authentication** | API Key (passed as `apikey` query parameter) or OAuth 2.0 Bearer token |
| **Response format** | JSON |
| **Data retention** | **6 months** (shorter than GSC's ~16 months — set up regular data collection) |
| **Rate limits** | ~40-50 calls/day per API key for stats endpoints |

## Script Usage

Scripts auto-read `BING_WEBMASTER_API_KEY` and `SITE_URL` from `$DATA_DIR/.env`. Once `.env` is configured, you don't need to pass these values on the command line.

### Search Traffic Queries

```bash
# Top queries with traffic stats (default)
python scripts/bing_query.py

# Top pages by traffic
python scripts/bing_query.py --mode page_stats

# Overall rank & traffic stats (daily impressions/clicks)
python scripts/bing_query.py --mode rank_traffic

# Stats for a specific query
python scripts/bing_query.py --mode query_detail --query "online 3d model converter"

# Stats for a specific page
python scripts/bing_query.py --mode page_detail --page "https://example.com/tools/converter"

# Stats for a specific query + page combination
python scripts/bing_query.py --mode query_page_detail --query "3d converter" --page "https://example.com/tools/converter"

# Keyword research (with country and date range)
python scripts/bing_query.py --mode keyword --query "image compressor" --country us \
    --start-date 2026-01-01 --end-date 2026-03-01

# Related keywords
python scripts/bing_query.py --mode related_keywords --query "image compressor" --country us \
    --start-date 2026-01-01 --end-date 2026-03-01

# Inbound link analysis
python scripts/bing_query.py --mode links

# Crawl stats
python scripts/bing_query.py --mode crawl_stats

# Output to file
python scripts/bing_query.py --mode query_stats -o "$DATA_DIR/data/bing_queries.json"
```

The `--site-url` CLI flag overrides `SITE_URL` from `.env`.

### Available Modes

| Mode | API Method | Description |
|------|-----------|-------------|
| `query_stats` | `GetQueryStats` | Top queries with impressions, clicks, position |
| `page_stats` | `GetPageStats` | Top pages with traffic stats |
| `rank_traffic` | `GetRankAndTrafficStats` | Daily impressions & clicks overview |
| `query_detail` | `GetQueryTrafficStats` | Detailed stats for a specific query |
| `page_detail` | `GetPageQueryStats` | All queries driving traffic to a specific page |
| `query_page_detail` | `GetQueryPageDetailStats` | Stats for a specific query + page combination |
| `keyword` | `GetKeyword` | Keyword impression data for a country & date range |
| `related_keywords` | `GetRelatedKeywords` | Related keyword suggestions with impressions |
| `links` | `GetLinkCounts` | Pages with inbound links and link counts |
| `crawl_stats` | `GetCrawlStats` | Crawl frequency, errors, and patterns |

### Returned Metrics

Each traffic stats row contains:
- `Impressions` — Impression count on Bing search
- `Clicks` — Click count from Bing search
- `AvgClickPosition` — Average ranking position (where available)
- `Date` — Date of the data point (for time-series endpoints)

### Keyword Research Metrics

Keyword endpoints return:
- `Impressions` — Search volume / impression count for the keyword
- `BroadImpressions` — Broad match impression count
- `Query` — The keyword text

## Comparison with GSC API

| Feature | GSC API | Bing Webmaster API |
|---------|---------|-------------------|
| Auth method | Service Account (OAuth2) | API Key or OAuth 2.0 |
| Dimension filtering | `dimensionFilterGroups` with operators | Per-endpoint (query/page/query+page) |
| Custom date range | `startDate` / `endDate` on all queries | Available on keyword endpoints; traffic stats return all available data |
| Data retention | ~16 months | **6 months** |
| Keyword research | Not available | ✅ `GetKeyword`, `GetRelatedKeywords` |
| Backlink analysis | Not available | ✅ `GetLinkCounts`, `GetUrlLinks` |
| Crawl stats | Limited (via URL Inspection) | ✅ `GetCrawlStats`, `GetCrawlIssues` |
| URL submission | Not via same API | ✅ `SubmitUrl`, `SubmitUrlBatch` |
| Rate limit | ~25,000 rows/request | ~40-50 calls/day |

## Common Analysis Scenarios

### Find Top Performing Queries on Bing

Use `query_stats` mode to get all queries with traffic data. Sort by impressions or clicks to identify what's working.

### Analyze a Specific Page's Search Performance

Use `page_detail` mode with `--page` to see all queries driving traffic to a specific page. Useful for content optimization.

### Keyword Research & Discovery

Use `keyword` and `related_keywords` modes to research search volume for target keywords. This is a capability GSC doesn't offer.

### Monitor Crawl Health

Use `crawl_stats` mode to check if Bing is crawling your site efficiently. Cross-reference with crawl issues.

### Compare Google vs Bing Performance

Run the same analysis period on both GSC and Bing data to identify:
- Keywords where you rank well on Bing but not Google (or vice versa)
- Pages with high Bing traffic but low Google traffic
- Device or geo differences between the two search engines
