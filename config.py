import os
from dotenv import load_dotenv

load_dotenv()

# ── 飞书 ──
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
BITABLE_APP_TOKEN = os.getenv("BITABLE_APP_TOKEN", "")
BITABLE_TABLE_ID = os.getenv("BITABLE_TABLE_ID", "")

# ── 抖音 (第三方API，可选) ──
DOUYIN_API_KEY = os.getenv("DOUYIN_API_KEY", "")
DOUYIN_API_SECRET = os.getenv("DOUYIN_API_SECRET", "")

# ── B站游戏标签 (只保留这些子分类的视频) ──
BILIBILI_GAMING_TAGS = {
    "单机游戏", "主机游戏", "电子竞技", "网络游戏", "手机游戏",
    "音游", "游戏资讯", "桌游棋牌", "游戏赛事",
    "MMD·3D", "游戏配音", "游戏集锦", "游戏杂谈",
}

# 单机/主机游戏权重 50%，其余游戏类型合计 50%
PRIORITY_TAGS = {"单机游戏", "主机游戏"}
PRIORITY_RATIO = 0.5

# ── 抓取配置 ──
MAX_VIDEOS_PER_SOURCE = 50          # 每个数据源最多抓取条数
HOT_THRESHOLD_PLAY_COUNT = 100000   # 播放量 > 10万 视为爆款
HOT_THRESHOLD_LIKE_COUNT = 5000     # 点赞量 > 5000 视为爆款
