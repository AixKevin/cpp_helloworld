# 25.6 — 虚表

25.6 — 虚表
Alex
2008 年 2 月 8 日，下午 3:29 PST
2024 年 12 月 7 日
考虑以下程序
#include <iostream>
#include <string_view>

class Base
{
public:
    std::string_view getName() const { return "Base"; }                // not virtual
    virtual std::string_view getNameVirtual() const { return "Base"; } // virtual
};

class Derived: public Base
{
public:
    std::string_view getName() const { return "Derived"; }
    virtual std::string_view getNameVirtual() const override { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& base { derived };

    std::cout << "base has static type " << base.getName() << '\n';
    std::cout << "base has dynamic type " << base.getNameVirtual() << '\n';

    return 0;
}
首先，我们来看一下对
base.getName()
的调用。由于这是一个非虚函数，编译器可以使用
base
的实际类型（
Base
）在编译时确定它应该解析为
Base::getName()
。
尽管看起来几乎相同，但对
base.getNameVirtual()
的调用必须以不同的方式解析。由于这是一个虚函数调用，编译器必须使用
base
的动态类型来解析调用，而
base
的动态类型在运行时之前是不可知的。因此，只有在运行时才能确定对
base.getNameVirtual()
的此特定调用解析为
Derived::getNameVirtual()
，而不是
Base::getNameVirtual()
。
那么虚函数究竟是如何工作的呢？
虚表
C++ 标准没有规定虚函数应该如何实现（这个细节留给了实现）。
然而，C++ 实现通常使用一种称为虚表的后期绑定形式来实现虚函数。
虚表
是一个函数查找表，用于以动态/后期绑定的方式解析函数调用。虚表有时也被称为“vtable”、“虚函数表”、“虚方法表”或“调度表”。在 C++ 中，虚函数解析有时被称为
动态调度
。
命名法
以下是 C++ 中更简单的理解方式
早期绑定/静态调度 = 直接函数调用重载解析
后期绑定 = 间接函数调用解析
动态调度 = 虚函数覆盖解析
因为了解虚表的工作原理对于使用虚函数并不是必需的，所以本节可以视为可选阅读。
虚表实际上非常简单，尽管用文字描述起来有点复杂。首先，每个使用虚函数（或派生自使用虚函数的类）的类都有一个相应的虚表。这个表只是一个编译器在编译时设置的静态数组。虚表包含该类对象可以调用的每个虚函数的一个条目。此表中的每个条目都只是一个函数指针，指向该类可访问的最派生函数。
其次，编译器还会添加一个隐藏指针，它是基类的一个成员，我们称之为
*__vptr
。当创建类对象时，
*__vptr
会自动设置，使其指向该类的虚表。与
this
指针不同，
this
指针实际上是编译器用于解析自引用的函数参数，而
*__vptr
是一个真实的指针成员。因此，它使分配的每个类对象的大小增加了一个指针的大小。这也意味着
*__vptr
被派生类继承，这一点很重要。
现在，你可能对这些东西是如何组合在一起的感到困惑，所以让我们看一个简单的例子
class Base
{
public:
    virtual void function1() {};
    virtual void function2() {};
};

class D1: public Base
{
public:
    void function1() override {};
};

class D2: public Base
{
public:
    void function2() override {};
};
因为这里有 3 个类，所以编译器将设置 3 个虚表：一个用于 Base，一个用于 D1，一个用于 D2。
编译器还会向使用虚函数的最基类添加一个隐藏的指针成员。尽管编译器会自动执行此操作，但我们将在下一个示例中将其放入，以显示它添加的位置
class Base
{
public:
    VirtualTable* __vptr;
    virtual void function1() {};
    virtual void function2() {};
};

class D1: public Base
{
public:
    void function1() override {};
};

class D2: public Base
{
public:
    void function2() override {};
};
当创建类对象时，
*__vptr
会被设置为指向该类的虚表。例如，当创建 Base 类型的对象时，
*__vptr
会被设置为指向 Base 的虚表。当构造 D1 或 D2 类型的对象时，
*__vptr
会分别被设置为指向 D1 或 D2 的虚表。
现在，我们来谈谈这些虚表是如何填充的。由于这里只有两个虚函数，每个虚表将有两个条目（一个用于 function1()，一个用于 function2()）。请记住，当填充这些虚表时，每个条目都会填充该类类型对象可以调用的最派生函数。
Base 对象的虚表很简单。Base 类型的对象只能访问 Base 的成员。Base 无法访问 D1 或 D2 函数。因此，function1 的条目指向 Base::function1()，function2 的条目指向 Base::function2()。
D1 的虚表稍微复杂一些。D1 类型的对象可以访问 D1 和 Base 的成员。但是，D1 已经覆盖了 function1()，使得 D1::function1() 比 Base::function1() 更派生。因此，function1 的条目指向 D1::function1()。D1 没有覆盖 function2()，所以 function2 的条目将指向 Base::function2()。
D2 的虚表与 D1 类似，只是 function1 的条目指向 Base::function1()，function2 的条目指向 D2::function2()。
这是图形化的图片
尽管此图看起来有点疯狂，但它实际上非常简单：每个类中的
*__vptr
指向该类的虚表。虚表中的条目指向该类对象允许调用的函数的最派生版本。
所以考虑一下当我们创建一个 D1 类型的对象时会发生什么
int main()
{
    D1 d1 {};
}
因为 d1 是一个 D1 对象，所以 d1 的 *__vptr 被设置为 D1 虚表。
现在，我们将基指针设置为 D1
int main()
{
    D1 d1 {};
    Base* dPtr = &d1;

    return 0;
}
请注意，由于 dPtr 是一个基指针，它只指向 d1 的 Base 部分。但是，还要注意
*__vptr
位于类的 Base 部分，因此 dPtr 可以访问此指针。最后，请注意
dPtr->__vptr
指向 D1 虚表！因此，即使 dPtr 的类型是
Base*
，它仍然可以访问 D1 的虚表（通过
__vptr
）。
那么当我们尝试调用 dPtr->function1() 时会发生什么？
int main()
{
    D1 d1 {};
    Base* dPtr = &d1;
    dPtr->function1();

    return 0;
}
首先，程序识别 function1() 是一个虚函数。其次，程序使用
dPtr->__vptr
来获取 D1 的虚表。第三，它在 D1 的虚表中查找要调用的 function1() 的哪个版本。这已设置为 D1::function1()。因此，
dPtr->function1()
解析为 D1::function1()！
现在，你可能会说：“但是如果 dPtr 真的指向一个 Base 对象而不是 D1 对象呢？它还会调用 D1::function1() 吗？”答案是不会。
int main()
{
    Base b {};
    Base* bPtr = &b;
    bPtr->function1();

    return 0;
}
在这种情况下，当创建 b 时，b.__vptr 指向 Base 的虚表，而不是 D1 的虚表。由于 bPtr 指向 b，因此
bPtr->__vptr
也指向 Base 的虚表。Base 的虚表中 function1() 的条目指向 Base::function1()。因此，
bPtr->function1()
解析为 Base::function1()，这是 Base 对象应该能够调用的 function1() 的最派生版本。
通过使用这些表，编译器和程序能够确保函数调用解析为适当的虚函数，即使你只使用指向基类的指针或引用！
调用虚函数比调用非虚函数要慢，原因有几个：首先，我们必须使用
*__vptr
来获取相应的虚表。其次，我们必须索引虚表以找到要调用的正确函数。只有这样才能调用函数。结果是，我们必须执行 3 次操作才能找到要调用的函数，而正常间接函数调用需要 2 次操作，直接函数调用需要 1 次操作。然而，对于现代计算机来说，这种增加的时间通常相当微不足道。
另外提醒一下，任何使用虚函数的类都有一个
*__vptr
，因此该类的每个对象都会大一个指针。虚函数功能强大，但它们确实会带来性能开销。
下一课
25.7
纯虚函数、抽象基类和接口类
返回目录
上一课
25.5
早期绑定和后期绑定