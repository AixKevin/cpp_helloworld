# 25.3 — override 和 final 说明符，以及协变返回类型

25.3 — override 和 final 说明符，以及协变返回类型
Alex
2016 年 11 月 6 日，太平洋标准时间晚上 8:34
2024 年 12 月 29 日
为了解决继承中一些常见的挑战，C++ 引入了两个与继承相关的标识符：
override
和
final
。请注意，这些标识符不是关键字——它们是普通单词，仅在特定上下文中使用时才具有特殊含义。C++ 标准称它们为“具有特殊含义的标识符”，但它们通常被称为“说明符”。
尽管 final 用得不多，但 override 是一个极好的补充，你应该经常使用。在本课中，我们将探讨两者，以及虚函数覆盖返回类型必须匹配规则的一个例外。
override 说明符
正如我们在上一课中提到的，派生类虚函数只有当其签名和返回类型完全匹配时才被视为覆盖。这可能导致意外问题，即一个原本打算进行覆盖的函数实际上并没有覆盖。
考虑以下示例
#include <iostream>
#include <string_view>

class A
{
public:
	virtual std::string_view getName1(int x) { return "A"; }
	virtual std::string_view getName2(int x) { return "A"; }
};

class B : public A
{
public:
	virtual std::string_view getName1(short x) { return "B"; } // note: parameter is a short
	virtual std::string_view getName2(int x) const { return "B"; } // note: function is const
};

int main()
{
	B b{};
	A& rBase{ b };
	std::cout << rBase.getName1(1) << '\n';
	std::cout << rBase.getName2(2) << '\n';

	return 0;
}
因为 rBase 是一个指向 B 对象的 A 引用，所以这里的意图是使用虚函数来访问 B::getName1() 和 B::getName2()。然而，因为 B::getName1() 采用不同的参数（一个 short 而不是一个 int），它不被认为是 A::getName1() 的覆盖。更具欺骗性的是，因为 B::getName2() 是 const 而 A::getName2() 不是，所以 B::getName2() 不被认为是 A::getName2() 的覆盖。
因此，这个程序打印出
A
A
在这个特定的例子中，因为 A 和 B 只是打印它们的名称，所以很容易看出我们搞错了覆盖，并且调用了错误的虚函数。然而，在一个更复杂的程序中，如果函数有行为或返回值没有被打印出来，这些问题可能很难调试。
为了帮助解决那些本应是覆盖但又不是的函数问题，可以将
override
说明符应用于任何虚函数，以告诉编译器强制该函数是覆盖。
override
说明符放置在成员函数声明的末尾（与函数级
const
放置的位置相同）。如果成员函数既是
const
又是
override
，则
const
必须在
override
之前。
如果标记为
override
的函数没有覆盖基类函数（或应用于非虚函数），编译器会将其标记为错误。
#include <string_view>

class A
{
public:
	virtual std::string_view getName1(int x) { return "A"; }
	virtual std::string_view getName2(int x) { return "A"; }
	virtual std::string_view getName3(int x) { return "A"; }
};

class B : public A
{
public:
	std::string_view getName1(short int x) override { return "B"; } // compile error, function is not an override
	std::string_view getName2(int x) const override { return "B"; } // compile error, function is not an override
	std::string_view getName3(int x) override { return "B"; } // okay, function is an override of A::getName3(int)

};

int main()
{
	return 0;
}
以上程序会产生两个编译错误：一个针对 B::getName1()，一个针对 B::getName2()，因为它们都没有覆盖之前的函数。B::getName3() 确实覆盖了 A::getName3()，因此该行没有产生错误。
由于使用 override 说明符没有性能损失，并且它有助于确保您确实覆盖了您认为已覆盖的函数，因此所有虚覆盖函数都应使用 override 说明符进行标记。此外，由于 override 说明符隐含了 virtual，因此无需使用 virtual 关键字标记使用 override 说明符的函数。
最佳实践
在基类的虚函数上使用 virtual 关键字。
在派生类的覆盖函数上使用 override 说明符（但不要使用 virtual 关键字）。这包括虚析构函数。
规则
如果一个成员函数既是
const
又是
override
，那么
const
必须列在前面。
const override
是正确的，
override const
是错误的。
final 说明符
在某些情况下，您可能不希望其他人能够覆盖虚函数或从某个类继承。final 说明符可以用来告诉编译器强制执行此限制。如果用户试图覆盖一个被指定为 final 的函数或从一个被指定为 final 的类继承，编译器将给出编译错误。
在我们要限制用户覆盖函数的情况下，**final 说明符**与 override 说明符使用在相同的位置，如下所示
#include <string_view>

class A
{
public:
	virtual std::string_view getName() const { return "A"; }
};

class B : public A
{
public:
	// note use of final specifier on following line -- that makes this function not able to be overridden in derived classes
	std::string_view getName() const override final { return "B"; } // okay, overrides A::getName()
};

class C : public B
{
public:
	std::string_view getName() const override { return "C"; } // compile error: overrides B::getName(), which is final
};
在上面的代码中，B::getName() 覆盖了 A::getName()，这是可以的。但是 B::getName() 带有 final 说明符，这意味着该函数的任何进一步覆盖都应被视为错误。事实上，C::getName() 试图覆盖 B::getName()（这里的 override 说明符不重要，只是为了良好的实践），所以编译器会给出一个编译错误。
在我们要阻止从一个类继承的情况下，final 说明符放在类名之后
#include <string_view>

class A
{
public:
	virtual std::string_view getName() const { return "A"; }
};

class B final : public A // note use of final specifier here
{
public:
	std::string_view getName() const override { return "B"; }
};

class C : public B // compile error: cannot inherit from final class
{
public:
	std::string_view getName() const override { return "C"; }
};
在上面的例子中，类 B 被声明为 final。因此，当 C 试图从 B 继承时，编译器会给出编译错误。
协变返回类型
有一种特殊情况，派生类虚函数覆盖可以具有与基类不同的返回类型，并且仍然被认为是匹配的覆盖。如果虚函数的返回类型是指向某个类的指针或引用，则覆盖函数可以返回指向派生类的指针或引用。这被称为**协变返回类型**。这是一个例子
#include <iostream>
#include <string_view>

class Base
{
public:
	// This version of getThis() returns a pointer to a Base class
	virtual Base* getThis() { std::cout << "called Base::getThis()\n"; return this; }
	void printType() { std::cout << "returned a Base\n"; }
};

class Derived : public Base
{
public:
	// Normally override functions have to return objects of the same type as the base function
	// However, because Derived is derived from Base, it's okay to return Derived* instead of Base*
	Derived* getThis() override { std::cout << "called Derived::getThis()\n";  return this; }
	void printType() { std::cout << "returned a Derived\n"; }
};

int main()
{
	Derived d{};
	Base* b{ &d };
	d.getThis()->printType(); // calls Derived::getThis(), returns a Derived*, calls Derived::printType
	b->getThis()->printType(); // calls Derived::getThis(), returns a Base*, calls Base::printType

	return 0;
}
这会打印
called Derived::getThis()
returned a Derived
called Derived::getThis()
returned a Base
关于协变返回类型一个有趣的注意事项：C++ 不能动态选择类型，所以你总是会得到与实际调用的函数版本匹配的类型。
在上面的例子中，我们首先调用 d.getThis()。由于 d 是 Derived 类型，这会调用 Derived::getThis()，它返回一个
Derived*
。然后，这个
Derived*
被用来调用非虚函数 Derived::printType()。
现在是比较有趣的情况。我们接着调用 b->getThis()。变量 b 是一个指向 Derived 对象的 Base 指针。Base::getThis() 是一个虚函数，所以这会调用 Derived::getThis()。尽管 Derived::getThis() 返回一个
Derived*
，但因为函数的 Base 版本返回一个
Base*
，所以返回的 Derived* 被向上转型为
Base*
。因为 Base::printType() 是非虚的，所以会调用 Base::printType()。
换句话说，在上面的例子中，只有当您首先使用类型为 Derived 对象的对象调用 getThis() 时，才会获得
Derived*
。
请注意，如果 printType() 是虚函数而不是非虚函数，那么 b->getThis() 的结果（类型为
Base*
的对象）将经历虚函数解析，并且会调用 Derived::printType()。
协变返回类型通常用于虚成员函数返回指向包含该成员函数的类的指针或引用的情况（例如 Base::getThis() 返回
Base*
，而 Derived::getThis() 返回
Derived*
）。然而，这并非严格必需。协变返回类型可以在任何情况下使用，只要覆盖成员函数的返回类型派生自基类虚成员函数的返回类型。
小测验时间
问题 #1
以下程序会输出什么？
#include <iostream>

class A
{
public:
    void print()
    {
        std::cout << "A";
    }
    virtual void vprint()
    {
        std::cout << "A";
    }
};
class B : public A
{
public:
    void print()
    {
        std::cout << "B";
    }
    void vprint() override
    {
        std::cout << "B";
    }
};


class C
{
private:
    A m_a{};

public:
    virtual A& get()
    {
        return m_a;
    }
};

class D : public C
{
private:
    B m_b{};

public:
    B& get() override // covariant return type
    {
        return m_b;
    }
};

int main()
{
    // case 1
    D d {};
    d.get().print();
    d.get().vprint();
    std::cout << '\n';
 
    // case 2
    C c {};
    c.get().print();
    c.get().vprint();
    std::cout << '\n';

    // case 3
    C& ref{ d };
    ref.get().print();
    ref.get().vprint();
    std::cout << '\n';

    return 0;
}
显示答案
BB
AA
AB
在所有情况下，由于
get()
具有协变返回类型，
get()
的返回类型将是隐式对象的
get()
成员函数的返回类型。
情况 1 很直接。在两个语句中，
d.get()
都调用
D::get()
，它返回
m_b
。因为
get()
是在
d
上调用的，而
d
的类型是
D
，所以使用
D::get()
的返回类型，即
B&
。对
print()
和
vprint()
的调用分别解析为
B::print()
和
B::vprint()
。
情况 2 也非常简单。在两个语句中，
c.get()
都调用
C::get()
，它返回
m_a
。因为
get()
是在
c
上调用的，而
c
的类型是
C
，所以使用
C::get()
的返回类型，即
A&
。对
print()
和
vprint()
的调用分别解析为
A::print()
和
A::vprint()
。
情况 3 是一个有趣的情况。
ref
是一个引用
D
的
C&
。
ref.get()
是一个虚函数，因此
ref.get()
虚拟解析为
D::get()
，它返回
m_b
。然而，
get()
具有协变返回类型，因此
get()
的返回类型由调用
get()
的隐式对象的类型决定。由于
ref
是一个
C&
，因此使用
C::get()
的返回类型，这意味着
ref.get()
的返回类型是
A&
（引用对象
m_b
，它是一个
B
）。
由于
ref.get()
的返回类型是
A&
，非虚函数调用
ref.get().print()
解析为
A::print()
。
当调用虚函数
ref.get().vprint()
时，会使用虚函数解析。虽然
ref.get()
的返回类型是
A&
，但被引用的对象实际上是
B
。因此，调用
B::vprint()
。
问题 #2
我们何时使用函数重载与函数覆盖？
显示答案
当我们希望成员函数或非成员函数在传递不同类型的参数时表现不同时，使用函数重载。
当我们需要一个成员函数在隐式对象是派生类时表现不同，我们使用函数覆盖。
下一课
25.4
虚析构函数、虚赋值和覆盖虚拟化
返回目录
上一课
25.2
虚函数和多态