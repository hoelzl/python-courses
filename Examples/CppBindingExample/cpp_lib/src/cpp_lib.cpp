#include "cpp_lib.hpp"

#include <iostream>

int add1_with_c_interface(int arg) { return arg + 1; }

namespace bex {

void print_cpp_binding_example_info()
{
    std::cout << "Project Info\n\n";
    std::cout << "  name:      cpp_binding_example\n";
    std::cout << "  namespace: bex\n";
}

std::string MyClass::get_name() { return name; }
void MyClass::set_name(std::string name) { this->name = std::move(name); }

} // namespace bex