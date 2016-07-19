#encoding=utf-8
import sys

def clean():
	with open("data/examination.txt", "rb") as infile,\
		 open("data/examination_clean.txt", "wb") as outfile:
		 for row in infile:
		 	row = row.strip().decode("utf-8")
		 	row_clean = ""
		 	pre = ""
		 	for word in row:
		 		if word == ' ' or word == '　':
		 			continue
		 		if pre != "" and word == u"、" and (pre == u"。" or pre == u"，" or pre == u"、" or pre == u"："):
		 			continue
		 		row_clean += word
		 		pre = word
		 	outfile.write(row_clean + "\r\n")

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	clean()

if __name__ == '__main__':
	main()
