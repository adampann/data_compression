import numpy as np
from PIL import Image
import math
from sys import argv, stdout, stdin


def quantizeMatrix(size):
	arr = np.array([[16, 11, 10, 16, 24, 40, 51, 61],[12, 12, 14, 19, 26, 58, 60, 55],[14, 13, 16, 24, 40, 57, 69, 56],[14, 17, 22, 29, 51, 87, 80, 62
],[18, 22, 37, 56, 68, 109, 103, 77],[24, 35, 55, 64, 81, 104, 113, 92],[49, 64, 78, 87, 103, 121, 120, 101],[72, 92, 95, 98, 112, 100, 103, 99]])
	if size == 16:
		arr = arr.repeat(2,axis=0).repeat(2,axis=1)

	return arr

def naturalLevel(lst):
	return lst - 128

def unlevel(lst):
	return lst + 128

def formatImage(name, blockSize):
	im = Image.open(name)

	rawData = np.array(im.getdata()) #get values of image

	pix_values = np.array([x[0] for x in rawData]) #convert image to single # per pixel (x,y,z) => (x)

	pix_values = naturalLevel(pix_values)

	x = im.size[0]
	y = im.size[1]
	xMod = x % blockSize
	yMod = y % blockSize

	pix_values = pix_values.reshape(im.size[0], im.size[1]) #reshape into 2d array of correct size
	if xMod > 0:
		for x in range(len(pix_values)):
			pix_values[x].append([0] * xMod)
	if yMod > 0:
		add = [[0] * len(pix_values[0])] * yMod
		pix_values = np.concatenate((pix_values, add))
	return pix_values.astype(float), im.size


def DctMatricForm(h=8, w=8):
	arr = np.zeros([h, w])
	for k in range(h):
		for u in range(w):
			if k == 0:
				arr[k][u] = math.sqrt(1.0 / w)
			else:
				arr[k][u] = math.sqrt(2.0 / w) * math.cos(((2 * u + 1) * k * math.pi) / (2 * w))
	return arr


def partition(arr, size):
	w, h = arr.shape
	return (arr.reshape(h // size, size, -1, size).swapaxes(1, 2).reshape(-1, size, size))

def undoPartition(blocks, imsize):
	w = imsize[0]
	h = imsize[1]
	n, nrows, ncols = blocks.shape
	blocks = np.array([np.flip(np.rot90(x, 1), 0) for x in blocks]).reshape(blocks.shape)
	return (blocks.reshape(h // nrows, -1, nrows, ncols).swapaxes(1, 2).reshape(w, h))


def performDCT(dct, dctT, chunks):
	a = []
	for chunk in chunks:
		a.append(np.matmul(dct, np.matmul(chunk, dctT)))
	return np.array(a)

def performQuantize(quant, chunks):
	for chunk in chunks:
		for w in range(len(chunk)):
			for h in range(len(chunk[0])):
				chunk[w][h] = chunk[w][h] / quant[w][h]
	return chunks.astype(int)

def deQuantize(quant, chunks):
	for chunk in chunks:
		for x in range(len(chunk[0])):
			for y in range(len(chunk[0])):
				chunk[x][y] = chunk[x][y] * quant[x][y]
	return chunks

def DCDiff(blocks):
	prev = blocks[0][0][0]
	x = np.array([prev])
	for block in blocks[1:]:
		x = np.concatenate((x, [block[0][0] - prev]))
		prev = block[0][0]
	return x

def ACs(pattern, blocks, size):
	hold = None
	result = np.zeros(size * size).astype(int)  # [0 for x in range(size * size)]
	for block in blocks:
		# hold = hold + zigzag(block)[1:]
		for w in range(size):
			for h in range(size):
				result[pattern[w][h]] = block[w][h]
		if hold is None:
			hold = np.copy(result[1:])
		else:
			hold = np.concatenate((hold, np.copy(result[1:])))
	# block
	return hold

def zigzagPattern(size): #2d arrays only
	m = [[0 for x in range(size)] for y in range(size)]
	index = -1
	for i in range(2 * (size - 1) + 1):
		if i < size:
			bound = 0
		else:
			bound = i - size + 1
		for j in range(bound, i - bound + 1):
			index = index + 1
			if i % 2 == 1:
				m[j][i - j] = index
			else:
				m[i - j][j] = index
	return m
 

def unzigzagPattern(size):
	#output = np.zeros(shape=(size,size))
	tmp = [[(x,y) for x in range(size)] for y in range(size)]
	output = [0 for x in range(size*size)]
	#arr = [0] + arr
	index = -1
	for i in range(2 * (size - 1) + 1):
		if i < size:
			bound = 0
		else:
			bound = i - size + 1
		for j in range(bound, i - bound + 1):
			index = index + 1
			if i % 2 == 1:
				output[index] = tmp[j][i-j]
			else:
				output[index] = tmp[i - j][j]
	return output


def rebuildDCAC(dcs, acs, blockSize):
	if blockSize == 8:
		step = 63
	elif blockSize == 16:
		step = 255

	rebuitBlocks = []
	index = 0
	pattern = unzigzagPattern(blockSize)
	for x in range(0, len(acs), step):
		allPixel = np.append(dcs[index], acs[x:x + step])
		toAdd = np.zeros(shape=(blockSize, blockSize))
		for position, value in zip(pattern, allPixel):
			toAdd[position[0]][position[1]] = value
		rebuitBlocks.append(toAdd.astype(int))
		index = index + 1

	return np.array(rebuitBlocks)#.flatten().astype(int)

def formatACDC(arr):
	index = 0
	hold = []

	while index < len(arr):
		value = arr[index]

		count = 0
		while index + 1 < len(arr) and arr[index + 1] == 0:
			index = index + 1
			count = count + 1
		zeros = count
		if zeros == 0:
			hold.append((value))
		else:
			hold.append((value, zeros))
		index = index + 1

	return hold

def unformat(dcformat):
	output = []
	for thing in dcformat:
		if isinstance(thing, tuple):
			output.append(thing[0])
			for x in range(thing[1]):
				output.append(0)
		else:
			output.append(thing)
	return output

def undiff(dcs):
	for x in range(1, len(dcs)):
		dcs[x] += dcs[x-1]

def compression(fileName, blockSize):
	arr, imsize = formatImage(fileName, blockSize)

	# returns array of [blockSize * blockSize] blocks
	chunks = partition(arr, blockSize)

	# performs MatMul on each chunk w/ DCT natric
	dct = DctMatricForm()
	DCTified = performDCT(dct, dct.transpose(), chunks)

	quantized = performQuantize(quantizeMatrix(blockSize), np.copy(DCTified))

	# returns list of DCs based off their difference to the one before it
	dcs = DCDiff(quantized)

	# list of ACs from all blocks in zigzag order
	acs = ACs(zigzagPattern(blockSize), quantized, blockSize)

	# format ACs into pairings of size and amplitude
	acformat = formatACDC(acs)
	# format ACs into pairings of size and amplitude
	dcformat = formatACDC(dcs)

	outputdata = (blockSize, imsize, dcformat, acformat)



	stdout.write(str(outputdata))



def decompression():

	inputData = stdin.read()
	#inputData = data

	fileName =  "testNAME"
	newName = fileName.rsplit('.',1)[0]
	# with open(newName, 'rb') as f:
	#x = inpputData.decode()
	inputData = eval(inputData)
	blockSize = inputData[0]
	imsize = inputData[1]
	dcformat = inputData[2]
	acformat = inputData[3]
	#print(inputData)

	dcs = unformat(dcformat)
	acs = unformat(acformat)

	undiff(dcs)

	blocks = rebuildDCAC(dcs, acs, blockSize)


	blocks = deQuantize(quantizeMatrix(blockSize), blocks)

	dct = DctMatricForm()
	blocks = performDCT(dct.transpose(), dct, blocks)

	blocks = blocks.astype(int)
	blocks = unlevel(blocks)

	arr = undoPartition(blocks, imsize)

	img = Image.new("L", (imsize[0], imsize[1]))
	# fromarray(arr.flatten(),'L')
	img.putdata(arr.flatten())
	#print(img)
	# img.format = "PNG"
	img.show()

	#img.save('shouldWork.bmp')


if __name__ == '__main__':
	action = argv[1]

	if action == '-c':
		fileName = argv[2]
		blockSize = int(argv[3])
		compression(fileName, blockSize)
	elif action == '-d':
		decompression()
