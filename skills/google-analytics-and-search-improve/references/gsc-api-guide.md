# Google Search Console API 参考

## 认证配置

GSC 和 GA4 共用同一个 Service Account。创建一次即可两边使用。

### 第一步：创建 Google Cloud 项目并启用 API

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)
2. 左上角点「项目选择器」→ 点「新建项目」→ 取个名字（如 "my-site-analytics"）→ 点「创建」
3. 确认已切换到新项目后，打开 [API 库](https://console.cloud.google.com/apis/library)
4. 搜索 **"Google Search Console API"** → 点进去 → 点「启用」
5. 再搜索 **"Google Analytics Data API"** → 点进去 → 点「启用」（这样 GA4 也一起启用了）
6. 再搜索 **"PageSpeed Insights API"** → 点进去 → 点「启用」（用于网站性能审计，不启用会报 429 配额错误）

### 第二步：创建 Service Account 并下载 JSON 密钥

1. 打开 [Service Account 页面](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. 点顶部「+ 创建 Service Account」
3. 填写名称（如 "analytics-reader"）→ 点「创建并继续」
4. 角色选择可跳过（不需要项目级角色）→ 点「继续」→ 点「完成」
5. 在列表中找到刚创建的 Service Account，点击它的邮箱地址进入详情页
6. 点「密钥」选项卡 → 点「添加密钥」→ 选「创建新密钥」→ 选 **JSON** → 点「创建」
7. 浏览器会自动下载一个 `.json` 文件（如 `my-site-analytics-xxxx.json`），这就是密钥文件
8. 记住这个文件保存在你电脑上的路径（如 `/Users/你的用户名/Downloads/my-site-analytics-xxxx.json`）

**重要**：同时记下 Service Account 的邮箱地址（形如 `analytics-reader@my-site-analytics.iam.gserviceaccount.com`），下面授权时要用。

### 第三步：在 Search Console 中授权

1. 打开 [Google Search Console](https://search.google.com/search-console/)
2. 选择你的网站资源
3. 左侧菜单最下方点「设置」→ 点「用户和权限」
4. 点「添加用户」→ 粘贴上面的 Service Account 邮箱 → 权限选「受限」（只读即可）→ 点「添加」

### 第四步：确认 GSC 网站资源类型

GSC 有两种资源类型，`GSC_SITE_URL` 的值必须与实际类型匹配：

- **网域资源** (Domain property)：在 GSC 左上角显示纯域名 → 使用 `sc-domain:example.com`
- **网址前缀资源** (URL-prefix property)：显示完整 URL → 使用 `https://example.com`

填错格式会导致 API 返回 403 权限错误。

### 第五步：写入 .env

将以下值写入 `$DATA_DIR/.env`（脚本会自动加载）：

```
GOOGLE_APPLICATION_CREDENTIALS=/你电脑上的绝对路径/my-site-analytics-xxxx.json
GSC_SITE_URL=sc-domain:example.com
```

> **注意**：`GOOGLE_APPLICATION_CREDENTIALS` 应使用**绝对路径**，相对路径在不同工作目录下可能找不到密钥文件。

## 脚本用法

脚本自动从 `$DATA_DIR/.env` 读取 `GOOGLE_APPLICATION_CREDENTIALS` 和 `GSC_SITE_URL`，配置好 `.env` 后命令行无需重复传这些值。

### Search Analytics 查询

```bash
# 最近 28 天按查询词和页面分组（默认）
python scripts/gsc_query.py

# 指定维度和日期范围
python scripts/gsc_query.py --dimensions query --limit 500 \
    --start-date 2025-01-01 --end-date 2025-03-01

# 按设备和国家分组
python scripts/gsc_query.py --dimensions device,country --limit 100

# 按日期查看趋势
python scripts/gsc_query.py --dimensions date

# 输出到文件
python scripts/gsc_query.py --dimensions query -o gsc_data.json
```

命令行 `--site-url` 可覆盖 `.env` 中的 `GSC_SITE_URL`。

### 可用维度

| 维度 | 说明 |
|------|------|
| `query` | 搜索查询词 |
| `page` | 页面 URL |
| `country` | 国家代码 |
| `device` | 设备类型 (DESKTOP/MOBILE/TABLET) |
| `date` | 日期 |
| `searchAppearance` | 搜索结果展示类型 |

### 返回指标

每行数据包含：
- `clicks` - 点击次数
- `impressions` - 展示次数
- `ctr` - 点击率 (clicks / impressions)
- `position` - 平均排名位置

### Sitemap 查询

```bash
python scripts/gsc_query.py --mode sitemaps
```

### URL 检查

```bash
python scripts/gsc_query.py --mode inspect --inspect-url "https://example.com/some-page"
```

返回索引状态、抓取信息、移动端可用性等。

## 常见分析场景

### 发现高展示低点击的关键词（CTR 优化机会）

查询 `search_analytics`，按 query 分组，找 impressions 高但 ctr 低的行。

### 发现排名下降的页面

按 `date,page` 分组，比较不同时间段的 position 变化。

### 找出未被索引的页面

使用 `inspect` 模式逐一检查关键页面的索引状态。
