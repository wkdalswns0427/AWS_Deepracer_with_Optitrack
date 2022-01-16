# vrpn_client_ros

## Requirements

The code requires VRPN to work. Unfortunately, currently the package is only
available in melodic and older ROS releases and can be installed with:
```
    apt-get install ros-melodic-vrpn
```

## What works?

I only use pose in my project, so I did not port anything else (TF, twist, accel). Also multiple sensors per tracker are not ported.
If there is anyone who would like to use the other features and is willing to test them, I'd be happy to help.
