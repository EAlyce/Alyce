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
        self._ensure_interactive_config()

    def _ensure_interactive_config(self):
        missing = [k for k in ['API_ID', 'API_HASH', 'PHONE'] if not self.get(k)]
        if missing:
            print("\n[ Alyce 配置向导 | Alyce Config Wizard ]\n")
            print("检测到缺少必要的配置信息，将引导你手动输入并自动保存到 .env 文件。\n")
            new_values = {}
            for key in missing:
                prompt = {
                    'API_ID': '请输入你的 Telegram API_ID: ',
                    'API_HASH': '请输入你的 Telegram API_HASH: ',
                    'PHONE': '请输入你的手机号 (带国家码, 如 +8613800138000): '
                }[key]
                value = ''
                while not value:
                    value = input(prompt).strip()
                new_values[key] = value
            # 保存到 .env
            with open(self.env_path, 'a', encoding='utf-8') as f:
                for k, v in new_values.items():
                    f.write(f"{k}={v}\n")
            print("\n配置信息已保存，下次无需重复输入。\n")
            # 重新加载
            load_dotenv(self.env_path, override=True)

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