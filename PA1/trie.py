class Node:
	def __init__(self, label=None, data=None):
		self.children = dict()
		self.data = data # this will be index in array
		self.label = label #the key that was used to find this node

	def addChild(self, key, data=None):
		if not isinstance(key, Node):
			self.children[key] = Node(key, data)
		else: #if adding a premade node
			self.children[key.label] =  key

	def __getitem__(self, item):
		return self.children[item]

class Trie:
	def __init__(self):
		self.head = Node()

	def __getitem__(self, item):
		return self.head.children[item]

	def add(self, word, data):
		current_node = self.head
		word_found = True

		for i in range(len(word)):
			if word[i] in current_node.children:
				current_node =  current_node[word[i]]
			else:
				word_found = False
				break

		if not word_found:
			while i < len(word):
				current_node.addChild(word[i])
				current_node = current_node.children[word[i]]
				i += 1

		current_node.data = data

	def locate_word(self, word):
		if word == '' or word == None:
			return False

		#go down trie
		current_node = self.head
		exits = True

		for letter in word:
			if letter in current_node.children:
				current_node = current_node.children[letter]
			else:
				exits = False
				break


		if exits == True:
			return current_node.data
		else:
			return False

def print_tree(node):
		current_node = node
		#print(type(current_node))
		print(current_node.label)
		for child in current_node.children:
			#print(child)
			print_tree(current_node.children[child])

if __name__ == '__main__':
	trie = Trie()
	words = 'hello y'
	for word in words.split():
		trie.add(word, 0)

	print_tree(trie.head)

