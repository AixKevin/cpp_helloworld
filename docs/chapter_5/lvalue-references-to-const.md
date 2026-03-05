# 12.4 — 对 const 的左值引用

12.4 — 对 const 的左值引用
Alex
2017 年 6 月 7 日，下午 3:30 PDT
2025 年 2 月 23 日
在上一课（
12.3 -- 左值引用
）中，我们讨论了左值引用如何只能绑定到可修改的左值。这意味着以下情况是非法的
int main()
{
    const int x { 5 }; // x is a non-modifiable (const) lvalue
    int& ref { x }; // error: ref can not bind to non-modifiable lvalue

    return 0;
}
这是不允许的，因为它将允许我们通过非常量引用（
ref
）修改常量变量（
x
）。
但是，如果我们想创建一个引用指向一个常量变量呢？普通的左值引用（指向非常量值）将无法做到。
const 的左值引用
通过在声明左值引用时使用
const
关键字，我们告诉左值引用将其引用的对象视为 const。这种引用被称为**const 值的左值引用**（有时也称为**const 引用**或**常量引用**）。
const 的左值引用可以绑定到不可修改的左值
int main()
{
    const int x { 5 };    // x is a non-modifiable lvalue
    const int& ref { x }; // okay: ref is a an lvalue reference to a const value

    return 0;
}
因为 const 的左值引用将其引用的对象视为 const，所以它们可以用于访问但不能修改被引用的值
#include <iostream>

int main()
{
    const int x { 5 };    // x is a non-modifiable lvalue
    const int& ref { x }; // okay: ref is a an lvalue reference to a const value

    std::cout << ref << '\n'; // okay: we can access the const object
    ref = 6;                  // error: we can not modify an object through a const reference
    
    return 0;
}
用可修改的左值初始化 const 的左值引用
const 的左值引用也可以绑定到可修改的左值。在这种情况下，当通过引用访问时，被引用的对象被视为 const（即使底层对象不是 const）
#include <iostream>

int main()
{
    int x { 5 };          // x is a modifiable lvalue
    const int& ref { x }; // okay: we can bind a const reference to a modifiable lvalue

    std::cout << ref << '\n'; // okay: we can access the object through our const reference
    ref = 7;                  // error: we can not modify an object through a const reference

    x = 6;                // okay: x is a modifiable lvalue, we can still modify it through the original identifier

    return 0;
}
在上面的程序中，我们将 const 引用
ref
绑定到可修改的左值
x
。然后我们可以使用
ref
访问
x
，但由于
ref
是 const，我们不能通过
ref
修改
x
的值。但是，我们仍然可以直接修改
x
的值（使用标识符
x
）。
最佳实践
除非您需要修改被引用的对象，否则请优先使用
const 的左值引用
，而不是
非常量的左值引用
。
用右值初始化 const 的左值引用
也许令人惊讶的是，const 的左值引用也可以绑定到右值
#include <iostream>

int main()
{
    const int& ref { 5 }; // okay: 5 is an rvalue

    std::cout << ref << '\n'; // prints 5

    return 0;
}
发生这种情况时，会创建一个临时对象并用右值对其进行初始化，然后将 const 引用绑定到该临时对象。
相关内容
我们在第
2.5 -- 局部作用域介绍
课中介绍了临时对象。
用不同类型的值初始化 const 的左值引用
const 的左值引用甚至可以绑定到不同类型的值，只要这些值可以隐式转换为引用类型
#include <iostream>

int main()
{
    // case 1
    const double& r1 { 5 };  // temporary double initialized with value 5, r1 binds to temporary

    std::cout << r1 << '\n'; // prints 5

    // case 2
    char c { 'a' };
    const int& r2 { c };     // temporary int initialized with value 'a', r2 binds to temporary

    std::cout << r2 << '\n'; // prints 97 (since r2 is a reference to int)

    return 0;
}
在情况 1 中，创建一个
double
类型的临时对象并用 int 值
5
初始化。然后
const double& r1
绑定到该临时 double 对象。
在情况 2 中，创建一个
int
类型的临时对象并用 char 值
a
初始化。然后
const int& r2
绑定到该临时 int 对象。
在两种情况下，引用的类型和临时对象的类型都匹配。
关键见解
如果您尝试将 const 左值引用绑定到不同类型的值，编译器将创建一个与引用类型相同的临时对象，使用该值对其进行初始化，然后将引用绑定到该临时对象。
另请注意，当我们打印
r2
时，它打印为 int 而不是 char。这是因为
r2
是对 int 对象（已创建的临时 int）的引用，而不是对 char
c
的引用。
尽管这看起来可能很奇怪，但我们将在
12.6 -- 通过 const 左值引用传递
课中看到这种用法的例子。
警告
我们通常假定引用与其绑定的对象相同——但是当引用绑定到对象的临时副本或由对象转换产生的临时对象时，这个假设就会被打破。随后对原始对象进行的任何修改都不会被引用看到（因为它引用的是不同的对象），反之亦然。
这是一个显示此情况的愚蠢示例
#include <iostream>

int main()
{
    short bombs { 1 };         // I can has bomb! (note: type is short)
    
    const int& you { bombs };  // You can has bomb too (note: type is int&)
    --bombs;                   // Bomb all gone

    if (you)                   // You still has?
    {
        std::cout << "Bombs away!  Goodbye, cruel world.\n"; // Para bailar la bomba
    }

    return 0;
}
在上面的示例中，
bombs
是一个
short
，
you
是一个
const int&
。因为
you
只能绑定到
int
对象，所以当
you
用
bombs
初始化时，编译器会将
bombs
隐式转换为
int
，这会导致创建一个临时
int
对象（值为
1
）。
you
最终绑定到这个临时对象而不是
bombs
。
当
bombs
递减时，
you
不受影响，因为它引用的是不同的对象。所以虽然我们期望
if (you)
评估为
false
，但它实际上评估为
true
。
如果您能停止炸毁世界，那就太好了。
绑定到临时对象的常量引用延长了临时对象的生命周期
临时对象通常在创建它们的表达式结束时被销毁。
给定语句
const int& ref { 5 };
，考虑如果创建用于保存右值
5
的临时对象在初始化
ref
的表达式结束时被销毁，会发生什么。引用
ref
将处于悬空状态（引用一个已被销毁的对象），当我们尝试访问
ref
时，我们将得到未定义行为。
为了避免在这种情况下出现悬空引用，C++ 有一个特殊规则：当 const 左值引用**直接**绑定到临时对象时，临时对象的生命周期将延长以匹配引用的生命周期。
#include <iostream>

int main()
{
    const int& ref { 5 }; // The temporary object holding value 5 has its lifetime extended to match ref

    std::cout << ref << '\n'; // Therefore, we can safely use it here

    return 0;
} // Both ref and the temporary object die here
在上面的示例中，当
ref
用右值
5
初始化时，会创建一个临时对象，并且
ref
绑定到该临时对象。临时对象的生命周期与
ref
的生命周期匹配。因此，我们可以在下一条语句中安全地打印
ref
的值。然后
ref
和临时对象都超出作用域并在块结束时被销毁。
关键见解
左值引用只能绑定到可修改的左值。
const 的左值引用可以绑定到可修改的左值、不可修改的左值和右值。这使它们成为一种更灵活的引用类型。
致进阶读者
生命周期延长仅在常量引用直接绑定到临时对象时才有效。从函数返回的临时对象（即使是常量引用返回的）不符合生命周期延长的条件。
我们在
12.12 -- 通过引用返回和通过地址返回
课中展示了这方面的一个示例。
对于类类型右值，将引用绑定到成员将延长整个对象的生命周期。
那么 C++ 为什么允许常量引用绑定到右值呢？我们将在下一课中回答这个问题！
Constexpr 左值引用
可选
当应用于引用时，
constexpr
允许在常量表达式中使用引用。Constexpr 引用有一个特殊的限制：它们只能绑定到具有静态持续时间的对象（全局变量或静态局部变量）。这是因为编译器知道静态对象在内存中实例化在哪里，所以它可以将该地址视为编译时常量。
constexpr 引用不能绑定到（非静态）局部变量。这是因为局部变量的地址直到它们定义的函数实际调用时才知道。
int g_x { 5 };

int main()
{
    [[maybe_unused]] constexpr int& ref1 { g_x }; // ok, can bind to global

    static int s_x { 6 };
    [[maybe_unused]] constexpr int& ref2 { s_x }; // ok, can bind to static local

    int x { 6 };
    [[maybe_unused]] constexpr int& ref3 { x }; // compile error: can't bind to non-static object

    return 0;
}
当定义常量变量的 constexpr 引用时，我们需要同时应用
constexpr
（应用于引用）和
const
（应用于被引用的类型）。
int main()
{
    static const int s_x { 6 }; // a const int
    [[maybe_unused]] constexpr const int& ref2 { s_x }; // needs both constexpr and const

    return 0;
}
鉴于这些限制，constexpr 引用通常很少使用。
下一课
12.5
通过左值引用传递
返回目录
上一课
12.3
左值引用