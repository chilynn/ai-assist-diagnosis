#encoding=utf-8
import sys
import numpy as np
import pickle

def newWordIdentification():
	word2feature = {}
	with open("data/feature.txt", "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8")
			items = row.split('\t')
			if len(items) != 4:
				continue
			word = items[0]
			fre = float(items[1])
			out = float(items[2])
			inner = float(items[3])
			score = np.log(fre + 1) + out + inner
			word2feature.setdefault(word, [score, fre, out, inner])

	new_words = set()
	sort_list = sorted(word2feature.items(), key=lambda p:p[1], reverse=True)
	for val in sort_list[:2000]:
		new_words.add(val[0])

	with open("data/new_word.txt", "wb") as outfile:
		for word in new_words:
			outfile.write(word+"\r\n")


def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	newWordIdentification()

if __name__ == '__main__':
	main()
