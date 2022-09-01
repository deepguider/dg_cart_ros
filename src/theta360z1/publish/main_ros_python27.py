#ccsmm@etri.re.kr

from __future__ import print_function

import cv2
import time
import numpy as np
from parse_image import GetPanoTool, GetPanTiltImg
from ipdb import set_trace as bp

import rospy  # python 2.7
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

import argparse

def get_parser():
    ## Defaults
    parser = argparse.ArgumentParser(description='ROS publish of ricoh theta 360 z1')
    parser.add_argument('--fps', type=int, default=1, help="Frame rate of publish")
    parser.add_argument('--mode', type=str, default="ros", choices=["ros", "demo"], help="Frame rate of publish")

    ## Parsing args to opt
    opt = parser.parse_args()
    return opt

def imresize(img, scale_percent=60):
    #scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)    
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def crop_image(frame, pano_tool, pans=[270, 0, 90, 180]):
    '''
    pans = [270, 0, 90, 180]  # front, right, left, back
    '''
    crop_images = []
    for pan in pans:
        crop_image = GetPanTiltImg(pano_tool, frame, pan = pan, tilt = 0.0, fov = 90.0, height = 240, width = 320)
        if len(crop_images) == 0:
            crop_images = crop_image
        else:
            crop_images = np.hstack([crop_images, crop_image])
    return crop_images

def record_image_loop(cap, outfile="output.avi", isPanorama=True, Crop=True, pans=[270, 0, 90, 180], fps=0):
    if fps == 0:
        delay = 0  # As soon as possible
    else:
        delay = 1.0 / fps

    delay = int(1.0 + delay*1000.0)

    if Crop == True:
        s_time = time.time()
        pano_tool = GetPanoTool()   # It takes several seconds.

    ret, frame = cap.read()
    if ret == False:
        return

    w = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    h = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("Width : " , w)
    print("Height : " , h)    
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # Window
    fourcc = cv2.VideoWriter_fourcc(*'X264')  # Linux
    out = cv2.VideoWriter(outfile, apiPreference=None, fourcc=fourcc, fps=int(fps), frameSize=(w,h))
    recording = False

    while(ret):
        s_time = time.time()
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow("Theta360_Z1(resized)", imresize(frame, 40))
            if Crop == True:
                cropped = crop_image(frame, pano_tool, pans)
                cv2.imshow("Crop", cropped)
    
        key = cv2.waitKey(delay)
        if key == 27:
            break  # esc to quit
        elif key == ord('r'):
            recording = not recording
        print("ROS publish : Theta360Z1 at {0:1.3f} fps\r".format(1/(time.time() - s_time)), end='')
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def ros_publish_raw_loop(cap, fps=0):
    max_fps = 30
    fps = int(fps)
    if fps < 1:
        fps = 1
    elif fps > 30:
        fps = 30

    every_save_frame = int (max_fps / fps)

    ret, frame = cap.read()
    if ret == False:
        return
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Width : " , w)
    print("Height : " , h)    

    topic_theta360z1 = "theta360z1_raw"

    rospy.init_node("theta360z1_pub", anonymous=True)
    image_pub = rospy.Publisher(topic_theta360z1, Image, queue_size=1)
    bridge = CvBridge()

    #rate = rospy.Rate(fps)
    #while(ret):
    frame_count = 0
    while(not rospy.is_shutdown()):
        s_time = time.time()
        ret, frame = cap.read()  # If you do not flush (or read) gstreamer pipeline as soon as possible, You will get the old stream from it. So do not sleep.
        if ret is True:
            frame_count = frame_count + 1
        else:
            continue
        try:
            if frame_count % every_save_frame == 0:
                image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            print(e)
        print("ROS publish : Theta360Z1 at {0:1.3f} fps\r".format(1/(time.time() - s_time)), end='')
        #rate.sleep()
        if frame_count > max_fps:
            frame_count = 0
    
    cap.release()
    
def ros_publish_compressed_loop(cap):
    ret, frame = cap.read()
    if ret == False:
        return
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    topic_theta360z1 = "theta360z1_compressed"

    rospy.init_node("theta360z1_pub", anonymous=True)
    image_pub = rospy.Publisher(topic_theta360z1, CompressedImage, queue_size=1)
    bridge = CvBridge()

    while(ret):
        ret, frame = cap.read()
        try:
            image_pub.publish(bridge.cv2_to_compressed_imgmsg(frame))
        except CvBridgeError as e:
            print(e)
    
    cap.release()

def get_capture_of_theta360_z1():
    cap = cv2.VideoCapture("thetauvcsrc ! decodebin ! autovideoconvert ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink", cv2.CAP_GSTREAMER)
    return cap

def get_capture_of_usbcam(cam=0):
    cap = cv2.VideoCapture(cam)
    return cap

if __name__ == "__main__":
    ## Select Camera
    opt = get_parser()
    fps = opt.fps
    cap = get_capture_of_theta360_z1()
    #cap = get_capture_of_usbcam()

    ## Record
    if opt.mode.lower() == "demo":
        record_image_loop(cap, Crop=True, pans=[270, 0, 90, 180], fps=fps)
        #record_image_loop(cap, Crop=True, pans=[0], fps=fps)
    else:
        ## ros publish
        ros_publish_raw_loop(cap, fps)
        #ros_publish_compressed_loop(cap)  # To do : do not work
