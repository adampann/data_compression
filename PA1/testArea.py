import collections
with open("TestData/obj2.txt", 'rb') as f:
	dict = collections.OrderedDict()
	for x in range(10):
		dict[chr(x)] = x
	print(dict)
	dict.move_to_end(chr(0))
	print(dict)
	dict.pop(chr(2))
	print(dict)
#
# x['a'] = 0
# print(len(x))
# x['b'] = 1
# print(len(x))
# x['c'] = 2
# print(len(x))


