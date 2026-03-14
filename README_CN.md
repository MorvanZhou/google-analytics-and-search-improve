# Google Analytics & Search Console 网站改进技能

[English](README.md)

一个 AI 代理技能，通过 Google Search Console (GSC) 和 Google Analytics 4 (GA4) API 分析网站数据，结合浏览器自动化审计和源代码分析，生成数据驱动的改进方案。

## 功能概述

给你的 AI 代理一个网站 URL，它会：

1. **采集数据** — 通过 API 从 GSC 和 GA4 获取数据（或手动导出 CSV）
2. **分析搜索表现** — 关键词、CTR、排名、索引健康度
3. **分析用户行为** — 流量来源、跳出率、设备分布、转化漏斗
4. **审计线上网站** — 截图、PageSpeed Insights、SEO 元数据提取
5. **审查源代码**（可选）— meta 标签、结构化数据、性能模式
6. **生成优先级报告** — 覆盖 6 大维度的 P0-P3 行动项

### 六大分析维度

| 维度 | 数据源 | 关键指标 |
|------|--------|----------|
| SEO 优化 | GSC | CTR、排名、展示量、索引覆盖率 |
| 网站性能 | PageSpeed Insights | LCP、INP、CLS、TTFB |
| 内容策略 | GA4 + GSC | 页面浏览量、互动率、内容缺口 |
| 用户体验 | GA4 | 跳出率、会话时长、设备分布 |
| 转化率 | GA4 | 漏斗分析、着陆页转化率 |
| 技术问题 | 浏览器 + 源代码 | meta 标签、JSON-LD、robots.txt、sitemap、无障碍 |

## 安装

```bash
npx skills add morvanzhou/google-analytics-and-search-improve
```

或手动克隆到你的技能目录：

```
skills/
  google-analytics-and-search-improve/
    SKILL.md              # 技能定义（工作流指令）
    scripts/
      gsc_query.py        # GSC API 数据提取
      ga4_query.py        # GA4 API 数据提取
      requirements.txt    # Python 依赖
    references/
      gsc-api-guide.md    # GSC 认证配置 & 脚本用法
      ga4-api-guide.md    # GA4 认证配置 & 预置模板
      metrics-glossary.md # 分析阈值 & 优先级矩阵
```

## 快速开始

告诉你的 AI 代理：

> 使用 google-analytics-and-search-improve 技能分析 example.com

技能提供三种数据采集模式：

| 模式 | 配置时间 | 数据覆盖 |
|------|---------|----------|
| **A. API 自动采集**（推荐）| 首次约 10 分钟 | 完整的 GSC + GA4 数据 |
| **B. 手动导出 CSV** | 无需配置 | 取决于你导出的内容 |
| **C. 仅浏览器审计** | 无需配置 | 仅技术审计 |

### 模式 A：API 配置

需要一个 Google Cloud Service Account，同时授权访问 GSC 和 GA4。

1. **创建 Google Cloud 项目**，启用以下 API：
   - Google Search Console API
   - Google Analytics Data API
   - PageSpeed Insights API

2. **创建 Service Account**，下载 JSON 密钥文件

3. **授权访问**：
   - 在 GSC 中：设置 → 用户和权限 → 添加 SA 邮箱为「受限」用户
   - 在 GA4 中：管理 → 属性访问管理 → 添加 SA 邮箱为「查看者」

4. **向 AI 代理提供配置**：
   - JSON 密钥文件路径（使用绝对路径）
   - GSC 网站地址 — 网域资源使用 `sc-domain:example.com`，网址前缀资源使用 `https://example.com`
   - GA4 Property ID（纯数字）

> **重要提示**：GSC 有两种资源类型，填错格式会导致 403 错误。在 [Search Console](https://search.google.com/search-console/) 左上角的网站选择器中查看——如果显示的是纯域名，使用 `sc-domain:` 前缀；如果显示完整 URL，直接使用该 URL。

详细的配置步骤见 [references/gsc-api-guide.md](skills/google-analytics-and-search-improve/references/gsc-api-guide.md)。

## 项目结构

```
.
├── skills/google-analytics-and-search-improve/
│   ├── SKILL.md                          # 技能定义 & 工作流
│   ├── scripts/
│   │   ├── gsc_query.py                  # GSC 搜索分析、Sitemap、URL 检查
│   │   ├── ga4_query.py                  # GA4 查询，内置 8 种预置模板
│   │   └── requirements.txt              # Python 依赖
│   └── references/
│       ├── gsc-api-guide.md              # 认证配置、脚本用法、维度说明
│       ├── ga4-api-guide.md              # 认证配置、预置模板、指标说明
│       └── metrics-glossary.md           # 分析阈值、诊断要点、优先级矩阵
├── .skills-data/                         # 运行时数据（已 gitignore）
│   └── google-analytics-and-search-improve/
│       ├── .env                          # 认证凭据 & 配置
│       ├── data/                         # 采集的 JSON/CSV 数据 & 报告
│       ├── tmp/                          # 截图
│       ├── cache/                        # API 响应缓存
│       └── venv/                         # Python 虚拟环境
└── .gitignore
```

## 输出

技能会生成一份完整的改进报告，保存在 `.skills-data/google-analytics-and-search-improve/data/improvement-report.md`，包含：

- **数据概览** — 关键指标汇总，含当前值和趋势
- **优先级行动项**（P0 紧急 → P3 低优）— 每项附带数据支撑、具体修复方案和预期效果
- **详细分析** — 按 6 大维度展开
- **执行路线图** — 按周制定的实施计划

## 协作技能

| 技能 | 用途 |
|------|------|
| `seo-geo` | 实施报告中的 SEO/GEO 优化建议 |
| `agent-browser` | 浏览器自动化，用于网站审计 |
| `frontend-design` | 实施前端/UX 改进 |

## 许可证

MIT
