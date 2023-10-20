cmake_minimum_required(VERSION 3.0.0)
project(convert)

find_package(PCL REQUIRED COMPONENTS common io registration)
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})



add_executable(convert convert.cpp)

target_link_libraries(convert ${PCL_LIBRARIES})