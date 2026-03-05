# 25.11 — 使用 operator<< 打印继承类

25.11 — 使用 operator<< 打印继承类
Alex
2016 年 11 月 23 日，下午 1:57 PST
2024 年 2 月 18 日
考虑以下使用虚函数的程序
#include <iostream>

class Base
{
public:
	virtual void print() const { std::cout << "Base";  }
};

class Derived : public Base
{
public:
	void print() const override { std::cout << "Derived"; }
};

int main()
{
	Derived d{};
	Base& b{ d };
	b.print(); // will call Derived::print()

	return 0;
}
现在，您应该已经熟悉 b.print() 将调用 Derived::print() 的事实（因为 b 引用的是 Derived 类对象，Base::print() 是一个虚函数，而 Derived::print() 是一个重写）。
虽然像这样调用成员函数进行输出是可以的，但这种函数风格与 std::cout 配合不佳
#include <iostream>

int main()
{
	Derived d{};
	Base& b{ d };

	std::cout << "b is a ";
	b.print(); // messy, we have to break our print statement to call this function
	std::cout << '\n';

	return 0;
}
在本课中，我们将探讨如何为使用继承的类重写 operator<<，以便我们可以像这样按预期使用 operator<<
std::cout << "b is a " << b << '\n'; // much better
operator<< 的挑战
让我们首先以典型方式重载 operator<<
#include <iostream>

class Base
{
public:
	virtual void print() const { std::cout << "Base"; }

	friend std::ostream& operator<<(std::ostream& out, const Base& b)
	{
		out << "Base";
		return out;
	}
};

class Derived : public Base
{
public:
	void print() const override { std::cout << "Derived"; }

	friend std::ostream& operator<<(std::ostream& out, const Derived& d)
	{
		out << "Derived";
		return out;
	}
};

int main()
{
	Base b{};
	std::cout << b << '\n';

	Derived d{};
	std::cout << d << '\n';

	return 0;
}
因为这里不需要虚函数解析，所以这个程序按预期工作，并打印
Base
Derived
现在，考虑以下 main() 函数
int main()
{
    Derived d{};
    Base& bref{ d };
    std::cout << bref << '\n';
    
    return 0;
}
这个程序打印
Base
这可能不是我们所期望的。发生这种情况是因为我们处理 Base 对象的 operator<< 版本不是虚的，所以 std::cout << bref 调用处理 Base 对象的 operator<< 版本，而不是 Derived 对象的版本。
挑战就在于此。
我们可以让 operator<< 成为虚函数吗？
如果问题是 operator<< 不是虚函数，我们不能简单地让它成为虚函数吗？
简短的答案是不行。这有几个原因。
首先，只有成员函数才能被虚化——这是有道理的，因为只有类才能继承其他类，而且无法重写类外部的函数（你可以重载非成员函数，但不能重写它们）。因为我们通常将 operator<< 实现为友元函数，而友元函数不被视为成员函数，所以友元版本的 operator<< 不符合虚化的条件。（要复习为什么我们以这种方式实现 operator<<，请重新访问课程
21.5 — 使用成员函数重载运算符
）。
其次，即使我们可以将 operator<< 虚化，也存在 Base::operator<< 和 Derived::operator<< 的函数参数不同的问题（Base 版本将采用 Base 参数，而 Derived 版本将采用 Derived 参数）。因此，Derived 版本不会被视为 Base 版本的重写，因此不符合虚函数解析的条件。
那么程序员该怎么办呢？
一种解决方案
事实证明，答案出人意料地简单。
首先，我们像往常一样在基类中将 `operator<<` 设置为友元函数。但是，我们不让 `operator<<` 决定打印什么，而是让它调用一个可以虚化的普通成员函数！这个虚函数将完成决定为每个类打印什么的工作。
在第一个解决方案中，我们的虚成员函数（我们称之为 `identify()`）返回一个 `std::string`，由 `Base::operator<<` 打印。
#include <iostream>

class Base
{
public:
	// Here's our overloaded operator<<
	friend std::ostream& operator<<(std::ostream& out, const Base& b)
	{
		// Call virtual function identify() to get the string to be printed
		out << b.identify();
		return out;
	}

	// We'll rely on member function identify() to return the string to be printed
	// Because identify() is a normal member function, it can be virtualized
	virtual std::string identify() const
	{
		return "Base";
	}
};

class Derived : public Base
{
public:
	// Here's our override identify() function to handle the Derived case
	std::string identify() const override
	{
		return "Derived";
	}
};

int main()
{
	Base b{};
	std::cout << b << '\n';

	Derived d{};
	std::cout << d << '\n'; // note that this works even with no operator<< that explicitly handles Derived objects

	Base& bref{ d };
	std::cout << bref << '\n';

	return 0;
}
这会打印预期结果
Base
Derived
Derived
让我们更详细地研究一下这是如何工作的。
在 `Base b` 的情况下，`operator<<` 被调用，参数 `b` 引用 Base 对象。虚函数调用 `b.identify()` 因此解析为 `Base::identify()`，它返回“Base”以供打印。这里没什么特别的。
在 `Derived d` 的情况下，编译器首先检查是否存在接受 Derived 对象的 `operator<<`。没有，因为我们没有定义。接下来编译器检查是否存在接受 Base 对象的 `operator<<`。存在，因此编译器将我们的 Derived 对象隐式向上转换为 `Base&` 并调用该函数（我们可以自己进行这种向上转换，但编译器在这方面很有帮助）。因为参数 `b` 引用的是 Derived 对象，所以虚函数调用 `b.identify()` 解析为 `Derived::identify()`，它返回“Derived”以供打印。
请注意，我们不需要为每个派生类定义 `operator<<`！处理 Base 对象的版本对于 Base 对象和任何从 Base 派生出来的类都同样适用！
第三种情况是前两种情况的混合。首先，编译器将变量 `bref` 与接受 `Base` 引用的 `operator<<` 匹配。因为参数 `b` 引用的是 `Derived` 对象，所以 `b.identify()` 解析为 `Derived::identify()`，返回“Derived”。
问题解决了。
一个更灵活的解决方案
上述解决方案效果很好，但有两个潜在的缺点
它假设所需输出可以表示为单个 std::string。
我们的 `identify()` 成员函数无法访问流对象。
后一个问题在我们需要流对象的情况下是棘手的，例如当我们要打印具有重载 operator<< 的成员变量的值时。
幸运的是，修改上述示例以解决这两个问题非常简单。在之前的版本中，虚函数 `identify()` 返回一个字符串，由 `Base::operator<<` 打印。在这个版本中，我们将改为定义虚成员函数 `print()` 并将打印的责任直接委托给该函数。
这是一个说明该想法的示例
#include <iostream>

class Base
{
public:
	// Here's our overloaded operator<<
	friend std::ostream& operator<<(std::ostream& out, const Base& b)
	{
		// Delegate printing responsibility for printing to virtual member function print()
		return b.print(out);
	}

	// We'll rely on member function print() to do the actual printing
	// Because print() is a normal member function, it can be virtualized
	virtual std::ostream& print(std::ostream& out) const
	{
		out << "Base";
		return out;
	}
};

// Some class or struct with an overloaded operator<<
struct Employee
{
	std::string name{};
	int id{};

	friend std::ostream& operator<<(std::ostream& out, const Employee& e)
	{
		out << "Employee(" << e.name << ", " << e.id << ")";
		return out;
	}
};

class Derived : public Base
{
private:
	Employee m_e{}; // Derived now has an Employee member

public:
	Derived(const Employee& e)
		: m_e{ e }
	{
	}

	// Here's our override print() function to handle the Derived case
	std::ostream& print(std::ostream& out) const override
	{
		out << "Derived: ";

		// Print the Employee member using the stream object
		out << m_e;

		return out;
	}
};

int main()
{
	Base b{};
	std::cout << b << '\n';

	Derived d{ Employee{"Jim", 4}};
	std::cout << d << '\n'; // note that this works even with no operator<< that explicitly handles Derived objects

	Base& bref{ d };
	std::cout << bref << '\n';

	return 0;
}
这输出
Base
Derived: Employee(Jim, 4)
Derived: Employee(Jim, 4)
在此版本中，`Base::operator<<` 本身不进行任何打印。相反，它只是调用虚成员函数 `print()` 并将其流对象传递给它。然后，`print()` 函数使用此流对象进行自己的打印。`Base::print()` 使用流对象打印“Base”。更有趣的是，`Derived::print()` 使用流对象打印“Derived: ”并调用 `Employee::operator<<` 打印成员 `m_e` 的值。后者在前面的例子中会更具挑战性！
下一课
25.x
第 25 章总结和测验
返回目录
上一课
25.10
动态转换