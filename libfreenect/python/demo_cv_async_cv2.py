#!/usr/bin/env python
import freenect
import cv2
import frame_convert
import inspect

cv2.namedWindow('Depth')
cv2.namedWindow('RGB')
keep_running = True


def display_depth(dev, data, timestamp):
    global keep_running
    cv2.imshow('Depth', frame_convert.pretty_depth(data))
    if cv2.waitKey(10) == 27:
        keep_running = False

def display_rgb(dev, data, timestamp):
    global keep_running
    data = data[:, :, ::-1]  # RGB -> BGR
    cv2.imshow('RGB', data)
    if cv2.waitKey(10) == 27:
        keep_running = False


def body(*args):
    if not keep_running:
        raise freenect.Kill
        cv2.destroyAllWindows()


print('Press ESC in window to stop')

ctx = freenect.init()
devPtr = freenect.open_device(ctx, 0)
#freenect.set_video_mode(devPtr, freenect.VIDEO_IR_8BIT, freenect.RESOLUTION_MEDIUM)
#ir, data = freenect.sync_get_video(format=freenect.VIDEO_IR_8BIT)
#print ir
#print data

freenect.runloop(depth=display_depth,
                 video=display_rgb,
                 body=body,
                 dev=devPtr
                 )
