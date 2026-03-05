# 14.x — 第 14 章总结与测验

14.x — 第 14 章总结与测验
Alex
2016 年 3 月 25 日，下午 6:01 PDT
2024 年 8 月 17 日
在本章中，我们探讨了 C++ 的核心——类！这是教程系列中最重要的章节，因为它为接下来的大部分内容奠定了基础。
章节回顾
在
过程式编程
中，重点是创建实现程序逻辑的“过程”（在 C++ 中称为函数）。我们将数据对象传递给这些函数，这些函数对数据执行操作，然后可能将结果返回给调用者使用。
通过
面向对象编程
（通常缩写为 OOP），重点是创建包含属性和一组定义明确行为的程序定义数据类型。
类不变式
是一个条件，必须在对象的整个生命周期内都为真，才能使对象保持有效状态。如果一个对象的类不变式被违反，则称该对象处于
无效状态
，进一步使用该对象可能会导致意外或未定义的行为。
类
是一种程序定义的复合类型，它将数据和操作该数据的函数捆绑在一起。
属于类类型的函数称为
成员函数
。调用成员函数的对象通常称为
隐式对象
。非成员函数称为
非成员函数
，以区别于成员函数。如果您的类类型没有数据成员，请优先使用命名空间。
const 成员函数
是保证不会修改对象或调用任何非 const 成员函数（因为它们可能会修改对象）的成员函数。不（并且永远不会）修改对象状态的成员函数应设为 const，以便可以在非 const 和 const 对象上调用它。
类类型的每个成员都有一个称为
访问级别
的属性，它决定了谁可以访问该成员。访问级别系统有时非正式地称为
访问控制
。访问级别是按类定义的，而不是按对象定义的。
公共成员
是类类型的成员，对其访问没有任何限制。公共成员可以由任何人访问（只要它们在作用域内）。这包括同一类的其他成员。公共成员也可以由
公共
访问，我们称之为存在于给定类类型成员之外的代码。公共的例子包括非成员函数，以及其他类类型的成员。
默认情况下，结构体的所有成员都是公共成员。
私有成员
是类类型的成员，只能由同一类的其他成员访问。
默认情况下，类的成员是私有的。具有私有成员的类不再是聚合，因此不能再使用聚合初始化。考虑将您的私有成员命名为以“m_”前缀开头，以帮助将它们与局部变量、函数参数和成员函数的名称区分开来。
我们可以通过使用
访问说明符
显式设置成员的访问级别。结构体通常应避免使用访问说明符，以便所有成员都默认为公共。
访问函数
是一个简单的公共成员函数，其作用是检索或更改私有成员变量的值。访问函数有两种类型：获取器和设置器。
获取器
（有时也称为
访问器
）是返回私有成员变量值的公共成员函数。
设置器
（有时也称为
修改器
）是设置私有成员变量值的公共成员函数。
类类型的
接口
定义了类类型的用户将如何与该类类型的对象进行交互。由于只有公共成员可以从类类型外部访问，因此类类型的公共成员构成了其接口。因此，由公共成员组成的接口有时称为
公共接口
。
类类型的
实现
包括实际使类按预期行为的代码。这包括存储数据的成员变量，以及包含程序逻辑和操作成员变量的成员函数体。
在编程中，
数据隐藏
（也称为
信息隐藏
或
数据抽象
）是一种用于通过向用户隐藏程序定义数据类型的实现来强制分离接口和实现的技术。
术语
封装
有时也用于指代数据隐藏。然而，该术语也用于指代数据和函数捆绑在一起（不考虑访问控制），因此其使用可能存在歧义。
定义类时，优先声明公共成员，最后声明私有成员。这突出了公共接口，并弱化了实现细节。
构造函数
是用于初始化类类型对象的特殊成员函数。必须找到匹配的构造函数才能创建非聚合类类型对象。
成员初始化列表
允许您在构造函数中初始化成员变量。成员初始化列表中的成员变量应按照它们在类中定义的顺序进行列出。优先使用成员初始化列表来初始化成员，而不是在构造函数体中赋值。
不带参数（或所有参数都有默认值）的构造函数称为
默认构造函数
。如果用户未提供初始化值，则使用默认构造函数。如果非聚合类类型对象没有用户声明的构造函数，编译器将生成一个默认构造函数（以便该类可以进行值初始化或默认初始化）。此构造函数称为
隐式默认构造函数
。
构造函数可以将其初始化委托给同一类类型中的另一个构造函数。此过程有时称为
构造函数链
，此类构造函数称为
委托构造函数
。构造函数可以委托或初始化，但不能两者兼而有之。
临时对象
（有时称为
匿名对象
或
未命名对象
）是没有名称且仅存在于单个表达式持续时间内的对象。
拷贝构造函数
是用于使用同一类型的现有对象初始化对象的构造函数。如果您不为类提供拷贝构造函数，C++ 将为您创建一个执行成员初始化操作的公共
隐式拷贝构造函数
。
“as-if”规则
指出，编译器可以随意修改程序以生成更优化的代码，只要这些修改不影响程序的“可观察行为”。“as-if”规则的一个例外是拷贝省略。
拷贝省略
是一种编译器优化技术，允许编译器删除不必要的对象拷贝。当编译器优化掉对拷贝构造函数的调用时，我们称构造函数已被
省略
。
我们编写的用于将值转换为或从程序定义类型转换的函数称为
用户定义转换
。可用于执行隐式转换的构造函数称为
转换构造函数
。默认情况下，所有构造函数都是转换构造函数。
我们可以使用
explicit
关键字告诉编译器构造函数不应被用作转换构造函数。此类构造函数不能用于进行拷贝初始化或拷贝列表初始化，也不能用于进行隐式转换。
默认情况下，将任何接受单个参数的构造函数设为 explicit。如果类型之间的隐式转换在语义上等价且性能良好（例如从
std::string
到
std::string_view
的转换），您可以考虑将构造函数设为非 explicit。不要将拷贝或移动构造函数设为 explicit，因为它们不执行转换。
成员函数（包括构造函数）可以是 constexpr。从 C++14 开始，constexpr 成员函数不隐式为 const。
小测验时间
作者注
曾经是本课一部分的二十一点测验已移至课程
17.x -- 第 17 章总结与测验
。
问题 #1
a) 编写一个名为
Point2d
的类。
Point2d
应包含两个
double
类型的成员变量：
m_x
和
m_y
，两者都默认为
0.0
。
提供一个构造函数和一个
print()
函数。
以下程序应该运行
#include <iostream>

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    // Point2d third{ 4.0 }; // should error if uncommented 

    first.print();
    second.print();

    return 0;
}
这应该打印
Point2d(0, 0)
Point2d(3, 4)
显示答案
#include <iostream>

class Point2d
{
private:
	double m_x{ 0.0 };
	double m_y{ 0.0 };

public:
	Point2d() = default;

	Point2d(double x, double y)
		: m_x{ x }, m_y{ y }
	{
	}

	void print() const
	{
		std::cout << "Point2d(" << m_x << ", " << m_y << ")\n";
	}
};

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    // Point2d third{ 4.0 }; // should error if uncommented 

    first.print();
    second.print();

    return 0;
}
b) 现在添加一个名为
distanceTo()
的成员函数，它接受另一个
Point2d
作为参数，并计算它们之间的距离。给定两个点 (x1, y1) 和 (x2, y2)，它们之间的距离可以使用公式
std::sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))
计算。
std::sqrt
函数位于头文件
cmath
中。
以下程序应该运行
#include <cmath>
#include <iostream>

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    first.print();
    second.print();

    std::cout << "Distance between two points: " << first.distanceTo(second) << '\n';

    return 0;
}
这应该打印
Point2d(0, 0)
Point2d(3, 4)
Distance between two points: 5
显示答案
#include <cmath>
#include <iostream>

class Point2d
{
private:
	double m_x{ 0.0 };
	double m_y{ 0.0 };

public:
	Point2d() = default;

	Point2d(double x, double y)
		: m_x{ x }, m_y{ y }
	{
	}

	void print() const
	{
		std::cout << "Point2d(" << m_x << ", " << m_y << ")\n";
	}

	double distanceTo(const Point2d& other) const
	{
		return std::sqrt(
            (m_x - other.m_x)*(m_x - other.m_x) +
            (m_y - other.m_y)*(m_y - other.m_y)
            );
	}
};

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    first.print();
    second.print();

    std::cout << "Distance between two points: " << first.distanceTo(second) << '\n';

    return 0;
}
问题 #2
在课程
13.10 -- 传递和返回结构体
中，我们使用
Fraction
结构体编写了一个小程序。参考解决方案如下：
#include <iostream>

struct Fraction
{
    int numerator{ 0 };
    int denominator{ 1 };
};

Fraction getFraction()
{
    Fraction temp{};
    std::cout << "Enter a value for numerator: ";
    std::cin >> temp.numerator;
    std::cout << "Enter a value for denominator: ";
    std::cin >> temp.denominator;
    std::cout << '\n';

    return temp;
}

Fraction multiply(const Fraction& f1, const Fraction& f2)
{
    return { f1.numerator * f2.numerator, f1.denominator * f2.denominator };
}

void printFraction(const Fraction& f)
{
    std::cout << f.numerator << '/' << f.denominator << '\n';
}

int main()
{
    Fraction f1{ getFraction() };
    Fraction f2{ getFraction() };

    std::cout << "Your fractions multiplied together: ";

    printFraction(multiply(f1, f2));

    return 0;
}
将
Fraction
从结构体转换为类。将所有函数转换为（非静态）成员函数。
作者注
注意：此测验不符合何时应使用非成员函数或成员函数的最佳实践。目标是测试您是否理解如何将非成员函数转换为成员函数。
显示答案
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    explicit Fraction(int numerator=0, int denominator=1)
        : m_numerator { numerator }, m_denominator { denominator}
    {
    }

    void getFraction()
    {
        std::cout << "Enter a value for numerator: ";
        std::cin >> m_numerator; // this is a member function, so we can access members directly
        std::cout << "Enter a value for denominator: ";
        std::cin >> m_denominator;
        std::cout << '\n';
    }

    Fraction multiply(const Fraction& f) const
    {
        return Fraction{ m_numerator * f.m_numerator, m_denominator * f.m_denominator };
    }

    void printFraction() const
    {
        std::cout << m_numerator << '/' << m_denominator << '\n';
    }
};

int main()
{
    Fraction f1{};
    f1.getFraction();
    
    Fraction f2{};
    f2.getFraction();

    std::cout << "Your fractions multiplied together: ";

    f1.multiply(f2).printFraction();

    return 0;
}
问题 #3
在之前的测验解决方案中，为什么
Fraction
构造函数被设为
explicit
？
显示答案
将构造函数设为 explicit 可以防止它通过单个值的隐式转换来创建
Fraction
。这有助于防止像
f1.multiply(true)
这样的无意义操作。
f1.multiply(true)
要求
true
隐式转换为
Fraction
。通常编译器会为此使用
Fraction(int numerator=0, int denominator=1)
，但如果我们将该构造函数设为 explicit，它就不符合用于隐式转换的条件。由于编译器将无法找到将
true
转换为
Fraction
的方法，它将发出编译错误。
问题 #4
在之前的测验问题中，为什么将
getFraction()
和
print()
保留为非成员函数可能更好？
显示答案
对于
getFraction()
的非成员版本，我们可以在一个步骤中定义和初始化一个 Fraction。成员版本需要两个步骤，因为我们必须首先创建一个对象，然后在其上调用成员函数。它还会为用户打印应用程序特定的文本提示。
通过将
print()
移为非成员（并使用访问函数访问成员），我们从类的接口中删除了该函数，使类的核心功能不那么混乱。这也意味着如果类的实现发生更改，我们不需要考虑
print()
是否需要更新，只要接口不变（因为我们知道它不能直接访问任何数据成员）。
下一课
15.1
隐藏的“this”指针和成员函数链
返回目录
上一课
14.17
Constexpr 聚合和类