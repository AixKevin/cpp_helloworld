# 4.12 — 类型转换和 static_cast 简介

4.12 — 类型转换和 static_cast 简介
Alex
2021 年 10 月 21 日，下午 2:27 PDT
2025 年 3 月 3 日
隐式类型转换
考虑以下程序
#include <iostream>

void print(double x) // print takes a double parameter
{
	std::cout << x << '\n';
}

int main()
{
	print(5); // what happens when we pass an int value?

	return 0;
}
在上面的例子中，
print()
函数有一个
double
类型的参数，但调用者传入的值
5
是
int
类型。在这种情况下会发生什么？
在大多数情况下，C++ 允许我们将一种基本类型的值转换为另一种基本类型。将数据从一种类型转换为另一种类型的过程称为
类型转换
。因此，int 参数
5
将被转换为 double 值
5.0
，然后复制到参数
x
中。
print()
函数将打印此值，得到以下输出
5
提醒
默认情况下，小数部分为 0 的浮点值在打印时不带小数位（例如，
5.0
打印为
5
）。
当编译器在未经我们明确要求的情况下替我们进行类型转换时，我们称之为
隐式类型转换
。上面的例子说明了这一点——我们没有明确告诉编译器将整数值
5
转换为 double 值
5.0
。相反，函数期望一个 double 值，我们传入一个整数参数。编译器会注意到不匹配并隐式地将整数转换为 double。
这是一个类似的例子，我们的参数是一个 int 变量而不是 int 字面量
#include <iostream>

void print(double x) // print takes a double parameter
{
	std::cout << x << '\n';
}

int main()
{
	int y { 5 };
	print(y); // y is of type int

	return 0;
}
这与上面完全相同。int 变量
y
持有的值 (
5
) 将被转换为 double 值
5.0
，然后复制到参数
x
中。
值的类型转换产生一个新值
类型转换过程不会修改提供待转换数据的值（或对象）。相反，转换过程将该数据作为输入，并产生转换后的结果。
关键见解
将值转换为另一种类型的值的行为非常类似于调用一个函数，该函数的返回类型与转换的目标类型匹配。待转换的数据作为参数传入，转换后的结果（在临时对象中）返回给调用者使用。
在上面的例子中，转换并没有将变量
y
从
int
类型更改为
double
，也没有将
y
的值从
5
更改为
5.0
。相反，转换使用
y
的值 (
5
) 作为输入，并返回一个值
5.0
的
double
类型临时对象。然后将此临时对象传递给函数
print
。
致进阶读者
一些高级类型转换（例如涉及
const_cast
或
reinterpret_cast
的转换）不会返回临时对象，而是重新解释现有值或对象的类型。
隐式类型转换警告
尽管隐式类型转换在大多数需要类型转换的情况下都足够了，但在某些情况下却不然。考虑以下程序，它与上面的例子类似
#include <iostream>

void print(int x) // print now takes an int parameter
{
	std::cout << x << '\n';
}

int main()
{
	print(5.5); // warning: we're passing in a double value

	return 0;
}
在此程序中，我们将
print()
更改为接受
int
参数，并且对
print()
的函数调用现在传入
double
值
5.5
。与上面类似，编译器将使用隐式类型转换将 double 值
5.5
转换为
int
类型的值，以便将其传递给函数
print()
。
与最初的示例不同，当编译此程序时，您的编译器将生成某种关于可能数据丢失的警告。并且因为您已启用“将警告视为错误”（您启用了，对吧？），您的编译器将中止编译过程。
提示
如果您想编译此示例，需要暂时禁用“将警告视为错误”。有关此设置的更多信息，请参阅课程
0.11 -- 配置编译器：警告和错误级别
。
编译并运行后，此程序打印以下内容
5
请注意，尽管我们传入的值是
5.5
，但程序打印的是
5
。因为整型值不能包含小数，当 double 值
5.5
被隐式转换为
int
时，小数部分会被丢弃，只保留整数值。
由于将浮点值转换为整型值会导致任何小数部分被丢弃，因此当编译器进行从浮点到整型值的隐式类型转换时，它会警告我们。即使我们传入一个没有小数部分的浮点值（例如
5.0
）也会发生这种情况——在这种特定情况下，转换为整型值
5
期间不会发生实际的值丢失，但编译器仍可能警告我们转换不安全。
关键见解
某些类型转换（例如
char
到
int
）总是保留被转换的值，而另一些（例如
double
到
int
）可能会导致值在转换过程中发生变化。不安全的隐式转换通常会生成编译器警告，或（在花括号初始化的情况下）错误。
这是花括号初始化成为首选初始化形式的主要原因之一。花括号初始化将确保我们不会尝试使用在隐式类型转换时会丢失值的初始化器来初始化变量
int main()
{
    double d { 5 }; // okay: int to double is safe
    int x { 5.5 }; // error: double to int not safe

    return 0;
}
相关内容
隐式类型转换是一个复杂的主题。我们将在未来的课程中更深入地探讨这个主题，从
10.1 -- 隐式类型转换
开始。
通过 static_cast 运算符进行显式类型转换简介
回到我们最近的
print()
示例，如果我们
有意
将 double 值传递给接受整数的函数（知道转换后的值会丢弃任何小数部分）怎么办？仅仅为了使程序编译而关闭“将警告视为错误”是一个坏主意，因为那样每次编译时我们都会收到警告（我们很快就会学会忽略），并且我们可能会忽略有关更严重问题的警告。
C++ 支持第二种类型转换方法，称为显式类型转换。
显式类型转换
允许我们（程序员）明确告诉编译器将一个值从一种类型转换为另一种类型，并且我们对该转换的结果承担全部责任。如果此类转换导致值丢失，编译器不会警告我们。
要执行显式类型转换，在大多数情况下我们将使用
static_cast
运算符。
static_cast
的语法看起来有点奇怪
static_cast<new_type>(expression)
static_cast 将表达式中的值作为输入，并返回转换为由
new_type
指定的类型（例如 int、bool、char、double）的值。
关键见解
无论何时您看到 C++ 语法（不包括预处理器）使用尖括号（<>），尖括号之间的内容很可能是一个类型。这通常是 C++ 处理需要参数化类型的代码的方式。
让我们使用
static_cast
更新我们之前的程序
#include <iostream>

void print(int x)
{
	std::cout << x << '\n';
}

int main()
{
	print( static_cast<int>(5.5) ); // explicitly convert double value 5.5 to an int

	return 0;
}
因为我们现在明确要求将 double 值
5.5
转换为
int
值，所以编译器在编译时不会生成关于可能数据丢失的警告（这意味着我们可以保持“将警告视为错误”启用）。
相关内容
C++ 支持其他类型的强制类型转换。我们将在未来的课程
10.6 -- 显式类型转换 (casting) 和 static_cast
中讨论更多关于不同类型强制类型转换的内容。
使用 static_cast 将 char 转换为 int
在字符的课程
4.11 -- 字符
中，我们看到使用
std::cout
打印 char 值会使该值作为 char 打印出来
#include <iostream>

int main()
{
    char ch{ 97 }; // 97 is ASCII code for 'a'
    std::cout << ch << '\n';

    return 0;
}
这会打印
a
如果我们想打印整数值而不是字符，我们可以通过使用
static_cast
将值从
char
强制转换为
int
来实现
#include <iostream>

int main()
{
    char ch{ 97 }; // 97 is ASCII code for 'a'
    // print value of variable ch as an int
    std::cout << ch << " has value " << static_cast<int>(ch) << '\n';

    return 0;
}
这会打印
a has value 97
值得注意的是，`static_cast` 的参数会作为一个表达式进行求值。当我们传入一个变量时，该变量会求值以产生其值，然后该值被转换为新类型。变量本身不受将其值强制转换为新类型的影响。在上述情况下，变量 `ch` 仍然是一个 char 类型，即使我们将其值强制转换为 `int` 后，它仍然持有相同的值。
使用 static_cast 进行符号转换
有符号整型值可以使用静态转换转换为无符号整型值，反之亦然。
如果待转换的值可以在目标类型中表示，则转换后的值将保持不变（仅类型会改变）。例如
#include <iostream>

int main()
{
    unsigned int u1 { 5 };
    // Convert value of u1 to a signed int 
    int s1 { static_cast<int>(u1) };
    std::cout << s1 << '\n'; // prints 5

    int s2 { 5 };
    // Convert value of s2 to an unsigned int
    unsigned int u2 { static_cast<unsigned int>(s2) };
    std::cout << u2 << '\n'; // prints 5

    return 0;
}
这会打印
5
5
由于值
5
处于有符号 int 和无符号 int 的范围内，因此可以将值
5
转换为任一类型而不会出现问题。
如果待转换的值不能在目标类型中表示
如果目标类型是无符号的，则该值将进行模数环绕。我们在课程
4.5 -- 无符号整数以及为何避免使用它们
中介绍了模数环绕。
如果目标类型是有符号的，在 C++20 之前，其值是实现定义的，而从 C++20 开始，它将进行模数环绕。
这是一个将两个不可在目标类型中表示的值进行转换的示例（假设为 32 位整数）
#include <iostream>

int main()
{
    int s { -1 };
    std::cout << static_cast<unsigned int>(s) << '\n'; // prints 4294967295 

    unsigned int u { 4294967295 }; // largest 32-bit unsigned int
    std::cout << static_cast<int>(u) << '\n'; // implementation-defined prior to C++20, -1 as of C++20
    
    return 0;
}
自 C++20 起，这将产生以下结果
4294967295
-1
有符号 int 值
-1
无法表示为无符号 int。结果将模数环绕为无符号 int 值
4294967295
。
无符号 int 值
4294967295
不能表示为有符号 int。在 C++20 之前，结果是实现定义的（但可能为
-1
）。从 C++20 开始，结果将模数环绕为
-1
。
警告
在 C++20 之前，如果待转换的无符号整型值不能在有符号类型中表示，则将其转换为有符号整型值将导致实现定义的行为。
std::int8_t 和 std::uint8_t 可能像字符而不是整数一样行为
正如在课程
4.6 -- 固定宽度整数和 size_t
中所指出的，大多数编译器定义并处理
std::int8_t
和
std::uint8_t
（以及相应的 fast 和 least 固定宽度类型）与
signed char
和
unsigned char
类型完全相同。既然我们已经了解了字符是什么，我们就可以演示这可能出现问题的地方
#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t myInt{65};      // initialize myInt with value 65
    std::cout << myInt << '\n'; // you're probably expecting this to print 65

    return 0;
}
因为
std::int8_t
声明自己是 int，你可能会被误导地认为上面的程序会打印整数值
65
。然而，在大多数系统上，这个程序会打印
A
（将
myInt
视为
signed char
）。但这并非必然（在某些系统上，它可能确实会打印
65
）。
如果您想确保
std::int8_t
或
std::uint8_t
对象被视为整数，可以使用
static_cast
将其值转换为整数
#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t myInt{65};
    std::cout << static_cast<int>(myInt) << '\n'; // will always print 65

    return 0;
}
在
std::int8_t
被视为字符的情况下，来自控制台的输入也可能导致问题
#include <cstdint>
#include <iostream>

int main()
{
    std::cout << "Enter a number between 0 and 127: ";
    std::int8_t myInt{};
    std::cin >> myInt;

    std::cout << "You entered: " << static_cast<int>(myInt) << '\n';

    return 0;
}
此程序的示例运行
Enter a number between 0 and 127: 35
You entered: 51
这是怎么回事。当
std::int8_t
被视为字符时，输入例程将我们的输入解释为字符序列，而不是整数。因此，当我们输入
35
时，我们实际上输入了两个字符，
'3'
和
'5'
。由于 char 对象只能容纳一个字符，因此提取
'3'
（
'5'
留在输入流中以供以后可能提取）。由于字符
'3'
的 ASCII 码点为 51，因此值
51
存储在
myInt
中，我们稍后将其打印为 int。
相比之下，其他固定宽度类型将始终打印并输入为整型值。
小测验时间
问题 #1
编写一个简短的程序，要求用户输入一个字符。使用
static_cast
打印该字符的值及其 ASCII 码。
程序的输出应与以下内容匹配
Enter a single character: a
You entered 'a', which has ASCII code 97.
显示答案
#include <iostream>

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;
	std::cout << "You entered '" << c << "', which has ASCII code " << static_cast<int>(c) << ".\n";

	return 0;
}
问题 #2
修改您为测验 #1 编写的程序，使用隐式类型转换而不是
static_cast
。您能想到多少种不同的方法来做到这一点？
注意：您应该倾向于使用显式转换而不是隐式转换，因此在实际程序中不要这样做——这只是为了测试您对隐式转换可能发生的位置的理解。
显示答案
有几种简单的方法可以做到这一点。
首先，我们可以创建一个
int
变量，并用我们的
char
值对其进行初始化。这将在初始化时进行隐式转换。
#include <iostream>

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;

	int ascii{ c };
	std::cout << "You entered '" << c << "', which has ASCII code " << ascii << ".\n";

	return 0;
}
或者，我们可以使用一个函数将
char
值作为
int
返回。这将在返回时进行隐式转换。
#include <iostream>

int charAsInt(char c)
{
	return c;
}

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;

	std::cout << "You entered '" << c << "', which has ASCII code " << charAsInt(c) << ".\n";

	return 0;
}
我们也可以使用函数，并在参数复制到函数参数时发生隐式转换
#include <iostream>

int getInt(int c)
{
	return c;
}

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;

	std::cout << "You entered '" << c << "', which has ASCII code " << getInt(c) << ".\n";

	return 0;
}
下一课
4.x
第 4 章总结和测验
返回目录
上一课
4.11
字符