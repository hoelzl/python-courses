pybind11_add_module("_core" "src/core_pybind.cpp")

target_link_libraries("_core" PUBLIC "cpp_lib")

target_compile_definitions("_core" PRIVATE VERSION_INFO=${PROJECT_VERSION})
install(TARGETS "_core" DESTINATION .)
