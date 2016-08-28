#-*-coding=utf-8-*-

"""
构建代理IP池，存放在mysql中。
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

class IPProxy():
    """实例化日志输出"""
    def __init__(self, log_lev = 'INFO'):
        date_today = datetime.datetime.now().date()
        log_name = os.path.splitext( os.path.split( sys.argv[0])[1])[0]
        log_dir = os.getenv('TASK_LOG_PATH_VOA')
        if  log_dir is None:
            log_dir = '/home/sunnyin/Project/Python/ProjectOfSelf/VOA/ipProxy'
        log_dir += '/' + date_today.strftime("%Y%m%d")
        if not os.path.isdir(log_dir):
            try:
                os.makedirs(log_dir)
            except :
                pass
        mylog = JobLogging(log_name,log_dir)
        self.log = mylog.get_logger()
        self.log.info("Log create success")

    #构建代理IP池
    def ipList(self):
        #将所有的url拼出来。
        url_raw = url = "http://www.mimiip.com/gngao/"
        urlList = []
        
        ipDicts = {}
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
            # address = content.find("a").text.encode('utf-8')

            ipDicts[ip] = port
        return ipDicts

    def insertTable(self,ipDicts):
        connection = pymysql.connect(host='localhost',
                                     user='hive',
                                     password='hive',
                                     db='ScrapyProxy',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                for ip in ipDicts:
                    sql = "INSERT INTO IPProxy (ip,port) VALUES (%s,%s)"
                    cursor.execute(sql,(ip,ipDicts[ip]))
                    self.log.info("The %s added the table IPProxy" ,ip )
            connection.commit()
        finally:
            connection.close()
            self.log.info("IP Proxy added ip completed,please check it..")

if __name__ == '__main__':
    x = CreateProxy()
    ips = x.ipList()
    x.insertTable(ips)