#-*-coding=utf-8-*-

from ClientDouBan import ClientDouBan

rawUrl = "https://book.douban.com"
tag = raw_input("Please enter the tag of you love: ")
downloadPath = "/home/sunnyin/Project/Python/ProjectOfSelf/DouBan/Data/BookDoubanPicture/" + tag + "/"
client = ClientDouBan()
allOfUrls = client.toNextPage(rawUrl,tag)
for url in allOfUrls:
	client.downloadCover(url,downloadPath)

