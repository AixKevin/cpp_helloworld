# 14.9 — 构造函数简介

14.9 — 构造函数简介
Alex
2007 年 9 月 5 日，下午 3:10 PDT
2024 年 12 月 29 日
当类类型是聚合时，我们可以使用聚合初始化直接初始化类类型
struct Foo // Foo is an aggregate
{
    int x {};
    int y {};
};

int main()
{
    Foo foo { 6, 7 }; // uses aggregate initialization

    return 0;
}
聚合初始化执行成员级初始化（成员按照它们定义的顺序进行初始化）。因此，在上面的例子中，当 `foo` 被实例化时，`foo.x` 被初始化为 `6`，`foo.y` 被初始化为 `7`。
相关内容
我们在课程
13.8 -- 结构体聚合初始化
中讨论了聚合的定义和聚合初始化。
然而，一旦我们将任何成员变量设为私有（以隐藏我们的数据），我们的类类型就不再是聚合（因为聚合不能有私有成员）。这意味着我们不再能够使用聚合初始化。
class Foo // Foo is not an aggregate (has private members)
{
    int m_x {};
    int m_y {};
};

int main()
{
    Foo foo { 6, 7 }; // compile error: can not use aggregate initialization

    return 0;
}
不允许带有私有成员的类类型通过聚合初始化进行初始化是出于多种原因的
聚合初始化需要了解类的实现（因为你必须知道成员是什么，以及它们定义的顺序），而这正是我们在隐藏数据成员时有意避免的。
如果我们的类有某种不变式，我们就会依赖用户以一种保持不变式的方式初始化类。
那么我们如何初始化一个带有私有成员变量的类呢？编译器针对上一个例子给出的错误消息提供了一个线索：“错误：没有匹配的构造函数用于初始化 'Foo'”
我们一定需要一个匹配的构造函数。但这到底是什么呢？
构造函数
**构造函数**是一个特殊的成员函数，它在非聚合类类型对象创建后自动调用。
当定义非聚合类类型对象时，编译器会查找是否存在一个可访问的构造函数，该构造函数与调用者提供的初始化值（如果有）匹配。
如果找到一个可访问的匹配构造函数，则为对象分配内存，然后调用构造函数。
如果找不到可访问的匹配构造函数，则会生成编译错误。
关键见解
许多新程序员对构造函数是否创建对象感到困惑。它们不创建对象 -- 编译器在调用构造函数之前为对象设置内存分配。然后，在未初始化的对象上调用构造函数。
然而，如果对于一组初始化器找不到匹配的构造函数，编译器将报错。因此，虽然构造函数不创建对象，但缺少匹配的构造函数将阻止对象的创建。
除了决定对象如何创建之外，构造函数通常执行两个功能
它们通常（通过成员初始化列表）执行任何成员变量的初始化
它们可能执行其他设置功能（通过构造函数体中的语句）。这可能包括错误检查初始化值，打开文件或数据库等……
构造函数执行完毕后，我们称该对象已“构建”，并且该对象现在应处于一致、可用的状态。
请注意，聚合不允许有构造函数——因此，如果您向聚合添加构造函数，它就不再是聚合。
构造函数命名
与普通成员函数不同，构造函数对命名有特定的规则
构造函数必须与类同名（大小写一致）。对于模板类，此名称不包括模板参数。
构造函数没有返回类型（甚至不是 `void`）。
由于构造函数通常是类接口的一部分，因此它们通常是 `public` 的。
一个基本构造函数示例
让我们在上面的示例中添加一个基本构造函数
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo(int x, int y) // here's our constructor function that takes two initializers
    {
        std::cout << "Foo(" << x << ", " << y << ") constructed\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo{ 6, 7 }; // calls Foo(int, int) constructor
    foo.print();

    return 0;
}
此程序现在将编译并产生结果
Foo(6, 7) constructed
Foo(0, 0)
当编译器看到定义 `Foo foo{ 6, 7 }` 时，它会寻找一个接受两个 `int` 参数的匹配 `Foo` 构造函数。`Foo(int, int)` 是一个匹配，因此编译器将允许该定义。
在运行时，当 `foo` 被实例化时，会为 `foo` 分配内存，然后调用 `Foo(int, int)` 构造函数，其中参数 `x` 初始化为 `6`，参数 `y` 初始化为 `7`。然后构造函数体的代码执行并打印 `Foo(6, 7) constructed`。
当我们调用 `print()` 成员函数时，您会注意到成员 `m_x` 和 `m_y` 的值为 0。这是因为尽管我们的 `Foo(int, int)` 构造函数被调用了，但它实际上并没有初始化成员。我们将在下一课中展示如何做到这一点。
相关内容
我们在课程
14.15 -- 类初始化和拷贝省略
中讨论了使用拷贝初始化、直接初始化和列表初始化通过构造函数初始化对象之间的区别。
构造函数参数隐式转换
在课程
10.1 -- 隐式类型转换
中，我们注意到编译器会在函数调用中（如果需要）执行参数的隐式转换，以匹配参数类型不同的函数定义
void foo(int, int)
{
}

int main()
{
    foo('a', true); // will match foo(int, int)

    return 0;
}
构造函数也是如此：`Foo(int, int)` 构造函数将匹配任何参数可隐式转换为 `int` 的调用
class Foo
{
public:
    Foo(int x, int y)
    {
    }
};

int main()
{
    Foo foo{ 'a', true }; // will match Foo(int, int) constructor

    return 0;
}
构造函数不应为 `const`
构造函数需要能够初始化正在构造的对象——因此，构造函数不得为 `const`。
#include <iostream>

class Something
{
private:
    int m_x{};

public:
    Something() // constructors must be non-const
    {
        m_x = 5; // okay to modify members in non-const constructor
    }

    int getX() const { return m_x; } // const
};

int main()
{
    const Something s{}; // const object, implicitly invokes (non-const) constructor

    std::cout << s.getX(); // prints 5
    
    return 0;
}
通常，非 `const` 成员函数不能在 `const` 对象上调用。但是，C++ 标准明确规定（根据
class.ctor.general#5
）`const` 不适用于正在构造的对象，并且只在构造函数结束后才生效。
构造函数与设置器
构造函数旨在在实例化时初始化整个对象。设置器旨在为现有对象的单个成员赋值。
下一课
14.10
构造函数成员初始化列表
返回目录
上一课
14.8
数据隐藏（封装）的好处