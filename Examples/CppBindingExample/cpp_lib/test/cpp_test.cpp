#include "cpp_lib.hpp"

#include "catch2/catch_test_macros.hpp"

TEST_CASE("add1_with_c_interface().")
{
    CHECK(add1_with_c_interface(0) == 1);
    CHECK(add1_with_c_interface(1) == 2);
}