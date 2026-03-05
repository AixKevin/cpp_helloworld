# 7.6 — 内部链接

7.6 — 内部链接
Alex
2020 年 1 月 3 日，太平洋标准时间上午 10:37
2025 年 1 月 30 日
在
7.3 — 局部变量
一课中，我们曾说：“标识符的链接性决定了该名称的其他声明是否引用同一对象”，并且我们讨论了局部变量如何具有
无链接
。
全局变量和函数标识符可以具有
内部链接
或
外部链接
。我们将在本课中介绍内部链接的情况，并在
7.7 — 外部链接和变量前向声明
课中介绍外部链接的情况。
具有
内部链接
的标识符可以在单个翻译单元中看到和使用，但无法从其他翻译单元访问。这意味着如果两个源文件具有相同名称的具有内部链接的标识符，这些标识符将被视为独立的（并且不会因为重复定义而导致 ODR 违规）。
关键见解
具有内部链接的标识符可能根本不会对链接器可见。或者，它们可能对链接器可见，但被标记为仅在特定翻译单元中使用。
相关内容
我们在
2.10 — 预处理器简介
课中介绍了翻译单元。
具有内部链接的全局变量
具有内部链接的全局变量有时称为
内部变量
。
要使非常量全局变量成为内部变量，我们使用
static
关键字。
#include <iostream>

static int g_x{}; // non-constant globals have external linkage by default, but can be given internal linkage via the static keyword

const int g_y{ 1 }; // const globals have internal linkage by default
constexpr int g_z{ 2 }; // constexpr globals have internal linkage by default

int main()
{
    std::cout << g_x << ' ' << g_y << ' ' << g_z << '\n';
    return 0;
}
const 和 constexpr 全局变量默认具有内部链接（因此不需要
static
关键字——如果使用了，它将被忽略）。
这是多个文件使用内部变量的示例
a.cpp
[[maybe_unused]] constexpr int g_x { 2 }; // this internal g_x is only accessible within a.cpp
main.cpp
#include <iostream>

static int g_x { 3 }; // this separate internal g_x is only accessible within main.cpp

int main()
{
    std::cout << g_x << '\n'; // uses main.cpp's g_x, prints 3

    return 0;
}
这个程序打印
3
因为
g_x
对于每个文件都是内部的，所以
main.cpp
不知道
a.cpp
也有一个名为
g_x
的变量（反之亦然）。
致进阶读者
上面
static
关键字的使用是
存储类说明符
的一个示例，它设置了名称的链接性和存储期。最常用的
存储类说明符
是
static
、
extern
和
mutable
。术语
存储类说明符
主要用于技术文档中。
致进阶读者
C++11 标准（附录 C）提供了常量变量默认具有内部链接的原因：“因为 const 对象在 C++ 中可以用作编译时值，所以此特性促使程序员为每个 const 提供显式初始化值。此特性允许用户将 const 对象放在包含在许多编译单元的头文件中。”
C++ 的设计者旨在实现两件事
常量对象应该可以在常量表达式中使用。为了在常量表达式中使用，编译器必须已经看到一个定义（而不是声明），以便它可以在编译时进行评估。
常量对象应该能够通过头文件传播。
具有外部链接的对象只能在单个翻译单元中定义，而不会违反 ODR——其他翻译单元必须通过前向声明访问这些对象。如果 const 对象默认具有外部链接，那么它们只能在包含定义的单个翻译单元中的常量表达式中使用，并且它们不能通过头文件有效传播，因为将头文件 #include 到多个源文件中会导致 ODR 违规。
具有内部链接的对象可以在每个需要的翻译单元中拥有一个定义，而不会违反 ODR。这允许将 const 对象放在头文件中，并根据需要 #include 到任意数量的翻译单元中，而不会违反 ODR。由于每个翻译单元都有一个定义而不是声明，这确保了这些常量可以在翻译单元内的常量表达式中使用。
内联变量（可以在不引起 ODR 违规的情况下具有外部链接）直到 C++17 才引入。
具有内部链接的函数
如上所述，函数标识符也具有链接。函数默认具有外部链接（我们将在下一课中介绍），但可以通过
static
关键字设置为内部链接
add.cpp
// This function is declared as static, and can now be used only within this file
// Attempts to access it from another file via a function forward declaration will fail
[[maybe_unused]] static int add(int x, int y)
{
    return x + y;
}
main.cpp
#include <iostream>

int add(int x, int y); // forward declaration for function add

int main()
{
    std::cout << add(3, 4) << '\n';

    return 0;
}
这个程序不会链接，因为函数
add
在
add.cpp
之外无法访问。
一次定义规则和内部链接
在
2.7 — 前向声明和定义
课中，我们提到一次定义规则指出一个对象或函数不能有多个定义，无论是在一个文件内还是在一个程序中。
然而，值得注意的是，在不同文件中定义的内部对象（和函数）被认为是独立的实体（即使它们的名称和类型相同），因此没有违反一次定义规则。每个内部对象只有一个定义。
static
与匿名命名空间
在现代 C++ 中，使用
static
关键字为标识符提供内部链接的做法正在失宠。匿名命名空间可以为更广泛的标识符（例如类型标识符）提供内部链接，并且它们更适合为许多标识符提供内部链接。
我们在
7.14 — 匿名命名空间和内联命名空间
课中介绍了匿名命名空间。
为什么要为标识符提供内部链接？
通常有两个原因要为标识符提供内部链接
有一个我们想确保不能被其他文件访问的标识符。这可能是一个我们不想被修改的全局变量，或者是一个我们不想被调用的辅助函数。
为了更严谨地避免命名冲突。因为具有内部链接的标识符不暴露给链接器，它们只能与同一翻译单元中的名称冲突，而不能与整个程序中的名称冲突。
许多现代开发指南建议为每个不打算从其他文件使用的变量和函数提供内部链接。如果你有纪律，这是一个很好的建议。
目前，我们将推荐一种更轻量级的方法作为最低要求：为任何你有明确理由不允许其他文件访问的标识符提供内部链接。
最佳实践
当你有明确理由不允许其他文件访问时，为标识符提供内部链接。
考虑为你不想被其他文件访问的所有标识符提供内部链接（为此使用匿名命名空间）。
快速总结
// Internal global variables definitions:
static int g_x;          // defines non-initialized internal global variable (zero initialized by default)
static int g_x{ 1 };     // defines initialized internal global variable

const int g_y { 2 };     // defines initialized internal global const variable
constexpr int g_y { 3 }; // defines initialized internal global constexpr variable

// Internal function definitions:
static int foo() {};     // defines internal function
我们在
7.12 — 作用域、持续时间和链接总结
课中提供了全面的总结。
下一课
7.7
外部链接和变量前向声明
返回目录
上一课
7.5
变量遮蔽（名称隐藏）