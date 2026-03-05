# 3.x — 第 3 章总结和测验

3.x — 第 3 章总结和测验
Alex
2019 年 2 月 1 日，太平洋标准时间 12:04
2024 年 8 月 13 日
章节回顾
语法错误
是指您编写的语句不符合 C++ 语言语法规则时发生的错误。编译器将捕获这些错误。
当语句在语法上有效，但没有实现程序员的预期目的时，就会发生
语义错误
。
从程序中查找和删除错误的过程称为
调试
。
我们可以使用五步法来处理调试
找到根本原因。
理解问题。
确定修复方案。
修复问题。
重新测试。
发现错误通常是调试中最难的部分。
静态分析工具
是分析您的代码并查找可能指示代码存在问题的语义问题的工具。
能够可靠地重现问题是调试的第一步也是最重要的一步。
我们可以使用多种策略来帮助发现问题
注释掉代码。
使用输出语句验证您的代码流。
打印值。
当使用打印语句进行调试时，请使用
std::cerr
而不是
std::cout
。但更好的是，避免通过打印语句进行调试。
日志文件
是记录程序中发生的事件的文件。将信息写入日志文件的过程称为
日志记录
。
在不改变代码行为的情况下重构代码的过程称为
重构
。这通常是为了使您的程序更有组织、更模块化或性能更好。
单元测试
是一种软件测试方法，通过该方法测试源代码的小单元以确定它们是否正确。
防御性编程
是一种技术，程序员试图预测软件可能被滥用的所有方式。这些滥用通常可以被检测和缓解。
程序中跟踪的所有信息（变量值、已调用的函数、当前的执行点）都属于
程序状态
。
调试器
是一种工具，允许程序员控制程序的执行方式并在程序运行时检查程序状态。
集成调试器
是一种集成到代码编辑器中的调试器。
单步执行
是一组相关的调试功能，允许您逐语句地单步执行代码。
步进
执行程序正常执行路径中的下一条语句，然后暂停执行。如果该语句包含函数调用，则
步进
会使程序跳转到被调用函数的顶部。
步过
执行程序正常执行路径中的下一条语句，然后暂停执行。如果该语句包含函数调用，则
步过
会执行该函数并在函数执行后将控制权返回给您。
步出
执行当前正在执行的函数中的所有剩余代码，然后在函数返回时将控制权返回给您。
运行到光标
执行程序，直到执行到达鼠标光标选择的语句。
继续
运行程序，直到程序终止或命中断点。
启动
与继续相同，只是从程序的开头开始。
断点
是一个特殊标记，它告诉调试器在到达断点时停止程序的执行。
设置下一条语句
命令允许我们改变执行点到其他语句（有时非正式地称为跳转）。这可以用来向前跳转执行点并跳过一些本应执行的代码，或者向后跳转并让已经执行的代码再次运行。
监视变量
允许您在调试模式下程序执行时检查变量的值。
监视窗口
允许您检查变量或表达式的值。
调用堆栈
是已执行以到达当前执行点的所有活动函数的列表。
调用堆栈窗口
是显示调用堆栈的调试器窗口。
小测验时间
问题 #1
以下程序旨在将两个数字相加，但无法正常工作。
使用集成调试器逐步执行此程序并监视 x 的值。根据您了解的信息，修复以下程序
#include <iostream>

int readNumber(int x)
{
	std::cout << "Please enter a number: ";
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "The sum is: " << x << '\n';
}

int main()
{
	int x {};
	readNumber(x);
	x = x + readNumber(x);
	writeAnswer(x);

	return 0;
}
显示答案
这里的主要问题是函数
main
的第二行——readNumber 的返回值没有赋给任何东西，所以它被丢弃了。一个小问题是
readNumber
在应该有一个局部变量时却带了一个参数。
#include <iostream>

int readNumber()
{
	std::cout << "Please enter a number: ";
	int x {};
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "The sum is: " << x << '\n';
}

int main()
{
	int x { readNumber() };
	x = x + readNumber();
	writeAnswer(x);

	return 0;
}
问题 #2
以下程序旨在将两个数字相除，但无法正常工作。
使用集成调试器逐步执行此程序。对于输入，输入 8 和 4。根据您了解的信息，修复以下程序
#include <iostream>

int readNumber()
{
	std::cout << "Please enter a number: ";
	int x {};
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "The quotient is: " << x << '\n';
}

int main()
{
	int x{ };
	int y{ };
	x = readNumber();
	x = readNumber();
	writeAnswer(x/y);

	return 0;
}
显示答案
这里的问题是第二次调用
readNumber
不小心将其值赋给了 x 而不是 y，导致除以 0，从而导致未定义行为。
#include <iostream>

int readNumber()
{
	std::cout << "Please enter a number: ";
	int x {};
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "The quotient is: " << x << '\n';
}

int main()
{
	int x{ readNumber() };
	int y{ readNumber() };
	writeAnswer(x/y);

	return 0;
}
您可能会注意到，当第二个输入不能被第一个输入整除时，此程序似乎会产生不正确的结果。当对整数进行除法运算时，C++ 将丢弃商的任何小数部分。我们将在第
6.2 — 算术运算符
课中更详细地讨论这一点。
问题 #3
当执行点在第 4 行时，以下程序中的调用堆栈是什么样子的？本次练习只需要函数名称，不需要指示返回点的行号。
我们在第
3.9 — 使用集成调试器：调用堆栈
课中讨论了调用堆栈。
#include <iostream>

void d()
{ // here
}

void c()
{
}

void b()
{
	c();
	d();
}

void a()
{
	b();
}

int main()
{
	a();

	return 0;
}
显示答案
d
b
a
main
问题 #4
额外加分：以下程序旨在将两个数字相加，但无法正常工作。
使用集成调试器逐步执行此程序。对于输入，输入 8 和 4。根据您了解的信息，修复以下程序
#include <iostream>

int readNumber()
{
    std::cout << "Please enter a number: ";
    char x{};
    std::cin >> x;
    
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The sum is: " << x << '\n';
}

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x + y);

    return 0;
}
显示答案
问题出在第 6 行的 `char` 数据类型。当我们输入数字值 8 时，它不会存储为值 `8`，而是存储为 `56`。当我们输入数字值 4 时，它不会存储为值 `4`，而是存储为 `52`。因此，`readNumber()` 函数返回 `56` 和 `52`，而不是预期的 `8` 和 `4`。
解决方案是将第 6 行的数据类型从 `char` 更改为 `int`。
作者注
鉴于目前所涉及的材料有限，很难找到具有非显而易见问题的简单程序的良好示例进行调试。各位读者有什么建议吗？
下一课
4.1
基本数据类型介绍
返回目录
上一课
3.10
在问题发生之前发现它们