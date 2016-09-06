#*-coding=utf-8-*-
"""
download the movie info

"""
from urlparse import urlparse
from urllib import urlretrieve
from bs4 import BeautifulSoup
import requests
import os,re,sys,operator,random,datetime,time,csv

logging_path = os.getenv('LOGGING_PATH')
sys.path.append(logging_path)

from JobLogging import JobLogging

class ClientMovie:

    #init log
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
        mylog = JobLogging(log_name,log_dir)
        self.log = mylog.get_logger()
        self.log.info("Log create success")

    #connection
    def conn(self,url,proxies=None):
        session = requests.Session()
        #add the header
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML,like Gecko) Chrome','Connection':'Keep-Alive','Accept-Language':'zh-CN,zh;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept':'*/*','Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','Cache-Control':'max-age=0'}
        req = session.get(url,headers=headers)
        bsObj = BeautifulSoup(req.text,"html.parser")
        return bsObj

    #all of the urls
    def run(self,rawUrl):
        tags = {'科幻':156,'爱情':377,'喜剧':392,'动画':274,'剧情':392,'科幻':155,'动作':198,'悬疑':209,'青春':160,'犯罪':227,'惊悚':190,'文艺':135,'搞笑':148,'战争':88,'纪录片':260,'励志':81,'短片':174}
        sortedTags = sorted(tags.iteritems(),key=operator.itemgetter(1),reverse=True)
        rawUrlNet = urlparse(rawUrl).netloc   #身
        rawUrlScheme = urlparse(rawUrl).scheme   #头
        movie_urls = []
        for _ in sortedTags:
            pageNum = [x * 20 for x in range(_[1])]
            for item in pageNum:
                tag = _[0].decode('utf-8')
                url = rawUrlScheme+"://"+rawUrlNet+"/tag/"+tag+"?start="+str(item)+"&type=T"
                self.infomation(url,tag)
                self.log.info("The url: "+url+" completed...")
                time.sleep(5)
    def infomation(self,url,tag):
        bsObj = self.conn(url)
        try:
            content = bsObj.findAll("tr",{"class":"item"})
            for _ in content:
                try :
                    score = _.find("span",{"class":"rating_nums"}).text.encode('utf-8')
                except Exception as e:
                    self.log.warn("This film didn't score \n" + e.message )
                    continue

                if float(score) >= 8.0:
                    info = []
                    img = _.find("img").attrs['src'].encode('utf-8')
                    movieName = _.find("a").attrs['title'].encode('utf-8')
                    actors = _.find("p").text.encode('utf-8')
                    actList = actors.split('/')
                    showTime = ""
                    actor = ""
                    for a in actList[:5]:
                        if ")" in a or "(" in a: 
                            showTime += a+" "
                        else:
                            actor += a+" " 
                    info.append(movieName)
                    info.append(tag.encode('utf-8'))
                    info.append(showTime)
                    info.append(actor)
                    info.append(score)
                    info.append(img)
                    fileName = open("/home/sunnyin/Project/Python/ProjectOfSelf/DouBan/Data/Movie/"+tag+".csv",'a+')
                    try:
                        writer = csv.writer(fileName)
                        writer.writerow(info)
                        self.log.info("writing the file: " + tag + ".csv")
                    except Exception as e:
                        self.log.warn("false!!!!!!! \n" + e.message )
                    finally:
                        fileName.close()
        except Exception as e:
            self.log.warn("There is no movie,see you later ,honey........\n" + e.message)
if __name__ == '__main__':
    rawUrl = "https://movie.douban.com"
    ClientMovie.run(rawUrl)