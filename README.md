# Khadas OpenClaw Workspace

这是我的 OpenClaw 工作区，包含各种实用脚本和工具。

## 📦 内容

### RSS 阅读器
一个简单、可定制的 RSS 阅读系统，支持多订阅源分类管理，定期推送最新文章摘要。

**特性：**
- ✅ 多 RSS 订阅源管理
- ✅ 分类整理（科技、新闻、博客等）
- ✅ 去重机制（不重复推送已读文章）
- ✅ 无依赖（使用 Python 标准库）
- ✅ 定时自动检查

**使用方法：**
```bash
# 检查更新
python3 scripts/rss-reader-simple.py

# 查看报告
cat rss-report.md
```

**配置订阅源：**
编辑 `rss-feeds.json` 添加你想要的 RSS 订阅：
```json
{
  "feeds": [
    {
      "name": "爱范儿",
      "url": "https://www.ifanr.com/feed",
      "enabled": true,
      "category": "科技"
    }
  ]
}
```

**定时任务：**
- 每天 UTC 13:00（北京时间 21:00）自动检查
- 日志位置：`logs/rss-check.log`

---

## 🔧 技术栈

- **Python 3** - RSS 阅读器
- **Git** - 版本控制
- **Bash** - 自动化脚本

---

## 📝 配置文件

- `rss-feeds.json` - RSS 订阅源配置
- `rss-state.json` - 已读文章记录（自动生成）
- `rss-report.md` - 最新报告（自动生成）

---

## 🚀 快速开始

1. 添加 RSS 订阅源到 `rss-feeds.json`
2. 运行 `python3 scripts/rss-reader-simple.py`
3. 查看生成的 `rss-report.md`

---

## 📧 反馈

有问题？欢迎提 Issue！

---

*由 OpenClaw 自动生成和维护*
