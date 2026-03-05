# 19.3 — 析构函数

19.3 — 析构函数
Alex
2007年9月6日，太平洋夏令时上午9:14
2023年11月30日
析构函数
是另一种特殊的类成员函数，当该类的对象被销毁时执行。构造函数旨在初始化类，而析构函数旨在帮助清理。
当对象正常超出范围，或者动态分配的对象使用 delete 关键字显式删除时，类析构函数会自动调用（如果存在）以在对象从内存中删除之前进行任何必要的清理。对于简单的类（只初始化普通成员变量值的类），不需要析构函数，因为 C++ 会自动为您清理内存。
但是，如果您的类对象持有任何资源（例如动态内存，或文件或数据库句柄），或者如果您需要在对象被销毁之前进行任何类型的维护，析构函数是执行此操作的完美场所，因为它通常是对象被销毁之前发生的最后一件事。
析构函数命名
像构造函数一样，析构函数有特定的命名规则
析构函数必须与类名相同，前面加上波浪号（~）。
析构函数不能带有参数。
析构函数没有返回类型。
一个类只能有一个析构函数。
通常您不应该显式调用析构函数（因为它会在对象销毁时自动调用），因为很少有您想多次清理对象的情况。然而，析构函数可以安全地调用其他成员函数，因为对象直到析构函数执行完毕后才销毁。
析构函数示例
让我们看一个使用析构函数的简单类
#include <iostream>
#include <cassert>
#include <cstddef>

class IntArray
{
private:
	int* m_array{};
	int m_length{};

public:
	IntArray(int length) // constructor
	{
		assert(length > 0);

		m_array = new int[static_cast<std::size_t>(length)]{};
		m_length = length;
	}

	~IntArray() // destructor
	{
		// Dynamically delete the array we allocated earlier
		delete[] m_array;
	}

	void setValue(int index, int value) { m_array[index] = value; }
	int getValue(int index) { return m_array[index]; }

	int getLength() { return m_length; }
};

int main()
{
	IntArray ar ( 10 ); // allocate 10 integers
	for (int count{ 0 }; count < ar.getLength(); ++count)
		ar.setValue(count, count+1);

	std::cout << "The value of element 5 is: " << ar.getValue(5) << '\n';

	return 0;
} // ar is destroyed here, so the ~IntArray() destructor function is called here
提示
如果您编译上面的示例并收到以下错误
error: 'class IntArray' has pointer data members [-Werror=effc++]|
error:   but does not override 'IntArray(const IntArray&)' [-Werror=effc++]|
error:   or 'operator=(const IntArray&)' [-Werror=effc++]|
那么您可以从编译设置中删除此示例的“-Weffc++”标志，或者您可以向类中添加以下两行
IntArray(const IntArray&) = delete;
	IntArray& operator=(const IntArray&) = delete;
我们在课程
14.14 -- 拷贝构造函数简介
中讨论了成员的
=delete
。
这个程序产生的结果是
The value of element 5 is: 6
在 main() 的第一行，我们实例化了一个名为 ar 的新 IntArray 类对象，并传入长度为 10。这会调用构造函数，构造函数为数组成员动态分配内存。我们在这里必须使用动态分配，因为在编译时我们不知道数组的长度（调用者决定）。
在 main() 的末尾，ar 超出范围。这会导致 ~IntArray() 析构函数被调用，它会删除我们在构造函数中分配的数组！
提醒
在课程
16.2 -- std::vector 和 list 构造函数简介
中，我们注意到当使用长度（而不是元素列表）初始化数组/容器/列表类时，应该使用基于括号的初始化。因此，我们使用
IntArray ar ( 10 );
初始化 IntArray。
构造函数和析构函数的时间
如前所述，构造函数在对象创建时调用，析构函数在对象销毁时调用。在以下示例中，我们在构造函数和析构函数内部使用 cout 语句来演示这一点
#include <iostream>

class Simple
{
private:
    int m_nID{};

public:
    Simple(int nID)
        : m_nID{ nID }
    {
        std::cout << "Constructing Simple " << nID << '\n';
    }

    ~Simple()
    {
        std::cout << "Destructing Simple" << m_nID << '\n';
    }

    int getID() { return m_nID; }
};

int main()
{
    // Allocate a Simple on the stack
    Simple simple{ 1 };
    std::cout << simple.getID() << '\n';

    // Allocate a Simple dynamically
    Simple* pSimple{ new Simple{ 2 } };
    
    std::cout << pSimple->getID() << '\n';

    // We allocated pSimple dynamically, so we have to delete it.
    delete pSimple;

    return 0;
} // simple goes out of scope here
此程序产生以下结果：
Constructing Simple 1
1
Constructing Simple 2
2
Destructing Simple 2
Destructing Simple 1
请注意，“Simple 1”在“Simple 2”之后销毁，因为我们在函数结束前删除了 pSimple，而 simple 直到 main() 结束才销毁。
全局变量在 main() 之前构造，在 main() 之后销毁。
RAII
RAII（资源获取即初始化）是一种编程技术，其中资源的使用与具有自动持续时间的对象（例如非动态分配对象）的生命周期相关联。在 C++ 中，RAII 通过具有构造函数和析构函数的类来实现。资源（例如内存、文件或数据库句柄等）通常在对象的构造函数中获取（如果合理，也可以在对象创建后获取）。然后可以在对象存在期间使用该资源。当对象被销毁时，资源在析构函数中释放。RAII 的主要优点是它有助于防止资源泄漏（例如内存未释放），因为所有持有资源的对象都会自动清理。
本课顶部的 IntArray 类就是实现 RAII 的一个例子——在构造函数中分配，在析构函数中释放。std::string 和 std::vector 是标准库中遵循 RAII 的类的例子——动态内存在初始化时获取，并在销毁时自动清理。
关于 std::exit() 函数的警告
请注意，如果您使用 std::exit() 函数，您的程序将终止并且不会调用任何析构函数。如果您依赖析构函数进行必要的清理工作（例如在退出前将某些内容写入日志文件或数据库），请务必小心。
总结
如您所见，当构造函数和析构函数一起使用时，您的类可以自行初始化和清理，而无需程序员做任何特殊工作！这降低了出错的可能性，并使类更易于使用。
下一课
19.4
指向指针的指针和动态多维数组
返回目录
上一课
19.2
动态分配数组