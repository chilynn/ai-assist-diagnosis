#encoding=utf-8

import scrapy
import copy
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from haodaifu.items import DiseaseItem

class MedicalSpider(BaseSpider):
	name = "haodaifu"
	domian = ["haodf.com"]

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
				request_url = u"http://www.haodf.com/jibing/"+department_en+"/list.htm"
				requests.append(
					scrapy.FormRequest(
						request_url, 
						callback=lambda response, disease_item=disease_item:self.parseFirstDepartment(response, disease_item)
					)
				)
				break
			return requests

	# 处理一级科室
	def parseFirstDepartment(self, response, disease_item):
		for a in response.xpath("//div[@class='ksbd']//a"):
			href = a.xpath("@href").extract()[0].strip()
			department_cn = a.xpath("text()").extract()[0].strip()
			url = u"http://www.haodf.com"+href
			disease_item_copy = copy.deepcopy(disease_item)
			disease_item_copy["second_department"] = department_cn
			yield Request(
				url=url,
				callback=lambda response, disease_item=disease_item_copy:self.parseSecondDepartment(response, disease_item)
			)
			break

	# 处理二级科室
	def parseSecondDepartment(self, response, disease_item):
		for a in response.xpath("//div[@class='ct']//div[@class='m_ctt_green']//li//a"):
			href = a.xpath("@href").extract()[0].strip()
			disease_cn = a.xpath("text()").extract()[0].strip()
			disease_en = href.split('/')[-1].split('.')[0].strip()
			url = u"http://www.haodf.com/jibing/"+disease_en+"/jieshao.htm"
			disease_item_copy = copy.deepcopy(disease_item)
			disease_item_copy["name"] = disease_cn
			yield Request(
				url=url,
				callback=lambda response, disease_item=disease_item_copy:self.parseDisease(response, disease_item)
			)

	# 处理疾病
	def parseDisease(self, response, disease_item):
		disease_item_copy = copy.deepcopy(disease_item)
		disease_item_copy["detail"] = {}
		for div in response.xpath("//div[@class='recommend_main']"):
			h2 = div.xpath("./h2//text()").extract()[0].strip()
			p = ''.join(div.xpath(".//p/@data-longcontent").extract()).strip()
			disease_item_copy["detail"][h2] = p
		yield disease_item_copy

