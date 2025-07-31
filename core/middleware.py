"""
中间件机制框架
支持全局/插件级消息前置处理
"""
from typing import Callable, List, Any

class MiddlewareManager:
    def __init__(self):
        self.middlewares: List[Callable] = []

    def add(self, middleware: Callable):
        self.middlewares.append(middleware)

    async def run(self, *args, **kwargs):
        for mw in self.middlewares:
            await mw(*args, **kwargs)
