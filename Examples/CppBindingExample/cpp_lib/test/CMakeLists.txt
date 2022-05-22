add_executable("cpp_test")

target_sources("cpp_test" PRIVATE
    "cpp_test.cpp"
)

target_link_libraries("cpp_test"
    "Catch2WithMain"
    "cpp_lib"
)