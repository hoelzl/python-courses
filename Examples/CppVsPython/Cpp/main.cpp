#include "calculator.hpp"
#include <iostream>


int main()
{
    std::cout << "Please enter two numbers: " << std::endl;
    double x, y;
    std::cin >> x >> y;
    std::cout << "The sum of " << x << " and " << y << " is " << add(x, y) << std::endl;
    return 0;
}
