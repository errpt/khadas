# OpenClaw 使用指南

## 📚 目录

- [RSS 阅读器使用](#rss-阅读器使用)
- [Git 常用命令](#git-常用命令)
- [定时任务管理](#定时任务管理)
- [常见问题](#常见问题)

---

## RSS 阅读器使用

### 添加订阅源

编辑 `rss-feeds.json`：

```json
{
  "feeds": [
    {
      "name": "网站名称",
      "url": "RSS订阅地址",
      "enabled": true,
      "category": "分类"
    }
  ]
}
```

### 常用 RSS 订阅地址

#### 中文科技媒体
- 爱范儿: `https://www.ifanr.com/feed`
- 少数派: `https://sspai.com/feed`
- 36氪: `https://36kr.com/feed`
- 虎嗅: `https://www.huxiu.com/rss/0.xml`

#### 国际科技媒体
- TechCrunch: `https://techcrunch.com/feed/`
- The Verge: `https://www.theverge.com/rss/index.xml`
- Ars Technica: `https://feeds.arstechnica.com/arstechnica/index`

#### 个人博客
- 阮一峰: `https://www.ruanyifeng.com/blog/atom.xml`

### 手动检查更新

```bash
cd /home/khadas/.openclaw/workspace
python3 scripts/rss-reader-simple.py
```

### 查看报告

```bash
cat rss-report.md
```

### 定时任务

**当前设置：** 每天晚上 9:00（北京时间）自动检查

**查看日志：**
```bash
tail -f logs/rss-check.log
```

**修改定时任务：**
```bash
crontab -e
```

---

## Git 常用命令

### 基本操作

```bash
# 查看状态
git status

# 添加所有更改
git add .

# 提交更改
git commit -m "提交说明"

# 推送到远程
git push

# 拉取更新
git pull
```

### 查看历史

```bash
# 查看提交历史
git log --oneline

# 查看最近 3 次提交
git log --oneline -3

# 查看文件变更
git diff
```

### 分支管理

```bash
# 查看分支
git branch

# 创建新分支
git branch feature-name

# 切换分支
git checkout feature-name

# 合并分支
git merge feature-name
```

---

## 定时任务管理

### Cron 表达式格式

```
* * * * * 命令
│ │ │ │ │
│ │ │ │ └─── 星期几 (0-7, 0和7都代表周日)
│ │ │ └───── 月份 (1-12)
│ │ └─────── 日期 (1-31)
│ └───────── 小时 (0-23)
└─────────── 分钟 (0-59)
```

### 常用示例

```bash
# 每天早上 9 点（UTC）
0 1 * * * /path/to/script.sh

# 每 4 小时
0 */4 * * * /path/to/script.sh

# 每周一早上 9 点
0 1 * * 1 /path/to/script.sh
```

### 管理定时任务

```bash
# 查看当前定时任务
crontab -l

# 编辑定时任务
crontab -e

# 删除所有定时任务
crontab -r
```

---

## 常见问题

### Q: 如何修改 RSS 检查时间？

编辑 crontab：
```bash
crontab -e
```
修改时间表达式后保存即可。

### Q: 如何临时禁用某个订阅源？

在 `rss-feeds.json` 中设置 `"enabled": false`

### Q: 报告保存在哪里？

`/home/khadas/.openclaw/workspace/rss-report.md`

### Q: 如何查看运行日志？

```bash
# RSS 检查日志
cat logs/rss-check.log

# Cron 日志
cat logs/rss-cron.log
```

### Q: 如何添加新的脚本？

1. 在 `scripts/` 目录创建脚本文件
2. 添加执行权限：`chmod +x scripts/your-script.sh`
3. 提交到 Git：`git add . && git commit -m "添加新脚本" && git push`

---

## 🔗 相关链接

- GitHub 仓库：https://github.com/errpt/khadas
- OpenClaw 文档：https://docs.openclaw.ai

---

*最后更新：2026-02-25*
