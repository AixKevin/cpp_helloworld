# 26.5 — 局部模板特化

26.5 — 局部模板特化
Alex
2008年8月17日，下午6:59 PDT
2024年3月16日
本课程和下一课程是为那些希望更深入了解 C++ 模板的人提供的可选阅读材料。局部模板特化并不常用（但在特定情况下可能很有用）。
在课程
26.2 -- 模板非类型参数
中，你学习了如何使用表达式参数来参数化模板类。
让我们再看看我们之前示例中使用的 Static Array 类
template <typename T, int size> // size is the expression parameter
class StaticArray
{
private:
    // The expression parameter controls the size of the array
    T m_array[size]{};
 
public:
    T* getArray() { return m_array; }
	
    const T& operator[](int index) const { return m_array[index]; }
    T& operator[](int index) { return m_array[index]; }
};
这个类接受两个模板参数：一个类型参数和一个表达式参数。
现在，假设我们想编写一个函数来打印整个数组。虽然我们可以将其实现为成员函数，但我们将其实现为非成员函数，因为这样可以更容易地理解后续示例。
使用模板，我们可以这样写
template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
    for (int count{ 0 }; count < size; ++count)
        std::cout << array[count] << ' ';
}
这将允许我们进行以下操作
#include <iostream>

template <typename T, int size> // size is a template non-type parameter
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

int main()
{
	// declare an int array
	StaticArray<int, 4> int4{};
	int4[0] = 0;
	int4[1] = 1;
	int4[2] = 2;
	int4[3] = 3;

	// Print the array
	print(int4);

	return 0;
}
并获得以下结果
0 1 2 3
尽管这可行，但它有一个设计缺陷。考虑以下情况
#include <algorithm>
#include <iostream>
#include <string_view>

int main()
{
    // Declare a char array
    StaticArray<char, 14> char14{};

    // Copy some data into it
    constexpr std::string_view hello{ "Hello, world!" };
    std::copy_n(hello.begin(), hello.size(), char14.getArray());

    // Print the array
    print(char14);

    return 0;
}
（如果你需要复习，我们在课程
17.10 -- C 风格字符串
中介绍了 std::strcpy）
该程序将编译、执行并产生以下值（或类似值）
H e l l o ,   w o r l d !
对于非 char 类型，在每个数组元素之间放置一个空格是有意义的，这样它们就不会连在一起。然而，对于 char 类型，将所有内容连在一起作为 C 风格字符串打印更有意义，而我们的 print() 函数没有这样做。
那么我们该如何解决这个问题呢？
模板特化来救援？
人们可能首先想到使用模板特化。完全模板特化的问题在于，所有模板参数都必须明确定义。
考虑
#include <algorithm>
#include <iostream>
#include <string_view>

template <typename T, int size> // size is the expression parameter
class StaticArray
{
private:
	// The expression parameter controls the size of the array
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

// Override print() for fully specialized StaticArray<char, 14>
template <>
void print(const StaticArray<char, 14>& array)
{
	for (int count{ 0 }; count < 14; ++count)
		std::cout << array[count];
}

int main()
{
    // Declare a char array
    StaticArray<char, 14> char14{};

    // Copy some data into it
    constexpr std::string_view hello{ "Hello, world!" };
    std::copy_n(hello.begin(), hello.size(), char14.getArray());

    // Print the array
    print(char14);

    return 0;
}
如你所见，我们现在为完全特化的
StaticArray
提供了一个重载的 print 函数。事实上，它打印出来是
Hello, world!
尽管这解决了确保 print() 可以与
StaticArray
一起调用的问题，但它带来了另一个问题：使用完全模板特化意味着我们必须明确定义此函数将接受的数组长度！考虑以下示例
int main()
{
    // Declare a char array
    StaticArray<char, 12> char12{};

    // Copy some data into it
    constexpr std::string_view hello{ "Hello, mom!" };
    std::copy_n(hello.begin(), hello.size(), char12.getArray());

    // Print the array
    print(char12);

    return 0;
}
使用
char12
调用
print()
将调用接受
StaticArray
版本的
print()
，因为
char12
的类型是
StaticArray
，而我们的重载 print() 只会在传递
StaticArray
时被调用。
虽然我们可以复制一个处理
StaticArray
的 print()，但是当我们想用大小为 5 或 22 的数组调用 print() 时会发生什么？我们必须为每个不同的数组大小复制函数。这是多余的。
显然，完全模板特化在这里是过于限制性的解决方案。我们正在寻找的解决方案是局部模板特化。
局部模板特化
局部模板特化允许我们特化类（但不能特化单个函数！），其中一些但不是所有模板参数都已明确定义。对于我们上面的挑战，理想的解决方案是让我们的重载 print 函数与 char 类型的 StaticArray 一起工作，但让长度表达式参数模板化，以便它可以在需要时改变。局部模板特化允许我们做到这一点！
这是我们的示例，其中一个重载的 print 函数接受一个局部特化的 StaticArray
// overload of print() function for partially specialized StaticArray<char, size>
template <int size> // size is still a template non-type parameter
void print(const StaticArray<char, size>& array) // we're explicitly defining type char here
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count];
}
如你所见，我们明确声明此函数仅适用于 char 类型的 StaticArray，但大小仍然是一个模板化的表达式参数，因此它将适用于任何大小的 char 数组。就是这样！
这是一个使用它的完整程序
#include <algorithm>
#include <iostream>
#include <string_view>

template <typename T, int size> // size is the expression parameter
class StaticArray
{
private:
	// The expression parameter controls the size of the array
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

// overload of print() function for partially specialized StaticArray<char, size>
template <int size>
void print(const StaticArray<char, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count];
}

int main()
{
	// Declare an char array of size 14
	StaticArray<char, 14> char14{};

	// Copy some data into it
	constexpr std::string_view hello14{ "Hello, world!" };
	std::copy_n(hello14.begin(), hello14.size(), char14.getArray());

	// Print the array
	print(char14);

	std::cout << ' ';

	// Now declare an char array of size 12
	StaticArray<char, 12> char12{};

	// Copy some data into it
	constexpr std::string_view hello12{ "Hello, mom!" };
	std::copy_n(hello12.begin(), hello12.size(), char12.getArray());

	// Print the array
	print(char12);

	return 0;
}
这会打印
Hello, world! Hello, mom!
正如我们所期望的。
局部模板特化只能用于类，不能用于模板函数（函数必须完全特化）。我们的
void print(StaticArray
&array)
示例之所以有效，是因为 print 函数没有局部特化（它只是一个重载的模板函数，恰好有一个局部特化的类参数）。
成员函数的局部模板特化
函数局部特化的限制可能会在处理成员函数时导致一些挑战。例如，如果我们这样定义 StaticArray 会怎样？
template <typename T, int size>
class StaticArray
{
private:
    T m_array[size]{};
 
public:
    T* getArray() { return m_array; }
	
    const T& operator[](int index) const { return m_array[index]; }
    T& operator[](int index) { return m_array[index]; }

    void print() const;
};

template <typename T, int size> 
void StaticArray<T, size>::print() const
{
    for (int i{ 0 }; i < size; ++i)
        std::cout << m_array[i] << ' ';
    std::cout << '\n';
}
print() 现在是类
StaticArray
的一个成员函数。那么当我们想要局部特化 print()，使其以不同方式工作时会发生什么？你可能会尝试这样做
// Doesn't work, can't partially specialize functions
template <int size>
void StaticArray<double, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << std::scientific << m_array[i] << ' ';
	std::cout << '\n';
}
不幸的是，这不起作用，因为我们正在尝试局部特化一个函数，这是不允许的。
那么我们如何解决这个问题呢？一个明显的方法是局部特化整个类
#include <iostream>

template <typename T, int size>
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }

	void print() const;
};

template <typename T, int size> 
void StaticArray<T, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << m_array[i] << ' ';
	std::cout << '\n';
}

// Partially specialized class
template <int size>
class StaticArray<double, size>
{
private:
	double m_array[size]{};

public:
	double* getArray() { return m_array; }

	const double& operator[](int index) const { return m_array[index]; }
	double& operator[](int index) { return m_array[index]; }

	void print() const;
};

// Member function of partially specialized class
template <int size>
void StaticArray<double, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << std::scientific << m_array[i] << ' ';
	std::cout << '\n';
}

int main()
{
	// declare an integer array with room for 6 integers
	StaticArray<int, 6> intArray{};

	// Fill it up in order, then print it
	for (int count{ 0 }; count < 6; ++count)
		intArray[count] = count;

	intArray.print();

	// declare a double buffer with room for 4 doubles
	StaticArray<double, 4> doubleArray{};

	for (int count{ 0 }; count < 4; ++count)
		doubleArray[count] = (4.0 + 0.1 * count);

	doubleArray.print();

	return 0;
}
这会打印
0 1 2 3 4 5
4.000000e+00 4.100000e+00 4.200000e+00 4.300000e+00
这之所以有效，是因为
StaticArray
::print()
不再是一个局部特化的函数——它是局部特化类
StaticArray
的一个非特化成员。
然而，这不是一个好的解决方案，因为我们必须从
StaticArray
到
StaticArray
复制大量代码。
如果有一种方法可以在
StaticArray
中重用
StaticArray
中的代码就好了。这听起来像是继承的工作！
你可能会尝试这样编写代码
template <int size> // size is the expression parameter
class StaticArray<double, size>: public StaticArray<T, size>
但这不起作用，因为我们使用了
T
但没有定义它。没有允许我们以这种方式继承的语法。
题外话…
即使我们能够将
T
定义为类型模板参数，当实例化
StaticArray
时，编译器也需要用实际类型替换
StaticArray
中的
T
。它会使用什么实际类型？唯一有意义的类型是
T=double
，但这将导致
StaticArray
继承自它自己！
幸运的是，有一种解决方法，通过使用一个公共基类
#include <iostream>

template <typename T, int size>
class StaticArray_Base
{
protected:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }

	void print() const
	{
		for (int i{ 0 }; i < size; ++i)
			std::cout << m_array[i] << ' ';
		std::cout << '\n';
	}

	// Don't forget a virtual destructor if you're going to use virtual function resolution
};

template <typename T, int size>
class StaticArray: public StaticArray_Base<T, size>
{
};

template <int size>
class StaticArray<double, size>: public StaticArray_Base<double, size>
{
public:

	void print() const
	{
		for (int i{ 0 }; i < size; ++i)
			std::cout << std::scientific << this->m_array[i] << ' ';
// note: The this-> prefix in the above line is needed.
// See https://stackoverflow.com/a/6592617 or https://isocpp.org.cn/wiki/faq/templates#nondependent-name-lookup-members for more info on why.
		std::cout << '\n';
	}
};

int main()
{
	// declare an integer array with room for 6 integers
	StaticArray<int, 6> intArray{};

	// Fill it up in order, then print it
	for (int count{ 0 }; count < 6; ++count)
		intArray[count] = count;

	intArray.print();

	// declare a double buffer with room for 4 doubles
	StaticArray<double, 4> doubleArray{};

	for (int count{ 0 }; count < 4; ++count)
		doubleArray[count] = (4.0 + 0.1 * count);

	doubleArray.print();

	return 0;
}
这与上面打印相同，但重复的代码明显更少。
下一课
26.6
指针的局部模板特化
返回目录
上一课
26.4
类模板特化