# 15.3 — 嵌套类型（成员类型）

15.3 — 嵌套类型（成员类型）
Alex
2016 年 12 月 21 日，太平洋标准时间上午 10:57
2025 年 2 月 27 日
考虑以下简短程序
#include <iostream>

enum class FruitType
{
	apple,
	banana,
	cherry
};

class Fruit
{
private:
	FruitType m_type { };
	int m_percentageEaten { 0 };

public:
	Fruit(FruitType type) :
		m_type { type }
	{
	}

	FruitType getType() { return m_type; }
	int getPercentageEaten() { return m_percentageEaten; }

	bool isCherry() { return m_type == FruitType::cherry; }

};

int main()
{
	Fruit apple { FruitType::apple };
	
	if (apple.getType() == FruitType::apple)
		std::cout << "I am an apple";
	else
		std::cout << "I am not an apple";
	
	return 0;
}
这个程序没有任何问题。但是，因为
enum class FruitType
旨在与
Fruit
类结合使用，所以让它独立于类存在，使我们不得不推断它们是如何连接的。
嵌套类型（成员类型）
到目前为止，我们已经看到了具有两种不同成员的类类型：数据成员和成员函数。上面示例中的
Fruit
类同时拥有这两种成员。
类类型支持另一种成员：**嵌套类型**（也称为**成员类型**）。要创建嵌套类型，只需在类内部，在适当的访问说明符下定义类型即可。
这是与上面相同的程序，但已重写为使用在
Fruit
类内部定义的嵌套类型
#include <iostream>

class Fruit
{
public:
	// FruitType has been moved inside the class, under the public access specifier
        // We've also renamed it Type and made it an enum rather than an enum class
	enum Type
	{
		apple,
		banana,
		cherry
	};

private:
	Type m_type {};
	int m_percentageEaten { 0 };

public:
	Fruit(Type type) :
		m_type { type }
	{
	}

	Type getType() { return m_type;  }
	int getPercentageEaten() { return m_percentageEaten;  }

	bool isCherry() { return m_type == cherry; } // Inside members of Fruit, we no longer need to prefix enumerators with FruitType::
};

int main()
{
	// Note: Outside the class, we access the enumerators via the Fruit:: prefix now
	Fruit apple { Fruit::apple };
	
	if (apple.getType() == Fruit::apple)
		std::cout << "I am an apple";
	else
		std::cout << "I am not an apple";
	
	return 0;
}
这里有几点值得指出。
首先，请注意
FruitType
现在在类内部定义，并已更名为
Type
，原因我们稍后会讨论。
其次，嵌套类型
Type
已在类的顶部定义。嵌套类型名称必须在使用之前完全定义，因此它们通常首先定义。
最佳实践
在类类型的顶部定义任何嵌套类型。
第三，嵌套类型遵循正常的访问规则。
Type
定义在
public
访问说明符下，因此类型名称和枚举器可以被公共直接访问。
第四，类类型充当其内部声明的名称的作用域区域，就像命名空间一样。因此，
Type
的完全限定名是
Fruit::Type
，而
apple
枚举器的完全限定名是
Fruit::apple
。
在类的成员中，我们不需要使用完全限定名。例如，在成员函数
isCherry()
中，我们访问
cherry
枚举器时没有使用
Fruit::
作用域限定符。
在类外部，我们必须使用完全限定名（例如
Fruit::apple
）。我们将
FruitType
重命名为
Type
，以便我们可以将其作为
Fruit::Type
访问（而不是更冗余的
Fruit::FruitType
）。
最后，我们把枚举类型从有作用域的改成了无作用域的。因为类本身现在充当一个作用域区域，所以再使用一个有作用域的枚举器会有点冗余。改成无作用域的枚举意味着我们可以将枚举器作为
Fruit::apple
访问，而不是如果我们使用有作用域的枚举器就必须使用的更长的
Fruit::Type::apple
。
嵌套 typedefs 和类型别名
类类型也可以包含嵌套的 typedefs 或类型别名
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
public:
    using IDType = int;

private:
    std::string m_name{};
    IDType m_id{};
    double m_wage{};

public:
    Employee(std::string_view name, IDType id, double wage)
        : m_name { name }
        , m_id { id }
        , m_wage { wage }
    {
    }

    const std::string& getName() { return m_name; }
    IDType getId() { return m_id; } // can use unqualified name within class
};

int main()
{
    Employee john { "John", 1, 45000 };
    Employee::IDType id { john.getId() }; // must use fully qualified name outside class

    std::cout << john.getName() << " has id: " << id << '\n';

    return 0;
}
这会打印
John has id: 1
请注意，在类内部我们可以直接使用
IDType
，但在类外部我们必须使用完全限定名
Employee::IDType
。
我们在课程
10.7 -- Typedefs and type aliases
中讨论了类型别名的好处，它们在这里也起到同样的作用。C++ 标准库中的类非常普遍地使用嵌套的 typedefs。截至撰写本文时，
std::string
定义了十个嵌套的 typedefs！
嵌套类和对外层类成员的访问
类拥有其他类作为嵌套类型的情况相当不常见，但这是可能的。在 C++ 中，嵌套类无法访问外层（包含）类的
this
指针，因此嵌套类无法直接访问外层类的成员。这是因为嵌套类可以独立于外层类实例化（在这种情况下，就没有外层类成员可以访问了！）
然而，由于嵌套类是外层类的成员，它们可以访问外层类作用域内的任何私有成员。
让我们用一个例子来说明
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
public:
    using IDType = int;

    class Printer
    {
    public:
        void print(const Employee& e) const
        {
            // Printer can't access Employee's `this` pointer
            // so we can't print m_name and m_id directly
            // Instead, we have to pass in an Employee object to use
            // Because Printer is a member of Employee,
            // we can access private members e.m_name and e.m_id directly
            std::cout << e.m_name << " has id: " << e.m_id << '\n';
        }
    };

private:
    std::string m_name{};
    IDType m_id{};
    double m_wage{};

public:
    Employee(std::string_view name, IDType id, double wage)
        : m_name{ name }
        , m_id{ id }
        , m_wage{ wage }
    {
    }

    // removed the access functions in this example (since they aren't used)
};

int main()
{
    const Employee john{ "John", 1, 45000 };
    const Employee::Printer p{}; // instantiate an object of the inner class
    p.print(john);

    return 0;
}
这会打印
John has id: 1
有一种情况下，嵌套类更常用。在标准库中，大多数迭代器类都被实现为它们旨在迭代的容器的嵌套类。例如，
std::string::iterator
被实现为
std::string
的嵌套类。我们将在未来的章节中介绍迭代器。
嵌套类型和前向声明
嵌套类型可以在其包含类中进行前向声明。然后，嵌套类型可以在包含类内部或外部定义。例如
#include <iostream>

class outer
{
public:
    class inner1;   // okay: forward declaration inside the enclosing class okay
    class inner1{}; // okay: definition of forward declared type inside the enclosing class
    class inner2;   // okay: forward declaration inside the enclosing class okay
};

class inner2 // okay: definition of forward declared type outside the enclosing class
{
};

int main()
{
    return 0;
}
然而，嵌套类型不能在包含类定义之前进行前向声明。
#include <iostream>

class outer;         // okay: can forward declare non-nested type
class outer::inner1; // error: can't forward declare nested type prior to outer class definition

class outer
{
public:
    class inner1{}; // note: nested type declared here
};

class outer::inner1; // okay (but redundant) since nested type has already been declared as part of outer class definition

int main()
{
    return 0;
}
虽然您可以在包含类定义之后前向声明嵌套类型，但由于包含类已经包含了嵌套类型的声明，这样做是多余的。
下一课
15.4
析构函数简介
返回目录
上一课
15.2
类和头文件