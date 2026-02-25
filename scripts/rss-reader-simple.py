#!/usr/bin/env python3
"""
RSS 阅读器 - 无依赖版本（改进版）
使用正则表达式解析，更加容错
"""

import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error
import html

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
    """加载状态文件"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"seen_entries": {}, "last_check": None}


def save_state(state):
    """保存状态文件"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def fetch_rss(url, timeout=15):
    """获取 RSS 内容"""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Compatible; RSSReader/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            # 尝试不同编码
            for encoding in ['utf-8', 'gbk', 'gb2312', 'iso-8859-1']:
                try:
                    return content.decode(encoding)
                except:
                    continue
            return content.decode('utf-8', errors='ignore')
    except urllib.error.URLError as e:
        print(f"  ❌ 网络错误: {e}")
        return None
    except Exception as e:
        print(f"  ❌ 获取失败: {e}")
        return None


def strip_html(text):
    """移除 HTML 标签"""
    if not text:
        return ''
    # 移除 script 和 style 标签及其内容
    text = re.sub(r'<script[^>]*?>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*?>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除所有 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 解码 HTML 实体
    text = html.unescape(text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_rss_regex(xml_content, feed_name):
    """使用正则表达式解析 RSS（更容错）"""
    entries = []

    try:
        # 提取所有 <item> 或 <entry> 块
        items = re.findall(r'<item[^>]*>(.*?)</item>', xml_content, re.DOTALL | re.IGNORECASE)
        if not items:
            items = re.findall(r'<entry[^>]*>(.*?)</entry>', xml_content, re.DOTALL | re.IGNORECASE)

        for item in items[:15]:  # 最多取15条
            entry = {}

            # 提取标题
            title_match = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL | re.IGNORECASE)
            if title_match:
                entry['title'] = strip_html(title_match.group(1))
            else:
                entry['title'] = '无标题'

            # 提取链接
            link_match = re.search(r'<link[^>]*>(.*?)</link>', item, re.DOTALL | re.IGNORECASE)
            if not link_match:
                link_match = re.search(r'<link[^>]*url=["\']([^"\']+)["\']', item, re.IGNORECASE)
            if link_match:
                entry['link'] = strip_html(link_match.group(1) if link_match.lastindex else link_match.group(1))
            else:
                entry['link'] = ''

            # 提取描述
            desc_match = re.search(r'<description[^>]*>(.*?)</description>', item, re.DOTALL | re.IGNORECASE)
            if not desc_match:
                desc_match = re.search(r'<content[^>]*>(.*?)</content>', item, re.DOTALL | re.IGNORECASE)
            if desc_match:
                desc = strip_html(desc_match.group(1))
                entry['summary'] = desc[:200] + '...' if len(desc) > 200 else desc
            else:
                entry['summary'] = ''

            # 提取发布日期
            pub_match = re.search(r'<pubDate[^>]*>(.*?)</pubDate>', item, re.DOTALL | re.IGNORECASE)
            if not pub_match:
                pub_match = re.search(r'<published[^>]*>(.*?)</published>', item, re.DOTALL | re.IGNORECASE)
            if pub_match:
                entry['published'] = strip_html(pub_match.group(1))
            else:
                entry['published'] = ''

            # 使用链接+标题作为唯一 ID
            entry['id'] = entry['link'] + '|' + entry['title']

            entries.append(entry)

    except Exception as e:
        print(f"  ❌ 解析错误: {e}")

    return entries


def format_entry(entry, feed_name):
    """格式化单篇文章"""
    title = entry.get('title', '无标题')
    link = entry.get('link', '')
    published = entry.get('published', '')
    summary = entry.get('summary', '')

    result = f"### {title}\n\n"
    if summary:
        result += f"{summary}\n\n"
    if published:
        result += f"📅 {published}\n"
    result += f"🔗 {link}\n"

    return result


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

        print(f"📡 {feed_name}")
        print(f"   {feed_url}")

        # 获取 RSS
        xml_content = fetch_rss(feed_url)
        if not xml_content:
            print(f"   ⏭️  跳过\n")
            continue

        # 解析
        entries = parse_rss_regex(xml_content, feed_name)
        if not entries:
            print(f"   ℹ️  没有找到文章\n")
            continue

        max_items = config.get("settings", {}).get("maxItemsPerFeed", 5)
        new_count = 0

        for entry in entries[:max_items]:
            entry_id = entry.get('id')

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

        print(f"   ✅ 发现 {new_count} 篇新文章\n")

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
    from datetime import timedelta
    now_utc = datetime.now(timezone.utc)
    now_cn = now_utc + timedelta(hours=8)

    report_lines = [
        f"# 📰 RSS 阅读摘要",
        f"",
        f"**时间**: {now_cn.strftime('%Y-%m-%d %H:%M')} (北京时间)",
        f"**新文章**: {len(new_entries)} 篇",
        f""
    ]

    include_categories = config.get("settings", {}).get("includeCategories", ["全部"])

    for category in sorted(by_category.keys()):
        if "全部" not in include_categories and category not in include_categories:
            continue

        report_lines.append(f"\n---\n")
        report_lines.append(f"## 📂 {category}\n")

        for entry in by_category[category]:
            report_lines.append(entry["content"])
            report_lines.append("")

    return "\n".join(report_lines)


def main():
    """主函数"""
    print("="*60)
    print("📡 RSS 阅读器")
    print("="*60 + "\n")

    # 加载配置
    config = load_config()
    if not config:
        print("❌ 配置文件不存在，请先创建 rss-feeds.json")
        sys.exit(1)

    # 加载状态
    state = load_state()
    last_check = state.get("last_check")
    if last_check:
        print(f"📅 上次检查: {last_check}\n")

    # 检查订阅
    new_entries = check_feeds(config, state)

    # 生成报告
    if new_entries:
        print(f"\n{'='*60}")
        print(f"✅ 总共发现 {len(new_entries)} 篇新文章")
        print(f"{'='*60}\n")

        report = generate_report(new_entries, config)

        if report:
            # 保存报告
            report_file = Path(__file__).parent.parent / "rss-report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"📝 报告已保存到: {report_file}")
            print(f"\n💡 告诉我 '发送 RSS 报告' 即可推送到飞书\n")
    else:
        print("\n✅ 没有新文章\n")


if __name__ == "__main__":
    main()
