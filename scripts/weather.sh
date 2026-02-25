#!/bin/bash
# 天气查询脚本
# 使用 wttr.in 服务（无需 API key）

CITY="${1:-Beijing}"  # 默认城市：北京

echo "🌤️  天气查询 - $CITY"
echo "================================================"

# 获取当前天气（简洁格式）
echo ""
echo "📍 当前天气："
curl -s "wttr.in/$CITY?format=%l:+%c+%t+(feels+like+%f)+湿度:%h+风力:%w" | tr '+' '\n' | sed 's/^/  /'

echo ""
echo "================================================"
echo "📊 详细预报："
echo ""
curl -s "wttr.in/$CITY?format=v2" | head -20

echo ""
echo "================================================"
echo "💡 提示："
echo "  - 使用: $0 [城市名]"
echo "  - 例如: $0 Shanghai"
echo "  - 支持中文和英文城市名"
