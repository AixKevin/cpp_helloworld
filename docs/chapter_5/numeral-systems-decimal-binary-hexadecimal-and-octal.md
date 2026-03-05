# 5.3 — 数字系统（十进制、二进制、十六进制和八进制）

5.3 — 数字系统（十进制、二进制、十六进制和八进制）
Alex
2022 年 6 月 16 日，太平洋夏令时下午 2:19
2025 年 2 月 11 日
作者注
本课程为选修课。
未来的课程会引用十六进制数字，因此在继续之前，您至少应该对这个概念有所了解。
在日常生活中，我们使用
十进制
数字进行计数，其中每个数字可以是 0、1、2、3、4、5、6、7、8 或 9。十进制也称为“基数 10”，因为有 10 个可能的数字（0 到 9）。在这个系统中，我们这样计数：0、1、2、3、4、5、6、7、8、9、10、11……默认情况下，C++ 程序中的数字被认为是十进制。
int x { 12 }; // 12 is assumed to be a decimal number
在
二进制
中，只有 2 个数字：0 和 1，所以它被称为“基数 2”。在二进制中，我们这样计数：0、1、10、11、100、101、110、111……为了便于阅读，较长的二进制数字通常用空格分隔成 4 位一组（例如 1101 0100）。
十进制和二进制是
数字系统
的两个例子，这是一个用于表示数字的符号集合（例如数字）的华丽名称。C++ 中有 4 种主要的数字系统。按受欢迎程度排序，它们是：十进制（基数 10）、二进制（基数 2）、十六进制（基数 16）和八进制（基数 8）。
命名法
在十进制和二进制中，数字
0
和
1
具有相同的含义。在这两个系统中，我们称这些数字为“零”和“一”。
但是数字
10
呢？
10
是数字系统中最后一个个位数字之后出现的数字。在十进制中，
10
等于九加一。我们称这个数字为“十”。
在二进制中，
10
使用相同的数字，但等于一加一（相当于十进制中的二）。将二进制的
10
称为“十”会令人困惑，因为“十”是九加一，而这个
10
是一加一。
因此，“十”、“十一”、“十二”等名称通常保留给十进制数字。在非十进制数字系统中，我们更喜欢将这些数字称为一零、一一、一二等……二进制的 101 不是“一百零一”，而是“一零一”。
八进制和十六进制字面量
八进制
是基数 8——也就是说，可用的数字只有：0、1、2、3、4、5、6 和 7。在八进制中，我们这样计数：0、1、2、3、4、5、6、7、10、11、12……（注意：没有 8 和 9，所以我们从 7 跳到 10）。
十进制
0
1
2
3
4
5
6
7
8
9
10
11
八进制
0
1
2
3
4
5
6
7
10
11
12
13
要使用八进制字面量，请在字面量前加上 0（零）
#include <iostream>

int main()
{
    int x{ 012 }; // 0 before the number means this is octal
    std::cout << x << '\n';
    return 0;
}
这个程序打印
10
为什么是 10 而不是 12？因为数字默认以十进制输出，而八进制的 12 等于十进制的 10。
八进制几乎从未使用过，我们建议您避免使用它。
十六进制
是基数 16。在十六进制中，我们这样计数：0、1、2、3、4、5、6、7、8、9、A、B、C、D、E、F、10、11、12……
十进制
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
十六进制
0
1
2
3
4
5
6
7
8
9
A
B
C
D
E
F
10
11
您也可以使用小写字母（尽管大写更常见）。
要使用十六进制字面量，请在字面量前加上
0x
#include <iostream>

int main()
{
    int x{ 0xF }; // 0x before the number means this is hexadecimal
    std::cout << x << '\n';
    return 0;
}
这个程序打印
15
您也可以使用
0X
前缀，但
0x
是约定俗成的，因为它更容易阅读。
数字系统表
这是四个数字系统的排列，以便更容易看出每个系统如何进展
Decimal         0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15
Binary          0     1    10    11   100   101   110   111  1000  1001  1010  1011  1100  1101  1110  1111
Octal           0     1     2     3     4     5     6     7    10    11    12    13    14    15    16    17
Hexadecimal     0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F

Decimal        16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31
Binary      10000 10001 10010 10011 10100 10101 10110 10111 11000 11001 11010 11011 11100 11101 11110 11111
Octal          20    21    22    23    24    25    26    27    30    31    32    33    34    35    36    37
Hexadecimal    10    11    12    13    14    15    16    17    18    19    1A    1B    1C    1D    1E    1F
这些行中的每一行都包含相同的模式：最右边的数字从 0 递增到 (基数-1)。当数字达到 (基数) 时，它将重置为 0，并且左侧的数字递增 1。如果这个左侧数字达到 (基数)，它将重置为 0，并且它左侧的数字递增 1。依此类推……
使用十六进制表示二进制
因为一个十六进制数字有 16 个不同的值，我们可以说一个十六进制数字包含 4 位。因此，一对十六进制数字可以用来精确表示一个完整的字节。
十六进制
0
1
2
3
4
5
6
7
8
9
A
B
C
D
E
F
二进制
0000
0001
0010
0011
0100
0101
0110
0111
1000
1001
1010
1011
1100
1101
1110
1111
考虑一个二进制值为 0011 1010 0111 1111 1001 1000 0010 0110 的 32 位整数。由于数字的长度和重复，它不容易阅读。在十六进制中，相同的值将是：3A7F 9826，这更加简洁。因此，十六进制值通常用于表示内存地址或内存中的原始数据（其类型未知）。
二进制字面量
在 C++14 之前，不支持二进制字面量。然而，十六进制字面量为我们提供了一个有用的变通方法（您可能仍然在现有代码库中看到）
#include <iostream>

int main()
{
    int bin{};    // assume 16-bit ints
    bin = 0x0001; // assign binary 0000 0000 0000 0001 to the variable
    bin = 0x0002; // assign binary 0000 0000 0000 0010 to the variable
    bin = 0x0004; // assign binary 0000 0000 0000 0100 to the variable
    bin = 0x0008; // assign binary 0000 0000 0000 1000 to the variable
    bin = 0x0010; // assign binary 0000 0000 0001 0000 to the variable
    bin = 0x0020; // assign binary 0000 0000 0010 0000 to the variable
    bin = 0x0040; // assign binary 0000 0000 0100 0000 to the variable
    bin = 0x0080; // assign binary 0000 0000 1000 0000 to the variable
    bin = 0x00FF; // assign binary 0000 0000 1111 1111 to the variable
    bin = 0x00B3; // assign binary 0000 0000 1011 0011 to the variable
    bin = 0xF770; // assign binary 1111 0111 0111 0000 to the variable

    return 0;
}
从 C++14 开始，我们可以通过使用 0b 前缀来使用二进制字面量
#include <iostream>

int main()
{
    int bin{};        // assume 16-bit ints
    bin = 0b1;        // assign binary 0000 0000 0000 0001 to the variable
    bin = 0b11;       // assign binary 0000 0000 0000 0011 to the variable
    bin = 0b1010;     // assign binary 0000 0000 0000 1010 to the variable
    bin = 0b11110000; // assign binary 0000 0000 1111 0000 to the variable

    return 0;
}
数字分隔符
由于长字面量可能难以阅读，C++14 还添加了使用引号 ( ' ) 作为数字分隔符的功能。
#include <iostream>

int main()
{
    int bin { 0b1011'0010 };  // assign binary 1011 0010 to the variable
    long value { 2'132'673'462 }; // much easier to read than 2132673462

    return 0;
}
另请注意，分隔符不能出现在值的第一位之前
int bin { 0b'1011'0010 };  // error: ' used before first digit of value
数字分隔符纯粹是视觉上的，不会以任何方式影响字面量值。
以十进制、八进制或十六进制输出值
默认情况下，C++ 以十进制输出值。但是，您可以通过使用
std::dec
、
std::oct
和
std::hex
I/O 操纵器来更改输出格式
#include <iostream>

int main()
{
    int x { 12 };
    std::cout << x << '\n'; // decimal (by default)
    std::cout << std::hex << x << '\n'; // hexadecimal
    std::cout << x << '\n'; // now hexadecimal
    std::cout << std::oct << x << '\n'; // octal
    std::cout << std::dec << x << '\n'; // return to decimal
    std::cout << x << '\n'; // decimal

    return 0;
}
这会打印
12
c
c
14
12
12
请注意，一旦应用，I/O 操纵器将保持设置以供将来输出，直到再次更改。
以二进制输出值
以二进制输出值稍微困难一些，因为
std::cout
没有内置此功能。幸运的是，C++ 标准库包含一个名为
std::bitset
的类型，它将为我们完成此操作（在
<bitset>
头文件中）。
要使用
std::bitset
，我们可以定义一个
std::bitset
变量并告诉
std::bitset
我们要存储多少位。位的数量必须是编译时常量。
std::bitset
可以用整数值初始化（任何格式，包括十进制、八进制、十六进制或二进制）。
#include <bitset> // for std::bitset
#include <iostream>

int main()
{
	// std::bitset<8> means we want to store 8 bits
	std::bitset<8> bin1{ 0b1100'0101 }; // binary literal for binary 1100 0101
	std::bitset<8> bin2{ 0xC5 }; // hexadecimal literal for binary 1100 0101

	std::cout << bin1 << '\n' << bin2 << '\n';
	std::cout << std::bitset<4>{ 0b1010 } << '\n'; // create a temporary std::bitset and print it

	return 0;
}
这会打印
11000101
11000101
1010
在上面的代码中，这行
std::cout << std::bitset<4>{ 0b1010 } << '\n'; // create a temporary std::bitset and print it
创建一个具有 4 位的临时（无名）
std::bitset
对象，用二进制字面量
0b1010
初始化它，以二进制打印值，然后丢弃临时对象。
相关内容
我们在第
O.1 -- 位标志和通过 std::bitset 进行位操作
课中更详细地介绍了 std::bitset。
使用格式/打印库以二进制输出值
高级
在 C++20 和 C++23 中，我们有更好的选项通过新的格式库 (C++20) 和打印库 (C++23) 打印二进制
#include <format> // C++20
#include <iostream>
#include <print> // C++23

int main()
{
    std::cout << std::format("{:b}\n", 0b1010);  // C++20, {:b} formats the argument as binary digits
    std::cout << std::format("{:#b}\n", 0b1010); // C++20, {:#b} formats the argument as 0b-prefixed binary digits

    std::println("{:b} {:#b}", 0b1010, 0b1010);  // C++23, format/print two arguments (same as above) and a newline

    return 0;
}
这会打印
1010
0b1010
1010 0b1010
小测验时间
问题 #1
使用上表，32 在二进制和十六进制中是多少？
显示答案
二进制：10 0000
十六进制：20
下一课
5.4
as-if 规则和编译时优化
返回目录
上一课
5.2
字面量