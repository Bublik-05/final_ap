from telegram import Bot
import asyncio


token="7581453769:AAEBNxwmaqVUvq_AbP7p1JRhMEJFcCLLaP0"
chat_id="5768005834"

async def send_telegram_alert(message):
    bot = Bot(token)
    await bot.send_message(chat_id, text=message)


async def test():
    await send_telegram_alert("Тестовое сообщение. Если видишь это, бот работает!")

#asyncio.run(test())