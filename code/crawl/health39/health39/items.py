# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 症状
class SymptomItem(scrapy.Item):
	name = scrapy.Field() # 症状名称
	intro = scrapy.Field() # 症状简介
	relevant_diseases = scrapy.Field() # 相关疾病

# 疾病
class DiseaseItem(scrapy.Item):
	name = scrapy.Field() # 疾病名称
	alias = scrapy.Field() # 疾病别名
	department = scrapy.Field() # 所属科室
	intro = scrapy.Field() # 疾病简介
	symptoms = scrapy.Field() # 疾病症状列表
	complications = scrapy.Field() # 疾病并发症列表

# 检查
class ExaminationItem(scrapy.Item):
	name = scrapy.Field() # 检查名称
	alias = scrapy.Field() # 检查别名
	intro = scrapy.Field() # 检查简介
	relevant_diseases = scrapy.Field() # 相关疾病
	relevant_symptoms = scrapy.Field() # 相关症状


