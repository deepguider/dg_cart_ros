#!/usr/bin/env python3

# door_detect publisher from reading file

import rospy
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import CompressedImage
from dg_cart_ros.msg import BoundingBoxes, BoundingBox

import os
import time
import glob
from door_detector import DoorDetector

import cv2

detector = DoorDetector()
last_data = ""
started = False

imagepath = 'test'

def talker():  # called whenever get subscribed data

    pub_det = rospy.Publisher('door_detect_det', BoundingBoxes, queue_size=10)
    rospy.init_node('door_detect', anonymous=True)

    # get current time
    rospytimenow = rospy.Time.now()

    while not rospy.is_shutdown():
        pred, timestamp = detector.apply(imagepath, 'timestamp')

        # convert detection result (pred) to ros msg
        det_msg = BoundingBoxes()
        det_msg.header.stamp = rospytimenow
        bounding_boxes = []
        for i, (x1, y1, x2, y2, conf) in enumerate(pred[0]):
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
        print ("Last message published")



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
