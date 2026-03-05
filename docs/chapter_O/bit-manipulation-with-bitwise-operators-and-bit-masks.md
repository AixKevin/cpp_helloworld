# O.3 — 使用按位运算符和位掩码进行位操作

O.3 — 使用按位运算符和位掩码进行位操作
Alex
2015年9月8日，太平洋夏令时晚上9:12
2024年7月21日
在上一节关于按位运算符的课程中（
O.2 -- 按位运算符
），我们讨论了各种按位运算符如何将逻辑运算符应用于操作数中的每个位。既然我们已经了解了它们的功能，现在让我们看看它们更常见的用法。
位掩码
为了操作单个位（例如，将它们打开或关闭），我们需要某种方式来识别我们想要操作的特定位。不幸的是，按位运算符不知道如何处理位位置。相反，它们使用位掩码。
位掩码
是预定义的一组位，用于选择后续操作将修改哪些特定位。
考虑一个现实生活中的例子：你想粉刷窗框。如果你不小心，你可能会不仅粉刷了窗框，还会粉刷到玻璃本身。你可能会买一些遮蔽胶带，把它贴在玻璃和任何其他你不想粉刷的部分。然后当你粉刷时，遮蔽胶带会阻止油漆接触到任何你不想粉刷的部分。最终，只有未遮蔽的部分（你想粉刷的部分）会被粉刷。
位掩码对位执行相同的功能——位掩码阻止按位运算符接触我们不想修改的位，并允许访问我们确实想修改的位。
让我们首先探讨如何定义一些简单的位掩码，然后我们将向您展示如何使用它们。
在 C++14 中定义位掩码
最简单的一组位掩码是为每个位位置定义一个位掩码。我们使用 0 来遮蔽我们不关心的位，使用 1 来表示我们想要修改的位。
尽管位掩码可以是字面量，但它们通常被定义为符号常量，以便可以给它们一个有意义的名称并轻松重用。
因为 C++14 支持二进制字面量，所以定义这些位掩码很容易
#include <cstdint>

constexpr std::uint8_t mask0{ 0b0000'0001 }; // represents bit 0
constexpr std::uint8_t mask1{ 0b0000'0010 }; // represents bit 1
constexpr std::uint8_t mask2{ 0b0000'0100 }; // represents bit 2 
constexpr std::uint8_t mask3{ 0b0000'1000 }; // represents bit 3
constexpr std::uint8_t mask4{ 0b0001'0000 }; // represents bit 4
constexpr std::uint8_t mask5{ 0b0010'0000 }; // represents bit 5
constexpr std::uint8_t mask6{ 0b0100'0000 }; // represents bit 6
constexpr std::uint8_t mask7{ 0b1000'0000 }; // represents bit 7
现在我们有了一组表示每个位位置的符号常量。我们可以使用它们来操作位（我们稍后将展示如何操作）。
在 C++11 或更早版本中定义位掩码
由于 C++11 不支持二进制字面量，我们必须使用其他方法来设置符号常量。有两种好的方法可以做到这一点。
第一种方法是使用十六进制字面量。
相关内容
我们在
5.2 -- 字面量
课中讨论十六进制。
以下是十六进制如何转换为二进制的示例
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
因此，我们可以使用十六进制定义位掩码，如下所示
constexpr std::uint8_t mask0{ 0x01 }; // hex for 0000 0001
constexpr std::uint8_t mask1{ 0x02 }; // hex for 0000 0010
constexpr std::uint8_t mask2{ 0x04 }; // hex for 0000 0100
constexpr std::uint8_t mask3{ 0x08 }; // hex for 0000 1000
constexpr std::uint8_t mask4{ 0x10 }; // hex for 0001 0000
constexpr std::uint8_t mask5{ 0x20 }; // hex for 0010 0000
constexpr std::uint8_t mask6{ 0x40 }; // hex for 0100 0000
constexpr std::uint8_t mask7{ 0x80 }; // hex for 1000 0000
有时会省略前导十六进制 0（例如，您只会看到
0x1
而不是
0x01
）。无论哪种方式，如果您不熟悉十六进制到二进制的转换，这可能有点难以阅读。
一种更简单的方法是使用左移运算符将单个位移入正确的位置
constexpr std::uint8_t mask0{ 1 << 0 }; // 0000 0001 
constexpr std::uint8_t mask1{ 1 << 1 }; // 0000 0010
constexpr std::uint8_t mask2{ 1 << 2 }; // 0000 0100
constexpr std::uint8_t mask3{ 1 << 3 }; // 0000 1000
constexpr std::uint8_t mask4{ 1 << 4 }; // 0001 0000
constexpr std::uint8_t mask5{ 1 << 5 }; // 0010 0000
constexpr std::uint8_t mask6{ 1 << 6 }; // 0100 0000
constexpr std::uint8_t mask7{ 1 << 7 }; // 1000 0000
测试位（查看它是打开还是关闭）
现在我们有了一组位掩码，我们可以将它们与位标志变量结合使用来操作我们的位标志。
要确定一个位是打开还是关闭，我们使用
按位与
结合相应位的位掩码
#include <cstdint>
#include <iostream>

int main()
{
	[[maybe_unused]] constexpr std::uint8_t mask0{ 0b0000'0001 }; // represents bit 0
	[[maybe_unused]] constexpr std::uint8_t mask1{ 0b0000'0010 }; // represents bit 1
	[[maybe_unused]] constexpr std::uint8_t mask2{ 0b0000'0100 }; // represents bit 2 
	[[maybe_unused]] constexpr std::uint8_t mask3{ 0b0000'1000 }; // represents bit 3
	[[maybe_unused]] constexpr std::uint8_t mask4{ 0b0001'0000 }; // represents bit 4
	[[maybe_unused]] constexpr std::uint8_t mask5{ 0b0010'0000 }; // represents bit 5
	[[maybe_unused]] constexpr std::uint8_t mask6{ 0b0100'0000 }; // represents bit 6
	[[maybe_unused]] constexpr std::uint8_t mask7{ 0b1000'0000 }; // represents bit 7

	std::uint8_t flags{ 0b0000'0101 }; // 8 bits in size means room for 8 flags

	std::cout << "bit 0 is " << (static_cast<bool>(flags & mask0) ? "on\n" : "off\n");
	std::cout << "bit 1 is " << (static_cast<bool>(flags & mask1) ? "on\n" : "off\n");

	return 0;
}
这会打印
bit 0 is on
bit 1 is off
让我们检查一下它是如何工作的。
在
flags & mask0
的情况下，我们有
0000'0101
&
0000'0001
。让我们将它们对齐
0000'0101 &
0000'0001
---------
0000'0001
然后我们将
0000'0001
转换为
bool
。由于任何非零数字都转换为
true
，并且此值具有非零数字，因此它评估为
true
。
在
flags & mask1
的情况下，我们有
0000'0101
&
0000'0010
。让我们将它们对齐
0000'0101 &
0000'0010
---------
0000'0000
由于零值转换为
false
，并且此值只有零数字，因此它评估为
false
。
设置位
要设置（打开）一个位（到值 1），我们使用按位或等于运算符（|=）结合相应位的位掩码
#include <cstdint>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr std::uint8_t mask0{ 0b0000'0001 }; // represents bit 0
    [[maybe_unused]] constexpr std::uint8_t mask1{ 0b0000'0010 }; // represents bit 1
    [[maybe_unused]] constexpr std::uint8_t mask2{ 0b0000'0100 }; // represents bit 2 
    [[maybe_unused]] constexpr std::uint8_t mask3{ 0b0000'1000 }; // represents bit 3
    [[maybe_unused]] constexpr std::uint8_t mask4{ 0b0001'0000 }; // represents bit 4
    [[maybe_unused]] constexpr std::uint8_t mask5{ 0b0010'0000 }; // represents bit 5
    [[maybe_unused]] constexpr std::uint8_t mask6{ 0b0100'0000 }; // represents bit 6
    [[maybe_unused]] constexpr std::uint8_t mask7{ 0b1000'0000 }; // represents bit 7
    
    std::uint8_t flags{ 0b0000'0101 }; // 8 bits in size means room for 8 flags

    std::cout << "bit 1 is " << (static_cast<bool>(flags & mask1) ? "on\n" : "off\n");

    flags |= mask1; // turn on bit 1

    std::cout << "bit 1 is " << (static_cast<bool>(flags & mask1) ? "on\n" : "off\n");

    return 0;
}
这会打印
bit 1 is off
bit 1 is on
我们还可以使用
按位或
同时打开多个位
flags |= (mask4 | mask5); // turn bits 4 and 5 on at the same time
重置位
要重置（清除）一个位（到值 0），我们同时使用
按位与
和
按位非
#include <cstdint>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr std::uint8_t mask0{ 0b0000'0001 }; // represents bit 0
    [[maybe_unused]] constexpr std::uint8_t mask1{ 0b0000'0010 }; // represents bit 1
    [[maybe_unused]] constexpr std::uint8_t mask2{ 0b0000'0100 }; // represents bit 2 
    [[maybe_unused]] constexpr std::uint8_t mask3{ 0b0000'1000 }; // represents bit 3
    [[maybe_unused]] constexpr std::uint8_t mask4{ 0b0001'0000 }; // represents bit 4
    [[maybe_unused]] constexpr std::uint8_t mask5{ 0b0010'0000 }; // represents bit 5
    [[maybe_unused]] constexpr std::uint8_t mask6{ 0b0100'0000 }; // represents bit 6
    [[maybe_unused]] constexpr std::uint8_t mask7{ 0b1000'0000 }; // represents bit 7
    
    std::uint8_t flags{ 0b0000'0101 }; // 8 bits in size means room for 8 flags

    std::cout << "bit 2 is " << (static_cast<bool>(flags & mask2) ? "on\n" : "off\n");

    flags &= ~mask2; // turn off bit 2

    std::cout << "bit 2 is " << (static_cast<bool>(flags & mask2) ? "on\n" : "off\n");

    return 0;
}
这会打印
bit 2 is on
bit 2 is off
我们可以同时关闭多个位
flags &= ~(mask4 | mask5); // turn bits 4 and 5 off at the same time
关键见解
一些编译器可能会抱怨此行的符号转换
flags &= ~mask2;
因为
mask2
的类型小于
int
，所以
operator~
导致操作数
mask2
进行整型提升到
int
类型。然后编译器会抱怨我们试图使用
operator&=
，其中左操作数是无符号的，右操作数是有符号的。
如果是这种情况，请尝试以下方法
flags &= static_cast<std::uint8_t>(~mask2);
我们在
O.2 -- 按位运算符
课程中讨论了这个问题。
翻转位
要切换（翻转）位状态（从 0 到 1 或从 1 到 0），我们使用
按位异或
#include <cstdint>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr std::uint8_t mask0{ 0b0000'0001 }; // represents bit 0
    [[maybe_unused]] constexpr std::uint8_t mask1{ 0b0000'0010 }; // represents bit 1
    [[maybe_unused]] constexpr std::uint8_t mask2{ 0b0000'0100 }; // represents bit 2 
    [[maybe_unused]] constexpr std::uint8_t mask3{ 0b0000'1000 }; // represents bit 3
    [[maybe_unused]] constexpr std::uint8_t mask4{ 0b0001'0000 }; // represents bit 4
    [[maybe_unused]] constexpr std::uint8_t mask5{ 0b0010'0000 }; // represents bit 5
    [[maybe_unused]] constexpr std::uint8_t mask6{ 0b0100'0000 }; // represents bit 6
    [[maybe_unused]] constexpr std::uint8_t mask7{ 0b1000'0000 }; // represents bit 7

    std::uint8_t flags{ 0b0000'0101 }; // 8 bits in size means room for 8 flags

    std::cout << "bit 2 is " << (static_cast<bool>(flags & mask2) ? "on\n" : "off\n");
    flags ^= mask2; // flip bit 2
    std::cout << "bit 2 is " << (static_cast<bool>(flags & mask2) ? "on\n" : "off\n");
    flags ^= mask2; // flip bit 2
    std::cout << "bit 2 is " << (static_cast<bool>(flags & mask2) ? "on\n" : "off\n");

    return 0;
}
这会打印
bit 2 is on
bit 2 is off
bit 2 is on
我们可以同时翻转多个位
flags ^= (mask4 | mask5); // flip bits 4 and 5 at the same time
位掩码和 std::bitset
std::bitset 支持完整的按位运算符集。因此，尽管使用函数（test、set、reset 和 flip）修改单个位更容易，但如果您愿意，可以使用按位运算符和位掩码。
你为什么要这么做？这些函数只允许你修改单个位。按位运算符允许你一次修改多个位。
#include <bitset>
#include <iostream>

int main()
{
	[[maybe_unused]] constexpr std::bitset<8> mask0{ 0b0000'0001 }; // represents bit 0
	[[maybe_unused]] constexpr std::bitset<8> mask1{ 0b0000'0010 }; // represents bit 1
	[[maybe_unused]] constexpr std::bitset<8> mask2{ 0b0000'0100 }; // represents bit 2 
	[[maybe_unused]] constexpr std::bitset<8> mask3{ 0b0000'1000 }; // represents bit 3
	[[maybe_unused]] constexpr std::bitset<8> mask4{ 0b0001'0000 }; // represents bit 4
	[[maybe_unused]] constexpr std::bitset<8> mask5{ 0b0010'0000 }; // represents bit 5
	[[maybe_unused]] constexpr std::bitset<8> mask6{ 0b0100'0000 }; // represents bit 6
	[[maybe_unused]] constexpr std::bitset<8> mask7{ 0b1000'0000 }; // represents bit 7

	std::bitset<8> flags{ 0b0000'0101 }; // 8 bits in size means room for 8 flags
	std::cout << "bit 1 is " << (flags.test(1) ? "on\n" : "off\n");
	std::cout << "bit 2 is " << (flags.test(2) ? "on\n" : "off\n");

	flags ^= (mask1 | mask2); // flip bits 1 and 2
	std::cout << "bit 1 is " << (flags.test(1) ? "on\n" : "off\n");
	std::cout << "bit 2 is " << (flags.test(2) ? "on\n" : "off\n");

	flags |= (mask1 | mask2); // turn bits 1 and 2 on
	std::cout << "bit 1 is " << (flags.test(1) ? "on\n" : "off\n");
	std::cout << "bit 2 is " << (flags.test(2) ? "on\n" : "off\n");

	flags &= ~(mask1 | mask2); // turn bits 1 and 2 off
	std::cout << "bit 1 is " << (flags.test(1) ? "on\n" : "off\n");
	std::cout << "bit 2 is " << (flags.test(2) ? "on\n" : "off\n");

	return 0;
}
这会打印
bit 1 is off
bit 2 is on
bit 1 is on
bit 2 is off
bit 1 is on
bit 2 is on
bit 1 is off
bit 2 is off
使位掩码有意义
将我们的位掩码命名为“mask1”或“mask2”告诉我们正在操作哪个位，但没有告诉我们该位标志实际用于什么。
最佳实践是给你的位掩码起有用的名称，以此来记录位标志的含义。这是一个我们可能编写的游戏示例
#include <cstdint>
#include <iostream>

int main()
{
        // Define a bunch of physical/emotional states
	[[maybe_unused]] constexpr std::uint8_t isHungry   { 1 << 0 }; // 0000 0001
	[[maybe_unused]] constexpr std::uint8_t isSad      { 1 << 1 }; // 0000 0010
	[[maybe_unused]] constexpr std::uint8_t isMad      { 1 << 2 }; // 0000 0100
	[[maybe_unused]] constexpr std::uint8_t isHappy    { 1 << 3 }; // 0000 1000
	[[maybe_unused]] constexpr std::uint8_t isLaughing { 1 << 4 }; // 0001 0000
	[[maybe_unused]] constexpr std::uint8_t isAsleep   { 1 << 5 }; // 0010 0000
	[[maybe_unused]] constexpr std::uint8_t isDead     { 1 << 6 }; // 0100 0000
	[[maybe_unused]] constexpr std::uint8_t isCrying   { 1 << 7 }; // 1000 0000

	std::uint8_t me{}; // all flags/options turned off to start
	me |= (isHappy | isLaughing); // I am happy and laughing
	me &= ~isLaughing; // I am no longer laughing

	// Query a few states
	// (we'll use static_cast<bool> to interpret the results as a boolean value)
	std::cout << std::boolalpha; // print true or false instead of 1 or 0
	std::cout << "I am happy? " << static_cast<bool>(me & isHappy) << '\n';
	std::cout << "I am laughing? " << static_cast<bool>(me & isLaughing) << '\n';

	return 0;
}
以下是使用 std::bitset 实现的相同示例
#include <bitset>
#include <iostream>

int main()
{
        // Define a bunch of physical/emotional states
	[[maybe_unused]] constexpr std::bitset<8> isHungry   { 0b0000'0001 };
	[[maybe_unused]] constexpr std::bitset<8> isSad      { 0b0000'0010 };
	[[maybe_unused]] constexpr std::bitset<8> isMad      { 0b0000'0100 };
	[[maybe_unused]] constexpr std::bitset<8> isHappy    { 0b0000'1000 };
	[[maybe_unused]] constexpr std::bitset<8> isLaughing { 0b0001'0000 };
	[[maybe_unused]] constexpr std::bitset<8> isAsleep   { 0b0010'0000 };
	[[maybe_unused]] constexpr std::bitset<8> isDead     { 0b0100'0000 };
	[[maybe_unused]] constexpr std::bitset<8> isCrying   { 0b1000'0000 };


	std::bitset<8> me{}; // all flags/options turned off to start
	me |= (isHappy | isLaughing); // I am happy and laughing
	me &= ~isLaughing; // I am no longer laughing

	// Query a few states (we use the any() function to see if any bits remain set)
	std::cout << std::boolalpha; // print true or false instead of 1 or 0
	std::cout << "I am happy? " << (me & isHappy).any() << '\n';
	std::cout << "I am laughing? " << (me & isLaughing).any() << '\n';

	return 0;
}
这里有两点需要注意：首先，std::bitset 没有一个很好的函数允许你使用位掩码查询位。因此，如果你想使用位掩码而不是位置索引，你将不得不使用
按位与
来查询位。其次，我们使用了 any() 函数，如果设置了任何位，它返回 true，否则返回 false，以查看我们查询的位是保持打开还是关闭。
位标志何时最有用？
敏锐的读者可能会注意到，上面的例子实际上并没有节省任何内存。8 个独立的布尔值通常需要 8 字节。但上面的例子（使用 std::uint8_t）使用了 9 字节——8 字节用于定义位掩码，1 字节用于标志变量！
当你有很多相同的标志变量时，位标志最有意义。例如，在上面的例子中，想象一下，你不是只有一个人（我），而是有 100 个人。如果你每人使用 8 个布尔值（每个可能状态一个），你将使用 800 字节的内存。使用位标志，你将使用 8 字节用于位掩码，100 字节用于位标志变量，总共 108 字节的内存——大约减少了 8 倍的内存。
对于大多数程序，使用位标志节省的内存不值得增加的复杂性。但在有数万甚至数百万相似对象的程序中，使用位标志可以大幅减少内存使用。如果需要，它是一个有用的优化工具。
还有另一种情况，位标志和位掩码可能是有意义的。想象一下你有一个函数，可以接受 32 种不同选项的任意组合。编写该函数的一种方法是使用 32 个独立的布尔参数
void someFunction(bool option1, bool option2, bool option3, bool option4, bool option5, bool option6, bool option7, bool option8, bool option9, bool option10, bool option11, bool option12, bool option13, bool option14, bool option15, bool option16, bool option17, bool option18, bool option19, bool option20, bool option21, bool option22, bool option23, bool option24, bool option25, bool option26, bool option27, bool option28, bool option29, bool option30, bool option31, bool option32);
希望你会给你的参数起更具描述性的名字，但这里的重点是向你展示参数列表有多么令人讨厌地长。
然后当你想要调用函数并将选项 10 和 32 设置为 true 时，你必须这样做
someFunction(false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true);
这非常难以阅读（是选项 9、10 还是 11 设置为 true？），也意味着你必须记住哪个参数对应哪个选项（设置“编辑标志”是第 9、10 还是 11 个参数？）。
相反，如果你像这样定义函数，使用位标志
void someFunction(std::bitset<32> options);
那么你就可以使用位标志只传入你想要的选项
someFunction(option10 | option32);
这更具可读性。
这是 OpenGL（一个备受推崇的 3D 图形库）选择使用位标志参数而不是许多连续布尔参数的原因之一。
这是 OpenGL 的一个示例函数调用
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // clear the color and the depth buffer
GL_COLOR_BUFFER_BIT 和 GL_DEPTH_BUFFER_BIT 是在 gl2.h 中定义的位掩码，如下所示
#define GL_DEPTH_BUFFER_BIT               0x00000100
#define GL_STENCIL_BUFFER_BIT             0x00000400
#define GL_COLOR_BUFFER_BIT               0x00004000
涉及多个位的位掩码
尽管位掩码通常用于选择单个位，但它们也可以用于选择多个位。让我们看一个稍微复杂一点的例子。
电视和显示器等彩色显示设备由数百万个像素组成，每个像素都可以显示一个颜色点。每个颜色点都是结合三种光束（红、绿、蓝 (RGB)）的结果。这些光的强度变化会产生不同的颜色。
通常，给定像素的 R、G 和 B 强度由一个 8 位无符号整数表示。例如，红色像素的 R=255，G=0，B=0。紫色像素的 R=255，G=0，B=255。中灰色像素的 R=127，G=127，B=127。
在为像素分配颜色值时，除了 R、G 和 B 之外，通常还会使用第四个值 A。“A”代表“alpha”，它控制颜色的透明度。如果 A=0，颜色完全透明。如果 A=255，颜色不透明。
R、G、B 和 A 通常存储为单个 32 位整数，每个分量使用 8 位
32 位 RGBA 值
位 31-24
位 23-16
位 15-8
位 7-0
RRRRRRRR
GGGGGGGG
BBBBBBBB
AAAAAAAA
红色
绿色
蓝色
alpha
以下程序要求用户输入一个 32 位十六进制值，然后提取 R、G、B 和 A 的 8 位颜色值。
#include <cstdint>
#include <iostream>

int main()
{
	constexpr std::uint32_t redBits{ 0xFF000000 };
	constexpr std::uint32_t greenBits{ 0x00FF0000 };
	constexpr std::uint32_t blueBits{ 0x0000FF00 };
	constexpr std::uint32_t alphaBits{ 0x000000FF };

	std::cout << "Enter a 32-bit RGBA color value in hexadecimal (e.g. FF7F3300): ";
	std::uint32_t pixel{};
	std::cin >> std::hex >> pixel; // std::hex allows us to read in a hex value

	// use Bitwise AND to isolate the pixels for our given color,
	// then right shift the value into the lower 8 bits
	const std::uint8_t red{ static_cast<std::uint8_t>((pixel & redBits) >> 24) };
	const std::uint8_t green{ static_cast<std::uint8_t>((pixel & greenBits) >> 16) };
	const std::uint8_t blue{ static_cast<std::uint8_t>((pixel & blueBits) >> 8) };
	const std::uint8_t alpha{ static_cast<std::uint8_t>(pixel & alphaBits) };

	std::cout << "Your color contains:\n";
	std::cout << std::hex; // print the following values in hex

        // reminder: std::uint8_t will likely print as a char
        // we static_cast to int to ensure it prints as an integer
	std::cout << static_cast<int>(red)   << " red\n";
	std::cout << static_cast<int>(green) << " green\n";
	std::cout << static_cast<int>(blue)  << " blue\n";
	std::cout << static_cast<int>(alpha) << " alpha\n";

	return 0;
}
这会产生输出
Enter a 32-bit RGBA color value in hexadecimal (e.g. FF7F3300): FF7F3300
Your color contains:
ff red
7f green
33 blue
0 alpha
在上面的程序中，我们使用
按位与
查询我们感兴趣的 8 位集，然后我们将它们
右移
到一个 8 位值中，以便我们可以将它们作为十六进制值打印出来。
总结
总结如何设置、清除、切换和查询位标志
要查询位状态，我们使用
按位与
if (flags & option4) ... // if option4 is set, do something
要设置位（打开），我们使用
按位或
flags |= option4; // turn option 4 on.
flags |= (option4 | option5); // turn options 4 and 5 on.
要清除位（关闭），我们使用
按位与
和
按位非
flags &= ~option4; // turn option 4 off
flags &= ~(option4 | option5); // turn options 4 and 5 off
要翻转位状态，我们使用
按位异或
flags ^= option4; // flip option4 from on to off, or vice versa
flags ^= (option4 | option5); // flip options 4 and 5
小测验时间
问题 #1
本测验中请勿使用
std::bitset
。我们只使用
std::bitset
进行打印。
给定以下程序：
#include <bitset>
#include <cstdint>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr std::uint8_t option_viewed{ 0x01 };
    [[maybe_unused]] constexpr std::uint8_t option_edited{ 0x02 };
    [[maybe_unused]] constexpr std::uint8_t option_favorited{ 0x04 };
    [[maybe_unused]] constexpr std::uint8_t option_shared{ 0x08 };
    [[maybe_unused]] constexpr std::uint8_t option_deleted{ 0x10 };

    std::uint8_t myArticleFlags{ option_favorited };

    // Place all lines of code for the following quiz here

    std::cout << std::bitset<8>{ myArticleFlags } << '\n';

    return 0;
}
a) 添加一行代码，将文章标记为已查看。
预期输出
00000101
显示答案
myArticleFlags |= option_viewed;
b) 添加一行代码，检查文章是否已删除。
显示答案
if (myArticleFlags & option_deleted) ...
c) 添加一行代码，将文章从收藏中清除。
预期输出（假设您完成了测验 (a)）
00000001
显示答案
myArticleFlags &= static_cast<std::uint8_t>(~option_favorited);
如果您得到
00000000
，请检查两件事
测验 (a) 的解决方案没有被删除。
您清除了
option_favorited
，而不是
option_viewed
。
1d) 额外加分：为什么以下两行是相同的？
myflags &= ~(option4 | option5); // turn options 4 and 5 off
myflags &= ~option4 & ~option5; // turn options 4 and 5 off
显示答案
德摩根定律指出，如果我们分布一个 NOT，我们需要将 OR 和 AND 翻转到另一个。所以
~(option4 | option5)
变为
~option4 & ~option5
。
下一课
O.4
在二进制和十进制表示之间转换整数
返回目录
上一课
O.2
按位运算符