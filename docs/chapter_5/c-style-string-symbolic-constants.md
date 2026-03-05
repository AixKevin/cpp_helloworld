# 17.11 — C 风格字符串符号常量

17.11 — C 风格字符串符号常量
Alex
2015 年 8 月 15 日下午 4:46 (太平洋夏令时)
2023 年 10 月 25 日
在上一课 (
17.10 -- C 风格字符串
) 中，我们讨论了如何创建和初始化 C 风格字符串对象
#include <iostream>

int main()
{
    char name[]{ "Alex" }; // C-style string
    std::cout << name << '\n';

    return 0;
}
C++ 支持两种不同的方式来创建 C 风格字符串符号常量
#include <iostream>

int main()
{
    const char name[] { "Alex" };        // case 1: const C-style string initialized with C-style string literal
    const char* const color{ "Orange" }; // case 2: const pointer to C-style string literal

    std::cout << name << ' ' << color << '\n';

    return 0;
}
这会打印
Alex Orange
虽然上述两种方法产生相同的结果，但 C++ 对它们的内存分配处理方式略有不同。
在情况 1 中，“Alex”被放入（可能是只读的）内存中的某个位置。然后程序为长度为 5 的 C 风格数组（四个显式字符加上空终止符）分配内存，并用字符串“Alex”初始化该内存。所以我们最终得到了两份“Alex”的副本——一份在某个全局内存中，另一份由
name
拥有。由于
name
是 const（并且永远不会被修改），因此进行复制是低效的。
在情况 2 中，编译器如何处理这种情况是实现定义的。通常会发生的是，编译器将字符串“Orange”放入只读内存中的某个位置，然后用字符串的地址初始化指针。
出于优化目的，多个字符串字面量可能会合并为一个值。例如
const char* name1{ "Alex" };
const char* name2{ "Alex" };
这是两个值相同的不同字符串字面量。因为这些字面量是常量，所以编译器可以选择通过将它们合并成一个共享的字符串字面量来节省内存，
name1
和
name2
都指向相同的地址。
使用 const C 风格字符串的类型推导
使用 C 风格字符串字面量的类型推导相当简单
auto s1{ "Alex" };  // type deduced as const char*
    auto* s2{ "Alex" }; // type deduced as const char*
    auto& s3{ "Alex" }; // type deduced as const char(&)[5]
输出指针和 C 风格字符串
您可能已经注意到
std::cout
处理不同类型指针的方式有些有趣。
考虑以下示例
#include <iostream>

int main()
{
    int narr[]{ 9, 7, 5, 3, 1 };
    char carr[]{ "Hello!" };
    const char* ptr{ "Alex" };

    std::cout << narr << '\n'; // narr will decay to type int*
    std::cout << carr << '\n'; // carr will decay to type char*
    std::cout << ptr << '\n'; // name is already type char*

    return 0;
}
在作者的机器上，这打印出来
003AF738
Hello!
Alex
为什么整数数组打印的是地址，而字符数组打印的是字符串？
答案是输出流（例如
std::cout
）对您的意图做了一些假设。如果您向它传递一个非 char 指针，它将简单地打印该指针的内容（指针持有的地址）。但是，如果您向它传递一个类型为
char*
或
const char*
的对象，它将假定您打算打印一个字符串。因此，它不会打印指针的值（一个地址），而是打印所指向的字符串！
虽然这在大多数情况下是期望的，但它可能导致意外的结果。考虑以下情况
#include <iostream>

int main()
{
    char c{ 'Q' };
    std::cout << &c;

    return 0;
}
在这种情况下，程序员打算打印变量
c
的地址。然而，
&c
的类型是
char*
，所以
std::cout
试图将其打印为字符串！由于
c
没有以 null 结尾，我们得到了未定义行为。
在作者的机器上，这打印出来
Q╠╠╠╠╜╡4;¿■A
它为什么这样做？首先，它假定
&c
（类型为
char*
）是一个 C 风格字符串。所以它打印了“Q”，然后继续。内存中的下一个是一堆垃圾。最终，它遇到了一些内存，其中包含一个
0
值，它将其解释为空终止符，所以它停止了。你看到的结果可能有所不同，这取决于变量
c
之后的内存内容。
这种情况在现实生活中不太可能发生（因为您不太可能真的想打印内存地址），但它说明了事物在底层是如何工作的，以及程序是如何在不经意间脱轨的。
如果您确实想打印 char 指针的地址，请将其
static_cast
为
const void*
类型
#include <iostream>

int main()
{
    const char* ptr{ "Alex" };

    std::cout << ptr << '\n';                           // print ptr as C-style string
    std::cout << static_cast<const void*>(ptr) << '\n'; // print address held by ptr
    
    return 0;
}
相关内容
我们将在
19.5 -- 空指针
一课中介绍
void*
。您无需了解它的工作原理即可在此处使用它。
优先使用 std::string_view 作为 C 风格字符串符号常量
在现代 C++ 中，很少有理由使用 C 风格字符串符号常量。相反，请优先使用
constexpr std::string_view
对象，它们通常同样快（甚至更快）且行为更一致。
最佳实践
避免使用 C 风格字符串符号常量，转而使用
constexpr std::string_view
。
下一课
17.12
多维 C 风格数组
返回目录
上一课
17.10
C 风格字符串