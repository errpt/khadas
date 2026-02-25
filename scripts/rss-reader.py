#!/usr/bin/env python3
"""
RSS 阅读器 - 定期拉取订阅的 RSS 并生成摘要
用法：python3 rss-reader.py
"""

import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# 尝试导入 feedparser，如果没有则提示安装
try:
    import feedparser
except ImportError:
    print("错误: 缺少 feedparser 库")
    print("请运行: pip3 install feedparser")
    sys.exit(1)

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "rss-feeds.json"
STATE_FILE = Path(__file__).parent.parent / "rss-state.json"


def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_state():
    """加载状态文件（记录已推送的文章）"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"seen_entries": {}, "last_check": None}


def save_state(state):
    """保存状态文件"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def parse_feed(feed_url):
    """解析 RSS feed"""
    try:
        feed = feedparser.parse(feed_url)
        return feed
    except Exception as e:
        print(f"解析 RSS 失败: {feed_url}, 错误: {e}")
        return None


def format_entry(entry, feed_name):
    """格式化单篇文章"""
    title = entry.get('title', '无标题')
    link = entry.get('link', '')
    published = entry.get('published', '')

    # 尝试获取摘要
    summary = entry.get('summary', '')
    if summary:
        # 移除 HTML 标签
        import re
        summary = re.sub('<[^<]+?>', '', summary)
        summary = summary[:150] + '...' if len(summary) > 150 else summary

    return f"""
### {title}

{summary}

📅 {published}
🔗 {link}
"""


def check_feeds(config, state):
    """检查所有订阅的 RSS"""
    if not config:
        print("配置文件不存在或为空")
        return None

    all_new_entries = []
    seen_entries = state.get("seen_entries", {})

    for feed_config in config.get("feeds", []):
        if not feed_config.get("enabled", True):
            continue

        feed_name = feed_config.get("name", "未知来源")
        feed_url = feed_config.get("url")
        category = feed_config.get("category", "未分类")

        print(f"正在检查: {feed_name} ({feed_url})")

        feed = parse_feed(feed_url)
        if not feed:
            continue

        max_items = config.get("settings", {}).get("maxItemsPerFeed", 5)
        new_count = 0

        for entry in feed.entries[:max_items]:
            entry_id = entry.get('id') or entry.get('link') or entry.get('title')

            if entry_id and entry_id not in seen_entries:
                seen_entries[entry_id] = {
                    "title": entry.get('title', ''),
                    "seen_at": datetime.now(timezone.utc).isoformat()
                }

                formatted = format_entry(entry, feed_name)
                all_new_entries.append({
                    "feed": feed_name,
                    "category": category,
                    "content": formatted
                })
                new_count += 1

        print(f"  → 发现 {new_count} 篇新文章")

    # 更新状态
    state["last_check"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    return all_new_entries


def generate_report(new_entries, config):
    """生成报告"""
    if not new_entries:
        return None

    # 按分类分组
    by_category = {}
    for entry in new_entries:
        cat = entry["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(entry)

    # 生成报告
    report_lines = [
        f"📰 **RSS 阅读摘要** - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC\n",
        f"共 {len(new_entries)} 篇新文章\n"
    ]

    include_categories = config.get("settings", {}).get("includeCategories", ["全部"])

    for category, entries in by_category.items():
        if "全部" not in include_categories and category not in include_categories:
            continue

        report_lines.append(f"\n---\n## 📂 {category}\n")

        for entry in entries:
            report_lines.append(entry["content"])

    return "\n".join(report_lines)


def send_to_feishu(message):
    """通过 OpenClaw 发送到飞书"""
    try:
        # 使用 message 工具发送
        result = subprocess.run(
            ['openclaw', 'message', 'send', '--channel=feishu', '--message', message],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"发送结果: {result.returncode}")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"错误: {result.stderr}")
    except Exception as e:
        print(f"发送失败: {e}")


def main():
    """主函数"""
    print("📡 RSS 阅读器启动")

    # 加载配置
    config = load_config()
    if not config:
        print("❌ 配置文件不存在，请先创建 rss-feeds.json")
        sys.exit(1)

    # 加载状态
    state = load_state()

    # 检查订阅
    new_entries = check_feeds(config, state)

    # 生成并发送报告
    if new_entries:
        print(f"\n✅ 发现 {len(new_entries)} 篇新文章")
        report = generate_report(new_entries, config)

        if report:
            print("\n" + "="*60)
            print(report)
            print("="*60)

            # 保存报告到文件
            report_file = Path(__file__).parent.parent / "rss-report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📝 报告已保存到: {report_file}")

            # 提示用户如何发送
            print("\n💡 要发送到飞书，请告诉我: '发送 RSS 报告'")
    else:
        print("✅ 没有新文章")


if __name__ == "__main__":
    main()
