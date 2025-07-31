"""
Alyce main entry module, supports running via 'python -m alyce'
"""

import asyncio
import sys
from main import main as _main

def main():
    """Main function entry point"""
    return asyncio.run(_main())

if __name__ == "__main__":
    sys.exit(main())