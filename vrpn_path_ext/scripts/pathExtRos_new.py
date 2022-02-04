#!/usr/bin/env python3

print('file init')

import os
import time
import sys
import rclpy
import ros2pkg
from rclpy.qos import QoSProfile

from math import pi, cos, sin, sqrt, pow, atan2
from nav_msgs.msg import Path, Odometry
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
# Found https://automaticaddison.com/how-to-create-a-tf-listener-using-ros-2-and-python/
# import tf2_ros 
# #it says that tf2_ros exists but i can't find it... maybe i need to download it?

from rclpy.node import Node #added line
from ament_index_python.packages import get_package_share_directory #for touchPathFile


class PathExtraction(Node):

    def __init__(self):
        super().__init__('vrpn_path_ext')
        
        print('ros init')
        self.touchPathFile()
        qos_profile = QoSProfile(depth=10)

        # ROS Publisher
        self.path_rviz_pub = self.create_publisher(Path, '/path_rviz', qos_profile)
        self.path_msg = Path()

        # ROS Subscriber
        print('bf sub')
        self.create_subscription(PoseStamped, "/RigidBody/pose", self.poseCallback, qos_profile)
        print('af sub')
        

        
        self.is_status = False
        self.prev_x = 0
        self.prev_y = 0
        

    def touchPathFile(self):
        pkg_path = get_package_share_directory('vrpn_path_ext')
        # full_path = pkg_path + '/' + self.path_directory_name + '/' + self.path_file_name
        abcde = time.time()
        full_path = pkg_path + '/' +'path_ext' + '/' +'data_log_{}.csv'.format(abcde)
        self.f =open(full_path, 'a')
    
    def poseCallback(self, msg):
        print('poseCallback init')
        self.is_status = True
        self.path_frame_id = msg.header.frame_id
        self.status_msg = msg.pose.position
        print('poseCallback done')
        if self.is_status == True:
            self.savePath()
        else:
            print("something went wrong")
        

    def savePath(self):
        
        x = self.status_msg.x
        y = self.status_msg.y
        z = 0

        # distance between 2 path points
        distance = sqrt(pow(x - self.prev_x, 2) + pow(y - self.prev_y, 2))

        if distance > 0.15:
            data = '{0},{1},{2}\n'.format(x, y, z)
            self.f.write(data)
            self.prev_x = x
            self.prev_y = y

            print(x, y)

            last_point = PoseStamped()
            last_point.pose.position.x = x
            last_point.pose.position.y = y
            last_point.pose.position.z = 0.0
            last_point.pose.orientation.x = 0.0
            last_point.pose.orientation.y = 0.0
            last_point.pose.orientation.z = 0.0
            last_point.pose.orientation.w = 1.0

            self.path_msg.header.frame_id = self.path_frame_id
            self.path_msg.poses.append(last_point)
            self.path_rviz_pub.publish(self.path_msg)

if __name__ == '__main__':
    rclpy.init()
    path_extractor = PathExtraction()
    try:
        while rclpy.ok():
            print("spin")
            rclpy.spin_once(path_extractor, timeout_sec = 0.1)
    

    except KeyboardInterrupt: 
        path_extractor.f.close()
        rclpy.shutdown()
        pass
        
    # Found https://github.com/ros2/rclpy/issues/22
    # Found https://github.com/ros2/rclpy/issues/224
    # but i can't make out what they are saying..
