# 13.7 — Structs、成员和成员选择的简介

13.7 — Structs、成员和成员选择的简介
Alex
2007 年 6 月 20 日，太平洋夏令时下午 6:34
2024 年 10 月 4 日
在编程中，很多情况下我们需要不止一个变量来表示某个感兴趣的事物。正如我们在上一章的介绍中所讨论的 (
12.1 -- 复合数据类型简介
)，分数有分子和分母，它们作为一个单一的数学对象链接在一起。
或者，假设我们想编写一个程序，需要存储公司员工的信息。我们可能感兴趣的属性包括员工姓名、职务、年龄、员工 ID、经理 ID、工资、生日、入职日期等……
如果我们要使用独立的变量来跟踪所有这些信息，那可能看起来像这样
std::string name;
std::string title;
int age;
int id;
int managerId;
double wage;
int birthdayYear;
int birthdayMonth;
int birthdayDay;
int hireYear;
int hireMonth;
int hireDay;
然而，这种方法存在许多问题。首先，不清楚这些变量是否实际相关（您必须阅读注释，或查看它们在上下文中的使用方式）。其次，现在有 12 个变量需要管理。如果我们要将这个员工传递给一个函数，我们必须传递 12 个参数（并且按正确的顺序），这将使我们的函数原型和函数调用变得一团糟。由于函数只能返回单个值，函数如何才能返回一个员工呢？
如果我们需要不止一个员工，我们需要为每个额外的员工定义 12 个变量（每个变量都需要一个唯一的名称）！这显然根本无法扩展。我们真正需要的是一种方法来将所有这些相关的数据组织在一起，使它们更易于管理。
幸运的是，C++ 提供了两种复合类型来解决这些挑战：structs（我们现在将介绍）和 classes（我们很快就会探索）。
struct
（
structure
的缩写）是一种程序定义的数据类型 (
13.1 -- 程序定义（用户定义）类型简介
)，它允许我们将多个变量捆绑到一个单一类型中。正如您很快就会看到的，这使得相关变量集的管理变得简单得多！
提醒
struct 是一种类类型（类和 union 也是）。因此，任何适用于类类型的东西也适用于 struct。
定义 struct
因为 struct 是一种程序定义类型，我们必须先告诉编译器我们的 struct 类型是什么样子，然后才能开始使用它。以下是一个简化的 employee struct 定义示例
struct Employee
{
    int id {};
    int age {};
    double wage {};
};
struct
关键字用于告诉编译器我们正在定义一个 struct，我们将其命名为
Employee
（因为程序定义类型通常以大写字母开头）。
然后，在一对花括号内，我们定义每个 Employee 对象将包含的变量。在这个例子中，我们创建的每个
Employee
都将有 3 个变量：一个
int id
、一个
int age
和一个
double wage
。作为 struct 一部分的变量称为
数据成员
（或
成员变量
）。
提示
在日常语言中，
成员
是指属于某个群体的一个个体。例如，您可能是篮球队的一员，而您的妹妹可能是合唱团的一员。
在 C++ 中，
成员
是属于 struct（或 class）的变量、函数或类型。所有成员都必须在 struct（或 class）定义中声明。
在未来的课程中，我们将大量使用“成员”这个术语，因此请确保您记住它的含义。
就像我们使用一对空花括号来值初始化 (
1.4 -- 变量赋值和初始化
) 普通变量一样，每个成员变量后的空花括号确保在创建
Employee
时，我们
Employee
内部的成员变量被值初始化。我们将在几节课中讨论默认成员初始化时进一步讨论这一点 (
13.9 -- 默认成员初始化
)。
最后，我们用分号结束类型定义。
提醒一下，
Employee
只是一个类型定义——此时实际上没有创建任何对象。
定义 struct 对象
要使用
Employee
类型，我们只需定义一个
Employee
类型的变量
Employee joe {}; // Employee is the type, joe is the variable name
这定义了一个名为
joe
的
Employee
类型的变量。当代码执行时，将实例化一个包含 3 个数据成员的 Employee 对象。空花括号确保我们的对象被值初始化。
就像任何其他类型一样，可以定义同一 struct 类型的多个变量
Employee joe {}; // create an Employee struct for Joe
Employee frank {}; // create an Employee struct for Frank
访问成员
考虑以下示例
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};

    return 0;
}
在上面的例子中，名称
joe
指的是整个 struct 对象（其中包含成员变量）。要访问特定的成员变量，我们使用
成员选择运算符
（
operator.
）在 struct 变量名和成员名之间。例如，要访问 Joe 的年龄成员，我们使用
joe.age
。
Struct 成员变量就像普通变量一样工作，因此可以对它们执行正常操作，包括赋值、算术、比较等……
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};

    joe.age = 32;  // use member selection operator (.) to select the age member of variable joe

    std::cout << joe.age << '\n'; // print joe's age

    return 0;
}
这会打印
32
struct 的最大优点之一是，我们只需为每个 struct 变量创建一个新名称（成员名称作为 struct 类型定义的一部分是固定的）。在下面的示例中，我们实例化了两个
Employee
对象：
joe
和
frank
。
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};
    joe.id = 14;
    joe.age = 32;
    joe.wage = 60000.0;

    Employee frank {};
    frank.id = 15;
    frank.age = 28;
    frank.wage = 45000.0;

    int totalAge { joe.age + frank.age };
    std::cout << "Joe and Frank have lived " << totalAge << " total years\n";

    if (joe.wage > frank.wage)
        std::cout << "Joe makes more than Frank\n";
    else if (joe.wage < frank.wage)
        std::cout << "Joe makes less than Frank\n";
    else
        std::cout << "Joe and Frank make the same amount\n";

    // Frank got a promotion
    frank.wage += 5000.0;

    // Today is Joe's birthday
    ++joe.age; // use pre-increment to increment Joe's age by 1

    return 0;
}
在上面的例子中，很容易分辨哪些成员变量属于 Joe，哪些属于 Frank。这提供了比独立变量更高的组织级别。此外，由于 Joe 和 Frank 的成员具有相同的名称，这在您有多个相同 struct 类型的变量时提供了连贯性。
我们将在下一课中继续探索 struct，包括如何初始化它们。
下一课
13.8
Struct 聚合初始化
返回目录
上一课
13.6
作用域枚举（enum class）