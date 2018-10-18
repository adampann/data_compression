import collections
with open("TestData/TESTDATAREADME.txt", 'rb') as f:
	for x in range(50):
		print(f.read(1))
	# print(str(f.tell())+ " " + f.read(1))
	# for x in range(24):
	# 	char = f.read(1)
	# 	print(str(x)+ '|' + char + '|' + str(ord(char)))
	# orderDict = collections.OrderedDict()
	# for num in range(256):
	# 	char = chr(num)
	# 	orderDict[num] = char
	#
	# x = True if 0 in orderDict else False
	# #print(x)
	# print(len(orderDict))
	# print(orderDict.pop(100))
	# print(len(orderDict))
	# print(len(orderDict))

	#print('asdf' not in orderDict)

# x = {}
#
# x['a'] = 0
# print(len(x))
# x['b'] = 1
# print(len(x))
# x['c'] = 2
# print(len(x))