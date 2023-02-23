#!/usr/bin/env python3

import rospy
import numpy as np
from rostopic import get_topic_type
import cv2
from detection_msgs.msg import BoundingBox, BoundingBoxes
from cv_bridge.core import CvBridge
from sensor_msgs.msg import Image, CompressedImage
# from sensor_msgs.msg import Range
# from sensor_msgs.msg import Imu
# from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point, Quaternion
# from nav_msgs.msg import Odometry
from std_msgs.msg import UInt8MultiArray
# from visualization_msgs.msg import Marker
import math
# import tf
import time

class prm_planner:
    
    def __init__(self):
        rospy.init_node('prm', anonymous=True)

        # Initialize subscriber to Image/CompressedImage topic
        # input_image_type, input_image_topic, _ = get_topic_type(rospy.get_param("~input_image_topic"), blocking = True)
        # self.compressed_input = input_image_type == "sensor_msgs/CompressedImage"

        # if self.compressed_input:
        #     self.image_sub = rospy.Subscriber(
        #         input_image_topic, CompressedImage, self.callback, queue_size=1
        #     )
        # else:
        #     self.image_sub = rospy.Subscriber(
        #         input_image_topic, Image, self.callback, queue_size=1
        #     )
        self.im = Image()
        rospy.Subscriber('/yolov5/image_out', Image, self.image_callback, queue_size=1)
        
        # Initialize the subscriber to yolo_v5 detections
        self.bounding_boxes = BoundingBoxes()
        rospy.Subscriber('/yolov5/detections', BoundingBoxes, self.controller, queue_size=1)



    def prm(self):
        vel_pub = rospy.Publisher('mobile_base/cmd_vel', Twist, queue_size=10)
        
        rate = rospy.Rate(30)
        
        move_cmd = Twist()
        move_cmd.linear.x = -4.0
        move_cmd.angular.z = 0.0

        while not rospy.is_shutdown():
            vel_pub.publish(move_cmd)
            rate.sleep()

    def controller(self, data):
        self.bounding_boxes = data
    

    def image_callback(self, data):
        self.im = data
        rospy.loginfo(self.im.header)




if __name__ == '__main__':
    try:
        planner_= prm_planner()
        planner_.prm()
    except rospy.ROSInitException:
        pass

