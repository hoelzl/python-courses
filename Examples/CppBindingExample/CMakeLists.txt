cmake_minimum_required (VERSION 3.18)
project("cpp_binding_example" VERSION "0.0.1")

set(CMAKE_CXX_STANDARD 14)

add_subdirectory(external)
add_subdirectory("cpp_lib")
add_subdirectory("cpp_main")
add_subdirectory("pybind_binding")
