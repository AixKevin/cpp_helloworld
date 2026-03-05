# 24.4 — 构造函数和派生类的初始化

24.4 — 构造函数和派生类的初始化
Alex
2008年1月9日，太平洋标准时间下午2:36
2023年9月11日
在过去的两个课程中，我们探索了C++中继承的一些基础知识以及派生类的初始化顺序。在本课程中，我们将更深入地研究构造函数在派生类初始化中的作用。为此，我们将继续使用我们在上一课中开发的简单Base和Derived类。
class Base
{
public:
    int m_id {};
 
    Base(int id=0)
        : m_id{ id }
    {
    }
 
    int getId() const { return m_id; }
};
 
class Derived: public Base
{
public:
    double m_cost {};
 
    Derived(double cost=0.0)
        : m_cost{ cost }
    {
    }
 
    double getCost() const { return m_cost; }
};
对于非派生类，构造函数只需要关注它们自己的成员。例如，考虑Base。我们可以像这样创建一个Base对象：
int main()
{
    Base base{ 5 }; // use Base(int) constructor

    return 0;
}
当base被实例化时，实际发生的情况是：
为base分配内存
调用适当的Base构造函数
成员初始化列表初始化变量
构造函数体执行
控制权返回给调用者
这相当直接。对于派生类，事情稍微复杂一些。
int main()
{
    Derived derived{ 1.3 }; // use Derived(double) constructor

    return 0;
}
当derived被实例化时，实际发生的情况是：
为derived分配内存（足以容纳Base和Derived两部分）
调用适当的Derived构造函数
首先使用适当的Base构造函数构造Base对象
。如果没有指定基类构造函数，将使用默认构造函数。
成员初始化列表初始化变量
构造函数体执行
控制权返回给调用者
这种情况与非继承情况之间唯一的真正区别是，在Derived构造函数做任何实质性工作之前，Base构造函数会首先被调用。Base构造函数设置对象的Base部分，控制权返回给Derived构造函数，然后Derived构造函数完成其工作。
初始化基类成员
我们目前编写的Derived类的一个缺点是，在创建Derived对象时无法初始化m_id。如果我们在创建Derived对象时希望同时设置m_cost（来自对象的Derived部分）和m_id（来自对象的Base部分），该怎么办？
新程序员通常尝试通过以下方式解决此问题：
class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0, int id=0)
        // does not work
        : m_cost{ cost }
        , m_id{ id }
    {
    }

    double getCost() const { return m_cost; }
};
这是一个很好的尝试，思路几乎正确。我们确实需要向构造函数添加另一个参数，否则C++将无法知道我们希望将m_id初始化为哪个值。
然而，C++阻止类在构造函数的成员初始化列表中初始化继承的成员变量。换句话说，成员变量的值只能在其所属类的构造函数的成员初始化列表中设置。
为什么C++要这样做？答案与const和引用变量有关。考虑如果m_id是const会发生什么。由于const变量必须在创建时用值初始化，因此基类构造函数必须在变量创建时设置其值。然而，当基类构造函数完成时，派生类构造函数的成员初始化列表随后执行。每个派生类都有机会初始化该变量，可能会改变其值！通过限制变量的初始化到这些变量所属的类的构造函数，C++确保所有变量只初始化一次。
最终结果是上面的例子不起作用，因为m_id是从Base继承的，并且只有非继承变量才能在成员初始化列表中初始化。
然而，继承的变量仍然可以在构造函数体内使用赋值来改变它们的值。因此，新程序员也经常尝试这种做法：
class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0, int id=0)
        : m_cost{ cost }
    {
        m_id = id;
    }

    double getCost() const { return m_cost; }
};
虽然这在这种情况下确实有效，但如果m_id是const或引用，它将不起作用（因为const值和引用必须在构造函数的成员初始化列表中初始化）。它也效率低下，因为m_id被赋值两次：一次在Base类构造函数的成员初始化列表中，然后再次在Derived类构造函数的函数体内。最后，如果Base类在构造期间需要访问这个值怎么办？它无法访问它，因为它直到Derived构造函数执行（几乎是最后执行的）才被设置。
那么，在创建Derived类对象时，我们如何正确初始化m_id呢？
到目前为止的所有例子中，当我们实例化一个Derived类对象时，Base类部分都是使用默认的Base构造函数创建的。为什么它总是使用默认的Base构造函数？因为我们从未告诉它做其他事情！
幸运的是，C++允许我们明确选择要调用的Base类构造函数！为此，只需在派生类的成员初始化列表中添加对Base类构造函数的调用即可。
class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0, int id=0)
        : Base{ id } // Call Base(int) constructor with value id!
        , m_cost{ cost }
    {
    }

    double getCost() const { return m_cost; }
};
现在，当我们执行这段代码时
#include <iostream>

int main()
{
    Derived derived{ 1.3, 5 }; // use Derived(double, int) constructor
    std::cout << "Id: " << derived.getId() << '\n';
    std::cout << "Cost: " << derived.getCost() << '\n';

    return 0;
}
基类构造函数Base(int)将用于将m_id初始化为5，派生类构造函数将用于将m_cost初始化为1.3！
因此，程序将打印
Id: 5
Cost: 1.3
更详细地说，发生的情况是：
为派生对象分配内存。
调用Derived(double, int)构造函数，其中cost = 1.3，id = 5。
编译器检查我们是否要求了特定的Base类构造函数。我们要求了！所以它调用Base(int)，id = 5。
基类构造函数成员初始化列表将m_id设置为5。
基类构造函数体执行，它什么也不做。
基类构造函数返回。
派生类构造函数成员初始化列表将m_cost设置为1.3。
派生类构造函数体执行，它什么也不做。
派生类构造函数返回。
这可能看起来有些复杂，但实际上非常简单。所发生的一切是Derived构造函数正在调用一个特定的Base构造函数来初始化对象的Base部分。因为m_id存在于对象的Base部分，所以Base构造函数是唯一可以初始化该值的构造函数。
请注意，Base构造函数在Derived构造函数成员初始化列表中的位置无关紧要——它总是会首先执行。
现在我们可以将成员设为私有
既然您知道如何初始化基类成员，就不需要将我们的成员变量保持为public。我们将成员变量再次设为private，这是它们应有的状态。
快速回顾一下，公共成员可以被任何人访问。私有成员只能由同一类的成员函数访问。请注意，这意味着派生类不能直接访问基类的私有成员！派生类需要使用访问函数来访问基类的私有成员。
考虑
#include <iostream>

class Base
{
private: // our member is now private
    int m_id {};
 
public:
    Base(int id=0)
        : m_id{ id }
    {
    }
 
    int getId() const { return m_id; }
};

class Derived: public Base
{
private: // our member is now private
    double m_cost;

public:
    Derived(double cost=0.0, int id=0)
        : Base{ id } // Call Base(int) constructor with value id!
        , m_cost{ cost }
    {
    }

    double getCost() const { return m_cost; }
};

int main()
{
    Derived derived{ 1.3, 5 }; // use Derived(double, int) constructor
    std::cout << "Id: " << derived.getId() << '\n';
    std::cout << "Cost: " << derived.getCost() << '\n';

    return 0;
}
在上面的代码中，我们将m_id和m_cost设为私有。这没问题，因为我们使用相关的构造函数来初始化它们，并使用公共访问器来获取这些值。
正如预期的那样，这会打印出
Id: 5
Cost: 1.3
我们将在下一课中讨论更多关于访问说明符的内容。
另一个例子
让我们看看我们之前使用过的另一对类：
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name;
    int m_age {};

    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

// BaseballPlayer publicly inheriting Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage {};
    int m_homeRuns {};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{ battingAverage },
         m_homeRuns{ homeRuns }
    {
    }
};
正如我们之前所写的，BaseballPlayer只初始化它自己的成员，并且没有指定要使用的Person构造函数。这意味着我们创建的每个BaseballPlayer都将使用默认的Person构造函数，它会将姓名初始化为空，年龄初始化为0。因为在创建BaseballPlayer时给它们一个姓名和年龄是有意义的，所以我们应该修改这个构造函数以添加这些参数。
这是我们更新后的使用私有成员的类，其中BaseballPlayer类调用适当的Person构造函数来初始化继承的Person成员变量。
#include <iostream>
#include <string>
#include <string_view>

class Person
{
private:
    std::string m_name;
    int m_age {};

public:
    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};
// BaseballPlayer publicly inheriting Person
class BaseballPlayer : public Person
{
private:
    double m_battingAverage {};
    int m_homeRuns {};

public:
    BaseballPlayer(std::string_view name = "", int age = 0,
        double battingAverage = 0.0, int homeRuns = 0)
        : Person{ name, age } // call Person(std::string_view, int) to initialize these fields
        , m_battingAverage{ battingAverage }, m_homeRuns{ homeRuns }
    {
    }

    double getBattingAverage() const { return m_battingAverage; }
    int getHomeRuns() const { return m_homeRuns; }
};
现在我们可以像这样创建棒球运动员：
#include <iostream>

int main()
{
    BaseballPlayer pedro{ "Pedro Cerrano", 32, 0.342, 42 };

    std::cout << pedro.getName() << '\n';
    std::cout << pedro.getAge() << '\n';
    std::cout << pedro.getBattingAverage() << '\n';
    std::cout << pedro.getHomeRuns() << '\n';

    return 0;
}
这输出
Pedro Cerrano
32
0.342
42
如您所见，基类中的姓名和年龄都得到了正确的初始化，派生类中的本垒打数量和打击平均值也得到了正确的初始化。
继承链
继承链中的类以完全相同的方式工作。
#include <iostream>

class A
{
public:
    A(int a)
    {
        std::cout << "A: " << a << '\n';
    }
};

class B: public A
{
public:
    B(int a, double b)
    : A{ a }
    {
        std::cout << "B: " << b << '\n';
    }
};

class C: public B
{
public:
    C(int a, double b, char c)
    : B{ a, b }
    {
        std::cout << "C: " << c << '\n';
    }
};

int main()
{
    C c{ 5, 4.3, 'R' };

    return 0;
}
在此示例中，类 C 派生自类 B，类 B 派生自类 A。那么当我们实例化类 C 的对象时会发生什么？
首先，main() 调用 C(int, double, char)。C 构造函数调用 B(int, double)。B 构造函数调用 A(int)。由于 A 不继承自任何人，所以这是我们要构造的第一个类。A 被构造，打印值 5，并将控制权返回给 B。B 被构造，打印值 4.3，并将控制权返回给 C。C 被构造，打印值 'R'，并将控制权返回给 main()。然后我们就完成了！
因此，这个程序打印
A: 5
B: 4.3
C: R
值得一提的是，构造函数只能调用其直接父/基类的构造函数。因此，C构造函数不能直接调用或传递参数给A构造函数。C构造函数只能调用B构造函数（B构造函数负责调用A构造函数）。
析构函数
当派生类被销毁时，每个析构函数都按照构造的
相反
顺序被调用。在上面的例子中，当c被销毁时，C析构函数首先被调用，然后是B析构函数，然后是A析构函数。
警告
如果您的基类有虚函数，您的析构函数也应该是虚的，否则在某些情况下会导致未定义行为。我们在课程
25.4 -- 虚析构函数、虚赋值和覆盖虚化
中介绍了这种情况。
总结
在构造派生类时，派生类构造函数负责确定调用哪个基类构造函数。如果未指定基类构造函数，则将使用默认基类构造函数。在这种情况下，如果找不到（或无法默认创建）默认基类构造函数，编译器将显示错误。然后，类按从最基类到最派生的顺序构造。
至此，您已经对C++继承有了足够的了解，可以创建自己的继承类了！
测验时间！
让我们实现我们在继承介绍中讨论过的Fruit示例。创建一个包含两个私有成员的Fruit基类：一个名称（std::string）和一个颜色（std::string）。创建一个继承Fruit的Apple类。Apple应该有一个额外的私有成员：纤维（double）。创建一个也继承Fruit的Banana类。Banana没有额外的成员。
以下程序应该运行
#include <iostream>

int main()
{
	const Apple a{ "Red delicious", "red", 4.2 };
	std::cout << a << '\n';

	const Banana b{ "Cavendish", "yellow" };
	std::cout << b << '\n';

	return 0;
}
并打印以下内容：
Apple(Red delicious, red, 4.2)
Banana(Cavendish, yellow)
提示：因为 a 和 b 是 const，你需要注意你的 const。确保你的参数和函数适当的 const。
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Fruit
{
private:
	std::string m_name;
	std::string m_color;

public:
	Fruit(std::string_view name, std::string_view color)
		: m_name{ name }, m_color{ color }
	{
	}

	const std::string& getName() const { return m_name; }
	const std::string& getColor() const { return m_color; }

};

class Apple : public Fruit
{
private:
	double m_fiber;

public:
	Apple(std::string_view name, std::string_view color, double fiber)
		:Fruit{ name, color },
		m_fiber{ fiber }
	{
	}

	double getFiber() const { return m_fiber; }

};

std::ostream& operator<<(std::ostream& out, const Apple& a)
{
	out << "Apple(" << a.getName() << ", " << a.getColor() << ", " << a.getFiber() << ')';
	return out;
}

class Banana : public Fruit
{
public:
	Banana(std::string_view name, std::string_view color)
		:Fruit{ name, color }
	{
	}
};

std::ostream& operator<<(std::ostream& out, const Banana& b)
{
	out << "Banana(" << b.getName() << ", " << b.getColor() << ')';
	return out;
}

int main()
{
	const Apple a{ "Red delicious", "red", 4.2 };
	std::cout << a << '\n';

	const Banana b{ "Cavendish", "yellow" };
	std::cout << b << '\n';

	return 0;
}
下一课
24.5
继承和访问说明符
返回目录
上一课
24.3
派生类的构造顺序