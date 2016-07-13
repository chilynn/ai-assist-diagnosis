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
						callback=lambda response, department=department_cn:self.parsePageNum(response, department)
					)
				)
			return requests

	# 提取有多少分页
	def parsePageNum(self, response, department):
		page_text = response.xpath("//span[@class='res_page']/text()").extract()[0]
		page_num = int(page_text.split('/')[1])
		for page_index in range(page_num):
			# if page_index >= 1:
			# 	break
			url = "http://jbk.39.net/bw/erke_t2_p"+str(page_index)
			yield Request(
				url=url,
				callback=lambda response, department=department:self.parsePageItem(response, department)
			)

	# 处理每个分页
	def parsePageItem(self, response, department):
		for a in response.xpath("//dt[@class='clearfix']//h3/a"):
			symptom_cn = a.xpath("text()").extract()[0].strip()
			href = a.xpath("@href").extract()[0].strip()
			symptom = SymptomItem()
			symptom["name"] = symptom_cn
			symptom["department"] = department
			# 处理“症状简介”页
			url = href
			yield Request(
				url=url,
				callback=lambda response, href=href, symptom=symptom:self.parseSymptonIntro(response, href, symptom)
			)	

	# 处理“症状简介”页
	def parseSymptonIntro(self, response, href, symptom):
		intro = ''.join(response.xpath("//dd[@id='intro']/p[@class='sort2']/text()").extract())
		relevant_diseases = response.xpath("//td[@class='name']/a/text()").extract()
		symptom["intro"] = intro
		symptom["relevant_diseases"] = relevant_diseases

		# 处理“症状起因”页
		url = href + "zzqy"	
		yield Request(
			url=url,
			callback=lambda response, href=href, symptom=symptom:self.parseSymptonReason(response, href, symptom)
		)	

	# 处理“症状起因”页
	def parseSymptonReason(self, response, href, symptom):
		reason = ''.join(response.xpath("//div[@class='item catalogItem']//text()").extract())
		symptom["reason"] = reason

		# 处理“诊断详述”页
		url = href + "zdxs"	
		yield Request(
			url=url,
			callback=lambda response, href=href, symptom=symptom:self.parseSymptonDiagnosis(response, href, symptom)
		)	

	# 处理“症状起因”页
	def parseSymptonDiagnosis(self, response, href, symptom):
		diagnosis_description = ''.join(response.xpath("//div[@class='item catalogItem']//text()").extract())
		symptom["diagnosis_description"] = diagnosis_description
		
		# 处理“鉴别检查”页
		url = href + "jcjb"	
		yield Request(
			url=url,
			callback=lambda response, href=href, symptom=symptom:self.parseSymptonExamination(response, href, symptom)
		)	

	# 处理“鉴别检查”页
	def parseSymptonExamination(self, response, href, symptom):
		symptom["examinations"] = response.xpath("//div[@class='checkbox-data']//td//a/text()").extract()[::2]
		symptom["similar_symptoms"] = response.xpath("//ul[@id='symList']//dt//text()").extract()
		yield symptom


