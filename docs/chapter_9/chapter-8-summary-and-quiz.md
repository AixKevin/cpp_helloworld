# 8.x — 第 8 章总结和测验

8.x — 第 8 章总结和测验
Alex
2015 年 7 月 16 日，下午 2:29 (太平洋夏令时)
2025 年 2 月 4 日
章节回顾
CPU 在程序中执行的特定语句序列称为程序的
执行路径
。一个
直线程序
每次运行时都采用相同的路径。
控制流语句
（也称为
流控制语句
）允许程序员改变正常的执行路径。当控制流语句导致程序开始执行某些非顺序指令序列时，这被称为
分支
。
条件语句
是指定某些相关语句是否应该执行的语句。
If 语句
允许我们根据某个条件是否为
true
来执行相关语句。如果相关条件为
false
，则执行
Else 语句
。您可以将多个 if 和 else 语句链接在一起。
当
else 语句
与哪个
if 语句
相关联不明确时，就会出现
悬空 else
。
悬空 else
语句与同一块中最后一个不匹配的
if 语句
匹配。因此，我们通过确保
if 语句
的主体放在一个块中来简单地避免
悬空 else
语句。
空语句
是仅由分号组成的语句。它什么也不做，当语言要求存在语句但程序员不需要该语句做任何事情时使用。
Switch 语句
提供了一种更简洁、更快的方法来在多个匹配项之间进行选择。Switch 语句仅适用于整数类型。
Case 标签
用于标识要匹配的评估条件的值。如果找不到匹配的 case 标签，则执行
default 标签
下的语句。
当执行从标签下的语句流向后续标签下的语句时，这被称为
穿透
。
break 语句
（或
return 语句
）可用于防止穿透。[[fallthrough]] 属性可用于记录有意穿透。
Goto 语句
允许程序跳转到代码中的其他位置，无论是向前还是向后。这些通常应该避免，因为它们可能创建
意大利面条式代码
，即当程序的执行路径类似于一碗意大利面条时发生的情况。
While 循环
允许程序在给定条件评估为
true
时进行循环。条件在循环执行前进行评估。
无限循环
是指条件始终评估为
true
的循环。这些循环将永远循环，除非使用其他控制流语句来停止它们。
循环变量
（也称为
计数器
）是用于计算循环执行次数的整数变量。循环的每次执行称为一次
迭代
。
Do while 循环
类似于 while 循环，但条件在循环执行后而不是之前进行评估。
For 循环
是最常用的循环，当您需要循环特定次数时，它们是理想的选择。当循环迭代次数多一次或少一次时，就会发生
差一错误
。
Break 语句
允许我们跳出 switch、while、do while 或 for 循环（也包括
基于范围的 for 循环
，我们尚未涵盖）。
Continue 语句
允许我们立即进入下一次循环迭代。
停止
允许我们终止程序。
正常终止
意味着程序以预期的方式退出（并且
状态码
将指示它是否成功）。
std::exit()
会在
main
结束时自动调用，或者可以显式调用它来终止程序。它会进行一些清理，但不会清理任何局部变量，也不会展开调用堆栈。
当程序遇到某种意外错误并不得不关闭时，就会发生
异常终止
。可以调用
std::abort
进行异常终止。
算法
是可用于解决某个问题或产生某个有用结果的有限指令序列。如果算法在调用之间保留某些信息，则认为它是
有状态的
。相反，
无状态
算法不存储任何信息（并且在调用时必须获得其工作所需的所有信息）。当应用于算法时，术语
状态
指的是有状态变量中当前持有的值。
如果算法对于给定的输入（为
start
提供的值）将始终产生相同的输出序列，则认为该算法是
确定性的
。
伪随机数生成器 (PRNG)
是一种生成其属性模拟随机数序列的数字序列的算法。当实例化 PRNG 时，可以提供一个初始值（或一组值），称为
随机种子
（或简称
种子
）来初始化 PRNG 的状态。当 PRNG 用种子初始化时，我们说它已经
播种
。种子值的大小可以小于 PRNG 状态的大小。发生这种情况时，我们说 PRNG 已经
欠播种
。PRNG 开始重复自身之前的序列长度称为
周期
。
随机数分布
将 PRNG 的输出转换为其他数字分布。
均匀分布
是一种随机数分布，它以相等的概率在两个数字 X 和 Y（包括）之间产生输出。
小测验时间
警告：从现在开始，测验会变得越来越难，但你可以做到。让我们好好完成这些测验！
问题 #1
在第
4.x — 第 4 章总结和测验
中，我们编写了一个程序来模拟一个球从塔上掉落。由于我们还没有循环，球只能下落 5 秒。
获取下面的程序并修改它，使球下落所需秒数，直到它到达地面。更新程序以使用所有涵盖的最佳实践（命名空间、constexpr 等）。
#include <iostream>

// Gets tower height from user and returns it
double getTowerHeight()
{
	std::cout << "Enter the height of the tower in meters: ";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// Returns the current ball height after "seconds" seconds
double calculateBallHeight(double towerHeight, int seconds)
{
	const double gravity { 9.8 };
    
	// Using formula: s = (u * t) + (a * t^2) / 2
	// here u (initial velocity) = 0, so (u * t) = 0
	const double fallDistance { gravity * (seconds * seconds) / 2.0 };
	const double ballHeight { towerHeight - fallDistance };

	// If the ball would be under the ground, place it on the ground
	if (ballHeight < 0.0)
		return 0.0;
    
	return ballHeight;
}

// Prints ball height above ground
void printBallHeight(double ballHeight, int seconds)
{
	if (ballHeight > 0.0)
		std::cout << "At " << seconds << " seconds, the ball is at height: " << ballHeight << " meters\n";
	else
		std::cout << "At " << seconds << " seconds, the ball is on the ground.\n";
}

// Calculates the current ball height and then prints it
// This is a helper function to make it easier to do this
void calculateAndPrintBallHeight(double towerHeight, int seconds)
{
	const double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);
}

int main()
{
	const double towerHeight{ getTowerHeight() };

	calculateAndPrintBallHeight(towerHeight, 0);
	calculateAndPrintBallHeight(towerHeight, 1);
	calculateAndPrintBallHeight(towerHeight, 2);
	calculateAndPrintBallHeight(towerHeight, 3);
	calculateAndPrintBallHeight(towerHeight, 4);
	calculateAndPrintBallHeight(towerHeight, 5);
       
	return 0;
}
显示答案
#include <iostream>

namespace Constants
{
	constexpr double gravity { 9.8 };
}

// Gets tower height from user and returns it
double getTowerHeight()
{
	std::cout << "Enter the height of the tower in meters: ";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// Returns the current ball height after "seconds" seconds
// note: this function could be constexpr, but we haven't covered constexpr functions yet
double calculateBallHeight(double towerHeight, int seconds)
{
	// Using formula: s = (u * t) + (a * t^2) / 2
	// here u (initial velocity) = 0, so (u * t) = 0
	const double fallDistance { Constants::gravity * (seconds * seconds) / 2.0 };
	const double ballHeight { towerHeight - fallDistance };

	if (ballHeight < 0.0)
		return 0.0;
    
	return ballHeight;
}

// Prints ball height above ground
void printBallHeight(double ballHeight, int seconds)
{
	if (ballHeight > 0.0)
		std::cout << "At " << seconds << " seconds, the ball is at height: " << ballHeight << " meters\n";
	else
		std::cout << "At " << seconds << " seconds, the ball is on the ground.\n";
}

// Calculates the current ball height and then prints it
// This is a helper function to make it easier to do this
double calculateAndPrintBallHeight(double towerHeight, int seconds)
{
	const double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);

	return ballHeight;
}

int main()
{
	const double towerHeight{ getTowerHeight() };

	int seconds { 0 };
	while (calculateAndPrintBallHeight(towerHeight, seconds) > 0.0)
	{
		++seconds;
	}
       
	return 0;
}
问题 #2
素数是大于 1 的自然数，只能被 1 和自身整除（没有余数）。
使用 for 循环编写
isPrime()
函数来完成以下程序。成功后，程序将打印“Success!”。
// Make sure that assert triggers even if we compile in release mode
#undef NDEBUG

#include <cassert> // for assert
#include <iostream>

bool isPrime(int x)
{
    return false;
    // write this function using a for loop
}

int main()
{
    assert(!isPrime(0)); // terminate program if isPrime(0) is true
    assert(!isPrime(1));
    assert(isPrime(2));  // terminate program if isPrime(2) is false
    assert(isPrime(3));
    assert(!isPrime(4));
    assert(isPrime(5));
    assert(isPrime(7));
    assert(!isPrime(9));
    assert(isPrime(11));
    assert(isPrime(13));
    assert(!isPrime(15));
    assert(!isPrime(16));
    assert(isPrime(17));
    assert(isPrime(19));
    assert(isPrime(97));
    assert(!isPrime(99));
    assert(isPrime(13417));

    std::cout << "Success!\n";

    return 0;
}
相关内容
assert
是一个预处理器宏，如果关联的参数评估为 false，它会终止程序。因此，当我们写
assert(!isPrime(0))
时，我们的意思是“如果 isPrime(0) 为 true，则终止程序”。我们将在第
9.6 — Assert 和 static_assert
课中更详细地介绍 assert。
显示答案
// Make sure that assert triggers even if we compile in release mode
#undef NDEBUG

#include <cassert> // for assert
#include <iostream>

// Non-optimized version
bool isPrime(int x)
{
    if (x <= 1) // if x is negative, 0, or 1 then the number is not prime
        return false;

    for (int test{ 2 }; test < x; ++test)
    {
        if (x % test == 0) // if x is evenly divisible
            return false;  // then this number isn't prime
    }

    return true; // if we didn't find any divisors, then x must be prime
}

int main()
{
    assert(!isPrime(0));
    assert(!isPrime(1));
    assert(isPrime(2));
    assert(isPrime(3));
    assert(!isPrime(4));
    assert(isPrime(5));
    assert(isPrime(7));
    assert(!isPrime(9));
    assert(isPrime(11));
    assert(isPrime(13));
    assert(!isPrime(15));
    assert(!isPrime(16));
    assert(isPrime(17));
    assert(isPrime(19));
    assert(isPrime(97));
    assert(!isPrime(99));
    assert(isPrime(13417));

    std::cout << "Success!\n";

    return 0;
}
额外加分题
上述解决方案中的 for 循环存在两个次优原因
它检查偶数除数。我们不需要测试这些（除了 2）。
它检查从 1 到
x
的每个数字，看它是否是除数。一个非素数（合数）必须至少有一个小于或等于其平方根的除数，因此检查
x
的平方根之外的除数是不必要的。
std::sqrt(x)
（在 <cmath> 头文件中）返回
x
的平方根。
对于后者，我们有两种选择：在循环之前计算
std::sqrt(x)
，然后用循环变量与该值进行测试。或者，我们可以通过平方比较的两边来完全优化
std::sqrt(x)
（感谢读者 JJag 提出此建议）（如果您需要额外帮助，请参阅提示）。我们将在测验解决方案中使用后一种选择。
显示提示
提示：给定两个变量
a >= 0
和
b >= 0
，我们可以对比较
a <= sqrt(b)
的两边进行平方，比较仍然成立。这给我们
a * a <= sqrt(b) * sqrt(b)
，这等价于
a * a <= b
。
更新上述解决方案以实现这两种优化。
显示答案
#include <cassert>
#include <cmath> // for std::sqrt
#include <iostream>

// optimized version
bool isPrime(int x)
{
    if (x <= 1)     // if x is negative, 0, or 1 then the number is not prime
        return false;
    if (x == 2)     // the number 2 is the only even prime
        return true;
    if (x % 2 == 0) // any other even number is not prime
        return false;

    // For any number 3 or greater, test odd values (this is why we add 2)
    // between 3 and sqrt(x) to see if they are a divisor
    // Also see https://stackoverflow.com/questions/5811151/why-do-we-check-up-to-the-square-root-of-a-number-to-determine-if-the-number-is
    // Since test >= 0 and x >=0, we can optimize test < std::sqrt(x) to test * text < x
    for (int test{ 3 }; test * test <= x; test += 2)
    {
        if (x % test == 0) // if x is evenly divisible
            return false;  // then this number isn't prime
    }

    return true; // if we didn't find any divisors, then x must be prime
}

int main()
{
    assert(!isPrime(0));
    assert(!isPrime(1));
    assert(isPrime(2));
    assert(isPrime(3));
    assert(!isPrime(4));
    assert(isPrime(5));
    assert(isPrime(7));
    assert(!isPrime(9));
    assert(isPrime(11));
    assert(isPrime(13));
    assert(!isPrime(15));
    assert(!isPrime(16));
    assert(isPrime(17));
    assert(isPrime(19));
    assert(isPrime(97));
    assert(!isPrime(99));
    assert(isPrime(13417));

    std::cout << "Success!\n";

    return 0;
}
问题 #3
实现 Hi-Lo 游戏。首先，您的程序应选择一个介于 1 到 100 之间的随机整数。用户有 7 次机会猜测该数字。
如果用户没有猜对数字，程序应该告诉他们是猜高了还是猜低了。如果用户猜对了数字，程序应该告诉他们赢了。如果他们用完了猜测次数，程序应该告诉他们输了，以及正确的数字是什么。游戏结束时，应该询问用户是否想再玩一次。如果用户没有输入“y”或“n”，则再次询问他们。
对于本测验，假设用户输入了一个有效数字。
使用来自
8.15 -- 全局随机数 (Random.h)
的 Random.h 头文件。
您的输出应该如下所示
Let's play a game. I'm thinking of a number between 1 and 100. You have 7 tries to guess what it is.
Guess #1: 64
Your guess is too high.
Guess #2: 32
Your guess is too low.
Guess #3: 54
Your guess is too high.
Guess #4: 51
Correct! You win!
Would you like to play again (y/n)? y
Let's play a game. I'm thinking of a number between 1 and 100. You have 7 tries to guess what it is.
Guess #1: 64
Your guess is too high.
Guess #2: 32
Your guess is too low.
Guess #3: 54
Your guess is too high.
Guess #4: 51
Your guess is too high.
Guess #5: 36
Your guess is too low.
Guess #6: 45
Your guess is too low.
Guess #7: 48
Your guess is too low.
Sorry, you lose. The correct number was 49.
Would you like to play again (y/n)? q
Would you like to play again (y/n)? n
Thank you for playing.
额外加分：将最小值、最大值和猜测次数设置为可配置参数。
显示答案
#include <iostream>
#include "Random.h" // https://learncpp.com.cn/cpp-tutorial/global-random-numbers-random-h/

// Returns true if the user won, false if they lost
// We don't use the return value in this program, but it doesn't add complexity to have it, and may be useful in a future update
// (e.g. if we wanted to move the won/lost messages out of the function, or conditionalize other behavior based on won/lost)
bool playHiLo(int guesses, int min, int max)
{
	std::cout << "Let's play a game. I'm thinking of a number between " << min << " and " << max << ". You have " << guesses << " tries to guess what it is.\n";
	const int number { Random::get(min, max) }; // this is the number the user needs to guess

	// Loop through all of the guesses
	for (int count{ 1 }; count <= guesses; ++count)
	{
		std::cout << "Guess #" << count << ": ";

		int guess{};
		std::cin >> guess;

		if (guess > number)
			std::cout << "Your guess is too high.\n";
		else if (guess < number)
			std::cout << "Your guess is too low.\n";
		else // guess == number, so the user won
		{
			std::cout << "Correct! You win!\n";
			return true;
		}
	}

	// The user lost
	std::cout << "Sorry, you lose. The correct number was " << number << '\n';
	return false;
}

bool playAgain()
{
	// Keep asking the user if they want to play again until they pick y or n.
	while (true)
	{
		char ch{};
		std::cout << "Would you like to play again (y/n)? ";
		std::cin >> ch;

		switch (ch)
		{
		case 'y': return true;
		case 'n': return false;
		}
	}
}

int main()
{
	constexpr int guesses { 7 }; // the user has this many guesses
	constexpr int min     { 1 };
	constexpr int max     { 100 };

	do
	{
		playHiLo(guesses, min, max);
	} while (playAgain());

	std::cout << "Thank you for playing.\n";

	return 0;
}
我们将在第
9.x — 第 9 章总结和测验
中为此解决方案添加错误处理。
下一课
9.1
代码测试简介
返回目录
上一课
8.15
全局随机数 (Random.h)