# 24.8 — 隐藏继承的功能

24.8 — 隐藏继承的功能
Alex
2017 年 6 月 27 日，下午 4:24 PDT
2024 年 7 月 17 日
更改继承成员的访问级别
C++ 允许我们更改派生类中继承成员的访问修饰符。这是通过使用 *using 声明* 来实现的，该声明在新访问修饰符下标识在派生类中更改其访问权限的（作用域）基类成员。
例如，考虑以下基类
#include <iostream>

class Base
{
private:
    int m_value {};

public:
    Base(int value)
        : m_value { value }
    {
    }

protected:
    void printValue() const { std::cout << m_value; }
};
因为 Base::printValue() 已声明为 protected，所以它只能由 Base 或其派生类调用。公共不能访问它。
让我们定义一个派生类，将 printValue() 的访问修饰符更改为 public
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }

    // Base::printValue was inherited as protected, so the public has no access
    // But we're changing it to public via a using declaration
    using Base::printValue; // note: no parenthesis here
};
这意味着这段代码现在可以工作了
int main()
{
    Derived derived { 7 };

    // printValue is public in Derived, so this is okay
    derived.printValue(); // prints 7
    return 0;
}
您只能更改派生类通常可以访问的基类成员的访问修饰符。因此，您永远不能将基类成员的访问修饰符从 private 更改为 protected 或 public，因为派生类无权访问基类的 private 成员。
隐藏功能
在 C++ 中，除了修改源代码之外，无法从基类中删除或限制功能。但是，在派生类中，可以隐藏基类中存在的功能，使其无法通过派生类访问。这可以通过简单地更改相关访问修饰符来实现。
例如，我们可以将公共成员设为私有
#include <iostream>

class Base
{
public:
	int m_value{};
};

class Derived : public Base
{
private:
	using Base::m_value;

public:
	Derived(int value) : Base { value }
	{
	}
};

int main()
{
	Derived derived{ 7 };
	std::cout << derived.m_value; // error: m_value is private in Derived

	Base& base{ derived };
	std::cout << base.m_value; // okay: m_value is public in Base

	return 0;
}
这使我们能够使用设计不佳的基类，并将其数据封装在我们的派生类中。或者，除了公开继承 Base 的成员并通过覆盖其访问修饰符使 m_value 成为私有之外，我们还可以私有继承 Base，这会首先导致 Base 的所有成员都私有继承。
但是，值得注意的是，虽然 m_value 在 Derived 类中是私有的，但它在 Base 类中仍然是公共的。因此，可以通过强制转换为 Base& 并直接访问成员来规避 Derived 中 m_value 的封装。
致进阶读者
出于同样的原因，如果一个基类有一个公共的虚函数，并且派生类将访问修饰符更改为私有，那么公共仍然可以通过将派生对象强制转换为 Base& 并调用虚函数来访问私有派生函数。编译器将允许这样做，因为该函数在 Base 中是公共的。但是，由于该对象实际上是一个 Derived，因此虚函数解析将解析为（并调用）（私有）Derived 版本的函数。访问控制在运行时不强制执行。
#include <iostream>

class A
{
public:
    virtual void fun()
    {
        std::cout << "public A::fun()\n";
    }
};

class B : public A
{
private:
    virtual void fun()
    {
         std::cout << "private B::fun()\n";
   }
};

int main()
{
    B b {};
    b.fun();                  // compile error: not allowed as B::fun() is private
    static_cast<A&>(b).fun(); // okay: A::fun() is public, resolves to private B::fun() at runtime

    return 0;
}
也许令人惊讶的是，给定基类中的一组重载函数，无法更改单个重载的访问修饰符。您只能更改所有重载
#include <iostream>

class Base
{
public:
    int m_value{};

    int getValue() const { return m_value; }
    int getValue(int) const { return m_value; }
};

class Derived : public Base
{
private:
	using Base::getValue; // make ALL getValue functions private

public:
	Derived(int value) : Base { value }
	{
	}
};

int main()
{
	Derived derived{ 7 };
	std::cout << derived.getValue();  // error: getValue() is private in Derived
	std::cout << derived.getValue(5); // error: getValue(int) is private in Derived

	return 0;
}
删除派生类中的函数
您还可以将成员函数标记为在派生类中已删除，这确保它们根本不能通过派生对象调用
#include <iostream>
class Base
{
private:
	int m_value {};

public:
	Base(int value)
		: m_value { value }
	{
	}

	int getValue() const { return m_value; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base { value }
	{
	}


	int getValue() const = delete; // mark this function as inaccessible
};

int main()
{
	Derived derived { 7 };

	// The following won't work because getValue() has been deleted!
	std::cout << derived.getValue();

	return 0;
}
在上面的示例中，我们将 getValue() 函数标记为已删除。这意味着当我们尝试调用函数的派生版本时，编译器会抱怨。请注意，Base 版本的 getValue() 仍然可以访问。我们可以通过两种方式调用 Base::getValue()
int main()
{
	Derived derived { 7 };

	// We can call the Base::getValue() function directly
	std::cout << derived.Base::getValue();

	// Or we can upcast Derived to a Base reference and getValue() will resolve to Base::getValue()
	std::cout << static_cast<Base&>(derived).getValue();

	return 0;
}
如果使用强制转换方法，我们强制转换为 Base& 而不是 Base，以避免复制 `derived` 的 Base 部分。
下一课
24.9
多重继承
返回目录
上一课
24.7
调用继承的函数和覆盖行为