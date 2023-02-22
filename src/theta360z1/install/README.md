ccsmm@etri.re.kr

Run ./install.sh to install environment for theta360z1 on your ubuntu18.04.
After that, you can test theta360 z1's ros(melodic) pub/sub with ../publsih/run_test.sh

If you have met error during running ./install.sh due to uninstalled opencv, then following opencv install process

# Prepare opencv installation

git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd opencv
mkdir build
cd build

sudo apt-get -y install build-essential cmake
sudo apt-get -y install pkg-config
sudo apt-get -y install libjpeg-dev libtiff5-dev libpng-dev 
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev
sudo apt-get -y install libv4l-dev v4l-utils
sudo apt-get -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get -y install libgtk2.0-dev libgtk-3-dev libqt4-dev libqt5-dev
sudo apt-get -y install mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev
sudo apt-get -y install libatlas-base-dev gfortran libeigen3-dev
sudo apt-get -y install python2.7-dev python3-dev python-numpy python3-numpy

cmake \
	-D CMAKE_BUILD_TYPE=Release	\
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D BUILD_WITH_DEBUG_INFO=OFF \
	-D BUILD_EXAMPLES=ON \
	-D BUILD_opencv_python3=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
	-D OPENCV_GENERATE_PKGCONFIG=ON \
	-D WITH_GSTREAMER=ON \
	-D WITH_V4L=ON \
	-D WITH_FFMPEG=ON \
	-D WITH_TBB=ON ..

# Build opencv
time make -j$(nproc); sudo make install
