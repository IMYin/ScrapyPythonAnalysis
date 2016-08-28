#-*-coding=utf-8-*-

#from scrapy.slector import Selector
from scrapy import Spider
from test20160531.items import Test20160531Item


class TestSpider(Spider):
	name = "test"
	allowed_domains = ["douban.com"]
	start_urls = ["https://book.douban.com"]

	def parse(self,response):
#		item = Test20160531Item()
#		item['name'] = 
		filename = response.url.split("/")[-1]
		with open(filename,'wb') as f:
			f.write(response.body)
