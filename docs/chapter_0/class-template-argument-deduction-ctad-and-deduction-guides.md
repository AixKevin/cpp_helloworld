# 13.14 — 类模板参数推导 (CTAD) 和推导指南

13.14 — 类模板参数推导 (CTAD) 和推导指南
Alex
2022年4月24日，太平洋夏令时下午7:49
2024年3月25日
类模板参数推导 (CTAD)
C++17
从 C++17 开始，当从类模板实例化对象时，编译器可以从对象的初始化器类型中推导出模板类型（这被称为
类模板参数推导
，简称
CTAD
）。例如：
#include <utility> // for std::pair

int main()
{
    std::pair<int, int> p1{ 1, 2 }; // explicitly specify class template std::pair<int, int> (C++11 onward)
    std::pair p2{ 1, 2 };           // CTAD used to deduce std::pair<int, int> from the initializers (C++17)

    return 0;
}
只有在没有模板参数列表的情况下才执行 CTAD。因此，以下两种情况都会报错：
#include <utility> // for std::pair

int main()
{
    std::pair<> p1 { 1, 2 };    // error: too few template arguments, both arguments not deduced
    std::pair<int> p2 { 3, 4 }; // error: too few template arguments, second argument not deduced

    return 0;
}
作者注
本网站上许多未来的课程都将使用 CTAD。如果您使用 C++14 标准（或更旧的版本）编译这些示例，您将收到缺少模板参数的错误。您需要显式地将这些参数添加到示例中才能使其编译。
由于 CTAD 是一种类型推导形式，我们可以使用字面量后缀来改变推导出的类型：
#include <utility> // for std::pair

int main()
{
    std::pair p1 { 3.4f, 5.6f }; // deduced to pair<float, float>
    std::pair p2 { 1u, 2u };     // deduced to pair<unsigned int, unsigned int>

    return 0;
}
模板参数推导指南
C++17
在大多数情况下，CTAD 开箱即用。然而，在某些情况下，编译器可能需要一些额外的帮助才能正确推导模板参数。
您可能会惊讶地发现，以下程序（与上面使用
std::pair
的示例几乎相同）在 C++17 中（仅限）无法编译：
// define our own Pair type
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

int main()
{
    Pair<int, int> p1{ 1, 2 }; // ok: we're explicitly specifying the template arguments
    Pair p2{ 1, 2 };           // compile error in C++17 (okay in C++20)

    return 0;
}
如果您在 C++17 中编译此程序，您可能会收到关于“类模板参数推导失败”或“无法推导模板参数”或“没有可行的构造函数或推导指南”的错误。这是因为在 C++17 中，CTAD 不知道如何推导聚合类模板的模板参数。为了解决这个问题，我们可以为编译器提供一个
推导指南
，它告诉编译器如何为给定的类模板推导模板参数。
这是带有推导指南的相同程序：
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

// Here's a deduction guide for our Pair (needed in C++17 only)
// Pair objects initialized with arguments of type T and U should deduce to Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
    
int main()
{
    Pair<int, int> p1{ 1, 2 }; // explicitly specify class template Pair<int, int> (C++11 onward)
    Pair p2{ 1, 2 };           // CTAD used to deduce Pair<int, int> from the initializers (C++17)

    return 0;
}
此示例应该在 C++17 下编译。
我们
Pair
类的推导指南非常简单，但让我们仔细看看它是如何工作的。
// Here's a deduction guide for our Pair (needed in C++17 only)
// Pair objects initialized with arguments of type T and U should deduce to Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
首先，我们使用与
Pair
类中相同的模板类型定义。这是有道理的，因为如果我们的推导指南要告诉编译器如何推导
Pair
的类型，我们就必须定义
T
和
U
是什么（模板类型）。其次，在箭头的右侧，是我们正在帮助编译器推导的类型。在这种情况下，我们希望编译器能够为
Pair
类型的对象推导模板参数，所以我们在这里放置的正是这个。最后，在箭头的左侧，我们告诉编译器要查找什么样的声明。在这种情况下，我们告诉它查找名为
Pair
的某个对象的声明，该对象带有两个参数（一个类型为
T
，另一个类型为
U
）。我们也可以将其写为
Pair(T t, U u)
（其中
t
和
u
是参数的名称，但由于我们不使用
t
和
u
，所以不需要给它们命名）。
总而言之，我们告诉编译器，如果它看到一个带有两个参数（分别类型为
T
和
U
）的
Pair
声明，它应该将类型推导为
Pair
。
因此，当编译器在我们的程序中看到定义
Pair p2{ 1, 2 };
时，它会说：“哦，这是一个
Pair
的声明，并且有两个
int
类型的参数，所以使用推导指南，我应该将它推导为
Pair
。”
这是一个接受单个模板类型的 Pair 的类似示例：
template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// Here's a deduction guide for our Pair (needed in C++17 only)
// Pair objects initialized with arguments of type T and T should deduce to Pair<T>
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 1, 2 }; // explicitly specify class template Pair<int> (C++11 onward)
    Pair p2{ 1, 2 };      // CTAD used to deduce Pair<int> from the initializers (C++17)

    return 0;
}
在这种情况下，我们的推导指南将
Pair(T, T)
（一个带有两个
T
类型参数的
Pair
）映射到
Pair
。
提示
C++20 增加了编译器自动为聚合类型生成推导指南的能力，因此推导指南应该只为了 C++17 兼容性而提供。
因此，没有推导指南的
Pair
版本应该在 C++20 中编译。
std::pair
（和其他标准库模板类型）带有预定义的推导指南，这就是为什么我们上面使用
std::pair
的示例在 C++17 中可以正常编译，而无需我们自己提供推导指南。
致进阶读者
非聚合类型在 C++17 中不需要推导指南，因为构造函数的存在起到了相同的作用。
带有默认值的类型模板参数
就像函数参数可以有默认参数一样，模板参数可以给定默认值。当模板参数未明确指定且无法推导时，将使用这些默认值。
这是我们上面
Pair
类模板程序的修改版本，其中类型模板参数
T
和
U
默认设置为
int
类型：
template <typename T=int, typename U=int> // default T and U to type int
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;

int main()
{
    Pair<int, int> p1{ 1, 2 }; // explicitly specify class template Pair<int, int> (C++11 onward)
    Pair p2{ 1, 2 };           // CTAD used to deduce Pair<int, int> from the initializers (C++17)

    Pair p3;                   // uses default Pair<int, int>

    return 0;
}
我们对
p3
的定义没有显式指定类型模板参数的类型，也没有这些类型可以从中推导的初始化器。因此，编译器将使用默认值中指定的类型，这意味着
p3
将是
Pair
类型。
CTAD 不适用于非静态成员初始化
当使用非静态成员初始化来初始化类类型的成员时，CTAD 在此上下文中将不起作用。所有模板参数都必须显式指定：
#include <utility> // for std::pair

struct Foo
{
    std::pair<int, int> p1{ 1, 2 }; // ok, template arguments explicitly specified
    std::pair p2{ 1, 2 };           // compile error, CTAD can't be used in this context
};

int main()
{
    std::pair p3{ 1, 2 };           // ok, CTAD can be used here
    return 0;
}
CTAD 不适用于函数参数
CTAD 代表类模板
实参
推导，而不是类模板
参数
推导，因此它只会推导模板实参的类型，而不是模板参数的类型。
因此，CTAD 不能用于函数参数。
#include <iostream>
#include <utility>

void print(std::pair p) // compile error, CTAD can't be used here
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p deduced to std::pair<int, int>
    print(p);

    return 0;
}
在这种情况下，您应该改用模板：
#include <iostream>
#include <utility>

template <typename T, typename U>
void print(std::pair<T, U> p)
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p deduced to std::pair<int, int>
    print(p);

    return 0;
}
下一课
13.15
别名模板
返回目录
上一课
13.13
类模板