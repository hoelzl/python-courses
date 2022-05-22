add_executable (cpp_main)

target_sources(cpp_main PRIVATE
    "src/main.cpp")

target_link_libraries(cpp_main 
    "GSL"
    "cpp_lib")
