#encoding=utf-8
import sys
import numpy as np
import re
import pandas as pd
import pickle

model_name = "crf"
test_path = "model/"+model_name+"/"+model_name+".out"

def getLexicon():
	with open("data/lexicon.pickle", "rb") as infile:
		(diseases, symptoms, examinations) = pickle.load(infile)
	return (diseases, symptoms, examinations) 

# input: (sentence = "abcdefg", labels = "OBMEOBE")
# output: ["bcd", "fg"]
def extractEntity(sentence, labels):
	entitys = []
	re_entity = re.compile(r'BM*E')
	m = re_entity.search(labels)
	while m:
		entity_labels = m.group()
		start_index = labels.find(entity_labels)
		entity = sentence[start_index:start_index + len(entity_labels)]
		labels = list(labels)
		# replace the "BM*E" with "OOO..."
		labels[start_index: start_index + len(entity_labels)] = ['O' for i in range(len(entity_labels))]
		entitys.append(entity)
		labels = ''.join(labels)
		m = re_entity.search(labels)
	return entitys

def getPredict():
	print "getting predict"
	X_test = []
	predict_words = set()
	predict = []
	sentence = ""
	labels = ""
	with open(test_path, "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8")
			if row == '':
				entitys = extractEntity(sentence, labels)
				X_test.append(sentence)
				predict.append(' '.join(entitys))
				predict_words |= set(entitys)
				sentence = ""
				labels = ""
			else:
				char = row.split()[0]
				pred = row.split()[2]
				sentence += char
				labels += pred			
	return X_test, predict, predict_words

def outputNewEntity(predict_words, diseases, symptoms, examinations):
	total_entity = diseases | symptoms | examinations
	new_entity = predict_words - total_entity
	with open("result/"+model_name+"_word.txt", "wb") as outfile:
		for word in predict_words:
			outfile.write(word + "\r\n")
	with open("result/"+model_name+"_new_word.txt", "wb") as outfile:
		for new_word in new_entity:
			outfile.write(new_word + "\r\n")

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	(diseases, symptoms, examinations) = getLexicon()
	X_test, pred, predict_words = getPredict()
	outputNewEntity(predict_words, diseases, symptoms, examinations)

if __name__ == '__main__':
	main()
