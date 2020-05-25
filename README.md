## DeepGuider Cart for ROS
DeepGuider Cart for ROS (shortly _dg\_cart\_ros_) is a mobile platform for [DeepGuider](https://github.com/deepguider) project to acquire datasets and test algorithms integrated with sensors.

### Mobile and Computing Platforms
* Mobile platform: CareLine [Nadri 500](http://www.care-line.co.kr/H-R-careline/scooter/nadri500.php)
  * Maximum velocity: 15 km/hr (~ 4.2 m/s)
  * Maximum climbing angle: 10 deg
  * Battery capacity: 64 AH (mileage: 35 km)
* Computing board: Gigabyte [Aero 15 OLED XA](https://www.notebookcheck.net/Gigabyte-Aero-15-XA-Laptop-Review-With-OLED-panel-and-4K-in-a-new-design.428407.0.html)
  * CPU: [Intel Core i7-9750H](https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i7-9750H+%40+2.60GHz&id=3425)
  * GPU: [NVIDIA GeForce RTX 2070 Max-Q](https://www.videocardbenchmark.net/gpu.php?id=4048)

### Sensor Specifications (and Their ROS Nodes)
* [UVC](https://en.wikipedia.org/wiki/USB_video_device_class) camera: Logitech [C930e](https://www.logitech.com/product/c930e-webcam) ([uvc\_camera](http://wiki.ros.org/uvc_camera))
  * [1920x1080](https://en.wikipedia.org/wiki/1080p) / 30 fps / FOV: 90 deg
* RGB-D camera: Intel [RealSense D435i](https://www.intelrealsense.com/depth-camera-d435i/) ([realsense2\_camera](http://wiki.ros.org/realsense2_camera))
  * RGB: 1920x1080 / 30 fps / FOV (HxV): 69.4x42.5 deg
  * Depth: 1280x720 / 90 fps / FOV (HxV): 87x58 deg
  * IMU: 3 DoF accleration ($\pm$4 g), 3 DoF gyroscope ($\pm$1000 deg/s)
* Spherical camera: Ricoh [Theta S](https://theta360.com/)
* IMU/AHRS: Xsens [MTi-30](https://www.xsens.com/products/mti-10-series) ([xsens\_driver](http://wiki.ros.org/xsens_driver))
  * Gyro bias stability: 18 deg/hr
  * Roll/Pitch accuracy: Static 0.2 deg, dynamic 0.5 deg
  * Yaw accuracy: 1.0 deg
* GPS receiver: Ascen Korea [GPS620](http://freenavi.co.kr/product/detail.html?product_no=38) ([nmea\_navsat\_driver](http://wiki.ros.org/nmea_navsat_driver))
  * Accuracy (Position Single Point L1): 3.0 m
  * Frequency: 1 Hz
  * [TTFF](https://en.wikipedia.org/wiki/Time_to_first_fix) (hot/cold): 1/35 sec
* RTK-GPS receiver: Novatel [PwrPak7](https://novatel.com/products/receivers/enclosures/pwrpak7) + [OEM7700](https://novatel.com/products/receivers/oem-receiver-boards/oem7-receivers/oem7700) + [GNSS-802](https://novatel.com/products/antennas/vexxis-series-antennas/vexxis-gnss-800-series-antennas) ([novatel\_gps\_driver](http://wiki.ros.org/novatel_gps_driver))
  * Accuracy (Position Single Point L1): 1.5 m
  * Accuracy (DGPS/RTK): 40/1 cm



### Installation
#### Prerequisite
* [ROS](https://www.ros.org/) Melodic Morenia ([Installation Instructions](http://wiki.ros.org/melodic/Installation))
  * Tested on [Ubuntu](https://ubuntu.com/download/alternative-downloads) 18.04 LTS

#### Installing ROS Nodes
* `sudo apt install ros-melodic-uvc-camera ros-melodic-realsense2-camera ros-melodic-xsens-driver ros-melodic-nmea-navsat-driver ros-melodic-novatel-gps-driver`

#### Making a ROS workspace
If you don't have a ROS workspace, please make it as the following. You can change its name `dg_ws` to your desired.
* `mkdir -p dg_ws/src && cd dg_ws && catkin_make`

If you can run the following to add `dg_ws` to `ROS_PACKAGE_PATH`.
* `echo "source ~/dg_ws/install/setup.bash" >> ~/.bashrc`

Or you need to run `source ~/dg_ws/install/setup.bash` every time when you open a terminal.

#### Installing dg\_cart\_ros
1. Clone dg\_cart\_ros repository
  * `cd dg_ws`
  * `git clone https://github.com/deepguider/dg_cart_ros.git src`

2. Build and install dg\_cart\_ros
  * `catkin_make install`

3. Add [udev](https://wiki.debian.org/udev) rules for accessing and mounting sensor devices
  * `sudo cp src/dg_cart_ros/udev.rules /etc/udev/rules.d/99-dg-device.rules`



### User Guides
#### Running and Visualizing Sensor Data
* Running sensor nodes
  * `roslaunch dg_cart_ros dg_run_sensor.launch`
* Running and visualizing sensor data
  * `roslaunch dg_cart_ros dg_show_sensor.launch`
* Running, visualizing, and recording sensor data
  * `roslaunch dg_cart_ros dg_record_sensor.launch`
  * Add `bag_path:=/your/target/path/` to specify a path to save a bag file (default: your `HOME` directory)

#### Running the DeepGuider Main Module
* `roslaunch dg_cart_ros dg_main_module.launch`

#### Running a Single Sensor Node
Sometimes you want to operate a single sensor without dg\_cart\_ros. The following single-line commands will run a ROS node for each sensor. (Please be aware of running `roscore` before `rosrun` commands.)

* [UVC](https://en.wikipedia.org/wiki/USB_video_device_class) camera ([uvc\_camera](http://wiki.ros.org/uvc_camera))
  * `rosrun uvc_camera uvc_camera_node`
  * Add  `device="/dev/videoLGT0"` to specify a camera device
* RGB-D camera ([realsense2\_camera](http://wiki.ros.org/realsense2_camera))
  * `roslaunch realsense2_camera rs_camera.launch`
  * Add `serial_no:="000000000000"` to specify a camera device
* IMU/AHRS ([xsens\_driver](http://wiki.ros.org/xsens_driver))
  * `roslaunch xsens_driver xsens_driver.launch`
  * Add `device:="/dev/ttyIMU0"` to specify a serial port
* GPS receiver ([nmea\_navsat\_driver](http://wiki.ros.org/nmea_navsat_driver))
  * `roslaunch nmea_navsat_driver nmea_serial_driver.launch`
  * Add `port:="/dev/ttyGPS0" baud="9600"` to specify its serial port
* RTK-GPS receiver ([novatel\_gps\_driver](http://wiki.ros.org/novatel_gps_driver))
  * `rosrun novatel_gps_driver novatel_gps_node`
  * Add `device:="/dev/ttyNVT0"` to specify a serial port



### License
Please refer [DeepGuider Project LSA](LICENSE.md).



### Acknowledgement
The authors thank the following contributors and projects.

* This work was supported by the ICT R&D program of [MSIT](https://msit.go.kr/)/[IITP](https://www.iitp.kr/), *Development of AI Technology for Guidance of a Mobile Robot to its Goal with Uncertain Maps in Indoor/Outdoor Environments* (2019-0-01309).
