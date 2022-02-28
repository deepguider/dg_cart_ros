#!/bin/bash
# ccsmm@etri.re.kr
# Refer to https://community.theta360.guide/t/linux-live-streaming-quick-start-on-ubuntu-x86-how-to-build-libuvc-for-ricoh-theta-v-and-z1/6123/3

topdir=`pwd`
## 1. Install libuvc-theta
cd ${topdir}
git clone https://github.com/ricohapi/libuvc-theta
cd libuvc-theta
mkdir build
cd build
cmake ..
make && sudo make install  # libuvc.so* will be copyed to /usr/local/lib/
sudo ldconfig  # Apply copied lib. files.

## 2. Build libuvc-theta-example
## 2-1 Build gst
cd ${topdir}
git clone https://github.com/ricohapi/libuvc-theta-sample
cd libuvc-theta-sample/gst
make

## 2-2. Make gst_viewer script
cd ${topdir}
script="run_gst_viewer.sh"

echo "#!/bin/bash" > ${script}
echo "" >> ${script}
echo "## 2-3. Turn on camera" >> ${script}
echo "# - Plug RICOH THETA V or Z1 into your computer’s USB port" >> ${script}
echo "# - Turn camera on, put into “LIVE” mode by pressing the physical mode button the side of the camera button." >> ${script}
echo "# - Then the OLED or LED on the camera needs to say “LIVE”." >> ${script}
echo "" >> ${script}
echo "# - Run follwing:" >> ${script}
echo "cd ./libuvc-theta-sample/gst" >> ${script}
echo "./gst_viewer" >> ${script}
echo "cd ../../" >> ${script}
chmod +x ${script}

## 2-3. Test sample code
echo "Run ${script} for camera test"

## 3. Install gstthetauvc : extra lib. of libuvc-theta
sudo apt install libgstreamer1.0-dev
git clone https://github.com/nickel110/gstthetauvc
cd gstthetauvc/thetauvc
make
plugin_path=/usr/local/lib/
sudo cp gstthetauvc.so ${plugin_path}
echo "export GST_PLUGIN_PATH=${plugin_path}" >> ~/.bashrc
source ~/.bashrc

echo 'gst-launch-1.0 thetauvcsrc mode=4K ! queue ! h264parse ! decodebin ! queue ! autovideosink sync=false' > ${topdir}/run_gst_launch.sh
chmod +x ${topdir}/run_gst_launch.sh
 
echo 'VideoCapture cap("thetauvcsrc ! decodebin ! autovideoconvert ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink");' > ${topdir}/ex.cpp
echo '//Refer to https://github.com/nickel110/gstthetauvc for details.' >> ${topdir}/ex.cpp

echo 'cap = cv2.VideoCapture("thetauvcsrc ! decodebin ! autovideoconvert ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink", cv2.CAP_GSTREAMER)' > ${topdir}/ex.py
echo '# Refer to https://github.com/nickel110/gstthetauvc for details.' >> ${topdir}/ex.py

## 3.1 Test example
#gst-launch-1.0 thetauvcsrc mode=4K ! queue ! h264parse ! decodebin ! queue ! autovideosink sync=false

## 4. Install Python pulbisher
echo "======== Done ========"
echo "Remove old opencv library and python-opencv library"
echo "Build opencv from source code"
echo "After buidling opencv, copy /usr/local/lib/python3.6/site-packages/cv2 /home/your/.virtualenvs/dg_venv3.6/lib/python3.6/site-packages"
echo "Refer to ex.py or ex.cpp to open theta_z1"
