#include "user_input.h"
#include <iostream>

int main()
{
    double x{enter_double()};
    double y{enter_double()};
    char s{enter_sign()};

    double result{};

    if (s == '+')
        result = x + y;
    else if (s == '-')
        result = x - y;
    else if (s == '*')
        result = x * y;
    else if (s == '/')
        result = x / y;
    else
        result = 0;

    std::cout << x << " " << s << " " << y << " is " << result << '\n';
    return 0;
}
