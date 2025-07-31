import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.env_path = Path('.') / '.env'
        load_dotenv(self.env_path)
        self._defaults = {
            'API_ID': '',
            'API_HASH': '',
            'PHONE': '',
            'SESSION_STRING': '',
            'SESSION_PATH': 'session',
            'DEBUG': 'False',
        }

    def get(self, key: str, default=None) -> str:
        value = os.getenv(key, self._defaults.get(key, default))
        return str(value) if value is not None else ''

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 't', 'y', 'yes')

    def get_int(self, key: str, default: int = 0) -> int:
        try:
            return int(self.get(key, str(default)))
        except (ValueError, TypeError):
            return default

    def get_session_path(self) -> Path:
        session_dir = Path(self.get('SESSION_PATH'))
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir / 'alyce.session'

    def validate(self) -> bool:
        required = ['API_ID', 'API_HASH', 'PHONE']
        return all(self.get(key) for key in required)

config = Config()