import telebot
import requests
import io
from PIL import Image

bot = telebot.TeleBot("179522397:AAFN1XumZ2TFfPkVOM14fO44NXMnttA8NFg")

@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(content_types=['photo'])
def handle_images(message):
    photo = message.photo[-1]
    imageFilePath = bot.get_file(photo.file_id).file_path
    imageFile = bot.download_file(imageFilePath) #str con caracteres chungos
    f = io.BytesIO(imageFile)
    image = Image.open(f)
    
    width   = int(photo.width)
    height  = int(photo.height)
    
    nTilesWidth = 10
    tWidth  = width / nTilesWidth
    
    nTilesHeight = (height/width) * nTilesWidth
    tHeight =  height / nTilesHeight

    pixels = image.getdata()
    x = 0
    y = 0
    tileRGBMeans = {}
    for pixel in pixels:
        x = int((x+1) % width)
        y = int(x / width)
        tx = x/tWidth
        ty = y/tHeight
        if (tx,ty,0) in tileRGBMeans: tileRGBMeans[tx,ty,0] += float(pixel[0])/(tWidth*tHeight) 
        else: tileRGBMeans[tx,ty,0] = 0
        if (tx,ty,1) in tileRGBMeans: tileRGBMeans[tx,ty,1] += float(pixel[1])/(tWidth*tHeight) 
        else: tileRGBMeans[tx,ty,1] = 0
        if (tx,ty,2) in tileRGBMeans: tileRGBMeans[tx,ty,2] += float(pixel[2])/(tWidth*tHeight) 
        else: tileRGBMeans[tx,ty,2] = 0
    
    for tx in range(nTilesWidth):
        for ty in range(nTilesHeight):
            print ("Mean: " + str(tileRGBMeans[tx,ty,0]) + ", " + str(tileRGBMeans[tx,ty,1]) + ", " + str(tileRGBMeans[tx,ty,2]))
    
    bot.send_message(message.chat.id, "IMATGE")
    #image.show()


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()