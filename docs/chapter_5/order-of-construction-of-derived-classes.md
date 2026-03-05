# 24.3 — 派生类的构造顺序

24.3 — 派生类的构造顺序
Alex
2008 年 1 月 7 日，下午 4:18（太平洋标准时间）
2024 年 4 月 30 日
在上一节关于
C++ 基本继承
的课程中，你了解到类可以从其他类继承成员和函数。在本节中，我们将仔细研究派生类实例化时发生的构造顺序。
首先，我们介绍一些新的类，它们将帮助我们阐明一些重要的观点。
class Base
{
public:
    int m_id {};

    Base(int id=0)
        : m_id { id }
    {
    }

    int getId() const { return m_id; }
};

class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0)
        : m_cost { cost }
    {
    }

    double getCost() const { return m_cost; }
};
在这个例子中，类 `Derived` 派生自类 `Base`。
因为 `Derived` 继承了 `Base` 的函数和变量，你可能会认为 `Base` 的成员被复制到了 `Derived` 中。然而，事实并非如此。相反，我们可以将 `Derived` 视为一个由两部分组成的类：一部分是 `Derived`，一部分是 `Base`。
你已经看到很多实例化普通（非派生）类时会发生什么情况的例子了
int main()
{
    Base base;

    return 0;
}
`Base` 是一个非派生类，因为它不继承自任何其他类。C++ 为 `Base` 分配内存，然后调用 `Base` 的默认构造函数进行初始化。
现在我们来看看实例化派生类时会发生什么
int main()
{
    Derived derived;

    return 0;
}
如果你自己尝试这个，你不会注意到与我们实例化非派生类 `Base` 的前一个例子有任何区别。但在幕后，事情发生的方式略有不同。如上所述，`Derived` 实际上是两部分：`Base` 部分和 `Derived` 部分。当 C++ 构造派生对象时，它分阶段进行。首先，构造最基类（在继承树的顶部）。然后按顺序构造每个子类，直到最后构造最子类（在继承树的底部）。
因此，当我们实例化 `Derived` 的一个实例时，首先构造 `Derived` 的 `Base` 部分（使用 `Base` 默认构造函数）。一旦 `Base` 部分完成，就构造 `Derived` 部分（使用 `Derived` 默认构造函数）。此时，没有更多的派生类，所以我们完成了。
这个过程实际上很容易说明。
#include <iostream>

class Base
{
public:
    int m_id {};

    Base(int id=0)
        : m_id { id }
    {
        std::cout << "Base\n";
    }

    int getId() const { return m_id; }
};

class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0)
        : m_cost { cost }
    {
        std::cout << "Derived\n";
    }

    double getCost() const { return m_cost; }
};

int main()
{
    std::cout << "Instantiating Base\n";
    Base base;

    std::cout << "Instantiating Derived\n";
    Derived derived;

    return 0;
}
此程序产生以下结果：
Instantiating Base
Base
Instantiating Derived
Base
Derived
正如你所看到的，当我们构造 `Derived` 时，`Derived` 的 `Base` 部分首先被构造。这是有道理的：逻辑上，没有父类，子类就无法存在。这也是安全的做法：子类经常使用父类的变量和函数，但父类对子类一无所知。首先实例化父类可确保这些变量在派生类创建并准备使用它们时已经初始化。
继承链的构造顺序
有时类派生自其他类，而这些类本身又派生自其他类。例如
#include <iostream>

class A
{
public:
    A()
    {
        std::cout << "A\n";
    }
};

class B: public A
{
public:
    B()
    {
        std::cout << "B\n";
    }
};

class C: public B
{
public:
    C()
    {
        std::cout << "C\n";
    }
};

class D: public C
{
public:
    D()
    {
        std::cout << "D\n";
    }
};
请记住，C++ 总是首先构造“第一个”或“最基”的类。然后它按顺序遍历继承树并构造每个后续的派生类。
这是一个简短的程序，它说明了沿继承链的所有创建顺序。
int main()
{
    std::cout << "Constructing A: \n";
    A a;

    std::cout << "Constructing B: \n";
    B b;

    std::cout << "Constructing C: \n";
    C c;

    std::cout << "Constructing D: \n";
    D d;
}
此代码打印以下内容
Constructing A:
A
Constructing B:
A
B
Constructing C:
A
B
C
Constructing D:
A
B
C
D
总结
C++ 分阶段构造派生类，从最基类（在继承树的顶部）开始，到最子类（在继承树的底部）结束。当每个类被构造时，将调用该类中相应的构造函数来初始化该类的该部分。
你会注意到本节中的示例类都使用了基类默认构造函数（为了简单起见）。在下一节中，我们将更深入地了解构造函数在构造派生类过程中的作用（包括如何明确选择派生类要使用的基类构造函数）。
下一课
24.4
派生类的构造函数和初始化
返回目录
上一课
24.2
C++ 中的基本继承