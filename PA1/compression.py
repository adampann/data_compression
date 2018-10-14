import trie as t
#Global Variables
encode_option = 0
delete_option = 0

def initalizeDict():
	dict = {}
	for num in range(256):
		dict[chr(num)] = makeByte(num)

	#dict = {'a':makeByte(0), 'b':makeByte(1)}

	return dict

def initalizeDecoderDict():
	dict = {}
	for num in range(256):
		dict[makeByte(num)] = chr(num)
	# print(dict)
	#dict = {makeByte(0): 'a', makeByte(1):'b' }
	return dict

def makeByte(number):
	return number.to_bytes(2, byteorder='big')

def makeInt(bytes):
	return int.from_bytes(bytes, byteorder='big')

def captureMatch(f, dict):
	return captureMatchHelper(f, dict, f.tell(), runningMatch='')

def captureMatchHelper(file, dict, startLocatation, runningMatch):
	current = file.read(1)
	if current and runningMatch + current in dict:
		runningMatch = runningMatch + current
		return captureMatchHelper(file, dict, file.tell(), runningMatch)
	else:
		x = file.seek(startLocatation, 0)
		return runningMatch


def fcDictMod(dict, previous, current):
	if previous != None and previous+current[0] not in dict:
		dict[previous+current[0]] = makeByte(len(dict))

def cmDictMod(dict, previous, current):
	if previous != None and previous+current not in dict:
		dict[previous+current] = makeByte(len(dict))

def fcDecodeDictMod(dict, previous, current):
	if previous != None and previous+current[0] not in dict:
		dict[makeByte(len(dict))] = previous+current[0]

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
	return True if len(dict) < 65000 else False

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
			cmDictMod(dict, prevMatch, currentMatch)
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
		print("size of start output file " + str(getSize(output)))
		for iter in range(getSize(f)):
			currentMatch = captureMatch(f, dict)
			if currentMatch:
				objectToAdd = dict[currentMatch]
				list.append(objectToAdd)

				dictModify(dict, prevMatch, currentMatch)

			prevMatch = currentMatch
		writeFile(output, list)
		print("size of end output file " + str(getSize(output)))
		#print(dict)
		#print(list)



def decode():
	dict = initalizeDecoderDict()
	with open("TestData/TestOutput.txt", "rb") as binary_file:

		prevMatch = None
		for byte in range(int(getSize(binary_file)/2)):
			currentMatch= binary_file.read(2)
			if currentMatch in dict:
				print(dict[currentMatch], end='')

			dictDecodeModify(dict, prevMatch, currentMatch)
			prevMatch = currentMatch

			#print(data)
			#print(makeInt(data))

if __name__ == "__main__":
	test = t.Trie()
	print(type(test))
	#encode()

	#decode()


