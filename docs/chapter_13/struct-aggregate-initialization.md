# 13.8 — 结构体聚合初始化

13.8 — 结构体聚合初始化
Alex
2022年1月18日，太平洋标准时间上午10:24
2025年1月6日
在上一课（
13.7 -- 结构体、成员和成员选择简介
）中，我们讨论了如何定义结构体、实例化结构体对象以及访问其成员。在本课中，我们将讨论如何初始化结构体。
数据成员默认不初始化
与普通变量非常相似，数据成员默认不初始化。考虑以下结构体
#include <iostream>

struct Employee
{
    int id; // note: no initializer here
    int age;
    double wage;
};

int main()
{
    Employee joe; // note: no initializer here either
    std::cout << joe.id << '\n';

    return 0;
}
因为我们没有提供任何初始化器，当实例化 `joe` 时，`joe.id`、`joe.age` 和 `joe.wage` 都将未初始化。当我们尝试打印 `joe.id` 的值时，我们将得到未定义行为。
然而，在我们向您展示如何初始化结构体之前，让我们稍作 detour。
什么是聚合？
在通用编程中，
聚合数据类型
（也称为
聚合
）是任何可以包含多个数据成员的类型。某些类型的聚合允许成员具有不同的类型（例如结构体），而另一些则要求所有成员必须是单一类型（例如数组）。
在 C++ 中，聚合的定义更窄，也更复杂。
作者注
在本系列教程中，当我们使用术语“聚合”（或“非聚合”）时，我们将指 C++ 对聚合的定义。
致进阶读者
为了简化一下，C++ 中的聚合要么是 C 风格数组（
17.7 -- C 风格数组简介
），要么是具有以下特征的类类型（结构体、类或联合）：
没有用户声明的构造函数（
14.9 -- 构造函数简介
）
没有私有或保护的非静态数据成员（
14.5 -- 公有和私有成员以及访问说明符
）
没有虚函数（
25.2 -- 虚函数和多态性
）
流行的类型 `std::array` (
17.1 -- `std::array` 简介
) 也是一个聚合。
您可以在
此处
找到 C++ 聚合的精确定义。
此时需要理解的关键是，只有数据成员的结构体是聚合。
结构体的聚合初始化
因为普通变量只能保存单个值，所以我们只需要提供一个初始化器
int x { 5 };
然而，一个结构体可以有多个成员
struct Employee
{
    int id {};
    int age {};
    double wage {};
};
当我们定义一个结构体类型的对象时，我们需要在初始化时以某种方式初始化多个成员。
Employee joe; // how do we initialize joe.id, joe.age, and joe.wage?
聚合使用一种称为
聚合初始化
的初始化形式，它允许我们直接初始化聚合的成员。为此，我们提供一个
初始化列表
作为初始化器，它只是一个用花括号括起来的逗号分隔值的列表。
聚合初始化主要有两种形式
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee frank = { 1, 32, 60000.0 }; // copy-list initialization using braced list
    Employee joe { 2, 28, 45000.0 };     // list initialization using braced list (preferred)

    return 0;
}
这些初始化形式中的每一种都执行
成员级初始化
，这意味着结构体中的每个成员都按照声明顺序进行初始化。因此，`Employee joe { 2, 28, 45000.0 };` 首先用值 `2` 初始化 `joe.id`，然后用值 `28` 初始化 `joe.age`，最后用值 `45000.0` 初始化 `joe.wage`。
最佳实践
在初始化聚合时，首选（非复制）花括号列表形式。
在 C++20 中，我们还可以使用带括号的值列表来初始化（一些）聚合
Employee robert ( 3, 45, 62500.0 );  // direct initialization using parenthesized list (C++20)
我们建议尽可能避免使用最后一种形式，因为它目前不适用于使用花括号省略的聚合（特别是 `std::array`）。
初始化列表中缺少初始化器
如果一个聚合被初始化，但初始化值的数量少于成员的数量，那么每个没有显式初始化器的成员将按如下方式初始化：
如果成员有默认成员初始化器，则使用该初始化器。
否则，成员将从空初始化列表进行复制初始化。在大多数情况下，这将对这些成员执行值初始化（对于类类型，即使存在列表构造函数，也会调用默认构造函数）。
struct Employee
{
    int id {};
    int age {};
    double wage { 76000.0 };
    double whatever;
};

int main()
{
    Employee joe { 2, 28 }; // joe.whatever will be value-initialized to 0.0

    return 0;
}
在上面的例子中，`joe.id` 将被初始化为 `2`，`joe.age` 将被初始化为 `28`。因为 `joe.wage` 没有显式初始化器但有一个默认成员初始化器，所以 `joe.wage` 将被初始化为 `76000.0`。最后，因为 `joe.whatever` 没有显式初始化器，`joe.whatever` 被值初始化为 `0.0`。
提示
这意味着我们通常可以使用空初始化列表来值初始化结构体的所有成员
Employee joe {}; // value-initialize all members
重载 `operator<<` 以打印结构体
在第
13.5 -- I/O 运算符重载简介
课中，我们展示了如何重载 `operator<<` 以打印枚举。为结构体重载 `operator<<` 也很有用。
这是上一节中的相同示例，现在重载了 `operator<<`
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

std::ostream& operator<<(std::ostream& out, const Employee& e)
{
    out << e.id << ' ' << e.age << ' ' << e.wage;
    return out;
}

int main()
{
    Employee joe { 2, 28 }; // joe.wage will be value-initialized to 0.0
    std::cout << joe << '\n';

    return 0;
}
这会打印
2 28 0
我们可以看到 `joe.wage` 确实被值初始化为 `0.0`（打印为 `0`）。
与枚举不同，结构体可以保存多个值。如何格式化输出（例如，分隔值）完全由您决定。
上面我们的重载 `operator<<` 输出的三个值并不直观，因为没有指示这些值意味着什么。让我们做同样的例子，但更新我们的输出函数，使其更具描述性。
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

std::ostream& operator<<(std::ostream& out, const Employee& e)
{
    out << "id: " << e.id << " age: " << e.age << " wage: " << e.wage;
    return out;
}

int main()
{
    Employee joe { 2, 28 }; // joe.wage will be value-initialized to 0.0
    std::cout << joe << '\n';

    return 0;
}
现在打印
id: 2 age: 28 wage: 0
这样更容易理解。
常量结构体
结构体类型的变量可以是 `const`（或 `constexpr`），就像所有 `const` 变量一样，它们必须被初始化。
struct Rectangle
{
    double length {};
    double width {};
};

int main()
{
    const Rectangle unit { 1.0, 1.0 };
    const Rectangle zero { }; // value-initialize all members

    return 0;
}
指定初始化器
C++20
当从值列表初始化结构体时，初始化器会按照声明的顺序应用于成员。
struct Foo
{
    int a {};
    int c {};
};

int main()
{
    Foo f { 1, 3 }; // f.a = 1, f.c = 3

    return 0;
}
现在考虑如果您更新此结构体定义以添加一个不是最后一个成员的新成员会发生什么？
struct Foo
{
    int a {};
    int b {}; // just added
    int c {};
};

int main()
{
    Foo f { 1, 3 }; // now, f.a = 1, f.b = 3, f.c = 0

    return 0;
}
现在所有的初始化值都移位了，更糟糕的是，编译器可能不会将其检测为错误（毕竟，语法仍然有效）。
为了帮助避免这种情况，C++20 增加了一种新的初始化结构体成员的方法，称为
指定初始化器
。指定初始化器允许您显式定义哪个初始化值映射到哪个成员。成员可以使用列表或复制初始化进行初始化，并且必须按照它们在结构体中声明的相同顺序进行初始化，否则将导致警告或错误。未指定初始化器的成员将进行值初始化。
struct Foo
{
    int a{ };
    int b{ };
    int c{ };
};

int main()
{
    Foo f1{ .a{ 1 }, .c{ 3 } }; // ok: f1.a = 1, f1.b = 0 (value initialized), f1.c = 3
    Foo f2{ .a = 1, .c = 3 };   // ok: f2.a = 1, f2.b = 0 (value initialized), f2.c = 3
    Foo f3{ .b{ 2 }, .a{ 1 } }; // error: initialization order does not match order of declaration in struct

    return 0;
}
对于 Clang 用户
在使用花括号进行单个值的指定初始化时，Clang 会不正确地发出警告“braces around scalar initializer”。希望这个问题能很快解决。
指定初始化器很好，因为它们提供了一定程度的自我文档，并有助于确保您不会无意中混淆初始化值的顺序。然而，指定初始化器也大大增加了初始化列表的混乱程度，因此我们目前不建议将其作为最佳实践。
此外，由于没有强制要求在初始化聚合的所有地方都始终如一地使用指定初始化器，因此最好避免在现有聚合定义的中间添加新成员，以避免初始化器移位的风险。
最佳实践
当向聚合添加新成员时，最安全的方法是将其添加到定义列表的底部，这样其他成员的初始化器就不会移位。
使用初始化列表赋值
如前一课所示，我们可以单独为结构体成员赋值
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };

    joe.age  = 33;      // Joe had a birthday
    joe.wage = 66000.0; // and got a raise

    return 0;
}
这对于单个成员来说很好，但当我们想更新许多成员时就不太好了。与使用初始化列表初始化结构体类似，您也可以使用初始化列表为结构体赋值（这会进行成员级赋值）
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };
    joe = { joe.id, 33, 66000.0 }; // Joe had a birthday and got a raise

    return 0;
}
请注意，因为我们不想改变 `joe.id`，所以我们需要在列表中提供 `joe.id` 的当前值作为占位符，以便成员级赋值可以将 `joe.id` 赋值给 `joe.id`。这有点难看。
带指定初始化器的赋值
C++20
指定初始化器也可以在列表赋值中使用
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };
    joe = { .id = joe.id, .age = 33, .wage = 66000.0 }; // Joe had a birthday and got a raise

    return 0;
}
在此类赋值中未指定的任何成员都将赋值为值初始化所使用的值。如果我们没有为 `joe.id` 指定初始化器，`joe.id` 将被赋值为 0。
用相同类型的另一个结构体初始化结构体
一个结构体也可以使用相同类型的另一个结构体进行初始化
#include <iostream>

struct Foo
{
    int a{};
    int b{};
    int c{};
};

std::ostream& operator<<(std::ostream& out, const Foo& f)
{
    out << f.a << ' ' << f.b << ' ' << f.c;
    return out;
}

int main()
{
    Foo foo { 1, 2, 3 };

    Foo x = foo; // copy-initialization
    Foo y(foo);  // direct-initialization
    Foo z {foo}; // direct-list-initialization

    std::cout << x << '\n';
    std::cout << y << '\n';
    std::cout << z << '\n';

    return 0;
}
上面打印
1 2 3
1 2 3
1 2 3
请注意，这使用的是我们熟悉的标准初始化形式（复制、直接或直接列表初始化），而不是聚合初始化。
这最常出现在使用返回相同类型结构体的函数返回值初始化结构体时。我们将在
13.10 -- 传递和返回结构体
课程中更详细地介绍这一点。
下一课
13.9
默认成员初始化
返回目录
上一课
13.7
结构体、成员和成员选择简介