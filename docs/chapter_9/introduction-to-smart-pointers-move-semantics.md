# 22.1 — 智能指针和移动语义简介

22.1 — 智能指针和移动语义简介
Alex
2017 年 2 月 17 日，太平洋标准时间上午 10:10
2025 年 2 月 4 日
考虑一个函数，在该函数中我们动态分配一个值
void someFunction()
{
    Resource* ptr = new Resource(); // Resource is a struct or class

    // do stuff with ptr here

    delete ptr;
}
尽管上述代码看起来相当简单，但很容易忘记释放 ptr。即使您确实记得在函数末尾删除 ptr，如果函数提前退出，也有无数种方法可能导致 ptr 未被删除。这可能通过提前返回发生
#include <iostream>

void someFunction()
{
    Resource* ptr = new Resource();

    int x;
    std::cout << "Enter an integer: ";
    std::cin >> x;

    if (x == 0)
        return; // the function returns early, and ptr won’t be deleted!

    // do stuff with ptr here

    delete ptr;
}
或通过抛出异常
#include <iostream>

void someFunction()
{
    Resource* ptr = new Resource();

    int x;
    std::cout << "Enter an integer: ";
    std::cin >> x;

    if (x == 0)
        throw 0; // the function returns early, and ptr won’t be deleted!

    // do stuff with ptr here

    delete ptr;
}
在上述两个程序中，提前返回或抛出语句执行，导致函数终止，而变量 ptr 未被删除。因此，为变量 ptr 分配的内存现在泄漏了（每次调用此函数并提前返回时都会再次泄漏）。
本质上，这些类型的问题发生是因为指针变量没有内在的机制来自动清理。
智能指针类来拯救？
类最好的优点之一是它们包含析构函数，当类的对象超出作用域时会自动执行。因此，如果您在构造函数中分配（或获取）内存，则可以在析构函数中释放它，并保证当类对象被销毁时（无论它是否超出作用域，是否被显式删除等），内存都会被释放。这是我们之前在
19.3 -- 析构函数
课程中讨论的 RAII 编程范式核心。
那么我们能否使用类来帮助我们管理和清理指针呢？我们可以！
考虑一个类，其唯一的工作是持有并“拥有”传递给它的指针，然后在类对象超出作用域时释放该指针。只要该类的对象仅作为局部变量创建，我们就可以保证该类将正确地超出作用域（无论我们的函数何时或如何终止），并且所拥有的指针将被销毁。
这是这个想法的初稿
#include <iostream>

template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	// Pass in a pointer to "own" via the constructor
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	// The destructor will make sure it gets deallocated
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	// Overload dereference and operator-> so we can use Auto_ptr1 like m_ptr.
	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

// A sample class to prove the above works
class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Auto_ptr1<Resource> res(new Resource()); // Note the allocation of memory here

        // ... but no explicit delete needed

	// Also note that we use <Resource>, not <Resource*>
        // This is because we've defined m_ptr to have type T* (not T)

	return 0;
} // res goes out of scope here, and destroys the allocated Resource for us
这个程序打印
Resource acquired
Resource destroyed
考虑这个程序和类是如何工作的。首先，我们动态创建一个 Resource，并将其作为参数传递给我们的模板化 Auto_ptr1 类。从那时起，我们的 Auto_ptr1 变量 res 拥有该 Resource 对象（Auto_ptr1 与 m_ptr 具有组合关系）。因为 res 被声明为局部变量并具有块作用域，所以它会在块结束时超出作用域并被销毁（不用担心忘记释放它）。因为它是一个类，所以当它被销毁时，Auto_ptr1 的析构函数将被调用。该析构函数将确保它持有的 Resource 指针被删除！
只要 Auto_ptr1 定义为局部变量（具有自动持续时间，因此类名中包含“Auto”），Resource 将保证在其声明的块结束时被销毁，无论函数如何终止（即使它提前终止）。
这样的类称为智能指针。**智能指针**是一种组合类，旨在管理动态分配的内存并确保当智能指针对象超出作用域时内存被删除。（相关地，内置指针有时被称为“哑指针”，因为它们不能自动清理）。
现在让我们回到上面的 someFunction() 示例，并展示智能指针类如何解决我们的挑战
#include <iostream>

template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	// Pass in a pointer to "own" via the constructor
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	// The destructor will make sure it gets deallocated
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	// Overload dereference and operator-> so we can use Auto_ptr1 like m_ptr.
	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

// A sample class to prove the above works
class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
    void sayHi() { std::cout << "Hi!\n"; }
};

void someFunction()
{
    Auto_ptr1<Resource> ptr(new Resource()); // ptr now owns the Resource
 
    int x;
    std::cout << "Enter an integer: ";
    std::cin >> x;
 
    if (x == 0)
        return; // the function returns early
 
    // do stuff with ptr here
    ptr->sayHi();
}

int main()
{
    someFunction();

    return 0;
}
如果用户输入非零整数，则上述程序将打印
Resource acquired
Hi!
Resource destroyed
如果用户输入零，上述程序将提前终止，打印
Resource acquired
Resource destroyed
请注意，即使在用户输入零且函数提前终止的情况下，Resource 仍然正确地被释放了。
因为 `ptr` 变量是一个局部变量，所以 `ptr` 会在函数终止时被销毁（无论它如何终止）。并且因为 `Auto_ptr1` 的析构函数会清理 `Resource`，我们确信 `Resource` 会被正确清理。
一个关键缺陷
Auto_ptr1 类潜藏着一个由自动生成代码引起的关键缺陷。在继续阅读之前，看看您是否能发现它是什么。我们等等看……
（提示：考虑如果你不提供，类的哪些部分会被自动生成）
（Jeopardy 音乐）
好的，时间到了。
与其告诉您，不如我们向您展示。请看下面的程序
#include <iostream>

// Same as above
template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Auto_ptr1<Resource> res1(new Resource());
	Auto_ptr1<Resource> res2(res1); // Alternatively, don't initialize res2 and then assign res2 = res1;

	return 0;
} // res1 and res2 go out of scope here
这个程序打印
Resource acquired
Resource destroyed
Resource destroyed
您的程序很可能（但不一定）会在此时崩溃。现在看到问题了吗？因为我们没有提供拷贝构造函数或赋值运算符，C++ 为我们提供了一个。它提供的函数执行浅拷贝。因此，当我们用 res1 初始化 res2 时，两个 Auto_ptr1 变量都指向同一个 Resource。当 res2 超出作用域时，它会删除该资源，留下 res1 悬空指针。当 res1 尝试删除其（已被删除的）Resource 时，将导致未定义行为（很可能是崩溃）！
您会遇到一个类似的问题，例如以下函数
void passByValue(Auto_ptr1<Resource> res)
{
}

int main()
{
	Auto_ptr1<Resource> res1(new Resource());
	passByValue(res1);

	return 0;
}
在这个程序中，`res1` 将按值复制到参数 `res` 中，因此 `res1.m_ptr` 和 `res.m_ptr` 都将持有相同的地址。
当 `res` 在函数结束时被销毁后，`res1.m_ptr` 就变成了悬空指针。当 `res1.m_ptr` 随后被删除时，将导致未定义行为。
所以这显然不好。我们该如何解决这个问题？
好吧，我们可以做的一件事是显式定义和删除拷贝构造函数和赋值运算符，从而从一开始就阻止任何拷贝的产生。这将阻止按值传递的情况（这很好，我们可能无论如何都不应该按值传递这些）。
但那样我们如何将 Auto_ptr1 从函数返回给调用者呢？
??? generateResource()
{
     Resource* r{ new Resource() };
     return Auto_ptr1(r);
}
我们不能按引用返回 Auto_ptr1，因为局部 Auto_ptr1 会在函数结束时被销毁，调用者会留下一个悬空引用。我们可以将指针 r 作为 `Resource*` 返回，但是我们可能会忘记稍后删除 r，这与使用智能指针的初衷相悖。所以这不行。按值返回 Auto_ptr1 是唯一有意义的选择——但那样我们会遇到浅拷贝、重复指针和崩溃。
另一个选择是重载拷贝构造函数和赋值运算符以进行深拷贝。这样，我们至少可以保证避免指向同一对象的重复指针。但是拷贝可能很昂贵（并且可能不可取甚至不可能），而且我们不想为了从函数返回 Auto_ptr1 而不必要地拷贝对象。此外，赋值或初始化一个“笨”指针并不会拷贝它所指向的对象，那么我们为什么会期望智能指针表现不同呢？
我们该怎么办？
移动语义
如果我们的拷贝构造函数和赋值运算符不是拷贝指针（“拷贝语义”），而是将指针的所有权从源对象转移/移动到目标对象呢？这是移动语义的核心思想。**移动语义**意味着类将转移对象的所有权，而不是进行拷贝。
让我们更新 Auto_ptr1 类，展示如何实现这一点
#include <iostream>

template <typename T>
class Auto_ptr2
{
	T* m_ptr {};
public:
	Auto_ptr2(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	~Auto_ptr2()
	{
		delete m_ptr;
	}

	// A copy constructor that implements move semantics
	Auto_ptr2(Auto_ptr2& a) // note: not const
	{
		// We don't need to delete m_ptr here.  This constructor is only called when we're creating a new object, and m_ptr can't be set prior to this.
		m_ptr = a.m_ptr; // transfer our dumb pointer from the source to our local object
		a.m_ptr = nullptr; // make sure the source no longer owns the pointer
	}
	
	// An assignment operator that implements move semantics
	Auto_ptr2& operator=(Auto_ptr2& a) // note: not const
	{
		if (&a == this)
			return *this;

		delete m_ptr; // make sure we deallocate any pointer the destination is already holding first
		m_ptr = a.m_ptr; // then transfer our dumb pointer from the source to the local object
		a.m_ptr = nullptr; // make sure the source no longer owns the pointer
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

int main()
{
	Auto_ptr2<Resource> res1(new Resource());
	Auto_ptr2<Resource> res2; // Start as nullptr

	std::cout << "res1 is " << (res1.isNull() ? "null\n" : "not null\n");
	std::cout << "res2 is " << (res2.isNull() ? "null\n" : "not null\n");

	res2 = res1; // res2 assumes ownership, res1 is set to null

	std::cout << "Ownership transferred\n";

	std::cout << "res1 is " << (res1.isNull() ? "null\n" : "not null\n");
	std::cout << "res2 is " << (res2.isNull() ? "null\n" : "not null\n");

	return 0;
}
这个程序打印
Resource acquired
res1 is not null
res2 is null
Ownership transferred
res1 is null
res2 is not null
Resource destroyed
注意，我们重载的 operator= 将 m_ptr 的所有权从 res1 转移给了 res2！因此，我们不会得到指针的重复副本，并且所有内容都得到了整洁的清理。
提醒
删除空指针是没问题的，因为它什么也不做。
std::auto_ptr，以及为什么它是一个坏主意
现在是时候讨论 std::auto_ptr 了。std::auto_ptr 在 C++98 中引入，在 C++17 中移除，是 C++ 第一次尝试标准化智能指针。std::auto_ptr 选择像 Auto_ptr2 类那样实现移动语义。
然而，std::auto_ptr（和我们的 Auto_ptr2 类）存在许多问题，使其使用起来很危险。
首先，因为 std::auto_ptr 通过拷贝构造函数和赋值运算符实现移动语义，所以将 std::auto_ptr 按值传递给函数会导致您的资源被移动到函数参数（并在函数参数超出作用域时在函数结束时销毁）。然后当您尝试从调用者访问您的 auto_ptr 参数时（没有意识到它已被转移和删除），您突然解引用了一个空指针。崩溃！
其次，`std::auto_ptr` 总是使用非数组删除来删除其内容。这意味着 `auto_ptr` 无法正确处理动态分配的数组，因为它使用了错误的释放方式。更糟的是，它不会阻止您向它传递动态数组，然后它会错误地管理，导致内存泄漏。
最后，`auto_ptr` 与标准库中的许多其他类（包括大多数容器和算法）不兼容。这是因为这些标准库类假设当它们复制一个项时，实际上是进行了复制，而不是移动。
由于上述缺点，std::auto_ptr 在 C++11 中已被弃用，并在 C++17 中移除。
向前迈进
`std::auto_ptr` 设计的核心问题是，在 C++11 之前，C++ 语言根本没有机制来区分“拷贝语义”和“移动语义”。重写拷贝语义来实现移动语义会导致奇怪的边缘情况和意外的 bug。例如，您可以编写 `res1 = res2`，却不知道 `res2` 是否会改变！
因此，在 C++11 中，正式定义了“移动”的概念，并将“移动语义”添加到语言中，以正确区分复制和移动。既然我们已经为移动语义的有用性奠定了基础，我们将在本章的其余部分探讨移动语义的主题。我们还将使用移动语义修复我们的 Auto_ptr2 类。
在 C++11 中，`std::auto_ptr` 已被许多其他类型的“移动感知”智能指针取代：`std::unique_ptr`、`std::weak_ptr` 和 `std::shared_ptr`。我们还将探讨其中最流行的两种：`unique_ptr`（它是 `auto_ptr` 的直接替代品）和 `shared_ptr`。
下一课
22.2
右值引用
返回目录
上一课
21.y
第 21 章项目