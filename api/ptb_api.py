"""
python-telegram-bot 兼容适配层 Scaffold
"""
from .base import BaseAPI

class PTBAPI(BaseAPI):
    """
    兼容 python-telegram-bot 的 Alyce API 适配器（待完善）
    """
    def __init__(self, client):
        self.client = client
