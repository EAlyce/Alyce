"""
Alyce 国际化与多语言支持基础结构
"""
import gettext
import os

LOCALE_DIR = os.path.join(os.path.dirname(__file__), '../locales')
LANG = os.environ.get("ALYCE_LANG", "zh_CN")

_trans = gettext.translation('messages', LOCALE_DIR, languages=[LANG], fallback=True)
_ = _trans.gettext

# 用法: _('你好')
