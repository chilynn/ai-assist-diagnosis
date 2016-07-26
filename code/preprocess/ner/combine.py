#encoding=utf-8
import sys
import numpy as np
import re
import pandas as pd
import pickle

def getWords(infile_path):
	words = set()
	with open(infile_path, "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8")
			words.add(row)
	return words

def combine():
	crf_words = getWords("result/crf_new_word.txt")
	hmm_words = getWords("result/hmm_new_word.txt")
	rule_words = getWords("result/rule_new_word.txt")

	intersect_words = crf_words & hmm_words & rule_words
	with open("result/combine_new_word.txt", "wb") as outfile:
		for word in intersect_words:
			outfile.write(word + "\r\n")
	
	intersect_words2 = crf_words & rule_words
	with open("result/combine_new_word2.txt", "wb") as outfile:
		for word in intersect_words2:
			outfile.write(word + "\r\n")	

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	combine()

if __name__ == '__main__':
	main()