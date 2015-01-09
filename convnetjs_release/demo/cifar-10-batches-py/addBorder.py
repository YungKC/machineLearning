import os
import subprocess


srcFiles = [['ducky1.jpg','ducky2.jpg','ducky3.jpg','ducky4.jpg','ducky5.jpg','ducky6.jpg'], ['hawaii1.jpg','hawaii2.jpg','hawaii3.jpg'], 
			['kid1.jpg','kid2.jpg','kid3.jpg'], ['maid1.jpg','maid2.jpg'], ['santa1.jpg','santa2.jpg'], ['stash1.jpg', 'stash2.jpg']]

srcImageName = os.path.join(os.getcwd(),'..','chiquita','srcImages', srcFiles[0][0])
cmdTxt = 'convert ' + srcImageName + ' -gravity West -crop 2x64+0+0 +repage tmp.jpg'
subprocess.call(cmdTxt, shell=True)
cmdTxt = 'convert tmp.jpg -scale 1x1\! -format "%[fx:int(255*r+.5)],%[fx:int(255*g+.5)],%[fx:int(255*b+.5)]" info:-'
result = subprocess.Popen(cmdTxt, stdout=subprocess.PIPE, shell=True).stdout.read().replace("\n","")
addBorderCmdTxt = 'convert ' + srcImageName + ' -bordercolor "rgb(' + result + ')" -border 32x64 tmp.jpg'
subprocess.call(addBorderCmdTxt, shell=True)

