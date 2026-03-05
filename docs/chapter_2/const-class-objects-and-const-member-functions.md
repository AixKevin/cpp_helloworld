# 14.4 — Const 类对象和 const 成员函数

14.4 — Const 类对象和 const 成员函数
Alex
2007 年 9 月 11 日下午 6:19 (太平洋夏令时)
2025 年 2 月 12 日
在课程
5.1 -- 常量变量（命名常量）
中，您了解到基本数据类型（
int
、
double
、
char
等）的对象可以通过
const
关键字设置为常量。所有常量变量必须在创建时初始化。
const int x;      // compile error: not initialized
const int y{};    // ok: value initialized
const int z{ 5 }; // ok: list initialized
类似地，类类型对象（结构体、类和联合体）也可以通过使用
const
关键字设置为常量。这类对象也必须在创建时初始化。
struct Date
{
    int year {};
    int month {};
    int day {};
};

int main()
{
    const Date today { 2020, 10, 14 }; // const class type object

    return 0;
}
就像普通变量一样，当您需要确保类类型对象在创建后不被修改时，通常会将其设置为常量（或 constexpr）。
禁止修改 const 对象的数据成员
一旦 const 类类型对象被初始化，任何尝试修改该对象数据成员的操作都是被禁止的，因为这会违反对象的 const 属性。这包括直接更改成员变量（如果它们是公有的），或调用设置成员变量值的成员函数。
struct Date
{
    int year {};
    int month {};
    int day {};

    void incrementDay()
    {
        ++day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.day += 1;        // compile error: can't modify member of const object
    today.incrementDay();  // compile error: can't call member function that modifies member of const object

    return 0;
}
Const 对象不能调用非 const 成员函数
您可能会惊讶地发现这段代码也会导致编译错误
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print()
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.print();  // compile error: can't call non-const member function

    return 0;
}
尽管
print()
没有尝试修改成员变量，但我们对
today.print()
的调用仍然违反了 const 属性。发生这种情况是因为
print()
成员函数本身没有被声明为 const。编译器不允许我们对 const 对象调用非 const 成员函数。
Const 成员函数
为了解决上述问题，我们需要将
print()
设为 const 成员函数。一个
const 成员函数
是一个保证不会修改对象或调用任何非 const 成员函数（因为它们可能会修改对象）的成员函数。
将
print()
设为 const 成员函数很简单——我们只需在函数原型中，参数列表之后，函数体之前，附加
const
关键字
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // now a const member function
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.print();  // ok: const object can call const member function

    return 0;
}
在上面的例子中，
print()
被设为 const 成员函数，这意味着我们可以在 const 对象（如
today
）上调用它。
致进阶读者
对于在类定义之外定义的成员函数，
const
关键字必须在类定义中的函数声明和类定义之外的函数定义上都使用。我们在课程
15.2 -- 类和头文件
中展示了这一点的一个例子。
构造函数不能被设为 const，因为它们需要初始化对象的成员，这需要修改它们。我们在课程
14.9 -- 构造函数简介
中介绍构造函数。
一个尝试更改数据成员或调用非 const 成员函数的 const 成员函数将导致编译错误。例如
struct Date
{
    int year {};
    int month {};
    int day {};

    void incrementDay() const // made const
    {
        ++day; // compile error: const function can't modify member
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.incrementDay();

    return 0;
}
在这个例子中，
incrementDay()
已被标记为 const 成员函数，但它试图改变
day
。这将导致编译错误。
const 成员函数可以像往常一样修改非成员（如局部变量和函数参数）并调用非成员函数。const 仅适用于成员。
关键见解
一个 const 成员函数不能：修改隐式对象，调用非 const 成员函数。
一个 const 成员函数可以：修改非隐式对象，调用 const 成员函数，调用非成员函数。
Const 成员函数可以在非 const 对象上调用
const 成员函数也可以在非 const 对象上调用
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // non-const

    today.print();  // ok: can call const member function on non-const object

    return 0;
}
因为 const 成员函数可以在 const 和非 const 对象上调用，所以如果一个成员函数不修改对象的状态，它应该被设为 const。
最佳实践
一个不（也永远不会）修改对象状态的成员函数应该被设为 const，这样它就可以在 const 和非 const 对象上调用。
请注意您将
const
应用于哪些成员函数。一旦一个成员函数被设为 const，该函数就可以在 const 对象上调用。稍后移除成员函数上的
const
将破坏任何在 const 对象上调用该成员函数的代码。
通过 const 引用传递的 const 对象
尽管实例化 const 局部变量是创建 const 对象的一种方式，但获得 const 对象的更常见方式是通过 const 引用将对象传递给函数。
在课程
12.5 -- 通过左值引用传递
中，我们讨论了通过 const 引用而不是通过值传递类类型参数的优点。回顾一下，通过值传递类类型参数会导致类的一个副本被创建（这很慢）——大多数时候，我们不需要副本，对原始参数的引用就很好，并避免了创建副本。我们通常将引用设为 const，以允许函数接受 const 左值参数和右值参数（例如字面量和临时对象）。
你能找出下面代码有什么问题吗？
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() // non-const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

void doSomething(const Date& date)
{
    date.print();
}

int main()
{
    Date today { 2020, 10, 14 }; // non-const
    today.print();

    doSomething(today);

    return 0;
}
答案是，在
doSomething()
函数内部，
date
被视为一个 const 对象（因为它通过 const 引用传递）。并且使用该 const
date
，我们正在调用非 const 成员函数
print()
。由于我们不能在 const 对象上调用非 const 成员函数，这将导致编译错误。
修复很简单：将
print()
设为 const
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // now const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

void doSomething(const Date& date)
{
    date.print();
}

int main()
{
    Date today { 2020, 10, 14 }; // non-const
    today.print();

    doSomething(today);

    return 0;
}
现在在函数
doSomething()
中，
const date
将能够成功调用 const 成员函数
print()
。
成员函数 const 和非 const 重载
最后，尽管不常做，但可以重载成员函数，使其具有同一函数的 const 和非 const 版本。这是因为 const 限定符被认为是函数签名的一部分，因此仅在 const 属性上不同的两个函数被认为是不同的。
#include <iostream>

struct Something
{
    void print()
    {
        std::cout << "non-const\n";
    }

    void print() const
    {
        std::cout << "const\n";
    }
};

int main()
{
    Something s1{};
    s1.print(); // calls print()

    const Something s2{};
    s2.print(); // calls print() const
    
    return 0;
}
这会打印
non-const
const
用 const 和非 const 版本重载函数通常在返回值需要有 const 差异时进行。这非常罕见。
下一课
14.5
公有成员和私有成员以及访问说明符
返回目录
上一课
14.3
成员函数