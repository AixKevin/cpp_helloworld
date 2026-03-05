# 25.10 — 动态类型转换

25.10 — 动态类型转换
Alex
2016 年 11 月 22 日下午 4:48 PST
2024 年 12 月 29 日
早在课程
10.6 -- 显式类型转换 (casting) 和 static_cast
中，我们研究了类型转换的概念，以及使用 static_cast 将变量从一种类型转换为另一种类型。
在本课程中，我们将继续研究另一种类型转换：dynamic_cast。
dynamic_cast 的必要性
在处理多态性时，您经常会遇到这样的情况：您有一个指向基类的指针，但您想访问只存在于派生类中的某些信息。
考虑以下（略显人为的）程序
#include <iostream>
#include <string>
#include <string_view>

class Base
{
protected:
	int m_value{};

public:
	Base(int value)
		: m_value{value}
	{
	}
	
	virtual ~Base() = default;
};

class Derived : public Base
{
protected:
	std::string m_name{};

public:
	Derived(int value, std::string_view name)
		: Base{value}, m_name{name}
	{
	}

	const std::string& getName() const { return m_name; }
};

Base* getObject(bool returnDerived)
{
	if (returnDerived)
		return new Derived{1, "Apple"};
	else
		return new Base{2};
}

int main()
{
	Base* b{ getObject(true) };

	// how do we print the Derived object's name here, having only a Base pointer?

	delete b;

	return 0;
}
在此程序中，函数 getObject() 总是返回一个 Base 指针，但该指针可能指向 Base 或 Derived 对象。如果 Base 指针实际上指向一个 Derived 对象，我们如何调用 Derived::getName()？
一种方法是向 Base 添加一个名为 getName() 的虚函数（这样我们就可以用 Base 指针/引用调用它，并让它动态解析到 Derived::getName()）。但是，如果您用 Base 指针/引用调用它，而该指针/引用实际上指向一个 Base 对象，这个函数会返回什么？没有真正有意义的值。此外，我们会用那些只应由 Derived 类关注的事物来污染我们的 Base 类。
我们知道 C++ 会隐式地允许您将 Derived 指针转换为 Base 指针（事实上，getObject() 就是这样做的）。这个过程有时称为
向上转型
。但是，有没有办法将 Base 指针转换回 Derived 指针呢？那样我们就可以直接使用该指针调用 Derived::getName()，完全不必担心虚函数解析。
dynamic_cast
C++ 提供了一个名为
dynamic_cast
的类型转换运算符，可用于此目的。尽管动态类型转换具有一些不同的功能，但到目前为止，动态类型转换最常见的用途是将基类指针转换为派生类指针。这个过程称为
向下转型
。
使用 dynamic_cast 的方法与 static_cast 相同。以下是我们上面示例中的 main()，使用 dynamic_cast 将我们的 Base 指针转换回 Derived 指针
int main()
{
	Base* b{ getObject(true) };

	Derived* d{ dynamic_cast<Derived*>(b) }; // use dynamic cast to convert Base pointer into Derived pointer

	std::cout << "The name of the Derived is: " << d->getName() << '\n';

	delete b;

	return 0;
}
这会打印
The name of the Derived is: Apple
dynamic_cast 失败
上面的例子之所以有效，是因为 b 实际上指向一个 Derived 对象，所以将 b 转换为 Derived 指针是成功的。
然而，我们做了一个相当危险的假设：b 指向一个 Derived 对象。如果 b 不指向一个 Derived 对象呢？这很容易通过将 getObject() 的参数从 true 更改为 false 来测试。在这种情况下，getObject() 将返回一个指向 Base 对象的 Base 指针。当我们尝试将其 dynamic_cast 到 Derived 时，它将失败，因为无法进行转换。
如果 dynamic_cast 失败，转换结果将是一个空指针。
因为我们没有检查空指针结果，所以我们访问 d->getName()，这将尝试解引用空指针，导致未定义行为（很可能是崩溃）。
为了使这个程序安全，我们需要确保 dynamic_cast 的结果确实成功了
int main()
{
	Base* b{ getObject(true) };

	Derived* d{ dynamic_cast<Derived*>(b) }; // use dynamic cast to convert Base pointer into Derived pointer

	if (d) // make sure d is non-null
		std::cout << "The name of the Derived is: " << d->getName() << '\n';

	delete b;

	return 0;
}
规则
始终通过检查空指针结果来确保您的动态转换确实成功。
请注意，因为 dynamic_cast 在运行时进行了一些一致性检查（以确保可以进行转换），所以使用 dynamic_cast 会带来性能开销。
另请注意，在以下几种情况下，使用 dynamic_cast 进行向下转型将不起作用
使用 protected 或 private 继承。
对于没有声明或继承任何虚函数的类（因此没有虚表）。
在某些涉及虚基类的情况下（有关其中一些情况的示例以及如何解决它们，请参阅
此页面
）。
使用 static_cast 进行向下转型
事实证明，向下转型也可以使用 static_cast 完成。主要区别在于 static_cast 不进行运行时类型检查以确保您所做的事情有意义。这使得使用 static_cast 更快，但更危险。如果您将 Base* 强制转换为 Derived*，即使 Base 指针没有指向 Derived 对象，它也会“成功”。当您尝试访问结果 Derived 指针（实际上指向 Base 对象）时，这将导致未定义行为。
如果您绝对确定您向下转型的指针会成功，那么使用 static_cast 是可以接受的。确保您知道所指向的对象类型的一种方法是使用虚函数。这是一种（不太好）的方法
#include <iostream>
#include <string>
#include <string_view>

// Class identifier
enum class ClassID
{
	base,
	derived
	// Others can be added here later
};

class Base
{
protected:
	int m_value{};

public:
	Base(int value)
		: m_value{value}
	{
	}

	virtual ~Base() = default;
	virtual ClassID getClassID() const { return ClassID::base; }
};

class Derived : public Base
{
protected:
	std::string m_name{};

public:
	Derived(int value, std::string_view name)
		: Base{value}, m_name{name}
	{
	}

	const std::string& getName() const { return m_name; }
	ClassID getClassID() const override { return ClassID::derived; }

};

Base* getObject(bool bReturnDerived)
{
	if (bReturnDerived)
		return new Derived{1, "Apple"};
	else
		return new Base{2};
}

int main()
{
	Base* b{ getObject(true) };

	if (b->getClassID() == ClassID::derived)
	{
		// We already proved b is pointing to a Derived object, so this should always succeed
		Derived* d{ static_cast<Derived*>(b) };
		std::cout << "The name of the Derived is: " << d->getName() << '\n';
	}

	delete b;

	return 0;
}
但是，如果您要费尽心思实现这一点（并付出调用虚函数和处理结果的代价），那么您不妨直接使用 dynamic_cast。
还要考虑如果我们的对象实际上是 Derived 派生出来的某个类（我们称之为
D2
）会发生什么。上面的检查
b->getClassID() == ClassID::derived
将失败，因为
getClassId()
将返回
ClassID::D2
，它不等于
ClassID::derived
。然而，将
D2
动态转换为
Derived
将成功，因为
D2
是
Derived
！
dynamic_cast 和引用
尽管上述所有示例都显示了指针的动态转换（这更常见），但 dynamic_cast 也可以与引用一起使用。这与 dynamic_cast 处理指针的方式类似。
#include <iostream>
#include <string>
#include <string_view>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{value}
	{
	}

	virtual ~Base() = default; 
};

class Derived : public Base
{
protected:
	std::string m_name;

public:
	Derived(int value, std::string_view name)
		: Base{value}, m_name{name}
	{
	}

	const std::string& getName() const { return m_name; }
};

int main()
{
	Derived apple{1, "Apple"}; // create an apple
	Base& b{ apple }; // set base reference to object
	Derived& d{ dynamic_cast<Derived&>(b) }; // dynamic cast using a reference instead of a pointer

	std::cout << "The name of the Derived is: " << d.getName() << '\n'; // we can access Derived::getName through d

	return 0;
}
因为 C++ 没有“空引用”，所以 dynamic_cast 在失败时不能返回空引用。相反，如果引用的 dynamic_cast 失败，则会抛出 std::bad_cast 类型的异常。我们将在本教程后面讨论异常。
dynamic_cast 与 static_cast
新程序员有时会混淆何时使用 static_cast 与 dynamic_cast。答案很简单：除非您正在向下转型，否则请使用 static_cast，在这种情况下，dynamic_cast 通常是更好的选择。但是，您也应该考虑完全避免类型转换，只使用虚函数。
向下转型与虚函数
有些开发人员认为 dynamic_cast 是邪恶的，并且预示着糟糕的类设计。相反，这些程序员说您应该使用虚函数。
通常，使用虚函数
应该
优于向下转型。但是，有时向下转型是更好的选择
当您无法修改基类以添加虚函数时（例如，因为基类是标准库的一部分）
当您需要访问派生类特有的内容时（例如，只存在于派生类中的访问函数）
当向基类添加虚函数没有意义时（例如，基类没有合适的返回值）。如果您不需要实例化基类，纯虚函数可能是一个选项。
关于 dynamic_cast 和 RTTI 的警告
运行时类型信息 (RTTI) 是 C++ 的一项功能，可在运行时公开有关对象数据类型的信息。dynamic_cast 利用了此功能。由于 RTTI 具有相当大的空间性能开销，因此一些编译器允许您将 RTTI 关闭作为优化。不用说，如果您这样做，dynamic_cast 将无法正常工作。
下一课
25.11
使用 operator<< 打印继承类
返回目录
上一课
25.9
对象切片