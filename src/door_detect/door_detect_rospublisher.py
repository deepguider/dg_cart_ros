#!/usr/bin/env python3

# door detection publisher with sensor input (subscriber)

import rospy
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import CompressedImage
from dg_cart_ros.msg import BoundingBoxes, BoundingBox

import os
import time
import glob
from door_detector import DoorDetector

import cv2
import numpy as np

detector = DoorDetector()
detector.init_model()
last_data = ""
started = False
pub_img = rospy.Publisher('door_detect_img/compressed', CompressedImage, queue_size=1000)
pub_det = rospy.Publisher('door_detect_det', BoundingBoxes, queue_size=10)

imagepath = 'test'

def subscribe_callback(data):  # called whenever get subscribed data
    # get current time
    rospytimenow = rospy.Time.now()

    
    # CompressedImage (ros msg) to cv2
    np_arr = np.fromstring(data.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # detect door
    pred, img_with_bboxresult = detector.detect_image(img)

    # convert img_with_bboxresult to ros msg
    img_msg = CompressedImage()
    img_msg.header.stamp = rospytimenow
    img_msg.format = "jpg"
    img_msg.data = np.array(cv2.imencode('.jpg', img_with_bboxresult)[1]).tostring()
    pub_img.publish(img_msg)

    # convert detection result (pred) to ros msg
    det_msg = BoundingBoxes()
    det_msg.header.stamp = rospytimenow
    bounding_boxes = []
    for i, (x1, y1, x2, y2, conf) in enumerate(pred):
        one_det_msg = BoundingBox()
        one_det_msg.id = int(i)
        one_det_msg.xmin = int(x1)
        one_det_msg.xmax = int(x2)
        one_det_msg.ymin = int(y1)
        one_det_msg.ymax = int(y2)
        one_det_msg.probability = conf
        bounding_boxes.append(one_det_msg)

    det_msg.bounding_boxes = bounding_boxes
    pub_det.publish(det_msg)




def listener():
    rospy.init_node('door_detect', anonymous=True)
    rospy.Subscriber("/uvc_camera/image_raw/compressed", CompressedImage, subscribe_callback)

    rospy.spin()



if __name__ == '__main__':
    listener()
