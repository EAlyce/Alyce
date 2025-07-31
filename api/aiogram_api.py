"""
aiogram 兼容适配层 Scaffold
"""
from .base import BaseAPI

class AiogramAPI(BaseAPI):
    """
    兼容 aiogram 的 Alyce API 适配器（待完善）
    """
    def __init__(self, client):
        self.client = client
