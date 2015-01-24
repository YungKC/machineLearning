import numpy as np
import json
from scipy import misc

ducky = misc.imread('../image/download.png')
duckyRescaled = ducky /255.0 - 0.5
duckyRescaled = duckyRescaled[:,:,0:3]

inSizeX = 32
inSizeY = 64

# get the top left corner roi of 32x64 rectangle
d0=duckyRescaled[0:inSizeY,0:inSizeX,0]
d1=duckyRescaled[0:inSizeY,0:inSizeX,1]
d2=duckyRescaled[0:inSizeY,0:inSizeX,2]

inData = np.empty([3,inSizeY,inSizeX])
inData[0] = duckyRescaled[0:inSizeY,0:inSizeX,0]
inData[1] = duckyRescaled[0:inSizeY,0:inSizeX,1]
inData[2] = duckyRescaled[0:inSizeY,0:inSizeX,2]


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

f = np.empty([filter_depth,colorDepth,filter_sx,filter_sy])
for filterID in range(filter_depth):
	tmp = wnp[filterID].reshape([filter_sx,filter_sy,colorDepth])
	for colorID in range(colorDepth):
		f[filterID][colorID]=tmp[:,:,colorID]
		f[filterID][colorID]=np.fliplr(np.flipud(f[filterID][colorID]))


from scipy.signal import convolve2d
from skimage.measure import block_reduce

def convolve():
	pooledResult = np.empty([filter_depth,inSizeY/2,inSizeX/2])
	result = np.empty([filter_depth,inSizeY,inSizeX])
	for filterID in range(filter_depth):
		c = np.zeros([inSizeY, inSizeX])
		for colorID in range(colorDepth):
			c+=convolve2d(inData[colorID],f[filterID][colorID],mode='same',boundary='fill',fillvalue=0)
		result[filterID] = c+layer['biases']['w'][str(filterID)]
		# max pool here
		pooledResult[filterID]  = block_reduce(result[filterID] , block_size=(2,2), func=np.max)
		# relu step is here
		pooledResult[filterID][pooledResult[filterID] < 0] = 0
	return result, pooledResult

result, pooledResult = convolve()
result.shape
pooledResult.shape


import timeit
timeit.timeit(convolve, number=100)/100
