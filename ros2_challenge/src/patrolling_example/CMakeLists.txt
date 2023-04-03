cmake_minimum_required(VERSION 3.5)
project(patrolling_example)

set(CMAKE_BUILD_TYPE Debug)

set(CMAKE_CONFIG_PATH ${CMAKE_MODULE_PATH}  "${CMAKE_CURRENT_LIST_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CONFIG_PATH}")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(behaviortree_cpp_v3 REQUIRED)
find_package(action_msgs REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(ament_index_cpp REQUIRED)

find_package(ZMQ)
if(ZMQ_FOUND)
    message(STATUS "ZeroMQ found.")
    add_definitions(-DZMQ_FOUND)
else()
  message(WARNING "ZeroMQ NOT found. Not including PublisherZMQ.")
endif()

set(CMAKE_CXX_STANDARD 17)

set(dependencies
  rclcpp
  rclcpp_lifecycle
  rclcpp_action
  behaviortree_cpp_v3
  action_msgs
  lifecycle_msgs
  geometry_msgs
  nav2_msgs
  ament_index_cpp
  sensor_msgs
  std_msgs
)

include_directories(include ${ZMQ_INCLUDE_DIRS})

add_library(recharge_bt_node SHARED src/patrolling_example/Recharge.cpp)
add_library(location_bt_node SHARED src/patrolling_example/Location.cpp)
add_library(move_bt_node SHARED src/patrolling_example/Move.cpp)
add_library(get_waypoint_bt_node SHARED src/patrolling_example/GetWaypoint.cpp)
add_library(battery_checker_bt_node SHARED src/patrolling_example/BatteryChecker.cpp)
list(APPEND plugin_libs
  recharge_bt_node
  location_bt_node
  move_bt_node
  get_waypoint_bt_node
  battery_checker_bt_node
)

foreach(bt_plugin ${plugin_libs})
  ament_target_dependencies(${bt_plugin} ${dependencies})
  target_compile_definitions(${bt_plugin} PRIVATE BT_PLUGIN_EXPORT)
endforeach()

add_executable(patrolling_example src/patrolling_example_main.cpp)
ament_target_dependencies(patrolling_example ${dependencies})
target_link_libraries(patrolling_example ${ZMQ_LIBRARIES})

install(TARGETS
  ${plugin_libs}
  patrolling_example
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/
)

install(DIRECTORY launch param map behavior_tree_xml
  DESTINATION share/${PROJECT_NAME}
)

ament_export_include_directories(include)
ament_export_dependencies(${dependencies})

ament_package()
