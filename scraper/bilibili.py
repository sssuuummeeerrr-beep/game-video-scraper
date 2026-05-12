"""B站游戏分区热门视频抓取 — 免费公开API，无需登录"""

import requests
from datetime import datetime
from config import MAX_VIDEOS_PER_SOURCE, BILIBILI_GAMING_TAGS, PRIORITY_TAGS, PRIORITY_RATIO

BILIBILI_POPULAR_API = "https://api.bilibili.com/x/web-interface/popular"
GAMING_RID = 4  # 游戏分区 ID

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
}


def _build_record(v: dict) -> dict:
    """将单条API数据转为标准记录"""
    stat = v.get("stat", {})
    owner = v.get("owner", {})
    return {
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
        "标签": v.get("tname", ""),
        "视频链接": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
        "抓取时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def fetch_bilibili_hot(max_count: int = MAX_VIDEOS_PER_SOURCE) -> list[dict]:
    """抓取B站游戏分区热门视频，单机/主机占50%，其余游戏类型占50%"""
    priority = []   # 单机/主机游戏
    other = []      # 其他游戏类型
    page = 1
    max_pages = 20

    # 需要的数量：各组目标数 + 一定冗余（因为后续还要过爆款筛选）
    needed = max_count * 2  # 翻倍冗余，确保两组都有足够素材

    while (len(priority) < needed or len(other) < needed) and page <= max_pages:
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
                continue

            record = _build_record(v)
            if tname in PRIORITY_TAGS:
                priority.append(record)
            else:
                other.append(record)

        page += 1

    # 按权重分配
    priority_count = int(max_count * PRIORITY_RATIO)
    other_count = max_count - priority_count

    # 取目标数，不足的从对方组补充
    result = priority[:priority_count] + other[:other_count]
    shortfall = max_count - len(result)
    if shortfall > 0:
        # 从备用池补充
        pool = priority[priority_count:] + other[other_count:]
        result += pool[:shortfall]

    return result[:max_count]
