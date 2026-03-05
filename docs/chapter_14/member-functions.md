# 14.3 — 成员函数

14.3 — 成员函数
Alex
2007 年 8 月 30 日，上午 9:42 PDT
2025 年 2 月 10 日
在
13.7 — 结构体、成员和成员选择简介
课程中，我们介绍了结构体程序定义类型，它可以包含成员变量。以下是用于保存日期的结构体示例
struct Date
{
    int year {};
    int month {};
    int day {};
};
现在，如果我们想将日期打印到屏幕上（我们可能经常需要这样做），那么编写一个函数来完成此操作是有意义的。这是一个完整的程序
#include <iostream>

struct Date
{
    // here are our member variables
    int year {};
    int month {};
    int day {};
};

void print(const Date& date)
{
    // member variables accessed using member selection operator (.)
    std::cout << date.year << '/' << date.month << '/' << date.day;
}

int main()
{
    Date today { 2020, 10, 14 }; // aggregate initialize our struct

    today.day = 16; // member variables accessed using member selection operator (.)
    print(today);   // non-member function accessed using normal calling convention

    return 0;
}
这个程序打印
2020/10/16
属性和操作的分离
环顾四周——你所到之处都是物体：书籍、建筑、食物，甚至是你自己。现实生活中的物体有两个主要组成部分：1) 若干可观察属性（例如重量、颜色、大小、固体性、形状等），以及 2) 它们可以执行或在其上执行的若干操作（例如被打开、损坏其他东西等），这些操作基于这些属性。这些属性和操作是密不可分的。
在编程中，我们用变量表示属性，用函数表示操作。
在上面的
Date
示例中，请注意我们已经将属性（
Date
的成员变量）和使用这些属性执行的操作（函数
print()
）分别定义。我们只能根据
print()
的
const Date&
参数来推断
Date
和
print()
之间的连接。
虽然我们可以将
Date
和
print()
都放入一个命名空间（以使它们更清楚地表明它们旨在打包在一起），但这会为我们的程序添加更多名称和更多命名空间前缀，从而使我们的代码变得混乱。
如果有一种方法可以将我们的属性和操作一起定义，作为一个单一的包，那该多好啊。
成员函数
除了拥有成员变量之外，类类型（包括结构体、类和联合体）也可以拥有自己的函数！属于类类型的函数称为
成员函数
。
题外话…
在其他面向对象语言（例如 Java 和 C#）中，这些函数被称为
方法
。尽管在 C++ 中不使用“方法”一词，但先学习过这些其他语言的程序员可能仍会使用该术语。
不是成员函数的函数称为
非成员函数
（或偶尔称为
自由函数
），以区别于成员函数。上面的
print()
函数是一个非成员函数。
作者注
在本课中，我们将使用结构体来展示成员函数的示例——但我们在这里展示的一切同样适用于类。由于某些原因，当我们在即将到来的课程（
14.5 — public 和 private 成员以及访问说明符
）中讨论时，这些原因将变得显而易见，我们将在未来的课程中展示带有成员函数的类的示例。
成员函数必须在类类型定义内部声明，并且可以在类类型定义内部或外部定义。提醒一下，定义也是声明，所以如果我们在类内部定义成员函数，这就算作声明。
为了简单起见，我们暂时在类类型定义内部定义成员函数。
相关内容
我们将在
15.2 — 类和头文件
课程中展示如何在类类型定义外部定义成员函数。
成员函数示例
让我们重写本课开头的
Date
示例，将
print()
从非成员函数转换为成员函数
// Member function version
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() // defines a member function named print
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // aggregate initialize our struct

    today.day = 16; // member variables accessed using member selection operator (.)
    today.print();  // member functions also accessed using member selection operator (.)

    return 0;
}
此程序编译并产生与上述相同的结果
2020/10/16
非成员示例和成员示例之间有三个主要区别
声明（和定义）
print()
函数的位置
如何调用
print()
函数
如何在
print()
函数内部访问成员
让我们依次探讨这些。
成员函数在类类型定义内部声明
在非成员示例中，
print()
非成员函数是在
Date
结构体之外的全局命名空间中定义的。默认情况下，它具有外部链接，因此可以从其他源文件调用（带有适当的前向声明）。
在成员示例中，
print()
成员函数在
Date
结构体定义内部声明（在本例中也定义）。因为
print()
被声明为
Date
的一部分，这告诉编译器
print()
是一个成员函数。
在类类型定义内部定义的成员函数是隐式内联的，因此如果类类型定义包含在多个代码文件中，它们不会违反一次定义规则。
相关内容
成员函数也可以在类定义内部（前向）声明，并在类定义之后定义。我们将在
15.2 — 类和头文件
课程中介绍这一点。
调用成员函数（以及隐式对象）
在非成员示例中，我们调用
print(today)
，其中
today
作为参数（显式）传递。
在成员示例中，我们调用
today.print()
。此语法使用成员选择运算符 (.) 来选择要调用的成员函数，这与我们访问成员变量的方式一致（例如
today.day = 16;
）。
所有（非静态）成员函数都必须使用该类类型的对象调用。在本例中，
today
是调用
print()
的对象。
请注意，在成员函数的情况下，我们不需要将
today
作为参数传递。调用成员函数的对象会
隐式
传递给成员函数。因此，调用成员函数的对象通常被称为
隐式对象
。
换句话说，当我们调用
today.print()
时，
today
是隐式对象，并且它被隐式地传递给
print()
成员函数。
相关内容
我们将在
15.1 — 隐藏的“this”指针和成员函数链式调用
课程中介绍相关对象实际如何传递给成员函数的机制。
在成员函数内部访问成员使用隐式对象
这是
print()
的非成员版本
// non-member version of print
void print(const Date& date)
{
    // member variables accessed using member selection operator (.)
    std::cout << date.year << '/' << date.month << '/' << date.day;
}
此版本的
print()
具有引用参数
const Date& date
。在函数内部，我们通过此引用参数访问成员，如
date.year
、
date.month
和
date.day
。当调用
print(today)
时，
date
引用参数绑定到参数
today
，并且
date.year
、
date.month
和
date.day
分别求值为
today.year
、
today.month
和
today.day
。
现在我们再次看看
print()
成员函数的定义
void print() // defines a member function named print()
    {
        std::cout << year << '/' << month << '/' << day;
    }
在成员示例中，我们将成员访问为
year
、
month
和
day
。
在成员函数内部，任何未加成员选择运算符 (.) 前缀的成员标识符都与隐式对象关联。
换句话说，当调用
today.print()
时，
today
是我们的隐式对象，并且
year
、
month
和
day
（没有前缀）分别求值为
today.year
、
today.month
和
today.day
的值。
关键见解
对于非成员函数，我们必须显式地将一个对象传递给函数才能使用它，并且成员通过该对象显式地访问。
对于成员函数，我们隐式地将一个对象传递给函数才能使用它，并且成员通过该对象隐式地访问。
另一个成员函数示例
这是一个包含稍微复杂一些的成员函数的示例
#include <iostream>
#include <string>

struct Person
{
    std::string name{};
    int age{};

    void kisses(const Person& person)
    {
        std::cout << name << " kisses " << person.name << '\n';
    }
};

int main()
{
    Person joe{ "Joe", 29 };
    Person kate{ "Kate", 27 };

    joe.kisses(kate);

    return 0;
}
这会产生输出
Joe kisses Kate
我们来研究一下它的工作原理。首先，我们定义了两个
Person
结构体，
joe
和
kate
。接下来，我们调用
joe.kisses(kate)
。这里
joe
是隐式对象，
kate
作为显式参数传递。
当
kisses()
成员函数执行时，标识符
name
没有使用成员选择运算符 (.)，因此它指的是隐式对象，即
joe
。所以这解析为
joe.name
。
person.name
使用了成员选择运算符，因此它不指隐式对象。由于
person
是
kate
的引用，所以这解析为
kate.name
。
关键见解
如果没有成员函数，我们会写
kisses(joe, kate)
。有了成员函数，我们写
joe.kisses(kate)
。请注意后者读起来多么好，以及它如何清楚地表明哪个对象正在发起动作，哪个是辅助对象。
成员变量和函数可以按任何顺序定义
C++ 编译器通常从上到下编译代码。对于遇到的每个名称，编译器都会确定是否已经看到该名称的声明，以便进行正确的类型检查。
非成员必须在使用前声明，否则编译器会报错
int x()
{
    return y(); // error: y not declared yet, so compiler doesn't know what it is
}
 
int y()
{
    return 5;
}
为了解决这个问题，我们通常要么按照大致的使用顺序定义非成员（这在需要更改顺序时需要额外的工作），要么使用前向声明（这需要额外的工作来添加）。
然而，在类定义内部，这个限制不适用：你可以在声明成员变量和成员函数之前访问它们。这意味着你可以按照你喜欢的任何顺序定义成员变量和成员函数！
例如
struct Foo
{
    int z() { return m_data; } // We can access data members before they are defined
    int x() { return y(); }    // We can access member functions before they are defined

    int m_data { y() };        // This even works in default member initializers (see warning below)
    int y() { return 5; }
};
我们将在即将到来的课程
14.8 — 数据隐藏（封装）的好处
中讨论成员定义的推荐顺序。
警告
数据成员按声明顺序初始化。如果数据成员的初始化访问了稍后才声明（因此尚未初始化）的另一个数据成员，则初始化将导致未定义行为。
struct Bad
{
    int m_bad1 { m_data }; // undefined behavior: m_bad1 initialized before m_data
    int m_bad2 { fcn() };  // undefined behavior: m_bad2 initialized before m_data (accessed through fcn())

    int m_data { 5 };
    int fcn() { return m_data; }
};
因此，通常最好避免在默认成员初始化器中使用其他成员。
致进阶读者
为了允许数据成员和成员函数以任何顺序定义，编译器采用了一个巧妙的技巧。当编译器遇到在类定义内部定义的成员函数时
成员函数被隐式前向声明。
成员函数定义紧接着移动到类定义结束之后。
这样，当编译器实际编译成员函数定义时，它已经看到了完整的类定义（包含所有成员的声明！）
例如，当编译器遇到这个时
struct Foo
{
    int z() { return m_data; } // m_data not declared yet
    int x() { return y(); }    // y not declared yet
    int y() { return 5; }

    int m_data{};
};
它将编译等价于此的代码
struct Foo
{
    int z(); // forward declaration of Foo::z()
    int x(); // forward declaration of Foo::x()
    int y(); // forward declaration of Foo::y()

    int m_data{};
};

int Foo::z() { return m_data; } // m_data already declared above
int Foo::x() { return y(); }    // y already declared above
int Foo::y() { return 5; }
成员函数可以重载
就像非成员函数一样，成员函数可以重载，只要每个成员函数都可以区分开来。
相关内容
我们在
11.2 — 函数重载区分
课程中介绍了函数重载区分。
这是一个带有重载
print()
成员函数的
Date
结构体示例
#include <iostream>
#include <string_view>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print()
    {
        std::cout << year << '/' << month << '/' << day;
    }

    void print(std::string_view prefix)
    {
        std::cout << prefix << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 };

    today.print(); // calls Date::print()
    std::cout << '\n';

    today.print("The date is: "); // calls Date::print(std::string_view)
    std::cout << '\n';

    return 0;
}
这会打印
2020/10/14
The date is: 2020/10/14
结构体和成员函数
在 C 语言中，结构体只有数据成员，没有成员函数。
在 C++ 中，在设计类时，Bjarne Stroustrup 花了一些时间考虑是否应允许结构体（从 C 继承而来）拥有成员函数。经过考虑，他认为应该允许。
题外话…
这一决定引发了一系列其他问题，关于结构体应该可以使用哪些其他新的 C++ 功能。Bjarne 担心，如果只允许结构体使用有限的功能子集，最终会增加语言的复杂性和边缘情况。为了简化，他最终决定结构体和类将拥有统一的规则集（这意味着结构体可以做类可以做的一切，反之亦然），并且约定可以规定结构体实际的使用方式。
在现代 C++ 中，结构体可以有成员函数。这不包括构造函数，构造函数是一种特殊的成员函数，我们将在即将到来的课程
14.9 — 构造函数简介
中介绍。带有构造函数的类类型不再是聚合体，而我们希望我们的结构体保持聚合体。
最佳实践
成员函数可以与结构体和类一起使用。
然而，结构体应避免定义构造函数成员函数，因为这样做会使它们成为非聚合体。
没有数据成员的类类型
可以创建没有数据成员的类类型（例如，只有成员函数的类类型）。也可以实例化此类类型的对象
#include <iostream>

struct Foo
{
    void printHi() { std::cout << "Hi!\n"; }
};

int main()
{
    Foo f{};
    f.printHi(); // requires object to call

    return 0;
}
然而，如果一个类类型没有任何数据成员，那么使用类类型可能过于复杂。在这种情况下，考虑使用命名空间（包含非成员函数）代替。这使读者更清楚地知道没有数据被管理（并且不需要实例化对象来调用函数）。
#include <iostream>

namespace Foo
{
    void printHi() { std::cout << "Hi!\n"; }
};

int main()
{
    Foo::printHi(); // no object needed

    return 0;
}
最佳实践
如果你的类类型没有数据成员，请优先使用命名空间。
小测验时间
问题 #1
创建一个名为
IntPair
的结构体，它包含两个整数。添加一个名为
print
的成员函数，用于打印这两个整数的值。
以下程序函数应该可以编译
#include <iostream>

// Provide the definition for IntPair and the print() member function here

int main()
{
	IntPair p1 {1, 2};
	IntPair p2 {3, 4};

	std::cout << "p1: ";
	p1.print();

	std::cout << "p2: ";
	p2.print();

	return 0;
}
并产生输出
p1: Pair(1, 2)
p2: Pair(3, 4)
显示答案
#include <iostream>

struct IntPair
{
	int first{};
	int second{};

	void print()
	{
		std::cout << "Pair(" << first << ", " << second << ")\n";
	}
};

int main()
{
	IntPair p1 {1, 2};
	IntPair p2 {3, 4};

	std::cout << "p1: ";
	p1.print();

	std::cout << "p2: ";
	p2.print();

	return 0;
}
问题 #2
向
IntPair
添加一个名为
isEqual
的新成员函数，该函数返回一个布尔值，指示一个
IntPair
是否等于另一个
IntPair
。
以下程序函数应该可以编译
#include <iostream>

// Provide the definition for IntPair and the member functions here

int main()
{
	IntPair p1 {1, 2};
	IntPair p2 {3, 4};

	std::cout << "p1: ";
	p1.print();

	std::cout << "p2: ";
	p2.print();

	std::cout << "p1 and p1 " << (p1.isEqual(p1) ? "are equal\n" : "are not equal\n");
	std::cout << "p1 and p2 " << (p1.isEqual(p2) ? "are equal\n" : "are not equal\n");

	return 0;
}
并产生输出
p1: Pair(1, 2)
p2: Pair(3, 4)
p1 and p1 are equal
p1 and p2 are not equal
显示答案
#include <iostream>

struct IntPair
{
	int first{};
	int second{};

	void print()
	{
		std::cout << "Pair(" << first << ", " << second << ")\n";
	}

	bool isEqual(IntPair a)
	{
		return (first == a.first) && (second == a.second);
	}
};

int main()
{
	IntPair p1 {1, 2};
	IntPair p2 {3, 4};

	std::cout << "p1: ";
	p1.print();

	std::cout << "p2: ";
	p2.print();

	std::cout << "p1 and p1 " << (p1.isEqual(p1) ? "are equal\n" : "are not equal\n");
	std::cout << "p1 and p2 " << (p1.isEqual(p2) ? "are equal\n" : "are not equal\n");

	return 0;
}
下一课
14.4
Const 类对象和 const 成员函数
返回目录
上一课
14.2
类简介