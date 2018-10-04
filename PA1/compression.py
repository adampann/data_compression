def initalizeDict():
	dict = {}
	# for num in range(256):
	# 	dict[chr(num)] = num#bytes(chr(num), 'utf-8')
	# print(dict)
	dict = {'a':0, 'b':1}

	return dict

def captureMatch(f, dict):
	return captureMatchHelper(f, dict, f.tell(), runningMatch='')

def captureMatchHelper(file, dict, startLocatation, runningMatch):
	current = file.read(1)
	print("currnet: " + current)
	print(type(current))
	if current and runningMatch + current in dict:
		runningMatch = runningMatch + current
		return captureMatchHelper(file, dict, file.tell(), runningMatch)
	else:
		x = file.seek(startLocatation, 0)
		return runningMatch


def fcDictMod(dict, previous, current):
	if previous != None and previous+current[0] not in dict:
		dict[previous+current[0]] = len(dict)

def getSize(fileobject):
	fileobject.seek(0,2) # move the cursor to the end of the file
	size = fileobject.tell()
	fileobject.seek(0,0)
	return size

if __name__ == "__main__":
	dict = initalizeDict()
	prevMatch = None
	list = []
	with open("mydata.txt") as f, open("TestOutput.txt", 'w') as test:


		for iter in range(getSize(f)):
			print("iter:" + str(iter))
			currentMatch = captureMatch(f, dict)
			# print(currentMatch)
			if currentMatch:
				objectToAdd =  dict[currentMatch]
				list.append(objectToAdd)
				fcDictMod(dict, prevMatch, currentMatch)
			prevMatch = currentMatch
			#test.write(dict[matchReturn])
		print(dict)
		print(list)


		# current_char = f.read(1)
		# current_position = f.tell()-1
		# current_match = current_char
		# while current_match in dict:
		# 	print(current_match)
		# 	pass
		#
