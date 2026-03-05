# 14.15 — 类初始化和拷贝省略

14.15 — 类初始化和拷贝省略
Alex
2016 年 6 月 5 日上午 10:49 PDT
2024 年 11 月 14 日
早在
1.4 — 变量赋值和初始化
这一课中，我们讨论了基本类型对象的 6 种基本初始化类型
int a;         // no initializer (default initialization)
int b = 5;     // initializer after equals sign (copy initialization)
int c( 6 );    // initializer in parentheses (direct initialization)

// List initialization methods (C++11)
int d { 7 };   // initializer in braces (direct list initialization)
int e = { 8 }; // initializer in braces after equals sign (copy list initialization)
int f {};      // initializer is empty braces (value initialization)
所有这些初始化类型都适用于类类型的对象
#include <iostream>

class Foo
{
public:
    
    // Default constructor
    Foo()
    {
        std::cout << "Foo()\n";
    }

    // Normal constructor
    Foo(int x)
    {
        std::cout << "Foo(int) " << x << '\n';
    }

    // Copy constructor
    Foo(const Foo&)
    {
        std::cout << "Foo(const Foo&)\n";
    }
};

int main()
{
    // Calls Foo() default constructor
    Foo f1;           // default initialization
    Foo f2{};         // value initialization (preferred)
    
    // Calls foo(int) normal constructor
    Foo f3 = 3;       // copy initialization (non-explicit constructors only)
    Foo f4(4);        // direct initialization
    Foo f5{ 5 };      // direct list initialization (preferred)
    Foo f6 = { 6 };   // copy list initialization (non-explicit constructors only)

    // Calls foo(const Foo&) copy constructor
    Foo f7 = f3;      // copy initialization
    Foo f8(f3);       // direct initialization
    Foo f9{ f3 };     // direct list initialization (preferred)
    Foo f10 = { f3 }; // copy list initialization

    return 0;
}
在现代 C++ 中，拷贝初始化、直接初始化和列表初始化本质上做的是同一件事——它们初始化一个对象。
对于所有初始化类型
当初始化类类型时，会检查该类的构造函数集，并使用重载解析来确定最佳匹配的构造函数。这可能涉及参数的隐式转换。
当初始化非类类型时，使用隐式转换规则来确定是否存在隐式转换。
关键见解
初始化形式之间有三个主要区别
列表初始化不允许窄化转换。
拷贝初始化只考虑非显式构造函数/转换函数。我们将在
14.16 — 转换构造函数和 explicit 关键字
这一课中介绍。
列表初始化优先匹配列表构造函数，而不是其他匹配的构造函数。我们将在
16.2 — std::vector 和列表构造函数简介
这一课中介绍。
还需要注意的是，在某些情况下，某些形式的初始化是不允许的（例如，在构造函数成员初始化列表中，我们只能使用直接形式的初始化，不能使用拷贝初始化）。
不必要的拷贝
考虑这个简单的程序
#include <iostream>

class Something
{
    int m_x{};

public:
    Something(int x)
        : m_x{ x }
    {
        std::cout << "Normal constructor\n";
    }

    Something(const Something& s)
        : m_x { s.m_x }
    {
        std::cout << "Copy constructor\n";
    }

    void print() const { std::cout << "Something(" << m_x << ")\n"; }
};

int main()
{
    Something s { Something { 5 } }; // focus on this line
    s.print();

    return 0;
}
在上述变量
s
的初始化中，我们首先构造一个临时
Something
，用值
5
初始化（它使用
Something(int)
构造函数）。然后，这个临时对象用于初始化
s
。因为临时对象和
s
具有相同的类型（它们都是
Something
对象），所以
Something(const Something&)
拷贝构造函数通常会在这里被调用，将临时对象中的值拷贝到
s
中。最终结果是
s
用值
5
初始化。
在没有任何优化的情况下，上述程序会打印
Normal constructor
Copy constructor
Something(5)
然而，这个程序效率低下，因为我们必须进行两次构造函数调用：一次是
Something(int)
，一次是
Something(const Something&)
。请注意，上述结果与我们直接编写以下代码相同
Something s { 5 }; // only invokes Something(int), no copy constructor
这个版本产生相同的结果，但效率更高，因为它只调用了
Something(int)
（不需要拷贝构造函数）。
拷贝省略
由于编译器可以自由地重写语句以进行优化，人们可能会想，编译器是否可以优化掉不必要的拷贝，将
Something s { Something{5} };
视为我们一开始就写了
Something s { 5 }
。
答案是肯定的，这个过程被称为
拷贝省略
。
拷贝省略
是一种编译器优化技术，允许编译器移除不必要的对象拷贝。换句话说，在编译器通常会调用拷贝构造函数的情况下，编译器可以自由地重写代码以完全避免调用拷贝构造函数。当编译器优化掉对拷贝构造函数的调用时，我们称该构造函数已被
省略
。
与其他类型的优化不同，拷贝省略不受“as-if”规则的约束。也就是说，即使拷贝构造函数有副作用（例如向控制台打印文本！），也允许进行拷贝省略！这就是为什么拷贝构造函数除了拷贝之外不应该有副作用——如果编译器省略了对拷贝构造函数的调用，副作用就不会执行，程序的可见行为就会改变！
相关内容
我们在
5.4 — as-if 规则和编译时优化
这一课中讨论了 as-if 规则。
我们可以在上面的例子中看到这一点。如果您在 C++17 编译器上运行该程序，它将产生以下结果
Normal constructor
Something(5)
编译器为了避免不必要的拷贝，省略了拷贝构造函数，因此，打印“Copy constructor”的语句没有执行！由于拷贝省略，我们程序的可见行为发生了变化！
传值和返回值中的拷贝省略
当同类型参数按值传递或使用返回值时，通常会调用拷贝构造函数。然而，在某些情况下，这些拷贝可能会被省略。以下程序演示了其中一些情况
#include <iostream>

class Something
{
public:
	Something() = default;
	Something(const Something&)
	{
		std::cout << "Copy constructor called\n";
	}
};

Something rvo()
{
	return Something{}; // calls Something() and copy constructor
}

Something nrvo()
{
	Something s{}; // calls Something()
	return s;      // calls copy constructor
}

int main()
{
	std::cout << "Initializing s1\n";
	Something s1 { rvo() }; // calls copy constructor

	std::cout << "Initializing s2\n";
	Something s2 { nrvo() }; // calls copy constructor

        return 0;
}
在 C++14 或更早的版本中，如果禁用拷贝省略，上述程序将调用拷贝构造函数 4 次
一次是在
rvo
将
Something
返回到
main
时。
一次是在
rvo()
的返回值用于初始化
s1
时。
一次是在
nrvo
将
s
返回到
main
时。
一次是在
nrvo()
的返回值用于初始化
s2
时。
然而，由于拷贝省略，您的编译器很可能会省略这些拷贝构造函数调用的绝大部分或全部。Visual Studio 2022 省略了 3 种情况（它不省略
nrvo()
返回值的情况），而 GCC 则省略了全部 4 种情况。
记住编译器何时执行/不执行拷贝省略并不重要。只需知道它是一种您的编译器在可能的情况下会执行的优化。如果您期望看到拷贝构造函数被调用而它没有被调用，那么拷贝省略很可能是原因。
C++17 中强制拷贝省略
C++17
在 C++17 之前，拷贝省略严格来说是一种可选的编译器优化。在 C++17 中，拷贝省略在某些情况下成为强制性的。在这些情况下，拷贝省略将自动执行（即使您告诉编译器不要执行拷贝省略）。
在 C++17 或更新的版本中运行上述相同示例时，当
rvo()
返回以及
s1
使用该值初始化时，本应发生的拷贝构造函数调用被要求省略。使用
nvro()
初始化
s2
并非强制省略情况，因此此处发生的 2 次拷贝构造函数调用可能或可能不会被省略，具体取决于您的编译器和优化设置。
在可选省略的情况下，必须存在一个可访问的拷贝构造函数（例如，未被删除），即使实际对拷贝构造函数的调用被省略了。
在强制省略的情况下，无需提供可访问的拷贝构造函数（换句话说，即使拷贝构造函数被删除，强制省略也可以发生）。
致进阶读者
在未执行可选拷贝省略的情况下，移动语义仍可能允许对象被移动而非拷贝。我们在
16.5 — 返回 std::vector 和移动语义简介
这一课中介绍了移动语义。
下一课
14.16
转换构造函数和 explicit 关键字
返回目录
上一课
14.14
拷贝构造函数简介