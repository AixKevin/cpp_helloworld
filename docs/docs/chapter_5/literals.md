# 5.2 — 字面量

5.2 — 字面量
Alex
2007 年 6 月 9 日，晚上 10:43 PDT
2025 年 3 月 17 日
字面量
是直接插入代码中的值。例如
return 5;                     // 5 is an integer literal
bool myNameIsAlex { true };   // true is a boolean literal
double d { 3.4 };             // 3.4 is a double literal
std::cout << "Hello, world!"; // "Hello, world!" is a C-style string literal
字面量有时被称为
字面常量
，因为它们的含义不能重新定义（
5
始终表示整数值 5）。
字面量的类型
就像对象有类型一样，所有字面量都有类型。字面量的类型是从字面量的值推导出来的。例如，一个整数（例如
5
）的字面量被推导为
int
类型。
默认情况下
字面值
示例
默认字面量类型
注意
整数值
5, 0, -3
int
布尔值
true, false
bool
浮点值
1.2, 0.0, 3.4
double (不是 float！)
字符
‘a’, ‘\n’
char
C 风格字符串
“Hello, world!”
const char[14]
参见下面的 C 风格字符串字面量部分
字面量后缀
如果字面量的默认类型不是所需的类型，可以通过添加后缀来更改字面量的类型。以下是一些更常见的后缀
数据类型
后缀
含义
整型
u 或 U
unsigned int
整型
l 或 L
long
整型
ul, uL, Ul, UL, lu, lU, Lu, LU
unsigned long
整型
ll 或 LL
long long
整型
ull, uLL, Ull, ULL, llu, llU, LLu, LLU
unsigned long long
整型
z 或 Z
std::size_t 的有符号版本 (C++23)
整型
uz, uZ, Uz, UZ, zu, zU, Zu, ZU
std::size_t (C++23)
浮点型
f 或 F
float
浮点型
l 或 L
long double
字符串
s
std::string
字符串
sv
std::string_view
我们稍后会更详细地讨论整型和浮点型字面量及其后缀。
在大多数情况下，不需要后缀（除了
f
）。
相关内容
s
和
sv
后缀需要额外的代码行才能使用。我们在课程
5.7 -- std::string 简介
和
5.8 -- std::string_view 简介
中进一步介绍这些内容。
还有用于复数和 chrono（时间）字面量的其他（很少使用）后缀。这些后缀在
此处
有说明。
致进阶读者
除了
f
后缀之外，后缀最常用于涉及类型推断的情况。参见
10.8 -- 使用 auto 关键字的对象类型推断
和
13.14 -- 类模板参数推断 (CTAD) 和推断指南
。
后缀大小写
大多数后缀不区分大小写。例外情况是
s
和
sv
必须是小写。
连续的两个
l
或
L
字符必须大小写相同（不接受
lL
和
Ll
）。
因为小写
L
在某些字体中可能看起来像数字
1
，所以一些开发人员更喜欢使用大写字面量。其他人则使用小写后缀，除了
L
。
最佳实践
首选字面量后缀 L（大写）而不是 l（小写）。
整型字面量
通常不需要对整型字面量使用后缀，但以下是示例
#include <iostream>

int main()
{
    std::cout << 5 << '\n';  // 5 (no suffix) is type int (by default)
    std::cout << 5L << '\n'; // 5L is type long
    std::cout << 5u << '\n'; // 5u is type unsigned int

    return 0;
}
在大多数情况下，使用不带后缀的
int
字面量是没问题的，即使在初始化非
int
类型时也是如此
int main()
{
    int a { 5 };          // ok: types match
    unsigned int b { 6 }; // ok: compiler will convert int value 6 to unsigned int value 6
    long c { 7 };         // ok: compiler will convert int value 7 to long value 7

    return 0;
}
在这种情况下，编译器会将 int 字面量转换为适当的类型。
在第一个例子中，
5
默认已经是
int
类型，所以编译器可以直接使用这个值来初始化
int
变量
a
。在第二个例子中，
int
值
6
与
unsigned int b
的类型不匹配。编译器会将 int 值
6
转换为
unsigned int
值
6
，然后用它作为
b
的初始化器。在第三个例子中，
int
值
7
与
long c
的类型不匹配。编译器会将 int 值
7
转换为
long
值
7
，然后用它作为
c
的初始化器。
浮点字面量
默认情况下，浮点字面量的类型为
double
。要将它们改为
float
字面量，应使用
f
（或
F
）后缀
#include <iostream>

int main()
{
    std::cout << 5.0 << '\n';  // 5.0 (no suffix) is type double (by default)
    std::cout << 5.0f << '\n'; // 5.0f is type float

    return 0;
}
新程序员经常对以下代码导致编译器警告感到困惑
float f { 4.1 }; // warning: 4.1 is a double literal, not a float literal
因为
4.1
没有后缀，所以字面量的类型是
double
，而不是
float
。当编译器确定字面量的类型时，它不关心你对字面量做了什么（例如，在这种情况下，用它来初始化一个
float
变量）。由于字面量的类型（
double
）与用于初始化的变量的类型（
float
）不匹配，所以字面量值必须转换为
float
，然后才能用于初始化变量
f
。将
double
值转换为
float
可能会导致精度损失，因此编译器会发出警告。
这里的解决方案是以下之一
float f { 4.1f }; // use 'f' suffix so the literal is a float and matches variable type of float
double d { 4.1 }; // change variable to type double so it matches the literal type double
浮点字面量的科学记数法
有两种不同的方式来书写浮点字面量。
在标准记数法中，我们用小数点书写数字
double pi { 3.14159 }; // 3.14159 is a double literal in standard notation
double d { -1.23 };    // the literal can be negative
double why { 0. };     // syntactically acceptable, but avoid this because it's hard to see the decimal point (prefer 0.0)
在科学记数法中，我们添加一个
e
来表示指数
double avogadro { 6.02e23 }; // 6.02 x 10^23 is a double literal in scientific notation
double protonCharge { 1.6e-19 }; // charge on a proton is 1.6 x 10^-19
字符串字面量
在编程中，
字符串
是按顺序排列的字符集合，用于表示文本（如姓名、单词和句子）。
你编写的第一个 C++ 程序可能看起来像这样
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!";
    return 0;
}
"Hello, world!"
是一个字符串字面量。字符串字面量放在双引号之间以将其识别为字符串（与字符字面量不同，字符字面量放在单引号之间）。
由于字符串在程序中常用，大多数现代编程语言都包含一个基本的字符串数据类型。由于历史原因，字符串在 C++ 中不是基本类型。相反，它们有一个奇怪的、复杂的类型，很难使用（我们将在未来的课程中，当我们覆盖了更多解释它们如何工作所需的基础知识后，再讨论如何/为什么）。这种字符串通常被称为
C 字符串
或
C 风格字符串
，因为它们继承自 C 语言。
关于 C 风格字符串字面量，有两点不明显但值得了解。
所有 C 风格字符串字面量都有一个隐式的空终止符。考虑一个字符串，例如
"hello"
。虽然这个 C 风格字符串看起来只有五个字符，但实际上它有六个字符：
'h'
、
'e'
、
'l'
、
'l'
、
'o'
和
'\0'
（ASCII 码为 0 的字符）。这个尾随的
'\0'
字符是一个特殊字符，称为
空终止符
，它用于指示字符串的结尾。以空终止符结尾的字符串称为
空终止字符串
。
致进阶读者
这就是字符串
"Hello, world!"
的类型是
const char[14]
而不是
const char[13]
的原因——隐藏的空终止符算作一个字符。
空终止符的原因也是历史性的：它可以用来确定字符串的结束位置。
与大多数其他字面量（它们是值，而不是对象）不同，C 风格字符串字面量是程序启动时创建的常量对象，并保证在程序的整个生命周期内都存在。这一点在几节课后，当我们讨论
std::string_view
时，将变得很重要。
关键见解
C 风格字符串字面量是在程序启动时创建的常量对象，并保证在程序的整个生命周期内都存在。
与 C 风格字符串字面量不同，
std::string
和
std::string_view
字面量创建的是临时对象。这些临时对象必须立即使用，因为它们在创建它们的完整表达式结束时就会被销毁。
相关内容
我们分别在课程
5.7 -- std::string 简介
和
5.8 -- std::string_view 简介
中讨论
std::string
和
std::string_view
字面量。
魔法数字
魔法数字
是指含义不明确或以后可能需要更改的字面量（通常是数字）。
以下是显示魔法数字示例的两个语句
const int maxStudentsPerSchool{ numClassrooms * 30 };
setMax(30);
在这些上下文中，字面量
30
是什么意思？在前者中，你可能可以猜到它是每个班级的学生人数，但并不是很明显。在后者中，谁知道呢。我们必须查看函数才能知道它做了什么。
在复杂的程序中，除非有注释解释，否则很难推断字面量代表什么。
使用魔法数字通常被认为是糟糕的做法，因为除了没有提供它们用途的上下文之外，如果值需要更改，它们还会带来问题。假设学校购买了新课桌，允许他们将班级人数从 30 增加到 35，我们的程序需要反映这一点。
为此，我们需要将一个或多个字面量从
30
更新为
35
。但是哪些字面量呢？
maxStudentsPerSchool
初始化器中的
30
似乎很明显。但是用作
setMax()
参数的
30
呢？那个
30
的含义是否与另一个
30
相同？如果是，则应该更新。如果不是，则应该保持不变，否则我们可能会在其他地方破坏程序。如果你进行全局搜索替换，你可能会在不应该更改的情况下无意中更新
setMax()
的参数。所以你必须检查所有代码中每个
30
字面量的实例（可能有数百个），然后单独确定它是否需要更改。这可能非常耗时（而且容易出错）。
幸运的是，上下文缺失和更新问题都可以通过使用符号常量轻松解决
const int maxStudentsPerClass { 30 };
const int totalStudents{ numClassrooms * maxStudentsPerClass }; // now obvious what this 30 means

const int maxNameLength{ 30 };
setMax(maxNameLength); // now obvious this 30 is used in a different context
常量的名称提供了上下文，我们只需要在一个地方更新值即可更改整个程序中的值。
请注意，魔法数字不总是数字——它们也可以是文本（例如名称）或其他类型
int main()
{
    printAppWelcome("MyCalculator"); // bad: app name may be used in other places or change in the future
}
在明显上下文中使用的、不太可能更改的字面量通常不被视为魔法数字。值
-1
、
0
、
0.0
和
1
经常用于此类上下文
int idGenerator { 0 };         // okay: we're starting our id generator with value 0
idGenerator = idGenerator + 1; // okay: we're just incrementing our generator
其他数字在上下文中也可能很明显（因此，不被视为魔法数字）
int kmtoM(int km)
{
    return km * 1000; // okay: it's obvious 1000 is a conversion factor
}
连续的整数 ID 通常也不被视为魔法数字
int main()
{
    // okay: these are just sequential ids/counts
    printPlayerInfo(1); // `1` would not really benefit from being named `player1` instead
    printPlayerInfo(2);
}
最佳实践
避免在代码中使用魔法数字（而是使用 constexpr 变量，参见课程
5.6 -- Constexpr 变量
）。
下一课
5.3
数值系统（十进制、二进制、十六进制和八进制）
返回目录
上一课
5.1
常量变量（命名常量）