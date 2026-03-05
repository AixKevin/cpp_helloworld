# 12.5 — 通过左值引用传递

12.5 — 通过左值引用传递
Alex
2007 年 7 月 24 日，下午 6:06 PDT
2024 年 12 月 6 日
在前面的课程中，我们介绍了左值引用 (
12.3 -- 左值引用
) 和指向 const 的左值引用 (
12.4 -- 指向 const 的左值引用
)。单独来看，这些可能看起来不太有用——当你可以直接使用变量本身时，为什么要为变量创建别名？
在本课中，我们将最终提供一些关于引用有用之处的见解。然后从本章后面开始，您将经常看到引用的使用。
首先，一些背景。回到
2.4 — 函数参数和实参简介
课程中，我们讨论了
按值传递
，其中传递给函数的实参被复制到函数的形参中。
#include <iostream>

void printValue(int y)
{
    std::cout << y << '\n';
} // y is destroyed here

int main()
{
    int x { 2 };

    printValue(x); // x is passed by value (copied) into parameter y (inexpensive)

    return 0;
}
在上面的程序中，当调用
printValue(x)
时，
x
的值（
2
）被
复制
到形参
y
中。然后，在函数结束时，对象
y
被销毁。
这意味着当我们调用函数时，我们复制了实参的值，仅仅是短暂使用然后就销毁了它！幸运的是，由于基本类型复制成本低廉，这不是问题。
有些对象复制成本高昂
标准库提供的大多数类型（例如
std::string
）都是类类型。类类型通常复制成本高昂。只要有可能，我们都希望避免不必要地复制复制成本高昂的对象，特别是当我们几乎会立即销毁这些副本时。
考虑以下程序说明这一点
#include <iostream>
#include <string>

void printValue(std::string y)
{
    std::cout << y << '\n';
} // y is destroyed here

int main()
{
    std::string x { "Hello, world!" }; // x is a std::string

    printValue(x); // x is passed by value (copied) into parameter y (expensive)

    return 0;
}
这会打印
Hello, world!
虽然这个程序表现得如我们所期望的那样，但效率低下。与前一个例子完全相同，当调用
printValue()
时，实参
x
被复制到
printValue()
的形参
y
中。然而，在这个例子中，实参是一个
std::string
而不是一个
int
，并且
std::string
是一种复制成本高昂的类类型。而且每次调用
printValue()
都会进行这种昂贵的复制！
我们可以做得更好。
按引用传递
调用函数时避免对参数进行昂贵复制的一种方法是使用
按引用传递
而不是
按值传递
。使用
按引用传递
时，我们将函数参数声明为引用类型（或 const 引用类型），而不是普通类型。当函数被调用时，每个引用参数都绑定到相应的参数。因为引用充当参数的别名，所以不会复制参数。
以下是上面的例子，使用按引用传递而不是按值传递
#include <iostream>
#include <string>

void printValue(std::string& y) // type changed to std::string&
{
    std::cout << y << '\n';
} // y is destroyed here

int main()
{
    std::string x { "Hello, world!" };

    printValue(x); // x is now passed by reference into reference parameter y (inexpensive)

    return 0;
}
此程序与之前的程序相同，只是参数
y
的类型已从
std::string
更改为
std::string&
（一个左值引用）。现在，当调用
printValue(x)
时，左值引用参数
y
绑定到实参
x
。绑定引用总是廉价的，并且不需要复制
x
。由于引用充当被引用对象的别名，当
printValue()
使用引用
y
时，它正在访问实际的实参
x
（而不是
x
的副本）。
关键见解
按引用传递允许我们将参数传递给函数，而无需在每次调用函数时都复制这些参数。
以下程序演示了值形参与实参是不同的对象，而引用形参则被视为实参本身
#include <iostream>

void printAddresses(int val, int& ref)
{
    std::cout << "The address of the value parameter is: " << &val << '\n';
    std::cout << "The address of the reference parameter is: " << &ref << '\n';   
}

int main()
{
    int x { 5 };
    std::cout << "The address of x is: " << &x << '\n';
    printAddresses(x, x);

    return 0;
}
该程序的一次运行产生了以下输出
The address of x is: 0x7ffd16574de0
The address of the value parameter is: 0x7ffd16574de4
The address of the reference parameter is: 0x7ffd16574de0
我们可以看到实参与值形参的地址不同，这意味着值形参是不同的对象。由于它们具有独立的内存地址，为了使值形参与实参具有相同的值，实参的值必须复制到值形参所持有的内存中。
另一方面，我们可以看到获取引用参数的地址会得到与实参相同的地址。这意味着引用参数被视为与实参相同的对象。
按引用传递允许我们更改参数的值
当对象按值传递时，函数参数接收实参的副本。这意味着对参数值所做的任何更改都作用于实参的副本，而不是实参本身。
#include <iostream>

void addOne(int y) // y is a copy of x
{
    ++y; // this modifies the copy of x, not the actual object x
}

int main()
{
    int x { 5 };

    std::cout << "value = " << x << '\n';

    addOne(x);

    std::cout << "value = " << x << '\n'; // x has not been modified

    return 0;
}
在上述程序中，因为值参数
y
是
x
的副本，所以当我们递增
y
时，这只会影响
y
。此程序输出
value = 5
value = 5
然而，由于引用与被引用对象的作用相同，因此当使用按引用传递时，对引用参数所做的任何更改
都将
影响实参
#include <iostream>

void addOne(int& y) // y is bound to the actual object x
{
    ++y; // this modifies the actual object x
}

int main()
{
    int x { 5 };

    std::cout << "value = " << x << '\n';

    addOne(x);

    std::cout << "value = " << x << '\n'; // x has been modified

    return 0;
}
此程序输出
value = 5
value = 6
在上面的例子中，
x
最初的值是
5
。当调用
addOne(x)
时，引用参数
y
绑定到参数
x
。当
addOne()
函数增加引用
y
时，它实际上是将参数
x
从
5
增加到
6
（而不是
x
的副本）。这个改变的值即使在
addOne()
执行完成后也仍然存在。
关键见解
通过引用将值传递给非 const 允许我们编写修改传入参数值的函数。
函数修改传入参数值的能力非常有用。想象一下你写了一个函数来判断一个怪物是否成功攻击了玩家。如果成功，怪物应该对玩家的生命值造成一定量的伤害。如果你通过引用传递玩家对象，该函数可以直接修改传入的实际玩家对象的生命值。如果你按值传递玩家对象，你只能修改玩家对象副本的生命值，这就不那么有用了。
按引用传递只能接受可修改的左值参数
因为对非 const 值的引用只能绑定到可修改的左值（本质上是非 const 变量），这意味着按引用传递只适用于可修改的左值参数。实际上，这极大地限制了按引用传递给非 const 的实用性，因为它意味着我们不能传递 const 变量或字面量。例如
#include <iostream>

void printValue(int& y) // y only accepts modifiable lvalues
{
    std::cout << y << '\n';
}

int main()
{
    int x { 5 };
    printValue(x); // ok: x is a modifiable lvalue

    const int z { 5 };
    printValue(z); // error: z is a non-modifiable lvalue

    printValue(5); // error: 5 is an rvalue

    return 0;
}
幸运的是，有一个简单的解决方法，我们将在下一课中讨论。我们还将探讨何时按值传递以及何时按引用传递。
下一课
12.6
通过 const 左值引用传递
返回目录
上一课
12.4
指向 const 的左值引用