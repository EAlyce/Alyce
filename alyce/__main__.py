""
Alyce 主入口模块
支持直接通过 python -m alyce 运行
"""
import asyncio
import sys

from alyce.main import main as _main

def main():
    """主函数入口"""
    return asyncio.run(_main())

if __name__ == "__main__":
    sys.exit(main())
