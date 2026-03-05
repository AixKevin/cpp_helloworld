# 11.x — 第 11 章总结与测验

11.x — 第 11 章总结与测验
Alex
2023 年 12 月 28 日，太平洋标准时间下午 5:30
2024 年 9 月 28 日
干得好。函数模板可能看起来很复杂，但它们是使代码与不同类型的对象一起工作的强大方法。我们将在未来的章节中看到更多模板内容，所以请系好安全带。
章节回顾
函数重载
允许我们创建多个同名函数，只要每个同名函数具有不同的参数类型集（或函数可以以其他方式区分）。这样的函数称为
重载函数
（或简称
重载
）。返回类型不用于区分。
在解析重载函数时，如果找不到精确匹配，编译器将优先选择可以通过数值提升匹配的重载函数，而不是那些需要数值转换的函数。当对已重载的函数进行函数调用时，编译器将尝试根据函数调用中使用的参数将函数调用与适当的重载匹配。这称为
重载解析
。
当编译器找到两个或更多个函数可以匹配对重载函数的函数调用并且无法确定哪个是最佳函数时，就会发生
模糊匹配
。
默认参数
是为函数参数提供的默认值。带有默认参数的参数必须始终是最右边的参数，并且在解析重载函数时它们不用于区分函数。
函数模板
允许我们创建一种函数式的定义，作为创建相关函数的模式。在函数模板中，我们使用
类型模板参数
作为占位符，用于稍后指定的任何类型。告诉编译器我们正在定义模板并声明模板类型的语法称为
模板参数声明
。
从函数模板（带有模板类型）创建函数（带有特定类型）的过程称为
函数模板实例化
（或简称
实例化
）。当这个过程由于函数调用而发生时，它被称为
隐式实例化
。一个被实例化的函数称为
函数实例
（或简称
实例
，有时也称为
模板函数
）。
模板参数推导
允许编译器根据函数调用的参数推导出应该用于实例化函数的实际类型。模板参数推导不进行类型转换。
模板类型有时被称为
泛型类型
，使用模板进行编程有时被称为
泛型编程
。
在 C++20 中，当 `auto` 关键字在普通函数中用作参数类型时，编译器会自动将该函数转换为函数模板，其中每个 `auto` 参数都成为一个独立的模板类型参数。这种创建函数模板的方法称为
缩写函数模板
。
非类型模板参数
是具有固定类型的模板参数，用作作为模板参数传入的 constexpr 值的占位符。
小测验时间
问题 #1
1a) 此程序的输出是什么，为什么？
#include <iostream>

void print(int x)
{
    std::cout << "int " << x << '\n';
}

void print(double x)
{
    std::cout << "double " << x << '\n';
}

int main()
{
    short s { 5 };
    print(s);

    return 0;
}
显示答案
输出是 `int 5`。将 `short` 转换为 `int` 是数值提升，而将 `short` 转换为 `double` 是数值转换。编译器将优先选择数值提升而不是数值转换。
1b) 为什么以下代码无法编译？
#include <iostream>

void print()
{
    std::cout << "void\n";
}

void print(int x=0)
{
    std::cout << "int " << x << '\n';
}

void print(double x)
{
    std::cout << "double " << x << '\n';
}

int main()
{
    print(5.0f);
    print();

    return 0;
}
显示答案
因为带有默认参数的参数不计入重载函数的解析，所以编译器无法判断 `print()` 的调用应该解析到 `print()` 还是 `print(int x=0)`。
1c) 为什么以下代码无法编译？
#include <iostream>

void print(long x)
{
    std::cout << "long " << x << '\n';
}

void print(double x)
{
    std::cout << "double " << x << '\n';
}

int main()
{
    print(5);

    return 0;
}
显示答案
字面量 5 是一个 `int`。将 `int` 转换为 `long` 或 `double` 是数值转换，编译器将无法确定哪个函数是更好的匹配。
问题 #2
> 步骤 #1
编写一个名为 `add()` 的函数模板，允许用户添加两个相同类型的值。以下程序应该运行
#include <iostream>

// write your add function template here

int main()
{
	std::cout << add(2, 3) << '\n';
	std::cout << add(1.2, 3.4) << '\n';

	return 0;
}
并产生以下输出
5
4.6
显示答案
#include <iostream>

template <typename T>
T add(T x, T y)
{
	return x + y;
}

int main()
{
	std::cout << add(2, 3) << '\n';
	std::cout << add(1.2, 3.4) << '\n';

	return 0;
}
> 步骤 #2
编写一个名为 `mult()` 的函数模板，允许用户将任意类型（第一个参数）的值与整数（第二个参数）相乘。第二个参数不应是模板类型。函数应返回与第一个参数相同的类型。以下程序应该运行
#include <iostream>

// write your mult function template here

int main()
{
	std::cout << mult(2, 3) << '\n';
	std::cout << mult(1.2, 3) << '\n';

	return 0;
}
并产生以下输出
6
3.6
显示答案
#include <iostream>

template <typename T>
T mult(T x, int y)
{
	return x * y;
}

int main()
{
	std::cout << mult(2, 3) << '\n';
	std::cout << mult(1.2, 3) << '\n';

	return 0;
}
> 步骤 #3
编写一个名为 `sub()` 的函数模板，允许用户减去两个不同类型的值。以下程序应该运行
#include <iostream>

// write your sub function template here

int main()
{
	std::cout << sub(3, 2) << '\n';
	std::cout << sub(3.5, 2) << '\n';
	std::cout << sub(4, 1.5) << '\n';

	return 0;
}
并产生以下输出
1
1.5
2.5
显示答案
#include <iostream>

template <typename T, typename U>
auto sub(T x, U y)
{
	return x - y;
}

/* 
//If C++20 capable, you can use an abbreviated function template instead
auto sub(auto x, auto y)
{
	return x - y;
}
*/

int main()
{
	std::cout << sub(3, 2) << '\n';
	std::cout << sub(3.5, 2) << '\n';
	std::cout << sub(4, 1.5) << '\n';

	return 0;
}
问题 #3
此程序的输出是什么，为什么？
#include <iostream>

template <typename T>
int count(T) // This is the same as int count(T x), except we're not giving the parameter a name since we don't use the parameter
{
    static int c { 0 };
    return ++c;
}

int main()
{
    std::cout << count(1) << '\n';
    std::cout << count(1) << '\n';
    std::cout << count(2.3) << '\n';
    std::cout << count<double>(1) << '\n';
    
    return 0;
}
显示答案
1
2
1
2
当调用 `count(1)` 时，编译器将实例化函数 `count
(int)` 并调用它。这将返回值 `1`。
当再次调用 `count(1)` 时，编译器将看到 `count
(int)` 已经存在，并再次调用它。这将返回值 `2`。
当调用 `count(2.3)` 时，编译器将实例化原型为 `count
(double)` 的函数并调用它。这是一个具有自己 `static c` 变量的新函数，因此它将返回值 `1`。
当调用 `count
(1)` 时，编译器将看到我们正在显式请求 `count()` 的 `double` 版本。由于之前的语句，此函数已经存在，因此将调用 `count
(double)`，并将 `int` 参数隐式转换为 `double`。此函数将返回值 `2`。
问题 #4
此程序的输出是什么？
#include <iostream>

int foo(int n)
{
    return n + 10;
}

template <typename T>
int foo(T n)
{
    return n;
}

int main()
{
    std::cout << foo(1) << '\n'; // #1

    short s { 2 };
    std::cout << foo(s) << '\n'; // #2
    
    std::cout << foo<int>(4) << '\n'; // #3

    std::cout << foo<int>(s) << '\n'; // #4

    std::cout << foo<>(6) << '\n'; // #5
    
    return 0;
}
显示答案
11
2
4
2
6
在情况 1 中，`foo(1)` 与 `foo(int)` 精确匹配，因此调用非模板函数 `foo(int)`。
在情况 2 中，`foo(s)` 不与非模板函数 `foo(int)` 精确匹配，但参数 `s` 可以转换为 `int`，因此 `foo(int)` 是一个候选。然而，编译器将更倾向于使用函数模板 `foo
(T)` 来实例化精确匹配的 `foo
(short)`。因此这会调用 `foo
(short)`。
在情况 3 中，`foo
(4)` 是对 `foo
` 的显式调用，因此不考虑 `foo(int)`。编译器实例化 `foo
(int)` 并调用它。
在情况 4 中，这同样是对 `foo
` 的显式调用。编译器将参数 `s` 提升为 `int` 以匹配参数。
在情况 5 中，此语法只匹配函数模板，因此不考虑 `foo(int)`。调用 `foo
(int)`。
下一课
F.1
Constexpr 函数
返回目录
上一课
11.10
在多个文件中使用函数模板