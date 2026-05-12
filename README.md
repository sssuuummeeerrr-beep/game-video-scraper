# 🎮 游戏行业爆款视频抓取 → 飞书多维表格

每天自动抓取 B站/抖音 游戏分区热门视频，筛选爆款后写入飞书多维表格进行分析。

## 项目结构

```
├── main.py              # 主入口：抓取 → 筛选 → 写入
├── config.py            # 配置（阈值、环境变量）
├── feishu_writer.py     # 飞书多维表格 API 写入
├── scraper/
│   ├── bilibili.py      # B站游戏分区热门（免费公开API）
│   └── douyin.py        # 抖音预留（需第三方API Key）
├── .github/workflows/
│   └── daily.yml        # GitHub Actions 每天18:00自动运行
├── requirements.txt
└── .env.example
```

## 你需要做的 2 件事

### 1️⃣ 创建飞书应用（3分钟）

1. 打开 https://open.feishu.cn → 创建「**企业自建应用**」
2. 左侧「**权限管理**」→ 搜索 `bitable` → 开通 `bitable:app` 权限
3. 左上角「**创建版本**」→ 发布应用（需管理员审核通过）
4. 记下「**凭证与基础信息**」页面的 **App ID** 和 **App Secret**

### 2️⃣ 创建多维表格（2分钟）

1. 飞书客户端 → 新建「**多维表格**」
2. 创建以下字段（字段名必须与表格一致）：

| 字段名 | 类型 |
|--------|------|
| source | 文本 |
| video_id | 文本 |
| title | 文本 |
| author | 文本 |
| play_count | 数字 |
| like_count | 数字 |
| comment_count | 数字 |
| share_count | 数字 |
| favorite_count | 数字 |
| duration_sec | 数字 |
| tags | 文本 |
| url | URL |
| fetch_time | 文本 |

3. 复制表格 URL，例如：
   `https://xxx.feishu.cn/base/BASEID?table=tblXXX`
   - **BASEID** 即 `BITABLE_APP_TOKEN`
   - **tblXXX** 即 `BITABLE_TABLE_ID`

### 3️⃣ 配置 GitHub Secrets（2分钟）

在 GitHub 仓库 → Settings → Secrets and variables → Actions → 添加：

| Secret 名称 | 值 |
|-------------|-----|
| `FEISHU_APP_ID` | 飞书应用的 App ID |
| `FEISHU_APP_SECRET` | 飞书应用的 App Secret |
| `BITABLE_APP_TOKEN` | 多维表格的 base_id |
| `BITABLE_TABLE_ID` | 多维表格的 table_id |
| `DOUYIN_API_KEY` | （可选）抖音第三方API Key |
| `DOUYIN_API_SECRET` | （可选）抖音第三方API Secret |

## 本地测试

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入真实的飞书 App ID / Secret / 表格ID

# 3. 运行
python main.py
```

## 定时运行

推送代码到 GitHub 后自动生效。每天北京时间 **18:00** 自动执行。
也可以在 GitHub Actions 页面点 **Run workflow** 手动触发。

## 自定义

`config.py` 中可修改：
- `HOT_THRESHOLD_PLAY_COUNT` — 爆款播放量阈值（默认 10万）
- `HOT_THRESHOLD_LIKE_COUNT` — 爆款点赞量阈值（默认 5000）
- `MAX_VIDEOS_PER_SOURCE` — 每个数据源最大抓取数
