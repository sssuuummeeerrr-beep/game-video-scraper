"""抖音游戏爆款视频抓取 — 需要第三方数据平台API（蝉妈妈/飞瓜等）

当前为框架代码，接入真实 API Key 后即可使用。

支持的第三方平台：
  - 蝉妈妈 (chanmama.com)  → 抖音数据量最大
  - 飞瓜数据 (feigua.cn)   → 播主分析强
  - 新榜 (newrank.cn)      → 全平台覆盖

接入步骤：
  1. 选定平台，购买 API 套餐（一般 ¥200-500/月）
  2. 获取 API Key / Secret
  3. 填入 .env 文件 DOUYIN_API_KEY / DOUYIN_API_SECRET
  4. 取消下面 fetch_douyin_hot 函数中的注释，按平台文档替换 API 调用
"""

from datetime import datetime
from config import MAX_VIDEOS_PER_SOURCE, DOUYIN_API_KEY, DOUYIN_API_SECRET
import requests


def fetch_douyin_hot(max_count: int = MAX_VIDEOS_PER_SOURCE) -> list[dict]:
    """抓取抖音游戏类爆款视频

    当前返回空列表。接入第三方 API 后取消注释并替换。
    """
    if not DOUYIN_API_KEY:
        print("[douyin] 未配置 API Key，跳过抖音抓取")
        return []

    # ─── 示例：蝉妈妈 API ───
    # url = "https://open.chanmama.com/v1/douyin/video/hot"
    # headers = {
    #     "Authorization": f"Bearer {DOUYIN_API_KEY}",
    #     "Content-Type": "application/json",
    # }
    # params = {
    #     "category": "游戏",
    #     "page_size": max_count,
    #     "sort_by": "play_count",
    # }
    # resp = requests.get(url, headers=headers, params=params, timeout=15)
    # data = resp.json()
    #
    # videos = []
    # for v in data.get("data", {}).get("list", []):
    #     videos.append({
    #         "source": "抖音",
    #         "video_id": v.get("video_id", ""),
    #         "title": v.get("title", ""),
    #         "author": v.get("author_name", ""),
    #         "play_count": v.get("play_count", 0),
    #         "like_count": v.get("like_count", 0),
    #         "comment_count": v.get("comment_count", 0),
    #         "share_count": v.get("share_count", 0),
    #         "favorite_count": 0,  # 抖音无收藏数
    #         "duration_sec": v.get("duration", 0),
    #         "tags": ",".join(v.get("tags", [])),
    #         "url": v.get("share_url", ""),
    #         "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     })
    # return videos[:max_count]

    return []
