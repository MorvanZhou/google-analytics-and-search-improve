# GA4 Exploration API Reference

## API Coverage

GA4's "Explore" section in the web UI offers several exploration types. Their API availability:

| Exploration Type | API Support | Method | API Version | Script |
|---|---|---|---|---|
| **Free-form** | ✅ Fully supported | `runReport` | v1beta (stable) | `ga4_query.py` |
| **Funnel exploration** | ✅ Supported | `runFunnelReport` | v1alpha (early preview) | `ga4_funnel.py` |
| **Path exploration** | ❌ No API | — | — | — |
| **Segment overlap** | ❌ No API | — | — | — |
| **User explorer** | ❌ No API | — | — | — |
| **Cohort exploration** | ❌ No API | — | — | — |
| **User lifetime** | ❌ No API | — | — | — |

> **Note**: `runFunnelReport` is in **v1alpha** (early preview). Google may introduce breaking changes before it reaches beta. The API is fully functional but you should monitor the [Google Analytics API announcements](https://groups.google.com/forum/#!forum/google-analytics-api-notify) for updates.

## Authentication

Funnel reports use the **same Service Account** as `ga4_query.py`. No additional setup is needed if you have already configured:

- `GOOGLE_APPLICATION_CREDENTIALS` — path to Service Account JSON key
- `GA4_PROPERTY_ID` — your GA4 property ID

Both are read from `$DATA_DIR/.env`.

## Free-form Exploration (ga4_query.py)

Free-form explorations map directly to the `runReport` method. The existing `ga4_query.py` already covers this with preset templates and custom dimension/metric queries.

See [ga4-api-guide.md](ga4-api-guide.md) for full documentation.

## Funnel Exploration (ga4_funnel.py)

### Concept

The funnel API lets you define a sequence of steps (events and/or dimension conditions) and tracks how users progress through them. It reports:

- **Active users** at each step
- **Completion rate** (step-over-step)
- **Abandonment count and rate** per step
- Optional **breakdown** by any dimension (device, country, source, etc.)
- Optional **trended view** showing daily trends per step

**Important**: This API creates funnel definitions programmatically at query time. It does **not** read funnels you created in the GA4 web UI — those are stored separately and have no API access.

### Quick Start

```bash
# Simple 3-step funnel
python scripts/ga4_funnel.py \
    --steps "page_view,signup,purchase" \
    -o "$DATA_DIR/data/ga4_funnel.json"

# With custom display names
python scripts/ga4_funnel.py \
    --steps "page_view,signup,purchase" \
    --step-names "View Page,Sign Up,Purchase" \
    -o "$DATA_DIR/data/ga4_funnel.json"
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--property-id ID` | GA4 property ID (or set `GA4_PROPERTY_ID` env) |
| `--steps "e1,e2,e3"` | Comma-separated event names for funnel steps |
| `--step-names "n1,n2,n3"` | Comma-separated display names (must match `--steps` count) |
| `--config FILE` | Path to JSON config file for advanced funnel definitions |
| `--start-date DATE` | Start date (default: `28daysAgo`) |
| `--end-date DATE` | End date (default: `yesterday`) |
| `--open` | Open funnel — users can enter at any step (default: closed) |
| `--breakdown DIM` | Dimension to break down by (e.g. `deviceCategory`) |
| `--trended` | Show trended funnel (daily trend per step) |
| `-o FILE` | Output file path (default: stdout) |

### OR Logic in Steps

Use `|` within a step to match multiple events:

```bash
# Step 1 matches either first_open OR first_visit
python scripts/ga4_funnel.py \
    --steps "first_open|first_visit,page_view,purchase" \
    --step-names "First Touch,View Page,Purchase"
```

### Open vs Closed Funnels

| Type | Behavior | Flag |
|------|----------|------|
| **Closed** (default) | Users must enter at step 1. Only users who complete step 1 are tracked. | (none) |
| **Open** | Users can enter the funnel at any step. Each step is evaluated independently. | `--open` |

### Breakdown Dimension

Add `--breakdown` to segment funnel data by a dimension:

```bash
# See funnel performance by device type
python scripts/ga4_funnel.py \
    --steps "page_view,add_to_cart,purchase" \
    --breakdown deviceCategory

# By traffic source
python scripts/ga4_funnel.py \
    --steps "page_view,signup" \
    --breakdown sessionDefaultChannelGroup
```

### Trended Funnel

Add `--trended` to see how each step performs over time (daily):

```bash
python scripts/ga4_funnel.py \
    --steps "page_view,purchase" \
    --trended --start-date 30daysAgo
```

### Advanced: JSON Config File

For complex funnels with field filters, timing constraints, or mixed conditions, use a JSON config:

```json
{
  "steps": [
    {
      "name": "Organic First Visit",
      "events": ["first_open", "first_visit"],
      "field_filter": {
        "field_name": "firstUserMedium",
        "value": "organic",
        "match_type": "CONTAINS"
      }
    },
    {
      "name": "View Product",
      "events": ["view_item"]
    },
    {
      "name": "Add to Cart",
      "events": ["add_to_cart"],
      "within_duration": "1800s"
    },
    {
      "name": "Purchase",
      "events": ["purchase", "in_app_purchase"],
      "directly_followed_by": true
    }
  ],
  "open": false,
  "breakdown": "deviceCategory",
  "trended": false
}
```

```bash
python scripts/ga4_funnel.py --config funnel_config.json -o funnel_report.json
```

**Config step fields**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Step display name (required) |
| `events` | string[] | Event names — matched with OR logic |
| `field_filter` | object | Dimension field filter: `{field_name, value, match_type}` |
| `field_filter.match_type` | string | `EXACT`, `BEGINS_WITH`, `ENDS_WITH`, `CONTAINS`, `FULL_REGEXP`, `PARTIAL_REGEXP` |
| `directly_followed_by` | bool | If `true`, this step must immediately follow the previous one (no intervening events) |
| `within_duration` | string | Max time from prior step, e.g. `"300s"` (5 minutes) |

**Config top-level fields** (optional, CLI flags override):

| Field | Type | Description |
|-------|------|-------------|
| `open` | bool | Open funnel |
| `breakdown` | string | Breakdown dimension |
| `trended` | bool | Trended funnel |

### Output Format

The JSON output contains two main sections:

```json
{
  "funnel_table": {
    "dimensions": ["funnelStepId", "funnelStepName", ...],
    "metrics": ["activeUsers", "funnelStepCompletionRate", "funnelStepAbandonments", "funnelStepAbandonmentRate"],
    "rows": [
      {
        "funnelStepId": "0",
        "funnelStepName": "View Page",
        "activeUsers": 5000,
        "funnelStepCompletionRate": 0.35,
        "funnelStepAbandonments": 3250,
        "funnelStepAbandonmentRate": 0.65
      }
    ]
  },
  "funnel_visualization": {
    "dimensions": ["funnelStepId", "funnelStepName"],
    "metrics": ["activeUsers"],
    "rows": [...]
  },
  "query": {
    "property_id": "123456789",
    "date_range": {"start": "28daysAgo", "end": "yesterday"},
    "is_open_funnel": false,
    "breakdown": "deviceCategory",
    "trended": false,
    "step_count": 3,
    "steps": ["View Page", "Sign Up", "Purchase"]
  }
}
```

**Key metrics in `funnel_table`**:

| Metric | Description |
|--------|-------------|
| `activeUsers` | Number of users who reached this step |
| `funnelStepCompletionRate` | % of users from this step who advanced to the next step |
| `funnelStepAbandonments` | Number of users who dropped off at this step |
| `funnelStepAbandonmentRate` | % of users who dropped off at this step |

When `--breakdown` is used, rows include the breakdown dimension value. The special value `RESERVED_TOTAL` indicates the total row across all dimension values.

### Sampling

Funnel reports may use data sampling. If the response includes a `"sampling"` key, the data is sampled:

```json
{
  "sampling": [
    {
      "samples_read_count": 500000,
      "sampling_space_size": 5000000
    }
  ]
}
```

This means 500,000 out of 5,000,000 events were sampled (10% sample rate). Results are extrapolated from this sample.

## Path Exploration — No API

Google has **not** released any API for path exploration. To analyze user navigation paths, use one of these alternatives:

1. **GA4 web UI**: Use the path exploration directly in the GA4 Explore section
2. **BigQuery export**: If your GA4 property is linked to BigQuery, query raw event-level data to reconstruct user paths with SQL
3. **Approximate with ga4_query.py**: Query `pagePath` + `eventName` dimensions to get page-level event distributions (not true sequential paths)

## Common Dimensions for Breakdown

| Dimension | Description |
|-----------|-------------|
| `deviceCategory` | Device type (desktop, mobile, tablet) |
| `country` / `city` | Geographic location |
| `sessionDefaultChannelGroup` | Traffic channel (Organic, Direct, Social, etc.) |
| `sessionSource` / `sessionMedium` | Traffic source and medium |
| `operatingSystem` / `browser` | OS and browser |
| `newVsReturning` | New vs returning users |
