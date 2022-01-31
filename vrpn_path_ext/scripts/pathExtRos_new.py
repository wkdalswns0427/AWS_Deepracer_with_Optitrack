#!/usr/bin/env python3

print('file init')

import os
import sys
import rclpy
import ros2pkg

from math import pi, cos, sin, sqrt, pow, atan2
from nav_msgs.msg import Path, Odometry
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
# Found https://automaticaddison.com/how-to-create-a-tf-listener-using-ros-2-and-python/
# import tf2_ros #it says that tf2_ros exists but i can't find it... maybe i need to download it?

from rclpy.node import Node #added line
from ament_index_python.packages import get_package_share_directory #for touchPathFile


class PathExtraction(Node):

    def __init__(self):
        super().__init__('vrpn_path_ext')
        
        print('ros init')
        # ROS Publisher
        self.path_rviz_pub = self.create_publisher(Path, '/path_rviz', 10)
        self.path_msg = Path()

        # ROS Subscriber
        self.create_subscription(PoseStamped, "/Path_Ext", self.poseCallback)
        
        print('configure start')
        self.configure()
        print('configure end')
        self.is_status = False
        self.prev_x = 0
        self.prev_y = 0
        
        # find directory to save path file
        self.touchPathFile()

        timer_period = 0.03
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        # print('loop start: timer_callback')
        try:
            while rclpy.ok():
                # print('loop start: timer_callback')
                if self.is_status == True :
                    print('loop start: timer_callback')
                    self.savePath()
                #rate.sleep()
        except KeyboardInterrupt:
            self.f.close()
        
    def configure(self):
        self.path_directory_name = self.declare_parameter("Path_Ext")
        self.path_file_name = self.declare_parameter("extractedPath.csv")
        self.min_sample_distance = self.declare_parameter("0.15")

    def touchPathFile(self):
        pkg_path = get_package_share_directory('vrpn_path_ext')
        # full_path = pkg_path + '/' + self.path_directory_name + '/' + self.path_file_name
        full_path = pkg_path + '/' +'path_ext' + '/' +'extractedPath.csv'
        self.f =open(full_path, 'w')
    
    def poseCallback(self, msg):
        self.is_status = True

        self.path_frame_id = msg.header.frame_id
        self.status_msg = msg.pose.position
        # Ego_HeadingAngle = [self.status_msg.orientation.x, self.status_msg.orientation.y, self.status_msg.orientation.z, self.status_msg.orientation.w]

        # since i can't find tf i'll just let these line be in ROS1 ver.
        # self.TFsender = tf.TransformBroadcaster()
        # self.TFsender.sendTransform((self.status_msg.position.x, self.status_msg.position.y, 0),
        #                 Ego_HeadingAngle,
        #                 rospy.Time.now(),
        #                 "gps",
        #                 "map")

    def savePath(self):
        x = self.status_msg.x
        y = self.status_msg.y
        z = 0

        # distance between 2 path points
        distance = sqrt(pow(x - self.prev_x, 2) + pow(y - self.prev_y, 2))

        if distance > self.min_sample_distance:
            data = '{0}\t{1}\t{2}\n'.format(x, y, z)
            self.f.write(data)
            self.prev_x = x
            self.prev_y = y

            # debug
            print(x, y)

            last_point = PoseStamped()
            last_point.pose.position.x = x
            last_point.pose.position.y = y
            last_point.pose.position.z = 0
            last_point.pose.orientation.x = 0
            last_point.pose.orientation.y = 0
            last_point.pose.orientation.z = 0
            last_point.pose.orientation.w = 1

            self.path_msg.header.frame_id = self.path_frame_id
            # self.path_msg.header.frame_id = 'map'
            self.path_msg.poses.append(last_point)
            self.path_rviz_pub.publish(self.path_msg)

if __name__ == '__main__':
    rclpy.init()
    try:
        path_extractor = PathExtraction()
        rclpy.spin(path_extractor)

    except KeyboardInterrupt: 
        rclpy.shutdown()
        pass
        
    # Found https://github.com/ros2/rclpy/issues/22
    # Found https://github.com/ros2/rclpy/issues/224
