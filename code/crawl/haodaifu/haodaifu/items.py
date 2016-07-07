# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# class DiseaseItem(scrapy.Item):
# 	name = scrapy.Field() # 疾病名称
# 	description = scrapy.Field() # 疾病简介描述
# 	first_department = scrapy.Field() # 所属一级科室
# 	second_department = scrapy.Field() # 所属二级科室
# 	subcategory = scrapy.Field() # 疾病类型
# 	pathogeny = scrapy.Field() # 病因
# 	symptom = scrapy.Field() # 症状
# 	manifestation = scrapy.Field() # 临床表现
# 	examination = scrapy.Field() # 检查
# 	diagnosis = scrapy.Field() # 临床诊断
# 	treatment = scrapy.Field() # 治疗
# 	prevention = scrapy.Field() # 预防
# 	complication = scrapy.Field() # 并发症（伴随疾病）

class DiseaseItem(scrapy.Item):
	name = scrapy.Field() # 疾病名称
	first_department = scrapy.Field() # 所属一级科室
	second_department = scrapy.Field() # 所属二级科室
	brief = scrapy.Field() # 疾病概述
	detail = scrapy.Field() # 疾病详细描述



