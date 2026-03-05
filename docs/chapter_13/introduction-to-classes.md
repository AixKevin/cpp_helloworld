# 14.2 — 类简介

14.2 — 类简介
Alex
2023年9月11日，太平洋夏令时12:14
2024年6月26日
在上一章中，我们讨论了结构体 (
13.7 -- 结构体、成员和成员选择简介
)，并讨论了它们如何非常适合将多个成员变量捆绑到一个可以作为单元初始化和传递的单个对象中。换句话说，结构体为存储和移动相关数据值提供了方便的封装。
考虑以下结构体
#include <iostream>

struct Date
{
    int day{};
    int month{};
    int year{};
};

void printDate(const Date& date)
{
    std::cout << date.day << '/' << date.month << '/' << date.year; // assume DMY format
}

int main()
{
    Date date{ 4, 10, 21 }; // initialize using aggregate initialization
    printDate(date);        // can pass entire struct to function

    return 0;
}
在上面的例子中，我们创建了一个
Date
对象，然后将其传递给一个打印日期的函数。这个程序打印
4/10/21
提醒
在这些教程中，我们所有的结构体都是聚合类型。我们在课程
13.8 -- 结构体聚合初始化
中讨论聚合类型。
尽管结构体很有用，但它们存在许多缺陷，这在尝试构建大型复杂程序（尤其是由多个开发人员协作开发的程序）时可能会带来挑战。
类不变式问题
也许结构体最大的困难在于它们无法提供有效的方法来文档化和强制执行类不变式。在课程
9.6 -- 断言和 static_assert
中，我们将不变式定义为“在某个组件执行期间必须为真的条件”。
在类类型（包括结构体、类和联合体）的上下文中，
类不变式
是一个在对象的整个生命周期内必须为真的条件，以便对象保持有效状态。违反类不变式的对象被称为处于
无效状态
，并且进一步使用该对象可能会导致意外或未定义行为。
关键见解
使用其类不变式已被违反的对象可能会导致意外或未定义行为。
首先，考虑以下结构体
struct Pair
{
    int first {};
    int second {};
};
first
和
second
成员可以独立设置为任何值，因此
Pair
结构体没有不变式。
现在考虑以下几乎相同的结构体
struct Fraction
{
    int numerator { 0 };
    int denominator { 1 };
};
我们从数学中知道，分母为
0
的分数在数学上是未定义的（因为分数的值是其分子除以其分母——而除以
0
在数学上是未定义的）。因此，我们希望确保 Fraction 对象的
denominator
成员永远不会设置为
0
。如果设置为
0
，则该 Fraction 对象处于无效状态，并且进一步使用该对象可能会导致未定义行为。
例如
#include <iostream>

struct Fraction
{
    int numerator { 0 };
    int denominator { 1 }; // class invariant: should never be 0
};

void printFractionValue(const Fraction& f)
{
     std::cout << f.numerator / f.denominator << '\n';
}

int main()
{
    Fraction f { 5, 0 };   // create a Fraction with a zero denominator
    printFractionValue(f); // cause divide by zero error

    return 0;
}
在上面的例子中，我们使用注释来文档化 Fraction 的不变式。我们还提供了一个默认成员初始化器，以确保如果用户未提供初始化值，则分母设置为
1
。这确保了如果用户决定值初始化 Fraction 对象，我们的 Fraction 对象将是有效的。这是一个不错的开始。
但没有什么能阻止我们明确违反此类的这个不变式：当我们创建
Fraction f
时，我们使用聚合初始化显式地将分母初始化为
0
。虽然这不会立即导致问题，但我们的对象现在处于无效状态，并且进一步使用该对象可能会导致意外或未定义行为。
而这正是我们稍后调用
printFractionValue(f)
时所看到的：程序因除以零错误而终止。
题外话…
一个小的改进是在
printFractionValue
函数体顶部添加
assert(f.denominator != 0);
。这增加了代码的文档价值，并使哪个前置条件被违反变得更加明显。然而，从行为上来说，这并没有真正改变任何东西。我们真正希望在问题源头（当成员被初始化或分配了错误值时）捕获这些问题，而不是在某个下游（当使用了错误值时）。
鉴于 Fraction 示例的相对简单性，避免创建无效的 Fraction 对象应该不会太难。然而，在更复杂的代码库中，它使用许多结构体、具有许多成员的结构体或成员之间具有复杂关系的结构体，理解哪种值的组合可能违反某些类不变式可能不那么明显。
一个更复杂的类不变式
Fraction 的类不变式很简单——
denominator
成员不能为
0
。这在概念上很容易理解，并且不难避免。
当结构体的成员必须具有相关值时，类不变式变得更具挑战性。
#include <string>

struct Employee
{
    std::string name { };
    char firstInitial { }; // should always hold first character of `name` (or `0`)
};
在上述（设计不良的）结构体中，存储在成员
firstInitial
中的字符值应始终与
name
的第一个字符匹配。
当
Employee
对象被初始化时，用户负责确保维护类不变式。如果
name
曾被赋予新值，用户也有责任确保
firstInitial
也随之更新。这种关联对于使用 Employee 对象的开发人员来说可能不明显，即使明显，他们也可能忘记这样做。
即使我们编写函数来帮助我们创建和更新 Employee 对象（确保
firstInitial
始终从
name
的第一个字符设置），我们仍然依赖用户了解并使用这些函数。
简而言之，依赖对象用户维护类不变式很可能会导致有问题的代码。
关键见解
依赖对象的用户维护类不变式很可能会导致问题。
理想情况下，我们希望我们的类类型能够“防弹”，这样对象要么无法进入无效状态，要么能够立即发出信号（而不是让未定义行为在未来的某个随机点发生）。
结构体（作为聚合体）只是没有以优雅方式解决此问题所需的机制。
类简介
在开发 C++ 时，Bjarne Stroustrup 希望引入能够让开发人员创建更直观地使用的程序定义类型的能力。他还对寻找优雅的解决方案感兴趣，以解决困扰大型复杂程序的一些常见陷阱和维护挑战（例如前面提到的类不变式问题）。
凭借他使用其他编程语言（特别是 Simula，第一种面向对象编程语言）的经验，Bjarne 坚信可以开发出一种通用且功能强大的程序定义类型，几乎可以用于任何事物。为了向 Simula 致敬，他将这种类型称为
类
。
就像结构体一样，
类
是一种程序定义的复合类型，可以包含许多具有不同类型的成员变量。
关键见解
从技术角度来看，结构体和类几乎相同——因此，任何使用结构体实现的示例都可以使用类实现，反之亦然。然而，从实际角度来看，我们使用结构体和类的方式不同。
我们将在课程
14.5 -- 公有和私有成员以及访问说明符
中介绍结构体和类之间的技术和实际差异
相关内容
我们将在课程
14.8 -- 数据隐藏（封装）的优点
中介绍类如何解决不变式问题。
定义一个类
因为类是一种程序定义的数据类型，所以它必须在使用之前进行定义。类的定义与结构体类似，只是我们使用
class
关键字而不是
struct
。例如，这是一个简单员工类的定义
class Employee
{
    int m_id {};
    int m_age {};
    double m_wage {};
};
相关内容
我们将在即将到来的课程
14.5 -- 公有和私有成员以及访问说明符
中讨论为什么类的成员变量通常以“m_”作为前缀
为了展示类和结构体有多么相似，以下程序与我们在课程开头介绍的程序是等效的，只是
Date
现在是一个类而不是一个结构体
#include <iostream>

class Date       // we changed struct to class
{
public:          // and added this line, which is called an access specifier
    int m_day{}; // and added "m_" prefixes to each of the member names
    int m_month{};
    int m_year{};
};

void printDate(const Date& date)
{
    std::cout << date.m_day << '/' << date.m_month << '/' << date.m_year;
}

int main()
{
    Date date{ 4, 10, 21 };
    printDate(date);

    return 0;
}
这会打印
4/10/21
相关内容
我们将在即将到来的课程
14.5 -- 公有和私有成员以及访问说明符
中介绍什么是访问说明符。
C++ 标准库的大部分都是类
您可能已经在使用类对象，也许没有意识到。
std::string
和
std::string_view
都被定义为类。事实上，标准库中大多数非别名类型都被定义为类！
类是 C++ 的核心和灵魂——它们是如此基础，以至于 C++ 最初被命名为“带类的 C”！一旦您熟悉了类，您在 C++ 中的大部分时间都将花在编写、测试和使用它们上。
小测验时间
问题 #1
给定一组值（年龄、地址编号等），我们可能想知道该集合中的最小值和最大值是什么。由于最小值和最大值是相关的，我们可以将它们组织在一个结构体中，如下所示
struct minMax
{
    int min; // holds the minimum value seen so far
    int max; // holds the maximum value seen so far
};
然而，如上所示，这个结构体有一个未指定的类不变式。不变式是什么？
显示答案
不变式是
min <= max
。如果
min
曾经大于
max
，任何使用此结构体的代码都可能出现故障。
下一课
14.3
成员函数
返回目录
上一课
14.1
面向对象编程简介