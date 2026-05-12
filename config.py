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

# ── 抓取配置 ──
MAX_VIDEOS_PER_SOURCE = 50          # 每个数据源最多抓取条数
HOT_THRESHOLD_PLAY_COUNT = 100000   # 播放量 > 10万 视为爆款
HOT_THRESHOLD_LIKE_COUNT = 5000     # 点赞量 > 5000 视为爆款
