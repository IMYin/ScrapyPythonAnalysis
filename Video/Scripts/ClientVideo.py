#*-coding=utf-8-*-
"""
此程序为了下载视频，以及其他一些视频

"""
from urlparse import urlparse
from urllib import urlretrieve
from urllib import quote
from urllib import urlencode
from bs4 import BeautifulSoup
import datetime
import cookielib
import os
import re
import json
import binascii
import rsa
import base64
import sys
import requests
import random
import urllib2

logging_path = os.getenv('LOGGING_PATH')
sys.path.append(logging_path)

from JobLogging import JobLogging

class ClientVideo:

    #实例化日志
    def __init__(self, log_lev = 'INFO',username=None, password=None):
        date_today = datetime.datetime.now().date()
        log_name = os.path.splitext( os.path.split( sys.argv[0])[1])[0]
        log_dir = os.getenv('TASK_LOG_PATH_VIDEO')
        if  log_dir is None:
            log_dir = '/home/sunnyin/Project/Python/ProjectOfSelf/Video/logs'
        log_dir += '/' + date_today.strftime("%Y%m%d")
        if not os.path.isdir(log_dir):
            try:
                os.makedirs(log_dir)
            except :
                pass
        mylog = JobLogging(log_name,log_dir)
        self.log = mylog.get_logger()
        self.log.info("Log create success")
        self.password = password
        self.username = username
        self.data = self.get_prelogin_args()
        self.post_data = self.build_post_data(self.data)
        self.log.info("The post data is ready.")

    def get_prelogin_args(self):

        '''
        该函数用于模拟预登录过程,并获取服务器返回的 nonce , servertime , pub_key 等信息
        '''
        json_pattern = re.compile('\((.*)\)')
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&' + self.get_encrypted_name() + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            raw_data = response.read().decode('utf-8')
            json_data = json_pattern.search(raw_data).group(1)
            data = json.loads(json_data)
            return data
        except urllib.error as e:
            print("%d"%e.code)
            return None

    def get_encrypted_pw(self,data):
        """
        用户编译密码
        """

        rsa_e = 65537 #0x10001
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'],16),rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''   #清空password
        passwd = binascii.b2a_hex(pw_encypted)
        self.log.info("Password compilation completed...")
        # print(passwd)
        return passwd

    def get_encrypted_name(self):
        """
        用户编译用户名
        """

        username_urllike   = quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike))
        self.log.info("The user name complication completed...")
        return username_encrypted.decode('utf-8')


    def enableCookies(self):
            #建立一个cookies 容器
            cookie_container = cookielib.CookieJar()
            #将一个cookies容器和一个HTTP的cookie的处理器绑定
            cookie_support = urllib2.HTTPCookieProcessor(cookie_container)
            #创建一个opener,设置一个handler用于处理http的url打开
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            #安装opener，此后调用urlopen()时会使用安装过的opener对象
            urllib2.install_opener(opener)


    def build_post_data(self,raw):
        post_data = {
            "entry":"weibo",
            "gateway":"1",
            "from":"",
            "savestate":"7",
            "useticket":"1",
            "pagerefer":"http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14",
            "vsnf":"1",
            "su":self.get_encrypted_name(),
            "service":"miniblog",
            "servertime":raw['servertime'],
            "nonce":raw['nonce'],
            "pwencode":"rsa2",
            "rsakv":raw['rsakv'],
            "sp":self.get_encrypted_pw(raw),
            "sr":"1280*800",
            "encoding":"UTF-8",
            "prelt":"77",
            "url":"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype":"META"
        }
        data = urlencode(post_data).encode('utf-8')
        return data


    #尝试连接
    def conn(self,ipList,userAgent):
        """
        如果连接不成功，则换一个proxyIP和user-agent，重新连接。
        """
        proxies = {}
        headers = {}
        iplist = random.choice(ipList)
        self.log.info("select "+iplist+" as the proxy IP.")
        #在请求头池内随机选择一个请求头
        headers['User-Agent'] = random.choice(userAgent)
        self.log.info("select "+headers['User-Agent']+" as the user-agent.")

        #登陆微博的第一层网页
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        
        try:
            request = urllib2.Request(url=url,data=self.post_data,headers=headers)
            # request.set_proxy(iplist,'http')
            response = urllib2.urlopen(request)
            html = response.read().decode('GBK')
            '''
            一开始用的是utf－8解码，然而得到的数据很丑陋，却隐约看见一个GBK字样。所以这里直接采用GBK解码
            '''
            self.log.info("The address is connected.")
            # print(html)
            return html

        except Exception as e:
            self.log.warn("The proxy IP "+iplist+" is not working...\n Try again...")
            self.conn(ipList,userAgent)
    def login(self,ipList,userAgent):
        self.enableCookies()
        #尝试连接
        html = self.conn(ipList,userAgent)

        p = re.compile('location\.replace\(\'(.*?)\'\)')
        p2 = re.compile(r'"userdomain":"(.*?)"')

        try:
            login_url = p.search(html).group(1)            
            request = urllib2.Request(login_url)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            self.log.info("Jumping page....")
            # print(page)
            login_url = 'http://weibo.com/' + p2.search(page).group(1)
            self.log.info("Jumping page again...")
            # print(login_url)
            request = urllib2.Request(login_url)
            response = urllib2.urlopen(request)
            bsObj = BeautifulSoup(response,"html.parser")
            # print(bsObj.text)
            self.log.info("Login success!")
            return bsObj
        except Exception as e:
            self.log.error('Login error!')
            self.log.error("\n"+e.message)
            self.login(ipList,userAgent)            