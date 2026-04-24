"""
飞书通知模块
发送早报更新通知到飞书
"""

import logging

logger = logging.getLogger(__name__)


class FeishuNotifier:
    """飞书通知器"""
    
    def __init__(self):
        pass
    
    def send_notification(self, report_path: str, date: str, success: bool = True):
        """发送通知"""
        from hermes_tools import send_message
        
        if success:
            message = f"""✅ AI 日报已更新
📅 日期：{date}
🔗 查看：file://{report_path}"""
        else:
            message = f"""❌ AI 日报更新失败
📅 日期：{date}
请检查日志"""
        
        try:
            send_message(message=message, target="feishu:oc_f4e9efc6365614e5bbb4aae76014bc90")
            logger.info("飞书通知发送成功")
        except Exception as e:
            logger.error(f"飞书通知发送失败：{e}")
