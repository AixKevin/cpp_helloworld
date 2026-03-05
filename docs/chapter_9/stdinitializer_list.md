# 23.7 — std::initializer_list

23.7 — std::initializer_list
Alex
2017年3月9日，太平洋标准时间下午6:32
2024年6月5日
考虑C++中的一个固定整数数组
int array[5];
如果我们想用值来初始化这个数组，我们可以直接通过初始化列表语法来完成
#include <iostream>

int main()
{
	int array[] { 5, 4, 3, 2, 1 }; // initializer list
	for (auto i : array)
		std::cout << i << ' ';

	return 0;
}
这会打印
5 4 3 2 1
这也适用于动态分配的数组
#include <iostream>

int main()
{
	auto* array{ new int[5]{ 5, 4, 3, 2, 1 } }; // initializer list
	for (int count{ 0 }; count < 5; ++count)
		std::cout << array[count] << ' ';
	delete[] array;

	return 0;
}
在上一课中，我们介绍了容器类的概念，并展示了一个IntArray类的例子，它包含一个整数数组
#include <cassert> // for assert()
#include <iostream>
 
class IntArray
{
private:
    int m_length{};
    int* m_data{};
 
public:
    IntArray() = default;
 
    IntArray(int length)
        : m_length{ length }
	, m_data{ new int[static_cast<std::size_t>(length)] {} }
    {
    }
 
    ~IntArray()
    {
        delete[] m_data;
        // we don't need to set m_data to null or m_length to 0 here, since the object will be destroyed immediately after this function anyway
    }
 
    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }
 
    int getLength() const { return m_length; }
};

int main()
{
	// What happens if we try to use an initializer list with this container class?
	IntArray array { 5, 4, 3, 2, 1 }; // this line doesn't compile
	for (int count{ 0 }; count < 5; ++count)
		std::cout << array[count] << ' ';

	return 0;
}
这段代码无法编译，因为IntArray类没有一个知道如何处理初始化列表的构造函数。结果，我们不得不单独初始化数组元素
int main()
{
	IntArray array(5);
	array[0] = 5;
	array[1] = 4;
	array[2] = 3;
	array[3] = 2;
	array[4] = 1;

	for (int count{ 0 }; count < 5; ++count)
		std::cout << array[count] << ' ';

	return 0;
}
这不太好。
使用std::initializer_list进行类初始化
当编译器看到初始化列表时，它会自动将其转换为std::initializer_list类型的对象。因此，如果我们创建一个接受std::initializer_list参数的构造函数，我们就可以使用初始化列表作为输入来创建对象。
std::initializer_list位于`<initializer_list>`头文件中。
关于std::initializer_list有几点需要了解。与std::array或std::vector非常相似，您必须使用尖括号告诉std::initializer_list列表中包含什么类型的数据，除非您立即初始化std::initializer_list。因此，您几乎永远不会看到一个普通的std::initializer_list。相反，您会看到类似`std::initializer_list<int>`或`std::initializer_list<std::string>`的类型。
其次，std::initializer_list有一个（命名不当的）size()函数，它返回列表中元素的数量。当我们想知道传入列表的长度时，这很有用。
第三，std::initializer_list通常通过值传递。就像std::string_view一样，std::initializer_list是一个视图。复制std::initializer_list不会复制列表中的元素。
让我们来看看用一个接受std::initializer_list的构造函数来更新我们的IntArray类。
#include <algorithm> // for std::copy
#include <cassert> // for assert()
#include <initializer_list> // for std::initializer_list
#include <iostream>

class IntArray
{
private:
	int m_length {};
	int* m_data{};

public:
	IntArray() = default;

	IntArray(int length)
		: m_length{ length }
		, m_data{ new int[static_cast<std::size_t>(length)] {} }
	{

	}

	IntArray(std::initializer_list<int> list) // allow IntArray to be initialized via list initialization
		: IntArray(static_cast<int>(list.size())) // use delegating constructor to set up initial array
	{
		// Now initialize our array from the list
		std::copy(list.begin(), list.end(), m_data);
	}

	~IntArray()
	{
		delete[] m_data;
		// we don't need to set m_data to null or m_length to 0 here, since the object will be destroyed immediately after this function anyway
	}

	IntArray(const IntArray&) = delete; // to avoid shallow copies
	IntArray& operator=(const IntArray& list) = delete; // to avoid shallow copies

	int& operator[](int index)
	{
		assert(index >= 0 && index < m_length);
		return m_data[index];
	}

	int getLength() const { return m_length; }
};

int main()
{
	IntArray array{ 5, 4, 3, 2, 1 }; // initializer list
	for (int count{ 0 }; count < array.getLength(); ++count)
		std::cout << array[count] << ' ';

	return 0;
}
这产生了预期的结果
5 4 3 2 1
它奏效了！现在，让我们更详细地探讨一下。
这是我们的IntArray构造函数，它接受一个`std::initializer_list<int>`。
IntArray(std::initializer_list<int> list) // allow IntArray to be initialized via list initialization
		: IntArray(static_cast<int>(list.size())) // use delegating constructor to set up initial array
	{
		// Now initialize our array from the list
		std::copy(list.begin(), list.end(), m_data);
	}
第1行：如上所述，我们必须使用尖括号来表示列表中期望的元素类型。在这种情况下，因为这是一个IntArray，我们期望列表填充int。注意我们没有通过const引用传递列表。与std::string_view类似，std::initializer_list非常轻量级，复制通常比间接访问更划算。
第2行：我们通过委托构造函数（以减少冗余代码）将IntArray的内存分配委托给另一个构造函数。这个另一个构造函数需要知道数组的长度，所以我们传入list.size()，其中包含列表中的元素数量。注意list.size()返回一个size_t（无符号类型），所以这里我们需要将其强制转换为有符号int。
构造函数的主体用于将元素从列表复制到我们的IntArray类中。最简单的方法是使用`std::copy()`，它位于`<algorithm>`头文件中。
访问std::initializer_list的元素
在某些情况下，您可能希望在将元素复制到内部数组之前访问std::initializer_list的每个元素（例如，进行合理性检查或以某种方式修改这些值）。
由于某些无法解释的原因，std::initializer_list不通过下标（operator[]）提供对列表元素的访问。这一遗漏已多次向标准委员会提出，但从未得到解决。
然而，有许多简单的变通方法
您可以使用基于范围的for循环来迭代列表的元素。
另一种方法是使用`begin()`成员函数来获取`std::initializer_list`的迭代器。因为这个迭代器是一个随机访问迭代器，所以迭代器可以被索引。
IntArray(std::initializer_list<int> list) // allow IntArray to be initialized via list initialization
		: IntArray(static_cast<int>(list.size())) // use delegating constructor to set up initial array
	{
		// Now initialize our array from the list
		for (std::size_t count{}; count < list.size(); ++count)
		{
			m_data[count] = list.begin()[count];
		}
	}
列表初始化优先于非列表构造函数
非空初始化列表总是优先选择匹配的initializer_list构造函数，而不是其他可能匹配的构造函数。考虑
IntArray a1(5);   // uses IntArray(int), allocates an array of size 5
IntArray a2{ 5 }; // uses IntArray<std::initializer_list<int>, allocates array of size 1
`a1`的情况使用直接初始化（不考虑列表构造函数），所以这个定义将调用`IntArray(int)`，分配一个大小为5的数组。
`a2`的情况使用列表初始化（它倾向于列表构造函数）。`IntArray(int)`和`IntArray(std::initializer_list<int>)`在这里都可能是匹配的，但由于列表构造函数受到青睐，将调用`IntArray(std::initializer_list<int>)`，分配一个大小为1的数组（该元素的值为5）。
这就是为什么我们上面的委托构造函数在委托时使用直接初始化
IntArray(std::initializer_list<int> list)
		: IntArray(static_cast<int>(list.size())) // uses direct init
这确保了我们委托给`IntArray(int)`版本。如果我们改用列表初始化进行委托，构造函数将尝试委托给自身，这将导致编译错误。
std::vector和其他容器类也会发生同样的情况，它们既有列表构造函数，也有带有类似参数类型的构造函数
std::vector<int> array(5); // Calls std::vector::vector(std::vector::size_type), 5 value-initialized elements: 0 0 0 0 0
std::vector<int> array{ 5 }; // Calls std::vector::vector(std::initializer_list<int>), 1 element: 5
关键见解
列表初始化优先于匹配的非列表构造函数。
最佳实践
当初始化一个具有列表构造函数的容器时
当打算调用列表构造函数时（例如，因为您的初始化器是元素值），请使用大括号初始化。
当打算调用非列表构造函数时（例如，因为您的初始化器不是元素值），请使用直接初始化。
向现有类添加列表构造函数是危险的
由于列表初始化倾向于列表构造函数，因此向以前没有列表构造函数的现有类添加列表构造函数可能会导致现有程序静默地改变行为。
考虑以下程序
#include <initializer_list> // for std::initializer_list
#include <iostream>

class Foo
{
public:
	Foo(int, int)
	{
		std::cout << "Foo(int, int)" << '\n';
	}
};

int main()
{
	Foo f1{ 1, 2 }; // calls Foo(int, int)

	return 0;
}
这会打印
Foo(int, int)
现在，让我们为这个类添加一个列表构造函数
#include <initializer_list> // for std::initializer_list
#include <iostream>

class Foo
{
public:
	Foo(int, int)
	{
		std::cout << "Foo(int, int)" << '\n';
	}

	// We've added a list constructor
	Foo(std::initializer_list<int>)
	{
		std::cout << "Foo(std::initializer_list<int>)" << '\n';
	}

};

int main()
{
	// note that the following statement has not changed
	Foo f1{ 1, 2 }; // now calls Foo(std::initializer_list<int>)

	return 0;
}
虽然我们没有对程序做任何其他更改，但此程序现在打印
Foo(std::initializer_list<int>)
警告
向没有列表构造函数的现有类添加列表构造函数可能会破坏现有程序。
使用std::initializer_list进行类赋值
您还可以通过重载赋值运算符以接受`std::initializer_list`参数来使用`std::initializer_list`为类赋值新值。这与上述情况类似。我们将在下面的测验解决方案中展示一个如何实现此功能的示例。
请注意，如果您实现了一个接受`std::initializer_list`的构造函数，您应该确保至少执行以下操作之一：
提供一个重载的列表赋值运算符
提供一个适当的深拷贝赋值运算符
删除复制赋值运算符
原因如下：考虑以下类（没有任何这些东西），以及一个列表赋值语句
#include <algorithm> // for std::copy()
#include <cassert>   // for assert()
#include <initializer_list> // for std::initializer_list
#include <iostream>

class IntArray
{
private:
	int m_length{};
	int* m_data{};

public:
	IntArray() = default;

	IntArray(int length)
		: m_length{ length }
		, m_data{ new int[static_cast<std::size_t>(length)] {} }
	{

	}

	IntArray(std::initializer_list<int> list) // allow IntArray to be initialized via list initialization
		: IntArray(static_cast<int>(list.size())) // use delegating constructor to set up initial array
	{
		// Now initialize our array from the list
		std::copy(list.begin(), list.end(), m_data);
	}

	~IntArray()
	{
		delete[] m_data;
	}

//	IntArray(const IntArray&) = delete; // to avoid shallow copies
//	IntArray& operator=(const IntArray& list) = delete; // to avoid shallow copies

	int& operator[](int index)
	{
		assert(index >= 0 && index < m_length);
		return m_data[index];
	}

	int getLength() const { return m_length; }
};

int main()
{
	IntArray array{};
	array = { 1, 3, 5, 7, 9, 11 }; // Here's our list assignment statement

	for (int count{ 0 }; count < array.getLength(); ++count)
		std::cout << array[count] << ' '; // undefined behavior

	return 0;
}
首先，编译器会注意到不存在接受std::initializer_list的赋值函数。接下来，它会寻找其他可以使用的赋值函数，并发现隐式提供的复制赋值运算符。然而，只有当它能将初始化列表转换为IntArray时，此函数才能使用。因为{ 1, 3, 5, 7, 9, 11 }是std::initializer_list，编译器会使用列表构造函数将初始化列表转换为一个临时IntArray。然后它会调用隐式赋值运算符，这将把临时IntArray浅拷贝到我们的数组对象中。
此时，临时IntArray的m_data和array->m_data都指向同一地址（由于浅拷贝）。您已经可以看到这将导致什么问题了。
在赋值语句结束时，临时IntArray被销毁。这会调用析构函数，该函数会删除临时IntArray的m_data。这使得array->m_data成为一个悬空指针。当您尝试出于任何目的使用array->m_data时（包括当array超出范围且析构函数去删除m_data时），您将得到未定义行为。
最佳实践
如果您提供了列表构造，那么最好也提供列表赋值。
总结
实现一个接受`std::initializer_list`参数的构造函数允许我们对自定义类使用列表初始化。我们还可以使用`std::initializer_list`来实现其他需要使用初始化列表的函数，例如赋值运算符。
小测验时间
问题 #1
使用上面的IntArray类，实现一个重载的赋值运算符，它接受一个初始化列表。
以下代码应运行
int main()
{
	IntArray array { 5, 4, 3, 2, 1 }; // initializer list
	for (int count{ 0 }; count < array.getLength(); ++count)
		std::cout << array[count] << ' ';

	std::cout << '\n';

	array = { 1, 3, 5, 7, 9, 11 };

	for (int count{ 0 }; count < array.getLength(); ++count)
		std::cout << array[count] << ' ';

	std::cout << '\n';

	return 0;
}
这应该打印
5 4 3 2 1 
1 3 5 7 9 11
显示答案
#include <algorithm> // for std::copy()
#include <cassert>   // for assert()
#include <initializer_list> // for std::initializer_list
#include <iostream>

class IntArray
{
private:
	int m_length {};
	int* m_data {};

public:
	IntArray() = default;

	IntArray(int length)
		: m_length{ length }
		, m_data{ new int[static_cast<std::size_t>(length)] {} }
	{

	}

	IntArray(std::initializer_list<int> list) : // allow IntArray to be initialized via list initialization
		IntArray(static_cast<int>(list.size())) // use delegating constructor to set up initial array
	{
		// Now initialize our array from the list
		std::copy(list.begin(), list.end(), m_data);
	}

	~IntArray()
	{
		delete[] m_data;
		// we don't need to set m_data to null or m_length to 0 here, since the object will be destroyed immediately after this function anyway
	}

	IntArray(const IntArray&) = delete; // to avoid shallow copies
	IntArray& operator=(const IntArray& list) = delete; // to avoid shallow copies

	IntArray& operator=(std::initializer_list<int> list)
	{
		// If the new list is a different size, reallocate it
		int length { static_cast<int>(list.size()) };
		if (length != m_length)
		{
			delete[] m_data;
			m_length = length;
			m_data = new int[list.size()]{};
		}

		// Now initialize our array from the list
		std::copy(list.begin(), list.end(), m_data);

		return *this;
	}

	int& operator[](int index)
	{
		assert(index >= 0 && index < m_length);
		return m_data[index];
	}

	int getLength() const { return m_length; }
};

int main()
{
	IntArray array { 5, 4, 3, 2, 1 }; // initializer list
	for (int count{ 0 }; count < array.getLength(); ++count)
		std::cout << array[count] << ' ';

	std::cout << '\n';

	array = { 1, 3, 5, 7, 9, 11 };

	for (int count{ 0 }; count < array.getLength(); ++count)
		std::cout << array[count] << ' ';

	std::cout << '\n';

	return 0;
}
下一课
23.x
第23章 总结与测验
返回目录
上一课
23.6
容器类