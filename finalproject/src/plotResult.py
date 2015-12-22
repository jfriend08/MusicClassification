import sys, re
from os import listdir
import numpy as np
from os.path import isfile, join
import numpy as np
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputDir", help="input results directory")
parser.add_argument("selected_nSplit", help="select n_split so can generate 3dim figure")

args = parser.parse_args()
mypath = args.inputDir
selected_nSplit = args.selected_nSplit

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
xs = []
ys = []
zs = []
val = []

for eachfile in onlyfiles:
  nameSplit = re.split('_|.o', eachfile)
  if len(nameSplit) > 2 and nameSplit[0] != 'Run' and nameSplit[0] == selected_nSplit:
    fo = open(mypath+"/"+eachfile, "r+")
    predict = fo.readlines()[-1]
    fo.close()
    try:
      val.append(float(predict))
    except:
      continue
    xs.append(float(nameSplit[1]))
    ys.append(float(nameSplit[2]))
    zs.append(float(nameSplit[3]))

xs = np.array(xs)
ys = np.array(ys)
zs = np.array(zs)
val = np.array(val)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')
colors = cm.jet(val/max(val))
colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(val)
yg = ax.scatter(xs, ys, zs, c=val, marker='o')
cb = fig.colorbar(colmap)

ax.set_xlabel('k Clusters')
ax.set_ylabel('Batch Size')
ax.set_zlabel('n Neighbors')
plt.title("Select n_split:%s"%selected_nSplit, y=1.08)
plt.show()

