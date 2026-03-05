# 21.2 — 使用友元函数重载算术运算符

21.2 — 使用友元函数重载算术运算符
Alex
2007年9月26日，太平洋夏令时上午11:36
2024年10月21日
C++ 中最常用的运算符之一是算术运算符——即加法运算符 (+)、减法运算符 (-)、乘法运算符 (*) 和除法运算符 (/)。请注意，所有算术运算符都是二元运算符——这意味着它们接受两个操作数——运算符的每一侧一个。这四个运算符都以完全相同的方式重载。
事实证明，重载运算符有三种不同的方式：成员函数方式、友元函数方式和普通函数方式。在本课中，我们将介绍友元函数方式（因为它对于大多数二元运算符来说更直观）。下一课，我们将讨论普通函数方式。最后，在本章后面的课程中，我们将介绍成员函数方式。当然，我们还将更详细地总结何时使用每种方式。
使用友元函数重载运算符
考虑以下类
class Cents
{
private:
	int m_cents {};

public:
	Cents(int cents) : m_cents{ cents } { }
	int getCents() const { return m_cents; }
};
以下示例展示了如何重载加法运算符 (+) 以将两个“Cents”对象相加
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	Cents(int cents) : m_cents{ cents } { }

	// add Cents + Cents using a friend function
	friend Cents operator+(const Cents& c1, const Cents& c2);

	int getCents() const { return m_cents; }
};

// note: this function is not a member function!
Cents operator+(const Cents& c1, const Cents& c2)
{
	// use the Cents constructor and operator+(int, int)
	// we can access m_cents directly because this is a friend function
	return c1.m_cents + c2.m_cents;
}

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 8 };
	Cents centsSum{ cents1 + cents2 };
	std::cout << "I have " << centsSum.getCents() << " cents.\n";

	return 0;
}
这会产生结果
I have 14 cents.
重载加法运算符 (+) 就像声明一个名为 operator+ 的函数一样简单，为其提供两个我们想要相加的操作数类型的参数，选择一个适当的返回类型，然后编写函数。
在我们的 Cents 对象的情况下，实现我们的 operator+() 函数非常简单。首先，参数类型：在这个版本的 operator+ 中，我们将把两个 Cents 对象相加，所以我们的函数将接受两个 Cents 类型的对象。其次，返回类型：我们的 operator+ 将返回 Cents 类型的结果，所以这就是我们的返回类型。
最后是实现：要将两个 Cents 对象相加，我们真正需要做的是将每个 Cents 对象的 m_cents 成员相加。因为我们重载的 operator+() 函数是该类的友元，所以我们可以直接访问我们参数的 m_cents 成员。此外，因为 m_cents 是一个整数，并且 C++ 知道如何使用适用于整数操作数的内置加法运算符将整数相加，所以我们可以简单地使用 + 运算符进行相加。
重载减法运算符 (-) 也同样简单
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// add Cents + Cents using a friend function
	friend Cents operator+(const Cents& c1, const Cents& c2);

	// subtract Cents - Cents using a friend function
	friend Cents operator-(const Cents& c1, const Cents& c2);

	int getCents() const { return m_cents; }
};

// note: this function is not a member function!
Cents operator+(const Cents& c1, const Cents& c2)
{
	// use the Cents constructor and operator+(int, int)
	// we can access m_cents directly because this is a friend function
	return Cents { c1.m_cents + c2.m_cents };
}

// note: this function is not a member function!
Cents operator-(const Cents& c1, const Cents& c2)
{
	// use the Cents constructor and operator-(int, int)
	// we can access m_cents directly because this is a friend function
	return Cents { c1.m_cents - c2.m_cents };
}

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 2 };
	Cents centsSum{ cents1 - cents2 };
	std::cout << "I have " << centsSum.getCents() << " cents.\n";

	return 0;
}
重载乘法运算符 (*) 和除法运算符 (/) 就像分别定义 `operator*` 和 `operator/` 函数一样简单。
友元函数可以在类内部定义
尽管友元函数不是类的成员，但如果需要，它们仍然可以在类内部定义
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// add Cents + Cents using a friend function
        // This function is not considered a member of the class, even though the definition is inside the class
	friend Cents operator+(const Cents& c1, const Cents& c2)
	{
		// use the Cents constructor and operator+(int, int)
		// we can access m_cents directly because this is a friend function
		return Cents { c1.m_cents + c2.m_cents };
	}

	int getCents() const { return m_cents; }
};

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 8 };
	Cents centsSum{ cents1 + cents2 };
	std::cout << "I have " << centsSum.getCents() << " cents.\n";

	return 0;
}
这对于具有简单实现的重载运算符来说是没问题的。
为不同类型的操作数重载运算符
通常情况下，您希望重载的运算符能够处理不同类型的操作数。例如，如果我们有 Cents(4)，我们可能希望将其与整数 6 相加，得到结果 Cents(10)。
当 C++ 评估表达式 `x + y` 时，x 成为第一个参数，y 成为第二个参数。当 x 和 y 具有相同类型时，无论是 x + y 还是 y + x 都无关紧要——无论哪种方式，都会调用相同版本的 operator+。但是，当操作数具有不同类型时，x + y 不会调用与 y + x 相同的函数。
例如，`Cents(4) + 6` 将调用 operator+(Cents, int)，而 `6 + Cents(4)` 将调用 operator+(int, Cents)。因此，每当我们为不同类型的操作数重载二元运算符时，我们实际上需要编写两个函数——每种情况一个。以下是一个示例
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// add Cents + int using a friend function
	friend Cents operator+(const Cents& c1, int value);

	// add int + Cents using a friend function
	friend Cents operator+(int value, const Cents& c1);


	int getCents() const { return m_cents; }
};

// note: this function is not a member function!
Cents operator+(const Cents& c1, int value)
{
	// use the Cents constructor and operator+(int, int)
	// we can access m_cents directly because this is a friend function
	return Cents { c1.m_cents + value };
}

// note: this function is not a member function!
Cents operator+(int value, const Cents& c1)
{
	// use the Cents constructor and operator+(int, int)
	// we can access m_cents directly because this is a friend function
	return Cents { c1.m_cents + value };
}

int main()
{
	Cents c1{ Cents{ 4 } + 6 };
	Cents c2{ 6 + Cents{ 4 } };

	std::cout << "I have " << c1.getCents() << " cents.\n";
	std::cout << "I have " << c2.getCents() << " cents.\n";

	return 0;
}
请注意，这两个重载函数具有相同的实现——这是因为它们执行相同的操作，只是以不同的顺序接受参数。
另一个例子
让我们看另一个例子
#include <iostream>

class MinMax
{
private:
	int m_min {}; // The min value seen so far
	int m_max {}; // The max value seen so far

public:
	MinMax(int min, int max)
		: m_min { min }, m_max { max }
	{ }

	int getMin() const { return m_min; }
	int getMax() const { return m_max; }

	friend MinMax operator+(const MinMax& m1, const MinMax& m2);
	friend MinMax operator+(const MinMax& m, int value);
	friend MinMax operator+(int value, const MinMax& m);
};

MinMax operator+(const MinMax& m1, const MinMax& m2)
{
	// Get the minimum value seen in m1 and m2
	int min{ m1.m_min < m2.m_min ? m1.m_min : m2.m_min };

	// Get the maximum value seen in m1 and m2
	int max{ m1.m_max > m2.m_max ? m1.m_max : m2.m_max };

	return MinMax { min, max };
}

MinMax operator+(const MinMax& m, int value)
{
	// Get the minimum value seen in m and value
	int min{ m.m_min < value ? m.m_min : value };

	// Get the maximum value seen in m and value
	int max{ m.m_max > value ? m.m_max : value };

	return MinMax { min, max };
}

MinMax operator+(int value, const MinMax& m)
{
	// calls operator+(MinMax, int)
	return m + value;
}

int main()
{
	MinMax m1{ 10, 15 };
	MinMax m2{ 8, 11 };
	MinMax m3{ 3, 12 };

	MinMax mFinal{ m1 + m2 + 5 + 8 + m3 + 16 };

	std::cout << "Result: (" << mFinal.getMin() << ", " <<
		mFinal.getMax() << ")\n";

	return 0;
}
MinMax 类跟踪它迄今为止看到的最大和最小值。我们已经重载了 + 运算符 3 次，以便我们可以将两个 MinMax 对象相加，或将整数添加到 MinMax 对象。
这个例子产生了以下结果
Result: (3, 16)
您会注意到这是我们添加到 mFinal 的最小值和最大值。
让我们多谈谈“MinMax mFinal { m1 + m2 + 5 + 8 + m3 + 16 }”是如何评估的。请记住，operator+ 从左到右评估，所以 m1 + m2 首先评估。这变成了一个对 operator+(m1, m2) 的调用，它产生返回值 MinMax(8, 15)。然后 MinMax(8, 15) + 5 接下来评估。这变成了一个对 operator+(MinMax(8, 15), 5) 的调用，它产生返回值 MinMax(5, 15)。然后 MinMax(5, 15) + 8 以相同的方式评估，产生 MinMax(5, 15)。然后 MinMax(5, 15) + m3 评估，产生 MinMax(3, 15)。最后，MinMax(3, 15) + 16 评估，产生 MinMax(3, 16)。这个最终结果然后用于初始化 mFinal。
换句话说，这个表达式的计算结果为“MinMax mFinal = (((((m1 + m2) + 5) + 8) + m3) + 16)”，每个后续操作都返回一个 MinMax 对象，该对象成为后续运算符的左侧操作数。
使用其他运算符实现运算符
在上面的例子中，请注意我们通过调用 operator+(MinMax, int) 定义了 operator+(int, MinMax) (这会产生相同的结果)。这使得我们可以将 operator+(int, MinMax) 的实现减少到一行，通过最小化冗余和使函数更易于理解来使我们的代码更易于维护。
通常可以通过调用其他重载运算符来定义重载运算符。如果这样做能产生更简单的代码，您就应该这样做。在实现微不足道（例如，单行）的情况下，这样做可能值得也可能不值得。
小测验时间
问题 #1
a) 编写一个名为 Fraction 的类，该类具有一个整数分子和分母成员。编写一个打印分数的 print() 函数。
以下代码应该能够编译
#include <iostream>

int main()
{
    Fraction f1{ 1, 4 };
    f1.print();

    Fraction f2{ 1, 2 };
    f2.print();

    return 0;
}
这应该打印
1/4
1/2
显示答案
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
	explicit Fraction(int numerator, int denominator=1)
		: m_numerator{numerator}, m_denominator{denominator}
	{
	}

	void print() const
	{
		std::cout << m_numerator << '/' << m_denominator << '\n';
	}
};

int main()
{
	Fraction f1 {1, 4};
	f1.print();
	
	Fraction f2 {1, 2};
	f2.print();

	return 0;
}
b) 添加重载的乘法运算符，以处理分数与整数之间以及两个分数之间的乘法。使用友元函数方法。
提示：要乘以两个分数，首先将两个分子相乘，然后将两个分母相乘。要乘以一个分数和一个整数，将分数的分子乘以整数，分母保持不变。
以下代码应该能够编译
#include <iostream>

int main()
{
    Fraction f1{2, 5};
    f1.print();

    Fraction f2{3, 8};
    f2.print();

    Fraction f3{ f1 * f2 };
    f3.print();

    Fraction f4{ f1 * 2 };
    f4.print();

    Fraction f5{ 2 * f2 };
    f5.print();

    Fraction f6{ Fraction{1, 2} * Fraction{2, 3} * Fraction{3, 4} };
    f6.print();

    return 0;
}
这应该打印
2/5
3/8
6/40
4/5
6/8
6/24
显示答案
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
	explicit Fraction(int numerator, int denominator=1)
		: m_numerator{numerator}, m_denominator{denominator}
	{
	}

	// We don't want to pass by value, because copying is slow.
	// We can't and shouldn't pass by non-const reference, because then
	// our functions wouldn't work with r-values.
	friend Fraction operator*(const Fraction& f1, const Fraction& f2);
	friend Fraction operator*(const Fraction& f1, int value);
	friend Fraction operator*(int value, const Fraction& f1);

	void print() const
	{
		std::cout << m_numerator << '/' << m_denominator << '\n';
	}
};

Fraction operator*(const Fraction& f1, const Fraction& f2)
{
	return Fraction { f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}

Fraction operator*(const Fraction& f1, int value)
{
	return Fraction { f1.m_numerator * value, f1.m_denominator };
}

Fraction operator*(int value, const Fraction& f1)
{
	return Fraction { f1 * value };
}

int main()
{
	Fraction f1{2, 5};
	f1.print();

	Fraction f2{3, 8};
	f2.print();

	Fraction f3{ f1 * f2 };
	f3.print();

	Fraction f4{ f1 * 2 };
	f4.print();

	Fraction f5{ 2 * f2 };
	f5.print();

	Fraction f6{ Fraction{1, 2} * Fraction{2, 3} * Fraction{3, 4} };
	f6.print();

	return 0;
}
c) 如果我们将构造函数设为非 explicit 并从之前的解决方案中移除整数乘法运算符，程序为什么仍能正常工作？
// Remove explicit from constructor
	Fraction(int numerator, int denominator=1)
		: m_numerator{numerator}, m_denominator{denominator}
	{
	}

// We can remove these operators, and the program continues to work
Fraction operator*(const Fraction& f1, int value);
Fraction operator*(int value, const Fraction& f1);
显示答案
我们仍然有
Fraction operator*(const Fraction& f1, const Fraction& f2)
当我们用整数乘以分数时，例如
Fraction f5{ 2 * f2 };
非 `explicit Fraction(int, int)` 构造函数将用于从 2 构造一个新的 `Fraction`。然后，这个新的 `Fraction` 会通过 `Fraction * Fraction` 运算符与 `f2` 相乘。
因为这需要将 `2` 转换为 `Fraction`，所以这比带有整数乘法重载运算符的实现略慢。
d) 如果我们将 `operator*(Fraction, Fraction)` 的引用参数设为非 const，则 `main` 函数中的以下行将不再起作用。为什么？
// The non-const multiplication operator looks like this
Fraction operator*(Fraction& f1, Fraction& f2)

// This doesn't work anymore
Fraction f6{ Fraction{1, 2} * Fraction{2, 3} * Fraction{3, 4} };
显示答案
我们正在乘以临时 `Fraction` 对象，但是非 const 引用不能绑定到临时对象。
e) 额外加分：分数 2/4 与 1/2 相同，但 2/4 未约分至最低项。我们可以通过找到分子和分母的最大公约数 (GCD)，然后用 GCD 同时除分子和分母，将任何给定分数约分至最低项。
`std::gcd()` 在 C++17 中添加到标准库中（在 <numeric> 头文件中）。
如果您使用的是较旧的编译器，可以使用此函数查找 GCD
#include <cmath> // for std::abs

int gcd(int a, int b) {
    return (b == 0) ? std::abs(a) : gcd(b, a % b);
}
编写一个名为 reduce() 的成员函数，用于约简你的分数。确保所有分数都正确约简。
以下内容应该可以编译
#include <iostream>

int main()
{
    Fraction f1{2, 5};
    f1.print();

    Fraction f2{3, 8};
    f2.print();

    Fraction f3{ f1 * f2 };
    f3.print();

    Fraction f4{ f1 * 2 };
    f4.print();

    Fraction f5{ 2 * f2 };
    f5.print();

    Fraction f6{ Fraction{1, 2} * Fraction{2, 3} * Fraction{3, 4} };
    f6.print();

    Fraction f7{0, 6};
    f7.print();

    return 0;
}
并产生结果
2/5
3/8
3/20
4/5
3/4
1/4
0/1
显示答案
#include <iostream>
#include <numeric> // for std::gcd

// This version of the Fraction class auto-reduces fractions
class Fraction
{
private:
	int m_numerator{ 0 };
	int m_denominator{ 1 };

public:
	explicit Fraction(int numerator, int denominator = 1)
		: m_numerator{ numerator }, m_denominator{ denominator }
	{
		// We put reduce() in the constructor to ensure any fractions we make get reduced!
		// Since all of the overloaded operators create new Fractions, we can guarantee this will get called here
		reduce();
	}

	void reduce()
	{
		int gcd{ std::gcd(m_numerator, m_denominator) };
		if (gcd) // Make sure we don't try to divide by 0
		{
			m_numerator /= gcd;
			m_denominator /= gcd;
		}
	}

	friend Fraction operator*(const Fraction& f1, const Fraction& f2);
	friend Fraction operator*(const Fraction& f1, int value);
	friend Fraction operator*(int value, const Fraction& f1);

	void print() const
	{
		std::cout << m_numerator << '/' << m_denominator << '\n';
	}
};

Fraction operator*(const Fraction& f1, const Fraction& f2)
{
	return Fraction { f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}

Fraction operator*(const Fraction& f1, int value)
{
	return Fraction { f1.m_numerator * value, f1.m_denominator };
}

Fraction operator*(int value, const Fraction& f1)
{
	return Fraction { f1 * value };
}

int main()
{
	Fraction f1{ 2, 5 };
	f1.print();

	Fraction f2{ 3, 8 };
	f2.print();

	Fraction f3{ f1 * f2 };
	f3.print();

	Fraction f4{ f1 * 2 };
	f4.print();

	Fraction f5{ 2 * f2 };
	f5.print();

	Fraction f6{ Fraction{1, 2} * Fraction{2, 3} * Fraction{3, 4} };
	f6.print();

	Fraction f7{ 0, 6 };
	f7.print();

	return 0;
}
下一课
21.3
使用普通函数重载运算符
返回目录
上一课
21.1
运算符重载简介