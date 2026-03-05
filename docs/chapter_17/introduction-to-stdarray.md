# 17.1 — std::array 介绍

17.1 — std::array 介绍
Alex
2015年9月14日，下午4:39 PDT
2024年7月22日
在课程
16.1 -- 容器和数组简介
中，我们介绍了容器和数组。总结如下：
容器为一组未命名的对象（称为元素）提供存储。
数组将其元素在内存中连续分配，并通过下标允许对任何元素进行快速直接访问。
C++ 有三种常用的数组类型：
std::vector
、
std::array
和 C 风格数组。
在课程
16.10 -- std::vector 大小调整和容量
中，我们提到数组分为两类：
固定大小数组（也称为固定长度数组）要求在实例化时知道数组的长度，并且该长度之后无法更改。C 风格数组和
std::array
都是固定大小数组。
动态数组可以在运行时调整大小。
std::vector
是一个动态数组。
在上一章中，我们重点介绍了
std::vector
，因为它速度快，相对易于使用且功能多样。这使其成为我们需要数组容器时的首选类型。
那么为什么不将动态数组用于所有情况呢？
动态数组功能强大且方便，但像生活中的所有事物一样，它们为了所提供的优势做出了一些权衡。
std::vector
的性能略低于固定大小数组。在大多数情况下，你可能不会注意到这种差异（除非你编写了导致大量意外重新分配的草率代码）。
std::vector
仅在非常有限的上下文中支持
constexpr
。
在现代 C++ 中，真正重要的是后一点。constexpr 数组提供了编写更健壮的代码的能力，并且还可以被编译器进行更高度的优化。只要我们能使用 constexpr 数组，我们就应该使用——如果我们需要 constexpr 数组，
std::array
是我们应该使用的容器类。
最佳实践
对 constexpr 数组使用
std::array
，对非 constexpr 数组使用
std::vector
。
定义
std::array
std::array
在 `
` 头文件中定义。它的设计类似于
std::vector
，正如你将看到的，两者之间相似之处多于差异。
一个区别在于我们如何声明
std::array
：
#include <array>  // for std::array
#include <vector> // for std::vector

int main()
{
    std::array<int, 5> a {};  // a std::array of 5 ints

    std::vector<int> b(5);    // a std::vector of 5 ints (for comparison)

    return 0;
}
我们的
std::array
声明有两个模板参数。第一个 (
int
) 是一个类型模板参数，定义数组元素的类型。第二个 (
5
) 是一个整型非类型模板参数，定义数组长度。
相关内容
我们在课程
11.9 -- 非类型模板参数
中介绍了非类型模板参数。
std::array
的长度必须是常量表达式。
与可以在运行时调整大小的
std::vector
不同，
std::array
的长度必须是常量表达式。通常，为长度提供的值将是整型字面量、constexpr 变量或无作用域枚举器。
#include <array>

int main()
{
    std::array<int, 7> a {}; // Using a literal constant

    constexpr int len { 8 };
    std::array<int, len> b {}; // Using a constexpr variable

    enum Colors
    {
         red,
         green,
         blue,
         max_colors
    };

    std::array<int, max_colors> c {}; // Using an enumerator

#define DAYS_PER_WEEK 7
    std::array<int, DAYS_PER_WEEK> d {}; // Using a macro (don't do this, use a constexpr variable instead)

    return 0;
}
请注意，非 const 变量和运行时常量不能用于长度。
#include <array>
#include <iostream>

void foo(const int length) // length is a runtime constant
{
    std::array<int, length> e {}; // error: length is not a constant expression
}

int main()
{
    // using a non-const variable
    int numStudents{};
    std::cin >> numStudents; // numStudents is non-constant

    std::array<int, numStudents> {}; // error: numStudents is not a constant expression

    foo(7);

    return 0;
}
警告
也许令人惊讶的是，
std::array
可以定义为长度为 0。
#include <array>
#include <iostream>

int main()
{
    std::array<int, 0> arr {}; // creates a zero-length std::array
    std::cout << arr.empty();  // true if arr is zero-length

    return 0;
}
零长度的
std::array
是一个没有数据的特殊类。因此，调用任何访问零长度
std::array
数据的成员函数（包括
operator[]
）都会导致未定义行为。
你可以使用
empty()
成员函数测试
std::array
是否为零长度，如果数组为零长度，则返回
true
，否则返回
false
。
std::array
的聚合初始化
也许令人惊讶的是，
std::array
是一个聚合。这意味着它没有构造函数，而是使用聚合初始化进行初始化。快速回顾一下，聚合初始化允许我们直接初始化聚合的成员。为此，我们提供一个初始化列表，它是一个用花括号括起来的逗号分隔的初始化值列表。
相关内容
我们在课程
13.8 -- 结构体聚合初始化
中介绍了结构体的聚合初始化。
#include <array>

int main()
{
    std::array<int, 6> fibonnaci = { 0, 1, 1, 2, 3, 5 }; // copy-list initialization using braced list
    std::array<int, 5> prime { 2, 3, 5, 7, 11 };         // list initialization using braced list (preferred)

    return 0;
}
这些初始化形式中的每一种都按顺序初始化数组成员，从元素 0 开始。
如果
std::array
在没有初始化器的情况下定义，则元素将进行默认初始化。在大多数情况下，这将导致元素未初始化。
因为我们通常希望我们的元素被初始化，所以当没有提供初始化器时，
std::array
应该进行值初始化（使用空花括号）。
#include <array>
#include <vector>

int main()
{
    std::array<int, 5> a;   // Members default initialized (int elements are left uninitialized)
    std::array<int, 5> b{}; // Members value initialized (int elements are zero initialized) (preferred)

    std::vector<int> v(5);  // Members value initialized (int elements are zero initialized) (for comparison)

    return 0;
}
如果在初始化列表中提供的初始化器多于定义的数组长度，编译器将报错。如果在初始化列表中提供的初始化器少于定义的数组长度，则剩余的没有初始化器的元素将进行值初始化。
#include <array>

int main()
{
    std::array<int, 4> a { 1, 2, 3, 4, 5 }; // compile error: too many initializers
    std::array<int, 4> b { 1, 2 };          // b[2] and b[3] are value initialized

    return 0;
}
Const 和 constexpr
std::array
一个
std::array
可以是 const。
#include <array>

int main()
{
    const std::array<int, 5> prime { 2, 3, 5, 7, 11 };

    return 0;
}
尽管
const std::array
的元素没有显式标记为 const，但它们仍然被视为 const（因为整个数组是 const 的）。
std::array
也完全支持 constexpr。
#include <array>

int main()
{
    constexpr std::array<int, 5> prime { 2, 3, 5, 7, 11 };

    return 0;
}
对 constexpr 的支持是使用
std::array
的主要原因。
最佳实践
尽可能将
std::array
定义为 constexpr。如果你的
std::array
不是 constexpr，请考虑改用
std::vector
。
std::array
的类模板参数推导 (CTAD)
C++17
在 C++17 中使用 CTAD（类模板参数推导），我们可以让编译器从初始化器列表中推导出
std::array
的元素类型和数组长度。
#include <array>
#include <iostream>

int main()
{
    constexpr std::array a1 { 9, 7, 5, 3, 1 }; // The type is deduced to std::array<int, 5>
    constexpr std::array a2 { 9.7, 7.31 };     // The type is deduced to std::array<double, 2>

    return 0;
}
我们尽可能偏爱这种语法。如果你的编译器不支持 C++17，你需要显式提供类型和长度模板参数。
最佳实践
使用类模板参数推导 (CTAD) 让编译器从其初始化器中推导出
std::array
的类型和长度。
CTAD 不支持模板参数的部分省略（截至 C++23），因此无法使用核心语言特性仅省略
std::array
的长度或仅省略类型。
#include <iostream>

int main()
{
    constexpr std::array<int> a2 { 9, 7, 5, 3, 1 };     // error: too few template arguments (length missing)
    constexpr std::array<5> a2 { 9, 7, 5, 3, 1 };       // error: too few template arguments (type missing)

    return 0;
}
使用
std::to_array
省略数组长度
C++20
然而，TAD（模板参数推导，用于函数模板解析）支持模板参数的部分省略。自 C++20 起，可以通过使用
std::to_array
帮助函数来省略
std::array
的数组长度。
#include <array>
#include <iostream>

int main()
{
    constexpr auto myArray1 { std::to_array<int, 5>({ 9, 7, 5, 3, 1 }) }; // Specify type and size
    constexpr auto myArray2 { std::to_array<int>({ 9, 7, 5, 3, 1 }) };    // Specify type only, deduce size
    constexpr auto myArray3 { std::to_array({ 9, 7, 5, 3, 1 }) };         // Deduce type and size

    return 0;
}
不幸的是，使用
std::to_array
比直接创建
std::array
更昂贵，因为它涉及创建一个临时的
std::array
，然后用它来复制初始化我们想要的
std::array
。因此，
std::to_array
仅应在无法有效地从初始化器确定类型的情况下使用，并且当数组多次创建时（例如在循环内部）应避免使用。
例如，由于无法指定
short
类型的字面量，你可以使用以下方法创建
short
值的
std::array
（无需显式指定
std::array
的长度）。
#include <array>
#include <iostream>

int main()
{
    constexpr auto shortArray { std::to_array<short>({ 9, 7, 5, 3, 1 }) };
    std::cout << sizeof(shortArray[0]) << '\n';

    return 0;
}
使用
operator[]
访问数组元素
就像
std::vector
一样，访问
std::array
元素最常用的方法是使用下标运算符 (
operator[]
)。
#include <array> // for std::array
#include <iostream>

int main()
{
    constexpr std::array<int, 5> prime{ 2, 3, 5, 7, 11 };

    std::cout << prime[3]; // print the value of element with index 3 (7)
    std::cout << prime[9]; // invalid index (undefined behavior)

    return 0;
}
提醒一下，
operator[]
不执行边界检查。如果提供了无效索引，将导致未定义行为。
我们将在下一课中讨论索引
std::array
的其他几种方法。
小测验时间
问题 #1
std::array
使用哪种类型的初始化？
显示答案
std::array
是一个聚合，因此它使用聚合初始化。
如果你没有提供初始化值，为什么应该显式地对
std::array
进行值初始化？
显示答案
如果没有提供初始化器，
std::array
将默认初始化成员。这将导致大多数类型的元素未初始化。
问题 #2
定义一个
std::array
，用于存储一年中每天的最高温度（精确到小数点后一位）。
显示答案
#include <array>

std::array<double, 365> highTemp {};
问题 #3
使用以下值初始化
std::array
：'h', 'e', 'l', 'l', 'o'。打印索引为 1 的元素的值。
显示答案
#include <array>
#include <iostream>

int main()
{
        constexpr std::array arr { 'h', 'e', 'l', 'l', 'o' };
        std::cout << arr[1] << '\n';

        return 0;
}
下一课
17.2
std::array 长度和索引
返回目录
上一课
16.x
第 16 章总结和测验