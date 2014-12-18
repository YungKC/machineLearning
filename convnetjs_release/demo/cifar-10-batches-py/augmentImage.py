import os
import cPickle
import numpy
import random
from scipy.misc import imsave, imread
import subprocess
import time
import sys

millis = int(round(time.time() * 1000))

srcFiles = [os.getcwd()+'/../chiquita/ducky2.jpg', os.getcwd()+'/../chiquita/hawaii2.jpg', os.getcwd()+'/../chiquita/kid2.jpg', os.getcwd()+'/../chiquita/maid2.jpg', os.getcwd()+'/../chiquita/santa2.jpg', os.getcwd()+'/../chiquita/stash2.jpg']

random.seed()
xs = []
ys = []
numImages = 1000
outFile = os.getcwd()+'/../chiquita/out/tmp.png'

for i in range(numImages):
	index = random.randint(0,5)
	srcFile = srcFiles[index]
	angle = random.randint(-10,10)
	cometVal = random.randint(0, 1)
	cometRot = random.randint(0,3)*90
	seedVal = random.randint(0,10000)
	attVal = random.randint(0,100)*0.01

#	outFile = os.getcwd()+'/../chiquita/out/tmp'+`index`+'_'+`angle`+'_'+`cometVal`+'_'+`cometRot`+'_'+`seedVal`+'_'+`attVal`+'.jpg'
#	outLongFile = os.getcwd()+'/../chiquita/out/tmpL'+`index`+'_'+`angle`+'_'+`cometVal`+'_'+`cometRot`+'_'+`seedVal`+'_'+`attVal`+'.jpg'
#	print outFile

	subprocess.call(['convert',srcFile,'-rotate',`angle`,'-morphology','Convolve','Comet:0x'+`cometVal`+'+'+`cometRot`,'-seed',`seedVal`,'-attenuate',`attVal`,'+noise','gaussian','-gravity','Center','-crop','32x32+0+0','+repage',outFile])

	imageData = imread(outFile)
#	print numpy.shape(imageData)
	sys.stdout.write('.')
	sys.stdout.flush()
	xs.append(imageData)
	ys.append([index])

x = numpy.concatenate(xs)
y = numpy.concatenate(ys)


outLongFile = os.getcwd()+'/../chiquita/out/tmp'+`millis`+'.png'
labelFile = os.getcwd()+'/../chiquita/out/labels'+`millis`+'.js'
imageDataReshaped = numpy.reshape(x,(numImages,32*32,3))
print numpy.shape(imageDataReshaped)
imsave(outLongFile, imageDataReshaped)
numpy.savetxt(labelFile, y, fmt='%d', newline=', ', header='var labels=[', footer='];', comments='')

