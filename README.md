# Interview assignment, Self Driving Car.

I integrated the use of YOLO and SORT to implement a simple object detector, Car/Person tracker, and driver warning system. I ran my tests on KITTI Dataset, data_odometry_gray.zip, it should be a 23.2GB download zip file.

![Alt Text](https://im4.ezgif.com/tmp/ezgif-4-1858e59887.gif)

## Requirements:
1) OpenCV (I used 3.3.1)
2) Able to run YOLO (not sure what all the dependencies are)
3) Ubuntu 16.04 
4) ROS Kinetic

## Setup:
I assume the above are all installed. First we set up the ROS workspace, assuming the name is catkin_ws
```
cd ~/catkin_ws/src
git clone https://github.com/aaaaaaron/autonomousCarAssignment.git
git clone https://github.com/aaaaaaron/darknet_ros.git
```
The darknet_ros package doesn't contain the configuration and weights of YOLO as they were too large, we can get them from https://github.com/leggedrobotics/darknet_ros
```
mkdir temp
cd temp
git clone https://github.com/leggedrobotics/darknet_ros.git
cd darknet_ros/darknet_ros/
cp yolo_network_config/ ~/catkin_ws/src/darknet_ros/
cd ~/catkin_ws/src/
rm -rf temp
```
now it should be set up.

## Dataset:
I downloaded it from the KITTI website http://www.cvlibs.net/datasets/kitti/eval_odometry.php, the first download listed as 22GB.
After finishing the looooonng download, unzip to somewhere you remember, take note of the absolute path.

## Making it:
cd ~/catkin_ws
source devel/setup.bash
catkin_make

## Setting Parameters:
Depending on which dataset, the image width and height might be different, this can be changed in the kitti_yolo_predictor.launch

Change the directory of the KITTI dataset in the launch file as well.

## Running it:
```
cd ~/catkin_ws/src/autonomousCarAssignment/
roslaunch kitti_yolo_predictor.launch
```
There should be a window showing the frames and bounding boxes, while the original terminal will start printing out warning statements.

## Afterthoughts:
I wanted to use the SORT tracker to do a Kalman Filter predictor to warn the driver, however was out of time.

Why use SORT? I could just use YOLO, but due to each bounding boxes being considered as new bounding boxes every frame, the self-driving car will get flooded by messages. With SORT, it warns the car of each obstacle only once when it is within its view.

Why YOLO? Because it has state-of-the-art detection rate, and the classes I require are only Cars and People, which are already pretrained well.

## Acknowledgements
1) Kudos to pjreddie, the guy who created YOLO, https://pjreddie.com/darknet/yolo/
2) YOLO ROS from https://github.com/leggedrobotics/darknet_ros
3) YOLO ROS also from https://github.com/pgigioli/darknet_ros
3) SORT from https://github.com/abewley/sort
