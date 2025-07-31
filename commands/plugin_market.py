import json
import aiohttp
import os
from pathlib import Path

# 示例插件市场，实际可对接远程API
PLUGIN_MARKET_URL = 'https://github.com/EAlyce/conf/raw/refs/heads/main/PagerMaid/plugin/list.json'
LOCAL_MARKET = Path(__file__).parent / 'plugin_market.json'

async def fetch_market():
    # 优先本地，失败则远程
    if LOCAL_MARKET.exists():
        with open(LOCAL_MARKET, 'r', encoding='utf-8') as f:
            return json.load(f)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(PLUGIN_MARKET_URL, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.json()
    except Exception:
        pass
    return {}

async def download_plugin(plugin_info, target_dir):
    url = plugin_info['url']
    filename = plugin_info.get('filename') or url.split('/')[-1]
    path = Path(target_dir) / filename
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as resp:
            if resp.status == 200:
                with open(path, 'wb') as f:
                    f.write(await resp.read())
                return path
    return None
