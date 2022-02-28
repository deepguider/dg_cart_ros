import glob
from ipdb import set_trace as bp
import cv2
import numpy as np

import os
import time

import panorama as pn

'''
pip install GPSPhoto, exifread, pillow, piexif, selenium, folium, utm, scipy
'''

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

def makedir(fdir):
    import os
    if not os.path.exists(fdir):
        os.makedirs(fdir)

def GetPanoTool():
    pano_tool = pn.PanoramicImageTool()
    return pano_tool

def GetPanTiltImg(pano_tool = None, pano_image = None, pan = 0.0, tilt = 0.0, fov = 70.0, height = 960, width = 1280):
    # pano_image is output of cv2.imread()
    # tilt angle in [deg]
    # pan angle in [deg]
    # width and height in [px]

    if pano_tool is None:
        pano_tool = pn.PanoramicImageTool()

    pano_tool.set_panoramic_image(pano_image)
    pano_tool.set_view_angles(pan, tilt, fov)
    crop_image = pano_tool.crop((height, width))
    return crop_image

def record_image_loop(cap, isPanorama=True, Crop=True, pans=[270, 0, 90, 180]):
    if Crop == True:
        s_time = time.time()
        pano_tool = GetPanoTool()   # It takes several seconds.

    ret, frame = cap.read()
    if ret == False:
        return

    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while(ret):
        s_time = time.time()
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Theta360_Z1(resized)", imresize(frame, 40))
            if Crop == True:
                cropped = crop_image(frame, pano_tool, pans)
                cv2.imshow("Crop", cropped)
    
        key = cv2.waitKey(1)
        if key == 27: 
            break  # esc to quit
    
    cap.release()
    cv2.destroyAllWindows()


def get_capture_of_usbcam(cam=0):
    cap = cv2.VideoCapture(cam)
    return cap 

def get_capture_of_theta360_z1():
    cap = cv2.VideoCapture("thetauvcsrc ! decodebin ! autovideoconvert ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink", cv2.CAP_GSTREAMER)
    return cap 

if __name__ == "__main__":
    if False:
        ## Web Cam.
        cap = get_capture_of_usbcam()
        record_image_loop(cap, Crop=False)

    if True:
        ## 360 Cam.
        cap = get_capture_of_theta360_z1()
        record_image_loop(cap, Crop=True, pans=[270, 0, 90, 180])
