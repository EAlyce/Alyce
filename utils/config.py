"""
配置管理模块
处理环境变量和配置文件
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv


class Config:
    """配置管理类"""
    
    def __init__(self):
        # 加载 .env 文件
        self.env_path = Path('.') / '.env'
        load_dotenv(self.env_path)
        
        # 默认配置
        self._defaults = {
            'API_ID': '',
            'API_HASH': '',
            'PHONE': '',
            'SESSION_STRING': '',  # 可选，用于快速登录
            'SESSION_PATH': 'session',  # 会话文件保存目录
            'DEBUG': 'False',
        }
        
    def get(self, key: str, default: Any = None) -> str:
        """获取配置项"""
        value = os.getenv(key, self._defaults.get(key, default))
        return str(value) if value is not None else ''
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔类型配置"""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 't', 'y', 'yes')
    
    def get_int(self, key: str, default: int = 0) -> int:
        """获取整数类型配置"""
        try:
            return int(self.get(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def get_session_path(self) -> Path:
        """获取会话文件路径"""
        session_dir = Path(self.get('SESSION_PATH'))
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir / 'alyce.session'
    
    def validate(self) -> bool:
        """验证必要配置"""
        required = ['API_ID', 'API_HASH', 'PHONE']
        return all(self.get(key) for key in required)


# 全局配置实例
config = Config()
