import numpy as np
import math
#np.set_printoptions(suppress=True)

# def DctMatricForm(h=8, w=8):
# 	arr = np.zeros([h,w])
# 	for k in range(h):
# 		for u in range(w):
# 			if k == 0:
# 				arr[k][u] = math.sqrt(1.0 / w)
# 			else:
# 				arr[k][u] = math.sqrt(2.0 / w) * math.cos(((2 * u + 1) * k * math.pi) / (2 * w))
# 	return arr
#
# #this is the array that I will be testing
# test = np.arange(64).reshape((8,8))
# test = np.random.rand(8,8) * 100
#
# print(test[0],'\n')
# #form DCT
# dt =  DctMatricForm()
# #form the transpose of DCT
# dctt =  dt.transpose()
# #apply DCT on test case
# output = np.matmul(dt, np.matmul(test, dctt))
# # cheat = scipy.dct(test)
# #attempt to recover test case
# recov = np.matmul(dctt, np.matmul(output, dt))
# print(recov[0],'\n')
#
#
# # \
# #print(newRecov)
# #print(np.round(recov).astype(int))
# #print(dct(test, norm='ortho'))
#
# #print(dct.transpose())
#
# x = np.zeros((4,4))
# print(x)
# print(x + 4)
# print(x)
w = 8
h = 4
size = 2
arr = np.arange(w*h).reshape((w,h))
print(arr)
arr = (arr.reshape(h // size, size, -1, size).swapaxes(1, 2).reshape(-1, size, size))
print(arr)
n, nrows, ncols = arr.shape
arr = (arr.reshape(h // nrows, -1, nrows, ncols).swapaxes(1, 2).reshape(w, h))
print(arr)







