# 5.6 — Constexpr 变量

5.6 — Constexpr 变量
Alex
2023 年 10 月 23 日，下午 1:58 PDT
2025 年 2 月 5 日
在上一课
5.5 -- 常量表达式
中，我们定义了什么是常量表达式，讨论了为什么常量表达式是理想的，并总结了常量表达式何时真正在编译时进行求值。
在本课中，我们将仔细研究如何在现代 C++ 中创建可用于常量表达式的变量。我们还将探索确保代码真正在编译时执行的第一种方法。
编译时
const
挑战
在上一课中，我们提到创建可用于常量表达式的变量的一种方法是使用
const
关键字。具有整型类型和常量表达式初始化的
const
变量可用于常量表达式。所有其他
const
变量都不能用于常量表达式。
然而，使用
const
创建可用于常量表达式的变量存在一些挑战。
首先，使用
const
并不能立即清楚变量是否可用于常量表达式。在某些情况下，我们可以相当容易地弄清楚
int a { 5 };       // not const at all
const int b { a }; // clearly not a constant expression (since initializer is non-const)
const int c { 5 }; // clearly a constant expression (since initializer is a constant expression)
在其他情况下，这可能相当困难
const int d { someVar };    // not obvious whether d is usable in a constant expression or not
const int e { getValue() }; // not obvious whether e is usable in a constant expression or not
在上面的示例中，变量
d
和
e
可能可用于也可能不可用于常量表达式，具体取决于
someVar
和
getValue()
的定义方式。这意味着我们必须检查这些初始化器的定义，并推断出我们所处的情况。这甚至可能不够——如果
someVar
是 const 并用变量或函数调用初始化，我们还需要检查其初始化器的定义！
其次，使用
const
无法通知编译器我们需要一个可用于常量表达式的变量（如果不是，则应停止编译）。相反，它只会静默创建一个只能用于运行时表达式的变量。
第三，使用
const
创建编译时常量变量不适用于非整型变量。在许多情况下，我们也希望非整型变量是编译时常量。
constexpr
关键字
幸运的是，我们可以借助编译器的帮助来确保我们在需要时获得编译时常量变量。为此，我们在变量声明中Instead of
const
，我们使用
constexpr
关键字（“constant expression”的缩写）。**constexpr** 变量始终是编译时常量。因此，constexpr 变量必须用常量表达式初始化，否则将导致编译错误。
例如
#include <iostream>

// The return value of a non-constexpr function is not constexpr
int five()
{
    return 5;
}

int main()
{
    constexpr double gravity { 9.8 }; // ok: 9.8 is a constant expression
    constexpr int sum { 4 + 5 };      // ok: 4 + 5 is a constant expression
    constexpr int something { sum };  // ok: sum is a constant expression

    std::cout << "Enter your age: ";
    int age{};
    std::cin >> age;

    constexpr int myAge { age };      // compile error: age is not a constant expression
    constexpr int f { five() };       // compile error: return value of five() is not constexpr

    return 0;
}
由于函数通常在运行时执行，因此函数的返回值不是 constexpr（即使返回表达式是常量表达式）。这就是为什么
five()
对于
constexpr int f
不是合法的初始化值。
相关内容
我们将在
F.1 -- Constexpr 函数
一课中讨论其返回值可用于常量表达式的函数。
此外，
constexpr
适用于非整型变量
constexpr double d { 1.2 }; // d can be used in constant expressions!
const 与 constexpr 对变量的含义
对于变量
const
意味着对象的值在初始化后不能更改。初始化器值可以在编译时或运行时已知。const 对象可以在运行时求值。
constexpr
意味着对象可以在常量表达式中使用。初始化器值必须在编译时已知。constexpr 对象可以在运行时或编译时求值。
Constexpr 变量是隐式 const。Const 变量不是隐式 constexpr（除了带有常量表达式初始化的 const 整型变量）。尽管变量可以同时定义为
constexpr
和
const
，但在大多数情况下这是冗余的，我们只需要使用
const
或
constexpr
。
与
const
不同，
constexpr
不是对象类型的一部分。因此，定义为
constexpr int
的变量实际上具有类型
const int
（由于
constexpr
为对象提供的隐式
const
）。
最佳实践
任何其初始化器为常量表达式的常量变量都应声明为
constexpr
。
任何其初始化器不是常量表达式的常量变量（使其成为运行时常量）都应声明为
const
。
注意：将来我们将讨论一些与
constexpr
不完全兼容的类型（包括
std::string
、
std::vector
以及其他使用动态内存分配的类型）。对于这些类型的常量对象，请使用
const
而不是
constexpr
，或者选择其他 constexpr 兼容的类型（例如
std::string_view
或
std::array
）。
命名法
术语
constexpr
是“constant expression”（常量表达式）的合成词。之所以选择这个名称，是因为 constexpr 对象（和函数）可以在常量表达式中使用。
形式上，关键字
constexpr
仅适用于对象和函数。通常，术语
constexpr
用作任何常量表达式（例如
1 + 2
）的简写。
作者注
本网站上的一些示例是在使用
constexpr
的最佳实践之前编写的——因此，您会注意到有些示例不遵循上述最佳实践。我们目前正在更新不符合要求的示例。
致进阶读者
在 C 和 C++ 中，数组对象的声明（可以包含多个值的对象）要求数组的长度（它可以包含的值的数量）在编译时已知（以便编译器可以确保为数组对象分配正确的内存量）。
由于字面量在编译时已知，它们可以用作数组长度
int arr[5]; // an array of 5 int values, length of 5 is known at compile-time
在许多情况下，最好使用符号常量作为数组长度（例如，为了避免魔术数字并使数组长度在多处使用时更容易更改）。在 C 中，这可以通过预处理器宏或枚举器完成，但不能通过 const 变量（不包括 VLA，它们有其他缺点）。C++ 试图改进这种情况，希望允许使用 const 变量代替宏。但变量的值通常被认为只在运行时已知，这使得它们不适合用作数组长度。
为了解决这个问题，C++ 语言标准增加了一个例外，以便带有常量表达式初始化的 const 整型类型将被视为在编译时已知的值，从而可以作为数组长度使用
const int arrLen = 5;
int arr[arrLen]; // ok: array of 5 ints
当 C++11 引入常量表达式时，将带有常量表达式初始化的 const int 纳入该定义是合理的。委员会讨论了是否也应包含其他类型，但最终决定不包括。
Const 和 constexpr 函数参数
正常的函数调用在运行时求值，提供的参数用于初始化函数参数。由于函数参数的初始化发生在运行时，这导致了两个结果
const
函数参数被视为运行时常量（即使提供的参数是编译时常量）。
函数参数不能声明为
constexpr
，因为它们的初始化值直到运行时才确定。
相关内容
我们将在下面讨论可以在编译时求值（从而用于常量表达式）的函数。
C++ 还支持将编译时常量传递给函数的方式。我们将在
11.9 -- 非类型模板参数
一课中讨论这些内容。
术语回顾
术语
定义
编译时常量
一个值或不可修改的对象，其值必须在编译时已知（例如字面量和 constexpr 变量）。
Constexpr
声明对象为编译时常量（以及可以在编译时求值的函数）的关键字。非正式地，是“常量表达式”的简写。
常量表达式
只包含编译时常量和支持编译时求值的运算符/函数的表达式。
运行时表达式
不是常量表达式的表达式。
运行时常量
不是编译时常量的值或不可修改的对象。
constexpr 函数简介
**constexpr 函数** 是可以在常量表达式中调用的函数。当 constexpr 函数所属的常量表达式必须在编译时求值时（例如，在 constexpr 变量的初始化器中），它必须在编译时求值。否则，constexpr 函数可以在编译时（如果符合条件）或运行时求值。要符合编译时执行的条件，所有参数都必须是常量表达式。
要创建 constexpr 函数，
constexpr
关键字放在函数声明中的返回类型之前
#include <iostream>

int max(int x, int y) // this is a non-constexpr function
{
    if (x > y)
        return x;
    else
        return y;
}

constexpr int cmax(int x, int y) // this is a constexpr function
{
    if (x > y)
        return x;
    else
        return y;
}

int main()
{
    int m1 { max(5, 6) };            // ok
    const int m2 { max(5, 6) };      // ok
    constexpr int m3 { max(5, 6) };  // compile error: max(5, 6) not a constant expression

    int m4 { cmax(5, 6) };           // ok: may evaluate at compile-time or runtime
    const int m5 { cmax(5, 6) };     // ok: may evaluate at compile-time or runtime
    constexpr int m6 { cmax(5, 6) }; // okay: must evaluate at compile-time

    return 0;
}
作者注
我们过去在本章中详细讨论 constexpr 函数，但读者的反馈表明该主题过于冗长和细致，不适合在本教程系列早期介绍。因此，我们已将完整的讨论移至
F.1 -- Constexpr 函数
一课。
本介绍的关键是要记住 constexpr 函数可以在常量表达式中调用。
您将在未来的某些示例中看到 constexpr 函数（如果适用），但在我们正式涵盖该主题之前，我们不会期望您进一步理解或编写自己的 constexpr 函数。
下一课
5.7
std::string 介绍
返回目录
上一课
5.5
常量表达式