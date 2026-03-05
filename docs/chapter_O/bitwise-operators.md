# O.2 — 位运算符

O.2 — 位运算符
Alex
2007 年 6 月 17 日，下午 1:12 PDT
2025 年 2 月 26 日
位运算符
C++ 提供了 6 种位操作符，通常称为
位运算符
运算符
符号
形式
操作返回一个值，其中
左移
<<
x << n
x
中的位向左移动
n
位，新位为
0
。
右移
>>
x >> n
x
中的位向右移动
n
位，新位为
0
。
按位非
~
~x
x
中的每个位都被翻转。
按位与
&
x & y
当
x
和
y
中相应的位都为
1
时，每个位都设置为
1
。
按位或
|
x | y
当
x
和
y
中相应的位有一个为
1
时，每个位都设置为
1
。
按位异或
^
x ^ y
当
x
和
y
中相应的位不同时，每个位都设置为
1
。
这些是非修改性运算符（它们不修改其操作数）。
作者注
在以下示例中，我们将主要使用 4 位二进制值。这是为了方便和简化示例。在实际程序中，使用的位数取决于对象的大小（例如，一个 2 字节的对象将存储 16 位）。
为了提高可读性，我们也可以在代码示例之外省略二进制字面量的
0b
前缀（例如，我们可能会选择使用
0101
而不是
0b0101
）。
位运算符是为整数类型和
std::bitset
定义的。我们将在示例中使用
std::bitset
，因为它更容易以二进制形式打印输出。
避免对有符号整数操作数使用位运算符，因为在 C++20 之前，许多运算符会返回实现定义的结果，或者存在其他潜在的陷阱，这些陷阱可以通过使用无符号操作数（或
std::bitset
）轻松避免。
最佳实践
为避免意外，请对无符号整数操作数或
std::bitset
使用位运算符。
按位左移 (<<) 和按位右移 (>>) 运算符
按位左移
(<<) 运算符将位向左移动。左操作数是提供初始位序列的表达式，右操作数是指定要移动的位数位置的整数。例如，当我们写
x << 2
时，我们是说“生成一个值，其中
x
中的位已向左移动 2 个位置。”
左操作数未被修改，从右侧移入的新位为
0
。
以下是一些左移位序列
0011
的示例
0011 \<\< 1 is 0110
0011 \<\< 2 is 1100
0011 \<\< 3 is 1000
请注意，在第三种情况下，我们从数字的末尾移出了一位
1
！从位序列末尾移出的位将永远丢失。
按位右移
(>>) 运算符的工作方式类似，但将位向右移动。
以下是一些右移位序列
1100
的示例
1100 />/> 1 is 0110
1100 />/> 2 is 0011
1100 />/> 3 is 0001
请注意，在第三种情况下，我们将一位移出了数字的右端，因此它丢失了。
让我们在 C++ 中做一个您可以编译和运行的示例
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<4> x { 0b1100 };

    std::cout << x << '\n';
    std::cout << (x >> 1) << '\n'; // shift right by 1, yielding 0110
    std::cout << (x << 1) << '\n'; // shift left by 1, yielding 1000

    return 0;
}
这会打印
1100
0110
1000
致进阶读者
C++ 中的位移是与
字节序
无关的。左移总是朝向最高有效位，右移总是朝向最低有效位。
什么！？运算符 << 和运算符 >> 不是用于输入和输出吗？
确实如此。
今天的程序通常不会大量使用位左移和右移运算符来移位。相反，位左移运算符更常与
std::cout
（或其他输出流对象）一起使用以输出文本。考虑以下程序
#include <bitset>
#include <iostream>

int main()
{
    unsigned int x { 0b0100 };
    x = x << 1; // use operator<< for left shift
    std::cout << std::bitset<4>{ x } << '\n'; // use operator<< for output

    return 0;
}
这个程序打印
1000
在上面的程序中，
operator<<
如何知道在一种情况下移位，而在另一种情况下输出
x
？答案是它查看操作数的类型。如果左操作数是整数类型，则
operator<<
知道执行其通常的位移行为。如果左操作数是
std::cout
等输出流对象，则它知道应该执行输出。
这同样适用于
operator>>
。
相关内容
运算符根据参数类型改变其行为的能力利用了称为
运算符重载
的特性，我们稍后将在课程
13.5 -- I/O 运算符重载简介
中介绍。
请注意，如果您将
operator<<
用于输出和左移，则左移需要括号
#include <bitset>
#include <iostream>

int main()
{
	std::bitset<4> x{ 0b0110 };

	std::cout << x << 1 << '\n'; // print value of x (0110), then 1
	std::cout << (x << 1) << '\n'; // print x left shifted by 1 (1100)

	return 0;
}
这会打印
01101
1100
第一行打印
x
的值 (
0110
)，然后是字面量
1
。第二行打印
x
左移
1
的值 (
1100
)。
按位非
按位非
运算符 (~) 在概念上很简单：它只是将每个位从
0
翻转为
1
，反之亦然。
~0011 is 1100
~0000 0100 is 1111 1011
致进阶读者
当被解释为整数时，按位非结果中的位数会影响生成的值。
以下程序说明了这一点
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<4> b4{ 0b100 }; // b4 is 0100
    std::bitset<8> b8{ 0b100 }; // b8 is 0000 0100

    std::cout << "Initial values:\n";
    std::cout << "Bits: " << b4 << ' ' << b8 << '\n';
    std::cout << "Values: " << b4.to_ulong() << ' ' << b8.to_ulong() << "\n\n";    

    b4 = ~b4; // flip b4 to 1011
    b8 = ~b8; // flip b8 to 1111 1011
    
    std::cout << "After bitwise NOT:\n";
    std::cout << "Bits: " << b4 << ' ' << b8 << '\n';
    std::cout << "Values: " << b4.to_ulong() << ' ' << b8.to_ulong() << '\n';    

    return 0;
}
这会打印
Initial values:
Bits: 0100 00000100
Values: 4 4

After bitwise NOT:
Bits: 1011 11111011
Values: 11 251
最初，
b4
和
b8
都设置为
0b100
。当用前导零填充时，
b4
最终变为
0100
，
b8
变为
00000100
，这将在下一行打印。
然后我们使用
to_ulong()
成员函数将位的​​值解释为
long
整数。您可以看到
b4
和
b8
都打印值
4
。尽管位数不同，它们都表示相同的值。这是因为前导零位对解释的整数没有贡献。
然后我们使用按位非来翻转每个位的​​位，所以
b4
现在有位
1011
，
b8
现在有位
1111 1011
。当作为整数打印时，这会打印值
11
和
251
。如您所见，这些值不再相同。这是因为前导一确实对解释的整数有贡献，并且
b8
比
b4
有更多的前导一。
按位或
按位或
(|) 的工作方式与逻辑或类似。如果您还记得，如果两个
操作数
中任一为
true
，逻辑或将计算结果为
true
(
1
)，否则计算结果为
false
(
0
)。
但是，逻辑或应用于整个操作数（以产生单个真或假结果），而按位或应用于操作数中的每一对位（为每个位产生单个真或假结果）。
让我们用一个例子来说明这一点。考虑表达式
0b0101 | 0b0110
。
提示
要手动执行任何二进制位运算，最简单的方法是将两个操作数像这样对齐
0 1 0 1 OR (or whatever bitwise operation you are doing)
0 1 1 0
然后，将操作应用于每个位
列
，并将结果写在下面。
在第一列中，
0
或
0
是
0
，所以我们在线下面放一个 0。
0 1 0 1 OR
0 1 1 0
-------
0
第二列，
1
或
1
是
1
。第三列
0
或
1
是
1
。第四列，
1
或
0
是
1
。
0 1 0 1 OR
0 1 1 0
-------
0 1 1 1
我们的结果是二进制
0111
。
#include <bitset>
#include <iostream>

int main()
{
	std::cout << (std::bitset<4>{ 0b0101 } | std::bitset<4>{ 0b0110 }) << '\n';

	return 0;
}
这会打印
0111
我们可以对复合按位或表达式做同样的事情，例如
0b0111 | 0b0011 | 0b0001
。如果一列中的任何位是
1
，则该列的结果是
1
0 1 1 1 OR
0 0 1 1 OR
0 0 0 1
--------
0 1 1 1
这是上面的代码
#include <bitset>
#include <iostream>

int main()
{
	std::cout << (std::bitset<4>{ 0b0111 } | std::bitset<4>{ 0b0011 } | std::bitset<4>{ 0b0001 }) << '\n';

	return 0;
}
这会打印
0111
按位与
按位与
(&) 的工作方式与上面类似，只是它使用 AND 逻辑而不是 OR 逻辑。也就是说，对于操作数中的每一对位，按位与将结果位设置为
true
(
1
)，如果两个配对位都为
1
，否则设置为
false
(
0
)。
考虑表达式
0b0101 & 0b0110
。将每个位对齐并将按位与应用于每一列位
0 1 0 1 AND
0 1 1 0
--------
0 1 0 0
#include <bitset>
#include <iostream>

int main()
{
	std::cout << (std::bitset<4>{ 0b0101 } & std::bitset<4>{ 0b0110 }) << '\n';

	return 0;
}
这会打印
0100
同样，我们可以对复合按位与表达式做同样的事情，例如
0b0001 & 0b0011 & 0b0111
。如果一列中的所有位都为
1
，则该列的结果为
1
。
0 0 0 1 AND
0 0 1 1 AND
0 1 1 1
--------
0 0 0 1
#include <bitset>
#include <iostream>

int main()
{
	std::cout << (std::bitset<4>{ 0b0001 } & std::bitset<4>{ 0b0011 } & std::bitset<4>{ 0b0111 }) << '\n';

	return 0;
}
这会打印
0001
按位异或
最后一个运算符是
按位异或
(^)，也称为
异或
。
对于操作数中的每一对位，按位异或在配对位中恰好有一个为
1
时将结果位设置为
true
(
1
)，否则设置为
false
(
0
)。换句话说，当配对位不同（一个为
0
另一个为
1
）时，按位异或将结果位设置为
true
。
考虑表达式
0b0110 ^ 0b0011
0 1 1 0 XOR
0 0 1 1
-------
0 1 0 1
也可以按列样式评估复合 XOR 表达式，例如
0b0001 ^ 0b0011 ^ 0b0111
。如果一列中有偶数个
1
位，则结果为
0
。如果一列中有奇数个
1
位，则结果为
1
。
0 0 0 1 XOR
0 0 1 1 XOR
0 1 1 1
--------
0 1 0 1
按位赋值运算符
与算术赋值运算符类似，C++ 提供了按位赋值运算符。这些运算符会修改左操作数。
运算符
符号
形式
该操作修改左操作数，其中
左移
<<
x <<= n
x
中的位向左移动
n
位，新位为
0
。
右移
>>
x >>= n
x
中的位向右移动
n
位，新位为
0
。
按位与
&
x &= y
当
x
和
y
中相应的位都为
1
时，每个位都设置为
1
。
按位或
|
x |= y
当
x
和
y
中相应的位有一个为
1
时，每个位都设置为
1
。
按位异或
^
x ^= y
当
x
和
y
中相应的位不同时，每个位都设置为
1
。
例如，您可以写
x >>= 1;
而不是写
x = x >> 1;
。
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<4> bits { 0b0100 };
    bits >>= 1;
    std::cout << bits << '\n';

    return 0;
}
这个程序打印
0010
题外话…
没有按位非赋值运算符。这是因为其他位运算符是二元运算符，而按位非是一元运算符（那么
~=
运算符的右侧会是什么？）。如果要翻转对象的所有位，可以使用普通赋值：
x = ~x;
位运算符对较小的整数类型执行整数提升
高级
如果位运算符的操作数是小于
int
的整数类型，则这些操作数将被提升（转换）为
int
或
unsigned int
，并且返回的结果也将是
int
或
unsigned int
。例如，如果我们的操作数是
unsigned short
，它们将被提升（转换）为
unsigned int
，并且操作的结果将作为
unsigned int
返回。
在许多情况下，这无关紧要。
相关内容
我们在课程
10.2 -- 浮点和整数提升
中介绍了整数提升。
但是，当对窄于
int
或
unsigned int
的整数类型使用位运算符时，有两种情况需要注意
operator~
和
operator<<
对宽度敏感，并且可能根据操作数的宽度产生不同的结果。
将结果初始化或赋值给较小整数类型的变量是一种窄化转换（因为将
int
或
unsigned int
转换为较小的整数类型可能导致数据丢失）。这在列表初始化中是不允许的，并且您的编译器可能会或可能不会抱怨窄化赋值。
以下程序展示了这些问题（假设是 32 位 int）
#include <bitset>
#include <cstdint>
#include <iostream>

int main()
{
    std::uint8_t c { 0b00001111 };
    
    std::cout << std::bitset<32>(~c) << '\n';     // incorrect: prints 11111111111111111111111111110000
    std::cout << std::bitset<32>(c << 6) << '\n'; // incorrect: prints 0000000000000000001111000000
    std::uint8_t cneg { ~c };                     // error: narrowing conversion from unsigned int to std::uint8_t
    c = ~c;                                       // possible warning: narrowing conversion from unsigned int to std::uint8_t
 
    return 0;
}
这些问题可以通过使用
static_cast
将位运算的结果转换回较窄的整数类型来解决。以下程序产生正确的结果
#include <bitset>
#include <cstdint>
#include <iostream>

int main()
{
    std::uint8_t c { 0b00001111 };

    std::cout << std::bitset<32>(static_cast<std::uint8_t>(~c)) << '\n';     // correct: prints 00000000000000000000000011110000
    std::cout << std::bitset<32>(static_cast<std::uint8_t>(c << 6)) << '\n'; // correct: prints 0000000000000000000011000000
    std::uint8_t cneg { static_cast<std::uint8_t>(~c) };                     // compiles
    c = static_cast<std::uint8_t>(~c);                                       // no warning
 
    return 0;
}
警告
位运算符会将具有较窄整数类型的操作数提升为
int
或
unsigned int
。
operator~
和
operator<<
对宽度敏感，并且可能根据操作数的宽度产生不同的结果。在使用此类位运算的结果之前，请将其
static_cast
回较窄的整数类型，以确保结果正确。
最佳实践
尽可能避免对小于
int
的整数类型进行位移。
总结
总结如何利用列方法评估位运算
当评估按位或时，如果一列中的任何位为 1，则该列的结果为 1。
当评估按位与时，如果一列中的所有位都为 1，则该列的结果为 1。
当评估按位异或时，如果一列中有奇数个 1 位，则该列的结果为 1。
在下一课中，我们将探讨如何将这些运算符与位掩码结合使用以促进位操作。
小测验时间
问题 #1
a) 0110 >> 2 在二进制中计算结果是什么？
显示答案
0110 >> 2 计算结果为 0001
b) 以下在二进制中计算结果是什么：0011 | 0101？
显示答案
0 0 1 1 OR
0 1 0 1
--------
0 1 1 1
c) 以下在二进制中计算结果是什么：0011 & 0101？
显示答案
0 0 1 1 AND
0 1 0 1
--------
0 0 0 1
d) 以下在二进制中计算结果是什么 (0011 | 0101) & 1001？
显示答案
Inside the parenthesis:

0 0 1 1 OR
0 1 0 1
--------
0 1 1 1

Then:

0 1 1 1 AND
1 0 0 1
--------
0 0 0 1
问题 #2
位旋转类似于位移，只是任何从一端移出的位都会添加到另一端。例如
0b1001 << 1
将是
0b0010
，但左旋 1 位将导致
0b0011
。实现一个函数，对
std::bitset<4>
进行左旋。对于这个，可以使用 test() 和 set()。
以下代码应执行
#include <bitset>
#include <iostream>

// "rotl" stands for "rotate left"
std::bitset<4> rotl(std::bitset<4> bits)
{
// Your code here
}

int main()
{
	std::bitset<4> bits1{ 0b0001 };
	std::cout << rotl(bits1) << '\n';

	std::bitset<4> bits2{ 0b1001 };
	std::cout << rotl(bits2) << '\n';

	return 0;
}
并打印以下内容
0010
0011
显示答案
#include <bitset>
#include <iostream>

std::bitset<4> rotl(std::bitset<4> bits)
{
	// keep track of whether the leftmost bit was a 1
	const bool leftbit{ bits.test(3) };

	bits <<= 1; // do left shift (which shifts the leftmost bit off the end)

	// if the left bit was a 1
	if (leftbit)
		bits.set(0); // set the rightmost bit to a 1

	return bits;
}

int main()
{
	std::bitset<4> bits1{ 0b0001 };
	std::cout << rotl(bits1) << '\n';

	std::bitset<4> bits2{ 0b1001 };
	std::cout << rotl(bits2) << '\n';

	return 0;
}
我们将函数命名为“rotl”而不是“rotateLeft”，因为“rotl”是计算机科学中一个成熟的名称，也是标准函数
std::rotl
的名称。
问题 #3
额外加分：重做测验 #2，但不要使用 test 和 set 函数（使用位运算符）。
显示提示
提示：我们如何将最左边的位移到最右边的位置？
显示提示
提示：考虑您的“视角”的“转变”
显示答案
#include <bitset>
#include <iostream>

// h/t to reader Chris for this solution
std::bitset<4> rotl(std::bitset<4> bits)
{
	// bits << 1 does the left shift
	// bits >> 3 handle the rotation of the leftmost bit
	return (bits<<1) | (bits>>3);
}

int main()
{
	std::bitset<4> bits1{ 0b0001 };
	std::cout << rotl(bits1) << '\n';

	std::bitset<4> bits2{ 0b1001 };
	std::cout << rotl(bits2) << '\n';

	return 0;
}
下一课
O.3
使用位运算符和位掩码进行位操作
返回目录
上一课
O.1
位标志和通过 std::bitset 进行位操作