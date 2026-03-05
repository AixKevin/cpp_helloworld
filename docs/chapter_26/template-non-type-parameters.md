# 26.2 — 模板非类型参数

26.2 — 模板非类型参数
Alex
2008年6月19日，太平洋夏令时晚上7:07
2023年9月11日
在之前的课程中，你已经学会了如何使用模板类型参数来创建与类型无关的函数和类。模板类型参数是一个占位符类型，它会被作为参数传入的类型所替代。
然而，模板类型参数并不是唯一可用的模板参数类型。模板类和函数可以利用另一种模板参数，称为非类型参数。
非类型参数
模板非类型参数是一种模板参数，其中参数的类型是预定义的，并被作为参数传入的 constexpr 值所替代。
非类型参数可以是以下任何类型：
整型
枚举类型
指向类对象的指针或引用
指向函数的指针或引用
指向类成员函数的指针或引用
std::nullptr_t
浮点类型 (自 C++20 起)
在下面的示例中，我们创建了一个非动态（静态）数组类，它同时使用了类型参数和非类型参数。类型参数控制静态数组的数据类型，而整型非类型参数控制静态数组的大小。
#include <iostream>

template <typename T, int size> // size is an integral non-type parameter
class StaticArray
{
private:
    // The non-type parameter controls the size of the array
    T m_array[size] {};

public:
    T* getArray();
	
    T& operator[](int index)
    {
        return m_array[index];
    }
};

// Showing how a function for a class with a non-type parameter is defined outside of the class
template <typename T, int size>
T* StaticArray<T, size>::getArray()
{
    return m_array;
}

int main()
{
    // declare an integer array with room for 12 integers
    StaticArray<int, 12> intArray;

    // Fill it up in order, then print it backwards
    for (int count { 0 }; count < 12; ++count)
        intArray[count] = count;

    for (int count { 11 }; count >= 0; --count)
        std::cout << intArray[count] << ' ';
    std::cout << '\n';

    // declare a double buffer with room for 4 doubles
    StaticArray<double, 4> doubleArray;

    for (int count { 0 }; count < 4; ++count)
        doubleArray[count] = 4.4 + 0.1 * count;

    for (int count { 0 }; count < 4; ++count)
        std::cout << doubleArray[count] << ' ';

    return 0;
}
此代码产生以下输出：
11 10 9 8 7 6 5 4 3 2 1 0
4.4 4.5 4.6 4.7
上述示例中值得注意的一点是，我们无需动态分配 m_array 成员变量！这是因为对于 StaticArray 类的任何给定实例，size 必须是 constexpr。例如，如果你实例化一个 StaticArray<int, 12>，编译器会将 size 替换为 12。因此 m_array 的类型是 int[12]，可以静态分配。
此功能被标准库类 std::array 使用。当你分配一个 std::array<int, 5> 时，int 是一个类型参数，而 5 是一个非类型参数！
请注意，如果你尝试使用非 constexpr 值实例化模板非类型参数，它将不起作用。
template <int size>
class Foo
{
};

int main()
{
    int x{ 4 }; // x is non-constexpr
    Foo<x> f; // error: the template non-type argument must be constexpr

    return 0;
}
在这种情况下，你的编译器将发出错误。
下一课
26.3
函数模板特化
返回目录
上一课
26.1
模板类