# 22.2 — 右值引用

22.2 — 右值引用
Alex
2017年2月20日 下午2:49 (太平洋标准时间)
2024年5月15日
在第12章中，我们介绍了值类别（
12.2 -- 值类别（左值和右值）
）的概念，它是表达式的一个属性，有助于确定表达式是解析为值、函数还是对象。我们还介绍了左值和右值，以便我们可以讨论左值引用。
如果您对左值和右值感到模糊，现在是温习该主题的好时机，因为我们将在本章中大量讨论它们。
左值引用回顾
在C++11之前，C++中只有一种类型的引用，因此它只被称为“引用”。然而，在C++11中，它被称为左值引用。左值引用只能用可修改的左值初始化。
左值引用
可初始化为
可修改
可修改的左值
是
是
不可修改的左值
否
否
右值
否
否
指向常量的左值引用可以与可修改和不可修改的左值以及右值进行初始化。然而，这些值不能被修改。
指向常量的左值引用
可初始化为
可修改
可修改的左值
是
否
不可修改的左值
是
否
右值
是
否
指向常量的左值引用特别有用，因为它们允许我们将任何类型的参数（左值或右值）传递给函数，而无需复制参数。
右值引用
C++11添加了一种新型的引用，称为右值引用。右值引用是一种旨在用右值（仅）初始化的引用。虽然左值引用使用单个&符号创建，但右值引用使用双&符号创建
int x{ 5 };
int& lref{ x }; // l-value reference initialized with l-value x
int&& rref{ 5 }; // r-value reference initialized with r-value 5
右值引用不能用左值初始化。
右值引用
可初始化为
可修改
可修改的左值
否
否
不可修改的左值
否
否
右值
是
是
指向常量的右值引用
可初始化为
可修改
可修改的左值
否
否
不可修改的左值
否
否
右值
是
否
右值引用有两个有用的特性。首先，右值引用将其初始化对象的生命周期延长到右值引用的生命周期（指向常量的左值引用也可以做到这一点）。其次，非常量右值引用允许您修改右值！
让我们看一些例子
#include <iostream>
 
class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };
 
public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
	}
 
	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1)
	{
		out << f1.m_numerator << '/' << f1.m_denominator;
		return out;
	}
};
 
int main()
{
	auto&& rref{ Fraction{ 3, 5 } }; // r-value reference to temporary Fraction
	
	// f1 of operator<< binds to the temporary, no copies are created.
	std::cout << rref << '\n';
 
	return 0;
} // rref (and the temporary Fraction) goes out of scope here
这个程序打印
3/5
作为匿名对象，Fraction(3, 5) 通常会在其定义表达式结束时超出作用域。然而，由于我们使用它初始化了一个右值引用，它的生命周期会延长到代码块的末尾。然后我们可以使用该右值引用打印 Fraction 的值。
现在我们来看一个不太直观的例子
#include <iostream>

int main()
{
    int&& rref{ 5 }; // because we're initializing an r-value reference with a literal, a temporary with value 5 is created here
    rref = 10;
    std::cout << rref << '\n';

    return 0;
}
这个程序打印
10
虽然用字面值初始化右值引用然后能够改变该值可能看起来很奇怪，但在用字面值初始化右值引用时，会从该字面值构造一个临时对象，以便该引用引用的是一个临时对象，而不是字面值。
右值引用在上述两种方式中都不是很常用。
作为函数参数的右值引用
右值引用更常被用作函数参数。这对于函数重载最有用，当您希望对左值和右值参数有不同的行为时。
#include <iostream>

void fun(const int& lref) // l-value arguments will select this function
{
	std::cout << "l-value reference to const: " << lref << '\n';
}

void fun(int&& rref) // r-value arguments will select this function
{
	std::cout << "r-value reference: " << rref << '\n';
}

int main()
{
	int x{ 5 };
	fun(x); // l-value argument calls l-value version of function
	fun(5); // r-value argument calls r-value version of function

	return 0;
}
这会打印
l-value reference to const: 5
r-value reference: 5
正如您所看到的，当传递一个左值时，重载函数解析为带有左值引用的版本。当传递一个右值时，重载函数解析为带有右值引用的版本（这被认为是比指向常量的左值引用更好的匹配）。
你为什么要这样做？我们将在下一课中更详细地讨论这个问题。毋庸置疑，它是移动语义的重要组成部分。
右值引用变量是左值
考虑以下代码片段
int&& ref{ 5 };
	fun(ref);
您期望上述代码调用哪个版本的
fun
：
fun(const int&)
还是
fun(int&&)
？
答案可能会让你感到惊讶。这调用的是
fun(const int&)
。
尽管变量
ref
的类型是
int&&
，但在表达式中使用时它是一个左值（所有命名变量都是左值）。对象的类型及其值类别是独立的。
您已经知道字面量
5
是
int
类型的右值，而
int x
是
int
类型的左值。同样，
int&& ref
是
int&&
类型的左值。
因此，
fun(ref)
不仅调用了
fun(const int&)
，甚至与
fun(int&&)
也不匹配，因为右值引用不能绑定到左值。
返回右值引用
您几乎不应该返回右值引用，原因与您几乎不应该返回左值引用相同。在大多数情况下，您最终会在函数结束时，当引用的对象超出作用域时返回一个悬空引用。
小测验时间
问题 #1
说明以下哪个带字母的语句将不会编译
int main()
{
	int x{};

	// l-value references
	int& ref1{ x }; // A
	int& ref2{ 5 }; // B

	const int& ref3{ x }; // C
	const int& ref4{ 5 }; // D

	// r-value references
	int&& ref5{ x }; // E
	int&& ref6{ 5 }; // F

	const int&& ref7{ x }; // G
	const int&& ref8{ 5 }; // H
	
	return 0;
}
显示答案
B、E和G不会编译。
绑定组合回顾
非const左值引用只能绑定到非const左值。
const左值引用可以绑定到非const左值、const左值和右值。
右值引用只能绑定到右值。
x
是一个非 const 左值，所以我们可以将非 const 左值引用 (A) 和 const 左值引用 (C) 绑定到它。我们不能将非 const 左值引用绑定到右值 (B)。
5
是一个右值，因此我们可以将一个 const 左值引用 (D) 和右值引用 (F & H) 绑定到它。我们不能将右值引用绑定到左值 (E & G)。
下一课
22.3
移动构造函数和移动赋值
返回目录
上一课
22.1
智能指针和移动语义简介