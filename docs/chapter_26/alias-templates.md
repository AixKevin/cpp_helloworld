# 13.15 — 别名模板

13.15 — 别名模板
Alex
2023 年 9 月 27 日上午 10:20 PDT
2024 年 6 月 11 日
在
10.7 课 — Typedefs 和类型别名
中，我们讨论了类型别名如何让我们为现有类型定义一个别名。
为所有模板参数都显式指定的类模板创建类型别名，其工作方式与普通类型别名相同
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
void print(const Pair<T>& p)
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    using Point = Pair<int>; // create normal type alias
    Point p { 1, 2 };        // compiler replaces this with Pair<int>

    print(p);

    return 0;
}
此类别名可以在局部（例如函数内部）或全局定义。
别名模板
在其他情况下，我们可能希望为模板类创建类型别名，其中并非所有模板参数都作为别名的一部分定义（而是由类型别名的用户提供）。为此，我们可以定义一个
别名模板
，它是一个可以用于实例化类型别名的模板。就像类型别名不定义不同的类型一样，别名模板也不定义不同的类型。
这是一个如何工作的例子
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// Here's our alias template
// Alias templates must be defined in global scope
template <typename T>
using Coord = Pair<T>; // Coord is an alias for Pair<T>

// Our print function template needs to know that Coord's template parameter T is a type template parameter
template <typename T>
void print(const Coord<T>& c)
{
    std::cout << c.first << ' ' << c.second << '\n';
}

int main()
{
    Coord<int> p1 { 1, 2 }; // Pre C++-20: We must explicitly specify all type template argument
    Coord p2 { 1, 2 };      // In C++20, we can use alias template deduction to deduce the template arguments in cases where CTAD works

    std::cout << p1.first << ' ' << p1.second << '\n';
    print(p2);

    return 0;
}
在此示例中，我们定义了一个名为
Coord
的别名模板作为
Pair<T>
的别名，其中类型模板参数
T
将由
Coord
别名的用户定义。
Coord
是别名模板，而
Coord<T>
是
Pair<T>
的实例化类型别名。一旦定义，我们可以在使用
Pair
的地方使用
Coord
，在使用
Pair<T>
的地方使用
Coord<T>
。
关于这个例子有几点值得注意。
首先，与普通类型别名（可以在块内部定义）不同，别名模板必须在全局作用域中定义（所有模板都必须如此）。
其次，在 C++20 之前，当我们使用别名模板实例化对象时，我们必须显式指定模板参数。从 C++20 开始，我们可以使用
别名模板推导
，它将在别名类型与 CTAD 配合使用的情况下从初始化器推导出模板参数的类型。
第三，由于 CTAD 不适用于函数参数，因此当我们使用别名模板作为函数参数时，我们必须显式定义别名模板使用的模板参数。换句话说，我们这样做
template <typename T>
void print(const Coord<T>& c)
{
    std::cout << c.first << ' ' << c.second << '\n';
}
而不是这样
void print(const Coord& c) // won't work, missing template arguments
{
    std::cout << c.first << ' ' << c.second << '\n';
}
这与我们使用
Pair
或
Pair<T>
而不是
Coord
或
Coord<T>
没有任何不同。
下一课
13.x
第 13 章总结与测验
返回目录
上一课
13.14
类模板参数推导 (CTAD) 和推导指南