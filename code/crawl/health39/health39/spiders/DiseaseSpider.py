#encoding=utf-8

import scrapy
import copy
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from health39.items import *

# 爬取命令： scrapy crawl health39_disease -o crawl_data/disease.json -t jsonlines
class MedicalSpider(BaseSpider):
	name = "health39_disease"
	domian = ["39.net"]
	
	# 爬虫入口函数
	def start_requests(self):
		requests = []
		# 科室列表
		with open("crawl_list.csv", "rb") as infile:
			for row in infile:
				if "===" in row:
					break			
				row = row.strip().decode("utf-8")
				department_cn = row.split(',')[0]
				department_en = row.split(',')[1]
				request_url = u"http://jbk.39.net/bw/"+department_en+"_t1"
				requests.append(
					scrapy.FormRequest(
						request_url, 
						callback=lambda response, department=department_en:self.parsePageNum(response, department)
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
			url = "http://jbk.39.net/bw/"+department+"_t1_p"+str(page_index)
			yield Request(
				url=url,
				callback=lambda response, department=department:self.parsePageItem(response, department)
			)

	# 处理每个分页，每个分页有10条记录
	def parsePageItem(self, response, department):
		for a in response.xpath("//dt[@class='clearfix']//h3/a"):
			disease_cn = a.xpath("text()").extract()[0].strip()
			href = a.xpath("@href").extract()[0].strip()
			disease = DiseaseItem()
			disease["name"] = disease_cn
			disease["alias"] = ""
			disease["organ"] = ""
			disease["department"] = department
			# 疾病知识页（简介）
			url_intro = href + "jbzs"
			yield Request(
				url=url_intro,
				callback=lambda response, href=href, disease=disease:self.parseDiseaseIntro(response, href, disease)
			)	

	# 处理“疾病简介”页
	def parseDiseaseIntro(self, response, href, disease):
		intro = response.xpath("//dl[@class='intro']/dd/text()").extract()[0]
		disease["intro"] = intro
		for sel in response.xpath("//div[@class='chi-know']/dl[@class='info']//dd"):
			for val in sel.xpath(".//text()").extract():
				if u"别名" in val:
					disease["alias"] = ''.join(sel.xpath("./text()").extract()).strip()
				if u"发病部位" in val:
					disease["organ"] = ''.join(sel.xpath("./a/text()").extract()).strip()

		# 处理“典型症状”页
		url_symptom = href + "zztz"	
		yield Request(
			url=url_symptom,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseSymptom(response, href, disease)
		)	

	# 处理“典型症状”页
	def parseDiseaseSymptom(self, response, href, disease):
		disease["symptoms"] = []
		for sel in response.xpath("//div[@class='chi-know chi-int']/dl[@class='links']//dd"):
			for symptom_name in sel.xpath("./a//text()").extract():
				disease["symptoms"].append(symptom_name.strip())
		disease["symptom"] = ''.join(response.xpath("//div[@class='art-box']//text()").extract())

		# 处理“发病原因”页
		url_complication = href + "blby"	
		yield Request(
			url=url_complication,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseReason(response, href, disease)
		)			

	# 处理“发病原因”页
	def parseDiseaseReason(self, response, href, disease):
		disease["reason"] = ''.join(response.xpath("//div[@class='art-box']//text()").extract())
		
		# 处理“临床检查”页
		url_examination = href + "jcjb"	
		yield Request(
			url=url_examination,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseExamination(response, href, disease)
		)	

	# 处理“临床检查”页
	def parseDiseaseExamination(self, response, href, disease):
		disease["examinations"] = response.xpath("//div[@class='checkbox']//td//a/text()").extract()[::2]
		disease["examination"] = ''.join(response.xpath("//div[@class='art-box']//text()").extract())
		
		# 处理“鉴别”页
		url_treatment = href + "jb"	
		yield Request(
			url=url_treatment,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseIdentification(response, href, disease)
		)	

	# 处理“鉴别”页
	def parseDiseaseIdentification(self, response, href, disease):
		disease["identification"] = ''.join(response.xpath("//div[@class='art-box']//text()").extract())

		# 处理“治疗方法”页
		url_complication = href + "yyzl"	
		yield Request(
			url=url_complication,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseTreatment(response, href, disease)
		)	

	# 处理“治疗方法”页
	def parseDiseaseTreatment(self, response, href, disease):
		disease["treatment"] = ''.join(response.xpath("//div[@class='art-box']//p//text()").extract())

		# 处理“并发症”页
		url_complication = href + "bfbz"	
		yield Request(
			url=url_complication,
			callback=lambda response, href=href, disease=disease:self.parseDiseaseComplication(response, href, disease)
		)		

	# 处理“并发症”页
	def parseDiseaseComplication(self, response, href, disease):
		disease["complications"] = []
		for sel in response.xpath("//div[@class='chi-know chi-int']/dl[@class='links']//dd"):
			complications = sel.xpath("./a//text()").extract()
			for comp_disease_name in sel.xpath("./a//text()").extract():
				disease["complications"].append(comp_disease_name.strip())
		
		yield disease
	


