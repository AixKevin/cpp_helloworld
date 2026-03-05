# 26.1 — 模板类

26.1 — 模板类
Alex
2008 年 6 月 16 日，太平洋夏令时晚上 8:04
2024 年 7 月 23 日
在上一章中，我们介绍了函数模板（
11.6 -- 函数模板
），它允许我们概括函数以适用于多种不同的数据类型。虽然这是走向泛化编程的一个很好的开端，但它并不能解决我们所有的问题。让我们看一个这种问题的例子，看看模板还能为我们做些什么。
模板与容器类
在关于
23.6 -- 容器类
的课程中，您学习了如何使用组合来实现包含其他类多个实例的类。作为这种容器的一个例子，我们考察了 IntArray 类。以下是该类的一个简化示例
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert>

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:

    IntArray(int length)
    {
        assert(length > 0);
        m_data = new int[length]{};
        m_length = length;
    }

    // We don't want to allow copies of IntArray to be created.
    IntArray(const IntArray&) = delete;
    IntArray& operator=(const IntArray&) = delete;

    ~IntArray()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // We need to make sure we set m_data to 0 here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
虽然这个类提供了一种创建整数数组的简单方法，但如果我们想创建双精度浮点数数组呢？使用传统的编程方法，我们将不得不创建一个全新的类！以下是 DoubleArray 的一个示例，这是一个用于存储双精度浮点数的数组类。
#ifndef DOUBLEARRAY_H
#define DOUBLEARRAY_H

#include <cassert>

class DoubleArray
{
private:
    int m_length{};
    double* m_data{};

public:

    DoubleArray(int length)
    {
        assert(length > 0);
        m_data = new double[length]{};
        m_length = length;
    }

    DoubleArray(const DoubleArray&) = delete;
    DoubleArray& operator=(const DoubleArray&) = delete;

    ~DoubleArray()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // We need to make sure we set m_data to 0 here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }

    double& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
尽管代码列表很长，但您会注意到这两个类几乎完全相同！事实上，唯一的实质性区别是包含的数据类型（int vs double）。正如您可能已经猜到的那样，这是模板可以很好地发挥作用的另一个领域，它使我们不必创建绑定到特定数据类型的类。
创建模板类与创建模板函数几乎完全相同，因此我们将通过示例进行说明。这是我们的数组类，模板版本
Array.h
#ifndef ARRAY_H
#define ARRAY_H

#include <cassert>

template <typename T> // added
class Array
{
private:
    int m_length{};
    T* m_data{}; // changed type to T

public:

    Array(int length)
    {
        assert(length > 0);
        m_data = new T[length]{}; // allocated an array of objects of type T
        m_length = length;
    }

    Array(const Array&) = delete;
    Array& operator=(const Array&) = delete;

    ~Array()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // We need to make sure we set m_data to 0 here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }

    // templated operator[] function defined below
    T& operator[](int index); // now returns a T&

    int getLength() const { return m_length; }
};

// member functions defined outside the class need their own template declaration
template <typename T>
T& Array<T>::operator[](int index) // now returns a T&
{
    assert(index >= 0 && index < m_length);
    return m_data[index];
}

#endif
如您所见，此版本与 IntArray 版本几乎相同，只是我们添加了模板声明，并将包含的数据类型从 int 更改为 T。
请注意，我们还将 `operator[]` 函数定义在类声明之外。这并非必要，但新程序员在首次尝试这样做时通常会因为语法而感到困惑，因此提供一个示例是有益的。在类声明之外定义的每个模板成员函数都需要自己的模板声明。此外，请注意，模板数组类的名称是 Array
，而不是 Array —— Array 将指代名为 Array 的非模板类版本，除非 Array 在类内部使用。例如，复制构造函数和复制赋值运算符使用了 Array 而不是 Array
。当类名在类内部不带模板参数使用时，参数与当前实例化的参数相同。
以下是使用上述模板数组类的一个简短示例
#include <iostream>
#include "Array.h"

int main()
{
	const int length { 12 };
	Array<int> intArray { length };
	Array<double> doubleArray { length };

	for (int count{ 0 }; count < length; ++count)
	{
		intArray[count] = count;
		doubleArray[count] = count + 0.5;
	}

	for (int count{ length - 1 }; count >= 0; --count)
		std::cout << intArray[count] << '\t' << doubleArray[count] << '\n';

	return 0;
}
这个例子打印以下内容
11     11.5
10     10.5
9       9.5
8       8.5
7       7.5
6       6.5
5       5.5
4       4.5
3       3.5
2       2.5
1       1.5
0       0.5
模板类的实例化方式与模板函数相同——编译器按需复制出一份副本，将模板参数替换为用户所需的实际数据类型，然后编译该副本。如果您从不使用模板类，编译器甚至不会编译它。
模板类非常适合实现容器类，因为它非常需要容器能够处理各种数据类型，而模板允许您在不重复代码的情况下实现这一点。尽管语法丑陋，错误消息可能晦涩难懂，但模板类确实是 C++ 最优秀和最有用的特性之一。
拆分模板类
模板不是类或函数——它是用于创建类或函数的模板。因此，它的工作方式与普通函数或类不完全相同。在大多数情况下，这并不是一个大问题。但是，有一个领域经常给开发人员带来问题。
对于非模板类，通常的做法是将类定义放在头文件中，将成员函数定义放在类似命名的代码文件中。这样，成员函数定义就作为单独的项目文件进行编译。但是，对于模板，这行不通。考虑以下情况
Array.h
#ifndef ARRAY_H
#define ARRAY_H

#include <cassert>

template <typename T> // added
class Array
{
private:
    int m_length{};
    T* m_data{}; // changed type to T

public:

    Array(int length)
    {
        assert(length > 0);
        m_data = new T[length]{}; // allocated an array of objects of type T
        m_length = length;
    }

    Array(const Array&) = delete;
    Array& operator=(const Array&) = delete;

    ~Array()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // We need to make sure we set m_data to 0 here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }

    // templated operator[] function defined below
    T& operator[](int index); // now returns a T&

    int getLength() const { return m_length; }
};

// Definition of Array<T>::operator[] moved into Array.cpp below

#endif
Array.cpp
#include "Array.h"

// member functions defined outside the class need their own template declaration
template <typename T>
T& Array<T>::operator[](int index) // now returns a T&
{
    assert(index >= 0 && index < m_length);
    return m_data[index];
}
main.cpp
#include <iostream>
#include "Array.h"

int main()
{
	const int length { 12 };
	Array<int> intArray { length };
	Array<double> doubleArray { length };

	for (int count{ 0 }; count < length; ++count)
	{
		intArray[count] = count;
		doubleArray[count] = count + 0.5;
	}

	for (int count{ length - 1 }; count >= 0; --count)
		std::cout << intArray[count] << '\t' << doubleArray[count] << '\n';

	return 0;
}
上面的程序将编译，但会导致链接器错误
undefined reference to `Array<int>::operator[](int)'
就像函数模板一样，只有当类模板在转换单元中使用时（例如作为 intArray 这种对象的类型），编译器才会实例化它。为了执行实例化，编译器必须同时看到完整的类模板定义（不仅仅是声明）和所需的特定模板类型。
还要记住 C++ 是单独编译文件的。当 main.cpp 被编译时，Array.h 头文件的内容（包括模板类定义）被复制到 main.cpp 中。当编译器发现我们需要两个模板实例 Array
和 Array
时，它会实例化它们，并将它们作为 main.cpp 转换单元的一部分进行编译。因为 `operator[]` 成员函数有一个声明，所以编译器会接受对其的调用，假设它会在其他地方定义。
当 Array.cpp 单独编译时，Array.h 头文件的内容被复制到 Array.cpp 中，但编译器在 Array.cpp 中找不到任何需要实例化 Array 类模板或 `Array
::operator[]` 函数模板的代码——所以它不会实例化任何东西。
因此，当程序链接时，我们将得到一个链接器错误，因为 main.cpp 调用了 `Array
::operator[]`，但该模板函数从未被实例化！
有相当多的方法可以解决这个问题。
最简单的方法是直接将所有模板类代码放入头文件（在这种情况下，将 Array.cpp 的内容放入 Array.h 中，位于类定义下方）。这样，当您 #include 头文件时，所有模板代码都将集中在一处。这种解决方案的优点是简单。缺点是如果模板类在许多文件中使用，您最终会得到许多模板类的本地实例，这可能会增加您的编译和链接时间（您的链接器应该会删除重复的定义，因此它不应该使您的可执行文件膨胀）。这是我们首选的解决方案，除非编译或链接时间开始成为问题。
如果您觉得将 Array.cpp 代码放入 Array.h 头文件会使头文件过长/混乱，一种替代方法是将 Array.cpp 的内容移动到一个名为 Array.inl 的新文件（.inl 代表 inline），然后在 Array.h 头文件的底部（在头文件保护内部）包含 Array.inl。这会产生与将所有代码放入头文件相同的结果，但有助于使事物更有条理。
提示
如果你使用 .inl 方法，然后遇到关于重复定义的编译器错误，你的编译器很可能将 .inl 文件作为项目的一部分进行编译，就好像它是一个代码文件一样。这会导致 .inl 的内容被编译两次：一次是当你的编译器编译 .inl 时，另一次是当包含 .inl 的 .cpp 文件被编译时。如果 .inl 文件包含任何非内联函数（或变量），那么我们将违反一次定义规则。如果发生这种情况，你需要将 .inl 文件排除在构建之外。
将 .inl 文件从构建中排除通常可以通过在项目视图中右键单击 .inl 文件，然后选择属性来完成。设置将在其中。在 Visual Studio 中，将“从构建中排除”设置为“是”。在 Code::Blocks 中，取消选中“编译文件”和“链接文件”。
其他解决方案涉及 #include .cpp 文件，但我们不推荐这些，因为 #include 的用法不符合标准。
另一种替代方案是使用三文件方法。模板类定义放在头文件中。模板类成员函数放在代码文件中。然后您添加第三个文件，其中包含您需要的所有实例化类
templates.cpp
// Ensure the full Array template definition can be seen
#include "Array.h"
#include "Array.cpp" // we're breaking best practices here, but only in this one place

// #include other .h and .cpp template definitions you need here

template class Array<int>; // Explicitly instantiate template Array<int>
template class Array<double>; // Explicitly instantiate template Array<double>

// instantiate other templates here
“template class”命令使编译器显式实例化模板类。在上面的例子中，编译器将在 templates.cpp 内部为 Array
和 Array
刻画出定义。其他想要使用这些类型的代码文件可以包含 Array.h（以满足编译器），链接器将从 template.cpp 链接这些显式类型定义。
此方法可能更有效率（取决于您的编译器和链接器如何处理模板和重复定义），但需要为每个程序维护 templates.cpp 文件。
下一课
26.2
模板非类型参数
返回目录
上一课
25.x
第 25 章总结与测验