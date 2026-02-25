#!/bin/bash
# RSS 自动检查并推送报告
# 每天 UTC 13:00（北京时间 21:00）运行

WORKSPACE="/home/khadas/.openclaw/workspace"
cd "$WORKSPACE"

# 运行 RSS 阅读器
python3 scripts/rss-reader-simple.py

# 检查是否有新报告
if [ -f "rss-report-latest.md" ]; then
    echo "✅ RSS 报告已生成"
    # 获取最新的报告文件
    LATEST_REPORT=$(ls -t reports/rss-report-*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_REPORT" ]; then
        echo "📄 最新报告: $LATEST_REPORT"
    fi
    # 这里可以添加发送到飞书的逻辑
    # 或者保存到特定位置
else
    echo "ℹ️  没有新文章"
fi

# 记录日志
echo "[$(date '+%Y-%m-%d %H:%M:%S')] RSS 检查完成" >> "$WORKSPACE/logs/rss-check.log"
