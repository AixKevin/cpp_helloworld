# 9.x — 第 9 章总结和测验

9.x — 第 9 章总结和测验
Alex
2023年12月28日，太平洋标准时间下午2:45
2024年12月1日
章节回顾
范围蔓延（Scope creep）
是指项目的能力超出了项目或项目阶段开始时最初的预期。
软件验证（Software verification）
是测试软件在所有情况下是否按预期工作的过程。
单元测试（Unit test）
是旨在独立测试代码的一小部分（通常是函数或调用）以确保特定行为按预期发生的测试。
单元测试框架（Unit test frameworks）
可以帮助您组织单元测试。
集成测试（Integration testing）
测试一堆单元的集成，以确保它们正常工作。
代码覆盖率（Code coverage）
是指测试时执行的源代码量。
语句覆盖率（Statement coverage）
是指程序中被测试例程执行的语句的百分比。
分支覆盖率（Branch coverage）
是指被测试例程执行的分支的百分比。
循环覆盖率（Loop coverage）
（也称为
0、1、2测试
）意味着如果您有一个循环，您应该确保它在迭代0次、1次和2次时都能正常工作。
顺利路径（happy path）
是指没有遇到错误时的执行路径。
错误路径（sad path）
是指发生错误或失败状态的路径。
不可恢复错误（non-recoverable error）
（也称为
致命错误（fatal error）
）是严重到程序无法继续运行的错误。能够很好地处理错误情况的程序是
健壮的（robust）
。
缓冲区（buffer）
是为临时存储数据而预留的一段内存，用于在数据从一个地方移动到另一个地方时使用。
检查用户输入是否符合程序预期的过程称为
输入验证（input validation）
。
std::cerr
是一个输出流（类似于
std::cout
），设计用于错误消息。
前置条件（precondition）
是在执行某个代码段之前必须始终为真的任何条件。
不变式（invariant）
是在某个组件执行时必须为真的条件。
后置条件（postcondition）
是在执行某些代码之后必须始终为真的任何条件。
断言（assertion）
是一个表达式，除非程序中存在错误，否则它将为真。在 C++ 中，运行时断言通常使用
assert
预处理器宏实现。断言通常在非调试代码中关闭。
static_assert
是在编译时评估的断言。
断言应该用于记录逻辑上不可能发生的情况。错误处理应该用于处理可能发生的情况。
小测验时间
问题 #1
在课程
8.x -- 第 8 章总结和测验
的测验中，我们实现了一个 Hi-Lo 游戏。
更新您之前的解决方案，以处理无效猜测（例如“x”）、超出范围的猜测（例如
0
或
101
），或包含多余字符的有效猜测（例如
43x
）。还要处理用户在游戏询问是否要再次玩时输入多余字符的情况。
提示：编写一个单独的函数来处理用户输入猜测（以及相关的错误处理）。
显示答案
#include <iostream>
#include <limits>   // for std::numeric_limits
#include "Random.h" // https://learncpp.com.cn/cpp-tutorial/global-random-numbers-random-h/

int getGuess(int count, int min, int max)
{
	while (true) // loop until user enters valid input
	{
		std::cout << "Guess #" << count << ": ";

		int guess {};
		std::cin >> guess;

		bool success { std::cin };
		std::cin.clear(); // put us back in 'normal' operation mode (if needed)
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // remove any extra input

		// If we didn't extract anything or the extracted guess is out of bounds, try again
		if (!success || guess < min || guess > max)
			continue;

		return guess;
	}
}

// returns true if the user won, false if they lost
bool playHiLo(int guesses, int min, int max)
{
	std::cout << "Let's play a game. I'm thinking of a number between " << min << " and " << max << ". You have " << guesses << " tries to guess what it is.\n";
	int number{ Random::get(min, max) }; // this is the number the user needs to guess

	// Loop through all of the guesses
	for (int count{ 1 }; count <= guesses; ++count)
	{
		int guess{ getGuess(count, min, max) };

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
	return false; // if the user lost
}

bool playAgain()
{
	// Keep asking the user if they want to play again until they pick y or n.
	while (true)
	{
		char ch{};
		std::cout << "Would you like to play again (y/n)? ";
		std::cin >> ch;

		// clear out any extraneous input
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        
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
下一课
10.1
隐式类型转换
返回目录
上一课
9.6
Assert 和 static_assert