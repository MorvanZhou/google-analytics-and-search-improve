# Google Analytics 4 Data API 参考

## 认证配置

GA4 和 GSC 共用同一个 Service Account。如果你还没有创建，请先按照 [gsc-api-guide.md](gsc-api-guide.md) 中的「第一步 ~ 第二步」完成 Google Cloud 项目创建、API 启用和 Service Account 密钥下载（那边已经包含了 GA4 API 的启用）。

### 在 GA4 中授权 Service Account

1. 打开 [Google Analytics](https://analytics.google.com/)
2. 左下角点齿轮图标（管理）
3. 在「属性」栏下点「属性访问管理」
4. 点右上角「+」→ 选「添加用户」
5. 粘贴 Service Account 邮箱（形如 `xxx@xxx.iam.gserviceaccount.com`）→ 角色选「查看者」→ 点「添加」

### 获取 GA4 Property ID

1. 在 Google Analytics 管理页面，点「属性」栏下的「属性设置」（或「属性详情」）
2. 页面右上角会显示「属性 ID」，是一串纯数字（如 `123456789`，不含 "UA-" 前缀）

### 写入 .env

将以下值写入 `$DATA_DIR/.env`（脚本会自动加载）：

```
GA4_PROPERTY_ID=123456789
```

`GOOGLE_APPLICATION_CREDENTIALS` 在 GSC 配置时已写入，GA4 共用同一个密钥文件，无需重复填写。

## 脚本用法

脚本自动从 `$DATA_DIR/.env` 读取 `GOOGLE_APPLICATION_CREDENTIALS` 和 `GA4_PROPERTY_ID`，配置好 `.env` 后命令行无需重复传这些值。

### 预置查询模板

```bash
python scripts/ga4_query.py --preset traffic_overview       # 每日流量趋势
python scripts/ga4_query.py --preset top_pages --limit 50   # 热门页面
python scripts/ga4_query.py --preset user_acquisition       # 用户来源
python scripts/ga4_query.py --preset device_breakdown        # 设备分布
python scripts/ga4_query.py --preset geo_distribution        # 地理分布
python scripts/ga4_query.py --preset landing_pages           # 着陆页
python scripts/ga4_query.py --preset user_behavior           # 用户行为
python scripts/ga4_query.py --preset conversion_events       # 转化事件
```

命令行 `--property-id` 可覆盖 `.env` 中的 `GA4_PROPERTY_ID`。

### 自定义查询

```bash
python scripts/ga4_query.py \
    --dimensions pagePath,deviceCategory \
    --metrics sessions,bounceRate,averageSessionDuration \
    --start-date 2025-01-01 --end-date 2025-03-01 \
    --order-by -sessions --limit 200
```

### 日期格式

支持绝对日期和相对日期：
- 绝对: `2025-01-01`
- 相对: `today`, `yesterday`, `NdaysAgo`（如 `28daysAgo`）

## 常用维度

| 维度 | 说明 |
|------|------|
| `date` | 日期 |
| `pagePath` | 页面路径 |
| `pageTitle` | 页面标题 |
| `landingPage` | 着陆页 |
| `sessionDefaultChannelGroup` | 渠道分组 |
| `sessionSource` / `sessionMedium` | 来源 / 媒介 |
| `deviceCategory` | 设备类别 |
| `operatingSystem` / `browser` | 操作系统 / 浏览器 |
| `country` / `city` | 国家 / 城市 |
| `eventName` | 事件名称 |

## 常用指标

| 指标 | 说明 |
|------|------|
| `sessions` | 会话数 |
| `totalUsers` / `newUsers` | 总用户数 / 新用户数 |
| `screenPageViews` | 页面浏览量 |
| `bounceRate` | 跳出率 |
| `averageSessionDuration` | 平均会话时长（秒） |
| `engagementRate` / `engagedSessions` | 互动率 / 互动会话数 |
| `eventCount` | 事件数 |
| `conversions` | 转化次数 |

## 预置模板说明

| 模板名 | 用途 |
|--------|------|
| `traffic_overview` | 每日流量趋势，发现流量异常 |
| `top_pages` | 找出最受欢迎的页面和低效页面 |
| `user_acquisition` | 分析用户来源渠道效果 |
| `device_breakdown` | 设备和浏览器分布，发现兼容性问题 |
| `geo_distribution` | 地理分布，优化国际化策略 |
| `landing_pages` | 着陆页效果，优化入口体验 |
| `user_behavior` | 用户行为路径和互动深度 |
| `conversion_events` | 转化事件追踪和漏斗分析 |
