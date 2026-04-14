---
name: google-analytics-and-search-improve
description: Understand website goals and user journeys first, then analyze GSC/GA4 data and audit the live site to validate whether users behave as intended. Identify gaps between goals and reality, and produce actionable, goal-aligned improvement plans. Use when user wants to diagnose website problems, improve search rankings, optimize traffic, analyze Google Analytics or Search Console data, audit website performance, or create a data-backed improvement roadmap.
---

# Goal-Driven Website Analytics & Improvement

First understand what the website does and what it wants users to do, then use GSC/GA4 data combined with live-site auditing to verify whether users actually follow the intended journey. Identify the gap between goals and reality, and generate prioritized, actionable improvement plans.

## Data Storage

All runtime data is stored in `$DATA_DIR`, separated from skill code.

```
<project_root>/.skills-data/google-analytics-and-search-improve/
  .env        # Configuration (auth, URLs, etc.), auto-loaded by scripts
  data/       # Raw data only: API responses, user-uploaded CSVs (GSC/GA4/PSI JSON/CSV)
  analysis/   # Analysis outputs: reports, audit results, website profile, funnel analysis
  charts/     # Generated chart images (PNG) for embedding in analysis reports
  scripts/    # Analysis scripts: code that reads from data/ and writes to analysis/
  tmp/        # Screenshots and temporary files
  cache/      # API response cache
  configs/    # Config files
  logs/       # Execution logs
  venv/       # Python virtual environment
```

**Directory separation principle**:
- `data/` = raw, unprocessed data from APIs or user exports (input)
- `analysis/` = processed results, reports, insights, audit findings (output)
- `charts/` = generated chart images (PNG) that are embedded in analysis reports via relative paths
- `scripts/` = analysis code that transforms `data/` → `analysis/`

## Core Principle

**Goal → Data → Gap → Action**

Every analysis must start from the website's purpose and intended user journey. Data is only valuable when measured against a goal. The skill's job is to:

1. Understand what the site wants users to do (goal)
2. Use data to check if users actually do it (reality)
3. Find where the gap is (diagnosis)
4. Tell the developer what to do next (action)

## Data Visualization

**Every analysis phase that produces quantitative data MUST generate accompanying charts.** Charts are embedded in Markdown reports as images and saved to `$DATA_DIR/charts/`.

### Visualization Principles

1. **Chart-first reporting**: When presenting data findings, always generate a chart BEFORE writing the textual interpretation. The chart is the primary evidence; the text explains the insight.
2. **One chart, one insight**: Each chart should communicate a single clear message. Use the chart title to state the insight (e.g., "Mobile bounce rate is 2x desktop" instead of "Bounce rate by device").
3. **Goal-aligned visualization**: Highlight goal-relevant thresholds, targets, or benchmarks in charts using reference lines or color coding.
4. **Consistent style**: Use a consistent color palette and style across all charts in a single report.

### Chart Generation Method

Use Python with `matplotlib` to generate charts. Write a standalone Python script for each chart (or batch of related charts), execute it, and embed the resulting PNG in the Markdown report.

**Standard chart generation pattern**:

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend, MUST be set before importing pyplot
import matplotlib.pyplot as plt
import json
import os

# ── Configuration ──────────────────────────────────────────
DATA_DIR = os.environ.get("DATA_DIR", ".skills-data/google-analytics-and-search-improve")
CHARTS_DIR = os.path.join(DATA_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ── Style defaults ─────────────────────────────────────────
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})

# Color palette (consistent across all charts)
COLORS = ["#4285F4", "#EA4335", "#FBBC04", "#34A853", "#FF6D01", "#46BDC6", "#7B61FF", "#F538A0"]
COLOR_GOOD = "#34A853"
COLOR_WARN = "#FBBC04"
COLOR_BAD = "#EA4335"
COLOR_NEUTRAL = "#4285F4"

# ── Load data ──────────────────────────────────────────────
with open(os.path.join(DATA_DIR, "data", "DATAFILE.json")) as f:
    data = json.load(f)

# ── Plot ───────────────────────────────────────────────────
fig, ax = plt.subplots()
# ... plotting code ...
ax.set_title("Insight-Driven Chart Title")
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")

output_path = os.path.join(CHARTS_DIR, "chart_name.png")
fig.savefig(output_path)
plt.close(fig)
print(f"Chart saved: {output_path}")
```

**Embed in Markdown report**:
```markdown
### Finding: [Insight Title]

![Chart description](../charts/chart_name.png)

[Textual interpretation of what the chart reveals and recommended action]
```

### Chart Type Selection Guide

| Data Pattern | Recommended Chart | When to Use |
|---|---|---|
| **Trend over time** | Line chart | GSC daily clicks/impressions, GA4 traffic trends, funnel trends |
| **Category comparison** | Horizontal bar chart | Top queries by clicks, pages by traffic, channels comparison |
| **Part of whole** | Stacked bar or pie chart (≤6 slices) | Traffic source distribution, device breakdown |
| **Funnel / conversion flow** | Funnel chart (horizontal stacked bars) | User journey drop-off, signup/purchase funnel |
| **Two metrics correlation** | Scatter plot | CTR vs position, bounce rate vs page load time |
| **Distribution** | Histogram or box plot | Session duration distribution, page load time spread |
| **Before/After or Gap** | Grouped bar chart | Expected vs actual behavior, mobile vs desktop comparison |
| **Performance scores** | Gauge or bullet chart | PSI scores, CWV metrics against thresholds |
| **Ranking with values** | Horizontal bar + value labels | Top 10 keywords, top pages by any metric |

### Required Charts per Phase

**Phase 2 (GSC Analysis)** — generate and embed:
- **Keyword intent distribution**: Stacked bar or pie chart showing query distribution across Awareness / Consideration / Decision / Retention stages
- **Top queries performance**: Horizontal bar chart of top 15 queries by clicks, with CTR annotated
- **CTR vs Position scatter**: Scatter plot of queries showing CTR vs average position, highlighting high-impression low-CTR outliers
- **Trend chart**: Line chart of daily clicks & impressions over the analysis period
- **Device/country breakdown**: Bar chart of clicks by device type and/or top countries

**Phase 3 (GA4 Analysis)** — generate and embed:
- **Traffic channel breakdown**: Pie or bar chart of sessions by source/medium
- **Top landing pages**: Horizontal bar chart with engagement rate or bounce rate overlay
- **Journey gap visualization**: Grouped bar chart comparing expected vs actual conversion rates at each journey stage
- **Device comparison**: Side-by-side bars comparing key metrics (bounce rate, engagement rate, conversion) across desktop/mobile/tablet
- **Trend chart**: Line chart of sessions/users over the analysis period

**Phase 3b (Funnel Analysis)** — generate and embed:
- **Funnel chart**: Horizontal funnel visualization showing step-by-step user counts and drop-off percentages
- **Funnel by device/channel**: Grouped funnel comparison across segments
- **Funnel trend**: Line chart of daily conversion rates for key funnel steps

**Phase 4 (Site Audit)** — generate and embed:
- **PSI scores radar/bar**: Bar chart of Performance, SEO, Accessibility, Best Practices scores (mobile & desktop)
- **Core Web Vitals**: Bar or gauge chart of LCP, FID/INP, CLS against Good/Needs Improvement/Poor thresholds

**Phase 6 (Final Report)** — generate and embed:
- **Executive summary dashboard**: A multi-panel figure (2×2 or 2×3 subplots) summarizing the most critical metrics at a glance
- **Goal achievement scorecard**: Bar chart showing goal achievement percentage for each journey stage
- **Priority distribution**: Horizontal bar chart showing count of issues by P0/P1/P2/P3 priority
- Reuse the most impactful charts from Phase 2-4 in the final report (reference the same image files)

### CJK Font Support

When the site content or data contains Chinese/Japanese/Korean characters, configure matplotlib to use a CJK-compatible font:

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import platform

# Auto-detect system CJK font
system = platform.system()
if system == "Darwin":
    plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC", "Heiti SC", "STHeiti"]
elif system == "Linux":
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "DejaVu Sans"]
else:  # Windows
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False  # Fix minus sign rendering
```

## Workflow

```
Analysis Progress:
- [ ] Phase 0: Website reconnaissance & goal definition
- [ ] Phase 1: Select data source & collect data
- [ ] Phase 2: GSC data analysis (aligned to goals)
- [ ] Phase 3: GA4 data analysis (aligned to goals)
- [ ] Phase 3b: GA4 funnel exploration (optional, if user has custom events)
- [ ] Phase 4: Live site audit
- [ ] Phase 5: Source code review
- [ ] Phase 5b: SEO & GEO optimization checklist audit
- [ ] Phase 6: Generate goal-aligned improvement report
```

---

### Phase 0: Website Reconnaissance & Goal Definition

> **Why this phase exists**: Without understanding what the site does, who it serves, and what it wants users to do, all subsequent data analysis is directionless. This phase turns the analysis from a generic "health check" into a goal-oriented diagnostic.

**0a. Visit the site and build a website profile**:

Use `agent-browser` to visit `$SITE_URL` and explore the site structure (homepage + 3-5 key pages from the navigation). Build a **Website Profile**:

```bash
agent-browser open "$SITE_URL" && agent-browser wait --load networkidle
agent-browser screenshot --full homepage_overview.png
```

Save screenshots to `$DATA_DIR/tmp/`.

From the homepage and key pages, extract and analyze:

```bash
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify({
  title: document.title,
  meta_desc: document.querySelector('meta[name="description"]')?.content,
  h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()),
  h2s: Array.from(document.querySelectorAll('h2')).slice(0, 10).map(h => h.textContent.trim()),
  nav_links: Array.from(document.querySelectorAll('nav a, header a')).slice(0, 20).map(a => ({text: a.textContent.trim(), href: a.href})),
  cta_buttons: Array.from(document.querySelectorAll('a[class*="btn"], button[class*="btn"], a[class*="cta"], button[class*="cta"], [role="button"]')).slice(0, 10).map(el => ({text: el.textContent.trim(), href: el.href || ''})),
  footer_links: Array.from(document.querySelectorAll('footer a')).slice(0, 15).map(a => ({text: a.textContent.trim(), href: a.href})),
  forms: Array.from(document.querySelectorAll('form')).map(f => ({action: f.action, id: f.id, inputs: Array.from(f.querySelectorAll('input,select,textarea')).map(i => i.name || i.type)})),
  has_pricing: !!document.body.innerText.match(/pric(e|ing)|plan|subscribe|buy|purchase|付费|价格|套餐/i),
  has_login: !!document.querySelector('a[href*="login"], a[href*="signin"], a[href*="signup"], a[href*="register"]'),
  has_ecommerce: !!document.querySelector('[class*="cart"], [class*="product"], [class*="shop"]'),
  has_blog: !!document.querySelector('a[href*="blog"], a[href*="article"], a[href*="news"]'),
})
EVALEOF
```

**0b. Determine website type and classify it**:

Based on the reconnaissance above, classify the website into one of these categories (a site may fit multiple):

| Website Type | Key Signals | Primary Goal | Core Metrics |
|---|---|---|---|
| **Content/Blog** | Blog section, articles, tutorials | Reader engagement & return visits | Page views, time on page, pages/session, return visitor rate |
| **SaaS/Tool** | Login/signup, pricing page, app features | User registration → activation → retention | Signup rate, trial-to-paid, feature adoption |
| **E-commerce** | Product pages, cart, checkout | Purchase conversion | Add-to-cart rate, cart abandonment, purchase conversion, AOV |
| **Lead Generation** | Contact forms, demo requests, whitepapers | Form submissions / demo bookings | Form completion rate, lead quality, cost per lead |
| **Portfolio/Showcase** | Project galleries, about page, contact | Contact or inquiry | Contact form submissions, inquiry rate |
| **Documentation/Docs** | API docs, guides, reference pages | Help users find answers | Search usage, page depth, time on page, exit rate from docs |
| **Community/Forum** | User posts, comments, threads | User engagement & content creation | Posts per user, comment rate, return rate |
| **Landing Page** | Single page, strong CTA, no navigation depth | Single conversion action | CTA click rate, conversion rate, bounce rate |

**0c. Infer the primary goals — present to user for confirmation**:

Based on the website type and observed elements, infer and present the **Website Goal Profile** to the user:

> Based on my visit to your site, here's what I understand:
>
> **Website Type**: [e.g., SaaS Tool]
> **Primary Goal**: [e.g., Get users to sign up for free trial and convert to paid]
> **Secondary Goals**: [e.g., Build brand awareness through blog content, provide documentation for retention]
>
> **Intended User Journey** (the path you want users to follow):
> ```
> [e.g., Search/Ad → Landing Page → Explore Features → Sign Up → Onboarding → First Value → Upgrade]
> ```
>
> **Key Conversion Points** I'll focus on:
> 1. [e.g., Landing page → Sign up page (acquisition)]
> 2. [e.g., Sign up → Complete onboarding (activation)]
> 3. [e.g., Free trial → Paid plan (monetization)]
>
> Does this match your understanding? Please correct or add anything I missed.
> Also, if you have specific KPIs or targets (e.g., "we want to increase signup rate from 3% to 5%"), please share them.

**0d. Define the analysis dimensions that matter for this site**:

Not all 7 analysis dimensions are equally important for every website type. Based on the goal profile, select and **rank** the applicable dimensions:

| Analysis Dimension | When It Matters Most |
|---|---|
| **Acquisition / SEO** | Sites that depend on organic search traffic (content, SaaS, e-commerce) |
| **Conversion Funnel** | Sites with clear multi-step user journeys (SaaS signup, e-commerce purchase) |
| **Content Engagement** | Content-heavy sites (blogs, docs, tutorials) |
| **User Experience (UX)** | All sites, but especially mobile-first sites or sites with high bounce rates |
| **Performance** | All sites, but critical for e-commerce and landing pages where speed = money |
| **Retention / Return Visits** | SaaS, community, and content sites where repeat visits matter |
| **Technical SEO / GEO** | All sites that need search visibility |

Output a ranked list of dimensions for this specific site, e.g.:
```
Priority analysis dimensions for [site]:
1. Conversion Funnel (SaaS → signup → trial → paid is the core business flow)
2. Acquisition / SEO (organic search is the main traffic channel)
3. Content Engagement (blog is used for top-of-funnel acquisition)
4. UX (mobile bounce rate appears high from initial visit)
5. Performance (site loads well, lower priority)
```

Save the Website Goal Profile to `$DATA_DIR/analysis/website-profile.md`.

**0e. Identify what additional information is needed**:

Based on the goal profile, proactively tell the user what information would help validate hypotheses:

> To give you the most actionable analysis, it would be very helpful if you could tell me:
>
> 1. **Your main traffic sources** — Is most traffic from organic search, paid ads, social media, or direct?
> 2. **Key GA4 events you've set up** — Do you track specific events like `signup`, `purchase`, `add_to_cart`, `form_submit`? (This determines whether I can do funnel analysis)
> 3. **Any known pain points** — Are there specific pages or flows where you suspect users are dropping off?
> 4. **Business context** — Any recent changes (redesign, new content, campaign launches) that might affect the data?
> 5. **Target audience** — Who are your primary users? (This helps interpret geographic and device data)
>
> Don't worry if you can't answer all of these — I'll work with what's available and flag areas where more data would help.

---

### Phase 1: Select Data Source & Collect Data

**1a. Initialize directories**:
```bash
DATA_DIR=".skills-data/google-analytics-and-search-improve"
mkdir -p "$DATA_DIR"/{data,analysis,charts,scripts,cache,logs,tmp}
```

**1b. Ask user to choose data source**:

Present three modes for the user to choose from:

> Choose how to obtain GSC/GA4 data:
>
> **A. API auto-collection** (recommended, most complete data)
> Requires creating a Google Cloud Service Account and configuring API auth. First-time setup takes ~10 minutes; subsequent analyses collect data automatically.
>
> **B. Manual CSV export** (zero config, simplest)
> You export data files from GA4 and GSC web consoles yourself, and I'll analyze them. No API configuration needed.
>
> **C. Browser audit only** (no GA4/GSC data needed)
> I'll visit the site directly for technical auditing and code analysis without using GA4/GSC data. Best for quick technical checks.

Enter the corresponding branch based on user selection:

---

#### Mode A: API Auto-Collection

**Check .env**: Read `$DATA_DIR/.env`; if missing config, guide the user to fill it in.

Configuration required from user (write to `$DATA_DIR/.env` after collection):

| Variable | Description |
|----------|-------------|
| `SITE_URL` | Website URL to audit (e.g., `https://example.com`) |
| `GSC_SITE_URL` | Site address in Search Console (see format note below) |
| `GA4_PROPERTY_ID` | GA4 Property ID (numeric only) |
| `BING_WEBMASTER_API_KEY` | (Optional) Bing Webmaster Tools API key for Bing search data |
| `SOURCE_CODE_PATH` | (Optional) Path to the project source code |
| `PSI_API_KEY` | (Optional) PageSpeed Insights API Key to avoid rate limiting |

**GSC_SITE_URL format note**: GSC has two property types with different formats. The value must match the type registered in GSC, otherwise a 403 permission error will be returned:

| GSC Property Type | GSC_SITE_URL Format | Example |
|-------------------|---------------------|---------|
| **Domain property** | `sc-domain:domain` | `sc-domain:example.com` |
| **URL-prefix property** | Full URL | `https://example.com` |

> How to check: In the [Search Console](https://search.google.com/search-console/) property selector (top-left), if it shows a bare domain name it's a Domain property (use `sc-domain:` prefix); if it shows a full URL it's a URL-prefix property.

Detailed auth setup steps in [references/gsc-api-guide.md](references/gsc-api-guide.md).

```bash
cat > "$DATA_DIR/.env" <<EOF
SITE_URL=provided by user
GSC_SITE_URL=provided by user (note sc-domain: or https:// format)
GA4_PROPERTY_ID=provided by user
BING_WEBMASTER_API_KEY=provided by user (optional, for Bing search data)
SOURCE_CODE_PATH=provided by user
PSI_API_KEY=
EOF
```

**Google Service Account credentials**: Place the Service Account JSON key file in `$DATA_DIR/configs/`. All scripts (`gsc_query.py`, `ga4_query.py`, `ga4_funnel.py`) auto-discover the `*.json` key file from this directory — no need to configure the path in `.env`. If multiple JSON files exist, the first one (alphabetically) is used.

**Collect data** (scripts auto-read auth from .env and configs/):
```bash
set -a; source "$DATA_DIR/.env"; set +a
python scripts/gsc_query.py --dimensions query --limit 500 -o "$DATA_DIR/data/gsc_queries.json"
python scripts/gsc_query.py --dimensions page --limit 500 -o "$DATA_DIR/data/gsc_pages.json"
python scripts/gsc_query.py --dimensions device,country -o "$DATA_DIR/data/gsc_devices.json"
python scripts/gsc_query.py --dimensions date -o "$DATA_DIR/data/gsc_trends.json"
python scripts/gsc_query.py --mode sitemaps -o "$DATA_DIR/data/gsc_sitemaps.json"
python scripts/ga4_query.py --preset traffic_overview -o "$DATA_DIR/data/ga4_traffic.json"
python scripts/ga4_query.py --preset top_pages --limit 100 -o "$DATA_DIR/data/ga4_pages.json"
python scripts/ga4_query.py --preset user_acquisition -o "$DATA_DIR/data/ga4_acquisition.json"
python scripts/ga4_query.py --preset device_breakdown -o "$DATA_DIR/data/ga4_devices.json"
python scripts/ga4_query.py --preset landing_pages --limit 50 -o "$DATA_DIR/data/ga4_landing.json"
python scripts/ga4_query.py --preset user_behavior --limit 100 -o "$DATA_DIR/data/ga4_behavior.json"
python scripts/ga4_query.py --preset conversion_events -o "$DATA_DIR/data/ga4_conversions.json"

# Optional: funnel exploration (if user has custom events for funnel analysis)
# python scripts/ga4_funnel.py --steps "event1,event2,event3" -o "$DATA_DIR/analysis/ga4_funnel.json"

# Optional: Bing Webmaster data (if BING_WEBMASTER_API_KEY is configured)
# python scripts/bing_query.py --mode query_stats -o "$DATA_DIR/data/bing_queries.json"
# python scripts/bing_query.py --mode page_stats -o "$DATA_DIR/data/bing_pages.json"
# python scripts/bing_query.py --mode rank_traffic -o "$DATA_DIR/data/bing_traffic.json"
# python scripts/bing_query.py --mode links -o "$DATA_DIR/data/bing_links.json"
# python scripts/bing_query.py --mode crawl_stats -o "$DATA_DIR/data/bing_crawl.json"
```

First-time use requires installing dependencies:
```bash
python3 -m venv "$DATA_DIR/venv" && source "$DATA_DIR/venv/bin/activate"
pip install -r scripts/requirements.txt
```

Script usage details in [references/gsc-api-guide.md](references/gsc-api-guide.md), [references/ga4-api-guide.md](references/ga4-api-guide.md), and [references/bing-webmaster-api-guide.md](references/bing-webmaster-api-guide.md).

---

#### Mode B: Manual CSV Export

Send the following export instructions to the user, asking them to place files in `$DATA_DIR/data/`:

> **Export GSC data**:
> 1. Open [Google Search Console](https://search.google.com/search-console/) → Select your site
> 2. Click "Search results" (Performance) in the left menu
> 3. Set date range to last 3 months, click "Export" → "Download CSV"
> 4. Save the downloaded CSV as `$DATA_DIR/data/gsc_export.csv`
>
> **Export GA4 data (export the following reports)**:
> 1. Open [Google Analytics](https://analytics.google.com/) → Select your property
> 2. Export "Pages and screens" report:
>    - Left menu: "Reports" → "Engagement" → "Pages and screens"
>    - Click the share icon (top-right) → "Download file" → CSV
>    - Save as `$DATA_DIR/data/ga4_pages.csv`
> 3. Export "Traffic acquisition" report:
>    - Left menu: "Reports" → "Acquisition" → "Traffic acquisition"
>    - Export CSV → Save as `$DATA_DIR/data/ga4_acquisition.csv`
> 4. Export "Landing pages" report:
>    - Left menu: "Reports" → "Engagement" → "Landing pages"
>    - Export CSV → Save as `$DATA_DIR/data/ga4_landing.csv`
>
> Let me know when the export is complete, and I'll read the files to start analysis.

Also ask the user for:
- **Target website URL** (required, write to `SITE_URL` in `$DATA_DIR/.env`)
- **Source code path** (optional, write to `SOURCE_CODE_PATH`)

After receiving files, read CSV files from `$DATA_DIR/data/` and proceed to Phase 2-3 analysis.

---

#### Mode C: Browser Audit Only

Only ask the user for:
- **Target website URL** (required)
- **Source code path** (optional)

Write to `$DATA_DIR/.env` and skip directly to Phase 4 (site audit) and Phase 5 (source code review), skipping Phase 2-3.

---

### Phase 2: GSC Data Analysis (Goal-Aligned)

Read GSC data (JSON or CSV) from `$DATA_DIR/data/`. **Before analyzing, review the Website Goal Profile from `$DATA_DIR/analysis/website-profile.md`** to focus on what matters for this site.

Analyze according to the "SEO" dimension thresholds in [references/metrics-glossary.md](references/metrics-glossary.md).

**Goal-aligned analysis approach**:

1. **Map search queries to user intent stages**: Classify top queries by which stage of the intended user journey they serve:
   - **Awareness**: Brand-unaware, problem-related queries (e.g., "how to compress images")
   - **Consideration**: Comparison/evaluation queries (e.g., "best image compressor", "tool A vs tool B")
   - **Decision**: Brand/product queries (e.g., "[product name] pricing", "[product name] review")
   - **Retention**: Support/usage queries (e.g., "[product name] how to export", "[product name] API docs")

2. **Check if the right pages rank for the right queries**: Cross-reference query intent with the landing pages — are users arriving at the stage-appropriate page, or are they landing on irrelevant pages?

3. **Standard SEO diagnostics**:
   - High-impression low-CTR keywords (best targets for title/description optimization)
   - Keywords ranked 4-10 (highest ROI to push into top 3)
   - Pages with declining ranking trends
   - Index coverage and sitemap health status

**Output**: Top 10 SEO optimization opportunities, **organized by user journey stage**, with data evidence and connection to site goals. Save to `$DATA_DIR/analysis/gsc_analysis.md`.

**Charts**: Generate all Phase 2 required charts (see [Data Visualization → Required Charts per Phase](#required-charts-per-phase)) by writing and executing a Python script. Save chart PNGs to `$DATA_DIR/charts/gsc_*.png` and embed them in the analysis report using relative paths (`../charts/gsc_*.png`).

#### Custom GSC Queries for Targeted Analysis

Beyond the standard Phase 1 data collection, GSC can serve as a powerful auxiliary analysis tool for deeper investigation. When the standard aggregated data is insufficient, write targeted queries to drill down into specific page sections, track daily trends for particular queries, or cross-filter dimensions.

**When to use custom GSC queries**:
- Standard Phase 1/Phase 2 data reveals an area that needs deeper investigation (e.g., a page group with anomalous metrics)
- The user asks about a specific subset of pages or queries (e.g., "How are my /3d/ tool pages performing in search?")
- You need to filter, segment, or cross-reference dimensions that the standard data collection didn't cover

**How to build custom queries**:

Use [scripts/gsc_query.py](scripts/gsc_query.py) for standard dimension/date queries. For advanced filtering (e.g., `dimensionFilterGroups`), write a custom script following the GSC Search Analytics API patterns documented in [references/gsc-api-guide.md](references/gsc-api-guide.md). Key capabilities:

- **Dimension filtering**: Filter results by any dimension — page path patterns, query keywords, country, device — using operators like `contains`, `equals`, `includingRegex`, etc.
- **Cross-dimension filtering**: Filter on a dimension that is not in the `dimensions` list (e.g., group by `query` + `date` while filtering on `page`)
- **Fresh data access**: Use `dataState: 'all'` to include preliminary data from the last 1-2 days for near-real-time monitoring
- **Pagination**: Retrieve up to 25,000 rows per request; paginate with `startRow` for larger datasets
- **Multi-condition filters**: Combine multiple filters within a group using AND logic

**Common analysis scenarios**:

1. **Section-specific analysis**: Filter by page path to isolate a site section (e.g., `/blog/`, `/tools/`, `/docs/`) and analyze its search performance independently
2. **Query trend tracking**: Group by `query` + `date` with a page filter to track daily performance trends for queries landing on specific pages
3. **Long-tail keyword discovery**: Query with high `rowLimit` to surface long-tail queries you rank for but may not appear in the top-level aggregation
4. **Country-specific page performance**: Filter by country and group by page to find geo-specific ranking opportunities
5. **Regex-based pattern matching**: Use `includingRegex` operator to match complex URL or query patterns across the site

**Integration with the analysis workflow**: Save custom query output to `$DATA_DIR/data/gsc_*.json` and reference it in Phase 2 analysis or directly in the Phase 6 improvement report. Custom query data supplements (not replaces) the standard data collection.

#### Bing Webmaster Data Analysis (Optional)

When `BING_WEBMASTER_API_KEY` is configured in `.env`, include Bing search data in the analysis. This is especially important when Bing is a significant traffic source (check GA4 acquisition data for Bing's share).

**Collect Bing data** (if not already done in Phase 1):
```bash
set -a; source "$DATA_DIR/.env"; set +a
python scripts/bing_query.py --mode query_stats -o "$DATA_DIR/data/bing_queries.json"
python scripts/bing_query.py --mode page_stats -o "$DATA_DIR/data/bing_pages.json"
python scripts/bing_query.py --mode rank_traffic -o "$DATA_DIR/data/bing_traffic.json"
python scripts/bing_query.py --mode links -o "$DATA_DIR/data/bing_links.json"
```

**Bing-specific analysis approach**:

1. **Cross-engine comparison**: Compare Bing query/page performance with GSC data to identify:
   - Queries where the site ranks well on Bing but poorly on Google (or vice versa) — these reveal search engine-specific optimization opportunities
   - Pages with disproportionate Bing vs Google traffic — may indicate content preferences or algorithmic differences
   - Overall traffic distribution across search engines (from GA4 acquisition data)

2. **Bing-unique insights** (capabilities GSC doesn't have):
   - **Keyword research**: Use `keyword` and `related_keywords` modes to discover keyword volume and expansion opportunities on Bing
   - **Backlink analysis**: Use `links` mode to review inbound link profile as seen by Bing
   - **Crawl health**: Use `crawl_stats` mode to monitor Bing's crawl frequency and identify crawl issues

3. **Deep-dive into specific queries or pages**:
   - Use `query_detail` mode to get detailed stats for a high-value query
   - Use `page_detail` mode to see all queries driving Bing traffic to a key page
   - Use `query_page_detail` mode for granular query + page combination analysis

**Output**: Include Bing analysis as a subsection in `$DATA_DIR/analysis/gsc_analysis.md` (under a "## Bing Search Performance" heading), or as a separate file `$DATA_DIR/analysis/bing_analysis.md` if Bing is a major traffic source.

**Charts**: Generate Bing-specific charts (e.g., `bing_top_queries.png`, `bing_traffic_trend.png`, `bing_vs_google.png`) and save to `$DATA_DIR/charts/bing_*.png`.

> **Data retention warning**: Bing only retains 6 months of data. If historical comparison is needed, set up regular data collection (e.g., monthly) to build your own data archive.

Script details in [references/bing-webmaster-api-guide.md](references/bing-webmaster-api-guide.md).

---

### Phase 3: GA4 Data Analysis (Goal-Aligned)

Read GA4 data (JSON or CSV) from `$DATA_DIR/data/`. **Before analyzing, review the Website Goal Profile from `$DATA_DIR/analysis/website-profile.md`** to interpret data through the lens of site goals.

Analyze according to "Content Strategy", "User Experience", and "Conversion Rate" dimension thresholds in [references/metrics-glossary.md](references/metrics-glossary.md).

**Goal-aligned analysis approach**:

1. **Intended Journey vs Actual Behavior**: Compare the user journey defined in Phase 0 with what GA4 data reveals:
   - **Landing page alignment**: Are users entering the site at the intended entry points? Which landing pages receive the most traffic, and do they match the journey's starting point?
   - **Path progression**: Do users move from landing pages to the next expected step (e.g., features → pricing → signup), or do they exit or wander?
   - **Conversion point performance**: For each key conversion point defined in Phase 0, what is the actual conversion rate? Where is the biggest drop-off?

2. **Identify behavior gaps** (where reality diverges from intention):
   - Pages with high traffic but **not leading to the next journey step** (dead-end pages)
   - Key journey pages with **unexpectedly low traffic** (users aren't reaching them)
   - High-traffic pages with **high bounce rate** (users arrive but don't engage)
   - **Device/channel disparities**: Is the journey broken on specific devices or for traffic from specific channels?

3. **Standard GA4 diagnostics**:
   - Traffic trends and channel effectiveness
   - High-traffic low-engagement / high-bounce-rate pages
   - Mobile vs desktop experience gaps
   - Conversion event analysis

4. **Flag what data is missing**: If the analysis reveals gaps that available data can't explain, explicitly tell the user what additional data or information would help:
   > I noticed that [X page] has a 75% bounce rate but I can't tell why from the data alone. It would help if you could:
   > - Check if you have heatmap data (e.g., Hotjar/Clarity) for this page
   > - Tell me if there were recent content changes to this page
   > - Consider adding a [specific GA4 event] to track [specific interaction]

**Output**: Top 10 GA4 insights, **framed as "expected behavior vs actual behavior"** with gap analysis and data evidence. Save to `$DATA_DIR/analysis/ga4_analysis.md`.

**Charts**: Generate all Phase 3 required charts (see [Data Visualization → Required Charts per Phase](#required-charts-per-phase)) by writing and executing a Python script. Save chart PNGs to `$DATA_DIR/charts/ga4_*.png` and embed them in the analysis report using relative paths (`../charts/ga4_*.png`).

---

### Phase 3b: GA4 Funnel Exploration (Optional)

If the user has custom events and wants funnel/conversion analysis, use `ga4_funnel.py` to generate funnel reports. This uses the GA4 Data API **v1alpha** (`AlphaAnalyticsDataClient`).

> **When to run this phase**: Ask the user if they have custom events they'd like to analyze as a funnel (e.g., signup flow, purchase flow, onboarding steps). Skip if the user has no custom events or doesn't need funnel analysis.

**Quick funnel** (user provides event names):
```bash
set -a; source "$DATA_DIR/.env"; set +a
python scripts/ga4_funnel.py \
    --steps "page_view,signup_click,signup_complete,first_purchase" \
    --step-names "View Page,Click Signup,Complete Signup,First Purchase" \
    -o "$DATA_DIR/analysis/ga4_funnel.json"
```

**Funnel with device breakdown**:
```bash
python scripts/ga4_funnel.py \
    --steps "page_view,signup_click,signup_complete" \
    --breakdown deviceCategory \
    -o "$DATA_DIR/analysis/ga4_funnel_by_device.json"
```

**Trended funnel** (daily trends):
```bash
python scripts/ga4_funnel.py \
    --steps "page_view,purchase" \
    --trended --start-date 30daysAgo \
    -o "$DATA_DIR/analysis/ga4_funnel_trend.json"
```

**Advanced funnel** (JSON config for complex filters):
```bash
python scripts/ga4_funnel.py --config "$DATA_DIR/configs/funnel_config.json" \
    -o "$DATA_DIR/analysis/ga4_funnel_advanced.json"
```

Key outputs:
- Step-by-step completion rates and abandonment rates
- Drop-off points in the conversion funnel
- Device/channel/geo breakdown of funnel performance
- Daily trends showing funnel health over time

Script details in [references/ga4-exploration-api-guide.md](references/ga4-exploration-api-guide.md).

> **API version note**: `ga4_funnel.py` uses the v1alpha API (`AlphaAnalyticsDataClient`). This API is in early preview — functional but may have breaking changes. No additional auth setup is needed beyond the existing Service Account.

> **Path exploration**: GA4's path exploration has **no API support**. For user path analysis, use the GA4 web UI directly or query raw event data via BigQuery export.

**Output**: Funnel conversion analysis with per-step metrics and improvement recommendations. Save to `$DATA_DIR/analysis/funnel_analysis.md`.

**Charts**: Generate all Phase 3b required charts (see [Data Visualization → Required Charts per Phase](#required-charts-per-phase)) by writing and executing a Python script. Save chart PNGs to `$DATA_DIR/charts/funnel_*.png` and embed them in the analysis report using relative paths (`../charts/funnel_*.png`).

---

### Phase 4: Live Site Audit

Use `agent-browser` to visit `$SITE_URL`:

```bash
agent-browser open "$SITE_URL" && agent-browser wait --load networkidle
agent-browser screenshot --full homepage_desktop.png
agent-browser set viewport 375 812
agent-browser screenshot --full homepage_mobile.png
agent-browser set viewport 1280 720
```

Save screenshots to `$DATA_DIR/tmp/`.

PageSpeed Insights performance audit (auto-appends `PSI_API_KEY` from .env if present):
```bash
PSI_BASE="https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$SITE_URL&category=PERFORMANCE&category=SEO&category=ACCESSIBILITY&category=BEST_PRACTICES"
PSI_KEY_PARAM="${PSI_API_KEY:+&key=$PSI_API_KEY}"
curl -s "${PSI_BASE}&strategy=mobile${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_mobile.json"
curl -s "${PSI_BASE}&strategy=desktop${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_desktop.json"
```

> **PSI failure fallback**: If a 429 (quota exceeded) or other error is returned, check whether "PageSpeed Insights API" has been enabled in the Google Cloud project (see [references/gsc-api-guide.md](references/gsc-api-guide.md) Step 1). When PSI data is missing, continue with subsequent phases and note the missing performance data in the report.

Extract Core Web Vitals from PSI; thresholds in the "Performance" dimension of [references/metrics-glossary.md](references/metrics-glossary.md).

If GA4 data is available, take screenshots (desktop + mobile) for each of the Top 10 landing pages, recording visual and interaction issues.

When no source code is available, extract front-end metadata via browser:
```bash
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify({
  title: document.title,
  meta_desc: document.querySelector('meta[name="description"]')?.content,
  h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent),
  has_jsonld: document.querySelectorAll('script[type="application/ld+json"]').length,
  images_no_alt: document.querySelectorAll('img:not([alt])').length,
  viewport: document.querySelector('meta[name="viewport"]')?.content,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
})
EVALEOF
```

**Output**: Performance scores + visual issue checklist. Save to `$DATA_DIR/analysis/site_audit.md`.

**Charts**: Generate all Phase 4 required charts (see [Data Visualization → Required Charts per Phase](#required-charts-per-phase)) by writing and executing a Python script. Save chart PNGs to `$DATA_DIR/charts/audit_*.png` and embed them in the analysis report using relative paths (`../charts/audit_*.png`).

---

### Phase 5: Source Code Review

If `SOURCE_CODE_PATH` is configured in `.env`, analyze project source code. Skip if no source code is available.

Check items detailed in the "Technical Issues" checklist in [references/metrics-glossary.md](references/metrics-glossary.md). Core focus:

- **SEO**: Meta tag completeness, JSON-LD, robots.txt / sitemap.xml, image alt, H1 conventions
- **Performance**: JS/CSS splitting and lazy loading, image formats and responsive images, third-party scripts, render-blocking resources
- **Technical**: `<html lang>`, viewport, HTTPS, canonical URL, internal dead links

**Output**: Code-level improvement checklist. Save to `$DATA_DIR/analysis/code_review.md`.

---

### Phase 5b: SEO & GEO Optimization Checklist Audit

Run through the SEO & GEO optimization checklist in [references/SEO-GEO-Optimization-Checklist.md](references/SEO-GEO-Optimization-Checklist.md) to evaluate the site's search engine and generative AI readiness.

**Run the audit scripts** to collect data automatically:

```bash
set -a; source "$DATA_DIR/.env"; set +a

# SEO audit — JSON-LD, meta tags, headings, sitemap, Open Graph, canonical, hreflang
python scripts/seo_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/seo_audit.json"

# GEO audit — llms.txt, robots.txt AI crawlers, content depth, question headings, FAQ/HowTo schemas
python scripts/geo_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/geo_audit.json"

# Performance audit — load time, compression, HSTS, HTML size, TLS, CDN detection
python scripts/perf_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/perf_audit.json"
```

Each script supports:
- `--url URL` — target site (or reads `SITE_URL` from `.env`)
- `--sitemap` — audit all pages from sitemap.xml
- `--pages "/path1,/path2"` — audit specific pages
- `--max-pages N` — limit pages when using `--sitemap`
- `-o FILE` — write JSON report to file (default: stdout)

The scripts check the following categories against the target site:

1. **Structured Data (JSON-LD)** (`seo_audit.py`): Coverage, SSR output, schema types, content uniqueness
2. **Meta Tags & Open Graph** (`seo_audit.py`): Title/description length, canonical, hreflang, og:image, Twitter Card
3. **Heading Structure** (`seo_audit.py`): H1 count, question-style heading ratio (GEO signal)
4. **Sitemap** (`seo_audit.py`): Presence, page count, lastmod, robots.txt declaration
5. **AI Readability (GEO)** (`geo_audit.py`): llms.txt/llms-full.txt, robots.txt AI crawler rules (GPTBot, ClaudeBot, etc.)
6. **Content Depth** (`geo_audit.py`): Word count (CJK-aware), intro summary detection, FAQ/HowTo sections, schema presence
7. **Performance** (`perf_audit.py`): Load time (FCP proxy), compression (Brotli/gzip), HTML size, CDN detection
8. **Security** (`perf_audit.py`): HSTS, HTTPS, CSP, X-Frame-Options, Cache-Control

For any items not covered by the scripts (e.g. off-page authority, visual content review), use the detection commands in Section 7 of the checklist reference.

**Output**: SEO/GEO readiness checklist with pass/fail status for each item and specific improvement recommendations, classified by the P0-P3 priority matrix in Section 8 of the checklist. Save to `$DATA_DIR/analysis/seo_geo_checklist.md`.

---

### Phase 6: Generate Goal-Aligned Improvement Report

Organize output around the **website goals defined in Phase 0**, using the "Priority Matrix" (P0-P3) in [references/metrics-glossary.md](references/metrics-glossary.md). Use the following template:

```markdown
# Website Data Analysis & Improvement Plan

## Website Profile
- **Target Website**: [URL]
- **Website Type**: [e.g., SaaS Tool / E-commerce / Content Blog]
- **Primary Goal**: [e.g., Convert visitors to paid subscribers]
- **Intended User Journey**: [Journey defined in Phase 0]
- **Data Source**: API auto-collection / Manual CSV export / Browser audit only
- **Analysis Period**: [start_date] ~ [end_date]

## Executive Summary
[2-3 sentences: What the site wants to happen vs. what's actually happening, and the single biggest opportunity]

![Executive Summary Dashboard](../charts/report_executive_dashboard.png)

## Goal Achievement Status

### Primary Goal: [goal name]

![Goal Achievement Scorecard](../charts/report_goal_scorecard.png)

| Journey Stage | Expected Behavior | Actual Data | Gap | Severity |
|---|---|---|---|---|
| [e.g., Landing → Features] | Users explore features after landing | 68% bounce rate on landing page | Users leave immediately | 🔴 Critical |
| [e.g., Features → Signup] | Users proceed to signup | Only 2% click signup CTA | Very low progression | 🔴 Critical |
| [e.g., Signup → Onboarding] | Users complete onboarding | 45% complete (if data available) | Moderate drop-off | 🟡 Moderate |

### Secondary Goals
(Same format for each secondary goal)

## Data Overview

![Traffic Trend](../charts/ga4_traffic_trend.png)

| Metric | Current Value | Trend | Interpretation |
|--------|---------------|-------|----------------|
| GSC Total Impressions / Clicks / CTR / Position | ... | ... | [How this relates to goals] |
| GA4 Sessions / Users / Bounce Rate / Engagement Rate | ... | ... | [How this relates to goals] |
| PSI Performance Score (Mobile/Desktop) | ... | ... | [Impact on user journey] |

![Device Comparison](../charts/ga4_device_comparison.png)

## Key Findings: Where Users Diverge from the Intended Journey

![Journey Gap Analysis](../charts/ga4_journey_gap.png)

1. **[Finding]** — Data evidence → Impact on goal → Recommended fix
2. ...
(Ordered by impact on primary goal, not by analysis dimension)

## Improvement Plan

![Priority Distribution](../charts/report_priority_distribution.png)

### P0 Critical (Directly blocks primary goal)
1. **[Issue]** — Data evidence / Fix / Expected impact on goal

### P1 High (Significantly impacts goal achievement)
### P2 Medium (Supports goal but not on the critical path)
### P3 Low (Nice to have)

## What Data Is Missing
| Question I Can't Answer | Why It Matters | How to Get This Data |
|---|---|---|
| [e.g., Why do users leave the pricing page?] | [It's the biggest funnel drop-off] | [Add heatmap tracking / Set up exit-intent survey] |

## Next Steps & Strategy
### Immediate Actions (This Week)
1. [Specific, actionable item tied to P0 finding]

### Short-term Strategy (This Month)
1. [Specific item tied to P1 findings]

### Medium-term Strategy (Next Quarter)
1. [Items requiring more effort, tied to P2-P3]

### Data Collection Improvements
1. [Specific events/tracking to add for better analysis next time]

## Detailed Analysis
(Organized by the priority dimensions from Phase 0:
e.g., Conversion Funnel → Acquisition/SEO → Content Engagement → UX → Performance → Technical → SEO/GEO Checklist)

[Embed relevant charts from Phase 2-4 in each subsection. Reuse chart files — do not regenerate.]

## Execution Roadmap
| Phase | Timeline | Tasks | Expected Outcome | How to Verify |
|-------|----------|-------|------------------|---------------|
| Week 1-2 | P0 | ... | ... | [Specific metric to check] |
| Week 3-4 | P1 | ... | ... | [Specific metric to check] |
| Month 2+ | P2-P3 | ... | ... | [Specific metric to check] |
```

**Charts**: Generate all Phase 6 required charts (see [Data Visualization → Required Charts per Phase](#required-charts-per-phase)) — the executive dashboard (2×2 subplot), goal scorecard, and priority distribution chart. Save to `$DATA_DIR/charts/report_*.png`. Reuse Phase 2-4 chart images in the Detailed Analysis section by referencing the same file paths.

Save the report to `$DATA_DIR/analysis/improvement-report.md`.

## Companion Skills

- SEO implementation → `seo-geo`
- Browser automation → `agent-browser`
- Frontend redesign → `frontend-design`

## Reference Docs

| Document | Contents |
|----------|----------|
| [references/gsc-api-guide.md](references/gsc-api-guide.md) | GSC auth setup (step-by-step), script usage, dimensions & metrics |
| [references/ga4-api-guide.md](references/ga4-api-guide.md) | GA4 auth setup, preset templates, dimensions & metrics |
| [references/ga4-exploration-api-guide.md](references/ga4-exploration-api-guide.md) | GA4 Exploration API coverage, funnel exploration script usage, JSON config format, output format |
| [references/bing-webmaster-api-guide.md](references/bing-webmaster-api-guide.md) | Bing Webmaster API auth setup, script usage, modes & metrics, GSC comparison, keyword research |
| [references/metrics-glossary.md](references/metrics-glossary.md) | Six analysis dimensions: thresholds, diagnostics, priority matrix |
| [references/SEO-GEO-Optimization-Checklist.md](references/SEO-GEO-Optimization-Checklist.md) | SEO & GEO optimization checklist: structured data, AI readability, content depth, technical SEO, performance, off-page authority, detection commands, priority matrix |
