# 10.8 — 使用 auto 关键字的对象类型推导

10.8 — 使用 auto 关键字的对象类型推导
Alex
2015 年 7 月 30 日，下午 1:02 PDT
2024 年 9 月 25 日
在这个简单的变量定义中隐藏着一个细微的冗余
double d{ 5.0 };
在 C++ 中，我们要求为所有对象提供显式类型。因此，我们指定变量
d
的类型为 double。
然而，用于初始化
d
的字面值
5.0
也具有 double 类型（通过字面值的格式隐式确定）。
相关内容
我们在课程
5.2 -- 字面值
中讨论字面值类型是如何确定的。
在变量及其初始化器需要具有相同类型的情况下，我们实际上提供了两次相同的类型信息。
已初始化变量的类型推导
类型推导
（有时也称为
类型推断
）是一种特性，允许编译器根据对象的初始化器推导出对象的类型。在定义变量时，可以通过使用
auto
关键字代替变量类型来调用类型推导
int main()
{
    auto d { 5.0 }; // 5.0 is a double literal, so d will be deduced as a double
    auto i { 1 + 2 }; // 1 + 2 evaluates to an int, so i will be deduced as an int
    auto x { i }; // i is an int, so x will be deduced as an int

    return 0;
}
在第一个例子中，因为
5.0
是一个 double 字面值，编译器将推导出变量
d
的类型应该是
double
。在第二个例子中，表达式
1 + 2
产生一个 int 结果，所以变量
i
的类型将是
int
。在第三个例子中，
i
之前被推导出为
int
类型，所以
x
也将被推导出为
int
类型。
警告
在 C++17 之前，
auto d{ 5.0 };
会将
d
推导出为
std::initializer_list<double>
而不是
double
。这在 C++17 中得到了修复，许多编译器（如 gcc 和 Clang）已将此更改反向移植到以前的语言标准。
如果您使用的是 C++14 或更早版本，并且上面的示例在您的编译器上无法编译，请改用带
auto
的复制初始化 (
auto d = 5.0
)。
因为函数调用是有效的表达式，所以当我们的初始化器是一个非 void 函数调用时，我们甚至可以使用类型推导
int add(int x, int y)
{
    return x + y;
}

int main()
{
    auto sum { add(5, 6) }; // add() returns an int, so sum's type will be deduced as an int

    return 0;
}
add()
函数返回一个
int
值，因此编译器将推导出变量
sum
的类型应该是
int
。
字面值后缀可以与类型推导结合使用以指定特定类型
int main()
{
    auto a { 1.23f }; // f suffix causes a to be deduced to float
    auto b { 5u };    // u suffix causes b to be deduced to unsigned int

    return 0;
}
使用类型推导的变量也可以使用其他说明符/限定符，例如
const
或
constexpr
int main()
{
    int a { 5 };            // a is an int

    const auto b { 5 };     // b is a const int
    constexpr auto c { 5 }; // c is a constexpr int

    return 0;
}
类型推导必须有可供推导的东西
类型推导不适用于没有初始化器或初始化器为空的对象。它也不适用于初始化器类型为
void
（或任何其他不完整类型）的情况。因此，以下代码无效
#include <iostream>

void foo()
{
}

int main()
{
    auto a;           // The compiler is unable to deduce the type of a
    auto b { };       // The compiler is unable to deduce the type of b
    auto c { foo() }; // Invalid: c can't have type incomplete type void
    
    return 0;
}
虽然对基本数据类型使用类型推导只能节省少量（如果有的话）击键次数，但在未来的课程中，我们将看到类型变得复杂而冗长（在某些情况下，可能难以理解）的示例。在这些情况下，使用
auto
可以节省大量输入（和拼写错误）。
相关内容
指针和引用的类型推导规则稍微复杂一些。我们将在
12.14 -- 指针、引用和 const 的类型推导
中讨论这些。
类型推导会从推导类型中去除
const
在大多数情况下，类型推导会从推导类型中去除
const
。例如
int main()
{
    const int a { 5 }; // a has type const int
    auto b { a };      // b has type int (const dropped)

    return 0;
}
在上面的例子中，
a
的类型是
const int
，但是当使用
a
作为初始化器为变量
b
推导类型时，类型推导将类型推导为
int
，而不是
const int
。
如果您希望推导类型为 const，则必须在定义中自行提供
const
int main()
{
    const int a { 5 };  // a has type const int
    const auto b { a }; // b has type const int (const dropped but reapplied)


    return 0;
}
在这个例子中，从
a
推导出的类型将是
int
（
const
被去除），但是由于我们在变量
b
的定义过程中重新添加了一个
const
限定符，所以变量
b
将具有
const int
类型。
字符串字面量的类型推导
由于历史原因，C++ 中的字符串字面量具有一种奇怪的类型。因此，以下代码可能不会按预期工作
auto s { "Hello, world" }; // s will be type const char*, not std::string
如果您希望从字符串字面量推导出的类型是
std::string
或
std::string_view
，您需要使用
s
或
sv
字面量后缀（在课程
5.7 -- std::string 简介
和
5.8 -- std::string_view 简介
中介绍）
#include <string>
#include <string_view>

int main()
{
    using namespace std::literals; // easiest way to access the s and sv suffixes

    auto s1 { "goo"s };  // "goo"s is a std::string literal, so s1 will be deduced as a std::string
    auto s2 { "moo"sv }; // "moo"sv is a std::string_view literal, so s2 will be deduced as a std::string_view

    return 0;
}
但在这种情况下，最好不要使用类型推导。
类型推导和 constexpr
因为
constexpr
不属于类型系统，所以它不能作为类型推导的一部分被推导出来。然而，一个
constexpr
变量是隐式 const 的，并且这个 const 会在类型推导期间被去除（如果需要可以重新添加）
int main()
{
    constexpr double a { 3.4 };  // a has type const double (constexpr not part of type, const is implicit)

    auto b { a };                // b has type double (const dropped)
    const auto c { a };          // c has type const double (const dropped but reapplied)
    constexpr auto d { a };      // d has type const double (const dropped but implicitly reapplied by constexpr)

    return 0;
}
类型推导的优点和缺点
类型推导不仅方便，而且还有许多其他优点。
首先，如果两个或更多变量定义在连续的行上，变量名将对齐，有助于提高可读性
// harder to read
int a { 5 };
double b { 6.7 };

// easier to read
auto c { 5 };
auto d { 6.7 };
其次，类型推导只适用于有初始化器的变量，所以如果你习惯使用类型推导，它可以帮助避免无意中未初始化的变量
int x; // oops, we forgot to initialize x, but the compiler may not complain
auto y; // the compiler will error out because it can't deduce a type for y
第三，您保证不会发生意外的性能影响转换
std::string_view getString();   // some function that returns a std::string_view

std::string s1 { getString() }; // bad: expensive conversion from std::string_view to std::string (assuming you didn't want this)
auto s2 { getString() };        // good: no conversion required
类型推导也有一些缺点。
首先，类型推导模糊了代码中对象的类型信息。尽管一个好的 IDE 应该能够显示推导出的类型（例如，当鼠标悬停在变量上时），但使用类型推导时仍然更容易出现基于类型的错误。
例如
auto y { 5 }; // oops, we wanted a double here but we accidentally provided an int literal
在上面的代码中，如果我们明确将
y
指定为 double 类型，即使我们不小心提供了一个 int 字面量初始化器，
y
也会是一个 double。使用类型推导，
y
将被推导为 int 类型。
这是另一个例子
#include <iostream>

int main()
{
     auto x { 3 };
     auto y { 2 };

     std::cout << x / y << '\n'; // oops, we wanted floating point division here

     return 0;
}
在这个例子中，我们得到的是整数除法而不是浮点数除法，这就不太清楚了。
当变量是
unsigned
时，也会出现类似的情况。由于我们不希望混合有符号和无符号值，因此明确知道变量具有无符号类型通常不应该被模糊化。
其次，如果初始化器的类型改变，使用类型推导的变量的类型也会改变，这可能是意外的。考虑一下
auto sum { add(5, 6) + gravity };
如果
add
的返回类型从 int 变为 double，或者
gravity
从 int 变为 double，则
sum
的类型也会从 int 变为 double。
总的来说，现代共识是，类型推导对于对象来说通常是安全的使用方式，并且这样做可以通过弱化类型信息来帮助您的代码更具可读性，从而使您的代码逻辑更加突出。
最佳实践
当对象的类型无关紧要时，为您的变量使用类型推导。
当您需要一个与初始化器类型不同的特定类型时，或者当您的对象在使类型明确有用的上下文中使用时，请优先使用显式类型。
作者注
在未来的课程中，当我们觉得显示类型信息有助于理解概念或示例时，我们将继续使用显式类型而不是类型推导。
下一课
10.9
函数类型推导
返回目录
上一课
10.7
类型定义和类型别名