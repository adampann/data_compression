compress = 0
import os
name = 'test.txt'
#os.system('gzip -d test.txt')
with open(name+'.pann', 'wb') as f:
	x = [1,2,3]
	f.write(bytes(str(x), encoding='utf-8' ))
	print(bytes(str(x), encoding='utf-8' ))

if compress == 0:
	os.system('gzip ' + name)
elif compress == 1:
	os.system('bzip2 ' + name)
elif compress == 2:
	os.system('compress ' + name)

print('zipped')
if compress == 0:
	os.system('gzip -d ' + name + '.gz')
elif compress == 1:
	os.system('gzip -d ' + name + '.bz2')
elif compress == 2:
	os.system('uncompress ' + name + '.Z')


with open(name, 'rb') as f:
	print('here')
	x = f.read().decode()
	x = eval(x)
	print(x)
	for a in x:
		print(a)
