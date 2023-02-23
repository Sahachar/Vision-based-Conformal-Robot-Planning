#!/usr/bin/env python3

import rospy
import numpy as np
import torch
from rostopic import get_topic_type
import cv2
from detection_msgs.msg import BoundingBox, BoundingBoxes
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CompressedImage
# from sensor_msgs.msg import Range
# from sensor_msgs.msg import Imu
# from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point, Quaternion
# from nav_msgs.msg import Odometry
from std_msgs.msg import UInt8MultiArray
import matplotlib.pyplot as plt
# from visualization_msgs.msg import Marker
import math
# import tf
import time


class prm_planner:
    
    def __init__(self):
        rospy.init_node('prm', anonymous=True)
        self.bridge = CvBridge()
        self.move_cmd = Twist()
        self.bbs = BoundingBoxes().bounding_boxes
        # self.im = np.array((480, 640, 3))
        self.grid = np.zeros((480, 640))
        plt.matshow(self.grid, cmap=plt.cm.YlOrRd)
        self.margin = 0
        self.tol = 0

        self.prev_dist = []
        self.dist = []
        self.dist = np.array(self.dist)
        self.prev_dist = np.array(self.prev_dist)

        # self.fig = plt.figure()
        
        

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
        self.img_msg = Image()
        rospy.Subscriber('/yolov5/image_out', Image, self.image_callback, queue_size=1)
        
        # Initialize the subscriber to yolo_v5 detections
        self.bounding_boxes = BoundingBoxes()
        rospy.Subscriber('/yolov5/detections', BoundingBoxes, self.prm, queue_size=1)
        self.bb = BoundingBox()

        # Initialize the Publisher for masked images
        self.image_pub = rospy.Publisher('/yolov5/masked_image', Image, queue_size=1)

        self.vel_pub = rospy.Publisher('mobile_base/cmd_vel', Twist, queue_size=1)
        



    def actuator(self, rcx, rcy, ccx, ccy, r_r, c_r):


        # if rcx.size != 0:
        #     self.dist = np.sqrt(((ccx-rcx[0])**2)+((ccy-rcy[0])**2))

        #     # Focusing on the closest cup to robot
        #     close_id = np.argmin(self.dist)
        #     self.margin = 0
        #     if(self.dist[close_id] <= (c_r[close_id] + r_r[0] + self.margin)):
        #         print("Robot Collided")
        #         self.move_cmd.linear.x = -4.0
        #         self.move_cmd.angular.z = 1.0
        #     else:
        #         self.move_cmd.linear.x = 4.0
        #         self.move_cmd.angular.z = 0.0
        # self.vel_pub.publish(self.move_cmd)

        # For testing the robot movement
        self.move_cmd.linear.x = 0.0
        self.move_cmd.angular.z = 1.0
        self.vel_pub.publish(self.move_cmd)



        # rate = rospy.Rate(30)
        # self.move_cmd.linear.x = -4.0
        # self.move_cmd.angular.z = 0.0
        # while not rospy.is_shutdown():
        #     vel_pub.publish(self.move_cmd)
        #     rate.sleep()

    def prm(self, data):
        self.bounding_boxes = data
        
        # im = self.bridge.imgmsg_to_cv2(self.img_msg, desired_encoding="bgr8")
        # for i in self.bounding_boxes.bounding_boxes:
        #     self.bb = i
            # rospy.loginfo(self.bb)


        
        
        self.bbs = self.bounding_boxes.bounding_boxes
        


        # im = torch.from_numpy(im)
        
        
        # rospy.loginfo(im.shape)


    def image_callback(self, data):
        # self.img_msg = data
        self.im = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        self.im = np.array(self.im)
        # rospy.loginfo(self.img_msg)

        # rospy.loginfo(str(self.im.shape) + ': Receiving Yolov5 Inferenced Image')

        self.bbs = np.array(self.bbs)
        rcx = []
        rcy = []
        ccx = []
        ccy = []
        r_r = []
        c_r = []

        for ebb in self.bbs:
            if ebb.Class=="Robot":
                rcx.append((ebb.xmin + ebb.xmax)/2)
                rcy.append((ebb.ymin + ebb.ymax)/2)
                r_r.append(int(np.sqrt(((ebb.xmax-ebb.xmin)**2)+(ebb.ymax-ebb.ymin)**2)/2))

                self.grid[ebb.ymin:ebb.ymax, ebb.xmin:ebb.xmax] = 1
                self.im[ebb.ymin:ebb.ymax, ebb.xmin:ebb.xmax, :] = 255

                # rospy.loginfo("Robot")
            else:
                ccx.append((ebb.xmin + ebb.xmax)/2)
                ccy.append((ebb.ymin + ebb.ymax)/2)
                c_r.append(int(np.sqrt(((ebb.xmax-ebb.xmin)**2)+(ebb.ymax-ebb.ymin)**2)/2))

                self.grid[ebb.ymin:ebb.ymax, ebb.xmin:ebb.xmax] = 2
                self.im[ebb.ymin:ebb.ymax, ebb.xmin:ebb.xmax, :] = 0
                # self.im[ebb.xmin:ebb.xmax, ebb.ymin:ebb.ymax, :] = 0
                # print(ebb.xmin, ebb.xmax, "---", ebb.ymin, ebb.ymax)        

        rcx = np.array(rcx)
        rcy = np.array(rcy)
        ccx = np.array(ccx)
        ccy = np.array(ccy)
        r_r = np.array(r_r)
        c_r = np.array(c_r)

        # self.margin = np.mean(r_r)/6

        self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.im, "bgr8"))

        self.actuator(rcx, rcy, ccx, ccy, r_r, c_r)
        
        # rospy.loginfo(len(rcx), len(rcx), len(ccx), len(ccy))
        # rospy.loginfo(rcx.shape)
        # print(ccx.shape)
        





if __name__ == '__main__':
    try:
        # global Velocity_vec
        # rospy.init_node('prm', anonymous=True)
        planner_= prm_planner()
        rospy.spin()
        # planner_.actuator()
    except rospy.ROSInitException:
        pass

