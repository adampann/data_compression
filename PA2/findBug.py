import numpy as np
from PIL import Image
import math
# import os
from sys import argv, stdout, stdin
import scipy


# import gzip
# import pickle

def quantizeMatrix(size):
	arr = np.array(
		[[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55], [14, 13, 16, 24, 40, 57, 69, 56],
		 [14, 17, 22, 29, 51, 87, 80, 62
		  ], [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
		 [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]])
	if size == 16:
		arr = arr.repeat(2, axis=0).repeat(2, axis=1)

	return arr


def naturalLevel(lst):
	# for x in range(len(lst)):
	# 	lst[x] -= 128
	return lst - 128


# return [x-128 for x in lst]

def unlevel(lst):
	return lst + 128


def formatImage(name, blockSize):
	im = Image.open(name)

	rawData = np.array(im.getdata())  # get values of image

	pix_values = np.array([x[0] for x in rawData])  # convert image to single # per pixel (x,y,z) => (x)

	pix_values = naturalLevel(pix_values)

	x = im.size[0]
	y = im.size[1]
	xMod = x % blockSize
	yMod = y % blockSize

	pix_values = pix_values.reshape(im.size[0], im.size[1])  # reshape into 2d array of correct size
	# print(arr)
	if xMod > 0:
		# print(xMod)
		for x in range(len(pix_values)):
			pix_values[x].append([0] * xMod)
	# arr = [np.append(pix_values[x],[0]*xMod) for x in range(len(pix_values))]
	if yMod > 0:
		# arr = arr + [[0] * len(arr[0])] * yMod
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
	# print(arr)
	return arr


def partition(arr, size):
	# x = len(arr)
	# y = len(arr[0])
	# #print(x)
	# chunks = []
	#
	# for xIndex in range(0, y, size):
	# 	for yIndex in range(0, x, size):
	# 		print(xIndex, yIndex)
	# 		#arr[xIndex:xIndex+size, yIndex:yIndex+size]
	# 		chunks.append(arr[yIndex:yIndex+size, xIndex:xIndex+size])
	#
	# return np.array(chunks)
	w, h = arr.shape
	return (arr.reshape(h // size, size, -1, size).swapaxes(1, 2).reshape(-1, size, size))


def undoPartition(blocks, imsize):
	# #blocks = np.array(blocks)
	# blocks.shape = (int(imsize[0]/len(blocks[0])), int(imsize[1]/len(blocks[0])), len(blocks[0]), len(blocks[0]))
	# #arr = np.zeros(shape= (imsize[1],imsize[0]))
	#
	# # for x in range(imsize[0]):
	# # 	for y in range(imsize[1]):
	# # 		blockX = x / 8 #which block in X direction
	# # 		innerX = x % 8 #X index w/in block
	# # 		blockY = y / 8 #which block in Y direction
	# # 		innerY = y % 8 #Y index w/in block
	# # 		arr[x][y] = blocks[blockX][blockY][innerX][innerY]
	# above = None
	# for x in range(len(blocks)-1):
	# 	across = blocks[x][0]
	# 	for y in range(len(blocks[x])):
	# 		across = np.concatenate((across, blocks[x+1][y]), axis=0)
	#
	# 	if x == 0:
	# 		above = across
	# 	else:
	# 		above =  np.concatenate((above, across), axis=1)
	#
	# return above
	h = imsize[0]
	w = imsize[1]
	n, nrows, ncols = blocks.shape
	return (blocks.reshape(h // nrows, -1, nrows, ncols).swapaxes(1, 2).reshape(h, w))


def performDCT(dct, dctT, chunks):
	a = []
	for chunk in chunks:
		a.append(np.matmul(dct, np.matmul(chunk, dctT)))
	return np.array(a)


def performQuantize(quant, chunks):
	for chunk in chunks:
		for w in range(len(chunk)):
			for h in range(len(chunk[0])):
				chunk[w][h] = int(round(chunk[w][h] / quant[w][h]))
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


def zigzagPattern(size):  # 2d arrays only
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
	# output = np.zeros(shape=(size,size))
	tmp = [[(x, y) for x in range(size)] for y in range(size)]
	output = [0 for x in range(size * size)]
	# arr = [0] + arr
	index = -1
	for i in range(2 * (size - 1) + 1):
		if i < size:
			bound = 0
		else:
			bound = i - size + 1
		for j in range(bound, i - bound + 1):
			index = index + 1
			if i % 2 == 1:
				output[index] = tmp[j][i - j]
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
		# unzigzag(acs[x:x+step], blockSize)
		#allPixel = [dcs[index]] + acs[x:x + step]
		allPixel = np.append(dcs[index], acs[x:x + step])
		# print(allPixel)
		toAdd = np.zeros(shape=(blockSize, blockSize))
		for position, value in zip(pattern, allPixel):
			toAdd[position[0]][position[1]] = value
		rebuitBlocks.append(toAdd.astype(int))
		index = index + 1

	return np.array(rebuitBlocks)  # .flatten().astype(int)


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
		dcs[x] += dcs[x - 1]


def compression(fileName, blockSize):

	arr, imsize = formatImage(fileName, blockSize)

	# returns array of [blockSize * blockSize] blocks
	chunks = partition(arr, blockSize)

	# performs MatMul on each chunk w/ DCT natric
	print('start', chunks[0], end='\n')
	# print(DctMatricForm())
	dct = DctMatricForm()
	DCTified = performDCT(dct, dct.transpose(), chunks)

	print(DCTified[0], end='\n')
	quantized = performQuantize(quantizeMatrix(blockSize), np.copy(DCTified))
	print('quantized', quantized[0], end='\n')
	# returns list of DCs based off their difference to the one before it
	# print('before diff dcs', [x[0][0] for x in quantized])
	dcs = DCDiff(quantized)
	# print('diff dcs' , dcs)

	# list of ACs from all blocks in zigzag order
	acs = ACs(zigzagPattern(blockSize), quantized, blockSize)
	# print('acs', acs)
	# print('length of og acs:', len(acs))

	# format ACs into pairings of size and amplitude
	acformat = formatACDC(acs.flatten())
	# format ACs into pairings of size and amplitude
	dcformat = formatACDC(dcs)



	undiff(dcs)
	# print('undiff dcs', dcs)

	blocks = rebuildDCAC(dcs, acs, blockSize)
	print('block 0 rebuilt', blocks[0], end='\n')

	blocks = deQuantize(quantizeMatrix(blockSize), blocks)
	print('deQuantize', blocks[0], end='\n')
	dct = DctMatricForm()
	blocks = performDCT(dct.transpose(), dct, blocks)

	blocks = np.around(blocks)
	blocks = unlevel(blocks)
	print('inverse DCT', blocks[0])
	# print('unleveld',blocks[0])
	arr = undoPartition(blocks, imsize)


	#print(arr[0])
	img = Image.new("L", (imsize[0], imsize[1]))
	# fromarray(arr.flatten(),'L')
	#arr = np.around(arr)
	#print(arr)
	img.putdata(arr)

	img.show()




if __name__ == '__main__':


	action = argv[1]

	if action == '-c':
		fileName = argv[2]
		blockSize = int(argv[3])
		compression(fileName, blockSize)



