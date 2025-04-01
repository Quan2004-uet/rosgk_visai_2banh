# rosgk_visai_2banh
catkin_make
source devel/setup.bash
roslaunch test1 gazebo.launch (open gazebo)
roslaunch test1 display.launch (open rviz)
Rviz: Add > Robot model > Sensor(camera, lidar, imu) > Topic 
rosrun test1 control1.py (control robot 2 wheels in gazebo by keyboard)
rosrun test1 arm1.py (control robot 2 links in gazebo by keyboard)
Lib/pkg need to install: pynput, gazebo-ros, gazebo-ros-control, controller-manager, velocity-controllers, effort-controllers
video in drive(set 1080p) 
