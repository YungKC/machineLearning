import os
import cPickle
import numpy
import random
from scipy.misc import imsave, imread
import subprocess

srcFiles = [os.getcwd()+'/../chiquita/ducky2.jpg', os.getcwd()+'/../chiquita/hawaii2.jpg', os.getcwd()+'/../chiquita/kid2.jpg', os.getcwd()+'/../chiquita/maid2.jpg', os.getcwd()+'/../chiquita/santa2.jpg', os.getcwd()+'/../chiquita/stash2.jpg']

random.seed()

for i in range(1):
	index = random.randint(0,5)
	srcFile = srcFiles[index]
	angle = random.randint(-10,10)
	cometVal = random.randint(0, 1)
	cometRot = random.randint(0,3)*90
	seedVal = random.randint(0,10000)
	attVal = random.randint(0,100)*0.01

	outFile = os.getcwd()+'/../chiquita/out/tmp'+`index`+'_'+`angle`+'_'+`cometVal`+'_'+`cometRot`+'_'+`seedVal`+'_'+`attVal`+'.jpg'
	print outFile

	subprocess.call(['convert',srcFile,'-rotate',`angle`,'-morphology','Convolve','Comet:0x'+`cometVal`+'+'+`cometRot`,'-seed',`seedVal`,'-attenuate',`attVal`,'+noise','gaussian','-gravity','Center','-crop','32x32+0+0','+repage',outFile])



