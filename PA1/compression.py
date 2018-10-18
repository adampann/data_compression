#import trie as t
import collections
from sys import argv
import time
#Global Variables
encode_option = 0
delete_option = 2

def initalizeDict():
	x = collections.OrderedDict()
	for num in range(256):
		char = chr(num)
		x[char] = num
	return x

def initalizeDecoderDict():
	x = collections.OrderedDict()
	for num in range(256):
		char = chr(num)
		x[num] = char
	y = collections.OrderedDict()
	return [x,y]

def makeByte(number):
	return number.to_bytes(2, byteorder='big')

def makeInt(bytes):
	return int.from_bytes(bytes, byteorder='big')

def captureMatch(f, dict):
	return captureMatchHelper(f, dict, f.tell(), runningMatch='')

def captureMatchHelper(file, dict, startLocatation, runningMatch):
	current = file.read(1)
	if current != None and current and runningMatch + current in dict:
		runningMatch = runningMatch + current
		return captureMatchHelper(file, dict, file.tell(), runningMatch)
	else:
		if current:
			x = file.seek(startLocatation, 0)
			return (runningMatch, True)
		return (runningMatch, False)

def fcDictMod(dict, previous, current):
	if previous != None and previous + current[0] not in dict:
		dict[previous + current[0]] = len(dict)

# def enAddWord(dict, word):
# 	#add to trie
# 	length = len(dict[0])
# 	dict[1].add(word, length)
# 	#add to array
# 	dict[0].append(makeByte(length))

# def deAddWord(dict, word):
# 	#add to trie
# 	length = len(dict[0])
# 	dict[1].add(word, length)
# 	#add to array
# 	dict[0].append(word)

def cmDictMod(dict, previous, current):
	if previous != None and previous + current not in dict:
		dict[previous + current] = len(dict)

def fcDecodeDictMod(dict, previous, current):
	if previous != None and previous + current[0] not in dict[1]:
		dict[0][len(dict[0])] = previous + current[0]
		dict[1][previous + current[0]] = len(dict[1])

def cmDecodeDictMod(dict, previous, current):
	if previous != None and previous + current not in dict[1]:
		dict[0][len(dict[0])] = previous+current
		dict[1][previous+current] = len(dict[1])
		#deAddWord(dict, previous + current)

def getSize(fileobject):
	fileobject.seek(0,2) # move the cursor to the end of the file
	size = fileobject.tell()
	fileobject.seek(0,0)
	return size

def writeFile(output, list):

	for thing in list:
		output.write(thing)

def dictNotFull(dict):
	return True if len(dict) < 65000 else False

def restart():
	return initalizeDict()

def decodeRestart():
	return initalizeDecoderDict()


def dictModify(dict, prevMatch, currentMatch):
	if dictNotFull(dict):
		if encode_option == 0:
			fcDictMod(dict, prevMatch, currentMatch)
		else:
			cmDictMod(dict, prevMatch, currentMatch)
	else:
		if delete_option == 0:
			pass # Freeze, do nothing
		elif delete_option == 1:
			dict = restart()
			dictModify(dict, prevMatch, currentMatch)
		elif delete_option == 2:
			dict.popitem(last=False)
			dictModify(dict, prevMatch, currentMatch)

def dictDecodeModify(dict, prevMatch, currentMatch):
	if dictNotFull(dict[0]):
		if encode_option == 0:
			fcDecodeDictMod(dict, prevMatch, currentMatch)
		else:
			cmDecodeDictMod(dict, prevMatch, currentMatch)
	else:
		if delete_option == 0:
			pass# Freeze, do nothing
		elif delete_option == 1:
			dict = decodeRestart()
			dictDecodeModify(dict, prevMatch, currentMatch)
		elif delete_option == 2:
			pair = dict[0].popitem(last=False)
			dict[1].pop(pair[1])
			dictModify(dict, prevMatch, currentMatch)
def encode():
	dict = initalizeDict()
	prevMatch = None
	with open("TestData/book1.txt") as f, open("TestData/TestOutput.txt", 'wb') as output:
		print("size of input file " + str(getSize(f)))
		for iter in range(getSize(f)):
			currentMatch = captureMatch(f, dict)
			if currentMatch[0]:
				#removes and adds back in for LRU
				objectToAdd = dict.pop(currentMatch[0])
				dict[currentMatch[0]] = objectToAdd


				output.write(makeByte(objectToAdd))

				dictModify(dict, prevMatch, currentMatch[0])

			prevMatch = currentMatch[0]

			if not currentMatch[1]:
				break

		print("size of end output file " + str(getSize(output)))

def decode():
	dict = initalizeDecoderDict()
	with open("TestData/TestOutput.txt", "rb") as binary_file, open("TestData/book1Results.txt", 'w') as results:
		prevMatch = None
		for byteNum in range(int(getSize(binary_file)/2)):
			byteInput = binary_file.read(2)

			matchIndex = makeInt(byteInput)
			currentMatch = dict[0][matchIndex]


			results.write(currentMatch)
			dictDecodeModify(dict, prevMatch, currentMatch)
			prevMatch = currentMatch

def validodateInput():
	if len(argv) != 4:
		print("Invalid Args, Must follow format: \"python compression.py <-n, -d> input output\"")
	if argv[1] != '-n' and argv[1] != '-d':
		print("Invalid Option: " + argv[1] + ', either -n (encode) or -d (decode)')


if __name__ == "__main__":
	validodateInput()
	#print(type(argv[1]))
	t0 = time.time()
	encode()
	#time.sleep(2.5)
	t1 = time.time()
	# print('start decoding')
	decode()
	t2 = time.time()

	print(t1 - t0, 'seconds to encode')
	print(t2 - t1, 'second to decode')


