#*-coding=utf-8-*-
"""
为了节省自己挑选书籍的时间，所以编写了此程序
有一些模块需要不断调整、升级

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

class ClientDouBan:

    #实例化日志
    def __init__(self, log_lev = 'INFO'):
        date_today = datetime.datetime.now().date()
        log_name = os.path.splitext( os.path.split( sys.argv[0])[1])[0]
        log_dir = os.getenv('TASK_LOG_PATH_DOUBAN')
        if  log_dir is None:
            log_dir = '/home/sunnyin/study/python/Scripts/DouBan/logs'
        log_dir += '/' + date_today.strftime("%Y%m%d")
        if not os.path.isdir(log_dir):
            try:
                os.makedirs(log_dir)
            except :
                pass
#        self.ignore_error = ignore_error
        mylog = JobLogging(log_name,log_dir)
        self.log = mylog.get_logger()
        self.log.info("Log create success")

    	self.ipDicts = self.ipList() 
	self.log.info("ipList is done...")


    #构建代理IP池模板
    def ipList(self):
	url = "http://www.xicidaili.com/nn/1"
	session = requests.Session()
#	proxies = {'http':'http://115.150.14.208:9000'}
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML,like Gecko) Chrome','Connection':'Keep-Alive','Accept-Language':'zh-CN,zh;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept':'*/*','Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','Cache-Control':'max-age=0'}

	req = session.get(url,headers=headers)
	bsObj = BeautifulSoup(req.text,"html.parser")
	ipField = bsObj.find("table",{"id":"ip_list"}).findAll("tr")
	ipDicts = []
	for content in ipField[1:]:
    		ip = content.find("td",text=re.compile("([0-9]{1,4}\.[0-9]{1,4}.*)")).text.encode('utf-8')
   		port = content.find("td",text=re.compile("^([0-9]{1,4})$")).text.encode('utf-8')
    		ipDicts.append(ip+":"+port)
	return ipDicts


    #代理IP池
    def proxiesPool(self,ipDicts):
        proxies = {}
 
        #随机选择一个代理IP
        choice = random.choice(ipDicts)

        proxies['http'] = "http://"+choice
	self.log.info("The IP address is "+choice+" ,now")
        return proxies

    #连接到网络
    def conn(self,url,proxies=None):
        for x in range(8):
            proxies = self.proxiesPool(self.ipDicts)
            session = requests.Session()
            #添加请求头
            headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML,like Gecko) Chrome','Connection':'Keep-Alive','Accept-Language':'zh-CN,zh;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept':'*/*','Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','Cache-Control':'max-age=0'}
            req = session.get(url,headers=headers,proxies=proxies)
            bsObj = BeautifulSoup(req.text,"html.parser")
            if len(bsObj.findAll("li")) < 10:
	            self.log.info("This is the content of bsObj: \n"+ str(bsObj.text)
	            self.log.info("Trying another IP address...")
                continue
            else:
                break
        return bsObj


    #拼出所有的链接地址
    def toNextPage(self,rawUrl,tag):
        pageNum = [x * 20 for x in range(100)]
        rawUrlNet = urlparse(rawUrl).netloc   #身
        rawUrlScheme = urlparse(rawUrl).scheme   #头
        bookLinks = []

        #拼出所有的链接地址
        for item in pageNum:
            url = rawUrlScheme+"://"+rawUrlNet+"/tag/"+tag+"?start="+str(item)+"&type=T"
            bookLinks.append(url)
        return bookLinks

    #下载相关的封面信息
    def downloadCover(self,url,downloadPath):
        #创建文件夹
        if not os.path.isdir(downloadPath):
            try:
                os.makedirs(downloadPath)
                self.log.info("The dictionary create success")
            except:
                pass

        bsObj = self.conn(url)
        #下载文件
        try:
            content = bsObj.find("div",{"id":"subject_list"}).findAll("li",{"class":"subject-item"})
            for link in content:
                score = link.find("span",{"class":"rating_nums"}).text
                if float(score) >= 9.1 :
                    img = link.find("img")
                    img = img.attrs['src']
                    self.log.info("the img's url is:" + str(img))
                    bookName = link.find("a",title=re.compile("(.*)"))
                    bookName = bookName.attrs['title']
                    self.log.info("The book's name is: " + bookName)
                    #下载图片
                    urlretrieve(img,downloadPath+'%s.jpg' % bookName.encode('utf-8') )
                    self.log.info("%s's cover is downloaded...." % bookName)
        except Exception as e:
            self.log.warn("There is no book,see you later ,honey........\n" + e.message)
