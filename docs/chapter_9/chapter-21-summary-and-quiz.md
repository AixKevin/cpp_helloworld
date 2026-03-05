# 21.x — 第 21 章总结与测验

21.x — 第 21 章总结与测验
Alex
2016 年 8 月 9 日，下午 2:44 PDT
2024 年 12 月 28 日
在本章中，我们探讨了与运算符重载、重载类型转换以及复制构造函数相关的主题。
总结
运算符重载是函数重载的一种变体，它允许你为你的类重载运算符。重载运算符时，运算符的意图应尽可能接近其原始意图。如果运算符应用于自定义类时的含义不明确或不直观，则应使用命名函数代替。
运算符可以作为普通函数、友元函数或成员函数进行重载。以下经验法则可以帮助你确定哪种形式最适合给定情况：
如果你正在重载赋值运算符 (=)、下标运算符 ([])、函数调用运算符 (()) 或成员选择运算符 (->)，则应将其作为成员函数进行重载。
如果你正在重载一元运算符，则应将其作为成员函数进行重载。
如果你正在重载修改其左操作数的二元运算符（例如 `operator+=`），如果可能，则应将其作为成员函数进行重载。
如果你正在重载不修改其左操作数的二元运算符（例如 `operator+`），则应将其作为普通函数或友元函数进行重载。
类型转换可以重载以提供转换函数，这些函数可用于将你的类显式或隐式转换为另一种类型。
复制构造函数是一种特殊类型的构造函数，用于从同类型的另一个对象初始化对象。复制构造函数用于从同类型对象进行直接/统一初始化、复制初始化 (`Fraction f = Fraction(5,3)`)，以及按值传递或返回参数时。
如果你不提供复制构造函数，编译器会为你创建一个。编译器提供的复制构造函数将使用逐成员初始化，这意味着副本的每个成员都从原始成员初始化。出于优化目的，复制构造函数可能会被省略，即使它有副作用，所以不要依赖你的复制构造函数实际执行。
构造函数默认被视为转换构造函数，这意味着编译器将使用它们将其他类型的对象隐式转换为你的类的对象。你可以通过在构造函数前面使用 `explicit` 关键字来避免这种情况。你还可以删除类中的函数，包括复制构造函数和重载的赋值运算符（如果需要）。如果调用已删除的函数，这将导致编译器错误。
赋值运算符可以重载，以允许赋值给你的类。如果你不提供重载的赋值运算符，编译器会为你创建一个。重载的赋值运算符应始终包含自赋值检查（除非它被自然处理，或者你正在使用复制和交换惯用法）。
新程序员经常混淆何时使用赋值运算符和复制构造函数，但它相当简单：
如果必须在复制发生之前创建新对象，则使用复制构造函数（注意：这包括按值传递或返回对象）。
如果无需在复制发生之前创建新对象，则使用赋值运算符。
默认情况下，编译器提供的复制构造函数和赋值运算符执行逐成员初始化或赋值，这是一种浅拷贝。如果你的类动态分配内存，这可能会导致问题，因为多个对象最终将指向相同的已分配内存。在这种情况下，你需要显式定义它们以进行深拷贝。更好的是，如果可以，避免自行管理内存，并使用标准库中的类。
小测验时间
问题 #1
假设 `Point` 是一个类，`point` 是该类的一个实例，以下运算符应使用普通/友元函数重载还是成员函数重载？
a) `point + point`
显示答案
二元 `operator+` 最好作为普通/友元函数实现。
b) `-point`
显示答案
一元 `operator-` 最好作为成员函数实现。
c) `std::cout << point`
显示答案
`operator<<` 必须作为普通/友元函数实现。
d) `point = 5;`
显示答案
`operator=` 必须作为成员函数实现。
问题 #2
编写一个名为 `Average` 的类，它将跟踪传递给它的所有整数的平均值。使用两个成员：第一个成员应为 `std::int32_t` 类型，用于跟踪到目前为止所有数字的总和。第二个成员应跟踪到目前为止已看到的数字数量。你可以将它们相除以找到平均值。
a) 编写以下程序运行所需的所有函数
int main()
{
	Average avg{};
	std::cout << avg << '\n';
	
	avg += 4;
	std::cout << avg << '\n'; // 4 / 1 = 4
	
	avg += 8;
	std::cout << avg << '\n'; // (4 + 8) / 2 = 6

	avg += 24;
	std::cout << avg << '\n'; // (4 + 8 + 24) / 3 = 12

	avg += -10;
	std::cout << avg << '\n'; // (4 + 8 + 24 - 10) / 4 = 6.5

	(avg += 6) += 10; // 2 calls chained together
	std::cout << avg << '\n'; // (4 + 8 + 24 - 10 + 6 + 10) / 6 = 7

	Average copy{ avg };
	std::cout << copy << '\n';

	return 0;
}
并生成结果
0
4
6
12
6.5
7
7
显示答案
#include <iostream>
#include <cstdint> // for fixed width integers

class Average
{
private:
	std::int32_t m_total{ 0 }; // the sum of all numbers we've seen so far
	int m_numbers{ 0 }; // the count of numbers we've seen so far

public:
	Average()
	{
	}

	friend std::ostream& operator<<(std::ostream& out, const Average& average)
	{
        // Handle case where we haven't seen any numbers yet
		if (average.m_numbers == 0)
		{
			out << 0;
			return out;
		}

		// Our average is the sum of the numbers we've seen divided by the count of the numbers we've seen
		// We need to remember to do a floating point division here, not an integer division
		out << static_cast<double>(average.m_total) / average.m_numbers;

		return out;
	}

	// Because operator+= modifies its left operand, we'll write it as a member
	Average& operator+=(std::int32_t num)
	{
		// Increment our total by the new number
		m_total += num;
		// And increase the count by 1
		++m_numbers;

		// return *this in case someone wants to chain +='s together
		return *this;
	}
};

int main()
{
	Average avg{};
	std::cout << avg << '\n';

	avg += 4;
	std::cout << avg << '\n';
	
	avg += 8;
	std::cout << avg << '\n';

	avg += 24;
	std::cout << avg << '\n';

	avg += -10;
	std::cout << avg << '\n';

	(avg += 6) += 10; // 2 calls chained together
	std::cout << avg << '\n';

	Average copy{ avg };
	std::cout << copy << '\n';

	return 0;
}
b) 你应该为这个类提供用户定义的复制构造函数或赋值运算符吗？
显示答案
不。因为这里使用逐成员初始化/复制是没问题的，所以使用编译器提供的默认值是可以接受的。
c) 为什么要使用 `std::int32_t` 而不是 `int`？
显示答案
`int` 在某些平台上可能是 16 位，这意味着我们的 `Average` 对象的最大分子值只能是 32,767。使用 `std::int32_t` 保证了 32 位整数值，这给了我们更大的范围来处理。
问题 #3
从头开始编写你自己的名为 `IntArray` 的整数数组类（不要使用 `std::array` 或 `std::vector`）。用户在创建数组时应传入数组的大小，并且数组应动态分配。使用断言语句来防止坏数据。创建使以下程序正常运行所需的任何构造函数或重载运算符
#include <iostream>

IntArray fillArray()
{
	IntArray a(5);

	a[0] = 5;
	a[1] = 8;
	a[2] = 2;
	a[3] = 3;
	a[4] = 6;

	return a;
}

int main()
{
	IntArray a{ fillArray() };

	std::cout << a << '\n';

	auto& ref{ a }; // we're using this reference to avoid compiler self-assignment errors
	a = ref;

	IntArray b(1);
	b = a;

	a[4] = 7;

	std::cout << b << '\n';

	return 0;
}
此程序应打印
5 8 2 3 6
5 8 2 3 6
显示答案
#include <iostream>
#include <cassert> // for assert

class IntArray
{
private:
	int m_length{ 0 };
	int* m_array{ nullptr };

public:
	explicit IntArray(int length)
		: m_length{ length }
	{
		assert(length > 0 && "IntArray length should be a positive integer");

		m_array = new int[static_cast<std::size_t>(m_length)] {};
	}

	// Copy constructor that does a deep copy
	IntArray(const IntArray& array)
		: m_length{ array.m_length }
	{
		// Allocate a new array
		m_array = new int[static_cast<std::size_t>(m_length)] {};

		// Copy elements from original array to new array
		for (int count{ 0 }; count < array.m_length; ++count)
			m_array[count] = array.m_array[count];
	}

	~IntArray()
	{
		delete[] m_array;
	}

	// If you're getting crazy values here you probably forgot to do a deep copy in your copy constructor
	friend std::ostream& operator<<(std::ostream& out, const IntArray& array)
	{
		for (int count{ 0 }; count < array.m_length; ++count)
		{
			out << array.m_array[count] << ' ';
		}
		return out;
	}

	int& operator[] (const int index)
	{
		assert(index >= 0);
		assert(index < m_length);
		return m_array[index];
	}

	// Assignment operator that does a deep copy
	IntArray& operator= (const IntArray& array)
	{
		// self-assignment guard
		if (this == &array)
			return *this;

		// If this array already exists, delete it so we don't leak memory
		delete[] m_array;

		m_length = array.m_length;

		// Allocate a new array
		m_array = new int[static_cast<std::size_t>(m_length)] {};

		// Copy elements from original array to new array
		for (int count{ 0 }; count < array.m_length; ++count)
			m_array[count] = array.m_array[count];

		return *this;
	}

};

IntArray fillArray()
{
	IntArray a(5);
	a[0] = 5;
	a[1] = 8;
	a[2] = 2;
	a[3] = 3;
	a[4] = 6;

	return a;
}

int main()
{
	IntArray a{ fillArray() };

	// If you're getting crazy values here you probably forgot to do a deep copy in your copy constructor
	std::cout << a << '\n';

	auto& ref{ a }; // we're using this reference to avoid compiler self-assignment errors
	a = ref;

	IntArray b(1);
	b = a;

	a[4] = 7; // change value in a, b should not change

	// If you're getting crazy values here you probably forgot to do self-assignment check
	// If b ends in 7, you probably forgot to do a deep copy in your copy assignment
	std::cout << b << '\n';

	return 0;
}
问题 #4
附加题：这有点棘手。
浮点数是带有小数的数字，其中小数部分后的位数是可变的。定点数是带有小数部分的数字，其中小数部分的位数是固定的。
在此测验中，我们将编写一个类来实现带有两位小数的定点数（例如 12.34、3.00 或 1278.99）。假设该类的范围应为 -32768.99 到 32767.99，小数部分应包含任意两位数字，我们不希望出现精度误差，并且我们希望节省空间。
> 步骤 #1
你认为我们应该使用哪种类型的成员变量来实现带有 2 位小数的定点数？（在继续下一个问题之前，请务必阅读答案）
显示答案
实现定点数有许多不同的方法。因为定点数本质上是浮点数的一个子案例（其中小数点后的位数是固定的而不是可变的），所以使用浮点数似乎是一个显而易见的选择。但浮点数存在精度问题。对于固定位数的小数，我们可以合理地枚举所有可能的小数值（在我们的例子中，从 .00 到 .99），因此使用具有精度问题的数据类型不是最好的选择。
更好的解决方案是使用 16 位有符号整数来保存数字的非小数部分，以及 8 位有符号整数来保存小数部分。
> 步骤 #2
编写一个名为 `FixedPoint2` 的类，它实现上一问题中推荐的解决方案。如果数字的非小数部分和/或小数部分是负数，则该数字应被视为负数。提供以下程序运行所需的重载运算符和构造函数。目前，不要担心小数部分超出范围（>99 或 <-99）。
#include <cassert>
#include <iostream>

int main()
{
	FixedPoint2 a{ 34, 56 };
	std::cout << a << '\n';
	std::cout << static_cast<double>(a) << '\n';
	assert(static_cast<double>(a) == 34.56);

	FixedPoint2 b{ -2, 8 };
	assert(static_cast<double>(b) == -2.08);

	FixedPoint2 c{ 2, -8 };
	assert(static_cast<double>(c) == -2.08);

	FixedPoint2 d{ -2, -8 };
	assert(static_cast<double>(d) == -2.08);

	FixedPoint2 e{ 0, -5 };
	assert(static_cast<double>(e) == -0.05);

	FixedPoint2 f{ 0, 10 };
	assert(static_cast<double>(f) == 0.1);
    
	return 0;
}
此程序应产生结果
34.56
34.56
提示：要输出你的数字，将其 `static_cast` 为 `double`。
显示答案
#include <cassert>
#include <cstdint> // for fixed width integers
#include <iostream>

class FixedPoint2
{
private:
	std::int16_t m_base{}; // here's our non-fractional part
	std::int8_t m_decimal{}; // here's our factional part

public:
	FixedPoint2(std::int16_t base = 0, std::int8_t decimal = 0)
		: m_base{ base }, m_decimal{ decimal }
	{
		// If either (or both) of the non-fractional and fractional part of the number are negative, the number should be treated as negative
		if (m_base < 0 || m_decimal < 0)
		{
			// Make sure base is negative
			if (m_base > 0)
				m_base = -m_base;
			// Make sure decimal is negative
			if (m_decimal > 0)
				m_decimal = -m_decimal;
		}
	}

	explicit operator double() const
	{
		return m_base + (static_cast<double>(m_decimal) / 100);
	}
};

// This doesn't require access to the internals of the class, so it can be defined outside the class
std::ostream& operator<<(std::ostream& out, const FixedPoint2& fp)
{
	out << static_cast<double>(fp);
	return out;
}

int main()
{
	FixedPoint2 a{ 34, 56 };
	std::cout << a << '\n';
	std::cout << static_cast<double>(a) << '\n';
	assert(static_cast<double>(a) == 34.56);

	FixedPoint2 b{ -2, 8 };
	assert(static_cast<double>(b) == -2.08);

	FixedPoint2 c{ 2, -8 };
	assert(static_cast<double>(c) == -2.08);

	FixedPoint2 d{ -2, -8 };
	assert(static_cast<double>(d) == -2.08);

	FixedPoint2 e{ 0, -5 };
	assert(static_cast<double>(e) == -0.05);

	FixedPoint2 f{ 0, 10 };
	assert(static_cast<double>(f) == 0.1);
    
	return 0;
}
> 步骤 #3
现在让我们处理小数部分超出范围的情况。我们这里有两种合理的策略：
限制小数部分（如果 >99，则设置为 99）。
将溢出视为相关（如果 >99，则减去 100 并向基数加 1）。
在此练习中，我们将小数溢出视为相关，因为这在下一步中会很有用。
以下内容应运行
#include <cassert>
#include <iostream>

// You will need to make testDecimal a friend of FixedPoint2
// so the function can access the private members of FixedPoint2
bool testDecimal(const FixedPoint2 &fp)
{
    if (fp.m_base >= 0)
        return fp.m_decimal >= 0 && fp.m_decimal < 100;
    else
        return fp.m_decimal <= 0 && fp.m_decimal > -100;
}

int main()
{
	FixedPoint2 a{ 1, 104 };
	std::cout << a << '\n';
	std::cout << static_cast<double>(a) << '\n';
	assert(static_cast<double>(a) == 2.04);
	assert(testDecimal(a));

	FixedPoint2 b{ 1, -104 };
	assert(static_cast<double>(b) == -2.04);
	assert(testDecimal(b));

	FixedPoint2 c{ -1, 104 };
	assert(static_cast<double>(c) == -2.04);
	assert(testDecimal(c));

	FixedPoint2 d{ -1, -104 };
	assert(static_cast<double>(d) == -2.04);
	assert(testDecimal(d));

	return 0;
}
并产生输出
2.04
2.04
显示答案
#include <cassert>
#include <cstdint> // for fixed width integers
#include <iostream>

class FixedPoint2
{
private:
	std::int16_t m_base{}; // here's our non-fractional part
	std::int8_t m_decimal{}; // here's our factional part

public:
	FixedPoint2(std::int16_t base = 0, std::int8_t decimal = 0)
		: m_base{ base }, m_decimal{ decimal }
	{
		// If either (or both) of the non-fractional and fractional part of the number are negative, the number should be treated as negative
		if (m_base < 0 || m_decimal < 0)
		{
			// Make sure base is negative
			if (m_base > 0)
				m_base = -m_base;
			// Make sure decimal is negative
			if (m_decimal > 0)
				m_decimal = -m_decimal;
		}

		// If decimal is out of bounds (in either direction),
		// adjust the decimal so it's in bounds,
		// and adjust base to account for the number of units removed from the decimal
		// h/t to reader David Pinheiro for simplifying this
		m_base += m_decimal / 100;    // integer division
		m_decimal = m_decimal % 100;  // integer remainder
	}

	explicit operator double() const
	{
		return m_base + (static_cast<double>(m_decimal) / 100);
	}

	friend bool testDecimal(const FixedPoint2 &fp);
};

// This doesn't require access to the internals of the class, so it can be defined outside the class
std::ostream& operator<<(std::ostream& out, const FixedPoint2& fp)
{
	out << static_cast<double>(fp);
	return out;
}

// You will need to make testDecimal a friend of FixedPoint2
// so the function can access the private members of FixedPoint2
bool testDecimal(const FixedPoint2 &fp)
{
	if (fp.m_base >= 0)
		return fp.m_decimal >= 0 && fp.m_decimal < 100;
	else
		return fp.m_decimal <= 0 && fp.m_decimal > -100;
}

int main()
{
	FixedPoint2 a{ 1, 104 };
	std::cout << a << '\n';
	std::cout << static_cast<double>(a) << '\n';
	assert(static_cast<double>(a) == 2.04);
	assert(testDecimal(a));

	FixedPoint2 b{ 1, -104 };
	assert(static_cast<double>(b) == -2.04);
	assert(testDecimal(b));

	FixedPoint2 c{ -1, 104 };
	assert(static_cast<double>(c) == -2.04);
	assert(testDecimal(c));

	FixedPoint2 d{ -1, -104 };
	assert(static_cast<double>(d) == -2.04);
	assert(testDecimal(d));

	return 0;
}
> 第4步
现在添加一个接受 `double` 类型的构造函数。以下程序应运行
#include <cassert>
#include <iostream>

int main()
{
	FixedPoint2 a{ 0.01 };
	assert(static_cast<double>(a) == 0.01);

	FixedPoint2 b{ -0.01 };
	assert(static_cast<double>(b) == -0.01);

	FixedPoint2 c{ 1.9 }; // make sure we handle single digit decimal
	assert(static_cast<double>(c) == 1.9);
    
	FixedPoint2 d{ 5.01 }; // stored as 5.0099999... so we'll need to round this
	assert(static_cast<double>(d) == 5.01);

	FixedPoint2 e{ -5.01 }; // stored as -5.0099999... so we'll need to round this
	assert(static_cast<double>(e) == -5.01);

	// Handle case where the argument's decimal rounds to 100 (need to increase base by 1)
	FixedPoint2 f { 106.9978 }; // should be stored with base 107 and decimal 0
	assert(static_cast<double>(f) == 107.0);

	// Handle case where the argument's decimal rounds to -100 (need to decrease base by 1)
	FixedPoint2 g { -106.9978 }; // should be stored with base -107 and decimal 0
	assert(static_cast<double>(g) == -107.0);

	return 0;
}
建议：这会有点棘手。分三步完成。首先，解决 `double` 参数可以直接表示的情况（上述变量 `a` 到 `c`）。然后，更新你的代码以处理 `double` 参数存在舍入误差的情况（变量 `d` 和 `e`）。变量 `f` 和 `g` 应由我们在上一步中添加的溢出处理来处理。
对于所有情况：
显示提示
提示：你可以通过乘以 10 将数字从小数点右侧移动到小数点左侧。乘以 100 以移动两位。
对于变量 `a` 到 `c`：
显示提示
提示：你可以通过将 `double` 静态转换为整数来获取 `double` 的非小数部分。要获取小数部分，你可以减去基数部分。
对于变量 `d` 和 `e`：
显示提示
提示：你可以使用 `std::round()` 函数（包含在 `
` 头文件中）对数字（小数点左侧）进行四舍五入，并使用 `std::trunc()` 函数取数字的向下取整（朝向零）。
显示答案
#include <cassert>
#include <cmath>
#include <cstdint> // for fixed width integers
#include <iostream>

class FixedPoint2
{
private:
	std::int16_t m_base{}; // here's our non-fractional part
	std::int8_t m_decimal{}; // here's our factional part

public:
	FixedPoint2(std::int16_t base = 0, std::int8_t decimal = 0)
		: m_base{ base }, m_decimal{ decimal }
	{
		// If either (or both) of the non-fractional and fractional part of the number are negative, the number should be treated as negative
		if (m_base < 0 || m_decimal < 0)
		{
			// Make sure base is negative
			if (m_base > 0)
				m_base = -m_base;
			// Make sure decimal is negative
			if (m_decimal > 0)
				m_decimal = -m_decimal;
		}

		// If decimal is out of bounds (in either direction),
		// adjust the decimal so it's in bounds,
		// and adjust base to account for the number of units removed from the decimal
		// h/t to reader David Pinheiro for simplifying this
		m_base += m_decimal / 100;    // integer division
		m_decimal = m_decimal % 100;  // integer remainder
	}

	// We'll delegate to the prior constructor so we don't have to duplicate the negative number and overflow handling logic
	FixedPoint2(double d) :
		FixedPoint2(
			static_cast<std::int16_t>(std::trunc(d)),
			static_cast<std::int8_t>(std::round(d * 100) - std::trunc(d) * 100)
		)
	{
	}

	explicit operator double() const
	{
		return m_base + (static_cast<double>(m_decimal) / 100);
	}
};

// This doesn't require access to the internals of the class, so it can be defined outside the class
std::ostream& operator<<(std::ostream& out, const FixedPoint2& fp)
{
	out << static_cast<double>(fp);
	return out;
}

int main()
{
	FixedPoint2 a{ 0.01 };
	std::cout << a << '\n';
	assert(static_cast<double>(a) == 0.01);

	FixedPoint2 b{ -0.01 };
	assert(static_cast<double>(b) == -0.01);

	FixedPoint2 c{ 1.9 }; // make sure we handle single digit decimal
	assert(static_cast<double>(c) == 1.9);
    
	FixedPoint2 d{ 5.01 }; // stored as 5.0099999... so we'll need to round this
	assert(static_cast<double>(d) == 5.01);

	FixedPoint2 e{ -5.01 }; // stored as -5.0099999... so we'll need to round this
	assert(static_cast<double>(e) == -5.01);

	// Handle case where the argument's decimal rounds to 100 (need to increase base by 1)
	FixedPoint2 f { 106.9978 }; // should be stored with base 107 and decimal 0
	assert(static_cast<double>(f) == 107.0);

	// Handle case where the argument's decimal rounds to -100 (need to decrease base by 1)
	FixedPoint2 g { -106.9978 }; // should be stored with base -107 and decimal 0
	assert(static_cast<double>(g) == -107.0);

	return 0;
}
> 步骤 #5
重载 `operator==`、`operator>>`、`operator-`（一元）和 `operator+`（二元）。
以下程序应该运行
#include <cassert>
#include <iostream>

int main()
{
	assert(FixedPoint2{ 0.75 } == FixedPoint2{ 0.75 });    // Test equality true
	assert(!(FixedPoint2{ 0.75 } == FixedPoint2{ 0.76 })); // Test equality false
    
	// Test additional cases -- h/t to reader Sharjeel Safdar for these test cases
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ 1.23 } == FixedPoint2{ 1.98 });    // both positive, no decimal overflow
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ 1.50 } == FixedPoint2{ 2.25 });    // both positive, with decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ -1.23 } == FixedPoint2{ -1.98 }); // both negative, no decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ -1.50 } == FixedPoint2{ -2.25 }); // both negative, with decimal overflow
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ -1.23 } == FixedPoint2{ -0.48 });  // second negative, no decimal overflow
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ -1.50 } == FixedPoint2{ -0.75 });  // second negative, possible decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ 1.23 } == FixedPoint2{ 0.48 });   // first negative, no decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ 1.50 } == FixedPoint2{ 0.75 });   // first negative, possible decimal overflow
    
	FixedPoint2 a{ -0.48 };
	assert(static_cast<double>(a) == -0.48);
	assert(static_cast<double>(-a) == 0.48);

	std::cout << "Enter a number: "; // enter 5.678
	std::cin >> a;
	std::cout << "You entered: " << a << '\n';
	assert(static_cast<double>(a) == 5.68);
	
	return 0;
}
显示提示
提示：利用 `double` 转换将两个 `FixedPoint2` 相加，然后将结果转换回 `FixedPoint2`。这优雅地处理了小数溢出。
显示提示
提示：对于 `operator>>`，使用你的 `double` 构造函数创建一个 `FixedPoint2` 类型的匿名对象，并将其赋值给你的 `FixedPoint2` 函数参数。
显示答案
#include <cassert>
#include <cmath>
#include <cstdint> // for fixed width integers
#include <iostream>

class FixedPoint2
{
private:
	std::int16_t m_base{}; // here's our non-fractional part
	std::int8_t m_decimal{}; // here's our factional part

public:
	FixedPoint2(std::int16_t base = 0, std::int8_t decimal = 0)
		: m_base{ base }, m_decimal{ decimal }
	{
		// If either (or both) of the non-fractional and fractional part of the number are negative, the number should be treated as negative
		if (m_base < 0 || m_decimal < 0)
		{
			// Make sure base is negative
			if (m_base > 0)
				m_base = -m_base;
			// Make sure decimal is negative
			if (m_decimal > 0)
				m_decimal = -m_decimal;
		}

		// If decimal is out of bounds (in either direction),
		// adjust the decimal so it's in bounds,
		// and adjust base to account for the number of units removed from the decimal
		// h/t to reader David Pinheiro for simplifying this
		m_base += m_decimal / 100;    // integer division
		m_decimal = m_decimal % 100;  // integer remainder
	}

	FixedPoint2(double d) :
		FixedPoint2(
			static_cast<std::int16_t>(std::trunc(d)),
			static_cast<std::int8_t>(std::round(d * 100) - std::trunc(d) * 100)
		)
	{
	}

	explicit operator double() const
	{
		return m_base + (static_cast<double>(m_decimal) / 100);
	}

	friend bool operator==(const FixedPoint2& fp1, const FixedPoint2& fp2)
	{
		return fp1.m_base == fp2.m_base && fp1.m_decimal == fp2.m_decimal;
	}

	FixedPoint2 operator-() const
	{
		// Cast to double, make the double negative, then convert back to FixedPoint2
		// h/t to reader EmtyC for this version
		return FixedPoint2{ -static_cast<double>(*this) };
	}
};

// This doesn't require access to the internals of the class, so it can be defined outside the class
std::ostream& operator<<(std::ostream& out, const FixedPoint2& fp)
{
	out << static_cast<double>(fp);
	return out;
}

std::istream& operator>>(std::istream& in, FixedPoint2& fp)
{
	double d{};
	in >> d;
	fp = FixedPoint2{ d };

	return in;
}

FixedPoint2 operator+(const FixedPoint2& fp1, const FixedPoint2& fp2)
{
	return FixedPoint2{ static_cast<double>(fp1) + static_cast<double>(fp2) };
}

int main()
{
	assert(FixedPoint2{ 0.75 } == FixedPoint2{ 0.75 });    // Test equality true
	assert(!(FixedPoint2{ 0.75 } == FixedPoint2{ 0.76 })); // Test equality false
    
	// Test additional cases -- h/t to reader Sharjeel Safdar for these test cases
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ 1.23 } == FixedPoint2{ 1.98 });    // both positive, no decimal overflow
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ 1.50 } == FixedPoint2{ 2.25 });    // both positive, with decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ -1.23 } == FixedPoint2{ -1.98 }); // both negative, no decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ -1.50 } == FixedPoint2{ -2.25 }); // both negative, with decimal overflow
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ -1.23 } == FixedPoint2{ -0.48 });  // second negative, no decimal overflow
	assert(FixedPoint2{ 0.75 } + FixedPoint2{ -1.50 } == FixedPoint2{ -0.75 });  // second negative, possible decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ 1.23 } == FixedPoint2{ 0.48 });   // first negative, no decimal overflow
	assert(FixedPoint2{ -0.75 } + FixedPoint2{ 1.50 } == FixedPoint2{ 0.75 });   // first negative, possible decimal overflow
    
	FixedPoint2 a{ -0.48 };
	assert(static_cast<double>(a) == -0.48);
	assert(static_cast<double>(-a) == 0.48);

	std::cout << "Enter a number: "; // enter 5.678
	std::cin >> a;
	std::cout << "You entered: " << a << '\n';
	assert(static_cast<double>(a) == 5.68);
	
	return 0;
}
下一课
21.y
第 21 章项目
返回目录
上一课
21.14
重载运算符和函数模板