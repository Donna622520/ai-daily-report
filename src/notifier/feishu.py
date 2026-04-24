"""
飞书通知模块
发送早报更新通知到飞书
"""

import logging
import subprocess
import json

logger = logging.getLogger(__name__)


class FeishuNotifier:
    """飞书通知器"""
    
    def __init__(self):
        pass
    
    def send_notification(self, report_path: str, date: str, success: bool = True, news_count: int = 0):
        """发送通知"""
        
        if success:
            message = f"""🤖 **AI 日报 V3 已生成**

📅 **日期**: {date}

📊 **采集结果**:
- 共采集 {news_count} 条新闻
- 交叉验证后剩余有效新闻

✅ **板块状态**:
1. 🔥 今日要闻 - 待采集
2. 🤖 大模型动态 - 待采集
3. 📊 GitHub Trending AI - 待采集
4. 📰 科技媒体精选 - 待采集
5. 💬 社区热议 - 待采集
6. 🎓 学术前沿 - 待采集

📄 **报告链接**: [查看日报](https://github.com/Donna622520/ai-daily-report/blob/master/{report_path})

🔧 **V3 优化**:
- 6 个板块结构
- 未找到板块明确标注
- 飞书消息格式优化"""
        else:
            message = f"""❌ AI 日报更新失败
📅 日期：{date}
请检查日志"""
        
        # 使用 terminal 调用 send_message
        try:
            # 注意：这里需要外部调用 send_message 工具
            # 当前版本暂不支持自动发送，需要手动触发
            logger.info(f"飞书通知准备发送：{date}")
            logger.info(f"报告路径：{report_path}")
            logger.info(f"新闻数量：{news_count}")
        except Exception as e:
            logger.error(f"飞书通知发送失败：{e}")
