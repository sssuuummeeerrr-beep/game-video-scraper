"""B站游戏分区热门视频抓取 — 免费公开API，无需登录"""

import requests
from datetime import datetime
from config import MAX_VIDEOS_PER_SOURCE

BILIBILI_POPULAR_API = "https://api.bilibili.com/x/web-interface/popular"
GAMING_RID = 4  # 游戏分区 ID

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


def fetch_bilibili_hot(max_count: int = MAX_VIDEOS_PER_SOURCE) -> list[dict]:
    """抓取B站游戏分区热门视频，返回标准化字段列表"""
    videos = []
    page = 1
    while len(videos) < max_count:
        params = {"ps": 50, "pn": page, "rid": GAMING_RID}
        resp = requests.get(BILIBILI_POPULAR_API, params=params, headers=HEADERS, timeout=15)
        data = resp.json()

        if data.get("code") != 0:
            break

        items = data["data"].get("list") or []
        if not items:
            break

        for v in items:
            stat = v.get("stat", {})
            owner = v.get("owner", {})
            videos.append({
                "source": "B站",
                "video_id": v.get("bvid", ""),
                "title": v.get("title", ""),
                "author": owner.get("name", ""),
                "play_count": stat.get("view", 0),
                "like_count": stat.get("like", 0),
                "comment_count": stat.get("reply", 0),
                "share_count": stat.get("share", 0),
                "favorite_count": stat.get("favorite", 0),
                "duration_sec": v.get("duration", 0),
                "tags": v.get("tname", ""),
                "url": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

        page += 1

    return videos[:max_count]
