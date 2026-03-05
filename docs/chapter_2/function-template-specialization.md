# 26.3 — 函数模板特化

26.3 — 函数模板特化
Alex
2016年12月3日，太平洋标准时间下午5:10
2024年7月30日
当为给定类型实例化函数模板时，编译器会根据模板函数生成一份副本，并将模板类型参数替换为变量声明中使用的实际类型。这意味着对于每个实例化类型，特定函数将具有相同的实现细节（只是使用不同的类型）。虽然大多数情况下这正是您想要的，但偶尔也会出现需要为特定数据类型稍微不同地实现模板函数的情况。
使用非模板函数
考虑以下示例
#include <iostream>

template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
这会打印
5
6.7
现在，假设我们希望 `double` 值（且仅 `double` 值）以科学计数法输出。
获取给定类型不同行为的一种方法是定义一个非模板函数
#include <iostream>

template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

void print(double d)
{
    std::cout << std::scientific << d << '\n';
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
当编译器解析 `print(6.7)` 时，它会看到 `print(double)` 已经被我们定义，并使用它而不是从 `print(const T&)` 实例化一个版本。
这会产生结果
5
6.700000e+000
以这种方式定义函数的一个优点是，非模板函数不需要与函数模板具有相同的签名。请注意，`print(const T&)` 使用 const 引用传递，而 `print(double)` 使用值传递。
通常，如果可行，首选定义一个非模板函数。
函数模板特化
实现类似结果的另一种方法是使用显式模板特化。
显式模板特化
（通常简称为
模板特化
）是一种允许我们为特定类型或值显式定义模板不同实现的功能。当所有模板参数都被特化时，它被称为
完全特化
。当只有部分模板参数被特化时，它被称为
部分特化
。
当 `T` 是 `double` 时，我们来为 `print
` 创建一个特化
#include <iostream>

// Here's our primary template (must come first)
template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

// A full specialization of primary template print<T> for type double
// Full specializations are not implicitly inline, so make this inline if put in header file
template<>                          // template parameter declaration containing no template parameters 
void print<double>(const double& d) // specialized for type double
{
    std::cout << std::scientific << d << '\n'; 
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
为了特化模板，编译器首先必须已经看到了主模板的声明。上面示例中的主模板是 `print
(const T&)`。
现在，我们仔细看看我们的函数模板特化
template<>                          // template parameter declaration containing no template parameters 
void print<double>(const double& d) // specialized for type double
首先，我们需要一个模板参数声明，这样编译器就知道我们正在做与模板相关的事情。但是，在这种情况下，我们实际上不需要任何模板参数，所以我们使用一对空的尖括号。由于特化中没有模板参数，因此这是一个完全特化。
在下一行中，`print
` 告诉编译器我们正在为 `double` 类型特化 `print` 主模板函数。特化必须与主模板具有相同的签名（除了特化将 `double` 替换为主模板中使用 `T` 的任何位置）。因为主模板的参数类型为 `const T&`，所以特化必须具有 `const double&` 类型的参数。当主模板使用引用传递时，特化不能使用值传递（反之亦然）。
此示例打印与上面相同的结果。
请注意，如果同时存在匹配的非模板函数和匹配的模板函数特化，则非模板函数将优先。此外，完全特化不是隐式内联的，因此如果您在头文件中定义它，请确保将其 `inline` 以避免 ODR 违规。
警告
完全特化不是隐式内联的（部分特化是隐式内联的）。如果您将完全特化放在头文件中，它应该被标记为 `inline`，这样当它被包含到多个翻译单元时就不会导致 ODR 违规。
就像普通函数一样，如果您希望任何解析为特化的函数调用都产生编译错误，则可以删除函数模板特化（使用 `= delete`）。
通常，应尽可能避免函数模板特化，而倾向于使用非模板函数。
成员函数的函数模板特化？
现在考虑以下类模板
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    // Define some storage units
    Storage i { 5 };
    Storage d { 6.7 };

    // Print out some values
    i.print();
    d.print();
}
这会打印
5
6.7
假设我们再次想创建一个 `print()` 函数的版本，该版本以科学计数法打印双精度浮点数。但是，这次 `print()` 是一个成员函数，因此我们无法定义一个非成员函数。那么我们该怎么做呢？
虽然看起来我们需要在这里使用函数模板特化，但那是一个错误的工具。请注意，`i.print()` 调用 `Storage
::print()`，而 `d.print()` 调用 `Storage
::print()`。因此，如果我们想在 `T` 是 `double` 时改变这个函数的行为，我们需要特化 `Storage
::print()`，这是一个类模板特化，而不是函数模板特化！
那么我们该怎么做呢？我们将在下一课中介绍类模板特化。
下一课
26.4
类模板特化
返回目录
上一课
26.2
模板非类型参数