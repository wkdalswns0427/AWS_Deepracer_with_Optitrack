# VRPN Client & Publish Pose and Velocity for DeepRacer

both process runs simultaneously on a singl launch action

```
ros2 launch vrpn_status_pub status.launch.py
```

Publishes Odometry type topic for DeepRacer

>**Pose** same as PoseStamped of VRPN Client

>**Twist.linear.x** is linear velocity of DeepRacer
