# 13.11 — 结构体杂项

13.11 — 结构体杂项
Alex
2023 年 7 月 21 日，下午 4:09 PDT
2024 年 9 月 25 日
具有程序定义成员的结构体
在 C++ 中，结构体（和类）可以拥有其他程序定义类型的成员。有两种方法可以实现这一点。
首先，我们可以定义一个程序定义类型（在全局作用域中），然后将其用作另一个程序定义类型的成员
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

struct Company
{
    int numberOfEmployees {};
    Employee CEO {}; // Employee is a struct within the Company struct
};

int main()
{
    Company myCompany{ 7, { 1, 32, 55000.0 } }; // Nested initialization list to initialize Employee
    std::cout << myCompany.CEO.wage << '\n'; // print the CEO's wage

    return 0;
}
在上面的例子中，我们定义了一个 `Employee` 结构体，然后将其用作 `Company` 结构体的成员。当我们初始化 `Company` 时，我们也可以使用嵌套初始化列表来初始化 `Employee`。如果我们想知道 CEO 的工资是多少，我们只需使用两次成员选择运算符：`myCompany.CEO.wage;`
其次，类型也可以嵌套在其他类型中，因此如果一个 Employee 仅作为 Company 的一部分存在，那么 Employee 类型可以嵌套在 Company 结构体中
#include <iostream>

struct Company
{
    struct Employee // accessed via Company::Employee
    {
        int id{};
        int age{};
        double wage{};
    };

    int numberOfEmployees{};
    Employee CEO{}; // Employee is a struct within the Company struct
};

int main()
{
    Company myCompany{ 7, { 1, 32, 55000.0 } }; // Nested initialization list to initialize Employee
    std::cout << myCompany.CEO.wage << '\n'; // print the CEO's wage

    return 0;
}
这在类中更常见，所以我们将在未来的课程中详细讨论（
15.3 -- 嵌套类型（成员类型）
）。
所有者结构体的数据成员也应是所有者
在第
5.9 课 -- std::string_view（第二部分）
中，我们介绍了所有者和查看者的双重概念。所有者管理自己的数据，并控制其何时销毁。查看者查看其他人的数据，不控制其何时被修改或销毁。
在大多数情况下，我们希望我们的结构体（和类）是其包含数据的“所有者”。这提供了几个有用的好处
数据成员的有效时间与结构体（或类）的有效时间相同。
这些数据成员的值不会意外改变。
使结构体（或类）成为所有者最简单的方法是为其每个数据成员提供一个所有者类型（例如，不是查看者、指针或引用）。如果一个结构体或类的数据成员都是所有者，那么该结构体或类本身就自动成为所有者。
如果一个结构体（或类）有一个数据成员是查看者，则该成员所查看的对象可能在该数据成员销毁之前就被销毁了。如果发生这种情况，该结构体将留下一个悬空成员，并且访问该成员将导致未定义行为。
最佳实践
在大多数情况下，我们希望我们的结构体（和类）是所有者。实现这一点的最简单方法是确保每个数据成员都具有所有权类型（例如，不是查看器、指针或引用）。
作者注
安全地使用结构体。不要让你的成员悬空。
这就是为什么字符串数据成员几乎总是 `std::string` 类型（所有者），而不是 `std::string_view` 类型（查看者）。下面的例子说明了这一点的重要性
#include <iostream>
#include <string>
#include <string_view>

struct Owner
{
    std::string name{}; // std::string is an owner
};

struct Viewer
{
    std::string_view name {}; // std::string_view is a viewer
};

// getName() returns the user-entered string as a temporary std::string
// This temporary std::string will be destroyed at the end of the full expression
// containing the function call.
std::string getName()
{
    std::cout << "Enter a name: ";
    std::string name{};
    std::cin >> name;
    return name;
}

int main()
{
    Owner o { getName() };  // The return value of getName() is destroyed just after initialization
    std::cout << "The owners name is " << o.name << '\n';  // ok

    Viewer v { getName() }; // The return value of getName() is destroyed just after initialization
    std::cout << "The viewers name is " << v.name << '\n'; // undefined behavior

    return 0;
}
`getName()` 函数将用户输入的名称作为临时 `std::string` 返回。此临时返回值在函数调用的完整表达式结束时被销毁。
在 `o` 的情况下，这个临时 `std::string` 用于初始化 `o.name`。由于 `o.name` 是一个 `std::string`，`o.name` 会复制这个临时 `std::string`。然后临时 `std::string` 被销毁，但 `o.name` 不受影响，因为它是一个副本。当我们在后续语句中打印 `o.name` 时，它会如我们预期地工作。
在 `v` 的情况下，这个临时 `std::string` 用于初始化 `v.name`。由于 `v.name` 是一个 `std::string_view`，`v.name` 只是对临时 `std::string` 的一个视图，而不是一个副本。然后临时 `std::string` 被销毁，导致 `v.name` 悬空。当我们在后续语句中打印 `v.name` 时，我们得到未定义行为。
结构体大小和数据结构对齐
通常情况下，结构体的大小是其所有成员大小的总和，但并非总是如此！
考虑以下程序
#include <iostream>

struct Foo
{
    short a {};
    int b {};
    double c {};
};

int main()
{
    std::cout << "The size of short is " << sizeof(short) << " bytes\n";
    std::cout << "The size of int is " << sizeof(int) << " bytes\n";
    std::cout << "The size of double is " << sizeof(double) << " bytes\n";

    std::cout << "The size of Foo is " << sizeof(Foo) << " bytes\n";

    return 0;
}
在作者的机器上，这打印出来
The size of short is 2 bytes
The size of int is 4 bytes
The size of double is 8 bytes
The size of Foo is 16 bytes
注意，`short` + `int` + `double` 的大小是 14 字节，但 `Foo` 的大小是 16 字节！
结果是，我们只能说一个结构体的大小将**至少**与其包含的所有变量的大小一样大。但它可能会更大！为了性能原因，编译器有时会在结构体中添加间隙（这被称为**填充**）。
在上面的 `Foo` 结构体中，编译器在成员 `a` 之后无形中添加了 2 字节的填充，使结构体的大小变为 16 字节而不是 14 字节。
致进阶读者
编译器可能添加填充的原因超出了本教程的范围，但想要了解更多信息的读者可以在维基百科上阅读有关
数据结构对齐
的内容。这是可选阅读，理解结构体或 C++ 不需要！
这实际上会对结构体的大小产生相当大的影响，如下面的程序所示
#include <iostream>

struct Foo1
{
    short a{}; // will have 2 bytes of padding after a
    int b{};
    short c{}; // will have 2 bytes of padding after c
};

struct Foo2
{
    int b{};
    short a{};
    short c{};
};

int main()
{
    std::cout << sizeof(Foo1) << '\n'; // prints 12
    std::cout << sizeof(Foo2) << '\n'; // prints 8

    return 0;
}
这个程序打印
12
8
请注意，`Foo1` 和 `Foo2` 具有相同的成员，唯一的区别是声明顺序。然而，由于增加了填充，`Foo1` 的大小增加了 50%。
提示
你可以通过按大小递减的顺序定义成员来最小化填充。
C++ 编译器不允许重新排序成员，因此必须手动完成。
下一课
13.12
使用指针和引用进行成员选择
返回目录
上一课
13.10
传递和返回结构体