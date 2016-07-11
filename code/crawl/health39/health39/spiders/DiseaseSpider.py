#encoding=utf-8

import scrapy
import copy
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from health39.items import *

# 爬取命令： scrapy crawl health39_disease -o disease.json -t jsonlines
class MedicalSpider(BaseSpider):
	name = "health39_disease"
	domian = ["39.net"]
	
	# 爬虫入口函数
	def start_requests(self):
		requests = []
		# 科室列表
		with open("list.csv", "rb") as infile:
			for row in infile:
				row = row.strip().decode("utf-8")
				department_cn = row.split(',')[0]
				department_en = row.split(',')[1]
				request_url = u"http://jbk.39.net/bw/"+department_en+"_t1"
				requests.append(
					scrapy.FormRequest(
						request_url, 
						callback=lambda response, department=department_cn:self.parsePageNum(response, department)
					)
				)
				break
			return requests

	# 提取有多少分页
	def parsePageNum(self, response, department):
		page_text = response.xpath("//span[@class='res_page']/text()").extract()[0]
		page_num = int(page_text.split('/')[1])
		for page_index in range(page_num):
			if page_index >= 1:
				break
			url = "http://jbk.39.net/bw/erke_t1_p"+str(page_index)
			yield Request(
				url=url,
				callback=lambda response, department=department:self.parsePageItem(response, department)
			)

	# 处理每个分页
	def parsePageItem(self, response, department):
		for a in response.xpath("//dt[@class='clearfix']//h3/a"):
			disease_cn = a.xpath("text()").extract()[0].strip()
			href = a.xpath("@href").extract()[0].strip()
			disease = DiseaseItem()
			disease["name"] = disease_cn
			disease["alias"] = ""
			disease["department"] = department
			# 疾病知识页（简介）
			url_intro = href + "jbzs"
			yield Request(
				url=url_intro,
				callback=lambda response, href=href, disease=disease:self.parseDiseaseIntro(response, href, disease)
			)			

	# 处理疾病知识页（简介）
	def parseDiseaseIntro(self, response, href, disease):
		intro = response.xpath("//dl[@class='intro']/dd/text()").extract()[0]
		disease["intro"] = intro
		for sel in response.xpath("//div[@class='chi-know']/dl[@class='info']")[:3]:
			for sel2 in sel.xpath("./dd"):
				key = ''.join(sel2.xpath("./i/text()").extract())
				val = ''.join(sel2.xpath("./text()").extract())
				if u"别名" in key:
					disease["alias"] = val.strip()

		# 疾病症状页
		url_symptom = href + "zztz"	
		yield Request(
			url=url_symptom,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseSymptom(response, href, disease)
		)	

	# 处理疾病症状页
	def parseDiseaseSymptom(self, response, href, disease):
		disease["symptoms"] = []
		for sel in response.xpath("//div[@class='chi-know chi-int']/dl[@class='links']//dd"):
			for symptom_name in sel.xpath("./a//text()").extract():
				disease["symptoms"].append(symptom_name.strip())

		# 疾病并发症
		url_complication = href + "bfbz"	
		yield Request(
			url=url_complication,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseComplication(response, href, disease)
		)			

	# 处理疾病并发症
	def parseDiseaseComplication(self, response, href, disease):
		disease["complications"] = []
		for sel in response.xpath("//div[@class='chi-know chi-int']/dl[@class='links']//dd"):
			complications = sel.xpath("./a//text()").extract()
			for comp_disease_name in sel.xpath("./a//text()").extract():
				disease["complications"].append(comp_disease_name.strip())
		yield disease







