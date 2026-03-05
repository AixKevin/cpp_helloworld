# 27.x — 第 27 章总结与测验

27.x — 第 27 章总结与测验
Alex
2017 年 2 月 11 日，太平洋标准时间下午 12:18
2023 年 10 月 7 日
章节回顾
异常处理提供了一种机制，可以将错误或其他异常情况的处理与代码的典型控制流解耦。这允许在给定情况下更自由地处理错误，从而减轻（如果不是全部）返回码造成的许多混乱。
throw
语句用于抛出异常。
try 块
查找在其内部编写或调用的代码抛出的异常。这些异常被路由到
catch 块
，catch 块捕获特定类型的异常（如果匹配）并处理它们。默认情况下，被捕获的异常被视为已处理。
异常会立即处理。如果抛出异常，控制权会跳转到最近的封闭 try 块，寻找可以处理异常的 catch 处理器。如果找到匹配的 try/catch，堆栈将回溯到 catch 块的位置，控制权在匹配的 catch 顶部恢复。如果未找到 try 块或无 catch 块匹配，程序将调用 std::terminate，该函数将因未处理的异常错误而终止。
可以抛出任何数据类型的异常，包括类。
Catch 块可以配置为捕获特定数据类型的异常，或者可以通过使用省略号 (…) 设置一个捕获所有异常的处理器。捕获基类引用的 catch 块也将捕获派生类的异常。标准库抛出的所有异常都派生自 std::exception 类（该类位于 exception 头文件中），因此通过引用捕获 std::exception 将捕获所有标准库异常。可以使用 what() 成员函数确定抛出了哪种 std::exception。
在 catch 块内部，可能会抛出新的异常。由于这个新异常是在与该 catch 块关联的 try 块之外抛出的，因此它不会被其抛出的 catch 块捕获。可以使用单独的关键字 throw 从 catch 块重新抛出异常。不要使用捕获到的异常变量重新抛出异常，否则可能会导致对象切片。
函数 try 块提供了一种捕获函数内或相关成员初始化列表中发生的任何异常的方法。这些通常仅与派生类构造函数一起使用。
永远不要从析构函数中抛出异常。
noexcept
异常说明符可用于表示函数是无抛出/无失败的。
std::move_if_noexcept 如果对象具有 noexcept 移动构造函数，则返回一个可移动的右值，否则返回一个可复制的左值。我们可以将 noexcept 说明符与 std::move_if_noexcept 结合使用，仅当存在强异常保证时才使用移动语义（否则使用复制语义）。
最后，异常处理确实有成本。在大多数情况下，使用异常的代码运行速度会稍微慢一些，并且处理异常的成本非常高。您应该只使用异常来处理异常情况，而不是用于正常的错误处理情况（例如无效输入）。
章节测验
编写一个 Fraction 类，其构造函数接受分子和分母。如果用户传入分母为 0，则抛出 std::runtime_error 类型的异常（包含在 stdexcept 头文件中）。在您的主程序中，要求用户输入两个整数。如果 Fraction 有效，则打印分数。如果 Fraction 无效，则捕获 std::exception，并告诉用户他们输入了无效分数。
以下是程序一次运行的输出示例
Enter the numerator: 5
Enter the denominator: 0
Invalid denominator
显示答案
#include <iostream>
#include <stdexcept> // for std::runtime_error
#include <exception> // for std::exception

class Fraction
{
private:
	int m_numerator = 0;
	int m_denominator = 1;

public:
	Fraction(int numerator = 0, int denominator = 1)
		: m_numerator{ numerator }
		, m_denominator{ denominator }
	{
		if (m_denominator == 0)
			throw std::runtime_error("Invalid denominator");
	}

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);

};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

int main()
{
	std::cout << "Enter the numerator: ";
	int numerator{};
	std::cin >> numerator;

	std::cout << "Enter the denominator: ";
	int denominator{};
	std::cin >> denominator;

	try
	{
		Fraction f{ numerator, denominator };
		std::cout << "Your fraction is: " << f << '\n';
	}
	catch (const std::exception& e)
	{
		std::cerr << e.what() << '\n';
	}

	return 0;
}
下一课
28.1
输入和输出 (I/O) 流
返回目录
上一课
27.10
std::move_if_noexcept