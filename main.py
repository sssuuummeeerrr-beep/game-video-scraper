"""主入口 — 抓取B站+抖音游戏爆款视频 → 写入飞书多维表格"""

from scraper import fetch_bilibili_hot, fetch_douyin_hot
from feishu_writer import FeishuBitable
from config import (
    BITABLE_APP_TOKEN, BITABLE_TABLE_ID,
    HOT_THRESHOLD_PLAY_COUNT, HOT_THRESHOLD_LIKE_COUNT,
)


def is_hot(video: dict) -> bool:
    return (
        video["play_count"] >= HOT_THRESHOLD_PLAY_COUNT
        or video["like_count"] >= HOT_THRESHOLD_LIKE_COUNT
    )


def main():
    print("=" * 50)
    print("🎮 游戏行业爆款视频抓取")
    print("=" * 50)

    # ── 1. 抓取 ──
    print("\n📺 抓取 B站 游戏分区热门...")
    bili_videos = fetch_bilibili_hot()
    print(f"   获取 {len(bili_videos)} 条")

    print("📺 抓取 抖音 游戏类热门...")
    douyin_videos = fetch_douyin_hot()
    print(f"   获取 {len(douyin_videos)} 条")

    all_videos = bili_videos + douyin_videos
    if not all_videos:
        print("❌ 未抓取到任何视频，退出")
        return

    # ── 2. 筛选爆款 ──
    hot_videos = [v for v in all_videos if is_hot(v)]
    print(f"\n🔥 筛选出爆款视频: {len(hot_videos)} 条")

    if not hot_videos:
        print("   无爆款视频，跳过写入")
        return

    for i, v in enumerate(hot_videos):
        emoji = "🔥" if v["play_count"] >= 1000000 else "📈"
        print(f"   {i+1}. [{v['source']}] {emoji} {v['title'][:50]} "
              f"| 播放{v['play_count']:,} | 赞{v['like_count']:,}")

    # ── 3. 写入飞书 ──
    print(f"\n📊 写入飞书多维表格...")
    feishu = FeishuBitable()
    count = feishu.append_records(BITABLE_APP_TOKEN, BITABLE_TABLE_ID, hot_videos)
    print(f"✅ 成功写入 {count} 条记录")
    print("=" * 50)


if __name__ == "__main__":
    main()
