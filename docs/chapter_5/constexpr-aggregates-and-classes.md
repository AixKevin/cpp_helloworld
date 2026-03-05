# 14.17 — Constexpr 聚合体和类

14.17 — Constexpr 聚合体和类
Alex
2024 年 5 月 22 日下午 4:43 (太平洋夏令时)
2025 年 1 月 29 日
在课程
F.1 -- Constexpr 函数
中，我们介绍了 constexpr 函数，这些函数可以在编译时或运行时进行评估。例如
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    std::cout << greater(5, 6) << '\n'; // greater(5, 6) may be evaluated at compile-time or runtime

    constexpr int g { greater(5, 6) };  // greater(5, 6) must be evaluated at compile-time
    std::cout << g << '\n';             // prints 6

    return 0;
}
在此示例中，
greater()
是一个 constexpr 函数，而
greater(5, 6)
是一个常量表达式，它可以在编译时或运行时进行评估。由于
std::cout << greater(5, 6)
在非 constexpr 上下文中调用
greater(5, 6)
，因此编译器可以自由选择是在编译时还是运行时评估
greater(5, 6)
。当
greater(5, 6)
用于初始化 constexpr 变量
g
时，
greater(5, 6)
在 constexpr 上下文中被调用，并且必须在编译时进行评估。
现在考虑以下类似示例
#include <iostream>

struct Pair
{
    int m_x {};
    int m_y {};

    int greater() const
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

int main()
{
    Pair p { 5, 6 };                  // inputs are constexpr values
    std::cout << p.greater() << '\n'; // p.greater() evaluates at runtime

    constexpr int g { p.greater() };  // compile error: greater() not constexpr
    std::cout << g << '\n';

    return 0;
}
在此版本中，我们有一个名为
Pair
的聚合结构体，而
greater()
现在是一个成员函数。但是，由于成员函数
greater()
不是 constexpr，因此
p.greater()
不是常量表达式。当
std::cout << p.greater()
调用
p.greater()
（在非 constexpr 上下文中）时，
p.greater()
将在运行时进行评估。但是，当我们尝试使用
p.greater()
初始化 constexpr 变量
g
时，我们会得到一个编译错误，因为
p.greater()
无法在编译时进行评估。
由于
p
的输入是 constexpr 值（
5
和
6
），因此
p.greater()
似乎应该能够在编译时进行评估。但是我们如何做到这一点呢？
Constexpr 成员函数
就像非成员函数一样，成员函数可以通过使用
constexpr
关键字使其成为 constexpr。Constexpr 成员函数可以在编译时或运行时进行评估。
#include <iostream>

struct Pair
{
    int m_x {};
    int m_y {};

    constexpr int greater() const // can evaluate at either compile-time or runtime
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

int main()
{
    Pair p { 5, 6 };
    std::cout << p.greater() << '\n'; // okay: p.greater() evaluates at runtime

    constexpr int g { p.greater() };  // compile error: p not constexpr
    std::cout << g << '\n';

    return 0;
}
在此示例中，我们将
greater()
设为 constexpr 函数，因此编译器可以在运行时或编译时对其进行评估。
当我们在运行时表达式
std::cout << p.greater()
中调用
p.greater()
时，它在运行时进行评估。
但是，当
p.greater()
用于初始化 constexpr 变量
g
时，我们会得到一个编译错误。尽管
greater()
现在是 constexpr，但
p
仍然不是 constexpr，因此
p.greater()
不是常量表达式。
Constexpr 聚合体
好的，如果我们需要
p
是 constexpr，那么我们只需将其设为 constexpr
#include <iostream>

struct Pair // Pair is an aggregate
{
    int m_x {};
    int m_y {};

    constexpr int greater() const
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

int main()
{
    constexpr Pair p { 5, 6 };        // now constexpr
    std::cout << p.greater() << '\n'; // p.greater() evaluates at runtime or compile-time

    constexpr int g { p.greater() };  // p.greater() must evaluate at compile-time
    std::cout << g << '\n';

    return 0;
}
由于
Pair
是一个聚合体，并且聚合体隐式支持 constexpr，因此我们完成了。这可行！由于
p
是一个 constexpr 类型，并且
greater()
是一个 constexpr 成员函数，因此
p.greater()
是一个常量表达式，并且可以在只允许常量表达式的地方使用。
相关内容
我们在课程
13.8 -- 结构体聚合初始化
中介绍了聚合体。
Constexpr 类对象和 constexpr 构造函数
现在让我们将
Pair
设为非聚合体
#include <iostream>

class Pair // Pair is no longer an aggregate
{
private:
    int m_x {};
    int m_y {};

public:
    Pair(int x, int y): m_x { x }, m_y { y } {}

    constexpr int greater() const
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

int main()
{
    constexpr Pair p { 5, 6 };       // compile error: p is not a literal type
    std::cout << p.greater() << '\n';

    constexpr int g { p.greater() };
    std::cout << g << '\n';

    return 0;
}
此示例与上一个示例几乎相同，只是
Pair
不再是聚合体（因为它具有私有数据成员和构造函数）。
当我们编译此程序时，我们得到一个关于
Pair
不是“字面类型”的编译错误。这是什么意思？
在 C++ 中，**字面类型**是任何可能在常量表达式中创建对象的类型。换句话说，除非类型符合字面类型，否则对象不能是 constexpr。而我们的非聚合
Pair
不符合。
命名法
字面量和字面类型是不同的（但相关）事物。字面量是插入到源代码中的 constexpr 值。字面类型是可以作为 constexpr 值的类型的类型。字面量总是具有字面类型。但是，具有字面类型的值或对象不一定是字面量。
字面类型的定义很复杂，可以在
cppreference
上找到摘要。但是，值得注意的是，字面类型包括
标量类型（持有单个值，例如基本类型和指针）
引用类型
大多数聚合体
具有 constexpr 构造函数的类
现在我们明白了为什么我们的
Pair
不是字面类型。当实例化类对象时，编译器将调用构造函数来初始化对象。而我们
Pair
类中的构造函数不是 constexpr，因此它不能在编译时被调用。因此，
Pair
对象不能是 constexpr。
解决此问题的方法很简单：我们只需将构造函数也设为
constexpr
#include <iostream>

class Pair
{
private:
    int m_x {};
    int m_y {};

public:
    constexpr Pair(int x, int y): m_x { x }, m_y { y } {} // now constexpr

    constexpr int greater() const
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

int main()
{
    constexpr Pair p { 5, 6 };
    std::cout << p.greater() << '\n';

    constexpr int g { p.greater() };
    std::cout << g << '\n';

    return 0;
}
这按预期工作，就像我们聚合体版本的
Pair
一样。
最佳实践
如果您希望您的类能够在编译时进行评估，请将您的成员函数和构造函数设为 constexpr。
隐式定义的构造函数如果是 constexpr，则可以这样定义。显式默认的构造函数必须显式定义为 constexpr。
提示
Constexpr 是类接口的一部分，以后删除它会破坏在常量上下文中调用该函数的调用者。
非 constexpr/非 const 对象可能需要 constexpr 成员
在上面的示例中，由于 constexpr 变量
g
的初始化程序必须是常量表达式，因此很明显
p.greater()
必须是常量表达式，因此
p
、
Pair
构造函数和
greater()
都必须是 constexpr。
但是，如果我们将
p.greater()
替换为 constexpr 函数，事情就会变得不那么明显
#include <iostream>

class Pair
{
private:
    int m_x {};
    int m_y {};

public:
    constexpr Pair(int x, int y): m_x { x }, m_y { y } {}

    constexpr int greater() const
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

constexpr int init()
{
    Pair p { 5, 6 };    // requires constructor to be constexpr when evaluated at compile-time
    return p.greater(); // requires greater() to be constexpr when evaluated at compile-time
}

int main()
{
    constexpr int g { init() }; // init() evaluated in compile-time context
    std::cout << g << '\n';

    return 0;
}
请记住，constexpr 函数可以在运行时或编译时进行评估。当 constexpr 函数在编译时进行评估时，它只能调用能够在编译时进行评估的函数。对于类类型，这意味着 constexpr 成员函数。
由于
g
是 constexpr，因此
init()
必须在编译时进行评估。在
init()
函数中，我们将
p
定义为非 constexpr/非 const（因为我们可以，而不是因为我们应该）。尽管
p
没有定义为 constexpr，但
p
仍然需要在编译时创建，因此需要一个 constexpr
Pair
构造函数。同样，为了使
p.greater()
在编译时进行评估，
greater()
必须是 constexpr 成员函数。如果
Pair
构造函数或
greater()
不是 constexpr，编译器就会出错。
关键见解
当 constexpr 函数在编译时上下文中进行评估时，只能调用 constexpr 函数。
Constexpr 成员函数可以是 const 或非 const
C++14
在 C++11 中，非静态 constexpr 成员函数隐式是 const（构造函数除外）。
然而，从 C++14 开始，constexpr 成员函数不再隐式是 const。这意味着如果您希望 constexpr 函数是 const 函数，则必须明确将其标记为 const。
Constexpr 非 const 成员函数可以更改数据成员
可选
Constexpr 非 const 成员函数可以更改类的数据成员，只要隐式对象不是 const。即使函数在编译时进行评估，这也是如此。
这是一个为此目的而设计的例子
#include <iostream>

class Pair
{
private:
    int m_x {};
    int m_y {};

public:
    constexpr Pair(int x, int y): m_x { x }, m_y { y } {}

    constexpr int greater() const // constexpr and const
    {
        return (m_x > m_y  ? m_x : m_y);
    }

    constexpr void reset() // constexpr but non-const
    {
        m_x = m_y = 0; // non-const member function can change members
    }

    constexpr const int& getX() const { return m_x; }
};

// This function is constexpr
constexpr Pair zero()
{
    Pair p { 1, 2 }; // p is non-const
    p.reset();       // okay to call non-const member function on non-const object
    return p;
}

int main()
{
    Pair p1 { 3, 4 };
    p1.reset();                     // okay to call non-const member function on non-const object
    std::cout << p1.getX() << '\n'; // prints 0
    
    Pair p2 { zero() };             // zero() will be evaluated at runtime
    p2.reset();                     // okay to call non-const member function on non-const object
    std::cout << p2.getX() << '\n'; // prints 0

    constexpr Pair p3 { zero() };   // zero() will be evaluated at compile-time
//    p3.reset();                   // Compile error: can't call non-const member function on const object
    std::cout << p3.getX() << '\n'; // prints 0

    return 0;
}
当我们分析此示例时，请记住
非 const 成员函数可以修改非 const 对象的成员。
constexpr 成员函数可以在运行时上下文或编译时上下文调用。
这两件事独立工作。
在
p1
的情况下，
p1
是非 const 的。因此，我们允许调用非 const 成员函数
p1.reset()
来修改
p1
。
reset()
是 constexpr 的事实在这里无关紧要，因为我们所做的任何事情都不需要编译时评估。
p2
的情况类似。在这种情况下，
p2
的初始化器是对
zero()
的函数调用。即使
zero()
是一个 constexpr 函数，在这种情况下它是在运行时上下文中调用的，并且行为就像一个普通函数。在
zero()
内部，我们实例化非 const
p
，在其上调用非 const 成员函数
p.reset()
，然后返回
p
。返回的
Pair
用作
p2
的初始化器。
zero()
和
reset()
是 constexpr 的事实在这种情况下无关紧要，因为我们所做的任何事情都不需要编译时评估。
p3
的情况才有趣。因为
p3
是 constexpr，所以它必须有一个常量表达式初始化器。因此，对
zero()
的此调用必须在编译时进行评估。并且由于我们正在编译时上下文中进行评估，因此我们只能调用 constexpr 函数。在
zero()
内部，
p
是非 const 的（这是允许的，即使我们在编译时进行评估）。但是，因为我们处于编译时上下文，所以用于创建
p
的构造函数必须是 constexpr。就像
p2
的情况一样，我们被允许在非 const 对象
p
上调用非 const 成员函数
p.reset()
。但是因为我们处于编译时上下文，所以
reset()
成员函数必须是 constexpr。然后函数返回
p
，它用于初始化
p3
。
作者注
是的，我们使用了一个非 const 对象来初始化一个 constexpr 对象。如果这让您感到困惑，那可能是因为您尚未完全区分 const 和 constexpr。
没有要求 constexpr 变量必须用 const 值初始化。这可能看起来是这样，因为大多数时候我们使用字面量（它们是 const）或其他 constexpr 变量（它们隐式是 const）来初始化 constexpr 变量，并且因为术语
const
和
constexpr
的名称相似。
实际要求是 constexpr 变量必须用常量表达式初始化。对于函数（和运算符），constexpr 不意味着 const，并且 constexpr 函数（和运算符）可以使用非 const 对象甚至返回它们。
重要的是它不是 const，而是编译器可以在编译时确定对象的值。在 constexpr 函数的情况下，即使它们返回非 const 对象，这也是可能的！
返回 const 引用（或指针）的 constexpr 函数
可选
通常您不会看到
constexpr
和
const
紧挨着使用，但这种情况确实发生的一种情况是当您有一个返回 const 引用（或（const）指向 const 的指针）的 constexpr 成员函数时。
在上面的
Pair
类中，
getX()
是一个返回 const 引用的 constexpr 成员函数
constexpr const int& getX() const { return m_x; }
这有很多 const-ing！
constexpr
表示成员函数可以在编译时进行评估。
const int&
是函数的返回类型。最右边的
const
意味着成员函数本身是 const，因此可以在 const 对象上调用。
题外话…
返回指向 const 的 const 指针的成员函数可能看起来像这样
constexpr const int* const getXPtr() const { return &m_x; }
它不漂亮吗？不？好吧，那就算了。
下一课
14.x
第 14 章总结与测验
返回目录
上一课
14.16
转换构造函数和 explicit 关键字