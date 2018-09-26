#Initialize a local dictionary D
dict = {}
#fill dict with alphabet
for num in range(128):
	dict[num] = chr(num)
print(dict)
print(dict.values())

#take in file
# with open("TESTDATAREADME.txt") as f, open("TestOutput.txt", 'w') as test:
# 	print( f.read(1))
# 	test.write("this is a test")