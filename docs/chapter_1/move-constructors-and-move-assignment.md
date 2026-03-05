# 22.3 — 移动构造函数和移动赋值

22.3 — 移动构造函数和移动赋值
Alex
2017 年 2 月 26 日，太平洋标准时间下午 12:43
2025 年 2 月 18 日
在课程
22.1 — 智能指针和移动语义简介
中，我们研究了 std::auto_ptr，讨论了对移动语义的渴望，并研究了当为复制语义（复制构造函数和复制赋值运算符）设计的函数被重新定义以实现移动语义时出现的一些缺点。
在本课程中，我们将深入研究 C++11 如何通过移动构造函数和移动赋值解决这些问题。
回顾复制构造函数和复制赋值
首先，让我们花点时间回顾一下复制语义。
复制构造函数用于通过复制相同类的对象来初始化类。复制赋值用于将一个类对象复制到另一个现有类对象。默认情况下，如果未显式提供复制构造函数和复制赋值运算符，C++ 将提供它们。这些编译器提供的函数执行浅复制，这可能会导致分配动态内存的类出现问题。因此，处理动态内存的类应重写这些函数以执行深复制。
回到本章第一课中的 Auto_ptr 智能指针类示例，让我们看一个实现深复制的复制构造函数和复制赋值运算符的版本，以及一个演示它们的示例程序。
#include <iostream>

template<typename T>
class Auto_ptr3
{
	T* m_ptr {};
public:
	Auto_ptr3(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr3()
	{
		delete m_ptr;
	}

	// Copy constructor
	// Do deep copy of a.m_ptr to m_ptr
	Auto_ptr3(const Auto_ptr3& a)
	{
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}

	// Copy assignment
	// Do deep copy of a.m_ptr to m_ptr
	Auto_ptr3& operator=(const Auto_ptr3& a)
	{
		// Self-assignment detection
		if (&a == this)
			return *this;

		// Release any resource we're holding
		delete m_ptr;

		// Copy the resource
		m_ptr = new T;
		*m_ptr = *a.m_ptr;

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr3<Resource> generateResource()
{
	Auto_ptr3<Resource> res{new Resource};
	return res; // this return value will invoke the copy constructor
}

int main()
{
	Auto_ptr3<Resource> mainres;
	mainres = generateResource(); // this assignment will invoke the copy assignment

	return 0;
}
在这个程序中，我们使用一个名为 generateResource() 的函数来创建一个智能指针封装的资源，然后将其传回 main() 函数。然后 main() 函数将其赋值给一个现有的 Auto_ptr3 对象。
当此程序运行时，它会打印：
Resource acquired
Resource acquired
Resource destroyed
Resource acquired
Resource destroyed
Resource destroyed
（注意：如果您的编译器省略了 generateResource() 函数的返回值，您可能只会得到 4 个输出）
对于这样一个简单的程序来说，发生了大量的资源创建和销毁！这里发生了什么？
让我们仔细看看。此程序中有 6 个关键步骤（每个打印消息对应一个）
在 generateResource() 内部，局部变量 res 被创建并用动态分配的 Resource 初始化，这导致了第一个“Resource acquired”。
Res 以值返回到 main()。我们在这里按值返回，因为 res 是一个局部变量——它不能通过地址或引用返回，因为当 generateResource() 结束时 res 将被销毁。因此，res 被复制构造到一个临时对象中。由于我们的复制构造函数执行深复制，这里会分配一个新的 Resource，这导致了第二个“Resource acquired”。
Res 超出作用域，销毁了最初创建的 Resource，这导致了第一个“Resource destroyed”。
临时对象通过复制赋值赋值给 mainres。由于我们的复制赋值也执行深复制，因此会分配一个新的 Resource，从而导致另一个“Resource acquired”。
赋值表达式结束，临时对象超出表达式作用域并被销毁，导致“Resource destroyed”。
在 main() 结束时，mainres 超出作用域，并显示我们最终的“Resource destroyed”。
所以，简而言之，由于我们调用复制构造函数一次将 res 复制构造到临时对象，并调用复制赋值一次将临时对象复制到 mainres，我们最终总共分配和销毁了 3 个独立对象。
效率低下，但至少它不会崩溃！
然而，使用移动语义，我们可以做得更好。
移动构造函数和移动赋值
C++11 定义了两个新的函数来支持移动语义：一个移动构造函数和一个移动赋值运算符。复制构造函数和复制赋值的目标是将一个对象复制到另一个对象，而移动构造函数和移动赋值的目标是将资源的所有权从一个对象移动到另一个对象（这通常比复制便宜得多）。
定义移动构造函数和移动赋值的工作方式类似于它们的复制对应项。然而，这些函数的复制版本采用 const 左值引用参数（它可以绑定到几乎任何东西），而这些函数的移动版本使用非 const 右值引用参数（它只绑定到右值）。
这里是与上面相同的 Auto_ptr3 类，增加了移动构造函数和移动赋值运算符。我们保留了执行深复制的复制构造函数和复制赋值运算符，以便进行比较。
#include <iostream>

template<typename T>
class Auto_ptr4
{
	T* m_ptr {};
public:
	Auto_ptr4(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr4()
	{
		delete m_ptr;
	}

	// Copy constructor
	// Do deep copy of a.m_ptr to m_ptr
	Auto_ptr4(const Auto_ptr4& a)
	{
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}

	// Move constructor
	// Transfer ownership of a.m_ptr to m_ptr
	Auto_ptr4(Auto_ptr4&& a) noexcept
		: m_ptr { a.m_ptr }
	{
		a.m_ptr = nullptr; // we'll talk more about this line below
	}

	// Copy assignment
	// Do deep copy of a.m_ptr to m_ptr
	Auto_ptr4& operator=(const Auto_ptr4& a)
	{
		// Self-assignment detection
		if (&a == this)
			return *this;

		// Release any resource we're holding
		delete m_ptr;

		// Copy the resource
		m_ptr = new T;
		*m_ptr = *a.m_ptr;

		return *this;
	}

	// Move assignment
	// Transfer ownership of a.m_ptr to m_ptr
	Auto_ptr4& operator=(Auto_ptr4&& a) noexcept
	{
		// Self-assignment detection
		if (&a == this)
			return *this;

		// Release any resource we're holding
		delete m_ptr;

		// Transfer ownership of a.m_ptr to m_ptr
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr; // we'll talk more about this line below

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr4<Resource> generateResource()
{
	Auto_ptr4<Resource> res{new Resource};
	return res; // this return value will invoke the move constructor
}

int main()
{
	Auto_ptr4<Resource> mainres;
	mainres = generateResource(); // this assignment will invoke the move assignment

	return 0;
}
移动构造函数和移动赋值运算符很简单。我们不将源对象 (
a
) 深复制到目标对象（隐式对象），而是简单地移动（窃取）源对象的资源。这涉及将源指针浅复制到隐式对象中，然后将源指针设置为 null。
运行时，此程序打印
Resource acquired
Resource destroyed
好多了！
程序的流程与之前完全相同。但是，此程序不是调用复制构造函数和复制赋值运算符，而是调用移动构造函数和移动赋值运算符。更深入地看：
在 generateResource() 内部，局部变量 res 被创建并用动态分配的 Resource 初始化，这导致了第一个“Resource acquired”。
Res 以值返回到 main()。Res 被移动构造到一个临时对象中，将存储在 res 中的动态创建对象转移到临时对象。我们将在下面讨论为什么会发生这种情况。
Res 超出作用域。因为 res 不再管理指针（它被移动到临时对象），所以这里没有发生什么有趣的事情。
临时对象被移动赋值给 mainres。这会将存储在临时对象中的动态创建对象转移到 mainres。
赋值表达式结束，临时对象超出表达式作用域并被销毁。然而，由于临时对象不再管理指针（它被移动到 mainres），这里也没有发生什么有趣的事情。
在 main() 结束时，mainres 超出作用域，并显示我们最终的“Resource destroyed”。
因此，我们不是复制 Resource 两次（一次用于复制构造函数，一次用于复制赋值），而是转移它两次。这更有效率，因为 Resource 只构造和销毁一次，而不是三次。
相关内容
移动构造函数和移动赋值应标记为
noexcept
。这会告诉编译器这些函数不会抛出异常。
我们在课程
27.9 — 异常规范和 noexcept
中介绍了
noexcept
，并在课程
27.10 — std::move_if_noexcept
中讨论了为什么移动构造函数和移动赋值被标记为
noexcept
。
何时调用移动构造函数和移动赋值？
当定义了移动构造函数和移动赋值，并且构造或赋值的参数是一个右值时，就会调用这些函数。通常，这个右值将是一个字面量或临时值。
否则使用复制构造函数和复制赋值（当参数是左值时，或者当参数是右值且未定义移动构造函数或移动赋值函数时）。
隐式移动构造函数和移动赋值运算符
如果以下所有条件都为真，编译器将创建一个隐式移动构造函数和移动赋值运算符：
没有用户声明的复制构造函数或复制赋值运算符。
没有用户声明的移动构造函数或移动赋值运算符。
没有用户声明的析构函数。
这些函数执行成员级移动，其行为如下：
如果成员具有移动构造函数或移动赋值（视情况而定），它将被调用。
否则，成员将被复制。
值得注意的是，这意味着指针将被复制，而不是移动！
警告
隐式移动构造函数和移动赋值将复制指针，而不是移动它们。如果您想移动指针成员，您需要自己定义移动构造函数和移动赋值。
移动语义背后的关键见解
现在您已经掌握了足够的上下文来理解移动语义背后的关键见解。
如果我们构造一个对象或执行赋值，其中参数是左值，我们唯一能合理做的事情就是复制左值。我们不能假设修改左值是安全的，因为它可能稍后在程序中再次使用。如果我们有一个表达式“a = b”（其中 b 是左值），我们不会合理地期望 b 以任何方式改变。
然而，如果我们构造一个对象或执行赋值，其中参数是一个右值，那么我们知道该右值只是一种临时对象。我们不必复制它（这可能很昂贵），而是可以简单地将其资源（这很便宜）转移到我们正在构造或赋值的对象。这样做是安全的，因为临时对象无论如何都将在表达式结束时销毁，所以我们知道它永远不会再被使用！
C++11 通过右值引用，使我们能够提供不同的行为，当参数是右值与左值时，从而使我们能够对对象应该如何行为做出更智能、更有效的决策。
关键见解
移动语义是一个优化机会。
移动函数应始终使两个对象都处于有效状态。
在上面的示例中，移动构造函数和移动赋值函数都将 a.m_ptr 设置为 nullptr。这可能看起来是多余的——毕竟，如果
a
是一个临时右值，为什么还要费心做“清理”呢，因为参数
a
无论如何都会被销毁？
答案很简单：当
a
超出作用域时，将调用
a
的析构函数，并且
a.m_ptr
将被删除。如果此时
a.m_ptr
仍然指向与
m_ptr
相同的对象，那么
m_ptr
将成为一个悬空指针。当包含
m_ptr
的对象最终被使用（或销毁）时，我们将得到未定义行为。
在实现移动语义时，重要的是要确保被移动的对象处于有效状态，以便它能够正确销毁（而不会产生未定义行为）。
按值返回的自动左值可以移动而不是复制
在上面 Auto_ptr4 示例的 generateResource() 函数中，当变量 res 按值返回时，它被移动而不是复制，即使 res 是一个左值。C++ 规范有一个特殊规则，即从函数按值返回的自动对象即使是左值也可以移动。这是有道理的，因为 res 无论如何都会在函数结束时销毁！我们不如窃取它的资源，而不是进行昂贵且不必要的复制。
虽然编译器可以移动左值返回值，但在某些情况下，它可以通过完全省略复制来做得更好（这完全避免了复制或移动的需要）。在这种情况下，复制构造函数和移动构造函数都不会被调用。
禁用复制
在上面的 Auto_ptr4 类中，我们保留了复制构造函数和赋值运算符以进行比较。但在支持移动的类中，有时需要删除复制构造函数和复制赋值函数以确保不进行复制。在我们的 Auto_ptr 类中，我们不希望复制我们的模板对象 T——既因为昂贵，也因为 T 类可能甚至不支持复制！
这是一个支持移动语义但不支持复制语义的 Auto_ptr 版本：
#include <iostream>

template<typename T>
class Auto_ptr5
{
	T* m_ptr {};
public:
	Auto_ptr5(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr5()
	{
		delete m_ptr;
	}

	// Copy constructor -- no copying allowed!
	Auto_ptr5(const Auto_ptr5& a) = delete;

	// Move constructor
	// Transfer ownership of a.m_ptr to m_ptr
	Auto_ptr5(Auto_ptr5&& a) noexcept
		: m_ptr { a.m_ptr }
	{
		a.m_ptr = nullptr;
	}

	// Copy assignment -- no copying allowed!
	Auto_ptr5& operator=(const Auto_ptr5& a) = delete;

	// Move assignment
	// Transfer ownership of a.m_ptr to m_ptr
	Auto_ptr5& operator=(Auto_ptr5&& a) noexcept
	{
		// Self-assignment detection
		if (&a == this)
			return *this;

		// Release any resource we're holding
		delete m_ptr;

		// Transfer ownership of a.m_ptr to m_ptr
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr;

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};
如果您尝试按值将 Auto_ptr5 左值传递给函数，编译器将抱怨初始化函数参数所需的复制构造函数已被删除。这是好的，因为我们无论如何都应该通过 const 左值引用传递 Auto_ptr5！
Auto_ptr5 (最终) 是一个好的智能指针类。事实上，标准库中包含一个与此非常相似的类（您应该改用它），名为 std::unique_ptr。我们将在本章后面详细讨论 std::unique_ptr。
另一个例子
让我们看看另一个使用动态内存的类：一个简单的动态模板数组。这个类包含一个深层复制构造函数和复制赋值运算符。
#include <cstddef> // for std::size_t

template <typename T>
class DynamicArray
{
private:
	T* m_array {};
	int m_length {};

	void alloc(int length)
	{
		m_array = new T[static_cast<std::size_t>(length)];
        	m_length = length;
	}
public:
	DynamicArray(int length)
	{
		alloc(length);
	}

	~DynamicArray()
	{
		delete[] m_array;
	}

	// Copy constructor
	DynamicArray(const DynamicArray &arr)
	{
		alloc(arr.m_length);
		std::copy_n(arr.m_array, m_length, m_array); // copy m_length elements from arr to m_array
	}

	// Copy assignment
	DynamicArray& operator=(const DynamicArray &arr)
	{
		if (&arr == this)
			return *this;

		delete[] m_array;

		alloc(arr.m_length);

		std::copy_n(arr.m_array, m_length, m_array); // copy m_length elements from arr to m_array

		return *this;
	}

	int getLength() const { return m_length; }
	T& operator[](int index) { return m_array[index]; }
	const T& operator[](int index) const { return m_array[index]; }
};
现在让我们在程序中使用这个类。为了向您展示当我们在堆上分配一百万个整数时这个类的性能，我们将利用我们在课程
18.4 — 计时您的代码
中开发的 Timer 类。我们将使用 Timer 类来计时我们的代码运行速度，并向您展示复制和移动之间的性能差异。
#include <algorithm> // for std::copy_n
#include <chrono> // for std::chrono functions
#include <iostream>

// Uses the above DynamicArray class

class Timer
{
private:
	// Type aliases to make accessing nested type easier
	using Clock = std::chrono::high_resolution_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;
	
	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}
	
	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};

// Return a copy of arr with all of the values doubled
DynamicArray<int> cloneArrayAndDouble(const DynamicArray<int> &arr)
{
	DynamicArray<int> dbl(arr.getLength());
	for (int i = 0; i < arr.getLength(); ++i)
		dbl[i] = arr[i] * 2;

	return dbl;
}

int main()
{
	Timer t;

	DynamicArray<int> arr(1000000);

	for (int i = 0; i < arr.getLength(); i++)
		arr[i] = i;

	arr = cloneArrayAndDouble(arr);

	std::cout << t.elapsed();
}
在作者的一台机器上，在发布模式下，该程序在 0.00825559 秒内执行。
现在让我们通过用移动构造函数和移动赋值替换复制构造函数和复制赋值来更新
DynamicArray
，然后再次运行程序。
#include <cstddef> // for std::size_t

template <typename T>
class DynamicArray
{
private:
	T* m_array {};
	int m_length {};

	void alloc(int length)
	{
		m_array = new T[static_cast<std::size_t>(length)];
		m_length = length;
	}
public:
	DynamicArray(int length)
	{
		alloc(length);
	}

	~DynamicArray()
	{
		delete[] m_array;
	}

	// Copy constructor
	DynamicArray(const DynamicArray &arr) = delete;

	// Copy assignment
	DynamicArray& operator=(const DynamicArray &arr) = delete;

	// Move constructor
	DynamicArray(DynamicArray &&arr) noexcept
		:  m_array { arr.m_array }, m_length { arr.m_length }
	{
		arr.m_length = 0;
		arr.m_array = nullptr;
	}

	// Move assignment
	DynamicArray& operator=(DynamicArray &&arr) noexcept
	{
		if (&arr == this)
			return *this;

		delete[] m_array;

		m_length = arr.m_length;
		m_array = arr.m_array;
		arr.m_length = 0;
		arr.m_array = nullptr;

		return *this;
	}

	int getLength() const { return m_length; }
	T& operator[](int index) { return m_array[index]; }
	const T& operator[](int index) const { return m_array[index]; }
};

#include <iostream>
#include <chrono> // for std::chrono functions

class Timer
{
private:
	// Type aliases to make accessing nested type easier
	using Clock = std::chrono::high_resolution_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;
	
	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}
	
	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};

// Return a copy of arr with all of the values doubled
DynamicArray<int> cloneArrayAndDouble(const DynamicArray<int> &arr)
{
	DynamicArray<int> dbl(arr.getLength());
	for (int i = 0; i < arr.getLength(); ++i)
		dbl[i] = arr[i] * 2;

	return dbl;
}

int main()
{
	Timer t;

	DynamicArray<int> arr(1000000);

	for (int i = 0; i < arr.getLength(); i++)
		arr[i] = i;

	arr = cloneArrayAndDouble(arr);

	std::cout << t.elapsed();
}
在同一台机器上，此程序在 0.0056 秒内执行。
比较两个程序的运行时间，(0.00825559 - 0.0056) / 0.00825559 * 100 = 32.1% 更快！
删除移动构造函数和移动赋值
您可以使用
= delete
语法删除移动构造函数和移动赋值，就像删除复制构造函数和复制赋值一样。
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;
    Name(Name&& name) = delete;
    Name& operator=(Name&& name) = delete;

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };
    n1 = Name{ "Joe" }; // error: move assignment deleted

    std::cout << n1.get() << '\n';

    return 0;
}
如果删除复制构造函数，编译器将不会生成隐式移动构造函数（使您的对象既不可复制也不可移动）。因此，在删除复制构造函数时，明确您希望移动构造函数具有什么行为是有用的。要么明确删除它们（清楚地表明这是期望的行为），要么将它们设置为默认值（使类只能移动）。
关键见解
五法则
指出，如果定义或删除了复制构造函数、复制赋值、移动构造函数、移动赋值或析构函数，则所有这些函数都应定义或删除。
虽然如果想要一个可复制但不可移动的对象，只删除移动构造函数和移动赋值似乎是个好主意，但这会带来不幸的后果，即在强制复制省略不适用的情况下，类无法按值返回。这是因为已删除的移动构造函数仍然是一个已声明的函数，因此有资格进行重载解析。而按值返回将优先于未删除的复制构造函数选择已删除的移动构造函数。下面的程序说明了这一点：
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = default;
    Name& operator=(const Name& name) = default;

    Name(Name&& name) = delete;
    Name& operator=(Name&& name) = delete;

    const std::string& get() const { return m_name; }
};

Name getJoe()
{
    Name joe{ "Joe" };
    return joe; // error: Move constructor was deleted
}

int main()
{
    Name n{ getJoe() };

    std::cout << n.get() << '\n';

    return 0;
}
移动语义和
std::swap
的问题
高级
在课程
21.12 — 重载赋值运算符
中，我们提到了复制和交换习语。复制和交换也适用于移动语义，这意味着我们可以通过与将被销毁的对象交换资源来实现移动构造函数和移动赋值。
这有两大好处：
持久对象现在控制着之前由将要销毁的对象拥有的资源（这是我们的主要目标）。
即将销毁的对象现在控制着之前由持久对象拥有的资源。当即将销毁的对象真正销毁时，它可以对这些资源进行任何所需的清理。
当您想到交换时，首先想到的是通常是
std::swap()
。然而，使用
std::swap()
实现移动构造函数和移动赋值存在问题，因为
std::swap()
会在可移动对象上调用移动构造函数和移动赋值。这将导致无限递归问题。
您可以在以下示例中看到这种情况发生：
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {}; // std::string is move capable

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;

    Name(Name&& name) noexcept
    {
        std::cout << "Move ctor\n";

        std::swap(*this, name); // bad!
    }

    Name& operator=(Name&& name) noexcept
    {
        std::cout << "Move assign\n";

        std::swap(*this, name); // bad!

        return *this;
    }

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };   
    n1 = Name{"Joe"}; // invokes move assignment

    std::cout << n1.get() << '\n';
    
    return 0;
}
这会打印
Move assign
Move ctor
Move ctor
Move ctor
Move ctor
等等……直到栈溢出。
您可以使用自己的交换函数实现移动构造函数和移动赋值，只要您的交换成员函数不调用移动构造函数或移动赋值。以下是实现方法示例：
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;
    
    // Create our own swap friend function to swap the members of Name
    friend void swap(Name& a, Name& b) noexcept
    {
        // We avoid recursive calls by invoking std::swap on the std::string member,
        // not on Name
        std::swap(a.m_name, b.m_name);
    }

    Name(Name&& name) noexcept
    {
        std::cout << "Move ctor\n";

        swap(*this, name); // Now calling our swap, not std::swap
    }

    Name& operator=(Name&& name) noexcept
    {
        std::cout << "Move assign\n";

        swap(*this, name); // Now calling our swap, not std::swap

        return *this;
    }

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };   
    n1 = Name{"Joe"}; // invokes move assignment

    std::cout << n1.get() << '\n';

    return 0;
}
这按预期工作，并打印
Move assign
Joe
下一课
22.4
std::move
返回目录
上一课
22.2
右值引用