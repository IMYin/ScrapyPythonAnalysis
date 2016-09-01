#-*-conding=utf-8-*-

from Client import VoaClient
from urlparse import urlparse
import os,datetime

timeNow = datetime.datetime.now().strftime('%Y%m%d%H')
client = VoaClient()
url = "http://www.51voa.com/VOA_Special_English/"
urlScheme = urlparse(url).scheme 
urlNet = urlparse(url).netloc  
ipList = client.ipList()
userAgent = client.userAgent()
bsObj_proxy = client.conn(url,ipList,userAgent)

urls = client.urls(bsObj_proxy)

for _ in urls:
    url_voa = urlScheme + "://" + urlNet + url
    bsObj_voa = client.conn(url_voa,ipList,userAgent)
    contents = client.getContents(bsObj_voa)
    file = open("/home/sunyin/Data/"+timeNow,'a+')
    for _ in contents:
        file.write(str(_))

file.close()
