#!/bin/bash
# 天气查询并发送到飞书

WORKSPACE="/home/khadas/.openclaw/workspace"
CITY="${1:-Beijing}"

cd "$WORKSPACE"

# 运行天气脚本
WEATHER_RESULT=$(python3 scripts/weather.py "$CITY" 2>&1)

# 生成飞书消息
FEISHU_MESSAGE="$WEATHER_RESULT

---
🤖 由 OpenClaw 自动生成
回复 '天气 [城市名]' 查询其他城市"

# 保存到文件
echo "$FEISHU_MESSAGE" > "$WORKSPACE/weather-alert.txt"

# 输出到控制台
echo "$FEISHU_MESSAGE"

# 保存日志
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 天气查询: $CITY" >> "$WORKSPACE/logs/weather.log"
