#encoding=utf-8
import sys
import pickle
from trie import Trie

def getLexicon():
	with open("../data/lexicon.pickle", "rb") as infile:
		(diseases, symptoms, examinations) = pickle.load(infile)
	return (diseases, symptoms, examinations) 

def getSymptomSentence():
	sentences = []
	with open("../data/symptom.txt", "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8").replace(' ', '')
			sentences += [sentence.strip() for sentence in row.split(u'。')[:-1]]
	return sentences

def getDiseaseSentence():
	sentences = []
	with open("../data/disease.txt", "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8").replace(' ', '')
			sentences += [sentence.strip() for sentence in row.split(u'。')[:-1]]
	return sentences	

def buildTrie(words):
	trie = Trie()
	for w in words:
		trie.insert(w)
	return trie

def autoLabel(sentence, trie):
	sentence_tagged = []
	i = 0
	while i < len(sentence):
		w = sentence[i]
		node = trie.root
		if w not in node.children.keys():
			sentence_tagged.append("O")
		else:
			node = node.children[w]
			j = i + 1
			while j < len(sentence) and sentence[j] in node.children.keys():
				node = node.children[sentence[j]]
				j += 1
			if node.sta != None:
				sentence_tagged += node.sta
				i = j - 1
			else:
				sentence_tagged += ["O" for t in range(j - i)]
				i = j - 1
		i += 1
	return sentence_tagged

def generateTrain(sentences, trie):
	print "start auto labeling ..."
	with open("train.txt", "wb") as outfile:
		for sentence in sentences:
			sentence_tagged = autoLabel(sentence, trie)
			for record in zip(sentence, sentence_tagged):
				outfile.write(' '.join(record) + "\n")
			outfile.write("\n")
	print "finished auto labeling"

def generateTest(sentences, trie):
	print "start auto labeling ..."
	with open("test.txt", "wb") as outfile:
		for sentence in sentences:
			sentence_tagged = autoLabel(sentence, trie)
			for record in zip(sentence, sentence_tagged):
				if record[0].strip() == "":
					continue
				outfile.write(' '.join(record) + "\n")
			outfile.write("\n")
	print "finished auto labeling"

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	(diseases, symptoms, examinations) = getLexicon()
	symptom_sentences = getSymptomSentence()
	disease_sentences = getDiseaseSentence()
	trie_symptom = buildTrie(symptoms)
	generateTrain(symptom_sentences, trie_symptom)
	generateTest(disease_sentences, trie_symptom)

if __name__ == '__main__':
	main()
