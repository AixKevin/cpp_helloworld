# 22.5 — std::unique_ptr

22.5 — std::unique_ptr
Alex
2017年3月15日，太平洋时间上午8:32
2024年8月20日
在本章开头，我们讨论了在某些情况下，指针的使用如何导致bug和内存泄漏。例如，当函数提前返回或抛出异常时，如果指针没有正确删除，就会发生这种情况。
#include <iostream>
 
void someFunction()
{
    auto* ptr{ new Resource() };
 
    int x{};
    std::cout << "Enter an integer: ";
    std::cin >> x;
 
    if (x == 0)
        throw 0; // the function returns early, and ptr won’t be deleted!
 
    // do stuff with ptr here
 
    delete ptr;
}
现在我们已经了解了移动语义的基础知识，我们可以回到智能指针类的话题。尽管智能指针可以提供其他功能，但智能指针的定义特征是它管理由智能指针用户提供的动态分配资源，并确保动态分配的对象在适当的时间（通常是智能指针超出范围时）被正确清理。
因此，智能指针本身不应动态分配（否则，智能指针可能无法正确释放，这意味着它拥有的对象也不会被释放，从而导致内存泄漏）。通过始终在栈上分配智能指针（作为局部变量或类的组合成员），我们可以保证当智能指针所在的函数或对象结束时，智能指针将正确超出范围，从而确保智能指针拥有的对象被正确释放。
C++11标准库提供了4个智能指针类：std::auto_ptr (在C++17中移除)、std::unique_ptr、std::shared_ptr和std::weak_ptr。std::unique_ptr是目前使用最广泛的智能指针类，所以我们将首先介绍它。在接下来的课程中，我们将介绍std::shared_ptr和std::weak_ptr。
std::unique_ptr
std::unique_ptr是C++11中std::auto_ptr的替代品。它应该用于管理任何不由多个对象共享的动态分配对象。也就是说，std::unique_ptr应该完全拥有它管理的对象，而不与其他类共享所有权。std::unique_ptr在
头文件中。
让我们看一个简单的智能指针示例
#include <iostream>
#include <memory> // for std::unique_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	// allocate a Resource object and have it owned by std::unique_ptr
	std::unique_ptr<Resource> res{ new Resource() };

	return 0;
} // res goes out of scope here, and the allocated Resource is destroyed
因为std::unique_ptr在这里是在栈上分配的，所以它最终一定会超出范围，当它超出范围时，它将删除它所管理的Resource。
与std::auto_ptr不同，std::unique_ptr正确实现了移动语义。
#include <iostream>
#include <memory> // for std::unique_ptr
#include <utility> // for std::move

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	std::unique_ptr<Resource> res1{ new Resource{} }; // Resource created here
	std::unique_ptr<Resource> res2{}; // Start as nullptr

	std::cout << "res1 is " << (res1 ? "not null\n" : "null\n");
	std::cout << "res2 is " << (res2 ? "not null\n" : "null\n");

	// res2 = res1; // Won't compile: copy assignment is disabled
	res2 = std::move(res1); // res2 assumes ownership, res1 is set to null

	std::cout << "Ownership transferred\n";

	std::cout << "res1 is " << (res1 ? "not null\n" : "null\n");
	std::cout << "res2 is " << (res2 ? "not null\n" : "null\n");

	return 0;
} // Resource destroyed here when res2 goes out of scope
这会打印
Resource acquired
res1 is not null
res2 is null
Ownership transferred
res1 is null
res2 is not null
Resource destroyed
由于std::unique_ptr在设计时考虑了移动语义，因此禁用了复制初始化和复制赋值。如果您想转移std::unique_ptr管理的内容，则必须使用移动语义。在上面的程序中，我们通过std::move实现这一点（它将res1转换为右值，从而触发移动赋值而不是复制赋值）。
访问管理对象
std::unique_ptr重载了operator*和operator->，可用于返回正在管理的资源。operator*返回对管理资源的引用，operator->返回指针。
请记住，std::unique_ptr可能并不总是管理一个对象——要么因为它被创建为空（使用默认构造函数或传入nullptr作为参数），要么因为它正在管理的资源被移动到另一个std::unique_ptr。因此，在使用这些运算符之前，我们应该检查std::unique_ptr是否确实有资源。幸运的是，这很容易：std::unique_ptr可以隐式转换为bool，如果std::unique_ptr正在管理资源，则返回true。
这是一个例子
#include <iostream>
#include <memory> // for std::unique_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

std::ostream& operator<<(std::ostream& out, const Resource&)
{
	out << "I am a resource";
	return out;
}

int main()
{
	std::unique_ptr<Resource> res{ new Resource{} };

	if (res) // use implicit cast to bool to ensure res contains a Resource
		std::cout << *res << '\n'; // print the Resource that res is owning

	return 0;
}
这会打印
Resource acquired
I am a resource
Resource destroyed
在上面的程序中，我们使用重载的operator*来获取std::unique_ptr res拥有的Resource对象，然后将其发送到std::cout进行打印。
std::unique_ptr和数组
与std::auto_ptr不同，std::unique_ptr足够智能，知道是使用标量删除还是数组删除，因此std::unique_ptr可以与标量对象和数组一起使用。
然而，std::array或std::vector（或std::string）几乎总是比使用std::unique_ptr与固定大小数组、动态数组或C风格字符串更好的选择。
最佳实践
优先使用std::array、std::vector或std::string，而不是管理固定大小数组、动态数组或C风格字符串的智能指针。
std::make_unique
C++14附带一个名为std::make_unique()的附加函数。此模板函数构造模板类型的对象，并使用传递给函数的参数对其进行初始化。
#include <memory> // for std::unique_ptr and std::make_unique
#include <iostream>

class Fraction
{
private:
	int m_numerator{ 0 };
	int m_denominator{ 1 };

public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
	}

	friend std::ostream& operator<<(std::ostream& out, const Fraction &f1)
	{
		out << f1.m_numerator << '/' << f1.m_denominator;
		return out;
	}
};


int main()
{
	// Create a single dynamically allocated Fraction with numerator 3 and denominator 5
	// We can also use automatic type deduction to good effect here
	auto f1{ std::make_unique<Fraction>(3, 5) };
	std::cout << *f1 << '\n';

	// Create a dynamically allocated array of Fractions of length 4
	auto f2{ std::make_unique<Fraction[]>(4) };
	std::cout << f2[0] << '\n';

	return 0;
}
上面的代码打印
3/5
0/1
std::make_unique()的使用是可选的，但建议您自己创建std::unique_ptr。这是因为使用std::make_unique的代码更简单，并且它需要的输入更少（与自动类型推导一起使用时）。此外，在C++14中，它解决了C++未指定函数参数评估顺序可能导致的异常安全问题。
最佳实践
使用std::make_unique()而不是自己创建std::unique_ptr并使用new。
异常安全问题更详细的说明
对于那些想知道上面提到的“异常安全问题”是什么的人，这里是对该问题的描述。
考虑一个这样的表达式
some_function(std::unique_ptr<T>(new T), function_that_can_throw_exception());
编译器在处理此调用时具有很大的灵活性。它可以创建一个新的T，然后调用function_that_can_throw_exception()，然后创建管理动态分配的T的std::unique_ptr。如果function_that_can_throw_exception()抛出异常，那么已分配的T将不会被释放，因为用于释放的智能指针尚未创建。这会导致T泄漏。
std::make_unique()没有这个问题，因为对象T的创建和std::unique_ptr的创建发生在std::make_unique()函数内部，执行顺序没有歧义。
这个问题在C++17中得到了解决，因为函数参数的评估不再可以交错。
从函数返回std::unique_ptr
std::unique_ptr可以安全地按值从函数返回
#include <memory> // for std::unique_ptr

std::unique_ptr<Resource> createResource()
{
     return std::make_unique<Resource>();
}

int main()
{
    auto ptr{ createResource() };

    // do whatever

    return 0;
}
在上面的代码中，createResource()按值返回一个std::unique_ptr。如果此值未赋值给任何内容，则临时返回值将超出作用域，Resource将被清理。如果它被赋值（如main()中所示），在C++14或更早的版本中，将采用移动语义将Resource从返回值转移到赋值的对象（在上面的示例中为ptr），而在C++17或更新的版本中，返回值将被省略。这使得通过std::unique_ptr返回资源比返回原始指针安全得多！
通常，您不应按指针（从不）或引用（除非您有特定的充分理由）返回std::unique_ptr。
将std::unique_ptr传递给函数
如果您希望函数获得指针内容的拥有权，请按值传递std::unique_ptr。请注意，由于已禁用复制语义，您需要使用std::move才能实际传递变量。
#include <iostream>
#include <memory> // for std::unique_ptr
#include <utility> // for std::move

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

std::ostream& operator<<(std::ostream& out, const Resource&)
{
	out << "I am a resource";
	return out;
}

// This function takes ownership of the Resource, which isn't what we want
void takeOwnership(std::unique_ptr<Resource> res)
{
     if (res)
          std::cout << *res << '\n';
} // the Resource is destroyed here

int main()
{
    auto ptr{ std::make_unique<Resource>() };

//    takeOwnership(ptr); // This doesn't work, need to use move semantics
    takeOwnership(std::move(ptr)); // ok: use move semantics

    std::cout << "Ending program\n";

    return 0;
}
上面的程序打印
Resource acquired
I am a resource
Resource destroyed
Ending program
请注意，在这种情况下，Resource的所有权已转移到takeOwnership()，因此Resource在takeOwnership()结束时而不是main()结束时被销毁。
然而，大多数时候，您不会希望函数拥有资源的拥有权。
尽管您可以按const引用传递std::unique_ptr（这将允许函数使用对象而不承担所有权），但最好只传递资源本身（按指针或引用，取决于null是否是有效参数）。这允许函数对调用方如何管理其资源保持不可知。
要从std::unique_ptr获取原始指针，可以使用get()成员函数
#include <memory> // for std::unique_ptr
#include <iostream>

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

std::ostream& operator<<(std::ostream& out, const Resource&)
{
	out << "I am a resource";
	return out;
}

// The function only uses the resource, so we'll accept a pointer to the resource, not a reference to the whole std::unique_ptr<Resource>
void useResource(const Resource* res)
{
	if (res)
		std::cout << *res << '\n';
	else
		std::cout << "No resource\n";
}

int main()
{
	auto ptr{ std::make_unique<Resource>() };

	useResource(ptr.get()); // note: get() used here to get a pointer to the Resource

	std::cout << "Ending program\n";

	return 0;
} // The Resource is destroyed here
上面的程序打印
Resource acquired
I am a resource
Ending program
Resource destroyed
std::unique_ptr和类
当然，您可以将std::unique_ptr用作类的组合成员。这样，您就不必担心确保类的析构函数删除动态内存，因为std::unique_ptr将在类对象被销毁时自动销毁。
但是，如果类对象没有正确销毁（例如，它是动态分配的并且没有正确释放），那么std::unique_ptr成员也不会被销毁，并且由std::unique_ptr管理的对象也不会被释放。
误用std::unique_ptr
有两种容易误用std::unique_ptr的方法，这两种方法都容易避免。首先，不要让多个对象管理同一个资源。例如
Resource* res{ new Resource() };
std::unique_ptr<Resource> res1{ res };
std::unique_ptr<Resource> res2{ res };
虽然这在语法上是合法的，但最终的结果是res1和res2都会尝试删除Resource，这将导致未定义行为。
其次，不要手动删除std::unique_ptr下面的资源。
Resource* res{ new Resource() };
std::unique_ptr<Resource> res1{ res };
delete res;
如果你这样做，std::unique_ptr将尝试删除一个已经删除的资源，再次导致未定义行为。
请注意，std::make_unique()可以防止上述两种情况的意外发生。
小测验时间
问题 #1
将以下程序从使用普通指针转换为在适当情况下使用std::unique_ptr
#include <iostream>

class Fraction
{
private:
	int m_numerator{ 0 };
	int m_denominator{ 1 };

public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
	}

	friend std::ostream& operator<<(std::ostream& out, const Fraction &f1)
	{
		out << f1.m_numerator << '/' << f1.m_denominator;
		return out;
	}
};

void printFraction(const Fraction* ptr)
{
	if (ptr)
		std::cout << *ptr << '\n';
	else
		std::cout << "No fraction\n";
}

int main()
{
	auto* ptr{ new Fraction{ 3, 5 } };

	printFraction(ptr);

	delete ptr;

	return 0;
}
显示答案
#include <memory> // for std::unique_ptr
#include <iostream>

class Fraction
{
private:
	int m_numerator{ 0 };
	int m_denominator{ 1 };

public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
	}

	friend std::ostream& operator<<(std::ostream& out, const Fraction &f1)
	{
		out << f1.m_numerator << '/' << f1.m_denominator;
		return out;
	}
};

// This function uses a Fraction object, so we just pass the Fraction itself
// That way we don't have to worry about what kind of smart pointer (if any) the caller may be using
void printFraction(const Fraction* ptr)
{
	if (ptr)
		std::cout << *ptr << '\n';
	else
		std::cout << "No fraction\n";
}

int main()
{
	auto ptr{ std::make_unique<Fraction>(3, 5) };

	printFraction(ptr.get());

	return 0;
}
下一课
22.6
std::shared_ptr
返回目录
上一课
22.4
std::move