#encoding=utf-8
import sys
import json
import jieba,jieba.posseg,jieba.analyse

def readJson():
	with open("../crawl/haodaifu/disease_child.json", "rb") as infile:
		row_index = 0
		for row in infile:
			# if row_index > 3:
			# 	break
			json_str = row.strip()
			json_obj = json.loads(json_str)
			print json_obj["name"]
			# print json_obj["first_department"]
			# print json_obj["second_department"]
			for k in json_obj["detail"].keys():
				print k
				print json_obj["detail"][k] 
				break

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	readJson()


if __name__ == '__main__':
	main()


