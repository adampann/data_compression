import collections
from sys import argv
import time
#Global Variables
encode_option = 1
delete_option = 0
open_indexs = []


def initalizeDict():
	x = collections.OrderedDict()
	for num in range(256):
		x[bytes([num])] = num
	return x

def initalizeDecoderDict():
	x = collections.OrderedDict()
	y = collections.OrderedDict()
	for num in range(256):
		x[num] = bytes([num])
		y[bytes([num])] = num

	return x,y

def makeByte(number):
	return number.to_bytes(2, byteorder='big')

def makeInt(bytes):
	return int.from_bytes(bytes, byteorder='big')

def captureMatch(f, dict):
	return captureMatchHelper(f, dict, f.tell(), runningMatch=b'')

def captureMatchHelper(file, dict, startLocatation, runningMatch):
	current = file.read(1)
	if current != None and current and runningMatch + current in dict:
		runningMatch = runningMatch + current
		return captureMatchHelper(file, dict, file.tell(), runningMatch)
	else:
		if current:
			x = file.seek(startLocatation, 0)
			return runningMatch, True
		return runningMatch, False

def fcDictMod(dict, previous, current, setID):
	if previous != None and previous + current[0:1] not in dict:
		index = len(dict) if not open_indexs else open_indexs.pop()
		dict[previous + current[0:1]] = index

def cmDictMod(dict, previous, current, setID):
	if previous != None and previous + current not in dict:
		index = len(dict) if not open_indexs else open_indexs.pop()
		dict[previous + current] = index

def fcDecodeDictMod(dict,dictReverse, previous, current):
	if previous != None and previous + current[0:1] not in dictReverse:
		index = len(dict) if not open_indexs else open_indexs.pop()

		dict[index] = previous + current[0:1]
		dictReverse[previous + current[0:1]] = index

def cmDecodeDictMod(dict, dictReverse, previous, current):
	if previous != None and previous + current not in dictReverse:
		index = len(dict) if not open_indexs else open_indexs.pop()
		dict[index] = previous + current
		dictReverse[previous + current] = index


def getSize(fileobject):
	fileobject.seek(0,2) # move the cursor to the end of the file
	size = fileobject.tell()
	fileobject.seek(0,0)
	return size

def dictNotFull(dict):
	return True if len(dict) < 65000 else False

def restart():
	return initalizeDict()

def decodeRestart():
	return initalizeDecoderDict()

def dictModify(dict, prevMatch, currentMatch, setID = None):
	if dictNotFull(dict):
		if encode_option == 0:
			fcDictMod(dict, prevMatch, currentMatch, setID)
		else:
			cmDictMod(dict, prevMatch, currentMatch, setID)
	else:
		if delete_option == 0:
			pass # Freeze, do nothing
		elif delete_option == 1:
			dict = restart()
			dictModify(dict, prevMatch, currentMatch)

		elif delete_option == 2: #LRU
			byte, num = dict.popitem(last = False)
			while num <= 255:
				dict[byte] = num
				byte, num = dict.popitem(last = False)
			open_indexs.append(num)
			dictModify(dict, prevMatch, currentMatch, num)

def dictDecodeModify(dict, dictReverse, prevMatch, currentMatch):
	if dictNotFull(dict):
		if encode_option == 0:
			fcDecodeDictMod(dict, dictReverse, prevMatch, currentMatch)
		else:
			cmDecodeDictMod(dict, dictReverse, prevMatch, currentMatch)
	else:
		if delete_option == 0:
			pass# Freeze, do nothing
		elif delete_option == 1: #restart
			dict, dictReverse = decodeRestart()
			dictDecodeModify(dict, dictReverse, prevMatch, currentMatch)

		elif delete_option == 2: #lru
			num, bytes = dict.popitem(last = False)
			while num <= 255:
				dict[num] = bytes
				num, bytes = dict.popitem(last = False)

			#if bytes in dictReverse:
			dictReverse.pop(bytes, None)

			open_indexs.append(num)
			dictDecodeModify(dict, dictReverse, prevMatch, currentMatch)


def encode(fileName):
	dict = initalizeDict()
	prevMatch = None
	open_indexs = []

	with open(fileName, 'rb') as f, open(fileName + '.pann', 'wb') as output:
		print("size of input file " + str(getSize(f)))
		for iter in range(getSize(f)):
			currentMatch, end = captureMatch(f, dict)
			if currentMatch:

				objectToAdd = dict[currentMatch]
				dict.move_to_end(currentMatch, True)

				output.write(makeByte(objectToAdd))

				dictModify(dict, prevMatch, currentMatch)

			prevMatch = currentMatch

			if not end:
				break

		print("size of end output file " + str(getSize(output)))

def decode(fileName):
	open_indexs = []
	dict, dictReverse = initalizeDecoderDict()
	with open(fileName, "rb") as binary_file, open(fileName.split('.pann')[0], 'wb') as results:
		prevMatch = None
		for byteNum in range(int(getSize(binary_file)/2)):
			byteInput = binary_file.read(2)
			matchIndex = makeInt(byteInput)

			currentMatch = dict[matchIndex]
			dict.move_to_end(matchIndex, True)


			if currentMatch in dictReverse:
				dictReverse.move_to_end(currentMatch, True)

			results.write(currentMatch)

			dictDecodeModify(dict, dictReverse, prevMatch, currentMatch)
			prevMatch = currentMatch


def validodateInput():
	if len(argv) != 5:
		print("Invalid Args, Must follow format: \"python compression.py <-n, -d> <x> <y> input\"")
		return False
	if argv[1] != '-n' and argv[1] != '-d':
		print("Invalid Option: " + argv[1] + ', either -n (encode) or -d (decode)')
		return False
	return True

def setVariable(x, y):
	encode_option = int(x)
	delete_option = int(y)

if __name__ == "__main__":
	print(argv)
	if validodateInput():
		setVariable(argv[2], argv[3])
		if argv[1] == '-n':
			t0 = time.time()
			encode(argv[4])
			t1 = time.time()
			print(t1 - t0, 'seconds to encode')
		elif argv[1] == '-d':
			t1 = time.time()
			decode(argv[4])
			t2 = time.time()
			print(t2 - t1, 'second to decode')


