#encoding=utf-8

import scrapy
import copy
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from health39.items import *

# 爬取命令： scrapy crawl health39_symptom -o crawl_data/symptom.json -t jsonlines
class SymptomSpider(BaseSpider):
	name = "health39_symptom"
	domian = ["39.net"]
	
	# 爬虫入口函数
	def start_requests(self):
		requests = []
		# 科室列表
		with open("crawl_list.csv", "rb") as infile:
			for row in infile:
				row = row.strip().decode("utf-8")
				department_cn = row.split(',')[0]
				department_en = row.split(',')[1]
				request_url = u"http://jbk.39.net/bw/"+department_en+"_t2"
				requests.append(
					scrapy.FormRequest(
						request_url, 
						callback=lambda response:self.parsePageNum(response)
					)
				)
				break
			return requests

	# 提取有多少分页
	def parsePageNum(self, response):
		page_text = response.xpath("//span[@class='res_page']/text()").extract()[0]
		page_num = int(page_text.split('/')[1])
		for page_index in range(page_num):
			if page_index >= 1:
				break
			url = "http://jbk.39.net/bw/erke_t2_p"+str(page_index)
			yield Request(
				url=url,
				callback=lambda response:self.parsePageItem(response)
			)

	# 处理每个分页
	def parsePageItem(self, response):
		for a in response.xpath("//dt[@class='clearfix']//h3/a"):
			symptom_cn = a.xpath("text()").extract()[0].strip()
			print symptom_cn
			href = a.xpath("@href").extract()[0].strip()
			symptom = SymptomItem()
			symptom["name"] = symptom_cn
			# 症状简介页
			url = href
			yield Request(
				url=url,
				callback=lambda response, href=href, symptom=symptom:self.parseSymptonIntro(response, href, symptom)
			)	
			break		

	# 处理症状简介页
	def parseSymptonIntro(self, response, href, symptom):
		intro = ''.join(response.xpath("//dd[@id='intro']/p[@class='sort2']/text()").extract())
		relevant_diseases = response.xpath("//td[@class='name']/a/text()").extract()
		symptom["intro"] = intro
		symptom["relevant_diseases"] = relevant_diseases
		yield symptom






