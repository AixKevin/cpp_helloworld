# 27.5 — 异常、类和继承

27.5 — 异常、类和继承
Alex
2008年10月26日，太平洋时间上午9:52
2025年1月29日
异常和成员函数
到目前为止，在本教程中，您只看到异常在非成员函数中使用。然而，异常在成员函数中同样有用，在重载运算符中更是如此。考虑以下作为简单整数数组类一部分的重载 [] 运算符
int& IntArray::operator[](const int index)
{
    return m_data[index];
}
虽然只要索引是有效的数组索引，此函数就能很好地工作，但它严重缺乏一些良好的错误检查。我们可以添加一个断言语句来确保索引是有效的
int& IntArray::operator[](const int index)
{
    assert (index >= 0 && index < getLength());
    return m_data[index];
}
现在，如果用户传入无效索引，程序将导致断言错误。不幸的是，由于重载运算符对它们可以接受和返回的参数数量和类型有特定的要求，因此没有灵活性可以将错误代码或布尔值传递回调用方进行处理。然而，由于异常不改变函数的签名，因此它们可以在这里发挥巨大作用。这是一个例子
int& IntArray::operator[](const int index)
{
    if (index < 0 || index >= getLength())
        throw index;

    return m_data[index];
}
现在，如果用户传入无效索引，operator[] 将抛出一个 int 异常。
构造函数失败时
构造函数是类中异常非常有用的另一个领域。如果构造函数因某种原因必须失败（例如，用户传入了无效输入），只需抛出异常以指示对象创建失败。在这种情况下，对象的构造将被中止，并且所有类成员（在构造函数体执行之前已经创建和初始化）都将照常析构。
然而，类的析构函数永远不会被调用（因为对象从未完成构造）。由于析构函数从不执行，您不能依赖该析构函数来清理任何已经分配的资源。
这引出了一个问题，即如果我们在构造函数中分配了资源，然后构造函数完成之前发生异常，我们应该怎么办。我们如何确保我们已经分配的资源得到正确清理？一种方法是将任何可能失败的代码包装在 try 块中，使用相应的 catch 块捕获异常并进行任何必要的清理，然后重新抛出异常（我们将在第
27.6 课——重新抛出异常
中讨论这个主题）。然而，这会增加很多代码，并且很容易出错，特别是如果您的类分配了多个资源。
幸运的是，有一种更好的方法。利用即使构造函数失败，类成员也会被析构的事实，如果您在类成员内部（而不是在构造函数本身中）进行资源分配，那么这些成员在析构时可以自行清理。
这是一个例子
#include <iostream>

class Member
{
public:
	Member()
	{
		std::cerr << "Member allocated some resources\n";
	}

	~Member()
	{
		std::cerr << "Member cleaned up\n";
	}
};

class A
{
private:
	int m_x {};
	Member m_member;

public:
	A(int x) : m_x{x}
	{
		if (x <= 0)
			throw 1;
	}
	
	~A()
	{
		std::cerr << "~A\n"; // should not be called
	}
};


int main()
{
	try
	{
		A a{0};
	}
	catch (int)
	{
		std::cerr << "Oops\n";
	}

	return 0;
}
这会打印
Member allocated some resources
Member cleaned up
Oops
在上面的程序中，当类 A 抛出异常时，A 的所有成员都会被析构。m_member 的析构函数被调用，提供了清理其分配的任何资源的机会。
这是 RAII（在第
19.3 课——析构函数
中介绍）被如此推崇的部分原因——即使在特殊情况下，实现 RAII 的类也能自行清理。
然而，创建像 Member 这样的自定义类来管理资源分配效率不高。幸运的是，C++ 标准库提供了符合 RAII 的类来管理常见的资源类型，例如文件（std::fstream，在第
28.6 课——基本文件 I/O
中介绍）和动态内存（std::unique_ptr 和其他智能指针，在
22.1 — 智能指针和移动语义介绍
中介绍）。
例如，而不是这样：
class Foo
private:
    int* ptr; // Foo will handle allocation/deallocation
这样做
class Foo
private:
    std::unique_ptr<int> ptr; // std::unique_ptr will handle allocation/deallocation
在前一种情况下，如果 Foo 的构造函数在 ptr 分配其动态内存后失败，则 Foo 将负责清理，这可能具有挑战性。在后一种情况下，如果 Foo 的构造函数在 ptr 分配其动态内存后失败，则 ptr 的析构函数将执行并将该内存返回给系统。当资源处理委托给符合 RAII 的成员时，Foo 无需执行任何显式清理！
异常类
使用基本数据类型（如 int）作为异常类型的主要问题之一是它们本质上是模糊的。一个更大的问题是，当 try 块中有多个语句或函数调用时，异常的含义难以区分。
// Using the IntArray overloaded operator[] above

try
{
    int* value{ new int{ array[index1] + array[index2]} };
}
catch (int value)
{
    // What are we catching here?
}
在此示例中，如果我们捕获 int 异常，这到底告诉我们什么？是其中一个数组索引越界了吗？operator+ 导致整数溢出了吗？operator new 因为内存不足而失败了吗？不幸的是，在这种情况下，没有简单的方法来区分。虽然我们可以抛出 const char* 异常来解决识别“出了什么问题”的问题，但这仍然无法为我们提供以不同方式处理来自不同来源的异常的能力。
解决此问题的一种方法是使用异常类。**异常类**只是一个普通的类，专门设计用于作为异常抛出。让我们设计一个简单的异常类，与我们的 IntArray 类一起使用
#include <string>
#include <string_view>

class ArrayException
{
private:
	std::string m_error;

public:
	ArrayException(std::string_view error)
		: m_error{ error }
	{
	}

	const std::string& getError() const { return m_error; }
};
这是一个使用此类的完整程序
#include <iostream>
#include <string>
#include <string_view>

class ArrayException
{
private:
	std::string m_error;

public:
	ArrayException(std::string_view error)
		: m_error{ error }
	{
	}

	const std::string& getError() const { return m_error; }
};

class IntArray
{
private:
	int m_data[3]{}; // assume array is length 3 for simplicity

public:
	IntArray() {}

	int getLength() const { return 3; }

	int& operator[](const int index)
	{
		if (index < 0 || index >= getLength())
			throw ArrayException{ "Invalid index" };

		return m_data[index];
	}

};

int main()
{
	IntArray array;

	try
	{
		int value{ array[5] }; // out of range subscript
	}
	catch (const ArrayException& exception)
	{
		std::cerr << "An array exception occurred (" << exception.getError() << ")\n";
	}
}
使用这样的类，我们可以让异常返回所发生问题的描述，这提供了错误发生的上下文。而且由于 ArrayException 是其自己的独特类型，如果需要，我们可以专门捕获由数组类抛出的异常，并将其与其他异常区别对待。
请注意，异常处理程序应通过引用而不是值捕获类异常对象。这可以防止编译器在捕获点复制异常，当异常是类对象时，这可能开销很大，并且在处理派生异常类时防止对象切片（我们稍后会讨论）。除非您有特定原因，否则通常应避免通过指针捕获异常。
最佳实践
基本类型的异常可以通过值捕获，因为它们复制成本低。
类类型的异常应该通过（const）引用捕获，以防止昂贵的复制和切片。
异常与继承
由于可以将类作为异常抛出，并且类可以从其他类派生，因此我们需要考虑当我们将继承的类用作异常时会发生什么。事实证明，异常处理程序不仅会匹配特定类型的类，它们还会匹配从该特定类型派生的类！考虑以下示例
#include <iostream>

class Base
{
public:
    Base() {}
};

class Derived: public Base
{
public:
    Derived() {}
};

int main()
{
    try
    {
        throw Derived();
    }
    catch (const Base& base)
    {
        std::cerr << "caught Base";
    }
    catch (const Derived& derived)
    {
        std::cerr << "caught Derived";
    }

    return 0;
}
在上面的示例中，我们抛出一个 Derived 类型的异常。然而，该程序的输出是
caught Base
发生了什么？
首先，如上所述，派生类将被基类型的处理程序捕获。因为 Derived 是从 Base 派生的，所以 Derived 是一个 Base（它们之间存在“is-a”关系）。其次，当 C++ 试图为抛出的异常查找处理程序时，它会按顺序进行。因此，C++ 所做的第一件事是检查 Base 的异常处理程序是否与 Derived 异常匹配。因为 Derived 是一个 Base，所以答案是肯定的，并且它执行 Base 类型的 catch 块！在这种情况下，甚至没有测试 Derived 的 catch 块。
为了使这个例子按预期工作，我们需要翻转 catch 块的顺序
#include <iostream>

class Base
{
public:
    Base() {}
};

class Derived: public Base
{
public:
    Derived() {}
};

int main()
{
    try
    {
        throw Derived();
    }
    catch (const Derived& derived)
    {
        std::cerr << "caught Derived";
    }
    catch (const Base& base)
    {
        std::cerr << "caught Base";
    }

    return 0;
}
这样，Derived 处理程序将首先尝试捕获 Derived 类型的对象（在 Base 的处理程序之前）。Base 类型的对象将不匹配 Derived 处理程序（Derived 是 Base，但 Base 不是 Derived），因此将“落空”到 Base 处理程序。
规则
派生异常类的处理程序应在基类处理程序之前列出。
使用基类的处理程序捕获派生类型异常的能力非常有用。
std::exception
标准库中的许多类和运算符在失败时会抛出异常类。例如，如果无法分配足够的内存，operator new 会抛出 std::bad_alloc。失败的 dynamic_cast 会抛出 std::bad_cast。依此类推。截至 C++20，可以抛出 28 种不同的异常类，每个后续语言标准中还会添加更多。
好消息是所有这些异常类都派生自一个名为 **std::exception** 的类（在 <exception> 头文件中定义）。std::exception 是一个小型接口类，旨在作为 C++ 标准库抛出的任何异常的基类。
很多时候，当标准库抛出异常时，我们不会关心它是坏分配、坏转换还是其他什么。我们只关心发生了灾难性的错误，现在我们的程序正在崩溃。多亏了 std::exception，我们可以设置一个异常处理程序来捕获 std::exception 类型的异常，最终我们将会在一个地方捕获 std::exception 和所有派生异常。很简单！
#include <cstddef> // for std::size_t
#include <exception> // for std::exception
#include <iostream>
#include <limits>
#include <string> // for this example

int main()
{
    try
    {
        // Your code using standard library goes here
        // We'll trigger one of these exceptions intentionally for the sake of the example
        std::string s;
        s.resize(std::numeric_limits<std::size_t>::max()); // will trigger a std::length_error or allocation exception
    }
    // This handler will catch std::exception and all the derived exceptions too
    catch (const std::exception& exception)
    {
        std::cerr << "Standard exception: " << exception.what() << '\n';
    }

    return 0;
}
在作者的机器上，上面的程序打印
Standard exception: string too long
上面的例子应该非常简单。值得注意的是，std::exception 有一个名为 **what()** 的虚成员函数，它返回异常的 C 风格字符串描述。大多数派生类都会覆盖 what() 函数来更改消息。请注意，此字符串仅用于描述性文本——不要将其用于比较，因为它不保证在不同编译器之间相同。
有时我们会希望以不同方式处理特定类型的异常。在这种情况下，我们可以为该特定类型添加一个处理程序，让所有其他异常“落空”到基本处理程序。考虑
try
{
     // code using standard library goes here
}
// This handler will catch std::length_error (and any exceptions derived from it) here
catch (const std::length_error& exception)
{
    std::cerr << "You ran out of memory!" << '\n';
}
// This handler will catch std::exception (and any exception derived from it) that fall
// through here
catch (const std::exception& exception)
{
    std::cerr << "Standard exception: " << exception.what() << '\n';
}
在此示例中，std::length_error 类型的异常将被第一个处理程序捕获并在那里处理。std::exception 类型的所有其他派生类的异常将被第二个处理程序捕获。
这种继承层次结构允许我们使用特定的处理程序来定位特定的派生异常类，或者使用基类处理程序来捕获整个异常层次结构。这使得我们能够精确控制要处理的异常类型，同时确保我们无需做太多工作即可捕获层次结构中的“所有其他”异常。
直接使用标准异常
没有人直接抛出 std::exception，您也不应该这样做。但是，如果标准库中的其他标准异常类能够充分满足您的需求，您可以随意抛出它们。您可以在
cppreference
上找到所有标准异常的列表。
std::runtime_error（作为 stdexcept 头文件的一部分）是一个流行的选择，因为它有一个通用的名称，并且其构造函数接受可自定义的消息
#include <exception> // for std::exception
#include <iostream>
#include <stdexcept> // for std::runtime_error

int main()
{
	try
	{
		throw std::runtime_error("Bad things happened");
	}
	// This handler will catch std::exception and all the derived exceptions too
	catch (const std::exception& exception)
	{
		std::cerr << "Standard exception: " << exception.what() << '\n';
	}

	return 0;
}
这会打印
Standard exception: Bad things happened
从 std::exception 或 std::runtime_error 派生自己的类
当然，您可以从 std::exception 派生自己的类，并覆盖虚函数 what() const。下面是与上面相同的程序，ArrayException 派生自 std::exception
#include <exception> // for std::exception
#include <iostream>
#include <string>
#include <string_view>

class ArrayException : public std::exception
{
private:
	std::string m_error{}; // handle our own string

public:
	ArrayException(std::string_view error)
		: m_error{error}
	{
	}

	// std::exception::what() returns a const char*, so we must as well
	const char* what() const noexcept override { return m_error.c_str(); }
};

class IntArray
{
private:
	int m_data[3] {}; // assume array is length 3 for simplicity

public:
	IntArray() {}
	
	int getLength() const { return 3; }

	int& operator[](const int index)
	{
		if (index < 0 || index >= getLength())
			throw ArrayException("Invalid index");

		return m_data[index];
	}

};

int main()
{
	IntArray array;

	try
	{
		int value{ array[5] };
	}
	catch (const ArrayException& exception) // derived catch blocks go first
	{
		std::cerr << "An array exception occurred (" << exception.what() << ")\n";
	}
	catch (const std::exception& exception)
	{
		std::cerr << "Some other std::exception occurred (" << exception.what() << ")\n";
	}
}
请注意，虚函数 what() 具有 noexcept 说明符（这意味着该函数承诺自身不会抛出异常）。因此，我们的覆盖也应该具有 noexcept 说明符。
因为 std::runtime_error 已经具有字符串处理能力，所以它也是派生异常类的常用基类。std::runtime_error 可以接受 C 风格的字符串参数，或者 `const std::string&` 参数。
下面是从 std::runtime_error 派生的相同示例
#include <exception> // for std::exception
#include <iostream>
#include <stdexcept> // for std::runtime_error
#include <string>

class ArrayException : public std::runtime_error
{
public:
	// std::runtime_error takes either a null-terminated const char* or a const std::string&.
	// We will follow their lead and take a const std::string&
	ArrayException(const std::string& error)
		: std::runtime_error{ error } // std::runtime_error will handle the string
	{
	}


        // no need to override what() since we can just use std::runtime_error::what()
};

class IntArray
{
private:
	int m_data[3]{}; // assume array is length 3 for simplicity

public:
	IntArray() {}

	int getLength() const { return 3; }

	int& operator[](const int index)
	{
		if (index < 0 || index >= getLength())
			throw ArrayException("Invalid index");

		return m_data[index];
	}

};

int main()
{
	IntArray array;

	try
	{
		int value{ array[5] };
	}
	catch (const ArrayException& exception) // derived catch blocks go first
	{
		std::cerr << "An array exception occurred (" << exception.what() << ")\n";
	}
	catch (const std::exception& exception)
	{
		std::cerr << "Some other std::exception occurred (" << exception.what() << ")\n";
	}
}
您是想创建自己的独立异常类，使用标准异常类，还是从 std::exception 或 std::runtime_error 派生自己的异常类，这取决于您。所有这些都是根据您的目标而有效的方法。
异常的生命周期
当抛出异常时，被抛出的对象通常是分配在栈上的临时变量或局部变量。然而，异常处理过程可能会展开函数，导致函数的所有局部变量被销毁。那么，被抛出的异常对象是如何在栈展开过程中存活下来的呢？
当抛出异常时，编译器会将异常对象复制到为处理异常而保留的某些未指定内存（调用栈之外）。这样，无论栈是否或展开多少次，异常对象都会持久存在。异常保证存在，直到异常被处理。
这意味着被抛出的对象通常需要是可复制的（即使栈实际上没有展开）。智能编译器可能能够执行移动操作，或者在特定情况下完全省略复制。
提示
异常对象需要是可复制的。
这是一个示例，展示当我们尝试抛出一个不可复制的 Derived 对象时会发生什么
#include <iostream>

class Base
{
public:
    Base() {}
};

class Derived : public Base
{
public:
    Derived() {}

    Derived(const Derived&) = delete; // not copyable
};

int main()
{
    Derived d{};

    try
    {
        throw d; // compile error: Derived copy constructor was deleted
    }
    catch (const Derived& derived)
    {
        std::cerr << "caught Derived";
    }
    catch (const Base& base)
    {
        std::cerr << "caught Base";
    }

    return 0;
}
编译此程序时，编译器会抱怨 Derived 复制构造函数不可用，并停止编译。
异常对象不应保留指向栈分配对象的指针或引用。如果抛出的异常导致栈展开（导致栈分配对象的销毁），这些指针或引用可能会悬空。
下一课
27.6
重新抛出异常
返回目录
上一课
27.4
未捕获异常和万能捕获处理程序