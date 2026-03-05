# F.X — F 章总结与测验

F.X — F 章总结与测验
Alex
2024 年 12 月 2 日，太平洋标准时间上午 11:32
2024 年 12 月 2 日
一个
constexpr
函数是允许在常量表达式中调用的函数。要将一个函数设为 constexpr 函数，我们只需在返回类型前使用
constexpr
关键字。Constexpr 函数仅在需要常量表达式的上下文中使用时，才保证在编译时进行求值。否则，它们可能会在编译时（如果符合条件）或运行时进行求值。Constexpr 函数是隐式内联的，并且编译器必须看到 constexpr 函数的完整定义才能在编译时调用它。
一个
consteval 函数
是必须在编译时求值的函数。Consteval 函数的其他规则与 constexpr 函数相同。
小测验时间
问题 #1
在以下程序中添加
const
和/或
constexpr
#include <iostream>

// gets tower height from user and returns it
double getTowerHeight()
{
	std::cout << "Enter the height of the tower in meters: ";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// Returns ball height from ground after "seconds" seconds
double calculateBallHeight(double towerHeight, int seconds)
{
	double gravity{ 9.8 };

	// Using formula: [ s = u * t + (a * t^2) / 2 ], here u(initial velocity) = 0
	double distanceFallen{ (gravity * (seconds * seconds)) / 2.0 };
	double currentHeight{ towerHeight - distanceFallen };

	return currentHeight;
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
void printCalculatedBallHeight(double towerHeight, int seconds)
{
	double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);
}

int main()
{
	double towerHeight{ getTowerHeight() };

	printCalculatedBallHeight(towerHeight, 0);
	printCalculatedBallHeight(towerHeight, 1);
	printCalculatedBallHeight(towerHeight, 2);
	printCalculatedBallHeight(towerHeight, 3);
	printCalculatedBallHeight(towerHeight, 4);
	printCalculatedBallHeight(towerHeight, 5);

	return 0;
}
显示答案
#include <iostream>

// This function should not be made constexpr because output and input can only be done at runtime.
// The versions of `operator<<` and `operator>>` that do output and input don't support constexpr.
double getTowerHeight()
{
	std::cout << "Enter the height of the tower in meters: ";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// Returns height from ground after "seconds" seconds
// This function is made constepxr because it just calculates a value from its inputs and return it.
// Arithmetic can be done at compile-time, and no non-constexpr functions are called.
// Reminder: A constexpr function can be evaluated at compile-time or runtime.
//   If its arguments are constexpr, it can be called at compile-time.
//   In this case, it's called at runtime because the argument for towerHeight isn't constexpr.
// If a function can be made constexpr, it should be.
// Remember: function parameters are not constexpr, even in a constexpr function
constexpr double calculateBallHeight(double towerHeight, int seconds)
{
	constexpr double gravity{ 9.8 }; // constexpr because it's a compile-time constant

	// Using formula: [ s = u * t + (a * t^2) / 2 ], here u(initial velocity) = 0
	// These variables can't be constexpr since their initializers aren't constant expressions
	const double distanceFallen{ (gravity * (seconds * seconds)) / 2.0 };
	const double currentHeight{ towerHeight - distanceFallen };

	return currentHeight;
}

// This function should not be made constexpr because output and input can only be done at runtime.
// The versions of `operator<<` and `operator>>` that do output and input don't support constexpr.
void printBallHeight(double ballHeight, int seconds)
{
	if (ballHeight > 0.0)
		std::cout << "At " << seconds << " seconds, the ball is at height: " << ballHeight << " meters\n";
	else
		std::cout << "At " << seconds << " seconds, the ball is on the ground.\n";
}

// This function should not be made constexpr because output and input can only be done at runtime.
// The versions of `operator<<` and `operator>>` that do output and input don't support constexpr.
void printCalculatedBallHeight(double towerHeight, int seconds)
{
	// height can only be const (not constexpr) because its initializer is not a constant expression
	const double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);
}

int main()
{
	// towerHeight can only be const (not constexpr) because its initializer is not a constant expression
	const double towerHeight{ getTowerHeight() };

	printCalculatedBallHeight(towerHeight, 0);
	printCalculatedBallHeight(towerHeight, 1);
	printCalculatedBallHeight(towerHeight, 2);
	printCalculatedBallHeight(towerHeight, 3);
	printCalculatedBallHeight(towerHeight, 4);
	printCalculatedBallHeight(towerHeight, 5);

	return 0;
}
下一课
12.1
复合数据类型简介
返回目录
上一课
F.4
Constexpr 函数（第 4 部分）