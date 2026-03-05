# 24.7 — 调用继承的函数和重写行为

24.7 — 调用继承的函数和重写行为
Alex
2017 年 6 月 27 日，下午 4:28 PDT
2024 年 6 月 9 日
默认情况下，派生类继承基类中定义的所有行为。在本节课中，我们将更详细地探讨成员函数如何被选中，以及如何利用这一点来改变派生类中的行为。
当在派生类对象上调用成员函数时，编译器首先检查派生类中是否存在具有该名称的函数。如果存在，则考虑所有具有该名称的重载函数，并使用函数重载解析过程来确定是否存在最佳匹配。如果不存在，编译器会向上遍历继承链，以相同的方式依次检查每个父类。
换句话说，编译器将从至少有一个同名函数的最派生类中选择最佳匹配函数。
调用基类函数
首先，让我们探讨当派生类没有匹配函数但基类有匹配函数时会发生什么。
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
这会打印
Base::identify()
Base::identify()
当调用 `base.identify()` 时，编译器会查找 `Base` 类中是否定义了名为 `identify()` 的函数。它已定义，因此编译器会查看它是否匹配。它匹配，因此被调用。
当调用 `derived.identify()` 时，编译器会查找 `Derived` 类中是否定义了名为 `identify()` 的函数。它没有定义。因此它移动到父类（在本例中是 `Base`），然后再次尝试。 `Base` 定义了一个 `identify()` 函数，因此它使用了那个。换句话说，`Base::identify()` 被使用了，因为 `Derived::identify()` 不存在。
这意味着如果基类提供的行为足够，我们可以简单地使用基类行为。
重新定义行为
但是，如果我们已经在 `Derived` 类中定义了 `Derived::identify()`，那么它将被使用。
这意味着我们可以通过在派生类中重新定义函数，使函数在我们的派生类中以不同的方式工作！
例如，假设我们希望 `derived.identify()` 打印 `Derived::identify()`。我们可以简单地在 `Derived` 类中添加函数 `identify()`，这样当我们使用 `Derived` 对象调用函数 `identify()` 时，它会返回正确的响应。
要修改基类中定义的函数在派生类中的工作方式，只需在派生类中重新定义该函数即可。
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const { std::cout << "Derived::identify()\n"; }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
这会打印
Base::identify()
Derived::identify()
请注意，当您在派生类中重新定义函数时，派生函数不会继承基类中同名函数的访问说明符。它使用在派生类中定义的任何访问说明符。因此，在基类中定义为 private 的函数可以在派生类中重新定义为 public，反之亦然！
#include <iostream>

class Base
{
private:
	void print() const 
	{
		std::cout << "Base";
	}
};
 
class Derived : public Base
{
public:
	void print() const 
	{
		std::cout << "Derived ";
	}
};
 
 
int main()
{
	Derived derived {};
	derived.print(); // calls derived::print(), which is public
	return 0;
}
现有功能新增
有时我们不想完全替换基类函数，而是希望在调用派生对象时为其添加额外功能。在上面的示例中，请注意 `Derived::identify()` 完全隐藏了 `Base::identify()`！这可能不是我们想要的。我们可以让派生函数调用同名函数的基版本（以重用代码），然后为其添加额外功能。
要让派生函数调用同名的基函数，只需进行正常函数调用，但在函数前加上基类的作用域限定符。例如：
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const
    {
        std::cout << "Derived::identify()\n";
        Base::identify(); // note call to Base::identify() here
    }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
这会打印
Base::identify()
Derived::identify()
Base::identify()
当 `derived.identify()` 执行时，它解析为 `Derived::identify()`。在打印 `Derived::identify()` 之后，它会调用 `Base::identify()`，后者打印 `Base::identify()`。
这应该很直接。为什么我们需要使用作用域解析运算符 (::)？如果我们将 `Derived::identify()` 定义成这样：
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const
    {
        std::cout << "Derived::identify()\n";
        identify(); // no scope resolution results in self-call and infinite recursion
    }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
在没有作用域解析限定符的情况下调用函数 `identify()` 将默认调用当前类中的 `identify()`，即 `Derived::identify()`。这将导致 `Derived::identify()` 调用自身，从而导致无限递归！
在尝试调用基类中的友元函数（例如 `operator<<`）时，我们可能会遇到一些棘手的问题。由于基类的友元函数实际上不是基类的一部分，因此使用作用域解析限定符将不起作用。相反，我们需要一种方法来使我们的 `Derived` 类临时看起来像 `Base` 类，以便可以调用正确的函数版本。
幸运的是，使用 `static_cast` 可以轻松做到这一点。这是一个示例：
#include <iostream>

class Base
{
public:
    Base() { }

	friend std::ostream& operator<< (std::ostream& out, const Base&)
	{
		out << "In Base\n";
		return out;
	}
};

class Derived: public Base
{
public:
    Derived() { }

 	friend std::ostream& operator<< (std::ostream& out, const Derived& d)
	{
		out << "In Derived\n";
		// static_cast Derived to a Base object, so we call the right version of operator<<
		out << static_cast<const Base&>(d); 
		return out;
    }
};

int main()
{
    Derived derived {};

    std::cout << derived << '\n';

    return 0;
}
因为 `Derived` 是 `Base`，所以我们可以将我们的 `Derived` 对象 `static_cast` 为 `Base` 引用，这样就会调用使用 `Base` 的 `operator<<` 的适当版本。
这会打印
In Derived
In Base
派生类中的重载解析
正如本课开头所述，编译器将从至少有一个同名函数的最派生类中选择最佳匹配函数。
首先，让我们看一个简单的重载成员函数示例：
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
};


int main()
{
    Derived d{};
    d.print(5); // calls Base::print(int)

    return 0;
}
对于调用 `d.print(5)`，编译器在 `Derived` 中找不到名为 `print()` 的函数，因此它检查 `Base`，并在其中找到两个同名函数。它使用函数重载解析过程来确定 `Base::print(int)` 比 `Base::print(double)` 更匹配。因此，`Base::print(int)` 被调用，正如我们所期望的。
现在让我们看一个可能不像我们预期那样表现的例子
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    void print(double) { std::cout << "Derived::print(double)"; } // this function added
};


int main()
{
    Derived d{};
    d.print(5); // calls Derived::print(double), not Base::print(int)

    return 0;
}
对于调用 `d.print(5)`，编译器在 `Derived` 中找到一个名为 `print()` 的函数，因此在尝试确定要解析哪个函数时，它只会考虑 `Derived` 中的函数。此函数也是 `Derived` 中此函数调用的最佳匹配函数。因此，这会调用 `Derived::print(double)`。
由于 `Base::print(int)` 的参数比 `Derived::print(double)` 更适合 int 参数 `5`，您可能一直期望此函数调用解析为 `Base::print(int)`。但是因为 `d` 是一个 `Derived`，在 `Derived` 中至少有一个 `print()` 函数，并且 `Derived` 比 `Base` 更派生，所以 `Base` 中的函数甚至没有被考虑。
那么，如果我们真的希望 `d.print(5)` 解析为 `Base::print(int)` 怎么办？一个不太好的方法是定义一个 `Derived::print(int)`。
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    void print(int n) { Base::print(n); } // works but not great, as we have to define 
    void print(double) { std::cout << "Derived::print(double)"; }
};

int main()
{
    Derived d{};
    d.print(5); // calls Derived::print(int), which calls Base::print(int)

    return 0;
}
虽然这有效，但它不太好，因为我们必须为每个希望传递到 `Base` 的重载向 `Derived` 添加一个函数。这可能会增加许多额外函数，它们基本上只是将调用路由到 `Base`。
更好的选择是在 `Derived` 中使用 `using-声明`，使所有具有特定名称的 `Base` 函数在 `Derived` 中可见。
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    using Base::print; // make all Base::print() functions eligible for overload resolution
    void print(double) { std::cout << "Derived::print(double)"; }
};


int main()
{
    Derived d{};
    d.print(5); // calls Base::print(int), which is the best matching function visible in Derived

    return 0;
}
通过在 `Derived` 中放置 `using Base::print;` 声明，我们告诉编译器所有名为 `print` 的 `Base` 函数都应该在 `Derived` 中可见，这将使它们符合重载解析的条件。因此，`Base::print(int)` 被选中，而不是 `Derived::print(double)`。
下一课
24.8
隐藏继承的功能
返回目录
上一课
24.6
向派生类添加新功能