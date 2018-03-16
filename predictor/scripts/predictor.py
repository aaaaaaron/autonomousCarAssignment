#!/usr/bin/env python

from sort import *;
from darknet_ros.msg import bbox;
from darknet_ros.msg import bbox_array;
import rospy;
import numpy as np;
import string;

curr_bbox_array  		= [];
prev_detections  		= [];
curr_detections  		= [];
curr_detection_classes 	= [];

image_width  	= rospy.get_param('kitti_loader/image_width');
one_fifth  	 	= image_width / 5;

def bbox_array_callback(data):
	global curr_bbox_array;
	global prev_detections;
	global curr_detections;
	global curr_detection_classes;
	global image_width;
	global one_fifth;
	prev_detections = curr_detections;
	curr_bbox_array = data.bboxes
	# get detections
	curr_detections = [];
	curr_detection_classes = [];
	for i in range (len(curr_bbox_array)):
		curr_bbox = curr_bbox_array[i];
		
		if (curr_bbox.Class == 'person' or curr_bbox.Class == 'car'):
			temp_detect = [curr_bbox.xmin, curr_bbox.ymin, curr_bbox.xmax, curr_bbox.ymax, curr_bbox.prob];
			temp_detect = np.array(temp_detect);
			curr_detections.append(temp_detect);
			curr_detection_classes.append(curr_bbox.Class);

	curr_detections = np.asarray(curr_detections);


def main():
	global mot_tracker;
	mot_tracker = Sort();

	rospy.init_node('tracker');
	sub = rospy.Subscriber('/YOLO_bboxes',bbox_array, bbox_array_callback);

	rate = 20;
	r = rospy.Rate(rate);

	past_track_bbs_ids  = [];
	curr_track_bbs_ids  = [];
	past_items 		 	= [];

	while not rospy.is_shutdown():
		global curr_bbox_array;
		global prev_detections;
		global curr_detections;
		global curr_detection_classes;
		global one_fifth;

		# update SORT
		try:
			past_track_bbs_ids = curr_track_bbs_ids;
			curr_track_bbs_ids = mot_tracker.update(curr_detections);
		# track_bbs_ids is a np array where each row contains a valid bounding box and track_id (last column)

		except:
			pass
		#no time to do proper prediction

		curr_items  	= [];
		for i in range(len(curr_track_bbs_ids)):
			curr_item = curr_track_bbs_ids[i];
			curr_items.append(curr_item[4]);

			if not (curr_item[4] in past_items):
				#simple warnings
				center 	= (curr_item[0] + curr_item[2]) / 2;
				if (center < 2*one_fifth):
					print "Careful, there is a %s on your left." % (curr_detection_classes[i]);
				elif (center >= 2*one_fifth and center < 3*one_fifth):
					print "WARNING, a %s very close to the front." % (curr_detection_classes[i]);
				else:
					print "Careful, there is a %s on your right." % (curr_detection_classes[i]);

		past_items 		= curr_items;

		r.sleep();


if __name__ == "__main__":
	main();