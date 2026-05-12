"""爆款原因分析 + 视频优化建议"""

from config import PRIORITY_TAGS


def hot_reason(v: dict) -> str:
    """基于视频数据指标生成爆款原因"""
    reasons = []
    views = v["播放量"]
    likes = v["点赞量"]
    comments = v["评论数"]
    shares = v["分享数"]
    favorites = v["收藏数"]
    duration = v.get("时长(秒)", 0)

    like_rate = likes / max(views, 1)
    comment_rate = comments / max(views, 1)

    if views >= 5_000_000:
        reasons.append("播放量超500万(现象级传播)")
    elif views >= 1_000_000:
        reasons.append("播放量破百万")
    elif views >= 500_000:
        reasons.append("播放量超50万")

    if like_rate > 0.10:
        reasons.append("超高点赞率(>10%)")
    elif like_rate > 0.05:
        reasons.append("高点赞率(>5%)")

    if comments >= 2000:
        reasons.append("评论区互动火爆(2000+评论)")
    elif comments >= 500:
        reasons.append("评论区活跃(500+评论)")

    if shares >= 1000:
        reasons.append("分享传播力强(1000+分享)")

    if favorites >= 5000:
        reasons.append("收藏价值极高(5000+收藏)")

    if not reasons:
        if views >= 100000:
            reasons.append("播放量稳定增长，综合数据平衡")
        else:
            reasons.append("精准定位目标受众，互动转化率高")

    return "；".join(reasons)


def improve_suggestion(v: dict) -> str:
    """基于数据短板和内容类型生成优化建议"""
    suggestions = []
    tag = v.get("标签", "")
    views = v["播放量"]
    likes = v["点赞量"]
    comments = v["评论数"]
    shares = v["分享数"]
    favorites = v["收藏数"]
    duration = v.get("时长(秒)", 0)

    like_rate = likes / max(views, 1)
    comment_rate = comments / max(views, 1)

    # 内容类型建议
    if tag in PRIORITY_TAGS:
        suggestions.append("单机/主机游戏热度持续走高，建议选题紧跟新游发布或经典IP二创")
    elif tag == "电子竞技":
        suggestions.append("电竞赛事热度高，建议跟进热门赛事节点制作复盘或高光集锦")
    elif tag in ("手机游戏", "网络游戏"):
        suggestions.append("手游/网游受众广，建议突出操作技巧或剧情解说差异化")

    # 互动率短板
    if like_rate < 0.03 and views > 50000:
        suggestions.append("点赞率偏低，建议在视频中段加入引导互动的话术或彩蛋")

    if comment_rate < 0.005 and views > 50000:
        suggestions.append("评论互动偏少，建议结尾设置争议话题或投票引导讨论")

    if shares < 100 and views > 100000:
        suggestions.append("分享量不足，建议增加转发抽奖或制作更具传播性的短片段")

    if favorites < 500 and views > 100000 and tag in PRIORITY_TAGS:
        suggestions.append("收藏偏低，单机攻略类内容建议提供完整的技巧总结以提升收藏率")

    # 时长建议
    if duration > 900 and views < 500000:
        suggestions.append("视频时长超过15分钟，建议精简至8-12分钟以提升完播率")
    elif 60 < duration < 180 and views > 500000:
        suggestions.append("短视频爆发力强，可制作系列化内容延续热度")

    if not suggestions:
        suggestions.append("各项数据均衡优秀，建议保持内容风格持续产出，巩固粉丝基础")

    return "；".join(suggestions[:4])


def analyze_videos(videos: list[dict]) -> list[dict]:
    """为视频列表添加爆款原因和优化建议"""
    for v in videos:
        v["爆款原因"] = hot_reason(v)
        v["优化建议"] = improve_suggestion(v)
    return videos
