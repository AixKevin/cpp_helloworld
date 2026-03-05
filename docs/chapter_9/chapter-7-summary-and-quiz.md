# 7.x — 第 7 章总结和测验

7.x — 第 7 章总结和测验
Alex
2015年5月9日，太平洋夏令时上午11:06
2024年12月2日
章节回顾
本章我们涵盖了大量材料。干得好，你做得非常棒！
复合语句
或
块
是一组由零个或多个语句组成的集合，编译器将其视为单个语句。块以
{
符号开始，以
}
符号结束，要执行的语句置于两者之间。块可以在允许单个语句的任何地方使用。块末尾不需要分号。块通常与
if语句
结合使用，以执行多个语句。
用户自定义命名空间
是您为自己的声明定义的命名空间。C++提供的命名空间（例如
全局命名空间
）或库提供的命名空间（例如
namespace std
）不被视为用户自定义命名空间。
您可以通过
作用域解析运算符 (::)
访问命名空间中的声明。作用域解析运算符告诉编译器，右侧操作数指定的标识符应在左侧操作数的范围内查找。如果未提供左侧操作数，则假定为全局命名空间。
局部变量是在函数内定义的变量（包括函数参数）。局部变量具有
块作用域
，这意味着它们从定义点到其定义所在块的末尾都在作用域内。局部变量具有
自动存储期
，这意味着它们在定义点创建并在其定义所在块的末尾销毁。
在嵌套块中声明的名称可以
遮蔽
或
名称隐藏
外部块中同名变量。应避免这种情况。
全局变量是在函数外部定义的变量。全局变量具有
文件作用域
，这意味着它们从声明点到声明所在文件末尾都可见。全局变量具有
静态持续期
，这意味着它们在程序启动时创建并在程序结束时销毁。应尽可能避免静态变量的动态初始化。
标识符的
链接
决定了该名称的其他声明是否引用同一对象。局部变量没有链接。具有
内部链接
的标识符可以在单个文件内看到和使用，但无法从其他文件访问。具有
外部链接
的标识符可以在其定义所在的文件以及其他代码文件（通过前向声明）中看到和使用。
尽可能避免使用非const全局变量。const全局变量通常被认为是可接受的。如果您的编译器支持C++17，请为全局常量使用
内联变量
。
局部变量可以通过
static
关键字赋予静态持续期。
限定名
是包含关联作用域的名称（例如
std::string
）。
非限定名
是不包含作用域限定符的名称（例如
string
）。
using语句
（包括
using声明
和
using指令
）可用于避免必须使用显式命名空间限定标识符。
using声明
允许我们将非限定名（无作用域）用作限定名的别名。
using指令
将命名空间中的所有标识符导入到using指令的作用域中。通常应避免使用这两种方式。
内联展开
是一个过程，其中函数调用被替换为被调用函数的定义代码。使用
inline
关键字声明的函数称为
内联函数
。
内联函数和变量有两个主要要求：
编译器需要在每个使用内联函数或变量的翻译单元中看到其完整定义（仅有前向声明是不够的）。如果提供了前向声明，定义可以出现在使用点之后。
内联函数或变量的每个定义都必须相同，否则将导致未定义行为。
在现代C++中，术语inline已经演变为“允许多个定义”的含义。因此，内联函数是允许在多个文件中定义的函数。C++17引入了
内联变量
，它们是允许在多个文件中定义的变量。
内联函数和变量对于
仅头文件库
特别有用，后者是一个或多个实现某些功能的头文件（不包含.cpp文件）。
最后，C++支持
匿名命名空间
，它隐式地将命名空间的所有内容视为具有内部链接。C++还支持
内联命名空间
，它为命名空间提供了一些原始的版本控制功能。
小测验时间
问题 #1
修正以下程序
#include <iostream>

int main()
{
	std::cout << "Enter a positive number: ";
	int num{};
	std::cin >> num;


	if (num < 0)
		std::cout << "Negative number entered.  Making positive.\n";
		num = -num;

	std::cout << "You entered: " << num;

	return 0;
}
显示答案
#include <iostream>

int main()
{
	std::cout << "Enter a positive number: ";
	int num{};
	std::cin >> num;


	if (num < 0)
	{ // block needed here so both statements execute if num is < 0
		std::cout << "Negative number entered.  Making positive.\n";
		num = -num;
	}

	std::cout << "You entered: " << num;

	return 0;
}
问题 #2
编写一个名为constants.h的文件，使以下程序运行。如果您的编译器支持C++17，请使用内联constexpr变量。否则，使用普通的constexpr变量。
maxClassSize
的值应为
35
。
main.cpp
#include "constants.h"
#include <iostream>

int main()
{
	std::cout << "How many students are in your class? ";
	int students{};
	std::cin >> students;


	if (students > Constants::maxClassSize)
		std::cout << "There are too many students in this class";
	else
		std::cout << "This class isn't too large";

	return 0;
}
显示答案
constants.h
#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace Constants
{
	inline constexpr int maxClassSize{ 35 }; // remove inline keyword if not C++17 capable
}
#endif
main.cpp
#include "constants.h"
#include <iostream>

int main()
{
	std::cout << "How many students are in your class? ";
	int students{};
	std::cin >> students;


	if (students > Constants::maxClassSize)
		std::cout << "There are too many students in this class";
	else
		std::cout << "This class isn't too large";

	return 0;
}
问题 #3
编写一个函数
int accumulate(int x)
。此函数应返回已传递给此函数的所有
x
值的总和。
显示提示
提示：使用静态局部变量存储总和。
以下程序应运行并产生注释中所示的输出：
#include <iostream>

int main()
{
    std::cout << accumulate(4) << '\n'; // prints 4
    std::cout << accumulate(3) << '\n'; // prints 7
    std::cout << accumulate(2) << '\n'; // prints 9
    std::cout << accumulate(1) << '\n'; // prints 10

    return 0;
}
显示答案
#include <iostream>

int accumulate(int x)
{
    static int sum{ 0 }; // initialize sum to 0 at start of program
    sum += x;
    return sum;
}

int main()
{
    std::cout << accumulate(4) << '\n'; // prints 4
    std::cout << accumulate(3) << '\n'; // prints 7
    std::cout << accumulate(2) << '\n'; // prints 9
    std::cout << accumulate(1) << '\n'; // prints 10

    return 0;
}
3b) 额外加分：上述
accumulate()
函数有两个缺点是什么？
显示答案
没有常规方法可以在不重新启动程序的情况下重置累积。
没有常规方法可以同时运行多个累加器。
致进阶读者
这两个缺点都可以通过使用函子（
21.10 -- 重载括号运算符
）而不是静态局部变量来解决。
下一课
8.1
控制流简介
返回目录
上一课
7.14
匿名和内联命名空间