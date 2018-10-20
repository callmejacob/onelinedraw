# -*- coding: utf-8 -*-

import os
import sys
import commands

root_dir = os.path.dirname(os.path.abspath(__file__))

params = ' ' + ' '.join(sys.argv[1:])
main = root_dir +  "/cpp/findpath"
rc, out = commands.getstatusoutput(main + params)

print rc, out

pos = out.split('\n')
len = len(pos)

x = range(len)
y = range(len)
for i in range(len):
	slice = pos[i].split(' ')
	x[i] = int(slice[0])
	y[i] = int(slice[1])
	


import matplotlib.pyplot as plt

plt.plot(x, y)
plt.show()
