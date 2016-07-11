#encoding=utf-8
import sys
import json
import jieba,jieba.posseg,jieba.analyse

def readJson():
	with open("../crawl/health39/health39.json", "rb") as infile:
		row_index = 0
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			print json_obj["name"]
			print json_obj["alias"]
			print json_obj["intro"]
			print ' '.join(json_obj["symptoms"])
			print ' '.join(json_obj["complications"])
			print "----------"
def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	readJson()


if __name__ == '__main__':
	main()


