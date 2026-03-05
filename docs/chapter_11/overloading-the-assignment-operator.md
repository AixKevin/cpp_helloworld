# 21.12 — 重载赋值运算符

21.12 — 重载赋值运算符
Alex
2016 年 6 月 5 日，上午 10:51 PDT
2024 年 7 月 22 日
拷贝赋值运算符
(operator=) 用于将值从一个对象拷贝到另一个
已存在的对象
。
相关内容
自 C++11 起，C++ 还支持“移动赋值”。我们在课程
22.3 -- 移动构造函数和移动赋值
中讨论移动赋值。
拷贝赋值与拷贝构造函数
拷贝构造函数和拷贝赋值运算符的目的几乎相同——两者都将一个对象拷贝到另一个对象。然而，拷贝构造函数初始化新对象，而赋值运算符替换现有对象的内容。
拷贝构造函数和拷贝赋值运算符之间的区别对于新程序员来说常常会造成很多困惑，但实际上并没有那么难。总结如下：
如果在拷贝发生之前必须创建新对象，则使用拷贝构造函数（注意：这包括按值传递或返回对象）。
如果在拷贝发生之前不需要创建新对象，则使用赋值运算符。
重载赋值运算符
重载拷贝赋值运算符 (operator=) 相当直接，只有一个我们将要讨论的特殊注意事项。拷贝赋值运算符必须作为成员函数重载。
#include <cassert>
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
	// Default constructor
	Fraction(int numerator = 0, int denominator = 1 )
		: m_numerator { numerator }, m_denominator { denominator }
	{
		assert(denominator != 0);
	}

	// Copy constructor
	Fraction(const Fraction& copy)
		: m_numerator { copy.m_numerator }, m_denominator { copy.m_denominator }
	{
		// no need to check for a denominator of 0 here since copy must already be a valid Fraction
		std::cout << "Copy constructor called\n"; // just to prove it works
	}

	// Overloaded assignment
	Fraction& operator= (const Fraction& fraction);

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
        
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

// A simplistic implementation of operator= (see better implementation below)
Fraction& Fraction::operator= (const Fraction& fraction)
{
    // do the copy
    m_numerator = fraction.m_numerator;
    m_denominator = fraction.m_denominator;

    // return the existing object so we can chain this operator
    return *this;
}

int main()
{
    Fraction fiveThirds { 5, 3 };
    Fraction f;
    f = fiveThirds; // calls overloaded assignment
    std::cout << f;

    return 0;
}
这会打印
5/3
现在这一切应该都相当直接了。我们重载的 operator= 返回 *this，这样我们就可以将多个赋值操作链式地连接起来。
int main()
{
    Fraction f1 { 5, 3 };
    Fraction f2 { 7, 2 };
    Fraction f3 { 9, 5 };

    f1 = f2 = f3; // chained assignment

    return 0;
}
自赋值引起的问题
事情在这里开始变得更有趣了。C++ 允许自赋值
int main()
{
    Fraction f1 { 5, 3 };
    f1 = f1; // self assignment

    return 0;
}
这将调用 f1.operator=(f1)，在上述简单实现中，所有成员都将赋值给自己。在这个特定的例子中，自赋值导致每个成员被赋值给自己，除了浪费时间，没有整体影响。在大多数情况下，自赋值根本不需要做任何事情！
然而，在赋值运算符需要动态分配内存的情况下，自赋值实际上可能很危险。
#include <algorithm> // for std::max and std::copy_n
#include <iostream>

class MyString
{
private:
	char* m_data {};
	int m_length {};

public:
	MyString(const char* data = nullptr, int length = 0 )
		: m_length { std::max(length, 0) }
	{
		if (length)
		{
			m_data = new char[static_cast<std::size_t>(length)];
			std::copy_n(data, length, m_data); // copy length elements of data into m_data
		}
	}
	~MyString()
	{
		delete[] m_data;
	}

	MyString(const MyString&) = default; // some compilers (gcc) warn if you have pointer members but no declared copy constructor

	// Overloaded assignment
	MyString& operator= (const MyString& str);

	friend std::ostream& operator<<(std::ostream& out, const MyString& s);
};

std::ostream& operator<<(std::ostream& out, const MyString& s)
{
	out << s.m_data;
	return out;
}

// A simplistic implementation of operator= (do not use)
MyString& MyString::operator= (const MyString& str)
{
	// if data exists in the current string, delete it
	if (m_data) delete[] m_data;

	m_length = str.m_length;
	m_data = nullptr;

	// allocate a new array of the appropriate length
	if (m_length)
		m_data = new char[static_cast<std::size_t>(str.m_length)];

	std::copy_n(str.m_data, m_length, m_data); // copies m_length elements of str.m_data into m_data

	// return the existing object so we can chain this operator
	return *this;
}

int main()
{
	MyString alex("Alex", 5); // Meet Alex
	MyString employee;
	employee = alex; // Alex is our newest employee
	std::cout << employee; // Say your name, employee

	return 0;
}
首先，按原样运行程序。您会看到程序按预期打印“Alex”。
现在运行以下程序
int main()
{
    MyString alex { "Alex", 5 }; // Meet Alex
    alex = alex; // Alex is himself
    std::cout << alex; // Say your name, Alex

    return 0;
}
您可能会得到乱码输出。发生了什么？
考虑在重载的 operator= 中，当隐式对象和传入参数 (str) 都是变量 alex 时会发生什么。在这种情况下，m_data 与 str.m_data 相同。首先发生的是函数检查隐式对象是否已经有一个字符串。如果是，它需要删除它，这样我们就不会导致内存泄漏。在这种情况下，m_data 已分配，因此函数会删除 m_data。但由于 str 与 *this 相同，我们想要拷贝的字符串已被删除，m_data（和 str.m_data）悬空。
稍后，我们为 m_data（和 str.m_data）分配新内存。因此，当我们随后将数据从 str.m_data 拷贝到 m_data 时，我们拷贝的是垃圾，因为 str.m_data 从未初始化。
检测和处理自赋值
幸运的是，我们可以检测到何时发生自赋值。以下是我们为 MyString 类重载的 operator= 的更新实现
MyString& MyString::operator= (const MyString& str)
{
	// self-assignment check
	if (this == &str)
		return *this;

	// if data exists in the current string, delete it
	if (m_data) delete[] m_data;

	m_length = str.m_length;
	m_data = nullptr;

	// allocate a new array of the appropriate length
	if (m_length)
		m_data = new char[static_cast<std::size_t>(str.m_length)];

	std::copy_n(str.m_data, m_length, m_data); // copies m_length elements of str.m_data into m_data

	// return the existing object so we can chain this operator
	return *this;
}
通过检查我们的隐式对象的地址是否与作为参数传入的对象的地址相同，我们可以让我们的赋值运算符立即返回，而不做任何其他工作。
由于这只是一个指针比较，它应该很快，并且不需要重载 operator==。
何时不处理自赋值
通常，拷贝构造函数会跳过自赋值检查。因为被拷贝构造的对象是新创建的，新创建的对象等于被拷贝对象的唯一情况是当您尝试用自身初始化一个新定义的对象时
someClass c { c };
在这种情况下，编译器应该警告您
c
是一个未初始化的变量。
其次，在能够自然处理自赋值的类中，可以省略自赋值检查。考虑这个带有自赋值保护的 Fraction 类赋值运算符
// A better implementation of operator=
Fraction& Fraction::operator= (const Fraction& fraction)
{
    // self-assignment guard
    if (this == &fraction)
        return *this;

    // do the copy
    m_numerator = fraction.m_numerator; // can handle self-assignment
    m_denominator = fraction.m_denominator; // can handle self-assignment

    // return the existing object so we can chain this operator
    return *this;
}
如果不存在自赋值保护，此函数在自赋值期间仍将正确运行（因为函数执行的所有操作都可以正确处理自赋值）。
由于自赋值是罕见事件，一些著名的 C++ 大师建议即使在受益于自赋值保护的类中也省略它。我们不建议这样做，因为我们认为防御性编程，然后选择性优化是更好的实践。
拷贝并交换惯用法
处理自赋值问题的更好方法是使用所谓的拷贝并交换惯用法。关于此惯用法如何工作的精彩文章可以在
Stack Overflow
上找到。
隐式拷贝赋值运算符
与其他运算符不同，如果您不提供用户定义的拷贝赋值运算符，编译器将为您的类提供一个隐式公共拷贝赋值运算符。此赋值运算符执行逐成员赋值（这与默认拷贝构造函数执行的逐成员初始化本质上相同）。
就像其他构造函数和运算符一样，您可以通过将拷贝赋值运算符设置为私有或使用 delete 关键字来阻止赋值。
#include <cassert>
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
    // Default constructor
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator { numerator }, m_denominator { denominator }
    {
        assert(denominator != 0);
    }

	// Copy constructor
	Fraction(const Fraction &copy) = delete;

	// Overloaded assignment
	Fraction& operator= (const Fraction& fraction) = delete; // no copies through assignment!

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
        
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

int main()
{
    Fraction fiveThirds { 5, 3 };
    Fraction f;
    f = fiveThirds; // compile error, operator= has been deleted
    std::cout << f;

    return 0;
}
请注意，如果您的类包含 const 成员，编译器将改为将隐式
operator=
定义为 deleted。这是因为 const 成员不能被赋值，因此编译器会假定您的类不应该是可赋值的。
如果您希望一个包含 const 成员的类是可赋值的（对于所有非 const 成员），您将需要显式重载
operator=
并手动赋值每个非 const 成员。
下一课
21.13
浅拷贝与深拷贝
返回目录
上一课
21.11
重载类型转换