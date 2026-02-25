#!/bin/bash
# 每日安全检查脚本
# 运行 OpenClaw 安全审计并生成报告

WORKSPACE="/home/khadas/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
REPORT_DIR="$WORKSPACE/security-reports"

# 创建目录
mkdir -p "$LOG_DIR" "$REPORT_DIR"

cd "$WORKSPACE"

# 生成带时间戳的文件名
TIMESTAMP=$(date +%Y%m%d-%H%M)
REPORT_FILE="$REPORT_DIR/security-report-$TIMESTAMP.md"

echo "============================================================" >> "$LOG_DIR/security-check.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始安全检查" >> "$LOG_DIR/security-check.log"

# 运行 OpenClaw 安全审计
echo "🔍 运行 OpenClaw 安全审计..."
openclaw security audit > /tmp/security-audit.txt 2>&1

# 检查系统状态
echo "" >> /tmp/security-audit.txt
echo "=== 系统信息 ===" >> /tmp/security-audit.txt
echo "磁盘使用：" >> /tmp/security-audit.txt
df -h / >> /tmp/security-audit.txt
echo "" >> /tmp/security-audit.txt
echo "监听端口：" >> /tmp/security-audit.txt
ss -ltnp | grep -E "LISTEN.*:(22|5555|18789)" >> /tmp/security-audit.txt
echo "" >> /tmp/security-audit.txt
echo "UFW 状态：" >> /tmp/security-audit.txt
ufw status verbose >> /tmp/security-audit.txt

# 保存最新报告副本
cp /tmp/security-audit.txt "$REPORT_DIR/security-report-latest.txt"

# 记录日志
echo "✅ 安全检查完成" >> "$LOG_DIR/security-check.log"
echo "报告保存到: $REPORT_FILE" >> "$LOG_DIR/security-check.log"

# 如果有严重问题，记录到日志
if grep -q "CRITICAL" /tmp/security-audit.txt; then
    echo "⚠️  发现严重问题！" >> "$LOG_DIR/security-check.log"
fi

# TODO: 推送到飞书知识库
# echo "📤 推送报告到飞书..." >> "$LOG_DIR/security-check.log"

echo "============================================================" >> "$LOG_DIR/security-check.log"
