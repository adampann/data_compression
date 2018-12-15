from PIL import Image
import numpy as np
import math
from sys import argv

def prepareImage(name):
	im = Image.open(name)
	#print(im, im.size)
	rawData = np.array(im.getdata())  # get values of image
	#print(rawData)
	if im.mode == 'RGB':
		pix_values = np.array([x[0] for x in rawData])  # convert image to single # per pixel (x,y,z) => (x)
	else:
		pix_values = rawData
	#print(pix_values)
	return im, pix_values

if __name__ == '__main__':
	real = argv[1]
	made = argv[2]
	x, real = prepareImage(real)
	madeImg = Image.open(made)
	madeData = madeImg.getdata()
	madeData = [x for x in madeData]
	count = 0

	for r, f in zip(real, madeData):
		# count += math.pow((r - f), 2)
		count += ((r - f)*(r - f))
	n = len(real)
	print(count / n)