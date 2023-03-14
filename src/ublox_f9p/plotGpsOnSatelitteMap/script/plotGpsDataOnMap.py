#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix,NavSatStatus,TimeReference
import matplotlib.pyplot as plt
import utm

def callback(data):
    rospy.loginfo("lat [%f], lon [%f], status [%i]", data.latitude, data.longitude, data.status.status)
    # with open('dataBlueTeam.txt','a') as f: f.write('{0} {1} {2}\n'.format(data.latitude, data.longitude, data.status.status))
    global gx, gy
    (gx,gy,_,_) = utm.from_latlon(data.latitude, data.longitude)
    #plt.scatter(x=[data.longitude], y=[data.latitude], s = 45, c='b') #sets your home position
    plot()

def plot():
    global gx, gy, gx0, gy0
    if (gx is not None) and (gy is not None):
        if (gx0 is None) and (gy0 is None):
            gx0, gy0 = gx, gy
        dgx, dgy = gx0-gx, gy0-gy
        #print("utm_x, utmy = {0:%f} , utm_y".format(dgx, dgy))
        #now plot the data on a graph
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('POSITION (in Decimal Degrees)')
        plt.scatter(x=dgx, y=dgy, s = 45, c='b') #sets your home position
        plt.draw()
        plt.pause(0.001)

def initialisation():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('plotGpsDataOnMap')

    rospy.Subscriber("/ublox_gps/fix", NavSatFix, callback)
    print("Reaches here only once.")

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    global gx, gy, gx0, gy0
    gx, gy, gx0, gy0 = None, None, None, None
    initialisation()
