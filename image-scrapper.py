# -*- coding: UTF-8 -*-
from urllib import request
import urllib.request
from PIL import Image
from PIL import ImageStat
import codecs

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
	urlStart = pageStr.find("<img src=\"", urlEnd, end) + 10
	urlEnd = pageStr.find("\"", urlStart, end)
	url = pageStr[urlStart:urlEnd]

	imgFile = request.urlopen(url)
	img = Image.open(imgFile)
	img.save("emojis/" + str(i) + ".png")
	print (str(i) + ".png")
	i = i + 1