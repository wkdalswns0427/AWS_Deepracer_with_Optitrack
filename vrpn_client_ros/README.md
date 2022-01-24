# vrpn_client_ros

## Requirements

The code requires VRPN to work. Unfortunately, currently the package is only
available in melodic and older ROS releases and can be installed with:
```
    apt-get install ros-melodic-vrpn
```
```
    sourc ROS melodic first, source ROS dashing on same terminal
    colcon build
```
launch with 
```
    ros2 launch vrpn_client_ros vrpn_launch.launch.py & ros2 run rviz2 rviz2
```
topic named 'RighdBody' should appear on your ros2 topic list command
