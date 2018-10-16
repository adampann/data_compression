import collections
with open("TestData/TESTDATAREADME.txt") as f:
	# print(str(f.tell())+ " " + f.read(1))
	# for x in range(24):
	# 	char = f.read(1)
	# 	print(str(x)+ '|' + char + '|' + str(ord(char)))
	orderDict = collections.OrderedDict()
	for num in range(256):
		char = chr(num)
		orderDict[char] = num
	print(orderDict)
	print(len(orderDict))
	print(orderDict.pop('\x00'))
	print(orderDict.popitem(last=False))
	print(len(orderDict))

# x = {}
#
# x['a'] = 0
# print(len(x))
# x['b'] = 1
# print(len(x))
# x['c'] = 2
# print(len(x))