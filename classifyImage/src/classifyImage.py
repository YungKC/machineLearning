from scipy import misc
ducky = misc.imread('../image/download.png')
duckyRescaled = ducky /255.0 - 0.5
duckyRescaled = duckyRescaled[:,:,0:3]

import numpy as np
import json
with open('../model/chiquita.json') as json_data:
    model = json.load(json_data)
    json_data.close()

layer = model['layers'][1]

filter_sx = layer['sx']	#5
filter_sy = layer['sy']	#5
colorDepth = layer['in_depth']	#3
filter_depth = layer['out_depth']	#16
filter_stride = layer['stride']	#1
filter_pad = layer['pad']	#2

wnp = np.zeros([filter_depth,filter_sx*filter_sy*colorDepth])
for filterID in range(filter_depth):
    w=layer['filters'][filterID]['w']
    for i in range(filter_sx*filter_sy*colorDepth):
        wnp[filterID][i] = w[str(i)]

filterID = 0
convolveMatrix = wnp[filterID].reshape([filter_sx,filter_sy,colorDepth])

# get the top left corner roi of 32x64 rectangle
d0=duckyRescaled[0:64,0:32,0]
d1=duckyRescaled[0:64,0:32,1]
d2=duckyRescaled[0:64,0:32,2]
f0=convolveMatrix[:,:,0]
f1=convolveMatrix[:,:,1]
f2=convolveMatrix[:,:,2]

from scipy.signal import convolve2d
c0=convolve2d(d0,f0,mode='same',boundary='fill',fillvalue=0)
c1=convolve2d(d1,f1,mode='same',boundary='fill',fillvalue=0)
c2=convolve2d(d2,f2,mode='same',boundary='fill',fillvalue=0)
c=c0+c1+c2

tmp = np.zeros([5,5])
tmp = np.vstack(([[0,0,0],[0,0,0]],d0[0:3,0:3]))
tmp = np.hstack(([[0,0],[0,0],[0,0],[0,0],[0,0]],tmp))
s0=sum(sum(f0*tmp))

tmp = np.zeros([5,5])
tmp = np.vstack(([[0,0,0],[0,0,0]],d1[0:3,0:3]))
tmp = np.hstack(([[0,0],[0,0],[0,0],[0,0],[0,0]],tmp))
s1=sum(sum(f1*tmp))

tmp = np.zeros([5,5])
tmp = np.vstack(([[0,0,0],[0,0,0]],d2[0:3,0:3]))
tmp = np.hstack(([[0,0],[0,0],[0,0],[0,0],[0,0]],tmp))
s2=sum(sum(f2*tmp))

answer = layer['biases']['w']['0'] + s0 + s1 + s2 
answer
