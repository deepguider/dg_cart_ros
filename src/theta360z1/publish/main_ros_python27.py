#ccsmm@etri.re.kr

import cv2
import time
import numpy as np
from parse_image import GetPanoTool, GetPanTiltImg
from ipdb import set_trace as bp

import rospy  # python 2.7
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

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

def record_image_loop(cap, outfile="output.avi", isPanorama=True, Crop=True, pans=[270, 0, 90, 180]):

    if Crop == True:
        s_time = time.time()
        pano_tool = GetPanoTool()   # It takes several seconds.

    ret, frame = cap.read()
    if ret == False:
        return

    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # Window
    fourcc = cv2.VideoWriter_fourcc(*'X264')  # Linux
    out = cv2.VideoWriter('output.avi', fourcc, 10.0, (w,h))
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
    
        key = cv2.waitKey(1)
        if key == 27:
            break  # esc to quit
        elif key == ord('r'):
            recording = not recording
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def ros_publish_loop(cap, fps=0):
    if fps == 0:
        delay = 0  # As soon as possible
    else:
        delay = 1 / fps
    
    ret, frame = cap.read()
    if ret == False:
        return
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print "Width :" , w
    print "Height :" , h

    topic_theta360z1 = "theta360z1_image"

    rospy.init_node("theta360z1_pub", anonymous=True)
    image_pub = rospy.Publisher(topic_theta360z1, Image, queue_size=1)
    bridge = CvBridge()

    while(ret):
        ret, frame = cap.read()
        image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        #cv2.waitKey(delay)  # blocked
        time.sleep(delay)
    
    cap.release()
    

def get_capture_of_theta360_z1():
    cap = cv2.VideoCapture("thetauvcsrc ! decodebin ! autovideoconvert ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink", cv2.CAP_GSTREAMER)
    return cap

def get_capture_of_usbcam(cam=0):
    cap = cv2.VideoCapture(cam)
    return cap

if __name__ == "__main__":
    ## Select Camera
    fps = 1
    cap = get_capture_of_theta360_z1()
    #cap = get_capture_of_usbcam()

    ## Record
    #record_image_loop(cap, Crop=True, pans=[270, 0, 90, 180])
    #record_image_loop(cap, Crop=True, pans=[0])

    ## ros publish
    ros_publish_loop(cap, fps=fps)
