cmake_minimum_required(VERSION 2.8.3)
project(kitti_loader)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  cv_bridge
  sensor_msgs
)

# add_service_files(
#   FILES
# )

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

# add_dependencies(md_vision ${catkin_EXPORTED_TARGETS})
# target_link_libraries(kitti_loader ${catkin_LIBRARIES} )
