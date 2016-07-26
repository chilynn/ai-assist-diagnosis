#encoding=utf-8
import sys
import re
import pickle

punctuation_set = set(["，", u"：", ";", ":"])

def isChinese(word):
	for w in word:
		if not(0x4e00<=ord(w)<0x9fa6):
			return False
	return True

def getLexicon():
	with open("../../data/lexicon.pickle", "rb") as infile:
		(diseases, symptoms, examinations) = pickle.load(infile)
	return (diseases, symptoms, examinations) 

def extractWord(diseases, symptoms, examinations):
	words = set()
	with open("../../data/symptom.txt", "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8")
			for val in row.split("、")[1:-1]:
				word = val.strip()
				if 1 < len(word) and len(word) <= 10 and isChinese(word):
					words.add(word)

	with open("../../result/rule_word.txt", "wb") as outfile:
		for word in words:
			outfile.write(word + "\r\n")

	total_entity = diseases | symptoms | examinations
	new_entity = words - total_entity
	
	with open("../../result/rule_new_word.txt", "wb") as outfile:
		for new_word in new_entity:
			outfile.write(new_word + "\r\n")	

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	(diseases, symptoms, examinations) = getLexicon()
	extractWord(diseases, symptoms, examinations)

if __name__ == '__main__':
	main()
