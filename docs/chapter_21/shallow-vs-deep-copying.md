# 21.13 — 浅拷贝与深拷贝

21.13 — 浅拷贝与深拷贝
Alex
2007 年 11 月 9 日，下午 3:39 (太平洋标准时间)
2023 年 9 月 11 日
浅拷贝
由于 C++ 对你的类知之甚少，它提供的默认拷贝构造函数和默认赋值运算符使用一种称为成员拷贝（也称为
浅拷贝
）的拷贝方法。这意味着 C++ 会单独拷贝类的每个成员（对于重载的运算符 = 使用赋值运算符，对于拷贝构造函数使用直接初始化）。当类很简单时（例如不包含任何动态分配的内存），这种方法效果很好。
例如，让我们看看我们的 Fraction 类
#include <cassert>
#include <iostream>
 
class Fraction
{
private:
    int m_numerator { 0 };
    int m_denominator { 1 };
 
public:
    // Default constructor
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        assert(denominator != 0);
    }
 
    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
};
 
std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}
编译器为这个类提供的默认拷贝构造函数和默认赋值运算符看起来像这样
#include <cassert>
#include <iostream>
 
class Fraction
{
private:
    int m_numerator { 0 };
    int m_denominator { 1 };
 
public:
    // Default constructor
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        assert(denominator != 0);
    }
 
    // Possible implementation of implicit copy constructor
    Fraction(const Fraction& f)
        : m_numerator{ f.m_numerator }
        , m_denominator{ f.m_denominator }
    {
    }

    // Possible implementation of implicit assignment operator
    Fraction& operator= (const Fraction& fraction)
    {
        // self-assignment guard
        if (this == &fraction)
            return *this;
 
        // do the copy
        m_numerator = fraction.m_numerator;
        m_denominator = fraction.m_denominator;
 
        // return the existing object so we can chain this operator
        return *this;
    }

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1)
    {
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
    }
};
请注意，由于这些默认版本对于拷贝这个类运行良好，在这种情况下真的没有理由编写我们自己的这些函数版本。
然而，在设计处理动态分配内存的类时，成员拷贝（浅拷贝）会给我们带来很多麻烦！这是因为指针的浅拷贝只拷贝指针的地址——它不分配任何内存也不拷贝指向的内容！
我们来看一个例子
#include <cstring> // for strlen()
#include <cassert> // for assert()

class MyString
{
private:
    char* m_data{};
    int m_length{};
 
public:
    MyString(const char* source = "" )
    {
        assert(source); // make sure source isn't a null string

        // Find the length of the string
        // Plus one character for a terminator
        m_length = std::strlen(source) + 1;
        
        // Allocate a buffer equal to this length
        m_data = new char[m_length];
        
        // Copy the parameter string into our internal buffer
        for (int i{ 0 }; i < m_length; ++i)
            m_data[i] = source[i];
    }
 
    ~MyString() // destructor
    {
        // We need to deallocate our string
        delete[] m_data;
    }
 
    char* getString() { return m_data; }
    int getLength() { return m_length; }
};
上面是一个简单的字符串类，它分配内存来保存我们传入的字符串。请注意，我们没有定义拷贝构造函数或重载赋值运算符。因此，C++ 将提供一个执行浅拷贝的默认拷贝构造函数和默认赋值运算符。拷贝构造函数将如下所示
MyString::MyString(const MyString& source)
    : m_length { source.m_length }
    , m_data { source.m_data }
{
}
注意，m_data 只是 source.m_data 的浅指针拷贝，这意味着它们现在都指向同一个东西。
现在，考虑下面的代码片段
#include <iostream>

int main()
{
    MyString hello{ "Hello, world!" };
    {
        MyString copy{ hello }; // use default copy constructor
    } // copy is a local variable, so it gets destroyed here.  The destructor deletes copy's string, which leaves hello with a dangling pointer

    std::cout << hello.getString() << '\n'; // this will have undefined behavior

    return 0;
}
虽然这段代码看起来无害，但它包含一个会使程序表现出未定义行为的隐蔽问题！
我们来逐行分解这个例子
MyString hello{ "Hello, world!" };
这一行是无害的。它调用 MyString 构造函数，该构造函数分配一些内存，将 hello.m_data 设置为指向它，然后将字符串“Hello, world!”拷贝到其中。
MyString copy{ hello }; // use default copy constructor
这一行看起来也无害，但它实际上是我们问题的根源！当这一行被求值时，C++ 将使用默认拷贝构造函数（因为我们没有提供自己的）。这个拷贝构造函数会执行浅拷贝，将 copy.m_data 初始化为与 hello.m_data 相同的地址。结果，copy.m_data 和 hello.m_data 现在都指向同一块内存！
} // copy gets destroyed here
当 copy 超出作用域时，MyString 析构函数会在 copy 上被调用。析构函数会删除 copy.m_data 和 hello.m_data 都指向的动态分配的内存！因此，通过删除 copy，我们也（无意中）影响了 hello。变量 copy 随后被销毁，但 hello.m_data 却留下来指向已删除的（无效）内存！
std::cout << hello.getString() << '\n'; // this will have undefined behavior
现在你可以明白为什么这个程序会表现出未定义行为了。我们删除了 hello 指向的字符串，现在我们试图打印不再分配的内存的值。
这个问题的根源是拷贝构造函数进行的浅拷贝——在拷贝构造函数或重载赋值运算符中对指针值进行浅拷贝几乎总会带来麻烦。
深拷贝
解决这个问题的一种方法是对任何非空指针进行深拷贝。
深拷贝
会为拷贝分配内存，然后拷贝实际值，这样拷贝就存在于与源不同的内存中。这样，拷贝和源是独立的，并且不会以任何方式相互影响。执行深拷贝需要我们编写自己的拷贝构造函数和重载赋值运算符。
我们继续展示如何为 MyString 类完成此操作
// assumes m_data is initialized
void MyString::deepCopy(const MyString& source)
{
    // first we need to deallocate any value that this string is holding!
    delete[] m_data;

    // because m_length is not a pointer, we can shallow copy it
    m_length = source.m_length;

    // m_data is a pointer, so we need to deep copy it if it is non-null
    if (source.m_data)
    {
        // allocate memory for our copy
        m_data = new char[m_length];

        // do the copy
        for (int i{ 0 }; i < m_length; ++i)
            m_data[i] = source.m_data[i];
    }
    else
        m_data = nullptr;
}

// Copy constructor
MyString::MyString(const MyString& source)
{
    deepCopy(source);
}
如你所见，这比简单的浅拷贝复杂得多！首先，我们必须检查以确保源甚至有一个字符串（第 11 行）。如果有，那么我们分配足够的内存来保存该字符串的副本（第 14 行）。最后，我们必须手动拷贝字符串（第 17 行和第 18 行）。
现在我们来做重载赋值运算符。重载赋值运算符稍微复杂一些
// Assignment operator
MyString& MyString::operator=(const MyString& source)
{
    // check for self-assignment
    if (this != &source)
    {
        // now do the deep copy
        deepCopy(source);
    }

    return *this;
}
注意，我们的赋值运算符与拷贝构造函数非常相似，但有三个主要区别
我们添加了自赋值检查。
我们返回 *this，以便可以链式调用赋值运算符。
我们需要显式地释放字符串已经持有的任何值（这样当 m_data 稍后重新分配时就不会有内存泄漏）。这在 deepCopy() 内部处理。
当调用重载赋值运算符时，被赋值的项可能已经包含一个先前的值，我们需要确保在为新值分配内存之前清除它。对于非动态分配的变量（它们是固定大小），我们不必费心，因为新值会直接覆盖旧值。然而，对于动态分配的变量，我们需要在分配任何新内存之前显式地释放任何旧内存。如果我们不这样做，代码不会崩溃，但每次赋值时都会出现内存泄漏，这将耗尽我们的可用内存！
三法则
还记得三法则吗？如果一个类需要用户定义的析构函数、拷贝构造函数或拷贝赋值运算符，那么它可能需要所有这三个。这就是原因。如果我们要用户定义这些函数中的任何一个，很可能是因为我们正在处理动态内存分配。我们需要拷贝构造函数和拷贝赋值来处理深拷贝，以及析构函数来释放内存。
一个更好的解决方案
标准库中处理动态内存的类，例如 std::string 和 std::vector，处理它们所有的内存管理，并且重载了拷贝构造函数和赋值运算符，执行正确的深拷贝。所以，你不需要自己进行内存管理，只需像普通的内置变量一样初始化或赋值它们！这使得这些类使用起来更简单，更不容易出错，而且你无需花费时间编写自己的重载函数！
总结
默认拷贝构造函数和默认赋值运算符执行浅拷贝，这对于不包含任何动态分配变量的类来说是没问题的。
包含动态分配变量的类需要有一个执行深拷贝的拷贝构造函数和赋值运算符。
优先使用标准库中的类，而不是自己进行内存管理。
下一课
21.14
重载运算符和函数模板
返回目录
上一课
21.12
重载赋值运算符