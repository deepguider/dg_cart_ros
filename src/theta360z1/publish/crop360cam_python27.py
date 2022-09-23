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

def crop_image(frame, pano_tool, pans=[270, 0, 90, 180], tilt=0.0, fov=90.0, height=480, width=640):
    '''
    pans = [270, 0, 90, 180]  # front, right, left, back
    '''
    crop_images = []
    for pan in pans:
        crop_image = GetPanTiltImg(pano_tool, frame, pan = pan, tilt = tilt, fov = fov, height = height, width = width)
        if len(crop_images) == 0:
            crop_images = crop_image
        else:
            crop_images = np.hstack([crop_images, crop_image])
    return crop_images

topic_theta360z1_crop = "theta360z1_crop"
crop_pub = rospy.Publisher(topic_theta360z1_crop, Image, queue_size=1)
bridge = CvBridge()
pano_tool = GetPanoTool()

def crop_360cam_callback(msg):
    print("Cropping 360cam to images!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_pano_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    # cropped = crop_image(cv2_pano_img, pano_tool, pans=[90, 180, 270])  # (old version) Left, Front, Right
    cropped = crop_image(cv2_pano_img, pano_tool, pans=[270, 0, 90])  # Left, Front, Right
    crop_pub.publish(bridge.cv2_to_imgmsg(cropped, "bgr8"))

def ros_subscriber_crop():
    topic_theta360z1 = "theta360z1_raw"
    rospy.init_node("theta360z1_crop", anonymous=True)
    rospy.Subscriber(topic_theta360z1, Image, crop_360cam_callback)
    # Spin until ctrl + c
    rospy.spin()
    
if __name__ == "__main__":
    ros_subscriber_crop()
