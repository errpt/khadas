#!/usr/bin/env python3
"""
天气查询脚本
使用 Open-Meteo API（免费，无需 API key）
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

def get_weather(city="Beijing"):
    """获取天气信息"""
    # 城市坐标映射
    cities = {
        "Beijing": (39.9042, 116.4074, "北京"),
        "Shanghai": (31.2304, 121.4737, "上海"),
        "Guangzhou": (23.1291, 113.2644, "广州"),
        "Shenzhen": (22.5431, 114.0579, "深圳"),
        "Hangzhou": (30.2741, 120.1551, "杭州"),
        "Chengdu": (30.5728, 104.0668, "成都"),
        "Wuhan": (30.5928, 114.3055, "武汉"),
        "Nanjing": (32.0603, 118.7969, "南京"),
    }

    # 城市名查找（支持中英文）
    city_key = city
    if city not in cities:
        # 尝试模糊匹配
        for key, value in cities.items():
            if city.lower() in value[2].lower() or city.lower() in key.lower():
                city_key = key
                break
        else:
            return None

    lat, lon, city_name = cities[city_key]

    try:
        # Open-Meteo API（免费）
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            # 解析当前天气
            current = data.get('current', {})
            daily = data.get('daily', {})

            # 天气代码映射
            weather_codes = {
                0: "晴", 1: "晴", 2: "晴", 3: "晴",
                45: "雾", 48: "雾",
                51: "毛毛雨", 53: "毛毛雨", 55: "毛毛雨",
                61: "小雨", 63: "小雨", 65: "小雨",
                80: "阵雨", 81: "阵雨", 82: "阵雨",
                95: "雷雨", 96: "雷雨", 99: "雷雨",
            }

            code = current.get('weather_code', 0)
            condition = weather_codes.get(code, "未知")

            result = f"""
🌤️  {city_name}天气
{'='*40}

📍 当前天气
------------------------
温度：{current.get('temperature_2m', 0):.1f}°C
湿度：{current.get('relative_humidity_2m', 0)}%
风速：{current.get('wind_speed_10m', 0):.1f} km/h
天气：{condition}

📊 未来3天预报
------------------------
"""

            # 显示未来3天
            for i in range(min(3, len(daily.get('time', [])))):
                date = datetime.fromisoformat(daily['time'][i]).strftime('%m-%d')
                code = daily['weather_code'][i]
                condition = weather_codes.get(code, "未知")
                t_max = daily['temperature_2m_max'][i]
                t_min = daily['temperature_2m_min'][i]

                result += f"{date}: {condition} {t_max:.0f}°C / {t_min:.0f}°C\n"

            result += f"\n{'='*40}\n"
            result += f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"

            return result

    except Exception as e:
        return f"❌ 获取天气失败：{e}"


if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Beijing"
    result = get_weather(city)

    if result:
        print(result)
    else:
        print(f"❌ 未找到城市：{city}")
        print("\n支持的城市：")
        print("  - Beijing (北京)")
        print("  - Shanghai (上海)")
        print("  - Guangzhou (广州)")
        print("  - Shenzhen (深圳)")
        print("  - Hangzhou (杭州)")
        print("  - Chengdu (成都)")
        print("  - Wuhan (武汉)")
        print("  - Nanjing (南京)")
