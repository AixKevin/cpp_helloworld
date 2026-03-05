# 14.12 — 委托构造函数

14.12 — 委托构造函数
Alex
2007 年 9 月 7 日，上午 9:22 PDT
2025 年 1 月 21 日
只要有可能，我们都希望减少冗余代码（遵循 DRY 原则——不要重复自己）。
考虑以下函数
void A()
{
    // statements that do task A
}

void B()
{
    // statements that do task A
    // statements that do task B
}
这两个函数都有一组执行完全相同操作（任务 A）的语句。在这种情况下，我们可以这样重构
void A()
{
    // statements that do task A
}

void B()
{
    A();
    // statements that do task B
}
通过这种方式，我们删除了函数
A()
和
B()
中存在的冗余代码。这使得我们的代码更容易维护，因为只需在一个地方进行更改。
当一个类包含多个构造函数时，如果每个构造函数中的代码不完全相同，也通常会非常相似，存在大量重复。我们同样希望在可能的情况下消除构造函数的冗余。
考虑以下示例
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id { 0 };
    bool m_isManager { false };

public:
    Employee(std::string_view name, int id) // Employees must have a name and an id
        : m_name{ name }, m_id { id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }

    Employee(std::string_view name, int id, bool isManager) // They can optionally be a manager
        : m_name{ name }, m_id{ id }, m_isManager { isManager }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James", 7 };
    Employee e2{ "Dave", 42, true };
}
每个构造函数的主体都有完全相同的打印语句。
作者注
通常不建议让构造函数打印内容（除非用于调试），因为这意味着在不希望打印内容的情况下，您无法使用该构造函数创建对象。在此示例中我们这样做是为了帮助说明正在发生的事情。
构造函数允许调用其他函数，包括类的其他成员函数。所以我们可以这样重构
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id{ 0 };
    bool m_isManager { false };

    void printCreated() const // our new helper function
    {
        std::cout << "Employee " << m_name << " created\n";
    }

public:
    Employee(std::string_view name, int id)
        : m_name{ name }, m_id { id }
    {
        printCreated(); // we call it here
    }

    Employee(std::string_view name, int id, bool isManager)
        : m_name{ name }, m_id{ id }, m_isManager { isManager }
    {
        printCreated(); // and here
    }
};

int main()
{
    Employee e1{ "James", 7 };
    Employee e2{ "Dave", 42, true };
}
虽然这比之前的版本要好（因为冗余语句已被冗余函数调用替换），但它需要引入一个新函数。而且我们的两个构造函数都在初始化
m_name
和
m_id
。理想情况下，我们也应该消除这种冗余。
我们可以做得更好吗？可以。但这正是许多新程序员遇到麻烦的地方。
在函数体中调用构造函数会创建临时对象
类似于我们在上面的示例中让函数
B()
调用函数
A()
，显而易见的解决方案似乎是从
Employee(std::string_view, int, bool)
的主体中调用
Employee(std::string_view, int)
构造函数，以便初始化
m_name
、
m_id
并打印语句。以下是它的样子
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id { 0 };
    bool m_isManager { false };

public:
    Employee(std::string_view name, int id)
        : m_name{ name }, m_id { id } // this constructor initializes name and id
    {
        std::cout << "Employee " << m_name << " created\n"; // our print statement is back here
    }

    Employee(std::string_view name, int id, bool isManager)
        : m_isManager { isManager } // this constructor initializes m_isManager
    {
        // Call Employee(std::string_view, int) to initialize m_name and m_id
        Employee(name, id); // this doesn't work as expected!
    }

    const std::string& getName() const { return m_name; }
};

int main()
{
    Employee e2{ "Dave", 42, true };
    std::cout << "e2 has name: " << e2.getName() << "\n"; // print e2.m_name
}
但这无法正常工作，因为程序输出以下内容
Employee Dave created
e2 has name: ???
尽管打印了
Employee Dave created
，但在
e2
完成构造后，
e2.m_name
似乎仍设置为其初始值
"???"
。这怎么可能？
我们期望
Employee(name, id)
调用构造函数以继续初始化当前的隐式对象 (
e2
)。但是，一旦成员初始化列表执行完毕，类对象的初始化就完成了。当我们开始执行构造函数的主体时，再进行更多初始化就为时已晚。
当从函数体中调用时，看起来像对构造函数的函数调用通常会创建并直接初始化一个临时对象（在另一种情况下，您会得到编译错误）。在上面的示例中，
Employee(name, id);
创建了一个临时的（未命名）Employee 对象。这个临时对象是其
m_name
设置为
Dave
的对象，并且是打印
Employee Dave created
的对象。然后临时对象被销毁。
e2
的
m_name
或
m_id
从未从默认值更改。
最佳实践
构造函数不应直接从另一个函数的主体中调用。这样做会导致编译错误，或者会直接初始化一个临时对象。
如果您确实想要一个临时对象，请优先使用列表初始化（这清楚地表明您打算创建一个对象）。
那么，如果我们不能从一个构造函数的主体中调用另一个构造函数，那么如何解决这个问题呢？
委托构造函数
构造函数允许将初始化委托（转移责任）给同一类的另一个构造函数。这个过程有时称为
构造函数链
，这样的构造函数称为
委托构造函数
。
要使一个构造函数将初始化委托给另一个构造函数，只需在成员初始化列表中调用该构造函数即可
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id { 0 };

public:
    Employee(std::string_view name)
        : Employee{ name, 0 } // delegate initialization to Employee(std::string_view, int) constructor
    {
    }

    Employee(std::string_view name, int id)
        : m_name{ name }, m_id { id } // actually initializes the members
    {
        std::cout << "Employee " << m_name << " created\n";
    }

};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
当
e1 { "James" }
初始化时，将调用匹配的构造函数
Employee(std::string_view)
，参数
name
设置为
"James"
。此构造函数的成员初始化列表将初始化委托给另一个构造函数，因此将调用
Employee(std::string_view, int)
。
name
的值（
"James"
）作为第一个参数传递，字面值
0
作为第二个参数传递。然后委托构造函数的成员初始化列表初始化成员。然后运行委托构造函数的主体。然后控制返回到初始构造函数，其（空）主体运行。最后，控制返回到调用者。
这种方法的缺点是它有时需要重复初始化值。在委托给 `Employee(std::string_view, int)` 构造函数时，我们需要一个 `int` 参数的初始化值。我们不得不硬编码字面值 `0`，因为没有办法引用默认成员初始化器。
关于委托构造函数的一些额外说明。首先，委托给另一个构造函数的构造函数不允许自己进行任何成员初始化。因此，您的构造函数可以委托或初始化，但不能两者兼而有之。
题外话…
请注意，我们让
Employee(std::string_view)
（参数较少的构造函数）委托给
Employee(std::string_view name, int id)
（参数较多的构造函数）。让参数较少的构造函数委托给参数较多的构造函数是很常见的。
如果我们选择让
Employee(std::string_view name, int id)
委托给
Employee(std::string_view)
，那么我们将无法使用
id
初始化
m_id
，因为构造函数只能委托或初始化，不能两者兼顾。
其次，一个构造函数可能会委托给另一个构造函数，而后者又委托回第一个构造函数。这会形成一个无限循环，并导致您的程序耗尽栈空间并崩溃。您可以通过确保所有构造函数都解析为非委托构造函数来避免这种情况。
最佳实践
如果您有多个构造函数，请考虑是否可以使用委托构造函数来减少重复代码。
使用默认实参减少构造函数
默认值有时也可以用于将多个构造函数减少为更少的构造函数。例如，通过在我们的
id
参数上放置一个默认值，我们可以创建一个需要名称参数但可选接受 id 参数的单个
Employee
构造函数
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 }; // default member initializer

public:

    Employee(std::string_view name, int id = 0) // default argument for id
        : m_name{ name }, m_id{ id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
由于默认值必须附加到函数调用中最右边的参数，因此在定义类时，一个好的做法是首先定义用户**必须**提供初始化值的成员（然后将它们作为构造函数的最左边参数）。用户可以可选提供的成员（因为默认值可接受）应该其次定义（然后将它们作为构造函数的最右边参数）。
最佳实践
用户必须提供初始化值的成员应该首先定义（并作为构造函数的最左边参数）。用户可以可选提供初始化值的成员（因为默认值是可接受的）应该其次定义（并作为构造函数的最右边参数）。
请注意，此方法还需要重复
m_id
的默认初始化值（'0'）：一次作为默认成员初始化器，一次作为默认实参。
一个难题：冗余构造函数与冗余默认值
在上面的示例中，我们使用委托构造函数和默认实参来减少构造函数冗余。但是这两种方法都要求我们在不同位置重复成员的初始化值。不幸的是，目前无法指定委托构造函数或默认实参应使用默认成员初始化器值。
关于是拥有更少的构造函数（带有初始化值重复）还是更多的构造函数（没有初始化值重复）有各种意见。我们的意见是，拥有更少的构造函数通常更直接，即使它会导致初始化值的重复。
致进阶读者
当我们有一个在多个地方使用的初始化值（例如，作为默认成员初始化器和构造函数参数的默认实参）时，我们可以定义一个命名常量并在需要初始化值的任何地方使用它。这允许在同一个地方定义初始化值。
虽然你可以为此使用 constexpr 全局变量，但更好的选择是在类内部使用 `static constexpr` 成员
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    static constexpr int default_id { 0 }; // define a named constant with our desired initialization value
    
    std::string m_name {};
    int m_id { default_id }; // we can use it here

public:

    Employee(std::string_view name, int id = default_id) // and we can use it here
        : m_name { name }, m_id { id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1 { "James" };
    Employee e2 { "Dave", 42 };
}
在此上下文中使用
static
关键字允许我们拥有一个由所有
Employee
对象共享的单个
default_id
成员。如果没有
static
，每个
Employee
对象都将拥有自己独立的
default_id
成员（这会起作用，但会浪费内存）。
这种方法的缺点是，每个额外的命名常量都会增加一个必须理解的名称，使您的类稍微更混乱和复杂。这是否值得取决于需要多少这样的常量，以及在多少地方需要初始化值。
我们在
15.6 -- 静态成员变量
课程中涵盖了静态数据成员。
小测验时间
问题 #1
编写一个名为 Ball 的类。Ball 应该有两个私有成员变量，一个用于存储颜色（默认值：
black
），一个用于存储半径（默认值：
10.0
）。添加 4 个构造函数，每个构造函数处理以下每种情况
int main()
{
    Ball def{};
    Ball blue{ "blue" };
    Ball twenty{ 20.0 };
    Ball blueTwenty{ "blue", 20.0 };

    return 0;
}
程序应该产生以下结果
Ball(black, 10)
Ball(blue, 10)
Ball(black, 20)
Ball(blue, 20)
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Ball
{
private:
	std::string m_color{ "black" };
	double m_radius{ 10.0 };

public:
	// Default constructor (color and radius will use default value)
	Ball()
	{
            print();
	}

	// Constructor with only radius parameter (color will use default value)
	Ball(double radius)
		: m_radius{ radius }
	{
            print();
	}

	// Constructor with only color parameter (radius will use default value)
	Ball(std::string_view color)
		: m_color{ color }
	{
            print();
	}

	// Constructor with both color and radius parameters
	Ball(std::string_view color, double radius)
		: m_color{ color }
		, m_radius{ radius }
	{
            print();
	}

    void print() const
    {
        std::cout << "Ball(" << m_color << ", " << m_radius << ")\n";
    }
};

int main()
{
    Ball def{};
    Ball blue{ "blue" };
    Ball twenty{ 20.0 };
    Ball blueTwenty{ "blue", 20.0 };

    return 0;
}
问题 #2
通过使用默认参数和委托构造函数来减少上述程序中的构造函数数量。
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Ball
{
private:
	std::string m_color{ "black" };
	double m_radius{ 10.0 };

public:
	// Handles Ball(radius)
	Ball(double radius)
		: Ball{ "black", radius } // delegate to the other constructor
	{
		// We don't need to call print() here since it will be called by
		// the constructor we delegate to		
	}

	// Handles Ball(color, radius), Ball(color), and Ball()
	Ball(std::string_view color="black", double radius=10.0)
		: m_color{ color }
		, m_radius{ radius }
	{
		print();
	}

	void print() const
	{
		std::cout << "Ball(" << m_color << ", " << m_radius << ")\n";
	}
};

int main()
{
    Ball def{};
    Ball blue{ "blue" };
    Ball twenty{ 20.0 };
    Ball blueTwenty{ "blue", 20.0 };

    return 0;
}
下一课
14.13
临时类对象
返回目录
上一课
14.11
默认构造函数和默认实参