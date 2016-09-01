#-*-conding=utf-8-*-

from Client import VoaClient
from urlparse import urlparse
import os,datetime,time

timeNow = datetime.datetime.now().strftime('%Y%m%d%H')
client = VoaClient()

voaUrl = "http://www.51voa.com/"
urlScheme = urlparse(voaUrl).scheme 
urlNet = urlparse(voaUrl).netloc  
ipList = client.ipList()
userAgent = client.userAgent()

num = [x for x in range(16)[1:]]
for _ in num:
    url = "http://www.51voa.com/Technology_Report_"+str(_)+".html"
    bsObj_proxy = client.conn(url,ipList,userAgent)
    urls = client.urls(bsObj_proxy)
    for q in urls:
        url_voa = urlScheme + "://" + urlNet + q
        bsObj_voa = client.conn(url_voa,ipList,userAgent)
        contents = client.getContents(bsObj_voa)
        file = open("/home/sunnyin/Project/Python/ProjectOfSelf/VOA/Data"+timeNow,'a+')
        for word in contents:
            file.write(word.encode('utf-8'))
        file.close()
        time.sleep(2)
