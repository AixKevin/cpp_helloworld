# 26.4 — 类模板特化

26.4 — 类模板特化
Alex
2008 年 8 月 16 日，太平洋夏令时下午 2:25
2024 年 7 月 5 日
在上一课
26.3 -- 函数模板特化
中，我们了解了如何特化函数以针对特定数据类型提供不同的功能。事实证明，不仅可以特化函数，还可以特化类！
考虑您需要一个存储 8 个对象的类的情况。下面是一个简化的类模板来实现这一点：
#include <iostream>

template <typename T>
class Storage8
{
private:
    T m_array[8];

public:
    void set(int index, const T& value)
    {
        m_array[index] = value;
    }

    const T& get(int index) const
    {
        return m_array[index];
    }
};

int main()
{
    // Define a Storage8 for integers
    Storage8<int> intStorage;

    for (int count{ 0 }; count < 8; ++count)
        intStorage.set(count, count);

    for (int count{ 0 }; count < 8; ++count)
        std::cout << intStorage.get(count) << '\n';

    // Define a Storage8 for bool
    Storage8<bool> boolStorage;
    for (int count{ 0 }; count < 8; ++count)
        boolStorage.set(count, count & 3);

	std::cout << std::boolalpha;

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << boolStorage.get(count) << '\n';
    }

    return 0;
}
此示例输出：
0
1
2
3
4
5
6
7
false
true
true
true
false
true
true
true
虽然这个类完全功能，但事实证明，
Storage8<bool>
的实现比它需要的更低效。因为所有变量都必须有一个地址，并且 CPU 不能寻址小于一个字节的任何东西，所以所有变量都必须至少是一个字节大小。因此，一个
bool
类型的变量最终会使用整个字节，尽管从技术上讲，它只需要一位来存储其真或假值！因此，一个
bool
是 1 位有用信息和 7 位浪费空间。我们的
Storage8<bool>
类包含 8 个
bool
，是 1 字节有用信息和 7 字节浪费空间。
事实证明，使用一些基本的位逻辑，可以将所有 8 个布尔值压缩到一个字节中，从而完全消除浪费的空间。然而，为了做到这一点，当与
bool
类型一起使用时，我们需要改造这个类，用一个单字节大小的变量替换 8 个
bool
的数组。虽然我们可以创建一个全新的类来做到这一点，但这有一个主要缺点：我们必须给它一个不同的名称。然后程序员必须记住
Storage8<T>
适用于非布尔类型，而
Storage8Bool
（或我们给新类起的任何名称）适用于
bool
。这是我们宁愿避免的不必要的复杂性。幸运的是，C++ 为我们提供了一个更好的方法：类模板特化。
类模板特化
类模板特化允许我们为特定数据类型（或多种数据类型，如果有多个模板参数）特化模板类。在这种情况下，我们将使用类模板特化来编写
Storage8<bool>
的定制版本，该版本将优先于通用
Storage8<T>
类。
类模板特化被视为完全独立的类，即使它们以与模板化类相同的方式实例化。这意味着我们可以改变特化类的任何和所有内容，包括它的实现方式，甚至它公开的函数，就像它是一个独立的类一样。
就像所有模板一样，编译器必须能够看到特化的完整定义才能使用它。此外，定义类模板特化要求首先定义非特化类。
以下是特化的
Storage8<bool>
类的示例：
#include <cstdint>

// First define our non-specialized class template
template <typename T>
class Storage8
{
private:
    T m_array[8];

public:
    void set(int index, const T& value)
    {
        m_array[index] = value;
    }

    const T& get(int index) const
    {
        return m_array[index];
    }
};

// Now define our specialized class template
template <> // the following is a template class with no templated parameters
class Storage8<bool> // we're specializing Storage8 for bool
{
// What follows is just standard class implementation details

private:
    std::uint8_t m_data{};

public:
    // Don't worry about the details of the implementation of these functions
    void set(int index, bool value)
    {
        // Figure out which bit we're setting/unsetting
        // This will put a 1 in the bit we're interested in turning on/off
        auto mask{ 1 << index };

        if (value)  // If we're setting a bit
            m_data |= mask;   // use bitwise-or to turn that bit on
        else  // if we're turning a bit off
            m_data &= ~mask;  // bitwise-and the inverse mask to turn that bit off
	}
	
    bool get(int index)
    {
        // Figure out which bit we're getting
        auto mask{ 1 << index };
        // bitwise-and to get the value of the bit we're interested in
        // Then implicit cast to boolean
        return (m_data & mask);
    }
};

// Same example as before
int main()
{
    // Define a Storage8 for integers (instantiates Storage8<T>, where T = int)
    Storage8<int> intStorage;

    for (int count{ 0 }; count < 8; ++count)
    {
        intStorage.set(count, count);
	}

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << intStorage.get(count) << '\n';
    }

    // Define a Storage8 for bool  (instantiates Storage8<bool> specialization)
    Storage8<bool> boolStorage;
    
    for (int count{ 0 }; count < 8; ++count)
    {
        boolStorage.set(count, count & 3);
    }

	std::cout << std::boolalpha;

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << boolStorage.get(count) << '\n';
    }

    return 0;
}
首先，请注意我们的特化类模板以
template<>
开头。
template
关键字告诉编译器后面是一个模板，而空尖括号表示没有模板参数。在这种情况下，没有模板参数，因为我们用特定类型（
bool
）替换了唯一的模板参数（
T
）。
接下来，我们在类名后面添加
<bool>
，表示我们正在特化
class Storage8
的
bool
版本。
所有其他更改都只是类实现细节。您不需要理解位逻辑是如何工作的才能使用该类（尽管如果您想了解它，但需要复习位运算符的工作原理，可以查阅
O.2 -- 位运算符
）。
请注意，这个特化类使用
std::uint8_t
（1 字节无符号整数）而不是 8 个
bool
的数组（8 字节）。
现在，当我们实例化一个
Storage<T>
类型的对象，其中
T
不是
bool
时，我们将获得从通用模板化
Storage8<T>
类模板化的版本。当我们实例化一个
Storage8<bool>
类型的对象时，我们将获得我们刚刚创建的特化版本。请注意，我们保持了两个类公开的接口相同——虽然 C++ 允许我们自由添加、删除或更改
Storage8<bool>
的函数，但保持一致的接口意味着程序员可以以完全相同的方式使用这两个类。
正如您可能预期的那样，这打印出与使用非特化版本
Storage8<bool>
的先前示例相同的结果：
0
1
2
3
4
5
6
7
false
true
true
true
false
true
true
true
特化成员函数
在上一课中，我们介绍了这个例子：
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
我们的愿望是特化
print()
函数，使其以科学记数法打印双精度浮点数。使用类模板特化，我们可以为
Storage<double>
定义一个特化类：
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

// Explicit class template specialization for Storage<double>
// Note how redundant this is
template <>
class Storage<double>
{
private:
    double m_value {};
public:
    Storage(double value)
      : m_value { value }
    {
    }

    void print();
};

// We're going to define this outside the class for reasons that will become obvious shortly
// This is a normal (non-specialized) member function definition (for member function print of specialized class Storage<double>)
void Storage<double>::print()
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // Define some storage units
    Storage i { 5 };
    Storage d { 6.7 }; // uses explicit specialization Storage<double>

    // Print out some values
    i.print(); // calls Storage<int>::print (instantiated from Storage<T>)
    d.print(); // calls Storage<double>::print (called from explicit specialization of Storage<double>)
}
然而，请注意这里有多少冗余。我们只是为了改变一个成员函数而复制了整个类定义！
幸运的是，我们可以做得更好。C++ 不需要我们显式特化
Storage<double>
来显式特化
Storage<double>::print()
。相反，我们可以让编译器从
Storage<T>
隐式特化
Storage<double>
，并提供一个只针对
Storage<double>::print()
的显式特化！下面是它的样子：
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

// This is a specialized member function definition
// Explicit function specializations are not implicitly inline, so make this inline if put in header file
template<>
void Storage<double>::print()
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // Define some storage units
    Storage i { 5 };
    Storage d { 6.7 }; // will cause Storage<double> to be implicitly instantiated

    // Print out some values
    i.print(); // calls Storage<int>::print (instantiated from Storage<T>)
    d.print(); // calls Storage<double>::print (called from explicit specialization of Storage<double>::print())
}
就是这样！
如前一课 (
26.3 -- 函数模板特化
) 中所述，显式函数特化不是隐式内联的，因此如果我们在头文件中定义
Storage<double>::print()
的特化，则应该将其标记为内联。
在哪里定义类模板特化
为了使用特化，编译器必须能够看到非特化类和特化类的完整定义。如果编译器只能看到非特化类的定义，它将使用非特化类而不是特化。
因此，特化类和函数通常定义在头文件中，紧跟在非特化类的定义之后，以便包含单个头文件即可包含非特化类和任何特化。这确保了只要非特化类可见，特化也始终可见。
如果特化只在单个翻译单元中需要，则可以在该翻译单元的源文件中定义它。因为其他翻译单元将无法看到特化的定义，它们将继续使用非特化版本。
请注意不要将特化放在自己的单独头文件中，并打算在需要特化的任何翻译单元中包含特化的头文件。设计基于头文件的存在或缺失而透明地改变行为的代码是一个坏主意。例如，如果您打算使用特化但忘记包含特化的头文件，您最终可能会使用非特化版本。如果您打算使用非特化版本，如果其他头文件通过传递性包含方式包含特化，您可能最终仍然会使用特化。
下一课
26.5
偏模板特化
返回目录
上一课
26.3
函数模板特化