#!/usr/bin/env python

import rospy;
import numpy as np;
import string;
import cv2;
from cv_bridge import CvBridge, CvBridgeError;
from sensor_msgs.msg import Image;
from sensor_msgs.msg import CameraInfo;

curr_index 	= 0;
data_dir 	= rospy.get_param('kitti_image_dir');

def main():

	rospy.init_node('kitti_loader');
	bridge = CvBridge();

	img_pub  	= rospy.Publisher('/kitti_loader/image_mono', Image, queue_size=1);
	width_pub 	= rospy.Publisher('/kitti_loader/camera_info', CameraInfo, queue_size=1);

	rate = 8;
	r = rospy.Rate(rate);

	past_track_bbs_ids = [];

	while not rospy.is_shutdown():
		global curr_index;
		global data_dir;

		#getting the image path
		str_curr_index 	= str(curr_index);
		for i in range(6 - len(str_curr_index)):
			str_curr_index = '0' + str_curr_index;
		image_name 		= str_curr_index + '.png';
		image_path 		= data_dir + image_name;

		#load the image in grayscale
		try:
			img 				= cv2.imread(image_path, 0);
			height, width 		= img.shape;
			msg  			 	= bridge.cv2_to_imgmsg(img, encoding="mono8");

			cam_info_msg 	 	= CameraInfo();
			cam_info_msg.width 	= width;
			cam_info_msg.height = height;

			img_pub.publish(msg);
			width_pub.publish(cam_info_msg);

			curr_index += 1;
		except:
			curr_index = 0;

		r.sleep();


if __name__ == "__main__":
	main();