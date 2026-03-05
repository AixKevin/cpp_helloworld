# 4.11 — 字符

4.11 — 字符
Alex
2007 年 6 月 9 日，太平洋时间下午 7:07
2025 年 3 月 19 日
到目前为止，我们学过的基本数据类型都用于存储数字（整数和浮点数）或真/假值（布尔值）。但是，如果我们想存储字母或标点符号怎么办？
#include <iostream>

int main()
{
    std::cout << "Would you like a burrito? (y/n)";

    // We want the user to enter a 'y' or 'n' character
    // How do we do this?

    return 0;
}
char
数据类型被设计用于存储单个
字符
。
字符
可以是单个字母、数字、符号或空白。
char 数据类型是一种整型，这意味着底层值以整数形式存储。类似于布尔值 `0` 被解释为 `false`，非零被解释为 `true`，char 变量存储的整数被解释为 `ASCII 字符`。
ASCII
代表美国信息交换标准代码，它定义了一种特定的方式，将英文字符（以及一些其他符号）表示为 0 到 127 之间的数字（称为
ASCII 码
或
代码点
）。例如，ASCII 码 97 被解释为字符 'a'。
字符字面量总是放在单引号之间（例如 'g', '1', ' '）。
以下是完整的 ASCII 字符表
代码
符号
代码
符号
代码
符号
代码
符号
0
NUL (空)
32
(空格)
64
@
96
`
1
SOH (标题开始)
33
!
65
A
97
a
2
STX (文本开始)
34
"
66
B
98
b
3
ETX (文本结束)
35
#
67
C
99
c
4
EOT (传输结束)
36
$
68
D
100
d
5
ENQ (询问)
37
%
69
E
101
e
6
ACK (确认)
38
&
70
F
102
f
7
BEL (响铃)
39
'
71
G
103
g
8
BS (退格)
40
(
72
H
104
h
9
HT (水平制表符)
41
)
73
I
105
i
10
LF (换行/新行)
42
*
74
J
106
j
11
VT (垂直制表符)
43
+
75
K
107
k
12
FF (换页符 / 新页)
44
,
76
L
108
l
13
CR (回车)
45
-
77
M
109
m
14
SO (移出)
46
.
78
N
110
n
15
SI (移入)
47
/
79
O
111
o
16
DLE (数据链路转义)
48
0
80
P
112
p
17
DC1 (数据控制 1)
49
1
81
Q
113
q
18
DC2 (数据控制 2)
50
2
82
R
114
r
19
DC3 (数据控制 3)
51
3
83
S
115
s
20
DC4 (数据控制 4)
52
4
84
T
116
t
21
NAK (否定确认)
53
5
85
U
117
u
22
SYN (同步空闲)
54
6
86
V
118
v
23
ETB (传输块结束)
55
7
87
W
119
w
24
CAN (取消)
56
8
88
X
120
x
25
EM (介质结束)
57
9
89
Y
121
y
26
SUB (替换)
58
:
90
Z
122
z
27
ESC (转义)
59
;
91
[
123
{
28
FS (文件分隔符)
60
<
92
\
124
|
29
GS (组分隔符)
61
=
93
]
125
}
30
RS (记录分隔符)
62
>
94
^
126
~
31
US (单元分隔符)
63
?
95
_
127
DEL (删除)
代码 0-31 和 127 被称为不可打印字符。这些代码旨在控制打印机等外围设备（例如，通过指示打印机如何移动打印头）。现在大多数已过时。如果您尝试打印这些字符，结果取决于您的操作系统（您可能会得到一些类似表情符号的字符）。
代码 32-126 被称为可打印字符，它们代表大多数计算机用于显示基本英文字符的字母、数字字符和标点符号。
如果您尝试打印超出 ASCII 范围的字符，结果也取决于您的操作系统。
初始化字符
您可以使用字符字面量初始化 char 变量
char ch2{ 'a' }; // initialize with code point for 'a' (stored as integer 97) (preferred)
您也可以用整数初始化 char，但应尽可能避免这样做
char ch1{ 97 }; // initialize with integer 97 ('a') (not preferred)
警告
注意不要混淆字符数字和整数数字。以下两种初始化方式不同
char ch{5}; // initialize with integer 5 (stored as integer 5)
char ch{'5'}; // initialize with code point for '5' (stored as integer 53)
字符数字旨在当我们想将数字表示为文本，而不是作为用于数学运算的数字时使用。
打印字符
当使用 std::cout 打印 char 时，std::cout 将 char 变量输出为 ASCII 字符
#include <iostream>

int main()
{
    char ch1{ 'a' }; // (preferred)
    std::cout << ch1; // cout prints character 'a'

    char ch2{ 98 }; // code point for 'b' (not preferred)
    std::cout << ch2; // cout prints a character ('b')


    return 0;
}
这会产生结果
ab
我们也可以直接输出字符字面量
std::cout << 'c';
这会产生结果
c
输入字符
以下程序要求用户输入一个字符，然后打印该字符
#include <iostream>

int main()
{
    std::cout << "Input a keyboard character: ";

    char ch{};
    std::cin >> ch;
    std::cout << "You entered: " << ch << '\n';

    return 0;
}
以下是运行结果
Input a keyboard character: q
You entered: q
请注意，std::cin 允许您输入多个字符。但是，变量 ch 只能容纳 1 个字符。因此，只有第一个输入字符被提取到变量 ch 中。用户输入的其余部分留在 std::cin 使用的输入缓冲区中，可以通过后续对 std::cin 的调用提取。
您可以在以下示例中看到此行为
#include <iostream>

int main()
{
    std::cout << "Input a keyboard character: "; // assume the user enters "abcd" (without quotes)

    char ch{};
    std::cin >> ch; // ch = 'a', "bcd" is left queued.
    std::cout << "You entered: " << ch << '\n';

    // Note: The following cin doesn't ask the user for input, it grabs queued input!
    std::cin >> ch; // ch = 'b', "cd" is left queued.
    std::cout << "You entered: " << ch << '\n';
    
    return 0;
}
Input a keyboard character: abcd
You entered: a
You entered: b
如果您想一次读取多个字符（例如，读取姓名、单词或句子），您将需要使用字符串而不是字符。字符串是字符的集合（因此，字符串可以包含多个符号）。我们将在接下来的课程中讨论这个问题 (
5.7 -- std::string 简介
)。
提取空白字符
由于提取输入会忽略前导空白，这在尝试将空白字符提取到 char 变量时可能会导致意外结果
#include <iostream>

int main()
{
    std::cout << "Input a keyboard character: "; // assume the user enters "a b" (without quotes)

    char ch{};
    std::cin >> ch; // extracts a, leaves " b\n" in stream
    std::cout << "You entered: " << ch << '\n';

    std::cin >> ch; // skips leading whitespace (the space), extracts b, leaves "\n" in stream
    std::cout << "You entered: " << ch << '\n';

    return 0;
}
Input a keyboard character: a b
You entered: a
You entered: b
在上面的例子中，我们可能期望提取空格，但由于前导空白被跳过，我们反而提取了字符“b”。
解决此问题的一种简单方法是使用 `std::cin.get()` 函数进行提取，因为此函数不忽略前导空格
#include <iostream>

int main()
{
    std::cout << "Input a keyboard character: "; // assume the user enters "a b" (without quotes)

    char ch{};
    std::cin.get(ch); // extracts a, leaves " b\n" in stream
    std::cout << "You entered: " << ch << '\n';

    std::cin.get(ch); // extracts space, leaves "b\n" in stream
    std::cout << "You entered: " << ch << '\n';

    return 0;
}
Input a keyboard character: a b
You entered: a
You entered:
字符大小、范围和默认符号
C++ 将 char 定义为始终为 1 字节大小。默认情况下，char 可以是有符号的或无符号的（尽管通常是有符号的）。如果您使用 char 来保存 ASCII 字符，则无需指定符号（因为有符号和无符号 char 都可以保存 0 到 127 之间的值）。
如果您使用 char 存储小整数（除非您明确优化空间，否则不应这样做），您应该始终指定它是有符号还是无符号。有符号 char 可以存储 -128 到 127 之间的数字。无符号 char 可以存储 0 到 255 之间的数字。
转义序列
C++ 中有一些字符序列具有特殊含义。这些字符被称为
转义序列
。转义序列以反斜杠“\”字符开头，然后是后续的字母或数字。
您已经见过最常见的转义序列：`'\n'`，它可以用于打印换行符
#include <iostream>

int main()
{
    int x { 5 };
    std::cout << "The value of x is: " << x << '\n'; // standalone \n goes in single quotes
    std::cout << "First line\nSecond line\n";        // \n can be embedded in double quotes
    return 0;
}
这输出
The value of x is: 5
First line
Second line
另一个常用转义序列是 `'\t'`，它嵌入一个水平制表符
#include <iostream>

int main()
{
    std::cout << "First part\tSecond part";
    return 0;
}
输出
First part	Second part
其他三个值得注意的转义序列是
\' 打印单引号
\" 打印双引号
\\ 打印反斜杠
这是所有转义序列的表格
名称
符号
含义
警报
\a
发出警报，例如蜂鸣声
退格
\b
将光标后退一个空格
换页
\f
将光标移动到下一逻辑页
换行
\n
将光标移动到下一行
回车
\r
将光标移动到行首
水平制表符
\t
打印水平制表符
垂直制表符
\v
打印垂直制表符
单引号
\'
打印单引号
双引号
\"
打印双引号
反斜杠
\\
打印一个反斜杠。
问号
\?
打印一个问号。
不再相关。您可以使用未转义的问号。
八进制数
\(数字)
转换为由八进制表示的字符
十六进制数
\x(数字)
转换为由十六进制数表示的字符
以下是一些示例
#include <iostream>

int main()
{
    std::cout << "\"This is quoted text\"\n";
    std::cout << "This string contains a single backslash \\\n";
    std::cout << "6F in hex is char '\x6F'\n";
    return 0;
}
打印
"This is quoted text"
This string contains a single backslash \
6F in hex is char 'o'
警告
转义序列以反斜杠（\）开头，而不是正斜杠（/）。如果您不小心使用了正斜杠，它可能仍然会编译，但不会产生所需的结果。
换行符 (\n) 与 std::endl
我们在课程
1.5 — iostream 简介：cout、cin 和 endl
中讨论了此主题。
将符号放在单引号和双引号之间的区别是什么？
单引号之间的文本被视为 `char` 字面量，表示单个字符。例如，`'a'` 表示字符 `a`，`'+'` 表示加号字符，`'5'` 表示字符 `5` (不是数字 5)，`'\n'` 表示换行符。
双引号之间的文本（例如“Hello, world!”）被视为 C 风格字符串字面量，可以包含多个字符。我们将在课程
5.2 — 字面量
中讨论字符串。
最佳实践
单个字符通常应使用单引号（例如 `‘t’` 或 `‘\n’`），而不是双引号（例如 `“t”` 或 `“\n”`）。一个可能的例外是在输出时，为了保持一致性，最好对所有内容使用双引号（请参阅课程
1.5 — iostream 简介：cout、cin 和 endl
）。
避免多字符字面量
由于向后兼容性原因，许多 C++ 编译器支持**多字符字面量**，即包含多个字符的 char 字面量（例如 `‘56’`）。如果支持，这些字面量具有实现定义的值（意味着它因编译器而异）。由于它们不属于 C++ 标准，并且其值未严格定义，因此应避免使用多字符字面量。
最佳实践
避免多字符字面量（例如 `‘56’`）。
多字符字面量支持通常会给新程序员带来问题，当他们忘记转义序列使用正斜杠还是反斜杠时
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

int main()
{
	std::cout << add(1, 2) << '/n'; // we used a forward slash instead of a backslash here

	return 0;
}
程序员期望此程序打印值 `3` 和一个换行符。但相反，在作者的机器上，它输出以下内容
312142
问题在于程序员不小心使用了 `'/n'` (一个由正斜杠和字符 `‘n’` 组成的多字符字面量)，而不是 `'\n'` (换行符的转义序列)。程序首先正确地打印了 `3` ( `add(1, 2)` 的结果)。但随后它打印了多字符字面量 `'/n'` 的值，在作者的机器上，该值是实现定义的 `12142`。
警告
确保您的换行符使用的是转义序列 `'\n'`，而不是多字符字面量 `'/n'`。
关键见解
请注意，如果我们对输出 `"/n"` 使用了双引号，程序将打印 `3/n`，这仍然是错误的，但混淆程度会大大降低。
这里是另一个例子。我们从以下内容开始
#include <iostream>

int main()
{
    int x { 5 };
    std::cout << "The value of x is " << x << '\n'; 

    return 0;
}
此程序输出结果与您预期完全一致
The value of x is 5
但是这个输出不够激动人心，所以我们决定在换行符之前添加一个感叹号
#include <iostream>

int main()
{
    int x { 5 };
    std::cout << "The value of x is " << x << '!\n'; // added exclamation point

    return 0;
}
虽然我们期望输出如下
The value of x is 5!
因为 `‘!\n’` 是一个多字符字面量，所以在作者的机器上，它实际打印了
The value of x is 58458
这不仅不正确，而且很难调试，因为您很可能会假设 `x` 的值是错误的。
在输出字符字面量时使用双引号（而不是单引号）可以更容易地发现或完全避免此类问题。
那么其他字符类型呢，`wchar_t`、`char8_t`、`char16_t` 和 `char32_t`？
就像 ASCII 将整数 0-127 映射到美国英语字符一样，其他字符编码标准也存在，用于将整数（不同大小）映射到其他语言中的字符。除了 ASCII 之外，最著名的映射是 Unicode 标准，它将超过 144,000 个整数映射到许多不同语言中的字符。因为 Unicode 包含如此多的代码点，一个 Unicode 代码点需要 32 位来表示一个字符（称为 UTF-32）。然而，Unicode 字符也可以使用多个 16 位或 8 位字符进行编码（分别称为 UTF-16 和 UTF-8）。
C++11 添加了 `char16_t` 和 `char32_t`，以提供对 16 位和 32 位 Unicode 字符的显式支持。这些字符类型的大小与 `std::uint_least16_t` 和 `std::uint_least32_t` 分别相同（但它们是不同的类型）。C++20 添加了 `char8_t`，以提供对 8 位 Unicode (UTF-8) 的支持。它是一个不同的类型，使用与 `unsigned char` 相同的表示。
您不需要使用 `char8_t`、`char16_t` 或 `char32_t`，除非您计划使您的程序与 Unicode 兼容。`wchar_t` 在几乎所有情况下都应避免使用（除非与 Windows API 接口），因为其大小是实现定义的。
Unicode 和本地化通常超出这些教程的范围，因此我们不再深入讨论。在此期间，您在处理字符（和字符串）时应仅使用 ASCII 字符。使用其他字符集中的字符可能会导致您的字符显示不正确。
下一课
4.12
类型转换和 static_cast 简介
返回目录
上一课
4.10
if 语句简介