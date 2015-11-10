import telebot
import requests
import io
from PIL import Image

bot = telebot.TeleBot("179522397:AAFN1XumZ2TFfPkVOM14fO44NXMnttA8NFg")

@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(content_types=['photo'])
def handle_images(message):
    imageFilePath = bot.get_file(message.photo[0].file_id).file_path
    imageFile = bot.download_file(imageFilePath) #str con caracteres chungos
    f = io.BytesIO(imageFile)
    image = Image.open(f)
    #pixels = image.getdata()
    #for pixel in pixels:
    #    print (str(pixel[0]) + ", " + str(pixel[1]) + ", " + str(pixel[2]))
    
    bot.send_message(message.chat.id, "IMATGE")
    image = Image.open("trololo.jpeg")
    image.show()


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()