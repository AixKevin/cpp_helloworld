# 23.2 — 组合

23.2 — 组合
Alex
2007 年 12 月 4 日，下午 2:55 PST
2023 年 9 月 11 日
对象组合
在现实生活中，复杂对象通常由更小、更简单的对象构建。例如，一辆汽车由金属框架、发动机、轮胎、变速箱、方向盘以及大量其他部件构成。一台个人电脑由 CPU、主板、内存等构成……甚至你也是由更小的部分构成：你有头部、身体、腿、手臂等等。这种用更简单的对象构建复杂对象的过程称为
对象组合
。
广义地说，对象组合建模了两个对象之间的“拥有”（has-a）关系。一辆汽车“拥有”一个变速箱。你的电脑“拥有”一个 CPU。你“拥有”一颗心脏。复杂对象有时被称为整体或父级。简单对象通常被称为部分、子级或组件。
在 C++ 中，你已经看到结构体和类可以拥有各种类型的数据成员（例如基本类型或其他类）。当我们用数据成员构建类时，我们实际上是在用更简单的部分构造一个复杂对象，这就是对象组合。因此，结构体和类有时被称为
复合类型
。
对象组合在 C++ 环境中很有用，因为它允许我们通过组合更简单、更容易管理的部分来创建复杂类。这降低了复杂性，并允许我们更快、更少错误地编写代码，因为我们可以重用已经编写、测试和验证过的代码。
对象组合的类型
对象组合有两种基本的子类型：组合和聚合。我们将在本课中探讨组合，在下一课中探讨聚合。
术语说明：“组合”一词通常既指组合也指聚合，而不仅仅指组合子类型。在本教程中，当我们指两者时，我们将使用“对象组合”一词；当我们特指组合子类型时，我们将使用“组合”。
组合
要符合
组合
的条件，对象和部分必须具有以下关系：
部分（成员）是对象（类）的一部分
该部分（成员）一次只能属于一个对象（类）
该部分（成员）的存在由该对象（类）管理
部分（成员）不知道对象（类）的存在
组合的一个很好的现实生活例子是人的身体和心脏之间的关系。让我们更详细地研究这些。
组合关系是部分-整体关系，其中部分必须构成整体对象的一部分。例如，心脏是人体的一部分。组合中的部分一次只能是一个对象的一部分。一个人身体中的心脏不能同时是另一个人的身体的一部分。
在组合关系中，对象负责部分的存在。通常，这意味着部分在对象创建时创建，在对象销毁时销毁。但更广泛地说，它意味着对象以一种用户无需参与的方式管理部分的生命周期。例如，当身体被创建时，心脏也随之创建。当一个人的身体被销毁时，他们的心脏也随之销毁。因此，组合有时被称为“死亡关系”。
最后，部分不知道整体的存在。你的心脏快乐地运作着，却不知道它是更大结构的一部分。我们称之为
单向
关系，因为身体知道心脏，反之则不然。
请注意，组合与部分的转移性无关。心脏可以从一个身体移植到另一个身体。然而，即使在移植后，它仍然符合组合的要求（心脏现在归接收者所有，并且只能是接收者对象的一部分，除非再次转移）。
我们无处不在的 Fraction 类是组合的一个很好的例子
class Fraction
{
private:
	int m_numerator;
	int m_denominator;
 
public:
	Fraction(int numerator=0, int denominator=1)
		: m_numerator{ numerator }, m_denominator{ denominator }
	{
	}
};
这个类有两个数据成员：一个分子和一个分母。分子和分母是 Fraction 的一部分（包含在其中）。它们不能一次属于多个 Fraction。分子和分母不知道它们是 Fraction 的一部分，它们只是保存整数。当 Fraction 实例创建时，分子和分母也随之创建。当 Fraction 实例销毁时，分子和分母也随之销毁。
虽然对象组合建模了“拥有”（has-a）类型关系（一个身体拥有心脏，一个分数拥有分母），但我们可以更精确地说，组合建模了“一部分”（part-of）关系（心脏是身体的一部分，分子是分数的一部分）。组合通常用于建模物理关系，其中一个对象物理上包含在另一个对象内部。
对象组合的部分可以是单一的，也可以是多重的——例如，心脏是身体的单一组成部分，但身体包含 10 根手指（可以建模为数组）。
实现组合
组合是 C++ 中最容易实现的关系类型之一。它们通常被创建为带有普通数据成员的结构体或类。因为这些数据成员直接作为结构体/类的一部分存在，所以它们的生命周期与类实例本身的生命周期绑定在一起。
需要进行动态分配或释放的组合可以使用指针数据成员实现。在这种情况下，组合类应负责自行完成所有必要的内存管理（而不是类的用户）。
一般来说，如果你“可以”使用组合来设计一个类，你就“应该”使用组合来设计一个类。使用组合设计的类是直接、灵活和健壮的（因为它们能很好地自行清理）。
更多例子
许多游戏和模拟中有生物或物体在棋盘、地图或屏幕上移动。所有这些生物/物体都有一个共同点，那就是它们都有一个位置。在这个例子中，我们将创建一个使用点类来保存生物位置的生物类。
首先，让我们设计点类。我们的生物将生活在一个二维世界中，所以我们的点类将有 X 和 Y 两个维度。我们将假设世界由离散的方格组成，所以这些维度将始终是整数。
Point2D.h
#ifndef POINT2D_H
#define POINT2D_H

#include <iostream>

class Point2D
{
private:
    int m_x;
    int m_y;

public:
    // A default constructor
    Point2D()
        : m_x{ 0 }, m_y{ 0 }
    {
    }

    // A specific constructor
    Point2D(int x, int y)
        : m_x{ x }, m_y{ y }
    {
    }

    // An overloaded output operator
    friend std::ostream& operator<<(std::ostream& out, const Point2D& point)
    {
        out << '(' << point.m_x << ", " << point.m_y << ')';
        return out;
    }

    // Access functions
    void setPoint(int x, int y)
    {
        m_x = x;
        m_y = y;
    }

};

#endif
请注意，由于我们将所有函数都实现在头文件中（为了保持示例简洁），所以没有 Point2D.cpp。
这个 Point2d 类是其组成部分的组合：位置值 x 和 y 是 Point2D 的一部分，它们的生命周期与给定 Point2D 实例的生命周期相关联。
现在让我们设计我们的 Creature。我们的 Creature 将有一些属性：一个字符串类型的名称，以及一个 Point2D 类类型的位置。
Creature.h
#ifndef CREATURE_H
#define CREATURE_H

#include <iostream>
#include <string>
#include <string_view>
#include "Point2D.h"

class Creature
{
private:
    std::string m_name;
    Point2D m_location;

public:
    Creature(std::string_view name, const Point2D& location)
        : m_name{ name }, m_location{ location }
    {
    }

    friend std::ostream& operator<<(std::ostream& out, const Creature& creature)
    {
        out << creature.m_name << " is at " << creature.m_location;
        return out;
    }

    void moveTo(int x, int y)
    {
        m_location.setPoint(x, y);
    }
};
#endif
这个 Creature 也是其组成部分的组合。生物的名称和位置只有一个父级，它们的生命周期与它们所属的 Creature 的生命周期绑定。
最后，main.cpp
#include <string>
#include <iostream>
#include "Creature.h"
#include "Point2D.h"

int main()
{
    std::cout << "Enter a name for your creature: ";
    std::string name;
    std::cin >> name;
    Creature creature{ name, { 4, 7 } };
	
    while (true)
    {
        // print the creature's name and location
        std::cout << creature << '\n';

        std::cout << "Enter new X location for creature (-1 to quit): ";
        int x{ 0 };
        std::cin >> x;
        if (x == -1)
            break;

        std::cout << "Enter new Y location for creature (-1 to quit): ";
        int y{ 0 };
        std::cin >> y;
        if (y == -1)
            break;
		
        creature.moveTo(x, y);
    }

    return 0;
}
这是此代码运行的输出：
Enter a name for your creature: Marvin
Marvin is at (4, 7)
Enter new X location for creature (-1 to quit): 6
Enter new Y location for creature (-1 to quit): 12
Marvin is at (6, 12)
Enter new X location for creature (-1 to quit): 3
Enter new Y location for creature (-1 to quit): 2
Marvin is at (3, 2)
Enter new X location for creature (-1 to quit): -1
组合主题的变体
尽管大多数组合在创建时直接创建其部件，在销毁时直接销毁其部件，但有些组合的变体稍微突破了这些规则。
例如
组合可以推迟某些部分的创建，直到需要它们。例如，一个字符串类可能直到用户为其分配要保存的数据时才创建动态字符数组。
组合可以选择使用作为输入给它的部分，而不是自己创建该部分。
组合可以将其部分的销毁委托给其他对象（例如，委托给垃圾回收例程）。
这里的关键点是，组合应该管理其部分，而无需组合的用户进行任何管理。
组合和类成员
初学者在学习对象组合时经常问的一个问题是：“我什么时候应该使用类成员而不是直接实现一个功能？” 例如，我们本可以不使用 Point2D 类来表示 Creature 的位置，而是向 Creature 类添加 2 个整数，并在 Creature 类中编写代码来处理定位。然而，将 Point2D 独立为一个类（并作为 Creature 的成员）具有许多优点：
每个单独的类都可以保持相对简单和直接，专注于出色地完成一项任务。这使得这些类更容易编写和理解，因为它们更专注。例如，Point2D 只关心与点相关的事情，这有助于保持其简单。
每个类都可以是自包含的，这使得它们可以重用。例如，我们可以在一个完全不同的应用程序中重用我们的 Point2D 类。或者如果我们的生物需要另一个点（例如，它试图到达的目的地），我们可以简单地添加另一个 Point2D 成员变量。
外部类可以让类成员完成大部分繁重的工作，而将精力集中在协调成员之间的数据流上。这有助于降低外部类的整体复杂性，因为它可以将任务委托给其成员，而成员已经知道如何执行这些任务。例如，当我们移动我们的 Creature 时，它将该任务委托给 Point 类，而 Point 类已经知道如何设置一个点。因此，Creature 类不必担心如何实现这些事情。
提示
一个好的经验法则是，每个类都应该构建为完成一项任务。该任务要么是某种数据的存储和操作（例如 Point2D、std::string），要么是其成员的协调（例如 Creature）。理想情况下，两者兼顾。
在我们的示例中，Creature 不必担心 Point 是如何实现的，或者名称是如何存储的，这是有道理的。Creature 的工作不是要知道这些内部细节。Creature 的工作是担心如何协调数据流，并确保每个类成员都知道它应该做什么。至于它们将如何去做，则由各个类来负责。
下一课
23.3
聚合
返回目录
上一课
23.1
对象关系