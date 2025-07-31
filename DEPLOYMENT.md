# Alyce 部署指南 (Debian/Ubuntu)

## 1. 服务器准备

### 1.1 系统要求
- Debian 10/11 或 Ubuntu 20.04/22.04
- Python 3.8+
- Git
- pip (Python 包管理器)

### 1.2 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y git python3-pip python3-venv

# 安装系统依赖 (Telethon 需要)
sudo apt install -y python3-dev libffi-dev libssl-dev
```

## 2. 部署 Alyce

### 2.1 克隆仓库

```bash
# 创建项目目录
mkdir -p ~/apps && cd ~/apps

# 克隆代码
# 方法1: 使用 HTTPS (推荐)
git clone https://github.com/yourusername/alyce.git

# 或方法2: 使用 SSH (需要配置 SSH 密钥)
# git clone git@github.com:yourusername/alyce.git

# 进入项目目录
cd alyce
```

### 2.2 创建并激活虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 2.3 安装依赖

```bash
# 安装开发依赖
pip install -e .

# 或安装生产依赖
# pip install .
```

## 3. 配置 Alyce

### 3.1 复制并编辑配置文件

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑配置文件
nano .env
```

修改 `.env` 文件，填入您的 Telegram API 凭证：

```ini
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=+1234567890  # 带国家区号的手机号

# 可选配置
# SESSION_PATH=session  # 会话文件保存目录
# DEBUG=True           # 调试模式
```

## 4. 运行 Alyce

### 4.1 直接运行 (开发模式)

```bash
# 确保在项目根目录
cd ~/apps/alyce

# 激活虚拟环境
source venv/bin/activate

# 运行 Alyce
python -m alyce
```

### 4.2 使用 systemd 服务 (生产环境)

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/alyce.service
```

添加以下内容（根据您的实际路径修改）：

```ini
[Unit]
Description=Alyce Telegram Client
After=network.target

[Service]
User=your_username
WorkingDirectory=/home/your_username/apps/alyce
Environment="PATH=/home/your_username/apps/alyce/venv/bin"
ExecStart=/home/your_username/apps/alyce/venv/bin/python -m alyce
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启用自启动
sudo systemctl enable alyce

# 启动服务
sudo systemctl start alyce

# 查看日志
journalctl -u alyce -f
```

## 5. 登录流程

### 5.1 首次登录

首次运行时，程序会提示您输入验证码：

```
Enter the code you received: 12345  # 输入您收到的验证码
```

如果启用了两步验证，还需要输入密码：

```
Enter your 2FA password: your_2fa_password
```

### 5.2 验证登录状态

成功登录后，您会看到类似以下输出：
```
2023-01-01 12:00:00 - alyce.client.telegram - INFO - Logged in as Your Name (@your_username)
Connected to Telegram! Press Ctrl+C to exit.
```

## 6. 常用命令

### 6.1 启动/停止/重启服务

```bash
# 启动
sudo systemctl start alyce

# 停止
sudo systemctl stop alyce

# 重启
sudo systemctl restart alyce

# 查看状态
systemctl status alyce
```

### 6.2 查看日志

```bash
# 查看实时日志
journalctl -u alyce -f

# 查看最近100行日志
journalctl -u alyce -n 100

# 查看特定时间段的日志
journalctl -u alyce --since "2023-01-01 12:00:00" --until "2023-01-01 13:00:00"
```

## 7. 更新 Alyce

```bash
# 进入项目目录
cd ~/apps/alyce

# 拉取最新代码
git pull

# 更新依赖
source venv/bin/activate
pip install -e .

# 重启服务
sudo systemctl restart alyce
```

## 8. 故障排除

### 8.1 登录问题

- 确保 API ID 和 HASH 正确
- 检查手机号格式是否正确（带国家区号）
- 如果收不到验证码，请检查手机号是否被 Telegram 限制

### 8.2 依赖问题

如果遇到依赖问题，可以尝试：

```bash
# 重新安装依赖
pip install --upgrade -r requirements.txt

# 或重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 8.3 会话文件问题

如果会话出现问题，可以删除会话文件后重新登录：

```bash
# 默认会话文件位置
rm -rf session/*.session
```

## 9. 安全建议

- 不要将 `.env` 文件提交到版本控制
- 使用强密码保护服务器
- 定期备份重要数据
- 使用非 root 用户运行服务
