cmake_minimum_required(VERSION 3.5)
project(vrpn_path_ext)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(VRPN REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

include_directories(include)

add_library(vrpn_path_ext
            src/vrpn_client_ros.cpp)
ament_target_dependencies(vrpn_path_ext rclcpp std_msgs geometry_msgs VRPN)

add_executable(vrpn_tracker_node src/vrpn_tracker_node.cpp)
target_link_libraries(vrpn_tracker_node vrpn_path_ext)
ament_target_dependencies(vrpn_tracker_node rclcpp std_msgs geometry_msgs VRPN)

add_executable(vrpn_client_node src/vrpn_client_node.cpp)
target_link_libraries(vrpn_client_node vrpn_path_ext)
ament_target_dependencies(vrpn_client_node rclcpp std_msgs geometry_msgs VRPN)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}/
)

install(TARGETS
#what/ vrpn_client_ros?
  vrpn_path_ext
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(TARGETS
  vrpn_tracker_node
  vrpn_client_node
  # path_extraction
  DESTINATION lib/${PROJECT_NAME}
)
# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  scripts/pathExtRos_new.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
