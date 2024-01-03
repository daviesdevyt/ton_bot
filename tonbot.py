from config import *

@bot.message_handler(['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello!')

bot.infinity_polling()