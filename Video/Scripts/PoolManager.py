#-*-coding=utf-8-*-

"""
为了方便管理代理IP池和user-agent池，编写了此脚本。
"""

from urlparse import urlparse
from urllib import urlretrieve
from bs4 import BeautifulSoup
import random
import datetime
import os
import re
import sys
import requests

logging_path = os.getenv('LOGGING_PATH')
sys.path.append(logging_path)

from JobLogging import JobLogging


class PoolManager():
    """docstring for PoolManager"""
    def __init__(self):
    	print("welcom use the proxies pool.")

    #构建代理IP池
    def ipList(self):
        #将所有的url拼出来。
        url_raw = url = "http://www.mimiip.com/"
        urlList = []
        
        ipDicts = []
        # for x in range(3)[1:]:
        #     url = url_raw + str(x) + "/"
        #     urlList.append(url) 
        # for address in urlList:
        session = requests.Session()
            #添加请求头
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}

        req = session.get(url,headers=headers)
        bsObj = BeautifulSoup(req.text,"html.parser")
            # print(bsObj)

        ipField = bsObj.find("table",{"class":"list"}).findAll("tr")
            # print(ipField)
            #找出所有的IP和PORT
        for content in ipField[1:]:
            ip =   content.find("td",text=re.compile("(\d{1,4}.*)")).text.encode('utf-8')
            port = content.find("td",text=re.compile("^(\d{1,4})$")).text.encode('utf-8')

            ipDicts.append(ip+":"+port)
        return ipDicts


    #构建user-agent池
    def userAgent(self):
        useragent = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11']
        return useragent

    def conn(self,url,ipList,userAgent):
        proxies = {}
        headers = {}
        #在代理ip池内随机抽取一个作为代理ip
        proxies['http'] = random.choice(ipList)
        # self.log.info("select "+proxies['http']+" as the proxy IP.")
        headers['User-Agent'] = random.choice(userAgent)
        # self.log.info("select "+headers['User-Agent']+" as the user-agent.")
        session = requests.Session()
        #添加请求头
        req = session.get(url,headers=headers,proxies=proxies)
        bsObj = BeautifulSoup(req.text,"html.parser")
        if len(bsObj) < 50:
            # self.log.warn("The address is not work,it will try again...")
            conn(url)
        else:
            # self.log.info("It connected with the url.")
            return bsObj
