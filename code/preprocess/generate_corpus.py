#encoding=utf-8
import sys
import json
import jieba,jieba.posseg,jieba.analyse
import pickle

def outputSet(records, outfile_name):
	with open("data/" + outfile_name, "wb") as outfile:
		for record in records:
			outfile.write(record + "\r\n")	

def generateText():
	with open("../crawl/health39/crawl_data/disease.json", "rb") as infile,\
		 open ("data/disease.txt", "wb") as outfile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			outfile.write(json_obj["intro"].strip() + "\r\n")

	with open("../crawl/health39/crawl_data/symptom.json", "rb") as infile,\
		 open ("data/symptom.txt", "wb") as outfile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			outfile.write(json_obj["intro"].strip() + "\r\n")

def generateLexicon():
	diseases = set()
	symptoms = set()
	examinations = set()
	with open("../crawl/health39/crawl_data/disease.json", "rb") as infile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			if "..." in json_obj["name"]:
				continue
			diseases.add(json_obj["name"])

	with open("../crawl/health39/crawl_data/symptom.json", "rb") as infile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			symptoms.add(json_obj["name"])
	
	with open("../crawl/health39/crawl_data/examination.json", "rb") as infile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			examinations.add(json_obj["name"])

	with open("data/lexicon.pickle", "wb") as outfile:
		pickle.dump((diseases, symptoms, examinations), outfile)

	outputSet(diseases, "disease.lexicon")
	outputSet(symptoms, "symptom.lexicon")
	outputSet(examinations, "examination.lexicon")

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	generateLexicon()
	generateText()

if __name__ == '__main__':
	main()


