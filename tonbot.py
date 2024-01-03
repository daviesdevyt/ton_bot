from config import *
from connector import get_connector
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from pytoniq_core import Address


@bot.message_handler(["start"])
async def start(message):
    connector = get_connector(message.chat.id)
    connected = await connector.restore_connection()
    if connected:
        await bot.send_message(message.chat.id, "Connected!")
    else:
        url = await connector.connect(
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
        await bot.send_message(
            message.chat.id, "Not connected to @wallet!", reply_markup=kb
        )
        for i in range(1, 40):
            await asyncio.sleep(1)
            if connector.connected:
                if connector.account.address:
                    wallet_address = connector.account.address
                    wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                    await bot.reply_to(
                        message,
                        f"You are connected with address <code>{wallet_address}</code>",
                    )
                return
        await bot.send_message(message.chat.id, f"Timeout error!", reply_markup=kb)


print("Starting...")
asyncio.run(bot.infinity_polling())
