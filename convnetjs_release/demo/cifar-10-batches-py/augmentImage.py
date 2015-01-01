import os
import cPickle
import numpy
import random
from scipy.misc import imsave, imread
import subprocess
import time
import sys

millis = int(round(time.time() * 1000))

srcFiles = [os.getcwd()+'/../chiquita/ducky1.jpg', os.getcwd()+'/../chiquita/hawaii1.jpg', os.getcwd()+'/../chiquita/kid1.jpg', os.getcwd()+'/../chiquita/maid1.jpg', os.getcwd()+'/../chiquita/santa1.jpg', os.getcwd()+'/../chiquita/stash1.jpg',
	os.getcwd()+'/../chiquita/logoDucky.jpg', os.getcwd()+'/../chiquita/logoHawaii.jpg', os.getcwd()+'/../chiquita/logoKid.jpg', os.getcwd()+'/../chiquita/logo2.jpg', os.getcwd()+'/../chiquita/logo2.jpg', os.getcwd()+'/../chiquita/logo2.jpg',
	os.getcwd()+'/../chiquita/logo.jpg', os.getcwd()+'/../chiquita/logo.jpg', os.getcwd()+'/../chiquita/logo1.jpg', os.getcwd()+'/../chiquita/logo1.jpg', os.getcwd()+'/../chiquita/logo1.jpg', os.getcwd()+'/../chiquita/logo1.jpg']

random.seed()
xs = []
ys = []
numImages = 1000
outFile = os.getcwd()+'/../chiquita/out/tmp.png'

rotAngle = 0
for i in range(numImages):
	index = random.randint(0,40)		# if index between 0 and 5, then use target images, otherwise, use random image as negative case.
	if index <= 17:
		srcFile = srcFiles[index]
		angle = random.randint(-10,10)
		cometVal = random.randint(0, 1)
		cometRot = random.randint(0,3)*90
		seedVal = random.randint(0,10000)
		attVal = random.randint(0,100)*0.01
		if index > 5:
			index=6
	#	outFile = os.getcwd()+'/../chiquita/out/tmp'+`index`+'_'+`angle`+'_'+`cometVal`+'_'+`cometRot`+'_'+`seedVal`+'_'+`attVal`+'.jpg'
	#	outLongFile = os.getcwd()+'/../chiquita/out/tmpL'+`index`+'_'+`angle`+'_'+`cometVal`+'_'+`cometRot`+'_'+`seedVal`+'_'+`attVal`+'.jpg'
	#	print outFile

		subprocess.call(['convert',srcFile,'-rotate',`angle`,'-morphology','Convolve','Comet:0x'+`cometVal`+'+'+`cometRot`,'-seed',`seedVal`,'-attenuate',`attVal`,'+noise','gaussian','-gravity','Center','-crop','32x64+0+0','+repage',outFile])
	else:
		fileNum = random.randint(0,99)
		offset = random.randint(0,32)
		index=6
		subprocess.call(['convert', 'kai/cifar10_batch_'+`fileNum`+'.png', '-resize', '64x64', '-crop', '32x64+'+`offset`+'+0', outFile])
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
imageDataReshaped = numpy.reshape(x,(numImages,32*64,3))
print numpy.shape(imageDataReshaped)
imsave(outLongFile, imageDataReshaped)
numpy.savetxt(labelFile, y, fmt='%d', newline=', ', header='var labels=[', footer='];', comments='')

