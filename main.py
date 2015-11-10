import telebot
import requests
import io
from PIL import Image

bot = telebot.TeleBot("179522397:AAFN1XumZ2TFfPkVOM14fO44NXMnttA8NFg")

color2emoji = []
f = open("color2emogi.txt", "r")
lines = f.readlines()
for line in lines: color2emoji.append(line.split(" "))

def color_to_emoji(color):
	minDist = 9999999999999999
	emoji = "#"
	for e in color2emoji:
		dist = abs(int(color[0]) - int(e[1])) + abs(int(color[1]) - int(e[2])) + abs(int(color[2]) - int(e[3]))
		if dist < minDist:
			minDist = dist
			emoji = e[0]
			print(e[5])
	return emoji

@bot.message_handler(content_types=['photo'])
def handle_images(message):
	photo = message.photo[-1]
	imageFilePath = bot.get_file(photo.file_id).file_path
	imageFile = bot.download_file(imageFilePath) #str con caracteres chungos
	f = io.BytesIO(imageFile)
	image = Image.open(f)
	
	width   = int(photo.width)
	height  = int(photo.height)
	print (width, height)
	
	nTilesWidth = 10
	tSize  = width / nTilesWidth
	
	nTilesHeight = int((float(height)/tSize))
   
	pixels = image.getdata()
	x = int(0)
	y = int(0)
	tileRGBMeans = {}
	for pixel in pixels:
		tx = int(x/tSize)
		ty = int(y/tSize)
		
		if (tx,ty,0) in tileRGBMeans: tileRGBMeans[tx,ty,0] += float(pixel[0])/(tSize*tSize) 
		else: tileRGBMeans[tx,ty,0] = 0
		if (tx,ty,1) in tileRGBMeans: tileRGBMeans[tx,ty,1] += float(pixel[1])/(tSize*tSize) 
		else: tileRGBMeans[tx,ty,1] = 0
		if (tx,ty,2) in tileRGBMeans: tileRGBMeans[tx,ty,2] += float(pixel[2])/(tSize*tSize) 
		else: tileRGBMeans[tx,ty,2] = 0

		if x+1 == width: y += 1
		x = int((x+1) % width)

	msg = ""
	for ty in range(nTilesHeight):
		for tx in range(nTilesWidth):
			color = (tileRGBMeans[tx,ty,0],tileRGBMeans[tx,ty,1],tileRGBMeans[tx,ty,2])
			emoji = color_to_emoji(color)
			msg += emoji
			print ("  Mean: " + str(tileRGBMeans[tx,ty,0]) + ", " + str(tileRGBMeans[tx,ty,1]) + ", " + str(tileRGBMeans[tx,ty,2]))
		
		print(str(ty) + "  =============")

		if (ty > 0 and ty < 5 and ty % 4 == 0) or (ty >= 5 and ty % 5 == 4):
			bot.send_message(message.chat.id, msg)
			msg = ""
		else:
			msg += "\r\n"

	if msg != "": bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()