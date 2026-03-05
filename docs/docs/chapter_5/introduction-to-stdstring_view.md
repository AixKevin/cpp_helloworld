# 5.8 — std::string_view 简介

5.8 — std::string_view 简介
nascardriver
2019年11月2日，太平洋夏令时上午7:17
2024年11月26日
考虑以下程序
#include <iostream>

int main()
{
    int x { 5 }; // x makes a copy of its initializer
    std::cout << x << '\n';

    return 0;
}
当
x
的定义被执行时，初始化值
5
被复制到为变量
int x
分配的内存中。对于基本类型，初始化和复制变量很快。
现在考虑这个类似的程序
#include <iostream>
#include <string>

int main()
{
    std::string s{ "Hello, world!" }; // s makes a copy of its initializer
    std::cout << s << '\n';

    return 0;
}
当
s
初始化时，C 风格的字符串字面量
"Hello, world!"
被复制到为
std::string s
分配的内存中。与基本类型不同，初始化和复制
std::string
很慢。
在上面的程序中，我们对
s
所做的只是将值打印到控制台，然后
s
被销毁。我们本质上只是为了打印然后销毁该副本而创建了“Hello, world!”的副本。这是低效的。
我们在下面的例子中看到了类似的情况
#include <iostream>
#include <string>

void printString(std::string str) // str makes a copy of its initializer
{
    std::cout << str << '\n';
}

int main()
{
    std::string s{ "Hello, world!" }; // s makes a copy of its initializer
    printString(s);

    return 0;
}
此示例创建了 C 风格字符串“Hello, world!”的两个副本：一个是在
main()
中初始化
s
时，另一个是在
printString()
中初始化参数
str
时。为了打印一个字符串，进行了大量的多余复制！
std::string_view
C++17
为了解决
std::string
初始化（或复制）开销大的问题，C++17 引入了
std::string_view
（它在
头文件中）。
std::string_view
提供对
现有
字符串（C 风格字符串、
std::string
或另一个
std::string_view
）的只读访问，而无需进行复制。
只读
意味着我们可以访问和使用被查看的值，但不能修改它。
以下示例与前一个相同，只是我们将
std::string
替换为
std::string_view
。
#include <iostream>
#include <string_view> // C++17

// str provides read-only access to whatever argument is passed in
void printSV(std::string_view str) // now a std::string_view
{
    std::cout << str << '\n';
}

int main()
{
    std::string_view s{ "Hello, world!" }; // now a std::string_view
    printSV(s);

    return 0;
}
此程序产生与前一个相同的输出，但不会创建字符串“Hello, world!”的副本。
当我们用 C 风格字符串字面量
"Hello, world!"
初始化
std::string_view s
时，
s
提供对“Hello, world!”的只读访问，而无需创建字符串的副本。当我们将
s
传递给
printSV()
时，参数
str
从
s
初始化。这允许我们通过
str
访问“Hello, world!”，同样无需创建字符串的副本。
最佳实践
当你需要只读字符串时，尤其是在函数参数中，优先使用
std::string_view
而不是
std::string
。
std::string_view
可以用许多不同类型的字符串进行初始化
std::string_view
的一个优点是它的灵活性。一个
std::string_view
对象可以用 C 风格字符串、
std::string
或另一个
std::string_view
初始化。
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view s1 { "Hello, world!" }; // initialize with C-style string literal
    std::cout << s1 << '\n';

    std::string s{ "Hello, world!" };
    std::string_view s2 { s };  // initialize with std::string
    std::cout << s2 << '\n';

    std::string_view s3 { s2 }; // initialize with std::string_view
    std::cout << s3 << '\n';
       
    return 0;
}
std::string_view
参数将接受许多不同类型的字符串参数
C 风格字符串和
std::string
都将隐式转换为
std::string_view
。因此，
std::string_view
参数将接受 C 风格字符串、
std::string
或
std::string_view
类型的参数
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view str)
{
    std::cout << str << '\n';
}

int main()
{
    printSV("Hello, world!"); // call with C-style string literal

    std::string s2{ "Hello, world!" };
    printSV(s2); // call with std::string

    std::string_view s3 { s2 };
    printSV(s3); // call with std::string_view
       
    return 0;
}
std::string_view
不会隐式转换为
std::string
因为
std::string
会复制其初始化程序（这很昂贵），所以 C++ 不允许将
std::string_view
隐式转换为
std::string
。这是为了防止意外地将
std::string_view
参数传递给
std::string
参数，并无意中进行了可能不需要的昂贵复制。
但是，如果需要这样做，我们有两种选择
显式地创建一个带有
std::string_view
初始化器的
std::string
（这是允许的，因为这很少是无意中完成的）
使用
static_cast
将现有的
std::string_view
转换为
std::string
以下示例展示了这两种选项
#include <iostream>
#include <string>
#include <string_view>

void printString(std::string str)
{
	std::cout << str << '\n';
}

int main()
{
	std::string_view sv{ "Hello, world!" };

	// printString(sv);   // compile error: won't implicitly convert std::string_view to a std::string

	std::string s{ sv }; // okay: we can create std::string using std::string_view initializer
	printString(s);      // and call the function with the std::string

	printString(static_cast<std::string>(sv)); // okay: we can explicitly cast a std::string_view to a std::string

	return 0;
}
赋值改变了
std::string_view
所查看的内容
将新字符串赋值给
std::string_view
会导致
std::string_view
查看新字符串。它不会以任何方式修改先前正在查看的字符串。
以下示例说明了这一点
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string name { "Alex" };
    std::string_view sv { name }; // sv is now viewing name
    std::cout << sv << '\n'; // prints Alex

    sv = "John"; // sv is now viewing "John" (does not change name)
    std::cout << sv << '\n'; // prints John

    std::cout << name << '\n'; // prints Alex

    return 0;
}
在上面的例子中，
sv = "John"
导致
sv
现在查看字符串
"John"
。它不会改变
name
中保存的值（仍然是
"Alex"
）。
std::string_view
的字面量
默认情况下，双引号字符串字面量是 C 风格字符串字面量。我们可以通过在双引号字符串字面量后面使用
sv
后缀来创建类型为
std::string_view
的字符串字面量。
sv
必须是小写。
#include <iostream>
#include <string>      // for std::string
#include <string_view> // for std::string_view

int main()
{
    using namespace std::string_literals;      // access the s suffix
    using namespace std::string_view_literals; // access the sv suffix

    std::cout << "foo\n";   // no suffix is a C-style string literal
    std::cout << "goo\n"s;  // s suffix is a std::string literal
    std::cout << "moo\n"sv; // sv suffix is a std::string_view literal

    return 0;
}
相关内容
我们在课程
5.7 -- std::string 简介
中讨论了
using namespace
的这种用法。同样的建议也适用于这里。
使用 C 风格字符串字面量初始化
std::string_view
对象是没问题的（你不需要用
std::string_view
字面量来初始化它）。
话虽如此，使用
std::string_view
字面量初始化
std::string_view
不会引起问题（因为这些字面量实际上是伪装的 C 风格字符串字面量）。
constexpr
std::string_view
与
std::string
不同，
std::string_view
完全支持 constexpr
#include <iostream>
#include <string_view>

int main()
{
    constexpr std::string_view s{ "Hello, world!" }; // s is a string symbolic constant
    std::cout << s << '\n'; // s will be replaced with "Hello, world!" at compile-time

    return 0;
}
这使得
constexpr std::string_view
成为需要字符串符号常量时的首选。
我们将在下一课中继续讨论
std::string_view
。
下一课
5.9
std::string_view (第二部分)
返回目录
上一课
5.7
std::string 简介