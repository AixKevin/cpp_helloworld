# 8.14 — 使用 Mersenne Twister 生成随机数

8.14 — 使用 Mersenne Twister 生成随机数
Alex
2008 年 12 月 7 日，太平洋标准时间下午 2:43
2025 年 2 月 2 日
在上一课
8.13 -- 随机数生成简介
中，我们介绍了随机数生成的概念，并讨论了 PRNG 算法通常如何用于在程序中模拟随机性。
在本课中，我们将探讨如何在程序中生成随机数。要访问 C++ 中的任何随机化功能，我们需要包含标准库的
<random>
头文件。
使用 Mersenne Twister 在 C++ 中生成随机数
Mersenne Twister PRNG 除了有一个很棒的名字外，可能是所有编程语言中最受欢迎的 PRNG。尽管按照今天的标准它有点旧，但它通常会产生高质量的结果并且性能良好。随机库支持两种 Mersenne Twister 类型
mt19937
是一个生成 32 位无符号整数的 Mersenne Twister
mt19937_64
是一个生成 64 位无符号整数的 Mersenne Twister
使用 Mersenne Twister 非常简单
#include <iostream>
#include <random> // for std::mt19937

int main()
{
	std::mt19937 mt{}; // Instantiate a 32-bit Mersenne Twister

	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 40; ++count)
	{
		std::cout << mt() << '\t'; // generate a random number

		// If we've printed 5 numbers, start a new row
		if (count % 5 == 0)
			std::cout << '\n';
	}

	return 0;
}
这会产生结果
3499211612      581869302       3890346734      3586334585      545404204
4161255391      3922919429      949333985       2715962298      1323567403
418932835       2350294565      1196140740      809094426       2348838239
4264392720      4112460519      4279768804      4144164697      4156218106
676943009       3117454609      4168664243      4213834039      4111000746
471852626       2084672536      3427838553      3437178460      1275731771
609397212       20544909        1811450929      483031418       3933054126
2747762695      3402504553      3772830893      4120988587      2163214728
首先，我们包含
<random>
头文件，因为所有随机数功能都在那里。接下来，我们通过语句
std::mt19937 mt
实例化一个 32 位 Mersenne Twister 引擎。然后，每次我们想生成一个随机的 32 位无符号整数时，我们调用
mt()
。
题外话…
由于
mt
是一个变量，您可能想知道
mt()
是什么意思。
在课程
5.7 -- std::string 简介
中，我们展示了一个示例，其中我们调用了函数
name.length()
，该函数在
std::string
变量
name
上调用了
length()
函数。
mt()
是调用函数
mt.operator()
的简洁语法，对于这些 PRNG 类型，它被定义为返回序列中的下一个随机结果。使用
operator()
而不是命名函数的优点是，我们不需要记住函数的名称，并且简洁的语法可以减少输入量。
使用 Mersenne Twister 掷骰子
一个 32 位 PRNG 将生成 0 到 4,294,967,295 之间的随机数，但我们不总是需要该范围内的数字。如果我们的程序模拟棋盘游戏或骰子游戏，我们可能希望通过生成 1 到 6 之间的随机数来模拟掷一个 6 面骰子。如果我们的程序是一个地牢冒险游戏，并且玩家有一把对怪物造成 7 到 11 点伤害的剑，那么当玩家击中怪物时，我们希望生成 7 到 11 之间的随机数。
不幸的是，PRNG 无法做到这一点。它们只能生成使用完整范围的数字。我们需要某种方法将 PRNG 的输出数字转换为我们想要的较小范围内的值（每个值出现的概率均等）。虽然我们可以自己编写一个函数来做到这一点，但以一种产生无偏结果的方式这样做并非易事。
幸运的是，随机库可以通过随机数分布的形式帮助我们。**随机数分布**将 PRNG 的输出转换为其他数字分布。
题外话…
对于统计学爱好者：随机数分布只是旨在将 PRNG 值作为输入的概率分布。
随机库有许多随机数分布，其中大部分您除非进行某种统计分析，否则永远不会使用。但有一种随机数分布非常有用：**均匀分布**是一种随机数分布，它以相等的概率在两个数字 X 和 Y（包括）之间产生输出。
这是一个与上面类似的程序，使用均匀分布来模拟掷一个 6 面骰子
#include <iostream>
#include <random> // for std::mt19937 and std::uniform_int_distribution

int main()
{
	std::mt19937 mt{};

	// Create a reusable random number generator that generates uniform numbers between 1 and 6
	std::uniform_int_distribution die6{ 1, 6 }; // for C++14, use std::uniform_int_distribution<> die6{ 1, 6 };

	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 40; ++count)
	{
		std::cout << die6(mt) << '\t'; // generate a roll of the die here

		// If we've printed 10 numbers, start a new row
		if (count % 10 == 0)
			std::cout << '\n';
	}

	return 0;
}
这会产生结果
3       1       3       6       5       2       6       6       1       2
2       6       1       1       6       1       4       5       2       5
6       2       6       2       1       3       5       4       5       6
1       4       2       3       1       2       2       6       2       1
与前一个示例相比，此示例中只有两个值得注意的差异。首先，我们创建了一个均匀分布变量（名为
die6
）来生成 1 到 6 之间的数字。其次，我们现在调用
die6(mt)
来生成 1 到 6 之间的值，而不是调用
mt()
来生成 32 位无符号整数随机数。
上述程序没有看起来那么随机
尽管我们上面的掷骰子示例的结果相当随机，但该程序存在一个主要缺陷。运行程序 3 次，看看您能否找出是什么问题。去吧，我们等着。
《危险边缘》音乐
如果您多次运行该程序，您会注意到它每次都打印相同的数字！虽然序列中的每个数字相对于前一个数字都是随机的，但整个序列根本不是随机的！我们程序的每次运行都会产生完全相同的结果。
想象一下，您正在编写一个高低游戏，用户有 10 次机会猜测一个随机选择的数字，电脑会告诉用户他们的猜测是过高还是过低。如果电脑每次都选择相同的随机数，那么游戏在第一次玩之后就不会再有趣了。所以让我们深入研究一下为什么会发生这种情况，以及我们如何修复它。
在上一课（
8.13 -- 随机数生成简介
）中，我们讨论了 PRNG 序列中的每个数字都是以确定性方式生成的。并且 PRNG 的状态是从种子值初始化的。因此，给定任何起始种子数，PRNG 将始终从该种子生成相同的数字序列。
因为我们正在对 Mersenne Twister 进行值初始化，所以每次程序运行时它都会使用相同的种子进行初始化。由于种子相同，生成的随机数也相同。
为了使我们的整个序列在每次程序运行时都以不同的方式随机化，我们需要选择一个不是固定数字的种子。首先想到的答案可能是我们需要一个随机数作为我们的种子！这是一个好想法，但是如果我们需要一个随机数来生成随机数，那么我们就会陷入一个两难境地。事实证明，我们实际上不需要我们的种子是一个随机数——我们只需要选择一些在每次程序运行时都会变化的东西。然后我们可以使用我们的 PRNG 从该种子生成一个独特的伪随机数序列。
有两种常用方法可以做到这一点
使用系统时钟
使用系统的随机设备
使用系统时钟作为种子
每次运行程序时有什么不同？除非您设法在完全相同的时间点运行程序两次，否则答案是当前时间是不同的。因此，如果我们使用当前时间作为我们的种子值，那么我们的程序每次运行时都会产生一组不同的随机数。C 和 C++ 长期以来一直使用当前时间（使用
std::time()
函数）为 PRNG 播种，因此您可能会在许多现有代码中看到这一点。
幸运的是，C++ 有一个 chrono 库，其中包含我们可以用来生成种子值的各种时钟。为了最大程度地减少程序连续快速运行时两个时间值相同的可能性，我们希望使用变化尽可能快的时间度量。为此，我们将询问时钟自它能测量到的最早时间以来经过了多少时间。这个时间以“滴答”为单位测量，这是一个非常小的时间单位（通常是纳秒，但也可能是毫秒）。
#include <iostream>
#include <random> // for std::mt19937
#include <chrono> // for std::chrono

int main()
{
	// Seed our Mersenne Twister using steady_clock
	std::mt19937 mt{ static_cast<std::mt19937::result_type>(
		std::chrono::steady_clock::now().time_since_epoch().count()
		) };

	// Create a reusable random number generator that generates uniform numbers between 1 and 6
	std::uniform_int_distribution die6{ 1, 6 }; // for C++14, use std::uniform_int_distribution<> die6{ 1, 6 };

	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 40; ++count)
	{
		std::cout << die6(mt) << '\t'; // generate a roll of the die here

		// If we've printed 10 numbers, start a new row
		if (count % 10 == 0)
			std::cout << '\n';
	}

	return 0;
}
上述程序与前一个程序只有两个变化。首先，我们包含了
<chrono>
，它使我们能够访问时钟。其次，我们使用时钟的当前时间作为 Mersenne Twister 的种子值。
该程序生成的结果现在每次运行时都应该不同，您可以通过多次运行它来实验验证。
这种方法的缺点是，如果程序连续快速运行多次，每次运行生成的种子不会有太大差异，这可能会从统计角度影响随机结果的质量。对于普通程序来说，这并不重要，但对于需要高质量、独立结果的程序来说，这种播种方法可能不足。
提示
std::chrono::high_resolution_clock
是
std::chrono::steady_clock
的流行替代品。
std::chrono::high_resolution_clock
是使用最精细时间单位的时钟，但它可能使用系统时钟来获取当前时间，这可以由用户更改或回滚。
std::chrono::steady_clock
的滴答时间可能不那么精细，但它是唯一一个保证用户无法调整的时钟。
使用随机设备播种
随机库包含一个名为
std::random_device
的类型，它是一个实现定义的 PRNG。通常我们避免实现定义的功能，因为它们没有关于质量或可移植性的保证，但这是一个例外情况。通常
std::random_device
会向操作系统请求一个伪随机数（它如何做到这一点取决于操作系统）。
#include <iostream>
#include <random> // for std::mt19937 and std::random_device

int main()
{
	std::mt19937 mt{ std::random_device{}() };

	// Create a reusable random number generator that generates uniform numbers between 1 and 6
	std::uniform_int_distribution die6{ 1, 6 }; // for C++14, use std::uniform_int_distribution<> die6{ 1, 6 };

	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 40; ++count)
	{
		std::cout << die6(mt) << '\t'; // generate a roll of the die here

		// If we've printed 10 numbers, start a new row
		if (count % 10 == 0)
			std::cout << '\n';
	}

	return 0;
}
在上面的程序中，我们使用从
std::random_device
的临时实例生成的一个随机数来为我们的 Mersenne Twister 播种。如果您多次运行此程序，它每次也应该产生不同的结果。
std::random_device
可能存在的一个潜在问题：它不需要是非确定性的，这意味着它在某些系统上**可能**在每次程序运行时产生相同的序列，而这正是我们试图避免的。MinGW 中存在一个
错误
（在 GCC 9.2 中已修复），它会做同样的事情，使
std::random_device
无用。
然而，最流行的编译器（GCC/MinGW、Clang、Visual Studio）的最新版本都支持
std::random_device
的正确实现。
最佳实践
使用
std::random_device
为您的 PRNG 播种（除非它在您的目标编译器/架构上没有正确实现）。
问：
std::random_device{}()
是什么意思？
std::random_device{}
创建一个值初始化的
std::random_device
类型的临时对象。然后
()
调用该临时对象上的
operator()
，它返回一个随机值（我们将其用作 Mersenne Twister 的初始化器）
它等同于调用以下函数，该函数使用您应该更熟悉的语法
unsigned int getRandomDeviceValue()
{
   std::random_device rd{}; // create a value initialized std::random_device object
   return rd(); // return the result of operator() to the caller
}
使用
std::random_device{}()
我们可以得到相同的结果，而无需创建命名函数或命名变量，因此它更简洁。
问：如果 std::random_device 本身是随机的，为什么我们不直接使用它而不是 Mersenne Twister 呢？
因为
std::random_device
是实现定义的，所以我们不能对它做太多假设。访问它可能很昂贵，或者它可能导致我们的程序在等待更多随机数可用时暂停。它从中提取的数字池也可能很快耗尽，这会影响通过相同方法请求随机数的其他应用程序的随机结果。因此，
std::random_device
更适合用于播种其他 PRNG，而不是作为 PRNG 本身。
只播种 PRNG 一次
许多 PRNG 可以在初始播种后重新播种。这实质上会重新初始化随机数生成器的状态，使其从新的种子状态开始生成结果。除非您有特定的理由，否则通常应避免重新播种，因为它可能导致结果随机性降低，或者根本不随机。
最佳实践
只播种给定伪随机数生成器一次，不要重新播种。
以下是新手程序员常犯的一个错误示例
#include <iostream>
#include <random>

int getCard()
{
    std::mt19937 mt{ std::random_device{}() }; // this gets created and seeded every time the function is called
    std::uniform_int_distribution card{ 1, 52 };
    return card(mt);
}

int main()
{
    std::cout << getCard() << '\n';

    return 0;
}
在
getCard()
函数中，每次调用该函数时都会创建并播种随机数生成器。这充其量效率低下，并且很可能导致糟糕的随机结果。
Mersenne Twister 和欠播种问题
Mersenne Twister 的内部状态需要 19937 位（2493 字节），即 624 个 32 位值或 312 个 64 位值。因此，
std::mt19937
分配 624 个整数，而
std::mt19937_64
分配 312 个整数。
题外话…
由
std::mt19937
分配的整数定义为
std::uint_fast32_t
类型，它可能是 32 位或 64 位整数，具体取决于架构。如果
std::uint_fast32_t
解析为 64 位整数，则
std::mt19937
将使用 624 个 64 位整数，使其大小变为所需的两倍。
在上面的示例中，我们从时钟或
std::random_device
为
std::mt19937
播种，我们的种子只是一个整数。这意味着我们实际上是用一个整数初始化 624 个整数，这严重不足 Mersenne Twister PRNG 的播种。随机库会尽力用“随机”数据填充剩余的 623 个值……但它无法施展魔法。欠播种的 PRNG 可能会生成对于需要最高质量结果的应用程序来说次优的结果。例如，用一个 32 位值播种
std::mt19937
永远不会将其第一个输出生成为数字
42
。
那么我们如何解决这个问题呢？截至 C++20，没有简单的方法。但我们确实有一些建议。
首先，我们来谈谈
std::seed_seq
（代表“种子序列”）。在上一课中，我们提到理想情况下，我们希望我们的种子数据与 PRNG 的状态位一样多，否则我们的 PRNG 将会欠播种。但在许多情况下（尤其是当我们的 PRNG 具有较大的状态时），我们没有那么多位的随机化种子数据。
std::seed_seq
是一种旨在帮助解决此问题的类型。我们可以将我们拥有的尽可能多的随机值传递给它，然后它将生成所需数量的额外无偏种子值，以初始化 PRNG 的状态。如果您用一个值（例如来自
std::random_device
）初始化
std::seed_seq
，然后用
std::seed_seq
对象初始化 Mersenne Twister，
std::seed_seq
将生成 623 个额外的种子数据值。这不会增加随机性，但会给我们更好的 0 和 1 位组合。然而，我们提供给
std::seed_seq
的随机数据越多，它为我们做得越好。因此，最简单的想法是简单地使用
std::random_device
来为
std::seed_seq
提供更多数据。如果我们将
std::seed_seq
初始化为 8 个来自
std::random_device
的值而不是 1 个，那么由
std::seed_seq
生成的剩余值应该会好得多
#include <iostream>
#include <random>

int main()
{
	std::random_device rd{};
	std::seed_seq ss{ rd(), rd(), rd(), rd(), rd(), rd(), rd(), rd() }; // get 8 integers of random numbers from std::random_device for our seed
	std::mt19937 mt{ ss }; // initialize our Mersenne Twister with the std::seed_seq

	// Create a reusable random number generator that generates uniform numbers between 1 and 6
	std::uniform_int_distribution die6{ 1, 6 }; // for C++14, use std::uniform_int_distribution<> die6{ 1, 6 };

	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 40; ++count)
	{
		std::cout << die6(mt) << '\t'; // generate a roll of the die here

		// If we've printed 10 numbers, start a new row
		if (count % 10 == 0)
			std::cout << '\n';
	}

	return 0;
}
这非常简单，因此至少没有理由不这样做。
问：为什么不从
std::random_device
给
std::seed_seq
624 个值呢？
你可以这样做，但这可能会很慢，并且有耗尽
std::random_device
使用的随机数池的风险。
您还可以使用其他“随机”输入到
std::seed_seq
。我们已经向您展示了如何从时钟获取值，因此您可以轻松地将其放入。有时还会使用其他内容，包括当前线程 ID、特定函数的地址、用户 ID、进程 ID 等……这超出了本文的范围，但
本文
提供了一些背景信息和
randutils.hpp
的链接，其中实现了这一点。
另一种方法是使用具有较小状态的不同 PRNG。许多优秀的 PRNG 使用 64 或 128 位状态，这可以通过使用填充了 8 次
std::random_device
调用的
std::seed_seq
轻松初始化。
预热 PRNG
当 PRNG 被赋予质量差的种子（或欠播种）时，PRNG 的初始结果可能质量不高。因此，一些 PRNG 受益于“预热”，这是一种丢弃 PRNG 生成的前 N 个结果的技术。这允许 PRNG 的内部状态混合，从而后续结果应该质量更高。通常会丢弃几百到几千个初始结果。PRNG 的周期越长，应丢弃的初始结果越多。
题外话…
Visual Studio 对
rand()
的实现存在一个错误（或者仍然存在？），即生成的第一个结果不会充分随机化。您可能会看到较旧的程序使用
rand()
丢弃单个结果，以避免此问题。
std::mt19937
使用的
seed_seq
初始化会执行预热，因此我们无需显式预热
std::mt19937
对象。
跨多个函数或文件的随机数 (Random.h)
此内容已移至
8.15 -- 全局随机数 (Random.h)
。
调试使用随机数的程序
使用随机数的程序可能难以调试，因为程序每次运行都可能表现出不同的行为。在这种情况下，错误的行为可能会发生，也可能不会发生。这可能会浪费大量时间。在调试时，确保程序每次都以相同（不正确）的方式执行会很有帮助。这样，您可以根据需要多次运行程序，以隔离错误所在。
因此，在调试时，一个有用的技术是用一个特定的固定值（例如
5
）来为您的 PRNG 播种，该值会导致错误行为发生。如果给定种子没有导致您的程序出现错误，请继续增加种子值，直到找到一个会引起错误的值。这将确保您的程序每次都生成相同的结果，从而简化调试。找到错误后，您可以使用正常的播种方法再次开始生成随机结果。
随机常见问题
问：救命！我的随机数生成器生成相同的随机数序列。
如果您的随机数生成器在每次程序运行时都生成相同的随机数序列，您可能没有正确播种它（或根本没有播种）。请确保您使用每次程序运行时都会更改的值进行播种。
问：救命！我的随机数生成器不断生成相同的数字。
如果您的随机数生成器每次您要求它提供随机数时都生成相同的数字，那么您可能是在生成随机数之前重新播种随机数生成器，或者您为每个随机数创建了一个新的随机生成器。
下一课
8.15
全局随机数 (Random.h)
返回目录
上一课
8.13
随机数生成简介