#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import NavSatFix


import sys
from socket import *
import time

# ECHO_PORT default port
ECHO_PORT = 7777

# buffer size
BUFSIZE = 1024

def talker():
    pub = rospy.Publisher('andro2linux_gps', NavSatFix, queue_size=10)
    rospy.init_node('andro2linux_gps_publisher', anonymous=True)
    
    # socket type (UDP = SOCK_DGRAM, TCP = SOCK_STREAM)
    s = socket(AF_INET, SOCK_DGRAM)
    
    # port setup
    s.bind(('', ECHO_PORT))
    
    # ready!
    print('udp echo server ready')

    # infinite loop
    while 1:
        # Waiting for client
        data, addr = s.recvfrom(BUFSIZE)

        # extract the information from fused provided
        splitted_data = str(data).split("\n")
        provider = splitted_data[0].split()[1]
        if provider == 'fused':
            gpsmsg=NavSatFix()
            gpsmsg.header.stamp = rospy.Time.now()
            gpsmsg.header.frame_id = "gps"
            
            #print(splitted_data)
            longitude = float(splitted_data[1].split()[1])
            latitude = float(splitted_data[2].split()[1])
            altitude = float(splitted_data[3].split()[1])
            accuracy = float(splitted_data[4].split()[1])
            variance = accuracy * accuracy
            hasspeed = splitted_data[5].split()[1] == 'true'

            gpsmsg.latitude=latitude
            gpsmsg.longitude=longitude
            gpsmsg.altitude=altitude
            gpsmsg.position_covariance_type=NavSatFix.COVARIANCE_TYPE_APPROXIMATED
            gpsmsg.position_covariance=(variance,0,0, 0,variance,0, 0,0,variance)

            print(gpsmsg)
            print("------------------------")

            # publish
            pub.publish(gpsmsg)
            if rospy.is_shutdown():
                break
    
        # send back to client
        s.sendto(data, addr)
        # back to the beginning of loop


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
