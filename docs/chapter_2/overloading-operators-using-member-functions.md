# 21.5 — 使用成员函数重载运算符

21.5 — 使用成员函数重载运算符
Alex
2007 年 10 月 11 日，太平洋夏令时上午 10:22
2023 年 10 月 30 日
在课程
21.2 -- 使用友元函数重载算术运算符
中，你学习了如何使用友元函数重载算术运算符。你还学习了可以将运算符重载为普通函数。许多运算符可以用不同的方式重载：作为成员函数。
使用成员函数重载运算符与使用友元函数重载运算符非常相似。当使用成员函数重载运算符时
重载运算符必须作为左操作数的成员函数添加。
左操作数成为隐式的 *this 对象
所有其他操作数成为函数参数。
提醒一下，这是我们如何使用友元函数重载 operator+ 的方法
#include <iostream>

class Cents
{
private:
    int m_cents {};

public:
    Cents(int cents)
        : m_cents { cents } { }

    // Overload Cents + int
    friend Cents operator+(const Cents& cents, int value);

    int getCents() const { return m_cents; }
};

// note: this function is not a member function!
Cents operator+(const Cents& cents, int value)
{
    return Cents(cents.m_cents + value);
}

int main()
{
	const Cents cents1 { 6 };
	const Cents cents2 { cents1 + 2 };
	std::cout << "I have " << cents2.getCents() << " cents.\n";
 
	return 0;
}
将友元重载运算符转换为成员重载运算符很简单
重载运算符被定义为成员而不是友元（Cents::operator+ 而不是 friend operator+）
左参数被移除，因为该参数现在成为隐式的 *this 对象。
在函数体内部，所有对左参数的引用都可以被移除（例如 cents.m_cents 变为 m_cents，它隐式引用 *this 对象）。
现在，使用成员函数方法重载的相同运算符
#include <iostream>

class Cents
{
private:
    int m_cents {};

public:
    Cents(int cents)
        : m_cents { cents } { }

    // Overload Cents + int
    Cents operator+(int value) const;

    int getCents() const { return m_cents; }
};

// note: this function is a member function!
// the cents parameter in the friend version is now the implicit *this parameter
Cents Cents::operator+ (int value) const
{
    return Cents { m_cents + value };
}

int main()
{
	const Cents cents1 { 6 };
	const Cents cents2 { cents1 + 2 };
	std::cout << "I have " << cents2.getCents() << " cents.\n";
 
	return 0;
}
请注意，运算符的使用方式没有改变（在两种情况下都是
cents1 + 2
），我们只是以不同的方式定义了函数。我们的双参数友元函数变成了单参数成员函数，友元版本中最左侧的参数 (cents) 成为成员函数版本中隐式的 *this 参数。
让我们仔细看看表达式
cents1 + 2
是如何求值的。
在友元函数版本中，表达式
cents1 + 2
变为函数调用 operator+(cents1, 2)。请注意，这里有两个函数参数。这很简单。
在成员函数版本中，表达式
cents1 + 2
变为函数调用
cents1.operator+(2)
。请注意，现在只有一个显式函数参数，并且 cents1 已成为对象前缀。然而，在课程
15.1 -- 隐藏的“this”指针和成员函数链式调用
中，我们提到编译器隐式地将对象前缀转换为一个名为 *this 的隐藏最左侧参数。因此，实际上，
cents1.operator+(2)
变为
operator+(&cents1, 2)
，这与友元版本几乎相同。
两种情况都产生相同的结果，只是方式略有不同。
那么如果我们可以将运算符重载为友元或成员，我们应该使用哪一个呢？为了回答这个问题，你还需要了解更多信息。
并非所有内容都可以重载为友元函数
赋值 (=)、下标 ([])、函数调用 (()) 和成员选择 (->) 运算符必须作为成员函数重载，因为语言要求它们如此。
并非所有内容都可以重载为成员函数
在课程
21.4 -- 重载 I/O 运算符
中，我们使用友元函数方法为我们的 Point 类重载了 operator<<。下面是我们如何做到的提醒
#include <iostream>
 
class Point
{
private:
    double m_x {};
    double m_y {};
    double m_z {};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0)
        : m_x { x }, m_y { y }, m_z { z }
    {
    }
 
    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};
 
std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // Since operator<< is a friend of the Point class, we can access Point's members directly.
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ")";
 
    return out;
}
 
int main()
{
    Point point1 { 2.0, 3.0, 4.0 };
 
    std::cout << point1;
 
    return 0;
}
但是，我们不能将 operator<< 重载为成员函数。为什么不能？因为重载运算符必须作为左操作数的成员添加。在这种情况下，左操作数是 std::ostream 类型的对象。std::ostream 作为标准库的一部分是固定的。我们不能修改类声明以将重载作为 std::ostream 的成员函数添加。
这使得 operator<< 必须作为普通函数（首选）或友元重载。
类似地，虽然我们可以将 operator+(Cents, int) 重载为成员函数（如上所示），但我们不能将 operator+(int, Cents) 重载为成员函数，因为 int 不是我们可以添加成员的类。
通常，如果左操作数不是类（例如 int），或者它是我们无法修改的类（例如 std::ostream），我们就无法使用成员重载。
何时使用普通函数、友元函数或成员函数重载
在大多数情况下，语言由你决定是使用重载的普通/友元函数版本还是成员函数版本。然而，两者之一通常是比另一个更好的选择。
当处理不修改左操作数的二元运算符（例如 operator+）时，通常首选普通函数或友元函数版本，因为它适用于所有参数类型（即使左操作数不是类对象，或者是不可修改的类）。普通函数或友元函数版本还具有“对称性”的额外好处，因为所有操作数都成为显式参数（而不是左操作数成为 *this，右操作数成为显式参数）。
当处理修改左操作数的二元运算符（例如 operator+=）时，通常首选成员函数版本。在这种情况下，最左侧的操作数将始终是类类型，并且将要修改的对象成为 *this 所指向的对象是很自然的。由于最右侧的操作数成为显式参数，因此不会混淆谁被修改以及谁被评估。
一元运算符通常也作为成员函数重载，因为成员版本没有参数。
以下经验法则可以帮助你确定哪种形式最适合给定情况
如果你要重载赋值 (=)、下标 ([])、函数调用 (()) 或成员选择 (->)，请将其作为成员函数进行。
如果你要重载一元运算符，请将其作为成员函数进行。
如果你要重载不修改其左操作数的二元运算符（例如 operator+），请将其作为普通函数（首选）或友元函数进行。
如果你要重载修改其左操作数的二元运算符，但你无法向左操作数的类定义中添加成员（例如 operator<<，其左操作数类型为 ostream），请将其作为普通函数（首选）或友元函数进行。
如果你要重载修改其左操作数的二元运算符（例如 operator+=），并且你可以修改左操作数的定义，请将其作为成员函数进行。
下一课
21.6
重载一元运算符 +、- 和 !
返回目录
上一课
21.4
重载 I/O 运算符