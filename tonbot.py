from config import *
from connector import Connector
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(["start"])
def start(message):
    connector = Connector(message.chat.id)
    connected = connector.restore_connection()
    print(connected)
    if connected:
        bot.send_message(message.chat.id, "Connected!")
    else:
        url = connector.connect(
            {
                "about_url": "https://wallet.tg/",
                "app_name": "telegram-wallet",
                "bridge_url": "https://bridge.tonapi.io/bridge",
                "image": "https://wallet.tg/images/logo-288.png",
                "name": "Wallet",
                "universal_url": "https://t.me/wallet?attach=wallet",
            }
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Connect", url=url))
        bot.send_message(message.chat.id, "Not connected!", reply_markup=kb)

print("Starting...")
bot.infinity_polling()
