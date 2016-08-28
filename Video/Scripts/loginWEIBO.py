#-*-coding=utf-8-*-

"""
登陆微博
"""

from ClientVideo import ClientVideo
from PoolManager import PoolManager
import re

custInfo = ClientVideo(username="txcg777@sina.com",password="xuxu919")
pool = PoolManager()
ipList = pool.ipList()
userAgent = pool.userAgent()
bsObj = custInfo.login(ipList,userAgent)

# content = bsObj.find("div",class_=re.compile("^(\\\")(.*WB_feed_v3)(\\\")")).findAll("div",mrid=re.compile("^(\\\")rid=(.*)"))
# for line in content:
# 	print(line.find("div",class_=re.compile("^(\\\")(WB_text W_f14)(\\\")")).text)

# print(bsObj)
content = bsObj.find("div",{"id","v6_pl_content_homefeed"})
print(content)

