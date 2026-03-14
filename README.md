# Google Analytics & Search Console Improvement Skill

[中文文档](README_CN.md)

An AI agent skill that analyzes website data via Google Search Console (GSC) and Google Analytics 4 (GA4) APIs, audits live sites with browser automation, reviews source code, and generates data-driven improvement plans.

## What It Does

Give your AI agent a website URL, and it will:

1. **Collect data** from GSC and GA4 via API (or manual CSV export)
2. **Analyze search performance** — keywords, CTR, rankings, indexing health
3. **Analyze user behavior** — traffic sources, bounce rates, device breakdowns, conversion funnels
4. **Audit the live site** — screenshots, PageSpeed Insights, SEO metadata extraction
5. **Review source code** (optional) — meta tags, structured data, performance patterns
6. **Generate a prioritized report** — P0-P3 action items across 6 dimensions

### Six Analysis Dimensions

| Dimension | Data Source | Key Metrics |
|-----------|------------|-------------|
| SEO | GSC | CTR, rankings, impressions, index coverage |
| Performance | PageSpeed Insights | LCP, INP, CLS, TTFB |
| Content Strategy | GA4 + GSC | Page views, engagement rate, content gaps |
| User Experience | GA4 | Bounce rate, session duration, device breakdowns |
| Conversion | GA4 | Funnel analysis, landing page conversion rates |
| Technical | Browser + Source | Meta tags, JSON-LD, robots.txt, sitemap, accessibility |

## Installation

```bash
npx skills add morvanzhou/google-analytics-and-search-improve
```

Or clone manually into your skills directory:

```
skills/
  google-analytics-and-search-improve/
    SKILL.md              # Skill definition (workflow instructions)
    scripts/
      gsc_query.py        # GSC API data extraction
      ga4_query.py        # GA4 API data extraction
      requirements.txt    # Python dependencies
    references/
      gsc-api-guide.md    # GSC auth setup & script usage
      ga4-api-guide.md    # GA4 auth setup & preset templates
      metrics-glossary.md # Analysis thresholds & priority matrix
```

## Quick Start

Tell your AI agent:

> Analyze example.com using the google-analytics-and-search-improve skill

The skill offers three data collection modes:

| Mode | Setup Time | Data Coverage |
|------|-----------|---------------|
| **A. API auto-collect** (recommended) | ~10 min first time | Full GSC + GA4 data |
| **B. Manual CSV export** | None | Whatever you export |
| **C. Browser audit only** | None | Technical audit only |

### Mode A: API Setup

Requires a Google Cloud Service Account with access to both GSC and GA4.

1. **Create a Google Cloud project** and enable these APIs:
   - Google Search Console API
   - Google Analytics Data API
   - PageSpeed Insights API

2. **Create a Service Account**, download the JSON key file

3. **Grant access**:
   - In GSC: Settings → Users → Add the SA email as "Restricted" user
   - In GA4: Admin → Property Access → Add the SA email as "Viewer"

4. **Provide config** to the AI agent:
   - JSON key file path (absolute path)
   - GSC site URL — use `sc-domain:example.com` for Domain properties or `https://example.com` for URL-prefix properties
   - GA4 Property ID (numeric)

> **Important**: GSC has two property types. Using the wrong format causes a 403 error. Check the property selector in [Search Console](https://search.google.com/search-console/) — if it shows a bare domain, use `sc-domain:` prefix.

See [references/gsc-api-guide.md](skills/google-analytics-and-search-improve/references/gsc-api-guide.md) for step-by-step instructions.

## Project Structure

```
.
├── skills/google-analytics-and-search-improve/
│   ├── SKILL.md                          # Skill definition & workflow
│   ├── scripts/
│   │   ├── gsc_query.py                  # GSC Search Analytics, Sitemaps, URL Inspect
│   │   ├── ga4_query.py                  # GA4 with 8 preset query templates
│   │   └── requirements.txt              # google-api-python-client, google-analytics-data, etc.
│   └── references/
│       ├── gsc-api-guide.md              # Auth setup, script usage, dimensions
│       ├── ga4-api-guide.md              # Auth setup, presets, metrics reference
│       └── metrics-glossary.md           # Thresholds, diagnostic criteria, priority matrix
├── .skills-data/                         # Runtime data (gitignored)
│   └── google-analytics-and-search-improve/
│       ├── .env                          # Credentials & config
│       ├── data/                         # Collected JSON/CSV data & reports
│       ├── tmp/                          # Screenshots
│       ├── cache/                        # API response cache
│       └── venv/                         # Python virtual environment
└── .gitignore
```

## Output

The skill generates a comprehensive improvement report at `.skills-data/google-analytics-and-search-improve/data/improvement-report.md` containing:

- **Data overview** — key metrics summary with current values and trends
- **Prioritized action items** (P0 urgent → P3 low priority) — each with data evidence, specific fix, and expected impact
- **Detailed analysis** — organized by the 6 dimensions
- **Execution roadmap** — week-by-week implementation plan

## Companion Skills

| Skill | Use Case |
|-------|----------|
| `seo-geo` | Implement SEO/GEO recommendations from the report |
| `agent-browser` | Browser automation for site auditing |
| `frontend-design` | Implement frontend/UX improvements |

## License

MIT
