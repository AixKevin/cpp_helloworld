#include "user_input.h"
#include <iostream>

double enter_double(){
    std::cout << "Enter a double value: ";
    double val;
    std::cin >> val;
    return val;
}

char enter_sign(){
    std::cout << "Enter +, -, *, or /:";
    char val;
    std::cin >> val;
    return val;
}
