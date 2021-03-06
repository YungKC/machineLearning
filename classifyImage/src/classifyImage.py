import numpy as np
import json
from scipy import misc

#from scipy.signal import convolve2d
from scipy.ndimage.filters import convolve   # this is much faster than scipy.signal.convolve2d
from skimage.measure import block_reduce

def initFCLayer(layer):
	filter_depth = layer['out_depth']
	in_size = layer['num_inputs']
	wnp = np.zeros([filter_depth,in_size])
	for filterID in range(filter_depth):
		w=layer['filters'][filterID]['w']
		for i in range(in_size):
			wnp[filterID][i] = w[str(i)]
	layer['wnp'] = wnp

def initConvolveLayer(layer):
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
	layer['f'] = f


def convolveKai(inData, inSizeX, inSizeY, layer):
	colorDepth = layer['in_depth']	#3
	filter_depth = layer['out_depth']	#16

	f = layer['f']

	pooledResult = np.empty([filter_depth,inSizeY/2,inSizeX/2])
	result = np.empty([filter_depth,inSizeY,inSizeX])
	for filterID in range(filter_depth):
		c = np.zeros([inSizeY, inSizeX])
		for colorID in range(colorDepth):
#			c+=convolve2d(inData[colorID],f[filterID][colorID],mode='same',boundary='fill',fillvalue=0)
			c+=convolve(inData[colorID],f[filterID][colorID],mode='constant',cval=0)
		result[filterID] = c+layer['biases']['w'][str(filterID)]
		# max pool here
		pooledResult[filterID]  = block_reduce(result[filterID] , block_size=(2,2), func=np.max)
		# relu step is here
		pooledResult[filterID][pooledResult[filterID] < 0] = 0
	return result, pooledResult

def fcLayer(inData, layer):
	filter_depth = layer['out_depth']
	result = np.zeros([filter_depth])
	for filterID in range(filter_depth):
	    result[filterID] = sum(layer['wnp'][filterID] * inData) + layer['biases']['w'][str(filterID)]
	return result

classes_txt = ['ducky', 'hawaii', 'kid', 'maid', 'santa', 'stash', 'notFound']

import Tkinter, tkFileDialog
root = Tkinter.Tk()
root.withdraw()
file_path = tkFileDialog.askopenfilename(title="Open File", initialdir=('~/study/machineLearning/convnetjs_release/demo/chiquita'))

ducky = misc.imread(file_path)
if ducky.shape[0] > 80:
	ducky = misc.imresize(ducky, 80.0/ducky.shape[0])

# need to rescale to max height of 80 pixels

import matplotlib.pyplot as plt 
plt.imshow(ducky)
plt.show(block=False)

duckyRescaled = ducky /255.0 - 0.5
duckyRescaled = duckyRescaled[:,:,0:3]

inSizeX = 32
inSizeY = 64


with open('../model/chiquita.json') as json_data:
    model = json.load(json_data)
    json_data.close()


layer = model['layers'][1]
initConvolveLayer(layer)

layer = model['layers'][4]
initConvolveLayer(layer)

layer = model['layers'][7]
initConvolveLayer(layer)

layer = model['layers'][10]
initFCLayer(layer)

def test():
	layer = model['layers'][1]
	result, pooledResult = convolveKai(inData, inSizeX, inSizeY, layer)

	layer = model['layers'][4]
	result, pooledResult = convolveKai(pooledResult, inSizeX/2, inSizeY/2, layer)

	layer = model['layers'][7]
	result, pooledResult = convolveKai(pooledResult, inSizeX/4, inSizeY/4, layer)	

	# display the result of the first image pixel
	#pooledResult[np.ix_(np.arange(layer['out_depth']),[0],[0])].flatten()

	#switch axes in preparation of fully connected layer
	swappedResult = np.swapaxes(pooledResult,0,2)
	swappedResult = np.swapaxes(swappedResult,0,1)
	swappedResult = swappedResult.flatten()

	layer = model['layers'][10]
	result = fcLayer(swappedResult, layer)

	#softmax
	softmax = np.exp(result-max(result))
	softmax_sum = sum(softmax)
	softmax = softmax/softmax_sum
	answer = np.argmax(softmax)
	return answer, softmax, result[answer]
#	print answer
#	print softmax
#	print result[answer]

#import timeit
#print timeit.timeit(test, number=100)/100

inData = np.empty([3,inSizeY,inSizeX])
maxAnswerValue = 0
answer_final = None
maxYRange = duckyRescaled.shape[0]-1-64
maxXRange = duckyRescaled.shape[1]-1-32
for yOffset in range(2,maxYRange,2):
	for xOffset in range(2,maxXRange,2):
		for i in range(3):
			inData[i] = duckyRescaled[yOffset:inSizeY+yOffset, xOffset:inSizeX+xOffset,i]
		answer, softmax, mag = test()
		print xOffset, yOffset, answer, softmax[answer], mag
		if answer != len(classes_txt)-1 and softmax[answer] > maxAnswerValue:
			maxAnswerValue = softmax[answer]
			x_final = xOffset
			y_final = yOffset
			answer_final = answer
			mag_final = mag

if answer_final != None:
	print "final: ", classes_txt[answer_final], x_final, y_final, maxAnswerValue, mag_final
	plt.gca()
	plt.gca().add_patch(plt.Rectangle((x_final,y_final),32,64, fill=None))
	plt.show(block=False)
else:
	print "Did not match any targets."
raw_input("Press Enter to continue...")