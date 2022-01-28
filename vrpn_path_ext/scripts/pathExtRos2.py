#!/usr/bin/env python3

print('file init')

import os
import sys
from turtle import distance
import rclpy
import ros2pkg

from math import pi, cos, sin, sqrt, pow, atan2
from nav_msgs.msg import Path, Odometry
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
# Found https://automaticaddison.com/how-to-create-a-tf-listener-using-ros-2-and-python/
import tf2_ros #it says that tf2_ros exists but i can't find it... maybe i need to download it?

from rclpy.node import Node #added line
from ament_index_python.packages import get_package_share_directory #for touchPathFile

# actually in most examples this starts as
# class PathExtraction(Node) : .. 
# but since i am not good at python files, i'll just mark it here
# hopefully someone will find the error and solve them..
class PathExtraction(Node):

    def __init__(self):
        super().__init__('path_extraction')
        # super().init(args=sys.argv)
        # node = rclpy.create_node('path_extraction')
        # not sure to use 'Node' or 'node'

        print('ros init')
        # ROS Publisher
        self.path_rviz_pub = self.create_publisher(Path, '/path_rviz', 10)
        self.path_msg = Path()

        # ROS Subscriber
        self.create_subscription(NavSatFix, "/nav_sat/fix", self.gpsCallback)
        #Node.create_subscription(NavSatFix, "/nav_sat/fix", self.gpsCallback)
        self.create_subscription(Odometry, "/Ego_globalstate", self.poseCallback)
        #Node.create_subscription(Odometry, "/Ego_globalstate", self.poseCallback)

        print('configure start')
        self.configure()
        print('configure end')
        self.is_status = False
        self.prev_x = 0
        self.prev_y = 0
        self.gps_init_latitude = 0
        self.gps_inti_longitude = 0
        self.gps_first = False
        
        # find directory to save path file
        self.touchPathFile()

        # receive pose msg and write path file
        #########################################################################
        rate = rclpy.spin() # actually Rate doesn't exist in rclpy
        # Found https://answers.ros.org/question/358343/rate-and-sleep-function-in-rclpy-library-for-ros2/
        # well, i can't fxxking understand^^

        print('before loop')
        try:
            while not rclpy.ok(): # replaced from rospy.is_shutdown()
                if self.is_status == True :
                    self.savePath()
                rate.sleep() # due to rate issue, this doesn't work
        except KeyboardInterrupt:
            self.f.close()
            # rospy.logwarn() or rospy.loginfo doesn't work for ROS2
            # this part i think should be 'node' not 'Node'
            # Found https://docs.ros.org/en/crystal/Contributing/Migration-Guide-Python.html
            self.get_logger().warn("-----------------------------------------------------")
            self.get_logger().info("[Init GPS Origin] Latitude / Longitude : %.9f / %.9f", self.gps_init_latitude, self.gps_inti_longitude)
            self.get_logger().warn("-----------------------------------------------------")
            #upper 3 lines...i'm not so sure
        
    def configure(self):
        # Found https://roboticsbackend.com/rclpy-params-tutorial-get-set-ros2-params-with-python/
        # i think this part should be 'node'... but....
        self.path_directory_name = self.declare_parameter("~path_directory_name").value
        self.path_file_name = self.declare_parameter("~path_file_name")
        self.min_sample_distance = self.declare_parameter("~min_sample_distance")

    def touchPathfile(self):
        # RosPack() doesn't work for ros2
        # Found https://answers.ros.org/question/288501/ros2-equivalent-of-rospackagegetpath/
        # below are changed lines
        pkg_path = get_package_share_directory('path_extraction')
        full_path = pkg_path + '/' + self.path_directory_name + '/' + self.path_file_name
        self.f = open(full_path, 'w')
    
    def gpsCallback(self, msg):
        if self.gps_first == False:
            self.gps_init_latitude = msg.latitude
            self.gps_inti_longitude = msg.longitude
            self.gps_first = True

            # same as above
            self.get_logger().warn("-----------------------------------------------------")
            self.get_logger().info("[Init GPS Origin] Latitude / Longitude : %.9f / %.9f", self.gps_init_latitude, self.gps_inti_longitude)
            self.get_logger().warn("-----------------------------------------------------")

    def poseCallback(self, msg):
        self.is_status = True

        self.path_frame_id = msg.header.frame_id
        self.status_msg = msg.pose.pose
        Ego_HeadingAngle = [self.status_msg.orientation.x, self.status_msg.orientation.y, self.status_msg.orientation.z, self.status_msg.orientation.w]

        # since i can't find tf i'll just let these line be in ROS1 ver.
        # self.TFsender = tf.TransformBroadcaster()
        # self.TFsender.sendTransform((self.status_msg.position.x, self.status_msg.position.y, 0),
        #                 Ego_HeadingAngle,
        #                 rospy.Time.now(),
        #                 "gps",
        #                 "map")

    def savePath(self):
        x = self.status_msg.position.x
        y = self.status_msg.position.y
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
    try:
        path_extracter = PathExtraction()
    except KeyboardInterrupt: # doen't run in rclpy
        pass
    # Found https://github.com/ros2/rclpy/issues/22
    # Found https://github.com/ros2/rclpy/issues/224
    # but i can't make out what they are saying..

rclpy.shutdown()