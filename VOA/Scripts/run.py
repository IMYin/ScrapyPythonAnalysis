#-*-conding=utf-8-*-

from Client import VoaClient
from urlparse import urlparse


client = VoaClient()
url = "http://www.51voa.com/VOA_Special_English/"
urlScheme = urlparse(url).scheme 
urlNet = urlparse(url).netloc  
ip = client.ipList()
userAgent = client.userAgent()
bsObj = client.conn(url,ip,userAgent)
# print(bsObj)
urls = client.urls(bsObj)
    url = urlScheme + "://" + urlNet + url
    print(url)