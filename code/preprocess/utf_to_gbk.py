#encoding=utf-8
import sys

def convert():
	sentence_set = set()
	with open("data/examination_clean.txt", "rb") as infile:
		for row in infile:
			row = row.strip().decode("utf-8")
			items = row.split(u"。")
			for item in items:
				if item == "":
					continue
				sentence_set.add(item)


	with open("data/examination_clean_seg_gbk.txt", "wb") as outfile:
		for sentence in sentence_set:
			# outfile.write(sentence+ u"。")
			outfile.write(sentence.encode("gbk", "ignore") + u"。".encode("gbk"))
			outfile.write("\r\n")

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	convert()

if __name__ == '__main__':
	main()
