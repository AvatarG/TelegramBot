import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from hyperliquid import HyperliquidSync

# Логирование (по желанию)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение цены BTC с Hyperliquid
def get_btc_price():
    try:
        client = HyperliquidSync({})
        data = client.info.getAllMids()
        for item in data:
            if item['feed'] == 'BTC-SPOT':
                return float(item['mid'])
    except Exception as e:
        logger.error(f"Ошибка при получении цены BTC: {e}")
    return None

# Обработка команды /price
async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    if price:
        await update.message.reply_text(f"🟢 Цена BTC на Hyperliquid: ${price:.2f}")
    else:
        await update.message.reply_text("🔴 Не удалось получить цену BTC. Попробуйте позже.")

# Запуск бота
async def main():
    # ЗАМЕНИ ЭТО НА СВОЙ ТОКЕН!
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("price", price_handler))

    logger.info("Бот запущен. Ожидает команду /price...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
