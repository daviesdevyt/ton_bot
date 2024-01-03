from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os
load_dotenv()

bot = AsyncTeleBot(os.getenv('BOT_TOKEN'), parse_mode="HTML")
manifest_url = os.getenv('MANIFEST_URL')

