#!/usr/bin/env python
import freenect
import cv2
import cv
import numpy as np

'''
try to mask the video feed to just area within the depth window
'''

def draw_str(dst, (x, y), s):
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.CV_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def change_kernel(value):
    global kernel_size
    kernel_size = value

def change_iterations(value):
    global iteration_count
    iteration_count = value

def change_averageSize(value):
    global averageSize
    averageSize = value

def getMaskValue(depth):
    global averageSize
    global threshold
    global current_depth
    return 255/averageSize * np.logical_and(depth >= current_depth - threshold,
                            depth <= current_depth + threshold)
def show_depth():
    global depthImage
    global depthSum
    global kernel_size
    global iteration_count

    depth, timestamp = freenect.sync_get_depth()
    if depthSum == None:
        depthSum = np.empty(depth.shape)
    if loop == 0:
        depthImage = depthSum.astype(np.uint8)
        dilateKernel = np.ones((kernel_size, kernel_size),np.uint8)
#    depthImage = cv2.erode(depthImage, erodeKernel, iterations=2)
        depthImage = cv2.dilate(depthImage, dilateKernel, iterations=iteration_count)
        depthSum = getMaskValue(depth)
        cv2.imshow('Depth', depthImage)

    else:
        depthSum += getMaskValue(depth)



def show_video():
    global t
    global dt
    global loop
    global depthImage
    global averageSize

    videoImage = freenect.sync_get_video()[0]
    videoImage = videoImage[:, :, ::-1]  # RGB -> BGR
    baseImage = np.empty(videoImage.shape)
    videoImage = cv2.bitwise_and(videoImage, videoImage, mask=depthImage)


    loop = (loop+1)%averageSize
    if loop == 0:
        dt = (clock() - t)/averageSize
        t = clock()
    draw_str(videoImage, (20, 20), 'time: %.1f ms' % (dt*1000))

    cv2.imshow('Video', videoImage)


threshold = 100
current_depth = 0
kernel_size = 4
iteration_count = 2
depthSum = None
depthImage = None
t = clock()
dt=0
loop = 0
averageSize = 1

cv.NamedWindow('Depth')
cv.NamedWindow('Video')
cv.CreateTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Depth', current_depth, 2048, change_depth)
cv.CreateTrackbar('kernel',     'Depth', kernel_size, 10, change_kernel)
cv.CreateTrackbar('iterations',  'Depth', iteration_count, 10, change_iterations)
cv.CreateTrackbar('averageSize',  'Depth', averageSize, 10, change_averageSize)

print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()

    if cv.WaitKey(10) == 27:
        break
