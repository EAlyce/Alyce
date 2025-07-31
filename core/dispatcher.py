"""
事件分发与处理机制
支持插件统一注册消息、命令、回调等事件
"""
from typing import Callable, Dict, List, Any

from utils.logging import get_logger
import traceback

class Dispatcher:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.logger = get_logger("alyce.dispatcher")

    def register(self, event: str, handler: Callable):
        """注册事件处理器"""
        self.logger.info(f"注册事件: {event} handler: {handler.__name__}")
        self.handlers.setdefault(event, []).append(handler)

    async def dispatch(self, event: str, *args, **kwargs):
        """分发事件"""
        self.logger.info(f"分发事件: {event} args: {args} kwargs: {kwargs}")
        for handler in self.handlers.get(event, []):
            try:
                await handler(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"事件处理异常: {handler.__name__} - {e}\n{traceback.format_exc()}")
