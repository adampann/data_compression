import trie as t
#Global Variables
encode_option = 0
delete_option = 0

def initalizeDict():
	x = []
	trie = t.Trie()
	for num in range(256):
		char = chr(num)
		trie.add(char, len(x))
		x.append(makeByte(num))

	return [x, trie]

def initalizeDecoderDict():
	x = []
	trie = t.Trie()
	for num in range(256):
		char = chr(num)
		trie.add(char, len(x))
		x.append(char)
	return [x, trie]

def makeByte(number):
	return number.to_bytes(2, byteorder='big')

def makeInt(bytes):
	return int.from_bytes(bytes, byteorder='big')

def captureMatch(f, dict):
	return captureMatchHelper(f, dict[1], f.tell(), runningMatch='')

def captureMatchHelper(file, trie, startLocatation, runningMatch):
	current = file.read(1)
	current = current
	if current != None and current and trie.has_word(runningMatch + current):#runningMatch + current in dict:
		runningMatch = runningMatch + current
		return captureMatchHelper(file, trie, file.tell(), runningMatch)
	else:
		if current:
			x = file.seek(startLocatation, 0)
			return (runningMatch, True)
		return (runningMatch, False)


def fcDictMod(dict, previous, current):
	# if previous != None and previous + current[0] not in dict:
	# 	dict[previous + current[0]] = makeByte(len(dict))
	if previous != None and not dict[1].has_word(previous + current[0]):
		enAddWord(dict, previous + current[0])

def enAddWord(dict, word):
	#add to trie
	length = len(dict[0])
	dict[1].add(word, length)
	#add to array
	dict[0].append(makeByte(length))

def deAddWord(dict, word):
	#add to trie
	length = len(dict[0])
	dict[1].add(word, length)
	#add to array
	dict[0].append(word)

def cmDictMod(dict, previous, current):
	# if previous != None and previous+current not in dict:
	# 	dict[previous+current] = makeByte(len(dict))
	if previous != None and not dict[1].has_word(previous + current):
		enAddWord(dict, previous + current)

def fcDecodeDictMod(dict, previous, current):
	#(type(current))
	#print(current)
	if previous != None and not dict[1].has_word(previous + current[0]):#previous+current[0] not in dict:
		#dict[makeByte(len(dict))] = previous+current[0]
		deAddWord(dict, previous + current[0])

def cmDecodeDictMod(dict, previous, current):
	if previous != None and not dict[1].has_word(previous + current):#previous+current[0] not in dict:
		#dict[makeByte(len(dict))] = previous+current[0]
		deAddWord(dict, previous + current)

def getSize(fileobject):
	fileobject.seek(0,2) # move the cursor to the end of the file
	size = fileobject.tell()
	fileobject.seek(0,0)
	return size

def writeFile(output, list):
	#this will have to write binary to file
	#print(list)
	for thing in list:
		output.write(thing)

def dictNotFull(dict):
	return True if len(dict[0]) < 65000 else False

def restart(dict):
	return initalizeDict(dict)

def decodeRestart(dict):
	return initalizeDecoderDict(dict)


def dictModify(dict, prevMatch, currentMatch):
	if dictNotFull(dict):
		if encode_option == 0:
			fcDictMod(dict, prevMatch, currentMatch)
		else:
			cmDictMod(dict, prevMatch, currentMatch)
	else:
		if delete_option == 0:
			pass
		# Freeze, do nothing
		elif delete_option == 1:
			dict = restart()
			dictModify(dict, prevMatch, currentMatch)

def dictDecodeModify(dict, prevMatch, currentMatch):
	if dictNotFull(dict):
		if encode_option == 0:
			fcDecodeDictMod(dict, prevMatch, currentMatch)
		else:
			cmDecodeDictMod(dict, prevMatch, currentMatch)
	else:
		if delete_option == 0:
			pass
		# Freeze, do nothing
		elif delete_option == 1:
			dict = decodeRestart()
			dictDecodeModify(dict, prevMatch, currentMatch)
def encode():
	dict = initalizeDict()
	prevMatch = None
	list = []
	with open("TestData/TESTDATAREADME.txt") as f, open("TestData/TestOutput.txt", 'wb') as output:
		print("size of input file " + str(getSize(f)))
		#print("size of start output file " + str(getSize(output)))
		for iter in range(getSize(f)):
			currentMatch = captureMatch(f, dict)
			if currentMatch[0]:
				objectToAdd = dict[0][dict[1].get_data(currentMatch[0])]
				#print(makeInt(objectToAdd))
				#list.append(objectToAdd)
				output.write(objectToAdd)

				dictModify(dict, prevMatch, currentMatch[0])

			prevMatch = currentMatch[0]

			if not currentMatch[1]:
				break
		#writeFile(output, list)
		print("size of end output file " + str(getSize(output)))
		#print(dict[0])
		#print(list)

def decode():
	dict = initalizeDecoderDict()
	with open("TestData/TestOutput.txt", "rb") as binary_file, open("TestData/ResultsOutput.txt", 'w') as results:
		stuff = [] #remove
		prevMatch = None
		for byteNum in range(int(getSize(binary_file)/2)):
			byteInput = binary_file.read(2)

			matchIndex = makeInt(byteInput)
			currentMatch = dict[0][matchIndex]
			stuff.append(currentMatch) #remove
			results.write(currentMatch)
			#print(byteNum, prevMatch) #remove
			dictDecodeModify(dict, prevMatch, currentMatch)
			prevMatch = currentMatch

		#print(stuff)#remove
		#writeFile(results, stuff) remove


if __name__ == "__main__":
	encode()
	print('start decoding')
	decode()


