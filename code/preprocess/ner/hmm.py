t#encoding:utf-8
import sys
from copy import deepcopy

# 以下5个元素是HMM模型的参数
V = set() # 观测集合
Q = set() # 状态集合
A = {} # 状态转移概率矩阵，P(状态|状态)
B = {} # 观测概率矩阵，P(观测|状态)
PI = {} # 初始状态概率向量

DEFAULT_PROB = 0.000000000001
MIN_PROB = -1 * float('inf')

def train(train_file):
	print "start training ..."
	# 统计模型参数
	with open(train_file, "rb") as infile:
		pre_s = -1 # t-1时刻的状态
		for line in infile:
			segs = line.strip().split()
			if len(segs) == 0: # 遇到空行时
				pre_s = -1
			else:
				o = segs[0] # t时刻的观测o
				s = segs[1] # t时刻的状态s
				# 统计状态s到观测o的次数
				B[s][o] = B.setdefault(s, {}).setdefault(o, 0) + 1
				V.add(o)
				Q.add(s)
				if pre_s == -1: # 统计每个句子开头第一个状态的次数
					PI[s] = PI.setdefault(s, 0) + 1
				else: # 统计状态pre_s到状态s的次数
					A[pre_s][s] = A.setdefault(pre_s, {}).setdefault(s, 0) + 1
				pre_s = s
	# 概率归一化
	for i in A.keys():
		prob_sum = 0
		for j in A[i].keys():
			prob_sum += A[i][j]
		for j in A[i].keys():
			A[i][j] = 1.0 * A[i][j] / prob_sum

	for i in B.keys():
		prob_sum = 0
		for j in B[i].keys():
			prob_sum += B[i][j]
		for j in B[i].keys():
			B[i][j] = 1.0 * B[i][j] / prob_sum

	prob_sum = sum(PI.values())
	for i in PI.keys():
		PI[i] = 1.0 * PI[i] / prob_sum
	print "finished training ..."

def predict(X):
	W = [{} for t in range(len(X))]
	path = {}
	for s in Q:
		W[0][s] = 1.0 * PI.get(s, DEFAULT_PROB) * B.get(s, {}).get(X[0], DEFAULT_PROB)
		path[s] = [s]
	for t in range(1, len(X)):
		new_path = {}
		for s in Q:
			max_prob = MIN_PROB
			max_s = ''
			for pre_s in Q:
				prob = W[t-1][pre_s] * \
					   A.get(pre_s, {}).get(s, DEFAULT_PROB) * \
					   B.get(s, {}).get(X[t], DEFAULT_PROB)
				(max_prob, max_s) = max((max_prob, max_s), (prob, pre_s))
			W[t][s] = max_prob
			tmp = deepcopy(path[max_s])
			tmp.append(s)
			new_path[s] = tmp
		path = new_path
	(max_prob, max_s) = max((W[len(X)-1][s], s) for s in Q)
	# return path['E']
	return path[max_s]

def test(test_file, output_file):
	print "start testing"
	words = set()
	with open(test_file, "rb") as infile, \
		 open(output_file, "wb") as outfile:
		X_test = []
		y_test = []
		for line in infile:
			segs = line.strip().split()
			if len(segs) == 0: # 遇到空行时
				if len(X_test) == 0:
					continue
				preds = predict(X_test)
				for vals in zip(X_test, y_test, preds):
					outfile.write("\t".join(vals) + "\r\n")	
				outfile.write("\r\n")
				tmp = ""
				for i in range(len(preds)):
					if preds[i] != 'O':
						tmp += X_test[i]
					else:
						tmp += " "
				for w in tmp.split():
					if w.strip() != "":
						words.add(w)
				X_test = []
				y_test = []
			else:
				if len(segs) != 2:
					print line
				
				o = segs[0] # t时刻的观测o
				s = segs[1] # t时刻的状态s		
				X_test.append(o)
				y_test.append(s)

	with open("word.txt", "wb") as outfile:
		for w in words:
			outfile.write(w + "\r\n")

	print "finished testing"

def main():
	if len(sys.argv) < 3:
		print "python hmm.py train.txt test.txt output.txt"
	else:
		train_file = sys.argv[1]
		test_file = sys.argv[2]
		output_file = sys.argv[3]
		train(train_file)
		test(test_file, output_file)

if __name__ == '__main__':
	main()