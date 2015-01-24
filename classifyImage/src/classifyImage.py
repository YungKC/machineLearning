import numpy as np
import json
from scipy import misc

#TODO: need to move the layer initialization portion out of the convolveKai method

from scipy.signal import convolve2d
from skimage.measure import block_reduce
def convolveKai(inData, inSizeX, inSizeY, layer):
	filter_sx = layer['sx']	#5
	filter_sy = layer['sy']	#5
	colorDepth = layer['in_depth']	#3
	filter_depth = layer['out_depth']	#16
	#filter_stride = layer['stride']	#1
	#filter_pad = layer['pad']	#2

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

def fcLayer(inData, layer):
	filter_depth = layer['out_depth']
	result = np.zeros([filter_depth])
	in_size = layer['num_inputs']
	wnp = np.zeros([filter_depth, in_size])
	for filterID in range(filter_depth):
	    w=layer['filters'][filterID]['w']
	    for i in range(in_size):
	        wnp[filterID][i] = w[str(i)]
	    result[filterID] = sum(wnp[filterID] * inData) + layer['biases']['w'][str(filterID)]
	return result

ducky = misc.imread('../image/download.png')
duckyRescaled = ducky /255.0 - 0.5
duckyRescaled = duckyRescaled[:,:,0:3]

inSizeX = 32
inSizeY = 64

# get the top left corner roi of 32x64 rectangle
inData = np.empty([3,inSizeY,inSizeX])
inData[0] = duckyRescaled[0:inSizeY,0:inSizeX,0]
inData[1] = duckyRescaled[0:inSizeY,0:inSizeX,1]
inData[2] = duckyRescaled[0:inSizeY,0:inSizeX,2]


with open('../model/chiquita.json') as json_data:
    model = json.load(json_data)
    json_data.close()

layer = model['layers'][1]
result, pooledResult = convolveKai(inData, inSizeX, inSizeY, layer)

layer = model['layers'][4]
result, pooledResult = convolveKai(pooledResult, inSizeX/2, inSizeY/2, layer)

layer = model['layers'][7]
result, pooledResult = convolveKai(pooledResult, inSizeX/4, inSizeY/4, layer)

# display the result of the first image pixel
pooledResult[np.ix_(np.arange(layer['out_depth']),[0],[0])].flatten()

#switch axes in preparation of fully connected layer
swappedResult = np.swapaxes(pooledResult,0,2)
swappedResult = np.swapaxes(swappedResult,0,1)
swappedResult = swappedResult.flatten()

layer = model['layers'][10]
result = fcLayer(swappedResult, layer)



def test():
	layer = model['layers'][1]
	result, pooledResult = convolveKai(inData, inSizeX, inSizeY, layer)

	layer = model['layers'][4]
	result, pooledResult = convolveKai(pooledResult, inSizeX/2, inSizeY/2, layer)

	layer = model['layers'][7]
	result, pooledResult = convolveKai(pooledResult, inSizeX/4, inSizeY/4, layer)	


#import timeit
#timeit.timeit(test, number=100)/100

