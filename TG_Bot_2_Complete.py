from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import logging
import matplotlib.pyplot as plt
from io import BytesIO

# 设置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TELEGRAM_BOT_TOKEN = '6400857282:AAHqOntMMFP2a570-S4NddDgldO-T8bYwMo'
COINMARKETCAP_API_KEY = '179b6638-9176-4769-a2c1-bdba05160357'

# 初始化Telegram Bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# CoinMarketCap API请求头
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start': '1',
        'limit': '30',
        'sort': 'market_cap',
        'sort_dir': 'desc',
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if data['status']['error_code'] == 0:
        coins = [coin['name'] for coin in data['data']]
        market_caps = [coin['quote']['USD']['market_cap'] for coin in data['data']]

        plt.figure(figsize=(10, 8))
        plt.barh(coins, market_caps, color='skyblue')
        plt.xlabel('Market Cap (USD)')
        plt.title('Top 30 Cryptocurrencies by Market Cap')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
    else:
        await update.message.reply_text("获取数据失败，请稍后再试。")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text('使用方法: /price <币种名称或符号>')
        return

    coin = ' '.join(context.args).upper()
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {'symbol': coin}
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if data['status']['error_code'] == 0 and coin in data['data']:
        coin_data = data['data'][coin]
        price_info = coin_data['quote']['USD']
        message = f"{coin} 当前价格: ${price_info['price']:.2f}\n市值: ${price_info['market_cap']:.2f}\n24小时交易量: ${price_info['volume_24h']:.2f}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("未能获取该币种的价格信息，请检查币种名称或符号是否正确。")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text('使用方法: /info <币种名称或符号>')
        return

    coin = ' '.join(context.args).upper()
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
    parameters = {'symbol': coin}
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if data['status']['error_code'] == 0 and coin in data['data']:
        info = data['data'][coin]
        message = f"名称: {info['name']} ({info['symbol']})\n描述: {info.get('description', '无描述')}\n网站: {info['urls']['website'][0] if info['urls']['website'] else '无'}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("未能获取该币种的信息，请检查币种名称或符号是否正确。")

async def airdrops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrops"
    parameters = {'status': 'active'}
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if data['status']['error_code'] == 0:
        airdrops_data = data['data']
        message = "当前活跃的空投信息:\n" + "\n".join([f"{airdrop['name']} - {airdrop['symbol']}: {airdrop['description']}" for airdrop in airdrops_data])
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("获取空投信息时发生错误，请稍后再试。")

# 注册命令处理器
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("airdrops", airdrops))

# 启动机器人
app.run_polling()
