#encoding=utf-8
import sys
import json
import jieba,jieba.posseg,jieba.analyse
import pickle

def outputSet(records, outfile_name):
	with open("data/" + outfile_name, "wb") as outfile:
		for record in records:
			outfile.write(record + "\r\n")	

def splitCleanOutput(document, outfile):
	document = document.strip()
	sentences = document.split(u"。")
	for sentence in sentences:
		if len(sentence) == 0:
			continue
		sentence_clean = ""
		for w in sentence.strip():
			if w in ["\r", "\n"]:
				continue
			sentence_clean += w
		outfile.write(sentence_clean)
		outfile.write("\r\n")

def generateText():
	with open("../crawl/health39/crawl_data/disease.json", "rb") as infile,\
		 open ("data/disease.txt", "wb") as outfile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			splitCleanOutput(json_obj["intro"], outfile)
			splitCleanOutput(json_obj["reason"], outfile)
			splitCleanOutput(json_obj["symptom"], outfile)
			splitCleanOutput(json_obj["identification"], outfile)

	with open("../crawl/health39/crawl_data/symptom.json", "rb") as infile,\
		 open ("data/symptom.txt", "wb") as outfile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			splitCleanOutput(json_obj["intro"], outfile)
			splitCleanOutput(json_obj["reason"], outfile)
			splitCleanOutput(json_obj["diagnosis"], outfile)

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
			if "..." in json_obj["name"]:
				continue			
			symptoms.add(json_obj["name"])
	
	with open("../crawl/health39/crawl_data/examination.json", "rb") as infile:
		for row in infile:
			json_str = row.strip()
			json_obj = json.loads(json_str)
			if "..." in json_obj["name"]:
				continue			
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


