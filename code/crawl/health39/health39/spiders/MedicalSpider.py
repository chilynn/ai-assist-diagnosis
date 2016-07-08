#encoding=utf-8

import scrapy
import copy
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from health39.items import DiseaseItem

class MedicalSpider(BaseSpider):
	name = "health39"
	domian = ["39.net"]
	
	# 从列表文件中获取需要爬取的url列表（一级科室列表）
	def start_requests(self):
		requests = []
		with open("list.csv", "rb") as infile:
			for row in infile:
				row = row.strip().decode("utf-8")
				department_cn = row.split(',')[0]
				department_en = row.split(',')[1]
				disease_item = DiseaseItem()
				disease_item["first_department"] = department_cn
				request_url = u"http://jbk.39.net/bw/"+department_en
				requests.append(
					scrapy.FormRequest(
						request_url, 
						callback=lambda response, disease_item=disease_item:self.parseFirstDepartment(response, disease_item)
					)
				)
				break
			return requests

	def 		















