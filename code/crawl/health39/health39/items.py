# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 症状
class SymptomItem(scrapy.Item):
	name = scrapy.Field() # 症状名称
	department = scrapy.Field() # 所属科室
	intro = scrapy.Field() # 症状简介
	reason = scrapy.Field() # 症状起因
	diagnosis = scrapy.Field() # 诊断描述
	examinations = scrapy.Field() # 检查列表(list)
	relevant_diseases = scrapy.Field() # 相关疾病(list)
	similar_symptoms = scrapy.Field() # 相似症状(list)

# 检查
class ExaminationItem(scrapy.Item):
	name = scrapy.Field() # 检查名称
	alias = scrapy.Field() # 检查别名
	intro = scrapy.Field() # 检查简介
	relevant_diseases = scrapy.Field() # 相关疾病(list)
	relevant_symptoms = scrapy.Field() # 相关症状(list)

# 疾病
class DiseaseItem(scrapy.Item):
	name = scrapy.Field() # 疾病名称
	alias = scrapy.Field() # 疾病别名
	department = scrapy.Field() # 所属科室
	organ = scrapy.Field() # 发病部位
	intro = scrapy.Field() # 疾病简介
	reason = scrapy.Field() # 疾病起因
	symptoms = scrapy.Field() # 疾病症状列表(list)
	symptom = scrapy.Field() # 症状描述
	identification = scrapy.Field() # 疾病鉴别
	examinations = scrapy.Field() # 检查列表(list)
	examination = scrapy.Field() # 检查描述
	complications = scrapy.Field() # 疾病并发症列表(list)
	treatment = scrapy.Field() # 治疗描述


