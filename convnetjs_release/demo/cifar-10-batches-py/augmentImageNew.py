import os
import cPickle
import numpy
import random
from scipy.misc import imsave, imread
import subprocess
import time
import sys
import os

millis = int(round(time.time() * 1000))

srcFiles = [['ducky1-Edit.jpg','ducky2-Edit.jpg','ducky3-Edit.jpg','ducky4-Edit.jpg','ducky5-Edit.jpg','ducky6-Edit.jpg'], ['hawaii1-Edit.jpg','hawaii2-Edit.jpg','hawaii3-Edit.jpg'], 
			['kid1-Edit.jpg','kid2-Edit.jpg','kid3-Edit.jpg'], ['maid1-Edit.jpg','maid2-Edit.jpg'], ['santa1-Edit.jpg','santa2-Edit.jpg'], ['stash1-Edit.jpg', 'stash2-Edit.jpg']]
numClasses = len(srcFiles)

random.seed()
ys = []
for loopCount in range(10):
	xs = []

	numImages = 1000
	outFile = os.path.join(os.getcwd(),'..','chiquita','out','tmp.jpg')

	rotAngle = 0
	for i in range(numImages):
		index = random.randint(0,40)		# if index between 0 and 5, then use target images, otherwise, use random image as negative case.
#		sys.stdout.write(`index`)
		if index < numClasses:
			size = len(srcFiles[index])
			subIndex = random.randint(0,size-1)
#			print `index` + ':' + `subIndex`
			inFileName = srcFiles[index][subIndex]
#			print inFileName
			srcFile = os.path.join(os.getcwd(),'..','chiquita','srcImages', inFileName)
			angle = random.randint(-3,3)
			level = random.randint(5,40)
			cometVal = random.randint(0, 1)
			cometRot = random.randint(0,3)*90
			seedVal = random.randint(0,10000)
			attVal = random.randint(0,100)*0.01
#			subprocess.call(['convert',srcFile,'+level',`level`+'%','-rotate',`angle`,'-seed',`seedVal`,'-attenuate',`attVal`,'+noise','gaussian','-gravity','Center','-crop','32x64+0+0','+repage',outFile])
			subprocess.call(['convert',srcFile,'+level',`level`+'%','-rotate',`angle`,'-gravity','Center','-crop','32x64+0+0','+repage',outFile])
		elif index < 24:
			index = index % numClasses
			size = len(srcFiles[index])
			subIndex = random.randint(0,size-1)
#			print `index` + ':' + `subIndex`
			inFileName = srcFiles[index][subIndex]
#			print inFileName
			srcFile = os.path.join(os.getcwd(),'..','chiquita','srcImages', inFileName)
			index=numClasses
			xoffset = random.randint(0,4) + 8
			yoffset = random.randint(0,6) + 10
			offsetSign = random.randint(0,3)

			if offsetSign == 0:
				subprocess.call(['convert', srcFile,'-gravity','Center','-crop', '32x64+'+`xoffset`+'+'+`yoffset`, outFile])
			elif offsetSign == 1:
				subprocess.call(['convert', srcFile,'-gravity','Center','-crop', '32x64+'+`xoffset`+'-'+`yoffset`, outFile])
			elif offsetSign == 2:
				subprocess.call(['convert', srcFile,'-gravity','Center','-crop', '32x64-'+`xoffset`+'+'+`yoffset`, outFile])
			elif offsetSign == 3:
				subprocess.call(['convert', srcFile,'-gravity','Center','-crop', '32x64-'+`xoffset`+'-'+`yoffset`, outFile])
		else:
			fileNum = random.randint(0,99)
			offset = random.randint(0,32)
			index=numClasses
			subprocess.call(['convert', os.path.join('kai','cifar10_batch_'+`fileNum`+'.png'), '-resize', '64x64', '-crop', '32x64+'+`offset`+'+0', outFile])
		imageData = imread(outFile)
#		dataSize = numpy.shape(imageData)
#		print dataSize
		
		sys.stdout.write('.')
		sys.stdout.flush()
		xs.append(imageData)
		ys.append([index])

	x = numpy.concatenate(xs)
	
	outLongFile = os.path.join(os.getcwd(),'..','chiquita','out','chiquita_batch_'+`loopCount`+'.png')
	sys.stdout.write(outLongFile)
	imageDataReshaped = numpy.reshape(x,(numImages,32*64,3))
#	print numpy.shape(imageDataReshaped)
	imsave(outLongFile, imageDataReshaped)
y = numpy.concatenate(ys)
labelFile = os.path.join(os.getcwd(),'..','chiquita','out','chiquita_labels.js')
numpy.savetxt(labelFile, y, fmt='%d', newline=', ', header='var labels=[', footer='];', comments='')

