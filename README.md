# Alyce - Telegram 客户端框架

Alyce 是一个模块化的 Telegram 客户端框架，支持多协议和插件化开发。

## 功能特点

- 支持 Telethon 和 Pyrogram 双协议
- 插件化架构，易于扩展
- 支持代理（MTProto/SOCKS5）
- 配置化管理
- 完善的日志系统

## 快速开始

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/EAlyce/Alyce.git
cd Alyce

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置

1. 复制示例配置文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入您的 Telegram API 凭证：
   ```ini
   API_ID=your_api_id
   API_HASH=your_api_hash
   PHONE=+1234567890  # 带国家区号的手机号
   ```

### 运行

```bash
python -m alyce
```

## 项目结构

```
Alyce/
├── .env.example          # 环境变量示例
├── .gitignore           # Git 忽略规则
├── DEPLOYMENT.md        # 部署文档
├── README.md            # 项目说明
├── requirements.txt     # 项目依赖
├── setup.py             # 打包配置
│
├── alyce/              # 主包
├── api/                # API 接口
├── core/               # 核心功能
├── docs/               # 文档
├── plugins/            # 插件
├── tests/              # 测试
└── utils/              # 工具函数
```

## 插件开发

请参考 `plugins/` 目录下的示例插件。

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
