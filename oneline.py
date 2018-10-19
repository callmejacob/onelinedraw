# -*- coding: utf-8 -*-
import os;

from skimage import data, io, filters
from skimage.filters import rank
from skimage.morphology import disk
import numpy as np

os.system("adb shell screencap -p /sdcard/tmp.png");
os.system("adb pull /sdcard/tmp.png /Users/jacob/PycharmProjects/onelinedraw/test.png");

img = data.load('/Users/jacob/PycharmProjects/onelinedraw/test.png', True)

#img_filter = filters.sobel(img)
img_filter = rank.gradient(img, disk(5))

h, w = img_filter.shape
for i in range(h):
     sum = np.sum(img_filter[i][:])


sum_rows = np.zeros(h, dtype=int)
for i in range(h):
	sum_rows[i] = np.sum(img_filter[i][:])


cout_rows = 20
record_rows = np.zeros(cout_rows * 4).reshape((cout_rows, 4))
cout_rows = 0

start = 0
end = 0
for i in range(h - 1):
	if (sum_rows[i + 1] != sum_rows[i]):
		if (end - start > 13 and sum_rows[i] > 1000 and sum_rows[i] < 9000):
			record_rows[cout_rows][0] = start
			record_rows[cout_rows][1] = end
			record_rows[cout_rows][2] = end - start
			record_rows[cout_rows][3] = sum_rows[i]
			print start, end
			cout_rows += 1;
		start = i + 1
	end = i + 1


cat_row = 0
for i in range(cout_rows):
	if (record_rows[i][2] < 100):
		cat_row = i;
		record_rows[i][1] += 70


# print 'cat_row:', cat_row

row_start = int(record_rows[0][1])
row_end = int(record_rows[cout_rows-1][1])

sum_cols = np.zeros(w)
for i in range(w):
        sum_cols[i] = np.sum(img_filter[row_start:row_end, i])


cout_cols = 20
record_cols = np.zeros(cout_cols * 4).reshape((cout_cols, 4))
cout_cols = 0

start = 0
end = 0
for i in range(w):
	if (sum_cols[i] == 0):
		if (end - start > 20):
			record_cols[cout_cols][0] = start
			record_cols[cout_cols][1] = end
			record_cols[cout_cols][2] = end - start
			record_cols[cout_cols][3] = sum_cols[i]
			cout_cols += 1
		start = i
		end = i
	else:
		end += 1;


# for i in range(cout_cols):
#	print record_cols[i]


pt = np.zeros(cout_rows * cout_cols * 2, dtype=int).reshape((cout_rows, cout_cols, 2))
sum_map = np.zeros(cout_rows * cout_cols, dtype=int).reshape((cout_rows, cout_cols))
for i in range(cout_rows):
	for j in range(cout_cols):
		left = int(record_cols[j][0])
		right = int(record_cols[j][1])
		top = int(record_rows[i][0])
		bottom = int(record_rows[i][1])
		# print left, right, top, bottom
		sum_map[i][j] = int(np.sum(img_filter[top:bottom, left:right]))
		pt[i][j][0] = (left + right) / 2
		pt[i][j][1] = (top + bottom) / 2


max_map = np.max(sum_map)

map = np.zeros(cout_rows * cout_cols, dtype=int).reshape((cout_rows, cout_cols))
cat_i = 0
cat_j = 0
for i in range(cout_rows):
	for j in range(cout_cols):
		if (sum_map[i][j] == max_map):
			cat_i = i
			cat_j = j
			map[i][j] = 1
		elif (sum_map[i][j] == 0):
			map[i][j] = 0
		else:
			map[i][j] = 1


print cout_rows, cout_cols
print cat_i, cat_j
print map

# convert params to resolve path
params = ''
params += ' ' + str(cout_rows)
params += ' ' + str(cout_cols)
params += ' ' + str(cat_i + 1)
params += ' ' + str(cat_j + 1)
for i in range(cout_rows):
	for j in range(cout_cols):
		if (map[i][j] == 0):
			params += ' ' + str(i + 1)
			params += ' ' + str(j + 1)

# begin resolve path
import os
import sys
import commands

#params = ' '.join(sys.argv[1:])

main = "./findpath"
# os.path.exists(main)
#rc, out = commands.getstatusoutput(main + ' 6 6 2 4 1 1 1 5 2 5 5 0' )
rc, out = commands.getstatusoutput(main + params)
print out


pos = out.split('\n')
len = len(pos)

x = range(len)
y = range(len)
for i in range(len):
	slice = pos[i].split(' ')
	x[i] = int(slice[0])
	y[i] = int(slice[1])

# auto touch the path
import time

for i in range(len):
	row = cout_rows - y[i]
	col = x[i]
	print row, col
	print pt[row][col]
	os.system('adb shell input tap ' + str(pt[row][col][0]) + ' ' + str(pt[row][col][1]))

	#time.sleep(0.02)


'''
import matplotlib.pyplot as plt

plt.plot(x, y)
plt.show()
'''

# done
time.sleep(2)
os.system('adb shell input tap 720 1500')
time.sleep(2)
