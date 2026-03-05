# 10.2 — 浮点和整数提升

10.2 — 浮点和整数提升
Alex
2021年6月17日，太平洋夏令时下午5:38
2024年7月31日
在课程
4.3 -- 对象大小和 sizeof 操作符
中，我们提到 C++ 对每种基本类型都有最小大小保证。然而，这些类型的实际大小会因编译器和架构而异。
这种可变性是允许的，以便可以将
int
和
double
数据类型设置为在给定架构上最大化性能的大小。例如，32 位计算机通常能够一次处理 32 位数据。在这种情况下，
int
很可能会被设置为 32 位的宽度，因为这是 CPU 操作的数据的“自然”大小（并且最有可能具有最佳性能）。
提醒
数据类型使用的位数称为其宽度。更宽的数据类型是指使用更多位的类型，而更窄的数据类型是指使用更少位的类型。
但是，当我们的 32 位 CPU 想要修改 8 位值（例如
char
）或 16 位值时会发生什么？一些 32 位处理器（例如 32 位 x86 CPU）可以直接操作 8 位或 16 位值。然而，这样做通常比操作 32 位值慢！其他 32 位 CPU（例如 32 位 PowerPC CPU）只能操作 32 位值，并且必须采用额外的技巧来操作更窄的值。
数值提升
由于 C++ 旨在在广泛的架构中实现可移植性和高性能，语言设计者不希望假设给定的 CPU 能够高效地操作比该 CPU 自然数据大小更窄的值。
为了帮助解决这个挑战，C++ 定义了一类非正式地称为
数值提升
的类型转换。
数值提升
是某些更窄的数值类型（例如
char
）到某些更宽的数值类型（通常是
int
或
double
）的类型转换，这些类型可以高效地处理。
所有数值提升都是值保留的。
值保留转换
（也称为
安全转换
）是指每个可能的源值都可以转换为目标类型的相等值。
由于提升是安全的，编译器会根据需要自由地使用数值提升，并且在这样做时不会发出警告。
数值提升减少冗余
数值提升还解决了另一个问题。考虑你想编写一个函数来打印
int
类型值的情况：
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}
虽然这很简单，但如果我们还想打印
short
类型或
char
类型的值会怎样？如果不存在类型转换，我们就必须为
short
编写一个不同的打印函数，为
char
编写另一个。别忘了还有
unsigned char
、
signed char
、
unsigned short
、
wchar_t
、
char8_t
、
char16_t
和
char32_t
的版本！你可以看到这很快变得难以管理。
数值提升在这里派上用场：我们可以编写带有
int
和/或
double
参数的函数（例如上面的
printInt()
函数）。然后，可以用可以数值提升以匹配函数参数类型的参数来调用相同的代码。
数值提升类别
数值提升规则分为两个子类别：
整型提升
和
浮点提升
。只有这些类别中列出的转换才被视为数值提升。
浮点提升
我们从更容易的一个开始。
使用
浮点提升
规则，
float
类型的值可以转换为
double
类型的值。
这意味着我们可以编写一个接受
double
的函数，然后用
double
或
float
值调用它
#include <iostream>

void printDouble(double d)
{
    std::cout << d << '\n';
}

int main()
{
    printDouble(5.0); // no conversion necessary
    printDouble(4.0f); // numeric promotion of float to double

    return 0;
}
在第二次调用
printDouble()
中，
float
字面量
4.0f
被提升为
double
，以便参数类型与函数参数的类型匹配。
整型提升
整型提升规则更为复杂。
使用
整型提升
规则，可以进行以下转换：
signed char
或
signed short
可以转换为
int
。
如果
int
可以容纳
unsigned char
、
char8_t
和
unsigned short
的整个范围，则它们可以转换为
int
，否则转换为
unsigned int
。
如果
char
默认是有符号的，则它遵循上述
signed char
转换规则。如果它默认是无符号的，则它遵循上述
unsigned char
转换规则。
bool
可以转换为
int
，其中
false
变为 0，
true
变为 1。
假设一个 8 位字节和
int
大小为 4 字节或更大（这在当今很常见），上述规则基本上意味着
bool
、
char
、
signed char
、
unsigned char
、
signed short
和
unsigned short
都被提升为
int
。
还有一些其他不常用的整型提升规则。这些可以在
https://cppreference.cn/w/cpp/language/implicit_conversion#Integral_promotion
找到。
在大多数情况下，这允许我们编写一个接受
int
参数的函数，然后将其与各种其他整型类型一起使用。例如：
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(2);

    short s{ 3 }; // there is no short literal suffix, so we'll use a variable for this one
    printInt(s); // numeric promotion of short to int

    printInt('a'); // numeric promotion of char to int
    printInt(true); // numeric promotion of bool to int

    return 0;
}
这里有两点值得注意。首先，在某些架构上（例如，使用 2 字节
int
），某些无符号整型类型可能会被提升为
unsigned int
而不是
int
。
其次，一些较窄的无符号类型（例如
unsigned char
）可能会被提升为较大的有符号类型（例如
int
）。因此，虽然整型提升是值保留的，但它不一定保留类型的有符号性（有符号/无符号）。
并非所有拓宽转换都是数值提升
一些拓宽类型转换（例如
char
到
short
，或
int
到
long
）在 C++ 中不被视为数值提升（它们是
数值转换
，我们将在课程
10.3 -- 数值转换
中很快介绍）。这是因为此类转换无助于将较小类型转换为可以更高效处理的较大类型的目标。
这种区别大多是学术性的。然而，在某些情况下，编译器会倾向于数值提升而不是数值转换。当我们介绍函数重载解析时（在即将到来的课程
11.3 -- 函数重载解析和模糊匹配
），我们将看到这会产生影响的示例。
下一课
10.3
数值转换
返回目录
上一课
10.1
隐式类型转换