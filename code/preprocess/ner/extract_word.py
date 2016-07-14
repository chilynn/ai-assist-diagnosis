#encoding=utf-8
import sys
import pickle

def extractWord(infile_name):
	print "extracting word of " + infile_name
	words = set()
	stack = []
	with open(infile_name, "rb") as infile:
		for row in infile:
			row = row.strip()
			items = row.split()
			if len(items) == 0:
				continue
			char = items[0]
			true = items[1]
			pred = items[2]
			if pred == 'O':
				stack = []
			elif pred == 'B' and len(stack) == 0:
				stack.append(char)
			elif pred == 'B' and len(stack) != 0:
				stack = []
				stack.append(char)
			elif pred == 'E':
				stack.append(char)
				words.add(''.join(stack))
				stack = []
			elif pred == 'M':
				stack.append(char)
			else:
				stack = []
	
	if "hmm" in infile_name:
		outfile_name = "word_hmm.txt"
	else:
		outfile_name = "word_crf.txt"
	with open(outfile_name, "wb") as outfile:
		for word in words:
			outfile.write(word+"\r\n")

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	extractWord("result_hmm.txt")
	extractWord("result_crf.txt")

if __name__ == '__main__':
	main()
