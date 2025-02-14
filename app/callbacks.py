from telegram import Bot

def send_telegram_alert(message):
    bot = Bot(token="7581453769:AAEBNxwmaqVUvq_AbP7p1JRhMEJFcCLLaP0")
    bot.send_message(chat_id="5768005834", text=message)
