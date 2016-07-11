#encoding=utf-8

import scrapy
import copy
import re
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from health39.items import *

# 爬取命令： scrapy crawl health39_examination -o crawl_data/examination.json -t jsonlines
class ExaminationSpider(BaseSpider):
	name = "health39_examination"
	domian = ["39.net"]
	
	# 爬虫入口函数
	def start_requests(self):
		requests = []
		request_url = "http://jbk.39.net/jiancha/search/"
		requests.append(
			scrapy.FormRequest(
				request_url, 
				callback=lambda response:self.parsePageNum(response)
			)
		)
		return requests

	# 提取有多少分页
	def parsePageNum(self, response):
		page_text = response.xpath("//span[@class='res_page']/text()").extract()[0]
		page_num = int(page_text.split('/')[1])
		for page_index in range(page_num):
			if page_index >= 1:
				break
			url = "http://jbk.39.net/jiancha/search_p"+str(page_index)
			yield Request(
				url=url,
				callback=lambda response:self.parsePageItem(response)
			)

	# 处理每个分页
	def parsePageItem(self, response):
		for a in response.xpath("//dt[@class='clearfix']//h3/a"):
			examination_cn = a.xpath("text()").extract()[0].strip()
			href = a.xpath("@href").extract()[0].strip()
			examination = ExaminationItem()
			examination["name"] = examination_cn
			examination["alias"] = ""
			# 检查简介页
			url = href
			yield Request(
				url=url,
				callback=lambda response, href=href, examination=examination:self.parseExaminationIntro(response, href, examination)
			)

	# 处理检查简介页
	def parseExaminationIntro(self, response, href, examination):
		examination_name = ''.join(response.xpath("//div[@class='s_con clearfix']//div[@class='tit clearfix']//b/text()").extract())
		examination_alias = ''.join(response.xpath("//div[@class='s_con clearfix']//div[@class='tit clearfix']//span[@class='alias']/text()").extract())
		if examination_alias != "":
			examination["alias"] = ''.join(examination_alias.strip().split(u"别名：")[1][:-1])
		examination["intro"] = ''.join(response.xpath("//div[@id='intro']//text()").extract()).strip()
		examination["relevant_diseases"] = response.xpath("//div[@id='refdisease']//a/text()").extract()
		examination["relevant_symptoms"] = response.xpath("//div[@id='refsymptom']//a/text()").extract()
		yield examination




