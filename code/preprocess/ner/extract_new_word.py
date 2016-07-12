#encoding=utf-8
import sys
import pickle

def getLexicon():
	with open("../data/lexicon.pickle", "rb") as infile:
		(diseases, symptoms, examinations) = pickle.load(infile)
	return (diseases, symptoms, examinations) 

def getHmmWord():
	words = set()
	with open("word.txt", "rb") as infile:
		for row in infile:
			words.add(row.strip().decode("utf-8"))
	return words

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	(diseases, symptoms, examinations) = getLexicon()
	words = getHmmWord()
	# print len(words)
	# print len(symptoms)
	# print len(words - symptoms)
	with open("new_word.txt", "wb") as outfile:
		for new_word in (words - symptoms):
			outfile.write(new_word + "\r\n")

if __name__ == '__main__':
	main()
