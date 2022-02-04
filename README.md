# AWS_Deepracer_with_Optitrack
---

## vrpn_client_ros
* current VRPN clients are built on ROS melodic or ROS2 foxy
* modified certain features to adapt to ROS dashing env
```
source ROS melodic & source ROS dashing
colcon build
```
change server IP to your optitrack compatible pc
> vrpn_client_ros/config/sample.params.yaml
```
ros2 launch vrpn_client_ros vrpn_launch.launch.py & ros2 run rviz2 rviz2
```
---
## vrpn_path_ext
* path extraction added along with VRPN client
* requires both python and cpp 
* path extracted will be displayed on rviz window
* csv log file created on package path share directory

change subscription to whatever body you are willing to track
```
source ROS melodic & source ROS dashing
colcon build
ros2 launch vrpn_path_ext path_launch.launch.py & ros2 run rviz2 rviz2
```
