#encoding:utf-8

class Node:
	def __init__(self):
		self.obs = None
		self.sta = None
		self.children = {} # type of {char, Node}

class Trie:
	def __init__(self):
		self.root = Node()

	def insert(self, key):
		node = self.root
		for char in key:
			if char not in node.children.keys():
				child = Node()
				node.children[char] = child
				node = child
			else:
				node = node.children[char]
		node.obs = key
		if len(key) == 1:
			node.sta = "E"
		elif len(key) == 2:
			node.sta = "BE"
		else:
			node.sta = "B" + ''.join(["M" for i in range(len(key) - 2)]) + "E"
			