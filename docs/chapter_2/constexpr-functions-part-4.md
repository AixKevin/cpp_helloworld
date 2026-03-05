# F.4 — Constexpr 函数（第 4 部分）

F.4 — Constexpr 函数（第 4 部分）
Alex
2024 年 11 月 26 日，太平洋标准时间下午 4:49
2025 年 3 月 17 日
Constexpr/consteval 函数可以使用非 const 局部变量
在 constexpr 或 consteval 函数内部，我们可以使用非 constexpr 的局部变量，并且这些变量的值可以被改变。
举个简单的例子：
#include <iostream>

consteval int doSomething(int x, int y) // function is consteval
{
    x = x + 2;       // we can modify the value of non-const function parameters

    int z { x + y }; // we can instantiate non-const local variables
    if (x > y)
        z = z - 1;   // and then modify their values

    return z;
}

int main()
{
    constexpr int g { doSomething(5, 6) };
    std::cout << g << '\n';

    return 0;
}
当这些函数在编译时求值时，编译器将本质上“执行”该函数并返回计算出的值。
Constexpr/consteval 函数可以使用函数参数和局部变量作为 constexpr 函数调用的参数
上面我们提到，“当 constexpr（或 consteval）函数在编译时求值时，它调用的任何其他函数都需要在编译时求值。”
也许令人惊讶的是，constexpr 或 consteval 函数可以将其函数参数（它们不是 constexpr）甚至局部变量（它们可能根本不是 const）用作 constexpr 函数调用的参数。当 constexpr 或 consteval 函数在编译时求值时，所有函数参数和局部变量的值都必须为编译器所知（否则它无法在编译时求值）。因此，在这种特定情况下，C++ 允许这些值用作对 constexpr 函数的调用的参数，并且该 constexpr 函数调用仍然可以在编译时求值。
#include <iostream>

constexpr int goo(int c) // goo() is now constexpr
{
    return c;
}

constexpr int foo(int b) // b is not a constant expression within foo()
{
    return goo(b);       // if foo() is resolved at compile-time, then `goo(b)` can also be resolved at compile-time
}

int main()
{
    std::cout << foo(5);
    
    return 0;
}
在上面的示例中，`foo(5)` 可能会在编译时求值，也可能不会。如果它在编译时求值，那么编译器知道 `b` 是 `5`。即使 `b` 不是 constexpr，编译器也可以将对 `goo(b)` 的调用视为 `goo(5)` 并在编译时求值该函数调用。如果 `foo(5)` 转而在运行时求值，那么 `goo(b)` 也将在运行时求值。
constexpr 函数可以调用非 constexpr 函数吗？
答案是肯定的，但仅当 constexpr 函数在非常量上下文中求值时。当 constexpr 函数在常量上下文中求值时，不能调用非 constexpr 函数（因为那样 constexpr 函数将无法生成编译时常量值），否则会产生编译错误。
允许调用非 constexpr 函数，以便 constexpr 函数可以执行以下操作：
#include <type_traits> // for std::is_constant_evaluated

constexpr int someFunction()
{
    if (std::is_constant_evaluated()) // if evaluating in constant context
        return someConstexprFcn();
    else
        return someNonConstexprFcn();
}
现在考虑这个变体
constexpr int someFunction(bool b)
{
    if (b)
        return someConstexprFcn();
    else
        return someNonConstexprFcn();
}
只要 `someFunction(false)` 从未在常量表达式中调用，这是合法的。
题外话…
在 C++23 之前，C++ 标准规定 constexpr 函数必须至少为一组参数返回一个 constexpr 值，否则在技术上是格式错误的。在 constexpr 函数中无条件调用非 constexpr 函数会使 constexpr 函数格式错误。但是，编译器不需要为此类情况生成错误或警告——因此，除非您尝试在常量上下文中调用此类 constexpr 函数，否则编译器可能不会抱怨。在 C++23 中，此要求已被取消。
为了获得最佳结果，我们建议如下：
尽可能避免从 constexpr 函数内部调用非 constexpr 函数。
如果您的 constexpr 函数在常量和非常量上下文之间需要不同的行为，请使用 `if (std::is_constant_evaluated())`（在 C++20 中）或 `if consteval`（C++23 及更高版本）来条件化行为。
始终在常量上下文中测试您的 constexpr 函数，因为它们在非常量上下文中调用时可能有效，但在常量上下文中失败。
我应该何时将函数声明为 constexpr？
通常，如果一个函数可以作为所需常量表达式的一部分进行求值，则应将其声明为 `constexpr`。
一个**纯函数**是满足以下条件的函数：
给定相同的参数，函数总是返回相同的返回值
函数没有副作用（例如，它不改变静态局部变量或全局变量的值，不进行输入或输出等）。
纯函数通常应声明为 constexpr。
题外话…
Constexpr 函数不总是需要是纯函数。在 C++23 中，constexpr 函数可以使用和修改静态局部变量。由于静态局部变量的值在函数调用之间持久存在，因此修改静态局部变量被视为副作用。
也就是说，如果你的程序是微不足道的或一次性的，并且你没有 constexpr 一个函数，世界也不会因此而终结。希望如此。
最佳实践
除非你有特定理由不这样做，否则可以作为常量表达式一部分求值的函数应声明为 `constexpr`（即使目前没有以这种方式使用它）。
不能作为所需常量表达式的一部分进行求值的函数不应标记为 `constexpr`。
为什么不将每个函数都声明为 constexpr？
有几个原因你可能不想将函数声明为 `constexpr`：
`constexpr` 表示一个函数可以在常量表达式中使用。如果你的函数不能作为常量表达式的一部分求值，则不应将其标记为 `constexpr`。
`constexpr` 是函数接口的一部分。一旦函数被设为 constexpr，它就可以被其他 constexpr 函数调用，或在需要常量表达式的上下文中使用。之后移除 `constexpr` 将会破坏此类代码。
`constexpr` 函数可能更难调试，因为你无法在调试器中设置断点或单步执行它们。
为什么在函数实际上没有在编译时求值时将其声明为 constexpr？
新程序员有时会问，“当函数在我的程序中只在运行时求值时（例如，因为函数调用中的参数不是 const），我为什么要将它声明为 constexpr？”
有几个原因：
使用 constexpr 的弊端很少，它可能有助于编译器优化您的程序，使其更小、更快。
仅仅因为您现在没有在编译时可求值的上下文中调用该函数，并不意味着您在修改或扩展程序时不会在这样的上下文中调用它。如果您还没有将函数声明为 constexpr，那么当您开始在这样的上下文中调用它时，您可能不会想到这样做，然后您就会错过性能优势。或者您可能被迫稍后将其声明为 constexpr，当您需要在某个需要常量表达式的上下文中使用返回值时。
重复有助于巩固最佳实践。
在一个非平凡的项目中，以函数将来可能被重用（或扩展）的心态来实现函数是一个好主意。任何时候修改现有函数，你都有可能破坏它，这意味着它需要重新测试，这会花费时间和精力。通常值得多花一两分钟“第一次就做对”，这样以后就不必重做（和重新测试）它。
下一课
F.X
F 章总结与测试
返回目录
上一课
F.3
Constexpr 函数（第 3 部分）和 consteval