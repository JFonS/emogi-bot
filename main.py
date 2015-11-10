import telebot
from telebot import util


# Split the text each 3000 characters.
# split_string returns a list with the splitted text.


bot = telebot.TeleBot("179522397:AAFN1XumZ2TFfPkVOM14fO44NXMnttA8NFg")

@bot.message_handler(commands=['test'])
def handle_test(message):
	large_text = open("color2emogi.txt", "r", encoding="utf-8").read()
	splitted_text = util.split_string(large_text, 3000)
	for text in splitted_text:
		bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['photo'])
def handle_images(message):
	bot.send_message(message.chat.id, "IMATGE")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
