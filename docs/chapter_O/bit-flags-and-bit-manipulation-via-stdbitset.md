# O.1 — 位标志和通过 std::bitset 进行位操作

O.1 — 位标志和通过 std::bitset 进行位操作
Alex
2019 年 8 月 17 日，太平洋夏令时 12:06
2025 年 2 月 15 日
在现代计算机架构中，最小的可寻址内存单位是字节。由于所有对象都需要有唯一的内存地址，这意味着对象的大小必须至少为一字节。对于大多数变量类型来说，这没问题。然而，对于布尔值来说，这有点浪费（双关语）。布尔类型只有两种状态：真（1）或假（0）。这组状态只需要一个位来存储。但是，如果一个变量必须至少为一字节，而一个字节是 8 位，这意味着一个布尔值使用 1 位，而将其余 7 位未使用。
在大多数情况下，这没问题——我们通常不会因为内存紧缺到需要关心浪费 7 位（我们最好优化可理解性和可维护性）。然而，在某些存储密集型情况下，为了存储效率，将 8 个独立的布尔值“打包”到一个字节中可能很有用。
做这些事情需要我们能够进行位级别的操作。幸运的是，C++ 提供了工具来精确地完成这项任务。修改对象中的单个位称为
位操作
。
作者注
位操作在某些编程上下文（例如图形、加密、压缩、优化）中大量使用，但在一般编程中则不那么多。
因此，本章全部内容为可选阅读。您可以随意跳过或粗略浏览，稍后再回来阅读。
位标志
到目前为止，我们使用变量来存储单个值。
int foo { 5 }; // assign foo the value 5 (probably uses 32 bits of storage)
std::cout << foo; // print the value 5
然而，我们不将对象视为存储单个值，而是将对象中的每个位视为一个独立的布尔值。当对象的单个位用作布尔值时，这些位称为
位标志
。
命名法
值为
0
的位称为“假”、“关”或“未设置”。
值为
1
的位称为“真”、“开”或“已设置”。
当一个位从
0
变为
1
或从
1
变为
0
时，我们称之为“翻转”或“反转”。
题外话…
在计算中，
标志
是一个值，它在程序中指示某种条件是否存在。对于位标志，值为
true
意味着该条件存在。
类似地，在美国，许多邮箱侧面都附有小（通常是红色）的物理标志。当有待邮递员取走的邮件时，会升起标志以表示有待寄出的邮件。
为了定义一组位标志，我们通常会使用适当大小的无符号整数（8 位、16 位、32 位等……取决于我们有多少个标志），或者
std::bitset
。
#include <bitset> // for std::bitset

std::bitset<8> mybitset {}; // 8 bits in size means room for 8 flags
最佳实践
位操作是您应该明确使用无符号整数（或
std::bitset
）的少数情况之一。
在本课中，我们将展示如何通过
std::bitset
轻松进行位操作。在接下来的几课中，我们将探讨如何以更困难但更通用的方式进行操作。
位编号和位位置
给定一个位序列，我们通常从右到左对位进行编号，从 0 开始（而不是 1）。每个数字表示一个
位位置
。
76543210  Bit position
00000101  Bit sequence
给定位序列 0000 0101，位于位置 0 和 2 的位的值为 1，其他位的值为 0。
通过
std::bitset
操作位
在课程
5.3 -- 数值系统（十进制、二进制、十六进制和八进制）
中，我们已经展示了如何使用
std::bitset
以二进制形式打印值。然而，这并不是
std::bitset
唯一有用的功能。
std::bitset
提供了 4 个用于位操作的关键成员函数：
test() 允许我们查询一个位是 0 还是 1。
set() 允许我们打开一个位（如果位已打开，则不执行任何操作）。
reset() 允许我们关闭一个位（如果位已关闭，则不执行任何操作）。
flip() 允许我们将位值从 0 翻转到 1，反之亦然。
这些函数都将我们想要操作的位的位置作为其唯一参数。
这是一个例子
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<8> bits{ 0b0000'0101 }; // we need 8 bits, start with bit pattern 0000 0101
    bits.set(3);   // set bit position 3 to 1 (now we have 0000 1101)
    bits.flip(4);  // flip bit 4 (now we have 0001 1101)
    bits.reset(4); // set bit 4 back to 0 (now we have 0000 1101)

    std::cout << "All the bits: " << bits<< '\n';
    std::cout << "Bit 3 has value: " << bits.test(3) << '\n';
    std::cout << "Bit 4 has value: " << bits.test(4) << '\n';

    return 0;
}
这会打印
All the bits: 00001101
Bit 3 has value: 1
Bit 4 has value: 0
提醒
我们在课程
5.7 -- std::string 简介
中介绍了成员函数。对于普通函数，我们调用
function(object)
。对于成员函数，我们调用
object.function()
。
我们在课程
5.3 -- 数值系统（十进制、二进制、十六进制和八进制）
中介绍了
0b
二进制字面量前缀和
'
数字分隔符。
给我们的位命名可以帮助我们的代码更具可读性
#include <bitset>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr int  isHungry   { 0 };
    [[maybe_unused]] constexpr int  isSad      { 1 };
    [[maybe_unused]] constexpr int  isMad      { 2 };
    [[maybe_unused]] constexpr int  isHappy    { 3 };
    [[maybe_unused]] constexpr int  isLaughing { 4 };
    [[maybe_unused]] constexpr int  isAsleep   { 5 };
    [[maybe_unused]] constexpr int  isDead     { 6 };
    [[maybe_unused]] constexpr int  isCrying   { 7 };

    std::bitset<8> me{ 0b0000'0101 }; // we need 8 bits, start with bit pattern 0000 0101
    me.set(isHappy);      // set bit position 3 to 1 (now we have 0000 1101)
    me.flip(isLaughing);  // flip bit 4 (now we have 0001 1101)
    me.reset(isLaughing); // set bit 4 back to 0 (now we have 0000 1101)

    std::cout << "All the bits: " << me << '\n';
    std::cout << "I am happy: " << me.test(isHappy) << '\n';
    std::cout << "I am laughing: " << me.test(isLaughing) << '\n';

    return 0;
}
相关内容
我们在课程
1.4 -- 变量赋值和初始化
中介绍了
[maybe_unused]
。
在课程
13.2 -- 无作用域枚举
中，我们展示了枚举器如何更好地收集命名位。
如果我们想一次性获取或设置多个位怎么办？
std::bitset
并没有使这变得容易。为了做到这一点，或者如果我们要使用无符号整数位标志而不是
std::bitset
，我们需要转向更传统的方法。我们将在接下来的几课中介绍这些方法。
std::bitset
的大小
一个潜在的惊喜是
std::bitset
针对速度进行了优化，而不是内存节省。
std::bitset
的大小通常是存储这些位所需的字节数，并向上舍入到最接近的
sizeof(size_t)
，在 32 位机器上是 4 字节，在 64 位机器上是 8 字节。
因此，一个
std::bitset<8>
通常会使用 4 或 8 字节的内存，尽管它技术上只需要 1 字节来存储 8 位。因此，
std::bitset
在我们追求便利而不是内存节省时最有用。
查询
std::bitset
还有一些其他成员函数也很有用：
size() 返回位集中位的数量。
count() 返回位集中设置为
true
的位的数量。
all() 返回一个布尔值，指示所有位是否都设置为
true
。
any() 返回一个布尔值，指示是否有任何位设置为
true
。
none() 返回一个布尔值，指示是否没有位设置为
true
。
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<8> bits{ 0b0000'1101 };
    std::cout << bits.size() << " bits are in the bitset\n";
    std::cout << bits.count() << " bits are set to true\n";

    std::cout << std::boolalpha;
    std::cout << "All bits are true: " << bits.all() << '\n';
    std::cout << "Some bits are true: " << bits.any() << '\n';
    std::cout << "No bits are true: " << bits.none() << '\n';
    
    return 0;
}
这会打印
8 bits are in the bitset
3 bits are set to true
All bits are true: false
Some bits are true: true
No bits are true: false
下一课
O.2
位运算符
返回目录
上一课
6.x
第 6 章总结与测验