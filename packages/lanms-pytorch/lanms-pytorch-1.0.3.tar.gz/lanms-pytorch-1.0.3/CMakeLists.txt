cmake_minimum_required(VERSION 3.1)
project(lanms)

find_package(Torch REQUIRED)
include_directories(include)
set(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/lanms)

add_library(lanms SHARED adaptor.cpp include/clipper/clipper.cpp)
target_compile_features(lanms PRIVATE cxx_std_14)
target_link_libraries(lanms "${TORCH_LIBRARIES}")