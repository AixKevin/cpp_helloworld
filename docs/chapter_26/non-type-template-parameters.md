# 11.9 — 非类型模板参数

11.9 — 非类型模板参数
Alex
2023年4月21日，下午4:12 PDT
2024年10月20日
在之前的课程中，我们讨论了如何创建使用类型模板参数的函数模板。类型模板参数充当实际类型（作为模板实参传入）的占位符。
虽然类型模板参数是迄今为止最常用的模板参数类型，但还有另一种值得了解的模板参数：非类型模板参数。
非类型模板参数
非类型模板参数
是一种具有固定类型，充当作为模板实参传入的 `constexpr` 值的占位符的模板参数。
非类型模板参数可以是以下任何类型：
整型
枚举类型
std::nullptr_t
浮点类型（C++20 起）
指向对象的指针或引用
指向函数的指针或引用
指向成员函数的指针或引用
字面量类类型（C++20 起）
我们在课程
O.1 -- 通过 std::bitset 进行位标志和位操作
中讨论 `std::bitset` 时，看到了第一个非类型模板参数的例子。
#include <bitset>

int main()
{
    std::bitset<8> bits{ 0b0000'0101 }; // The <8> is a non-type template parameter

    return 0;
}
在 `std::bitset` 的例子中，非类型模板参数用于告诉 `std::bitset` 我们希望它存储多少位。
定义我们自己的非类型模板参数
这是一个使用 `int` 非类型模板参数的简单函数示例：
#include <iostream>

template <int N> // declare a non-type template parameter of type int named N
void print()
{
    std::cout << N << '\n'; // use value of N here
}

int main()
{
    print<5>(); // 5 is our non-type template argument

    return 0;
}
此示例输出：
5
在第3行，我们有模板参数声明。在尖括号内，我们定义了一个名为 `N` 的非类型模板参数，它将作为 `int` 类型值的占位符。在 `print()` 函数内部，我们使用了 `N` 的值。
在第11行，我们调用了 `print()` 函数，它使用 `int` 值 `5` 作为非类型模板实参。当编译器看到此调用时，它将实例化一个类似于此的函数：
template <>
void print<5>()
{
    std::cout << 5 << '\n';
}
在运行时，当 `main()` 调用此函数时，它会打印 `5`。
然后程序结束。很简单，对吧？
就像 `T` 通常用作第一个类型模板参数的名称一样，`N` 通常用作 `int` 非类型模板参数的名称。
最佳实践
将 `N` 用作 `int` 非类型模板参数的名称。
非类型模板参数有什么用？
截至 C++20，函数参数不能是 `constexpr`。这对于普通函数、`constexpr` 函数（这很有意义，因为它们必须能够在运行时运行）都是如此，甚至令人惊讶的是，`consteval` 函数也是如此。
假设我们有这样一个函数：
#include <cassert>
#include <cmath> // for std::sqrt
#include <iostream>

double getSqrt(double d)
{
    assert(d >= 0.0 && "getSqrt(): d must be non-negative");

    // The assert above will probably be compiled out in non-debug builds
    if (d >= 0)
        return std::sqrt(d);

    return 0.0;
}

int main()
{
    std::cout << getSqrt(5.0) << '\n';
    std::cout << getSqrt(-5.0) << '\n';

    return 0;
}
运行时，调用 `getSqrt(-5.0)` 将导致运行时断言。虽然这总比没有好，但由于 `-5.0` 是一个字面量（并且隐式 `constexpr`），如果我们可以使用 `static_assert`，以便在编译时捕获此类错误，那会更好。然而，`static_assert` 需要一个常量表达式，而函数参数不能是 `constexpr`……
然而，如果我们将函数参数改为非类型模板参数，那么我们就可以实现我们想要的功能：
#include <cmath> // for std::sqrt
#include <iostream>

template <double D> // requires C++20 for floating point non-type parameters
double getSqrt()
{
    static_assert(D >= 0.0, "getSqrt(): D must be non-negative");

    if constexpr (D >= 0) // ignore the constexpr here for this example
        return std::sqrt(D); // strangely, std::sqrt isn't a constexpr function (until C++26)

    return 0.0;
}

int main()
{
    std::cout << getSqrt<5.0>() << '\n';
    std::cout << getSqrt<-5.0>() << '\n';

    return 0;
}
此版本编译失败。当编译器遇到 `getSqrt<-5.0>()` 时，它将实例化并调用一个类似于此的函数：
template <>
double getSqrt<-5.0>()
{
    static_assert(-5.0 >= 0.0, "getSqrt(): D must be non-negative");

    if constexpr (-5.0 >= 0) // ignore the constexpr here for this example
        return std::sqrt(-5.0);

    return 0.0;
}
`static_assert` 条件为假，因此编译器断言退出。
关键见解
非类型模板参数主要用于我们需要将 `constexpr` 值传递给函数（或类类型），以便它们可以在需要常量表达式的上下文中使用。
类类型 `std::bitset` 使用非类型模板参数来定义要存储的位数，因为位数必须是 `constexpr` 值。
作者注
不得不使用非类型模板参数来规避函数参数不能是 `constexpr` 的限制并不理想。目前有相当多的不同提案正在评估中，以帮助解决此类情况。我预计我们可能会在未来的 C++ 语言标准中看到更好的解决方案。
非类型模板实参的隐式转换
可选
某些非类型模板实参可以隐式转换，以匹配不同类型的非类型模板参数。例如：
#include <iostream>

template <int N> // int non-type template parameter
void print()
{
    std::cout << N << '\n';
}

int main()
{
    print<5>();   // no conversion necessary
    print<'c'>(); // 'c' converted to type int, prints 99

    return 0;
}
这会打印
5
99
在上面的例子中，`'c'` 被转换为 `int` 以匹配函数模板 `print()` 的非类型模板参数，然后以 `int` 的形式打印值。
在此上下文中，只允许某些类型的 `constexpr` 转换。最常见的允许转换类型包括：
整型提升（例如 `char` 到 `int`）
整型转换（例如 `char` 到 `long` 或 `int` 到 `char`）
用户定义转换（例如某个程序定义的类到 `int`）
左值到右值转换（例如某个变量 `x` 到 `x` 的值）
请注意，此列表比列表初始化允许的隐式转换类型限制更严格。例如，您可以使用 `constexpr int` 列表初始化 `double` 类型的变量，但 `constexpr int` 非类型模板实参不会转换为 `double` 非类型模板参数。
允许转换的完整列表可以在
此处
的“转换常量表达式”小节中找到。
与普通函数不同，匹配函数模板调用到函数模板定义的算法并不复杂，某些匹配不会根据所需的转换类型（或缺乏转换）优先于其他匹配。这意味着，如果为不同种类的非类型模板参数重载了函数模板，则很容易导致歧义匹配：
#include <iostream>

template <int N> // int non-type template parameter
void print()
{
    std::cout << N << '\n';
}

template <char N> // char non-type template parameter
void print()
{
    std::cout << N << '\n';
}

int main()
{
    print<5>();   // ambiguous match with int N = 5 and char N = 5
    print<'c'>(); // ambiguous match with int N = 99 and char N = 'c'

    return 0;
}
或许令人惊讶的是，`print()` 的这两个调用都导致了歧义匹配。
使用 `auto` 进行非类型模板参数的类型推导
C++17
从 C++17 开始，非类型模板参数可以使用 `auto` 让编译器从模板实参中推导非类型模板参数：
#include <iostream>

template <auto N> // deduce non-type template parameter from template argument
void print()
{
    std::cout << N << '\n';
}

int main()
{
    print<5>();   // N deduced as int `5`
    print<'c'>(); // N deduced as char `c`

    return 0;
}
这可以编译并产生预期的结果：
5
c
致进阶读者
您可能想知道为什么这个例子不会像前一节的例子那样产生歧义匹配。编译器首先查找歧义匹配，如果不存在歧义匹配，则实例化函数模板。在这种情况下，只有一个函数模板，因此不可能存在歧义。
实例化上述示例的函数模板后，程序看起来像这样：
#include <iostream>

template <auto N>
void print()
{
    std::cout << N << '\n';
}

template <>
void print<5>() // note that this is print<5> and not print<int>
{
    std::cout << 5 << '\n';
}

template <>
void print<'c'>() // note that this is print<`c`> and not print<char>
{
    std::cout << 'c' << '\n';
}

int main()
{
    print<5>();   // calls print<5>
    print<'c'>(); // calls print<'c'>

    return 0;
}
小测验时间
问题 #1
编写一个 `constexpr` 函数模板，它带有一个非类型模板参数，并返回模板实参的阶乘。当程序到达 `factorial<-3>()` 时，应编译失败。
// define your factorial() function template here

int main()
{
    static_assert(factorial<0>() == 1);
    static_assert(factorial<3>() == 6);
    static_assert(factorial<5>() == 120);

    factorial<-3>(); // should fail to compile

    return 0;
}
显示答案
template <int N>
constexpr int factorial()
{
    static_assert(N >= 0);

    int product { 1 };
    for (int i { 2 }; i <= N; ++i)
        product *= i;

    return product;
}

int main()
{
    static_assert(factorial<0>() == 1);
    static_assert(factorial<3>() == 6);
    static_assert(factorial<5>() == 120);

    factorial<-3>(); // should fail to compile

    return 0;
}
下一课
11.10
在多个文件中使用函数模板
返回目录
上一课
11.8
具有多个模板类型的函数模板