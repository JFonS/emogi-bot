import telebot

bot = telebot.TeleBot("179522397:AAFN1XumZ2TFfPkVOM14fO44NXMnttA8NFg")

@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(content_types=['photo'])
def handle_images(message):
    bot.send_message(message.chat.id, "IMATGE")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()