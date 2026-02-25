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
echo "防火墙状态：" >> /tmp/security-audit.txt
if command -v ufw &> /dev/null; then
    ufw status verbose >> /tmp/security-audit.txt 2>&1
else
    echo "UFW 未安装" >> /tmp/security-audit.txt
fi

# 保存最新报告副本
cp /tmp/security-audit.txt "$REPORT_DIR/security-report-latest.txt"

# 生成 Markdown 格式报告
UFW_STATUS="未安装"
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(ufw status verbose 2>&1)
fi

cat > "$REPORT_FILE" << EOF
# 安全检查报告

**检查时间**：$(date '+%Y-%m-%d %H:%M:%S UTC')
**设备**：Khadas (Ubuntu 24.04)

---

## 检查摘要

\`\`\`
$(cat /tmp/security-audit.txt)
\`\`\`

---

## 系统状态

**磁盘使用**：
\`\`\`
$(df -h /)
\`\`\`

**监听端口**：
\`\`\`
$(ss -ltnp | grep -E "LISTEN.*:(22|5555|18789)")
\`\`\`

**UFW 防火墙**：
\`\`\`
$UFW_STATUS
\`\`\`

---

*报告位置：$REPORT_FILE*
EOF

# 记录日志
echo "✅ 安全检查完成" >> "$LOG_DIR/security-check.log"
echo "报告保存到: $REPORT_FILE" >> "$LOG_DIR/security-check.log"

# 统计问题
CRITICAL_COUNT=$(grep -c "CRITICAL" /tmp/security-audit.txt || echo "0")
WARN_COUNT=$(grep -c "^WARN" /tmp/security-audit.txt || echo "0")

# 生成飞书消息
FEISHU_MESSAGE="# 🔒 安全检查报告 - $(date '+%Y-%m-%d')

**检查时间**：$(date '+%H:%M') UTC
**发现问题**：$CRITICAL_COUNT 个严重 · $WARN_COUNT 个警告

---
📊 **完整报告**：\`$REPORT_FILE\`

---
🤖 由 OpenClaw 自动生成"

# 保存消息到文件，便于后续发送
echo "$FEISHU_MESSAGE" > "$WORKSPACE/security-alert.txt"

# 如果有严重问题，记录到日志
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "⚠️  发现 $CRITICAL_COUNT 个严重问题！" >> "$LOG_DIR/security-check.log"
fi

echo "============================================================" >> "$LOG_DIR/security-check.log"
