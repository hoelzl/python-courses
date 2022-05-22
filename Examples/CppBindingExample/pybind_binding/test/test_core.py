import cpp_binding_example_pybind as bex

def test_add1():
    assert bex.add1(0) == 1
    assert bex.add1(1) == 2