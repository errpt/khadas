# RSS 阅读器 - 使用说明

一个简单、可定制的 RSS 阅读方案，支持多订阅源分类管理，定期推送最新文章摘要到飞书。

## 📋 功能特性

- ✅ 多 RSS 订阅源管理
- ✅ 分类整理（科技、新闻、博客等）
- ✅ 去重机制（不重复推送已读文章）
- ✅ 可配置检查频率和推送时间
- ✅ 生成 Markdown 格式报告
- ✅ 支持通过飞书接收推送

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install feedparser
```

### 2. 配置订阅源

编辑 `rss-feeds.json`，添加你想要的 RSS 订阅：

```json
{
  "feeds": [
    {
      "name": "爱范儿",
      "url": "https://www.ifanr.com/feed",
      "enabled": true,
      "category": "科技"
    },
    {
      "name": "少数派",
      "url": "https://sspai.com/feed",
      "enabled": true,
      "category": "科技"
    },
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "enabled": true,
      "category": "科技"
    }
  ],
  "settings": {
    "checkIntervalMinutes": 240,
    "maxItemsPerFeed": 5,
    "pushTime": "09:00",
    "pushTimeZone": "Asia/Shanghai",
    "includeCategories": ["科技", "全部"]
  }
}
```

### 3. 运行检查

```bash
cd /home/khadas/.openclaw/workspace/scripts
python3 rss-reader.py
```

## ⚙️ 配置说明

### 订阅源配置

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 订阅源名称 | "爱范儿" |
| `url` | RSS 订阅地址 | "https://www.ifanr.com/feed" |
| `enabled` | 是否启用 | `true` / `false` |
| `category` | 分类标签 | "科技", "新闻", "博客" |

### 全局设置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `checkIntervalMinutes` | 检查间隔（分钟） | 240（4小时） |
| `maxItemsPerFeed` | 每个源最多获取文章数 | 5 |
| `pushTime` | 推送时间 | "09:00" |
| `pushTimeZone` | 时区 | "Asia/Shanghai" |
| `includeCategories` | 包含的分类 | ["科技", "全部"] |

## 📝 常用 RSS 订阅地址

### 中文科技媒体
- 爱范儿: `https://www.ifanr.com/feed`
- 少数派: `https://sspai.com/feed`
- 36氪: `https://36kr.com/feed`
- 虎嗅: `https://www.huxiu.com/rss/0.xml`
- 钛媒体: `https://www.tmtpost.com/rss.xml`

### 国际科技媒体
- TechCrunch: `https://techcrunch.com/feed/`
- The Verge: `https://www.theverge.com/rss/index.xml`
- Ars Technica: `https://feeds.arstechnica.com/arstechnica/index`

### 其他推荐
- 阮一峰的网络日志: `https://www.ruanyifeng.com/blog/atom.xml`
- 维基百科每日新闻: `https://zh.wikipedia.org/wiki/Wikipedia:%E4%BB%8A%E6%97%A5%E5%A4%B4%E6%9D%A1`

## 🔧 自动化运行

### 方式一：使用 Cron（推荐）

编辑 crontab：

```bash
crontab -e
```

添加定时任务（例如每 4 小时检查一次）：

```cron
0 */4 * * * cd /home/khadas/.openclaw/workspace/scripts && python3 rss-reader.py >> /tmp/rss-reader.log 2>&1
```

### 方式二：让我帮你设置

告诉我：
- "每天早上 9 点检查 RSS"
- "每 6 小时检查一次"

我会用 OpenClaw 的定时功能帮你设置。

## 📤 发送到飞书

运行脚本后，报告会保存在 `rss-report.md`。

然后告诉我：**"发送 RSS 报告"**，我会把最新报告推送到飞书。

## 🗂️ 文件说明

```
workspace/
├── rss-feeds.json      # 订阅源配置
├── rss-state.json      # 状态文件（已读文章记录）
├── rss-report.md       # 最新报告
└── scripts/
    └── rss-reader.py   # RSS 阅读器脚本
```

## 💡 使用技巧

1. **批量添加订阅**：直接编辑 `rss-feeds.json`，一次性添加多个订阅源
2. **分类管理**：使用 `category` 字段分组，方便筛选
3. **临时禁用**：设置 `enabled: false` 暂停某个订阅源
4. **去重机制**：已推送的文章不会重复，不用担心 spam

---

有问题随时问我！
