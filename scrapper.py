# -*- coding: UTF-8 -*-
from urllib import request
import urllib.request
from PIL import Image
from PIL import ImageStat
import codecs

#f = open("color2emogi.txt", "w")
f = codecs.open("color2emogi.txt", "w", "utf-8")

url = "http://emojipedia.org/apple/"
baseUrl = 'http://emojipedia.org'
myHeaders = {'User-Agent': 'Mozilla/5.0'}

req = request.Request(url, headers=myHeaders)
page = request.urlopen(req)
pageStr = str(page.read())

start = pageStr.find("<ul class=\"emoji-grid\">")
end = pageStr.find("</ul>", start)
 
urlStart = start
urlEnd = start 

i = 0
while (urlStart != 9):
	hrefStart = pageStr.find("<a href=\"", urlEnd, end) + 9 
	hrefEnd = pageStr.find("\"", hrefStart, end)
	href = pageStr[hrefStart:hrefEnd]

	emojiReq  = request.Request(baseUrl + href, headers = myHeaders)
	emojiPage = request.urlopen(emojiReq)
	emojiPageStr = emojiPage.read().decode("utf-8")

	emojiStart = emojiPageStr.find("<h1><span class=\"emoji\">") + 24
	emojiEnd = emojiPageStr.find("</span>", emojiStart)
	emoji = emojiPageStr[emojiStart:emojiEnd]
	print (str(i) + " -> " +  href[1:-1])

	urlStart = pageStr.find("<img src=\"", urlEnd, end) + 10
	urlEnd = pageStr.find("\"", urlStart, end)
	url = pageStr[urlStart:urlEnd]

	imgFile = request.urlopen(url)
	img = Image.open(imgFile)
	pixels = img.getdata()

	avg = (0,0,0)
	nPixels = 0
	#newData = []
	for pixel in pixels:
		nPixels = nPixels + 1
		if pixel[3] < 10:
			avg = (avg[0] + 255, avg[1] + 255, avg[2] + 255)
			#newData.append((255,255,0))
		else:
			avg = (avg[0] + pixel[0], avg[1] + pixel[1], avg[2] + pixel[2])
			#newData.append(pixel)
	#img.putdata(newData)
	#img.show()
	avg = (float(avg[0])/float(nPixels),
		   float(avg[1])/float(nPixels),
		   float(avg[2])/float(nPixels))

	print (avg[0], avg[1], avg[2])
	#imgStats = ImageStat.Stat(img, img.split()[3])	

	line = emoji + " " + str(int(avg[0])) + " " + str(int(avg[1])) + " " + str(int(avg[2])) + " // " + str(i) + " " + href[1:-1] + "\n"
	f.write(line)
	i = i + 1