# -*- coding: UTF-8 -*-
from urllib import request
import urllib.request
from PIL import Image
from PIL import ImageStat
import codecs

#f = open("color2emogi.txt", "w")
f = codecs.open("color2emogi-sub.txt", "w", "utf-8")

baseUrl = 'http://emojipedia.org'
url = baseUrl + "/apple/"

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
	

	urlStart = pageStr.find("<img src=\"", urlEnd, end) + 10
	urlEnd = pageStr.find("\"", urlStart, end)
	url = pageStr[urlStart:urlEnd]

	imgFile = request.urlopen(url)
	img = Image.open(imgFile)
	pixels = img.getdata()

	w = int(img.width/2)
	h = int(img.height/2)

	line = emoji + " " 

	for m in range(0,2):
		for n in range(0,2):
			avg = (0,0,0)
			nPixels = 0

			for x in range(m*w, (m+1)*w):
				for y in range(n*h, (n+1)*h):
					# print(x, y, "pos")
					pixel = img.getpixel((x,y))
					nPixels = nPixels + 1
					if pixel[3] < 10:
						avg = (avg[0] + 255, avg[1] + 255, avg[2] + 255)
					else:
						avg = (avg[0] + pixel[0], avg[1] + pixel[1], avg[2] + pixel[2])
		
			avg = (float(avg[0])/float(nPixels),
			   	   float(avg[1])/float(nPixels),
			   	   float(avg[2])/float(nPixels))
			line += str(int(avg[0])) + " " + str(int(avg[1])) + " " + str(int(avg[2])) + " "
			print(n, m, avg)			

		

	print (str(i) + " -> " +  href[1:-1] + "   " + str(int(avg[0])) + "   " + str(int(avg[1])) + "   " + str(int(avg[2])))

	line += " // " + str(i) + " " + href[1:-1] + "\n"
	f.write(line)
	i = i + 1