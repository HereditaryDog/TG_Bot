# Telegram 机器人项目

这个项目是一个Telegram机器人，利用Python编写，能够从CoinMarketCap获取加密货币的信息，并通过Telegram机器人接口与用户互动。

## 功能

- `/start`：显示市值排名前30的加密货币信息。
- `/price [币种名称或符号]`：显示指定加密货币的当前价格、市值和24小时交易量。
- `/info [币种名称或符号]`：显示指定加密货币的详细信息。
- `/airdrops`：显示当前进行中的空投活动信息。

## 开始使用

要使用这个Telegram机器人，您需要先在Telegram上创建一个机器人并获取您的机器人Token，还需要一个CoinMarketCap的API密钥。

### 准备

1. 在 [Telegram BotFather](https://t.me/botfather) 创建您的机器人并获取`TOKEN`。
2. 注册 [CoinMarketCap API](https://coinmarketcap.com/api/) 并获取`API_KEY`。

### 安装

克隆此仓库到您的本地或服务器：

```bash
git clone https://github.com/yourusername/yourrepositoryname.git
cd yourrepositoryname

安装所需的依赖：
pip install -r requirements.txt

在TG_Bot_2_Complete.py文件中，替换以下行为您的实际值：
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token_here'
COINMARKETCAP_API_KEY = 'your_coinmarketcap_api_key_here'

运行机器人：
python TG_Bot_2_Complete.py
