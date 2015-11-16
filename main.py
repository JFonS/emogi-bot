import telebot
import requests
import io
from PIL import Image
import random

bot = telebot.TeleBot("179522397:AAFN1XumZ2TFfPkVOM14fO44NXMnttA8NFg")

color2emoji = []
f = open("color2emogi-sub.txt", "r")
lines = f.readlines()
for line in lines: color2emoji.append(line.split(" "))

def color_to_emoji(color):
	minDist = 9999999999999999
	emoji = "#"
	for e in color2emoji:
		dist = 0
		for suby in range(0,2):
			for subx in range(0,2):
				offset = (subx + 2*suby)*3
				dist += abs(int(color[suby,subx][0]) - int(e[1+offset])) + abs(int(color[suby,subx][1]) - int(e[2+offset])) + abs(int(color[suby,subx][2]) - int(e[3+offset]))
		if dist < minDist or (dist == minDist and random.choice([True, False])):
			minDist = dist
			emoji = (e[0], e[15], e[16])


	return emoji

@bot.message_handler(commands=['help', 'start'])
def help(msg):
        bot.send_message(msg.chat.id, "I convert images to emoji art. Send a picture to me. It only works on mobile devices")

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
	
	nTilesWidth = 14
	tSize  = width / (nTilesWidth*2)
	
	nTilesHeight = int((float(height)/(tSize*2)))
   
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


	nLines = int(50/nTilesWidth)
	print ("NLINES " + str(nLines))
	msg = ""
	dbg_msg = ""
	ty = 0
	while ty < nTilesHeight*2:		
		tx = 0 
		while tx < nTilesWidth*2:
			color = {}
			for suby in range(0,2):
				for subx in range(0,2):
					color[subx,suby] = (tileRGBMeans[tx+subx,ty+suby,0],tileRGBMeans[tx+subx,ty+suby,1],tileRGBMeans[tx+subx,ty+suby,2])
					
			emoji = color_to_emoji(color)
			msg += emoji[0]
			dbg_msg += "//" + emoji[1] + ", " + emoji[2] 
			#print ("  Mean: " + str(tileRGBMeans[tx,ty,0]) + ", " + str(tileRGBMeans[tx,ty,1]) + ", " + str(tileRGBMeans[tx,ty,2]))
			tx += 2

		print(str(ty) + "  =============")

		if (ty/2 % nLines == nLines - 1):
			print(msg)
			print(dbg_msg)
			bot.send_message(message.chat.id, msg)
			msg = ""
			dbg_msg = ""
		else:
			msg += "\r\n"
			dbg_msg += "NEWLINE\r\n"
		ty += 2

	if msg != "": bot.send_message(message.chat.id, msg)


bot.polling()
