#include "cpp_lib.hpp"
#include "pybind11/pybind11.h"

namespace py = pybind11;

// ReSharper disable once CppParameterMayBeConstPtrOrRef
PYBIND11_MODULE(_core, m)
{
    m.doc() = "C++ binding example using pybind11.";

    m.def(
        "add1", &add1_with_c_interface, "Add 1 using a C interface.", py::arg("i") = 1);

    m.def(
        "print_info", &bex::print_cpp_binding_example_info,
        "Print information about the project.");

    const auto my_class
        = py::class_<bex::MyClass>(m, "MyClass")
              .def(py::init<std::string>())
              .def(py::init<>())
              .def("get_name", &bex::MyClass::get_name)
              .def("set_name", &bex::MyClass::set_name, py::arg("name"))
              .def_property("name", &bex::MyClass::get_name, &bex::MyClass::set_name);

    my_class.doc() = "MyClass: A C++ class bound with pybind11.";
}
