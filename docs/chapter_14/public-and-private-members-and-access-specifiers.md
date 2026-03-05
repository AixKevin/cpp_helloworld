# 14.5 — 公有和私有成员以及访问说明符

14.5 — 公有和私有成员以及访问说明符
Alex
2007 年 9 月 4 日，太平洋夏令时下午 2:17
2024 年 7 月 3 日
假设在一个凉爽的秋日，你走在街上，吃着卷饼。你想找个地方坐下，于是四处张望。你的左边是一个公园，有修剪整齐的草坪和遮荫树，几张不舒服的长凳，以及附近游乐场上尖叫的孩子。你的右边是一个陌生人的住所。透过窗户，你看到一张舒适的躺椅和噼啪作响的壁炉。
你重重地叹了口气，选择了公园。
你选择的关键决定因素是公园是公共场所，而住所是私人场所。你（以及任何其他人）被允许自由进出公共场所。但只有住所的成员（或获得明确许可进入的人）才被允许进入私人住所。
成员访问
类似的概念适用于类类型的成员。类类型的每个成员都有一个名为**访问级别**的属性，它决定了谁可以访问该成员。
C++ 有三种不同的访问级别：*public*、*private* 和 *protected*。在本课中，我们将介绍两种常用的访问级别：public 和 private。
相关内容
我们将在继承章节（
24.5 — 继承和访问说明符
）中讨论 protected 访问级别。
每当访问成员时，编译器都会检查该成员的访问级别是否允许访问该成员。如果访问不被允许，编译器将生成编译错误。这种访问级别系统有时非正式地称为**访问控制**。
结构体的成员默认是公有的
具有 *public* 访问级别的成员称为 *public 成员*。**Public 成员**是类类型的成员，对其访问方式没有任何限制。就像我们开头类比中的公园一样，public 成员可以被任何人访问（只要它们在作用域内）。
Public 成员可以被同一类的其他成员访问。值得注意的是，public 成员也可以被**公众**访问，我们称之为存在于给定类类型的成员*之外*的代码。*公众*的例子包括非成员函数，以及其他类类型的成员。
关键见解
结构体的成员默认是公有的。Public 成员可以被类类型的其他成员以及公众访问。
“公众”一词用于指代存在于给定类类型的成员之外的代码。这包括非成员函数，以及其他类类型的成员。
默认情况下，结构体的所有成员都是 public 成员。
考虑以下结构体
#include <iostream>

struct Date
{
    // struct members are public by default, can be accessed by anyone
    int year {};       // public by default
    int month {};      // public by default
    int day {};        // public by default

    void print() const // public by default
    {
        // public members can be accessed in member functions of the class type
        std::cout << year << '/' << month << '/' << day;
    }
};

// non-member function main is part of "the public"
int main()
{
    Date today { 2020, 10, 14 }; // aggregate initialize our struct

    // public members can be accessed by the public
    today.day = 16; // okay: the day member is public
    today.print();  // okay: the print() member function is public

    return 0;
}
在此示例中，成员在三个地方被访问
在成员函数
print()
中，我们访问隐式对象的
year
、
month
和
day
成员。
在
main()
中，我们直接访问
today.day
来设置其值。
在
main()
中，我们调用成员函数
today.print()
。
所有这三个访问都被允许，因为 public 成员可以从任何地方访问。
因为
main()
不是
Date
的成员，所以它被认为是*公众*的一部分。然而，因为*公众*可以访问 public 成员，所以
main()
可以直接访问
Date
的成员（包括对
today.print()
的调用）。
类的成员默认是私有的
具有 *private* 访问级别的成员称为 *private 成员*。**Private 成员**是类类型的成员，只能由同一类的其他成员访问。
考虑以下示例，它与上面几乎相同
#include <iostream>

class Date // now a class instead of a struct
{
    // class members are private by default, can only be accessed by other members
    int m_year {};     // private by default
    int m_month {};    // private by default
    int m_day {};      // private by default

    void print() const // private by default
    {
        // private members can be accessed in member functions
        std::cout << m_year << '/' << m_month << '/' << m_day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // compile error: can no longer use aggregate initialization

    // private members can not be accessed by the public
    today.m_day = 16; // compile error: the m_day member is private
    today.print();    // compile error: the print() member function is private

    return 0;
}
在此示例中，成员在相同的三个地方被访问
在成员函数
print()
中，我们访问隐式对象的
m_year
、
m_month
和
m_day
成员。
在
main()
中，我们直接访问
today.m_day
来设置其值。
在
main()
中，我们调用成员函数
today.print()
。
但是，如果您编译此程序，您会注意到生成了三个编译错误。
在
main()
中，语句
today.m_day = 16
和
today.print()
现在都生成编译错误。这是因为
main()
是公众的一部分，并且公众不允许直接访问 private 成员。
在
print()
中，允许访问成员
m_year
、
m_month
和
m_day
。这是因为
print()
是类的成员，并且类的成员被允许访问 private 成员。
那么第三个编译错误从何而来呢？也许令人惊讶的是，
today
的初始化现在导致了编译错误。在
13.8 — 结构体聚合初始化
一课中，我们注意到聚合体不能有“私有或受保护的非静态数据成员”。我们的
Date
类有私有数据成员（因为类的成员默认是私有的），所以我们的
Date
类不符合聚合体的条件。因此，我们不能再使用聚合初始化来初始化它。
我们将在即将到来的
14.9 — 构造函数简介
一课中讨论如何正确初始化类（通常是非聚合体）。
关键见解
类的成员默认是私有的。Private 成员可以被类的其他成员访问，但不能被公众访问。
具有 private 成员的类不再是聚合体，因此不能再使用聚合初始化。
命名你的 private 成员变量
在 C++ 中，通常约定将 private 数据成员以“m_”前缀命名。这样做有两个重要原因。
考虑某个类的以下成员函数
// Some member function that sets private member m_name to the value of the name parameter
void setName(std::string_view name)
{
    m_name = name;
}
首先，“m_”前缀使我们能够轻松区分成员函数中的数据成员与函数参数或局部变量。我们可以很容易地看到“m_name”是一个成员，而“name”不是。这有助于明确此函数正在更改类的状态。这很重要，因为当我们更改数据成员的值时，它会持续超出成员函数的范围（而对函数参数或局部变量的更改通常不会）。
这与我们建议为局部静态变量使用“s_”前缀，为全局变量使用“g_”前缀的原因相同。
其次，“m_”前缀有助于防止 private 成员变量与局部变量、函数参数和成员函数的名称发生命名冲突。
如果我们将 private 成员命名为
name
而不是
m_name
，那么
我们的
name
函数参数将遮蔽
name
private 数据成员。
如果我们有一个名为
name
的成员函数，我们将因为标识符
name
的重定义而得到编译错误。
最佳实践
考虑将 private 数据成员以“m_”前缀命名，以帮助将它们与局部变量、函数参数和成员函数的名称区分开来。
如果需要，类的 public 成员也可以遵循此约定。但是，结构体的 public 成员通常不使用此前缀，因为结构体通常没有多少成员函数（如果有的话）。
通过访问说明符设置访问级别
默认情况下，结构体（和联合体）的成员是 public 的，而类的成员是 private 的。
但是，我们可以通过使用**访问说明符**显式设置成员的访问级别。访问说明符设置了跟随该说明符的*所有成员*的访问级别。C++ 提供了三个访问说明符：
public:
、
private:
和
protected:
。
在以下示例中，我们同时使用
public:
访问说明符来确保
print()
成员函数可以被公众使用，以及
private:
访问说明符来使我们的数据成员私有。
class Date
{
// Any members defined here would default to private

public: // here's our public access specifier

    void print() const // public due to above public: specifier
    {
        // members can access other private members
        std::cout << m_year << '/' << m_month << '/' << m_day;
    }

private: // here's our private access specifier 

    int m_year { 2020 };  // private due to above private: specifier
    int m_month { 14 }; // private due to above private: specifier
    int m_day { 10 };   // private due to above private: specifier
};

int main()
{
    Date d{};
    d.print();  // okay, main() allowed to access public members

    return 0;
}
此示例编译成功。因为
print()
由于
public:
访问说明符而是一个 public 成员，所以
main()
（它是公众的一部分）被允许访问它。
由于我们有 private 成员，我们无法聚合初始化
d
。在这个例子中，我们使用默认成员初始化作为替代（作为临时解决方案）。
由于类默认私有访问，您可以省略开头的
private:
访问说明符
class Foo
{
// private access specifier not required here since classes default to private members
    int m_something {};  // private by default
};
然而，由于类和结构体有不同的访问级别默认值，许多开发人员更喜欢明确地指定
class Foo
{
private: // redundant, but makes it clear that what follows is private
    int m_something {};  // private by default
};
尽管这在技术上是冗余的，但使用显式的
private:
说明符可以明确地表明以下成员是私有的，而无需根据
Foo
是定义为类还是结构体来推断默认访问级别。
访问级别摘要
以下是不同访问级别的快速摘要表
访问级别
访问说明符
成员访问
派生类访问
公共访问
公共
public
是
是
是
受保护的
protected
是
是
否
私有的
private
是
否
否
一个类类型允许使用任意数量的访问说明符，顺序不限，并且可以重复使用（例如，你可以有一些 public 成员，然后一些 private 成员，然后更多 public 成员）。
大多数类都为各种成员使用 private 和 public 访问说明符。我们将在下一节中看到一个示例。
结构体和类的访问级别最佳实践
现在我们已经了解了访问级别是什么，让我们来谈谈我们应该如何使用它们。
结构体应该完全避免使用访问说明符，这意味着所有结构体成员将默认是 public 的。我们希望我们的结构体是聚合体，而聚合体只能有 public 成员。使用
public:
访问说明符将与默认值冗余，而使用
private:
或
protected:
将使结构体成为非聚合体。
类通常应该只拥有 private（或 protected）数据成员（无论是通过使用默认的 private 访问级别，还是使用
private:
（或
protected:
）访问说明符）。我们将在下一课
14.6 — 访问函数
中讨论这样做的理由。
类通常有 public 成员函数（以便这些成员函数在对象创建后可以被公众使用）。但是，如果成员函数不打算被公众使用，偶尔也会将其设置为 private（或 protected）。
最佳实践
类通常应将成员变量设为 private（或 protected），并将成员函数设为 public。
结构体通常应避免使用访问说明符（所有成员将默认为 public）。
访问级别是基于类的
C++ 访问级别的一个细微之处经常被遗漏或误解，那就是成员的访问是基于类的，而不是基于对象的。
你已经知道成员函数可以直接访问 private 成员（隐式对象）。然而，因为访问级别是基于类的，而不是基于对象的，所以成员函数也可以直接访问作用域内任何其他相同类类型的对象的 private 成员。
让我们用一个例子来说明这一点
#include <iostream>
#include <string>
#include <string_view>

class Person
{
private:
    std::string m_name{};

public:
    void kisses(const Person& p) const
    {
        std::cout << m_name << " kisses " << p.m_name << '\n';
    }

    void setName(std::string_view name)
    {
        m_name = name;
    }
};

int main()
{
    Person joe;
    joe.setName("Joe");
    
    Person kate;
    kate.setName("Kate");

    joe.kisses(kate);

    return 0;
}
这会打印
Joe kisses Kate
这里有几点需要注意。
首先，
m_name
已被设为私有，因此它只能由
Person
类的成员访问（不能由公共访问）。
其次，由于我们的类有私有成员，它不是一个聚合体，我们不能使用聚合初始化来初始化我们的 Person 对象。作为一种变通方法（直到我们找到这个问题的正确解决方案），我们创建了一个名为
setName()
的公共成员函数，允许我们为 Person 对象赋值。
第三，因为
kisses()
是一个成员函数，它可以直接访问私有成员
m_name
。然而，你可能会惊讶地发现它也可以直接访问
p.m_name
！这是因为
p
是一个
Person
对象，而
kisses()
可以访问作用域内任何
Person
对象的私有成员！
我们将在运算符重载一章中看到更多使用此功能的示例。
结构体和类的技术和实际区别
现在我们已经介绍了访问级别，我们终于可以讨论结构体和类之间的技术差异了。准备好了吗？
一个类将其成员默认为私有，而一个结构体将其成员默认为公共。
...
是的，就是这样。
作者注
严格来说，还有一个次要的区别——结构体公开继承其他类类型，而类私有继承。我们将在继承章节中讨论这意味着什么，但这一点在实践中无关紧要，因为无论如何你都不应该依赖继承的默认行为。
在实践中，我们以不同的方式使用结构体和类。
经验法则：当以下所有条件都为真时，使用结构体
你有一个简单的数据集合，限制访问并没有益处。
聚合初始化就足够了。
你没有类不变量、设置需求或清理需求。
一些可能使用结构体的例子：constexpr 全局程序数据、一个点结构体（一个简单的 int 成员集合，将其设为 private 没有益处）、用于从函数返回一组数据的结构体。
否则使用类。
我们希望我们的结构体是聚合体。因此，如果您使用任何使您的结构体成为非聚合体的功能，您应该改用类（并遵循类的所有最佳实践）。
小测验时间
问题 #1
a) 什么是 public 成员？
显示答案
Public 成员是类的一个成员，任何人都可以访问它，包括同一类的其他成员和公共。
b) 什么是 private 成员？
显示答案
Private 成员是类的一个成员，只能由类的其他成员访问。
c) 什么是访问说明符？
显示答案
访问说明符决定了谁可以访问跟随该说明符的成员。
d) 有多少个访问说明符，它们是什么？
显示答案
三个。public、private 和 protected。
问题 #2
a) 编写一个名为
Point3d
的类。该类应包含
三个名为
m_x
、
m_y
和
m_z
的
int
类型的 private 成员变量；
一个名为
setValues()
的 public 成员函数，允许你设置
m_x
、
m_y
和
m_z
的值。
一个名为
print()
的 public 成员函数，以以下格式打印点：<m_x, m_y, m_z>
确保以下程序正确执行
int main()
{
    Point3d point;
    point.setValues(1, 2, 3);

    point.print();
    std::cout << '\n';

    return 0;
}
这应该打印
<1, 2, 3>
显示答案
#include <iostream>

class Point3d
{
private:
    int m_x {};
    int m_y {};
    int m_z {};

public:
	void setValues(int x, int y, int z)
	{
		m_x = x;
		m_y = y;
		m_z = z;
	}

	void print() const
	{
		std::cout << '<' << m_x << ", " << m_y << ", " << m_z << '>';
	}
};

int main()
{
    Point3d point;
    point.setValues(1, 2, 3);

    point.print();
    std::cout << '\n';

    return 0;
}
b) 在你的 Point3d 类中添加一个名为
isEqual()
的函数。以下代码应正确运行
int main()
{
	Point3d point1{};
	point1.setValues(1, 2, 3);

	Point3d point2{};
	point2.setValues(1, 2, 3);

	std::cout << "point 1 and point 2 are" << (point1.isEqual(point2) ? "" : " not") << " equal\n";

	Point3d point3{};
	point3.setValues(3, 4, 5);

	std::cout << "point 1 and point 3 are" << (point1.isEqual(point3) ? "" : " not") << " equal\n";

	return 0;
}
这应该打印
point 1 and point 2 are equal
point 1 and point 3 are not equal
显示答案
#include <iostream>

class Point3d
{
private:
	int m_x {};
	int m_y {};
	int m_z {};

public:
	void setValues(int x, int y, int z)
	{
		m_x = x;
		m_y = y;
		m_z = z;
	}

	void print() const
	{
		std::cout << '<' << m_x << ", " << m_y << ", " << m_z << '>';
	}

	// We can use the fact that access controls work on a per-class basis here
	// to directly access the private members of Point3d parameter p
	bool isEqual(const Point3d& p) const
	{
		return (m_x == p.m_x) && (m_y == p.m_y) && (m_z == p.m_z);
	}
};

int main()
{
	Point3d point1{};
	point1.setValues(1, 2, 3);

	Point3d point2{};
	point2.setValues(1, 2, 3);

	std::cout << "point 1 and point 2 are" << (point1.isEqual(point2) ? "" : " not") << " equal\n";

	Point3d point3{};
	point3.setValues(3, 4, 5);

	std::cout << "point 1 and point 3 are" << (point1.isEqual(point3) ? "" : " not") << " equal\n";

	return 0;
}
下一课
14.6
访问函数
返回目录
上一课
14.4
Const 类对象和 const 成员函数