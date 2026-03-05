# 25.2 — 虚函数和多态性

25.2 — 虚函数和多态性
Alex
2008 年 1 月 30 日，太平洋标准时间下午 3:46
2024 年 12 月 11 日
在上一课关于
指向派生对象基类的指针和引用
中，我们看了一些使用指向基类的指针或引用可能简化代码的例子。然而，在每个例子中，我们都遇到了一个问题：基类指针或引用只能调用函数的基类版本，而不能调用派生版本。
这是一个这种行为的简单示例
#include <iostream>
#include <string_view>

class Base
{
public:
    std::string_view getName() const { return "Base"; }
};

class Derived: public Base
{
public:
    std::string_view getName() const { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& rBase{ derived };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
这个例子打印结果
rBase is a Base
因为 rBase 是一个 Base 引用，它调用 Base::getName()，即使它实际上引用的是 Derived 对象的 Base 部分。
在本课中，我们将展示如何使用虚函数解决此问题。
虚函数
一个
虚函数
是一种特殊类型的成员函数，当它被调用时，会解析为被引用或指向的对象的实际类型中函数的最多派生版本。
如果派生函数具有与函数基类版本相同的签名（名称、参数类型以及是否为 const）和返回类型，则认为它是匹配的。此类函数称为
重写
。
要使函数成为虚函数，只需在函数声明前放置“virtual”关键字。
这是上面带有虚函数的例子
#include <iostream>
#include <string_view>

class Base
{
public:
    virtual std::string_view getName() const { return "Base"; } // note addition of virtual keyword
};

class Derived: public Base
{
public:
    virtual std::string_view getName() const { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& rBase{ derived };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
这个例子打印结果
rBase is a Derived
提示
一些现代编译器可能会因具有虚函数和可访问的非虚析构函数而报错。如果是这种情况，请为基类添加一个虚析构函数。在上面的程序中，将其添加到
Base
的定义中
virtual ~Base() = default;
我们在第
25.4 -- 虚析构函数、虚赋值和覆盖虚拟化
课中讨论虚析构函数。
因为 rBase 是一个指向 Derived 对象 Base 部分的引用，当
rBase.getName()
被评估时，它通常会解析为 Base::getName()。然而，Base::getName()是虚函数，这告诉程序去查找 Derived 对象是否有更派生的函数版本可用。在这种情况下，它会解析为 Derived::getName()！
让我们看一个稍微复杂的例子
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    virtual std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
    virtual std::string_view getName() const { return "C"; }
};

class D: public C
{
public:
    virtual std::string_view getName() const { return "D"; }
};

int main()
{
    C c {};
    A& rBase{ c };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
你认为这个程序会输出什么？
让我们看看它是如何工作的。首先，我们实例化一个 C 类对象。rBase 是一个 A 引用，我们将其设置为引用 C 对象的 A 部分。最后，我们调用 rBase.getName()。rBase.getName() 求值为 A::getName()。但是，A::getName() 是虚函数，因此编译器将调用 A 和 C 之间最派生的匹配项。在这种情况下，那是 C::getName()。请注意，它不会调用 D::getName()，因为我们原始的对象是 C，而不是 D，因此只考虑 A 和 C 之间的函数。
结果，我们的程序输出
rBase is a C
请注意，虚函数解析仅在通过指向类类型对象的指针或引用调用虚成员函数时才有效。这是因为编译器可以区分指针或引用的类型与所指向或引用的对象的类型。我们在上面的示例中看到了这一点。
直接在对象上调用虚成员函数（而不是通过指针或引用）将始终调用属于该对象相同类型的成员函数。例如
C c{};
std::cout << c.getName(); // will always call C::getName

A a { c }; // copies the A portion of c into a (don't do this)
std::cout << a.getName(); // will always call A::getName
关键见解
虚函数解析仅在通过指向类类型对象的指针或引用调用成员函数时才有效。
多态性
在编程中，
多态性
是指实体具有多种形式的能力（术语“多态性”字面意思就是“多种形式”）。例如，考虑以下两个函数声明
int add(int, int);
double add(double, double);
标识符
add
有两种形式：
add(int, int)
和
add(double, double)
。
编译时多态性
是指由编译器解析的多态性形式。这些包括函数重载解析以及模板解析。
运行时多态性
是指在运行时解析的多态性形式。这包括虚函数解析。
一个更复杂的例子
让我们再看看上一课中正在处理的 Animal 例子。这是原始类，以及一些测试代码
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // We're making this constructor protected because
    // we don't want people creating Animal objects directly,
    // but we still want derived classes to be able to use it.
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    std::string_view speak() const { return "???"; }
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const { return "Woof"; }
};

void report(const Animal& animal)
{
    std::cout << animal.getName() << " says " << animal.speak() << '\n';
}

int main()
{
    Cat cat{ "Fred" };
    Dog dog{ "Garbo" };

    report(cat);
    report(dog);

    return 0;
}
这会打印
Fred says ???
Garbo says ???
这是将 speak() 函数设为虚函数的等效类
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // We're making this constructor protected because
    // we don't want people creating Animal objects directly,
    // but we still want derived classes to be able to use it.
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    virtual std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    virtual std::string_view speak() const { return "Woof"; }
};

void report(const Animal& animal)
{
    std::cout << animal.getName() << " says " << animal.speak() << '\n';
}

int main()
{
    Cat cat{ "Fred" };
    Dog dog{ "Garbo" };

    report(cat);
    report(dog);

    return 0;
}
这个程序产生的结果是
Fred says Meow
Garbo says Woof
它奏效了！
当 `animal.speak()` 被评估时，程序注意到 `Animal::speak()` 是一个虚函数。在 `animal` 引用 `Cat` 对象的 `Animal` 部分的情况下，程序会查看 `Animal` 和 `Cat` 之间的所有类，以查看是否能找到一个更派生的函数。在这种情况下，它找到了 `Cat::speak()`。在 `animal` 引用 `Dog` 对象的 `Animal` 部分的情况下，程序将函数调用解析为 `Dog::speak()`。
请注意，我们没有将 Animal::getName() 设为虚函数。这是因为 getName() 从未在任何派生类中被重写，因此没有必要。
同样，以下数组示例现在按预期工作
Cat fred{ "Fred" };
Cat misty{ "Misty" };
Cat zeke{ "Zeke" };
 
Dog garbo{ "Garbo" };
Dog pooky{ "Pooky" };
Dog truffle{ "Truffle" };

// Set up an array of pointers to animals, and set those pointers to our Cat and Dog objects
Animal* animals[]{ &fred, &garbo, &misty, &pooky, &truffle, &zeke };

for (const auto* animal : animals)
    std::cout << animal->getName() << " says " << animal->speak() << '\n';
结果是
Fred says Meow
Garbo says Woof
Misty says Meow
Pooky says Woof
Truffle says Woof
Zeke says Meow
尽管这两个例子只使用了 Cat 和 Dog，但我们从 Animal 派生的任何其他类也都可以与我们的 report() 函数和 animal 数组一起工作，无需进一步修改！这可能是虚函数最大的好处——能够以一种方式组织代码，使得新派生类将自动与旧代码一起工作，而无需修改！
警告：派生类函数的签名必须
完全
匹配基类虚函数的签名，派生类函数才能被使用。如果派生类函数有不同的参数类型，程序很可能仍然可以编译，但虚函数将无法按预期解析。在下一课中，我们将讨论如何防止这种情况发生。
请注意，如果一个函数被标记为虚函数，那么派生类中所有匹配的重写也隐式地被认为是虚函数，即使它们没有明确标记。
规则
如果一个函数是虚函数，则派生类中所有匹配的重写都是隐式虚函数。
但这反过来就不行了——派生类中的虚重写不会隐式地使基类函数成为虚函数。
虚函数的返回类型
在正常情况下，虚函数及其重写的返回类型必须匹配。请看以下示例
class Base
{
public:
    virtual int getValue() const { return 5; }
};

class Derived: public Base
{
public:
    virtual double getValue() const { return 6.78; }
};
在这种情况下，Derived::getValue() 不被视为 Base::getValue() 的匹配重写，编译将失败。
不要从构造函数或析构函数中调用虚函数
这是另一个经常让不知情的新程序员措手不及的陷阱。你不应该从构造函数或析构函数中调用虚函数。为什么？
请记住，当创建派生类时，首先构造基类部分。如果您从基类构造函数调用虚函数，而类的派生部分尚未创建，它将无法调用函数的派生版本，因为没有派生对象供派生函数操作。在 C++ 中，它将改为调用基类版本。
对于析构函数也存在类似的问题。如果您在基类析构函数中调用虚函数，它将始终解析为函数的基类版本，因为类的派生部分将已经被销毁。
最佳实践
切勿从构造函数或析构函数中调用虚函数。
虚函数的缺点
既然大多数情况下你希望你的函数是虚函数，为什么不直接让所有函数都是虚函数呢？答案是因为它效率低下——解析虚函数调用比解析常规函数调用花费的时间更长。
此外，为了使虚函数工作，编译器必须为每个具有虚函数的类对象分配一个额外的指针。这给原本很小的对象带来了很大的开销。我们将在本章的后续课程中详细讨论这一点。
小测验时间
以下程序会打印什么？此练习旨在通过检查完成，而不是通过编译器编译示例。
1a)
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    virtual std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
// Note: no getName() function here
};

class D: public C
{
public:
    virtual std::string_view getName() const { return "D"; }
};

int main()
{
    C c {};
    A& rBase{ c };
    std::cout << rBase.getName() << '\n';

    return 0;
}
显示答案
B. rBase 是一个指向 C 对象的 A 引用。通常 rBase.getName() 会调用 A::getName()，但 A::getName() 是虚函数，因此它会转而调用 A 和 C 之间最派生的匹配函数。那是 B::getName()，它打印 B。
1b)
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    virtual std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
    virtual std::string_view getName() const { return "C"; }
};

class D: public C
{
public:
    virtual std::string_view getName() const { return "D"; }
};

int main()
{
    C c;
    B& rBase{ c }; // note: rBase is a B this time
    std::cout << rBase.getName() << '\n';

    return 0;
}
显示答案
C。这很简单，因为 C::getName() 是 B 和 C 类之间最派生的匹配调用。
1c)
#include <iostream>
#include <string_view>

class A
{
public:
    // note: no virtual keyword
    std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    virtual std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
    virtual std::string_view getName() const { return "C"; }
};

class D: public C
{
public:
    virtual std::string_view getName() const { return "D"; }
};

int main()
{
    C c {};
    A& rBase{ c };
    std::cout << rBase.getName() << '\n';

    return 0;
}
显示答案
A. 由于 A 不是虚函数，当调用 rBase.getName() 时，会调用 A::getName()。
1d)
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    // note: no virtual keyword in B, C, and D
    std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
    std::string_view getName() const { return "C"; }
};

class D: public C
{
public:
    std::string_view getName() const { return "D"; } 
};

int main()
{
    C c {};
    B& rBase{ c }; // note: rBase is a B this time
    std::cout << rBase.getName() << '\n';

    return 0;
}
显示答案
C. 即使 B 和 C 没有被标记为虚函数，A::getName() 是虚函数，而 B::getName() 和 C::getName() 都是重写。因此，B::getName() 和 C::getName() 被隐式地认为是虚函数，从而对 rBase.getName() 的调用解析为 C::getName()，而不是 B::getName()。
1e)
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    // Note: Functions in B, C, and D are non-const.
    virtual std::string_view getName() { return "B"; }
};

class C: public B
{
public:
    virtual std::string_view getName() { return "C"; }
};

class D: public C
{
public:
    virtual std::string_view getName() { return "D"; }
};

int main()
{
    C c {};
    A& rBase{ c };
    std::cout << rBase.getName() << '\n';

    return 0;
}
显示答案
A. 这个有点棘手。rBase 是一个指向 C 对象的 A 引用，所以 rBase.getName() 通常会调用 A::getName()。但是 A::getName() 是虚函数，所以它会调用 A 和 C 之间最派生版本的函数。而那就是 A::getName()。因为 B::getName() 和 C::getName() 不是 const，它们不被认为是重写！因此，这个程序打印 A。
1f)
#include <iostream>
#include <string_view>

class A
{
public:
	A() { std::cout << getName(); } // note addition of constructor (getName() now called from here)

	virtual std::string_view getName() const { return "A"; }
};

class B : public A
{
public:
	virtual std::string_view getName() const { return "B"; }
};

class C : public B
{
public:
	virtual std::string_view getName() const { return "C"; }
};

class D : public C
{
public:
	virtual std::string_view getName() const { return "D"; }
};

int main()
{
	C c {};

	return 0;
}
显示答案
A. 另一个棘手的例子。当我们创建一个 C 对象时，首先构造 A 部分。当调用 A 构造函数来完成此操作时，它会调用虚函数 getName()。由于类的 B 和 C 部分尚未设置，因此这会解析为 A::getName()。
下一课
25.3
override 和 final 说明符，以及协变返回类型
返回目录
上一课
25.1
指向派生对象基类的指针和引用