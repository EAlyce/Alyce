import json
import aiohttp
import os
from pathlib import Path

import json
import aiohttp
import os
import hashlib
import subprocess
from pathlib import Path

# 支持多市场源
PLUGIN_MARKET_URLS = [
    'https://github.com/EAlyce/conf/raw/refs/heads/main/PagerMaid/plugin/list.json',
    # 可添加更多市场源
]
LOCAL_MARKET = Path(__file__).parent / 'plugin_market.json'

async def fetch_market():
    # 优先本地，失败则远程
    if LOCAL_MARKET.exists():
        with open(LOCAL_MARKET, 'r', encoding='utf-8') as f:
            return json.load(f)
    for url in PLUGIN_MARKET_URLS:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception:
            continue
    return {}

def check_signature(path, expected_sha256):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)
    actual = sha256.hexdigest()
    return actual.lower() == (expected_sha256 or '').lower()

async def install_dependencies(deps):
    if not deps:
        return True
    if isinstance(deps, str):
        deps = [deps]
    try:
        proc = await asyncio.create_subprocess_exec(
            'pip3', 'install', *deps,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        return proc.returncode == 0
    except Exception:
        return False

def check_permissions(plugin_info, user_permissions):
    # 插件声明 permissions: ['admin', 'read_file', ...]
    # user_permissions 由 Alyce 系统提供
    required = set(plugin_info.get('permissions', []))
    return required.issubset(set(user_permissions))

async def download_plugin(plugin_info, target_dir):
    url = plugin_info['url']
    filename = plugin_info.get('filename') or url.split('/')[-1]
    path = Path(target_dir) / filename
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as resp:
            if resp.status == 200:
                with open(path, 'wb') as f:
                    f.write(await resp.read())
                # 签名校验
                if plugin_info.get('signature'):
                    if not check_signature(path, plugin_info['signature']):
                        os.remove(path)
                        return None, '签名校验失败'
                # 自动依赖安装
                if plugin_info.get('dependencies'):
                    ok = await install_dependencies(plugin_info['dependencies'])
                    if not ok:
                        return None, '依赖安装失败'
                return path, None
    return None, '下载失败'
