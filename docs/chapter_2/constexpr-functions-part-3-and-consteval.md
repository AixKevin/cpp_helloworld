# F.3 — Constexpr 函数（第 3 部分）和 consteval

F.3 — Constexpr 函数（第 3 部分）和 consteval
Alex
2024 年 11 月 26 日，太平洋标准时间下午 4:49
2025 年 3 月 5 日
强制 constexpr 函数在编译时求值
目前没有办法告诉编译器 constexpr 函数应该尽可能在编译时求值（例如，在 constexpr 函数的返回值用于非常量表达式的情况下）。
然而，我们可以通过确保返回值在需要常量表达式的地方使用，来强制一个有资格在编译时求值的 constexpr 函数在编译时实际求值。这需要针对每个调用进行操作。
最常见的方法是使用返回值初始化一个 constexpr 变量（这就是为什么我们在之前的例子中一直使用变量“g”）。不幸的是，这需要在我们的程序中引入一个新变量，仅仅是为了确保编译时求值，这很丑陋并降低了代码可读性。
致进阶读者
人们尝试了多种“hacky”方法来解决每次强制编译时求值时都必须引入一个新的 constexpr 变量的问题。请参阅
此处
和
此处
。
然而，在 C++20 中，有一个更好的解决方法，我们稍后将介绍。
Consteval
C++20
C++20 引入了关键字
consteval
，用于指示函数
必须
在编译时求值，否则将导致编译错误。此类函数称为
立即函数
。
#include <iostream>

consteval int greater(int x, int y) // function is now consteval
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int g { greater(5, 6) };              // ok: will evaluate at compile-time
    std::cout << g << '\n';

    std::cout << greater(5, 6) << " is greater!\n"; // ok: will evaluate at compile-time

    int x{ 5 }; // not constexpr
    std::cout << greater(x, 6) << " is greater!\n"; // error: consteval functions must evaluate at compile-time

    return 0;
}
在上面的例子中，对
greater()
的前两个调用将在编译时求值。对
greater(x, 6)
的调用无法在编译时求值，因此将导致编译错误。
最佳实践
如果您的函数出于某种原因必须在编译时求值（例如，因为它执行只有在编译时才能完成的操作），请使用
consteval
。
也许令人惊讶的是，consteval 函数的参数不是 constexpr（尽管 consteval 函数只能在编译时求值）。此决定是为了保持一致性。
确定 constexpr 函数调用是在编译时还是运行时求值
C++ 目前没有提供任何可靠的机制来做到这一点。
那么
std::is_constant_evaluated
或
if consteval
呢？
高级
这些功能都不能告诉您函数调用是在编译时还是运行时求值。
std::is_constant_evaluated()
（定义在
头文件中）返回一个
bool
值，指示当前函数是否在常量求值上下文中执行。
常量求值上下文
（也称为
常量上下文
）被定义为需要常量表达式的上下文（例如 constexpr 变量的初始化）。因此，在编译器需要编译时求值常量表达式的情况下，
std::is_constant_evaluated()
将按预期返回
true
。
这旨在允许您执行以下操作
#include <type_traits> // for std::is_constant_evaluated()

constexpr int someFunction()
{
    if (std::is_constant_evaluated()) // if evaluating in constant context
        doSomething();
    else
        doSomethingElse();
}
然而，编译器也可能选择在不需要常量表达式的上下文中在编译时求值 constexpr 函数。在这种情况下，即使函数确实在编译时求值，
std::is_constant_evaluated()
也将返回
false
。因此，
std::is_constant_evaluated()
真正的含义是“编译器被强制在编译时求值此表达式”，而不是“此表达式正在编译时求值”。
关键见解
虽然这可能看起来很奇怪，但有几个原因
正如
提出此功能的论文
所指出的，标准实际上并没有区分“编译时”和“运行时”。定义涉及这种区分的行为将是一个更大的改变。
优化不应改变程序的可见行为（除非标准明确允许）。如果
std::is_constant_evaluated()
在函数因任何原因在编译时求值时返回
true
，那么优化器决定在编译时而不是运行时求值函数可能会潜在地改变函数的可见行为。因此，您的程序可能会根据其编译的优化级别而表现出非常不同的行为！
虽然这可以通过各种方式解决，但这些都涉及增加优化器的额外复杂性或限制其优化某些情况的能力。
C++23 中引入的
if consteval
是
if (std::is_constant_evaluated())
的替代品，它提供了更简洁的语法并修复了一些其他问题。然而，它的求值方式是相同的。
使用 consteval 使 constexpr 在编译时执行
C++20
consteval 函数的缺点是它们无法在运行时求值，这使得它们不如 constexpr 函数灵活，后者可以执行两者。因此，仍然需要一种便捷的方法来强制 constexpr 函数在编译时求值（即使返回值在不需要常量表达式的地方使用），以便我们可以在可能的情况下明确强制编译时求值，并在不可能的情况下进行运行时求值。
这是一个展示如何实现这一点的示例
#include <iostream>

#define CONSTEVAL(...) [] consteval { return __VA_ARGS__; }()               // C++20 version per Jan Scultke (https://stackoverflow.com/a/77107431/460250)
#define CONSTEVAL11(...) [] { constexpr auto _ = __VA_ARGS__; return _; }() // C++11 version per Justin (https://stackoverflow.com/a/63637573/460250)

// This function returns the greater of the two numbers if executing in a constant context
// and the lesser of the two numbers otherwise
constexpr int compare(int x, int y) // function is constexpr
{
    if (std::is_constant_evaluated())
        return (x > y ? x : y);
    else
        return (x < y ? x : y);
}

int main()
{
    int x { 5 };
    std::cout << compare(x, 6) << '\n';                  // will execute at runtime and return 5

    std::cout << compare(5, 6) << '\n';                  // may or may not execute at compile-time, but will always return 5
    std::cout << CONSTEVAL(compare(5, 6)) << '\n';       // will always execute at compile-time and return 6
    

    return 0;
}
致进阶读者
这使用了一个可变参数预处理器宏（#define、
...
和
__VA_ARGS__
）来定义一个立即调用的 consteval lambda（通过尾随括号）。
您可以在
https://cppreference.cn/w/cpp/preprocessor/replace
找到有关可变参数宏的信息。
我们在第
20.6 课 -- Lambda 表达式（匿名函数）简介
中介绍 lambda 表达式。
以下方法也应该有效（并且更简洁，因为它不使用预处理器宏）
对于 gcc 用户
GCC 14 及更高版本存在一个错误，当启用任何级别的优化时，会导致以下示例产生错误的结果。
#include <iostream>

// Uses abbreviated function template (C++20) and `auto` return type to make this function work with any type of value
// See 'related content' box below for more info (you don't need to know how these work to use this function)
// We've opted to use an uppercase name here for consistency with the prior example, but it also makes it easier to see the call
consteval auto CONSTEVAL(auto value)
{
    return value;
}

// This function returns the greater of the two numbers if executing in a constant context
// and the lesser of the two numbers otherwise
constexpr int compare(int x, int y) // function is constexpr
{
    if (std::is_constant_evaluated())
        return (x > y ? x : y);
    else
        return (x < y ? x : y);
}

int main()
{
    std::cout << CONSTEVAL(compare(5, 6)) << '\n';       // will execute at compile-time

    return 0;
}
因为 consteval 函数的参数总是明显地进行常量求值，所以如果我们将 constexpr 函数作为 consteval 函数的参数调用，那么该 constexpr 函数必须在编译时求值！然后 consteval 函数将 constexpr 函数的结果作为其自己的返回值返回，以便调用者可以使用它。
请注意，consteval 函数按值返回。虽然这在运行时可能效率低下（如果该值是某种复制成本高昂的类型，例如
std::string
），但在编译时上下文中，这无关紧要，因为对 consteval 函数的整个调用将简单地替换为计算出的返回值。
致进阶读者
我们在第
10.9 课 -- 函数类型推导
中介绍自动返回类型。
我们在第 11.8 课 -- 带有多个模板类型的函数模板
11.8 课 -- 带有多个模板类型的函数模板
中介绍缩写函数模板（自动参数）。
下一课
F.4
Constexpr 函数（第 4 部分）
返回目录
上一课
F.2
Constexpr 函数（第 2 部分）