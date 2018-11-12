# def solution(D, A):
# 	n = list(A) #output list
# 	failure_track = [-1] * len(A)
# 	for index in range(len(A)):
# 		#print('index: ', index, '| ', end='')
# 		current = A[index]
# 		for depth in range(D):
# 			if current != -1:
# 				#print(current, ' ', end='')
#
# 				n[index] = current
# 				current = A[current]
#
# 			else:
# 				n[index] = -1
# 				failure_track[index] = depth
# 				break
#
# 	return n
# x = [-1, 0,4,2,1]
# print(solution(3, x))
#print([0] * len(x))
class Node:
	def __init__(self, value=None, childL=None, childR=None):
		self.value = value
		self.childL = childL
		self.childR = childR

	def addChild(self, key):
		if key < self.value:
			self.childL = Node(key)
		else:
			self.childR = Node(key)

	def __getleft__(self):
		return self.childL
	def __getrigth__(self):
		return self.childR

class binaryTree:
	def __init__(self, list):
		self.head = Node(list[0])
		for item in list[1:]:
			current = self.head
			while current != None:
				if item < current.value:
					if current.childL != None:
						current = current.childL
					else:
						current.childL = Node(item)
				else:
					if current.childR != None:
						current = current.childR
					else:
						current.childR = Node(item)

	def findClosest(self, house):
		current_node = self.head
		closest = current_node
		best_distance = float("inf")
		while current_node != None:
			if current_node.value == house:
				return current_node.value
			elif (current_node.value - house) < best_distance:
				closest = current_node
				best_distance = abs(current_node.value - house)

			if house < current_node.value:
				current_node = current_node.childL
			else:
				current_node = current_node.childR

		return closest.value

def solution(stores, houses):
	n =[]
	tree = binaryTree(stores)
	for house in houses:
		n.append(tree.findClosest(house))

	return n
print(solution([1,5,20,11,16],[5,10,17]))