# SEO & GEO Optimization Checklist

> **Purpose**: Reference document for the AI agent to audit any website's SEO (Search Engine Optimization) and GEO (Generative Engine Optimization) readiness.
> **Core principle**: SEO optimizes rankings; GEO optimizes AI citations. They are complementary, not competing.
> **Variable**: All commands below use `$SITE_URL` — the target website URL from `.env`.

---

## Table of Contents

- [1. Structured Data (JSON-LD)](#1-structured-data-json-ld)
- [2. AI Readability (GEO Core)](#2-ai-readability-geo-core)
- [3. Page Content Depth](#3-page-content-depth)
- [4. Technical SEO Basics](#4-technical-seo-basics)
- [5. Page Performance](#5-page-performance)
- [6. Off-page Authority Building](#6-off-page-authority-building)
- [7. Detection Commands](#7-detection-commands)
- [8. Priority Overview](#8-priority-overview)

---

## 1. Structured Data (JSON-LD)

### 1.1 Recommended JSON-LD Types

Select the types applicable to the target site. Not every site needs all types — choose based on site category.

| @type | Applicable Pages | Purpose | Check Points |
|-------|-----------------|---------|-------------|
| **WebSite** | All pages | Site-wide info with search box | Localize for each language version |
| **Organization** | All pages | Organization info (name, logo, contact) | `inLanguage` must match page language |
| **WebPage** | All pages | Current page info | Include `speakable` (voice search) and `dateModified` |
| **BreadcrumbList** | All pages | Breadcrumb navigation | Multi-level paths, e.g. `Home > Category > Page` |
| **SoftwareApplication** | Tool/product pages | Tool/product description | Each page must have unique content, not templated |
| **FAQPage** | Content/tool pages | FAQ section | 3-5 targeted Q&As matching user search intent per page |
| **ItemList** | Category/listing pages | List items in a category | Helps search engines understand page hierarchy |
| **HowTo** | Tutorial/tool pages | Step-by-step guide | 3-5 steps; can trigger Google rich snippets |
| **Article** | Blog/article pages | Article metadata | Include author, datePublished, dateModified |
| **Product** | E-commerce pages | Product info | Include price, availability, reviews |
| **LocalBusiness** | Local business sites | Location info | Include address, hours, phone |

### 1.2 Checklist

- [ ] **Coverage**: All indexable pages have at least WebSite + WebPage + BreadcrumbList JSON-LD
- [ ] **SSR output**: JSON-LD is rendered server-side in the HTML (some crawlers don't execute JS)
- [ ] **Content uniqueness**: Each page has distinct `name`, `description`, and FAQ content
- [ ] **Localization**: Multi-language sites have localized JSON-LD for each language version
- [ ] **Language tag**: `inLanguage` field is correct (e.g. `en-US`, `zh-CN`)
- [ ] **URL consistency**: `url` in JSON-LD matches the canonical URL

### 1.3 Common Pitfalls

| Problem | Symptom | Solution |
|---------|---------|---------|
| SSR empty shell | Page returns `<meta http-equiv="refresh">` self-redirect with no real content | Check SSG/SSR pre-rendering config (Nuxt/Next/Astro), ensure routes are correctly built |
| Trailing slash mismatch | `/page` returns 301 → `/page/`, causing crawl issues | Unify URL format; use `curl -sL` (follow redirects) when testing |
| Unlocalized JSON-LD | Non-English pages still have English WebSite/Organization | Configure localized JSON-LD blocks for each language in i18n setup |
| Duplicate content | Multiple pages share identical JSON-LD name/description | Generate page-specific structured data from actual page content |

---

## 2. AI Readability (GEO Core)

### 2.1 llms.txt File (P0 — Must Do)

> `llms.txt` is a standard proposed by Jeremy Howard in 2024, adopted by Anthropic, Mintlify and others. It provides AI crawlers with a curated site map.

- [ ] **`/llms.txt`**: Summary version — site overview + categorized page list with links and one-line descriptions
- [ ] **`/llms-full.txt`**: Full version — each page with URL + detailed description + use cases + technical details
- [ ] **robots.txt reference**: Add `Llms-txt: https://yoursite.com/llms.txt` at the end of robots.txt

**llms.txt template**:

```markdown
# Site Name

> One-line description of the site's purpose and core value

- Key feature 1
- Key feature 2
- Site URL

## Category 1
- [Page Name](URL): One-line description

## Category 2
- [Page Name](URL): One-line description

## Optional
- [Secondary Content](URL): Description
```

**llms-full.txt template**:

```markdown
# Site Name — Complete Reference

> Detailed description

## Overview
- Total pages/tools, privacy model, tech stack, supported languages, etc.

## Category (N items)

### Page/Tool Name
- **URL**: https://...
- **Description**: Detailed description (include technical details)
- **Use cases**: Usage scenario list

## Technical Details
- Tech stack, processing methods, i18n, SEO config, etc.

## Contact
- Contact info
```

### 2.2 robots.txt AI Crawler Configuration

- [ ] Explicitly allow major AI crawlers:

```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /
```

- [ ] Avoid over-restriction: A single `Allow: /` per bot is sufficient

### 2.3 H2/H3 Heading Format (Question-style)

> AI engines pattern-match headings against user queries. Question-style headings are cited far more often than declarative ones.

- [ ] Convert declarative headings to question format:

| ❌ Declarative | ✅ Question-style |
|---------------|------------------|
| `Features` | `What Makes This Tool Different?` |
| `Getting Started` | `How to Get Started with [Product]?` |
| `Pricing` | `How Much Does [Product] Cost?` |
| `Related Tools` | `What Other Tools Are Available?` |

### 2.4 HowTo Schema + Visible Step Content

- [ ] Pages with tutorials or workflows should have `HowTo` JSON-LD (3-5 steps)
- [ ] Steps must also be **visually present** on the page (not just in JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [Action]",
  "step": [
    {"@type": "HowToStep", "position": 1, "name": "Step 1 Title", "text": "Step 1 description..."},
    {"@type": "HowToStep", "position": 2, "name": "Step 2 Title", "text": "Step 2 description..."},
    {"@type": "HowToStep", "position": 3, "name": "Step 3 Title", "text": "Step 3 description..."}
  ]
}
```

---

## 3. Page Content Depth

### 3.1 Word Count Targets

> 2026 GEO research consistently shows: AI engines prefer reference-grade content. Content with statistics and cited sources gets 30-40% more AI citations.

- [ ] Target **800-1200 words** per key page (excluding navigation and footer)
- [ ] Detection method: see [Detection Commands](#7-detection-commands)

### 3.2 Recommended Content Structure

| Content Block | Description | Target Words |
|--------------|-------------|:----------:|
| **TL;DR Paragraph** | Top of page — directly answers "what is this, what does it do" | 100 |
| **How to Use** | 3-5 step guide, paired with HowTo Schema | 200 |
| **Technical Details** | Technical principles (algorithms, architecture, privacy model) | 200 |
| **Use Cases / Scenarios** | Usage scenarios: "ideal for designers", "perfect for developers" | 150 |
| **Comparison** | Competitive comparison (features, pros/cons) | 150 |
| **FAQ** | 3-5 targeted questions matching user search intent | 200 |

### 3.3 Key Principles

- [ ] **First 200 words must directly answer the core question** (TL;DR-first principle)
- [ ] One deep guide > ten shallow pages
- [ ] Include specific data and cited sources (e.g. "reduces size by 70%", "based on WebAssembly")
- [ ] Avoid pure feature lists — add explanatory content

---

## 4. Technical SEO Basics

### 4.1 Meta Tags

- [ ] **title**: 50-60 characters, include core keyword, avoid truncation
- [ ] **description**: 150-160 characters, include call to action
- [ ] **canonical**: Every page has a unique canonical URL
- [ ] **hreflang**: Multi-language pages correctly configured (`<link rel="alternate" hreflang="zh" href="...">`)

### 4.2 Open Graph & Social

- [ ] **og:title**: Unique per page
- [ ] **og:description**: Unique per page
- [ ] **og:image**: Each page uses a distinct social share image (with page title and brief description)
- [ ] **Twitter Card**: Correctly set `twitter:card`, `twitter:title`, etc.

### 4.3 Sitemap

- [ ] sitemap.xml includes all indexable pages (separate by language if multi-language)
- [ ] Each URL has a `<lastmod>` date
- [ ] Sitemap declared in robots.txt

### 4.4 URL Structure

- [ ] Consistent trailing slash strategy (recommend always with `/`)
- [ ] URLs use lowercase English with hyphens
- [ ] Avoid deep nesting (recommend no more than 3 levels)

### 4.5 Security & Trust

- [ ] **HSTS Header**: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- [ ] **HTTPS**: Enforced site-wide
- [ ] These factors affect E-E-A-T trust scores

### 4.6 Content Freshness

- [ ] Page displays a **visible** `Last Updated` date (not just in JSON-LD)
- [ ] `dateModified` in JSON-LD matches the actual update date

### 4.7 IndexNow

- [ ] Integrate IndexNow protocol (supported by Bing/Yandex)
- [ ] Automatically notify search engines on content updates for faster indexing

---

## 5. Page Performance

### 5.1 Loading Speed

> 2026 GEO research: Pages with FCP < 0.4s average 6.7 AI citations; pages > 1.13s average only 2.1. Fast pages are cited 3x more.

- [ ] **FCP (First Contentful Paint)**: Target < 0.4s
- [ ] **TLS optimization**: Enable OCSP Stapling, stable TLS Session Ticket reuse
- [ ] **Compression**: Enable Brotli compression (better than gzip)
- [ ] **CDN**: Use CDN for static assets (e.g. CloudFlare, Fastly)
- [ ] **HTML size**: Keep under 100KB, consider code splitting

### 5.2 Detection Method

```bash
# Page load time
curl -sL -o /dev/null -w "Total: %{time_total}s\nTLS: %{time_appconnect}s\nFCP proxy: %{time_starttransfer}s\n" "$SITE_URL/"

# Compression check
curl -sI -H "Accept-Encoding: gzip, br" "$SITE_URL/" | grep -i 'content-encoding'
```

---

## 6. Off-page Authority Building

> Research shows brands are cited by AI engines via third-party domains 6.5x more often than via their own domain.

### 6.1 Platform Presence

- [ ] **Product Hunt**: Publish a product page
- [ ] **AlternativeTo**: Create an entry benchmarked against competitors
- [ ] **Reddit**: Share in relevant subreddits (r/webdev, r/SideProject, etc.)
- [ ] **GitHub**: Open-source part of the code, link back in README
- [ ] **Wikidata**: Create a product entity
- [ ] **Industry directories**: Submit to relevant niche directories

### 6.2 Comparison Content Pages

> AI search queries average 23 words — much longer than traditional search — and often contain comparison intent.

- [ ] Create `vs` comparison pages (e.g. `/product-vs-competitor/`)
- [ ] Include feature comparison tables and pros/cons analysis

### 6.3 Multi-modal Optimization

- [ ] Add tutorial videos to key pages (YouTube embed + text transcript)
- [ ] All images have descriptive alt text
- [ ] Add `VideoObject` Schema when videos are present

---

## 7. Detection Commands

All commands use `$SITE_URL` from the `.env` file. Replace paths as needed for the target site.

### 7.1 JSON-LD Coverage Check

```bash
# Check JSON-LD count on a specific page
curl -sL "$SITE_URL/" | grep -c 'application/ld+json'

# List JSON-LD types on a page
curl -sL "$SITE_URL/" | \
  grep -o '<script type="application/ld+json">[^<]*</script>' | \
  sed 's/<script type="application\/ld+json">//;s/<\/script>//' | \
  python3 -c "
import sys, json
for i, line in enumerate(sys.stdin, 1):
    line = line.strip()
    if not line: continue
    d = json.loads(line)
    t = d.get('@type','?')
    name = d.get('name','')[:60] if isinstance(d.get('name'), str) else ''
    print(f'  Block {i}: @type={t}  name={name}')
"
```

### 7.2 Sitemap-based Full-site JSON-LD Audit

```bash
# Extract URLs from sitemap and check JSON-LD count on each page
curl -sL "$SITE_URL/sitemap.xml" | \
  grep '<loc>' | sed 's/.*<loc>//;s/<\/loc>.*//' | \
  while read url; do
    count=$(curl -sL "$url" | grep -c 'application/ld+json')
    if [ "$count" -lt 3 ]; then
      echo "⚠️  ${url}: ${count} JSON-LD blocks"
    else
      echo "✅ ${url}: ${count} JSON-LD blocks"
    fi
  done
```

### 7.3 Page Word Count

```bash
curl -sL "$SITE_URL/" | python3 -c "
import sys, re
html = sys.stdin.read()
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
words = text.split()
print(f'Total visible text words: {len(words)}')
"
```

### 7.4 SSR Empty Shell Detection

```bash
# Check if pages return real HTML (not empty-shell redirects)
# Healthy pages should be > 10KB; empty shells are typically < 200 bytes
curl -sL "$SITE_URL/" | wc -c
```

### 7.5 llms.txt Check

```bash
echo "=== llms.txt ===" && curl -sL "$SITE_URL/llms.txt" | head -10
echo "=== llms-full.txt ===" && curl -sL "$SITE_URL/llms-full.txt" | wc -l
echo "=== robots.txt reference ===" && curl -sL "$SITE_URL/robots.txt" | grep -i llms
```

### 7.6 Meta Tags Check

```bash
curl -sL "$SITE_URL/" | grep -oE '<meta [^>]+>' | head -20
curl -sL "$SITE_URL/" | grep -o '<title>[^<]*</title>'
curl -sL "$SITE_URL/" | grep -i canonical
curl -sL "$SITE_URL/" | grep -i hreflang
curl -sL "$SITE_URL/" | grep -i 'og:'
curl -sL "$SITE_URL/" | grep -i 'twitter:'
```

### 7.7 Security & Performance Check

```bash
# HSTS
curl -sI "$SITE_URL/" | grep -i 'strict-transport'

# HTTP protocol version
curl -sI "$SITE_URL/" | head -1

# Compression
curl -sI -H "Accept-Encoding: gzip, br" "$SITE_URL/" | grep -i 'content-encoding'

# Load time
curl -sL -o /dev/null -w "Total: %{time_total}s\n" "$SITE_URL/"
```

### 7.8 og:image Uniqueness Check

```bash
# Check if different pages have distinct og:image values
# Replace paths with actual pages from the target site's sitemap
curl -sL "$SITE_URL/" | grep -o 'og:image" content="[^"]*"' | head -1
```

### 7.9 Heading Format Check

```bash
curl -sL "$SITE_URL/" | grep -oE '<h[1-6][^>]*>[^<]*</h[1-6]>'
```

### 7.10 HowTo Schema Check

```bash
curl -sL "$SITE_URL/" | grep -c '"HowTo"'
```

---

## 8. Priority Overview

When generating the SEO/GEO audit section of the improvement report, use this priority matrix to classify findings:

```
Priority    Item                                    Impact    Effort   Est. Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P0 🔴   JSON-LD site-wide coverage + SSR output      ★★★★★   ★★★     1-2 days
P0 🔴   Add llms.txt + llms-full.txt                 ★★★★★   ★☆☆     1 hour
P0 🔴   Increase page content depth                  ★★★★★   ★★★     2-3 days
P0 🔴   Convert H2/H3 to question format             ★★★★☆   ★☆☆     2 hours
P1 🟡   Add HowTo Schema                             ★★★★☆   ★★☆     Half day
P1 🟡   robots.txt AI crawler rules                   ★★★☆☆   ★☆☆     10 min
P1 🟡   Page load speed optimization                  ★★★★☆   ★★★     1-2 days
P1 🟡   og:image uniqueness per page                  ★★★☆☆   ★★☆     Half day
P2 🟢   Visible Last Updated date                     ★★★☆☆   ★☆☆     1 hour
P2 🟢   Title length optimization (50-60 chars)       ★★☆☆☆   ★☆☆     5 min
P2 🟢   HSTS Header                                   ★★☆☆☆   ★☆☆     5 min
P2 🟢   robots.txt reference to llms.txt              ★★☆☆☆   ★☆☆     1 min
P3 🔵   Off-page authority building                    ★★★★★   ★★★     Ongoing
P3 🔵   IndexNow integration                          ★★★☆☆   ★★☆     Half day
P3 🔵   Comparison content pages                       ★★★★☆   ★★★     Ongoing
P3 🔵   Multi-modal optimization (video + transcript)  ★★★☆☆   ★★★     Ongoing
```

---

## References

- [llms.txt Standard Proposal](https://llmstxt.org/) — Jeremy Howard, 2024
- [Google Structured Data Docs](https://developers.google.com/search/docs/appearance/structured-data)
- [Schema.org](https://schema.org/) — Structured data vocabulary
- [IndexNow Protocol](https://www.indexnow.org/)
- GEO Research: *"GEO: Generative Engine Optimization"* (2024)
