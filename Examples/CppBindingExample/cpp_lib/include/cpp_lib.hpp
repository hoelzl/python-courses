#pragma once
#ifndef CPP_BINDING_EXAMPLE_HPP
#define CPP_BINDING_EXAMPLE_HPP
#include <string>

extern "C" {
int add1_with_c_interface(int arg);
}

namespace bex {

void print_cpp_binding_example_info();

class MyClass
{
private:
    std::string name;
public:
    
    explicit MyClass(std::string name) : name{std::move(name)} {}
    MyClass() : MyClass{"No Name"} {}

    std::string get_name();
    void set_name(std::string name);
};

} // namespace bex


#endif // CPP_BINDING_EXAMPLE_HPP
