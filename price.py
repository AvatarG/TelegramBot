import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Логирование (для отладки)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция для получения цены BTC с Hyperliquid
def get_btc_price():
    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "metaAndAssetCtxs"
    }
    response = requests.post(url, json=payload)
    data = response.json()

    for asset in data['assetCtxs']:
        if asset['name'] == 'BTC':
            return float(asset['markPrice'])

    return None

# Обработчик команды /price
async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    if price:
        await update.message.reply_text(f"Текущая цена BTC на Hyperliquid: ${price:.2f}")
    else:
        await update.message.reply_text("Не удалось получить цену BTC.")

# Точка входа
async def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    app.add_handler(CommandHandler("price", price_handler))

    print("Бот запущен...")
    await app.run_polling()

# Запуск
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
