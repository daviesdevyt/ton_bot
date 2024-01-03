from config import *
from connector import get_connector
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from pytoniq_core import Address
from utils import create_transaction
import pytonconnect


async def start_message(message, connector):
    wallet_address = Address(connector.account.address).to_str(is_bounceable=False)

    await bot.send_message(
        message,
        f"""<b>Wallet Address:</b> <code>{wallet_address}</code>

/buy [amount] - 💹Buy TON

/sell [amount] - 📈Sell TON

/disconnect - 🔌Disconnect @wallet
""")


@bot.message_handler(["start"])
async def start(message):
    connector = get_connector(message.chat.id)
    connected = await connector.restore_connection()
    if connected:
        await start_message(message.chat.id, connector)
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
                    await start_message(message.chat.id, connector)
                return
        await bot.send_message(message.chat.id, f"Timeout error!", reply_markup=kb)


@bot.message_handler(["buy"])
async def buy_ton(message):
    connector = get_connector(message.chat.id)
    await connector.restore_connection()
    if not connector.connected:
        return await start(message)
    amount = message.text.split(" ")[-1]
    try:
        amount = float(amount)
    except ValueError:
        return await bot.send_message(
            message.chat.id, "Amount must be a number!.\nFormat /buy [amount]"
        )

    await bot.send_message(
        message.chat.id, "Approve transaction in your @wallet app!\nYou have 5 minutes⌛"
    )
    try:
        await asyncio.wait_for(
            connector.send_transaction(
                transaction=create_transaction(destination_address, amount)
            ),
            300,
        )
    except asyncio.TimeoutError:
        await bot.reply_to(message, "Timeout error!")
    except pytonconnect.exceptions.UserRejectsError:
        await bot.reply_to(message, "You rejected the transaction!")
    except Exception as e:
        await bot.reply_to(message, f"Unknown error: {e}")

    await bot.send_message(message.chat.id, "Buy TON")


print("Starting...")
asyncio.run(bot.infinity_polling())
