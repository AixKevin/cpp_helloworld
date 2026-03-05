# 25.4 — 虚析构函数、虚赋值和重写虚拟化

25.4 — 虚析构函数、虚赋值和重写虚拟化
Alex
2008年2月1日，下午1:50 PST
2024年10月18日
虚析构函数
尽管如果您不提供析构函数，C++ 会为您的类提供一个默认析构函数，但有时您会希望提供自己的析构函数（特别是当类需要释放内存时）。如果您正在处理继承，则应**始终**将析构函数设为虚函数。请考虑以下示例
#include <iostream>
class Base
{
public:
    ~Base() // note: not virtual
    {
        std::cout << "Calling ~Base()\n";
    }
};

class Derived: public Base
{
private:
    int* m_array {};

public:
    Derived(int length)
      : m_array{ new int[length] }
    {
    }

    ~Derived() // note: not virtual (your compiler may warn you about this)
    {
        std::cout << "Calling ~Derived()\n";
        delete[] m_array;
    }
};

int main()
{
    Derived* derived { new Derived(5) };
    Base* base { derived };

    delete base;

    return 0;
}
注意：如果您编译上述示例，您的编译器可能会警告您非虚析构函数（这在此示例中是故意的）。您可能需要禁用将警告视为错误的编译器标志才能继续。
由于 base 是一个 Base 指针，当 base 被删除时，程序会查找 Base 析构函数是否是虚函数。它不是，所以它假定只需要调用 Base 析构函数。我们可以从上面的示例输出中看到这一点：
Calling ~Base()
但是，我们确实希望 delete 函数调用 Derived 的析构函数（这会反过来调用 Base 的析构函数），否则 m_array 将不会被删除。我们通过使 Base 的析构函数成为虚函数来实现这一点：
#include <iostream>
class Base
{
public:
    virtual ~Base() // note: virtual
    {
        std::cout << "Calling ~Base()\n";
    }
};

class Derived: public Base
{
private:
    int* m_array {};

public:
    Derived(int length)
      : m_array{ new int[length] }
    {
    }

    virtual ~Derived() // note: virtual
    {
        std::cout << "Calling ~Derived()\n";
        delete[] m_array;
    }
};

int main()
{
    Derived* derived { new Derived(5) };
    Base* base { derived };

    delete base;

    return 0;
}
现在这个程序产生以下结果：
Calling ~Derived()
Calling ~Base()
规则
每当您处理继承时，您都应该将任何显式析构函数设为虚函数。
与普通虚成员函数一样，如果基类函数是虚函数，则所有派生类的重写都将被视为虚函数，无论它们是否被指定为虚函数。没有必要为了将其标记为虚函数而创建一个空的派生类析构函数。
请注意，如果您希望基类有一个虚析构函数，而该析构函数本身是空的，则可以这样定义析构函数：
virtual ~Base() = default; // generate a virtual default destructor
虚赋值
可以将赋值运算符设为虚函数。然而，与析构函数的情况（虚拟化总是一个好主意）不同，将赋值运算符虚拟化会带来一大堆问题，并涉及到本教程范围之外的一些高级主题。因此，为了简洁起见，我们建议您暂时将赋值设为非虚函数。
忽略虚拟化
极少数情况下，您可能希望忽略函数的虚拟化。例如，请考虑以下代码：
#include <string_view>
class Base
{
public:
    virtual ~Base() = default;
    virtual std::string_view getName() const { return "Base"; }
};

class Derived: public Base
{
public:
    virtual std::string_view getName() const { return "Derived"; }
};
在某些情况下，您可能希望指向 Derived 对象的 Base 指针调用 Base::getName() 而不是 Derived::getName()。为此，只需使用作用域解析运算符即可：
#include <iostream>
int main()
{
    Derived derived {};
    const Base& base { derived };

    // Calls Base::getName() instead of the virtualized Derived::getName()
    std::cout << base.Base::getName() << '\n';

    return 0;
}
您可能不会经常使用它，但知道它至少是可能的很好。
我们应该把所有的析构函数都设为虚函数吗？
这是新手程序员常问的问题。如上面的示例所示，如果基类析构函数未标记为虚函数，那么如果程序员后来删除了指向派生对象的基类指针，程序就有内存泄漏的风险。避免这种情况的一种方法是将所有析构函数标记为虚函数。但是您应该这样做吗？
很容易说“是”，这样以后就可以将任何类用作基类——但是这样做会有性能损失（每个类实例都会添加一个虚指针）。所以您必须权衡这个成本，以及您的意图。
我们建议如下：如果一个类没有明确设计为基类，那么通常最好不要有虚成员和虚析构函数。该类仍然可以通过组合使用。如果一个类被设计为用作基类和/或有任何虚函数，那么它应该始终有一个虚析构函数。
如果决定一个类不可继承，那么下一个问题是如何强制执行此决定。
传统观点（最初由备受推崇的 C++ 大师 Herb Sutter 提出）建议避免非虚析构函数内存泄漏情况，如下所示：“基类析构函数应该是 public 和虚函数，或者是 protected 和非虚函数。”带有 protected 析构函数的基类不能使用基类指针删除，这可以防止通过基类指针删除派生类对象。
不幸的是，这也阻止了公众对基类析构函数的**任何**使用。这意味着
我们不应该动态分配基类对象，因为我们没有常规方法来删除它们（有一些非常规的解决方法，但很糟糕）。
我们甚至不能静态分配基类对象，因为当它们超出作用域时，析构函数是不可访问的。
换句话说，使用这种方法，为了使派生类安全，我们必须使基类本身几乎无法使用。
现在语言中引入了 `final` 关键字，我们的建议如下：
如果您打算从您的类继承，请确保您的析构函数是虚函数且是公有的。
如果您不打算从您的类继承，请将您的类标记为 final。这将首先阻止其他类继承它，而不会对类本身施加任何其他使用限制。
下一课
25.5
早期绑定和后期绑定
返回目录
上一课
25.3
override 和 final 关键字，以及协变返回类型