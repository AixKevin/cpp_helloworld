# F.1 — Constexpr 函数

F.1 — Constexpr 函数
Alex
2022 年 3 月 28 日，太平洋夏令时上午 9:12
2025 年 2 月 18 日
在课程
5.6 -- Constexpr 变量
中，我们介绍了
constexpr
关键字，我们用它来创建编译时（符号）常量。我们还介绍了常量表达式，即可以在编译时而不是运行时求值的表达式。
常量表达式的一个挑战是，在常量表达式中不允许调用普通函数。这意味着我们不能在需要常量表达式的任何地方使用此类函数调用。
考虑以下程序
#include <iostream>

int main()
{
    constexpr double radius { 3.0 };
    constexpr double pi { 3.14159265359 };
    constexpr double circumference { 2.0 * radius * pi };
    
    std::cout << "Our circle has circumference " << circumference << "\n";

    return 0;    
}
这会产生结果
Our circle has circumference 18.8496
为
circumference
提供复杂的初始化式并不好（并且需要我们实例化两个支持变量，
radius
和
pi
）。所以我们把它变成一个函数。
#include <iostream>

double calcCircumference(double radius)
{
    constexpr double pi { 3.14159265359 };
    return 2.0 * pi * radius;
}

int main()
{
    constexpr double circumference { calcCircumference(3.0) }; // compile error
    
    std::cout << "Our circle has circumference " << circumference << "\n";

    return 0;    
}
这段代码更简洁。它也无法编译。Constexpr 变量
circumference
要求其初始化式是一个常量表达式，而调用
calcCircumference()
不是一个常量表达式。
在这个特定的例子中，我们可以将
circumference
设置为非 constexpr，程序就能编译。虽然我们会失去常量表达式的好处，但至少程序会运行。
然而，在 C++ 中还有其他情况（我们将来会介绍），我们没有可用的替代选项，只有常量表达式才能奏效。在这些情况下，我们确实希望能够使用函数，但对普通函数的调用就是不起作用。那么我们该怎么办呢？
Constexpr 函数可以在常量表达式中使用
constexpr 函数
是允许在常量表达式中调用的函数。
要将函数设为 constexpr 函数，我们只需在函数返回类型前使用
constexpr
关键字。
关键见解
constexpr
关键字用于向编译器和其他开发人员表明函数可以在常量表达式中使用。
以下是与上面相同的示例，但使用了 constexpr 函数
#include <iostream>

constexpr double calcCircumference(double radius) // now a constexpr function
{
    constexpr double pi { 3.14159265359 };
    return 2.0 * pi * radius;
}

int main()
{
    constexpr double circumference { calcCircumference(3.0) }; // now compiles
    
    std::cout << "Our circle has circumference " << circumference << "\n";

    return 0;    
}
因为
calcCircumference()
现在是一个 constexpr 函数，所以它可以在常量表达式中使用，例如
circumference
的初始化式。
Constexpr 函数可以在编译时求值
在课程
5.5 -- 常量表达式
中，我们注意到在需要常量表达式的上下文中（例如 constexpr 变量的初始化），要求常量表达式在编译时求值。如果所需的常量表达式包含 constexpr 函数调用，则该 constexpr 函数调用必须在编译时求值。
在我们的示例中，变量
circumference
是 constexpr 类型，因此需要一个常量表达式初始化式。由于
calcCircumference()
是这个必需常量表达式的一部分，所以
calcCircumference()
必须在编译时求值。
当函数调用在编译时求值时，编译器将在编译时计算函数调用的返回值，然后用返回值替换函数调用。
因此，在我们的示例中，对
calcCircumference(3.0)
的调用被函数调用的结果替换，即
18.8496
。换句话说，编译器将编译这个
#include <iostream>

constexpr double calcCircumference(double radius)
{
    constexpr double pi { 3.14159265359 };
    return 2.0 * pi * radius;
}

int main()
{
    constexpr double circumference { 18.8496 };
    
    std::cout << "Our circle has circumference " << circumference << "\n";

    return 0;    
}
要在编译时求值，还需要满足另外两个条件
对 constexpr 函数的调用必须具有在编译时已知（例如是常量表达式）的参数。
constexpr 函数中的所有语句和表达式都必须在编译时可求值。
当 constexpr（或 consteval）函数在编译时进行求值时，它调用的任何其他函数都要求在编译时求值（否则初始函数将无法在编译时返回结果）。
致进阶读者
还有一些其他较少遇到的标准。这些可以在
这里
找到。
Constexpr 函数也可以在运行时求值
Constexpr 函数也可以在运行时求值，在这种情况下它们将返回一个非 constexpr 结果。例如
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    int x{ 5 }; // not constexpr
    int y{ 6 }; // not constexpr

    std::cout << greater(x, y) << " is greater!\n"; // will be evaluated at runtime

    return 0;
}
在此示例中，由于参数
x
和
y
不是常量表达式，因此函数无法在编译时解析。但是，该函数仍将在运行时解析，将预期值作为非 constexpr
int
返回。
关键见解
当 constexpr 函数在运行时求值时，它的求值方式与普通（非 constexpr）函数相同。换句话说，在这种情况下
constexpr
没有作用。
关键见解
允许具有 constexpr 返回类型的函数在编译时或运行时求值，是为了让单个函数能够同时服务于这两种情况。
否则，你需要有单独的函数（一个具有 constexpr 返回类型的函数，以及一个具有非 constexpr 返回类型的函数）。这不仅需要重复代码，而且这两个函数还需要具有不同的名称！
再提醒我一次，我们为什么关心函数在编译时执行？
现在是回顾编译时编程技术所能带来的好处的好时机：
5.5 -- 常量表达式
。
下一课
F.2
Constexpr 函数（第二部分）
返回目录
上一课
11.x
第 11 章总结和测验