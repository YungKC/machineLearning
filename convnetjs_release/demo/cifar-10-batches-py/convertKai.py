import cPickle
import numpy
from scipy.misc import imsave

def unpickle(file):  
  fo = open(file, 'rb')
  dict = cPickle.load(fo)
  fo.close()
  return dict

xs = []
ys = []
for j in range(5):
  d = unpickle('data_batch_'+`j+1`)
  x = d['data']
  y = d['labels']
  xs.append(x)
  ys.append(y)

d = unpickle('test_batch')
xs.append(d['data'])
ys.append(d['labels'])

x = numpy.concatenate(xs)
y = numpy.concatenate(ys)

x = numpy.dstack((x[:, :1024], x[:, 1024:2048], x[:, 2048:]))

imsave('cifar10_batch_'+'kai'+'.png', x[50000:50001,:])
for i in range(51000):
  tmp = x[i,:]
  tmp = numpy.reshape(tmp,(32,32,3))
  imsave('kai/cifar10_batch_'+`i`+'.png', tmp)


