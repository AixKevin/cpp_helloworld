# 4.x — 第 4 章总结和测验

4.x — 第 4 章总结和测验
Alex
2007 年 6 月 11 日下午 5:42 PDT
2024 年 11 月 29 日
章节回顾
最小的内存单位是
二进制数字
，也称为
位
。可以直接寻址（访问）的最小内存量是
字节
。现代标准是一个字节等于 8 位。
数据类型
告诉编译器如何以有意义的方式解释内存内容。
C++ 支持许多基本数据类型，包括浮点数、整数、布尔值、字符、空指针和 void。
Void
用于表示无类型。它主要用于表示函数不返回值。
不同的类型占用不同的内存量，并且所使用的内存量可能因机器而异。
相关内容
有关指示每个基本类型的最小大小的表格，请参阅
4.3 -- 对象大小和 sizeof 运算符
。
sizeof
运算符可用于以字节为单位返回类型的大小。
有符号整数
用于保存正负整数，包括 0。特定数据类型可以保存的值集合称为其
范围
。使用整数时，请注意溢出和整数除法问题。
无符号整数
只保存正数（和 0），通常应避免使用，除非您正在进行位级操作。
固定宽度整数
是具有保证大小的整数，但它们可能并非存在于所有体系结构上。快速和最小整数是至少达到一定大小的最快和最小整数。通常应避免使用
std::int8_t
和
std::uint8_t
，因为它们倾向于表现得像字符而不是整数。
size_t
是一种无符号整数类型，用于表示对象的大小或长度。
科学计数法
是一种书写长数字的简写方式。C++ 支持与浮点数结合使用科学计数法。有效数字（e 之前的部分）中的数字称为
有效数字
。
浮点数
是一组旨在保存实数（包括带小数部分的数字）的类型。数字的
精度
定义了它可以表示多少位有效数字而不会丢失信息。当浮点数中存储的有效数字过多而无法保持该精度时，可能会发生
舍入误差
。舍入误差一直发生，即使是 0.1 这样的简单数字。因此，您不应直接比较浮点数。
布尔
类型用于存储
true
或
false
值。
If 语句
允许我们根据条件是否为真执行一行或多行代码。if 语句的条件表达式被解释为布尔值。当先前的 if 语句条件评估为假时，可以使用
else 语句
执行语句。
Char
用于存储被解释为 ASCII 字符的值。使用字符时，请注意不要混淆 ASCII 代码值和数字。将字符打印为整数值需要使用
static_cast
。
C++ 中通常使用尖括号来表示需要参数化类型的东西。这与
static_cast
一起使用，以确定参数应转换为哪种数据类型（例如，
static_cast
(x)
将返回
x
的值作为
int
）。
小测验时间
问题 #1
在以下每种情况下，为变量选择适当的数据类型。尽可能具体。如果答案是整数，请选择 int（如果大小不重要），或根据范围选择特定的固定宽度整数类型（例如 std::int16_t）。
a) 用户的年龄（以年为单位）（假设类型大小不重要）
显示答案
int
b) 用户是否希望应用程序检查更新
显示答案
bool
c) pi (3.14159265)
显示答案
double
d) 教科书的页数（假设大小不重要）
显示答案
由于书籍的页数可能不会超过 32,767 页，因此 int 在此处应该没问题。
e) 沙发的长度（以英尺为单位，精确到小数点后 2 位）（假设大小很重要）
显示答案
float
f) 自出生以来眨眼的次数（注意：答案以百万计）
显示答案
std::int32_t
g) 用户通过字母从菜单中选择一个选项
显示答案
char
h) 某人出生的年份（假设大小很重要）
显示答案
std::int16_t。您可以使用正数表示公元纪年的出生日期，负数表示公元前纪年的出生日期。
问题 #2
作者注
从这里开始，测验变得更具挑战性。这些要求您编写程序的测验旨在确保您可以整合在课程中介绍的多个概念。您应该准备好花一些时间来解决这些问题。如果您是编程新手，您不应期望能够立即回答这些问题。
请记住，这里的目标是帮助您确定您知道什么，以及您可能需要花更多时间学习哪些概念。如果您发现自己有点挣扎，那没关系。
这里有一些提示
不要试图一次性写出整个解决方案。编写一个函数，然后测试它以确保它按预期工作。然后继续。
使用调试器来帮助找出问题出在哪里。
回顾并复习本章前面课程中测验的答案，因为它们通常包含相似的概念。
如果您确实卡住了，请随意查看解决方案，但请花时间确保您在继续之前了解每一行代码的作用。只要您离开时理解了这些概念，您是否能够自己解决问题，或者在继续之前是否需要查看解决方案，这都没有太大关系。
编写以下程序：要求用户输入 2 个浮点数（使用双精度）。然后要求用户输入以下数学符号之一：+、-、* 或 /。程序计算用户输入的两个数字的答案并打印结果。如果用户输入无效符号，程序应不打印任何内容。
程序示例
Enter a double value: 6.2
Enter a double value: 5
Enter +, -, *, or /: *
6.2 * 5 is 31
显示提示
提示：编写三个函数：一个获取双精度值，一个获取算术符号，一个计算并打印答案。
显示提示
提示：使用 if 语句和
operator==
将用户输入与所需的算术符号进行比较。
显示提示
提示：如果用户没有传入受支持的操作，请考虑使用早期返回（在
4.10 -- if 语句简介
课程中介绍）。
显示答案
#include <iostream>

double getDouble()
{
    std::cout << "Enter a double value: ";
    double x{};
    std::cin >> x;
    return x;
}

char getOperator()
{
    std::cout << "Enter +, -, *, or /: ";
    char operation{};
    std::cin >> operation;
    return operation;
}

void printResult(double x, char operation, double y)
{
    double result{};

    if (operation == '+')
        result = x + y;
    else if (operation == '-')
        result = x - y;
    else if (operation == '*')
        result = x * y;
    else if (operation == '/')
        result = x / y;
    else        // if the user did not pass in a supported operation
        return; // early return

    std::cout << x << ' ' << operation << ' ' << y << " is " << result << '\n';
}

int main()
{
    double x { getDouble() };
    double y { getDouble() };

    char operation { getOperator() };

    printResult(x, operation, y);

    return 0;
}
问题 #3
额外加分：这个有点挑战性。
编写一个短程序来模拟球从塔上掉落。首先，应要求用户输入塔的高度（以米为单位）。假设正常重力（9.8 m/s
2
），并且球没有初始速度（球开始时未移动）。让程序输出球在 0、1、2、3、4 和 5 秒后离地面的高度。球不应落到地面以下（高度 0）。
使用函数计算球在 x 秒后的高度。该函数可以使用以下公式计算球在 x 秒后下落的距离：下落距离 = 重力常数 * x 秒
2
/ 2
预期输出
Enter the height of the tower in meters: 100
At 0 seconds, the ball is at height: 100 meters
At 1 seconds, the ball is at height: 95.1 meters
At 2 seconds, the ball is at height: 80.4 meters
At 3 seconds, the ball is at height: 55.9 meters
At 4 seconds, the ball is at height: 21.6 meters
At 5 seconds, the ball is on the ground.
注意：根据塔的高度，球可能在 5 秒内未到达地面——这没关系。我们将在学习循环后改进此程序。
注意：
^
符号在 C++ 中不是幂运算符。使用乘法而不是幂运算来实现公式。
注意：记住对双精度数使用双精度字面量，例如
2.0
而不是
2
。
显示答案
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
	double gravity { 9.8 };
    
	// Using formula: s = (u * t) + (a * t^2) / 2
	// here u (initial velocity) = 0, so (u * t) = 0
	double fallDistance { gravity * (seconds * seconds) / 2.0 };
	double ballHeight { towerHeight - fallDistance };

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
	double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);
}

int main()
{
	double towerHeight{ getTowerHeight() };

	calculateAndPrintBallHeight(towerHeight, 0);
	calculateAndPrintBallHeight(towerHeight, 1);
	calculateAndPrintBallHeight(towerHeight, 2);
	calculateAndPrintBallHeight(towerHeight, 3);
	calculateAndPrintBallHeight(towerHeight, 4);
	calculateAndPrintBallHeight(towerHeight, 5);
       
	return 0;
}
对于此程序，我们有 3 个任务：获取初始塔高，计算球的当前高度，并打印球的当前高度。根据函数应该只做一件事的最佳实践，我们为每个任务设置了不同的函数。
calculateAndPrintBallHeight()
是一个辅助函数，它使从
main()
调用时计算和打印高度更具可读性。
下一课
5.1
常量变量（命名常量）
返回目录
上一课
4.12
类型转换和 static_cast 简介