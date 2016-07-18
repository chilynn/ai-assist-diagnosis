#encoding=utf-8
import sys
import re
import pickle

def extractWord():
	words = []
	with open("../data/symptom.txt", "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8")
			for val in row.split("、")[1:-1]:
				word = val.strip()
				if 1 < len(word) and len(word) <= 10 and u"，" not in word and u"：" not in word and ";" not in word and ":" not in word:
					words.append(val.strip())
	with open("word_rule.txt", "wb") as outfile:
		for word in words:
			outfile.write(word + "\r\n")
def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	extractWord()

if __name__ == '__main__':
	main()
