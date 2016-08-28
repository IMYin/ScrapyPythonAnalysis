#-*-coding=utf-8-*-

"""
下载VOA中的文字，存储、自然语言分析。
"""
from urlparse import urlparse
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError,ConnectionError
import chardet
import requests
import os
import re
import sys
import datetime
import random
import pymysql.cursors

logging_path = os.getenv('LOGGING_PATH')
sys.path.append(logging_path)

from JobLogging import JobLogging

class VoaClient():
    """实例化日志输出"""
    def __init__(self, log_lev = 'INFO'):
        date_today = datetime.datetime.now().date()
        log_name = os.path.splitext( os.path.split( sys.argv[0])[1])[0]
        log_dir = os.getenv('TASK_LOG_PATH_VOA')
        if  log_dir is None:
            log_dir = '/home/sunnyin/Project/Python/ProjectOfSelf/VOA/logs'
        log_dir += '/' + date_today.strftime("%Y%m%d")
        if not os.path.isdir(log_dir):
            try:
                os.makedirs(log_dir)
            except :
                pass
        mylog = JobLogging(log_name,log_dir)
        self.log = mylog.get_logger()
        self.log.info("Log create success")

    def ipList(self):
        connection = pymysql.connect(host='localhost',
                                     user='hive',
                                     password='hive',
                                     db='ScrapyProxy',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT ip,port FROM IPProxy"
                x = cursor.execute(sql)
                result = cursor.fetchmany(x) 
                ipList = []
                for word in result:
                    for x in word:
                        ipList.append(word['ip']+":"+word['port'])
        # print ipList[0:4]
        finally:
            connection.close()

        return ipList

    #构建user-agent池
    def userAgent(self):
        useragent = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11']
        return useragent

    def conn(self,url,ipList,userAgent):
        proxies = {}
        headers = {}
        #在代理ip池内随机抽取一个作为代理ip
        proxies['http'] = random.choice(ipList)
        self.log.info("select "+proxies['http']+" as the proxy IP.")
        headers['User-Agent'] = random.choice(userAgent)
        self.log.info("select "+headers['User-Agent']+" as the user-agent.")
        session = requests.Session()
        # 添加请求头

        try:
            req = session.get(url,headers=headers,proxies=proxies)
            bsObj = BeautifulSoup(req.text,"html.parser",from_encoding='utf-8')
            self.log.info("It connected with the url.")
            return bsObj
        except ProxyError as e:
            self.log.warn("The address is not work,it will try again...\n\n"+str(e.message))
            self.conn(url,ipList,userAgent)
        except ConnectionError as e:
            self.log.warn("The address is not work,it will try again...\n\n"+str(e.message))
            self.conn(url,ipList,userAgent)

    def urls(self,bsObj):
        """"获取所有类别的文章url"""
        content = bsObj.find("div",id=re.compile("^(right_box)$")).find("div",id={"list"})
        # print(content)
        urls = []
        address = content.findAll("a")
        for _ in address:
            getone = _.attrs['href']
            self.log.info("Get one url: "+getone+". \nIt's going on...")
            urls.append(getone)
        self.log.info("It's end...")
        return urls


    def getContents(self,bsObj):
        """进入URL，获取所有的语句内容。"""
        content = bsObj.find("div",id={"content"}).findAll("p")
        words = []
        for _ in content:
            word = _.text
            words.append(word)
        return words