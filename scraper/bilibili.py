"""B站游戏分区热门视频抓取 — 免费公开API，无需登录"""

import requests
from datetime import datetime
from config import MAX_VIDEOS_PER_SOURCE, BILIBILI_GAMING_TAGS

BILIBILI_POPULAR_API = "https://api.bilibili.com/x/web-interface/popular"
GAMING_RID = 4  # 游戏分区 ID

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


def fetch_bilibili_hot(max_count: int = MAX_VIDEOS_PER_SOURCE) -> list[dict]:
    """抓取B站游戏分区热门视频，仅保留游戏标签的子分类"""
    videos = []
    page = 1
    max_pages = 20  # 安全上限，避免无限翻页

    while len(videos) < max_count and page <= max_pages:
        params = {"ps": 50, "pn": page, "rid": GAMING_RID}
        resp = requests.get(BILIBILI_POPULAR_API, params=params, headers=HEADERS, timeout=15)
        data = resp.json()

        if data.get("code") != 0:
            break

        items = data["data"].get("list") or []
        if not items:
            break

        for v in items:
            tname = v.get("tname", "")
            if tname not in BILIBILI_GAMING_TAGS:
                continue  # 跳过非游戏标签视频

            stat = v.get("stat", {})
            owner = v.get("owner", {})
            videos.append({
                "来源": "B站",
                "视频ID": v.get("bvid", ""),
                "视频标题": v.get("title", ""),
                "UP主": owner.get("name", ""),
                "播放量": stat.get("view", 0),
                "点赞量": stat.get("like", 0),
                "评论数": stat.get("reply", 0),
                "分享数": stat.get("share", 0),
                "收藏数": stat.get("favorite", 0),
                "时长(秒)": v.get("duration", 0),
                "标签": tname,
                "视频链接": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                "抓取时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

        page += 1

    return videos[:max_count]
