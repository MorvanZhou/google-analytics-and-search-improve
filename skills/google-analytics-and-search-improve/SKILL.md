---
name: google-analytics-and-search-improve
description: Analyze website data via Google Search Console API and GA4 Data API, audit live site with browser automation, review project source code, and generate data-driven improvement plans covering SEO, performance, content strategy, UX, conversion rate, and technical issues. Use when user wants to diagnose website problems, improve search rankings, optimize traffic, analyze Google Analytics or Search Console data, audit website performance, or create a data-backed improvement roadmap.
---

# Google Analytics & Search Console 数据分析改进

通过 GSC 和 GA4 数据，结合浏览器审计和源代码分析，生成覆盖六大维度（SEO、性能、内容策略、UX、转化率、技术问题）的改进方案。

## 数据存储

所有运行时数据存放在 `$DATA_DIR`，与技能代码分离。

```
<project_root>/.skills-data/google-analytics-and-search-improve/
  .env        # 配置（认证、URL 等），脚本自动加载
  data/       # GSC/GA4/PSI 数据（JSON 或 CSV）
  tmp/        # 截图等临时文件
  cache/      # API 响应缓存
  logs/       # 执行日志
  venv/       # Python 虚拟环境
```

## 工作流

```
分析进度:
- [ ] Phase 1: 选择数据来源 & 采集数据
- [ ] Phase 2: GSC 数据分析
- [ ] Phase 3: GA4 数据分析
- [ ] Phase 4: 网站实际审计
- [ ] Phase 5: 源代码分析
- [ ] Phase 6: 生成改进报告
```

---

### Phase 1: 选择数据来源 & 采集数据

**1a. 初始化目录**:
```bash
DATA_DIR=".skills-data/google-analytics-and-search-improve"
mkdir -p "$DATA_DIR"/{data,cache,logs,tmp}
```

**1b. 询问用户选择数据来源**:

向用户提供三种模式，让用户选择：

> 请选择 GSC/GA4 数据的获取方式：
>
> **A. API 自动采集**（推荐，数据最全）
> 需要在 Google Cloud 创建 Service Account 并配置 API 认证。首次配置约 10 分钟，之后每次分析可自动采集。
>
> **B. 手动导出 CSV**（零配置，最简单）
> 你自己从 GA4 和 GSC 网页后台导出数据文件，我来分析。不需要任何 API 配置。
>
> **C. 仅浏览器审计**（无需 GA4/GSC 数据）
> 我直接访问网站做技术审计和代码分析，不使用 GA4/GSC 数据。适合快速检查技术问题。

根据用户选择进入对应分支：

---

#### 模式 A：API 自动采集

**检查 .env**：读取 `$DATA_DIR/.env`，如果缺少配置则引导用户填写。

需要用户提供的配置（收集后写入 `$DATA_DIR/.env`）：

| 变量名 | 说明 |
|--------|------|
| `SITE_URL` | 要审计的网站 URL（如 `https://example.com`） |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service Account JSON 密钥文件在本机的**绝对路径** |
| `GSC_SITE_URL` | Search Console 中的网站地址（见下方格式说明） |
| `GA4_PROPERTY_ID` | GA4 Property ID（纯数字） |
| `SOURCE_CODE_PATH` | （可选）项目源代码路径 |
| `PSI_API_KEY` | （可选）PageSpeed Insights API Key，避免限流 |

**GSC_SITE_URL 格式说明**：GSC 有两种网站资源类型，格式不同，必须与用户在 GSC 中注册的类型一致，否则会返回 403 权限错误：

| GSC 资源类型 | GSC_SITE_URL 格式 | 示例 |
|-------------|-------------------|------|
| **网域资源** (Domain property) | `sc-domain:域名` | `sc-domain:example.com` |
| **网址前缀资源** (URL-prefix property) | 完整 URL | `https://example.com` |

> 如何确认：在 [Search Console](https://search.google.com/search-console/) 左上角的网站选择器中查看，如果显示的是纯域名则为网域资源（使用 `sc-domain:` 前缀），如果显示完整 URL 则为网址前缀资源。

认证创建详细步骤见 [references/gsc-api-guide.md](references/gsc-api-guide.md)（含截图级指引）。

```bash
cat > "$DATA_DIR/.env" <<EOF
SITE_URL=用户提供
GOOGLE_APPLICATION_CREDENTIALS=用户提供（绝对路径）
GSC_SITE_URL=用户提供（注意 sc-domain: 或 https:// 格式）
GA4_PROPERTY_ID=用户提供
SOURCE_CODE_PATH=用户提供
PSI_API_KEY=
EOF
```

**采集数据**（脚本自动从 .env 读取认证）:
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
```

首次使用需安装依赖：
```bash
python3 -m venv "$DATA_DIR/venv" && source "$DATA_DIR/venv/bin/activate"
pip install -r scripts/requirements.txt
```

脚本用法详见 [references/gsc-api-guide.md](references/gsc-api-guide.md) 和 [references/ga4-api-guide.md](references/ga4-api-guide.md)。

---

#### 模式 B：手动导出 CSV

向用户发送以下导出指引，请用户将文件放到 `$DATA_DIR/data/` 下：

> **导出 GSC 数据**：
> 1. 打开 [Google Search Console](https://search.google.com/search-console/) → 选择你的网站
> 2. 左侧点「搜索结果」（效果）
> 3. 日期范围选最近 3 个月，点「导出」→ 选「下载 CSV」
> 4. 将下载的 CSV 文件保存为 `$DATA_DIR/data/gsc_export.csv`
>
> **导出 GA4 数据（需要导出以下几份报告）**：
> 1. 打开 [Google Analytics](https://analytics.google.com/) → 选择你的媒体资源
> 2. 导出「页面和屏幕」报告：
>    - 左侧「报告」→「互动度」→「页面和屏幕」
>    - 右上角点分享图标 → 「下载文件」→ CSV
>    - 保存为 `$DATA_DIR/data/ga4_pages.csv`
> 3. 导出「流量获取」报告：
>    - 左侧「报告」→「流量获取」→「流量获取概览」
>    - 同样导出 CSV → 保存为 `$DATA_DIR/data/ga4_acquisition.csv`
> 4. 导出「着陆页」报告：
>    - 左侧「报告」→「互动度」→「着陆页」
>    - 同样导出 CSV → 保存为 `$DATA_DIR/data/ga4_landing.csv`
>
> 导出完成后告诉我，我会读取这些文件开始分析。

同时询问用户：
- **目标网站 URL**（必需，写入 `$DATA_DIR/.env` 的 `SITE_URL`）
- **源代码路径**（可选，写入 `SOURCE_CODE_PATH`）

收到文件后读取 `$DATA_DIR/data/` 下的 CSV 文件，解析后进入 Phase 2-3 分析。

---

#### 模式 C：仅浏览器审计

只需询问用户：
- **目标网站 URL**（必需）
- **源代码路径**（可选）

写入 `$DATA_DIR/.env` 后直接跳到 Phase 4（网站审计）和 Phase 5（源代码分析），跳过 Phase 2-3。

---

### Phase 2: GSC 数据分析

读取 `$DATA_DIR/data/` 下的 GSC 数据（JSON 或 CSV），按 [references/metrics-glossary.md](references/metrics-glossary.md) 中「SEO 优化」维度的阈值分析。

重点输出：
- 高展示低 CTR 关键词（优化标题/描述的最佳目标）
- 排名 4-10 的关键词（推至前 3 的 ROI 最高）
- 排名下降趋势页面
- 索引覆盖率和 sitemap 健康状态

**输出**: Top 10 SEO 优化机会，附带数据支撑。

---

### Phase 3: GA4 数据分析

读取 `$DATA_DIR/data/` 下的 GA4 数据（JSON 或 CSV），按 [references/metrics-glossary.md](references/metrics-glossary.md) 中「内容策略」「用户体验」「转化率优化」维度的阈值分析。

重点输出：
- 流量趋势和来源渠道效果
- 高流量低互动 / 高跳出率页面
- 移动端 vs 桌面端体验差异
- 转化漏斗断点

**输出**: Top 10 GA4 洞察发现，附带数据支撑。

---

### Phase 4: 网站实际审计

使用 `agent-browser` 访问 `$SITE_URL`：

```bash
agent-browser open "$SITE_URL" && agent-browser wait --load networkidle
agent-browser screenshot --full homepage_desktop.png
agent-browser set viewport 375 812
agent-browser screenshot --full homepage_mobile.png
agent-browser set viewport 1280 720
```

截图保存到 `$DATA_DIR/tmp/`。

PageSpeed Insights 性能审计（如 .env 中有 `PSI_API_KEY` 会自动附加）:
```bash
PSI_BASE="https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$SITE_URL&category=PERFORMANCE&category=SEO&category=ACCESSIBILITY&category=BEST_PRACTICES"
PSI_KEY_PARAM="${PSI_API_KEY:+&key=$PSI_API_KEY}"
curl -s "${PSI_BASE}&strategy=mobile${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_mobile.json"
curl -s "${PSI_BASE}&strategy=desktop${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_desktop.json"
```

> **PSI 失败降级**：如果返回 429（配额不足）或其他错误，检查是否在 Google Cloud 项目中启用了 "PageSpeed Insights API"（见 [references/gsc-api-guide.md](references/gsc-api-guide.md) 第一步）。PSI 数据缺失时，继续执行后续阶段，在报告中注明性能数据缺失。

从 PSI 提取 Core Web Vitals，阈值参考 [references/metrics-glossary.md](references/metrics-glossary.md) 中「网站性能」维度。

如有 GA4 数据，针对 Top 10 着陆页逐一截图（桌面+移动），记录视觉和交互问题。

无源代码时，通过浏览器提取前端元数据：
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

**输出**: 性能评分 + 视觉问题清单。

---

### Phase 5: 源代码分析

如果 `.env` 中配置了 `SOURCE_CODE_PATH`，分析项目源代码。无源代码则跳过。

检查项详见 [references/metrics-glossary.md](references/metrics-glossary.md) 中「技术问题」检查清单。核心关注：

- **SEO**: meta 标签完整性、JSON-LD、robots.txt / sitemap.xml、图片 alt、H1 规范
- **性能**: JS/CSS 分割和懒加载、图片格式和响应式、第三方脚本、render-blocking 资源
- **技术**: `<html lang>`、viewport、HTTPS、canonical URL、内部死链

**输出**: 代码级改进点清单。

---

### Phase 6: 生成改进报告

按 [references/metrics-glossary.md](references/metrics-glossary.md) 中「优先级矩阵」(P0-P3) 组织输出。使用以下模板：

```markdown
# 网站数据分析与改进方案

## 概要
- **目标网站**: [URL]
- **数据来源**: API 自动采集 / 手动导出 CSV / 仅浏览器审计
- **分析时间范围**: [start_date] ~ [end_date]
- **总结**: [1-2 句核心发现]

## 数据概览
| 指标 | 当前值 | 趋势 |
|------|--------|------|
| GSC 总展示量 / 点击量 / CTR / 排名 | ... | ... |
| GA4 会话数 / 用户数 / 跳出率 / 互动率 | ... | ... |
| PSI 性能评分 (Mobile/Desktop) | ... | ... |

## 改进方案
### P0 紧急（高影响，低难度）
1. **[问题]** — 数据支撑 / 改进方案 / 预期效果

### P1 高优 → P2 中优 → P3 低优
（同上格式）

## 详细分析
（按 SEO / 性能 / 内容策略 / 用户体验 / 转化率 / 技术问题 六个维度展开）

## 执行路线图
| 阶段 | 时间 | 任务 | 预期成果 |
|------|------|------|----------|
| Week 1-2 | P0 | ... | ... |
| Week 3-4 | P1 | ... | ... |
| Month 2+ | P2-P3 | ... | ... |
```

报告保存到 `$DATA_DIR/data/improvement-report.md`。

## 协作技能

- SEO 优化实施 → `seo-geo`
- 浏览器交互 → `agent-browser`
- 前端改造 → `frontend-design`

## 参考文档

| 文档 | 内容 |
|------|------|
| [references/gsc-api-guide.md](references/gsc-api-guide.md) | GSC 认证配置（手把手指引）、脚本用法、维度/指标说明 |
| [references/ga4-api-guide.md](references/ga4-api-guide.md) | GA4 认证配置、预置模板、维度/指标说明 |
| [references/metrics-glossary.md](references/metrics-glossary.md) | 六大分析维度的阈值、诊断要点、优先级矩阵 |
