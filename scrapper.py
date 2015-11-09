from urllib import request
import urllib.request
from PIL import Image
from PIL import ImageStat

f = open("color2emogi.txt", "w")

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
	print (baseUrl + href)

	emojiStart = emojiPageStr.find("<span class=\"emoji\">") + 20
	emojiEnd = emojiPageStr.find("</span>", emojiStart)
	emoji = emojiPageStr[emojiStart:emojiEnd]

	urlStart = pageStr.find("<img src=\"", urlEnd, end) + 10
	urlEnd = pageStr.find("\"", urlStart, end)
	url = pageStr[urlStart:urlEnd]

	imgFile = request.urlopen(url)
	img = Image.open(imgFile)
	imgStats = ImageStat.Stat(img, img.split()[3])
	f.write(emoji + " " + str(int(imgStats.mean[0])) + " " + str(int(imgStats.mean[1])) + " " + str(int(imgStats.mean[2])) + " // " + str(i) + " " + href[1:-1] + "\n")
	print (emoji + " : " + str(imgStats.mean[0]) + "," + str(imgStats.mean[1]) + ","+ str(imgStats.mean[2])  )
	i = i + 1