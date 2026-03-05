# 14.14 — 拷贝构造函数简介

14.14 — 拷贝构造函数简介
Alex
2007年11月4日，上午8:52 PST
2024年12月19日
考虑以下程序
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // Default constructor
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };  // Calls Fraction(int, int) constructor
    Fraction fCopy { f }; // What constructor is used here?

    f.print();
    fCopy.print();

    return 0;
}
你可能会惊讶地发现，这个程序编译运行良好，并产生了以下结果
Fraction(5, 3)
Fraction(5, 3)
让我们仔细看看这个程序是如何工作的。
变量
f
的初始化只是一个标准的括号初始化，它调用了
Fraction(int, int)
构造函数。
但下一行呢？变量
fCopy
的初始化显然也是一个初始化，而且你知道构造函数用于初始化类。那么这一行调用的是哪个构造函数呢？
答案是：拷贝构造函数。
拷贝构造函数
拷贝构造函数
是一个构造函数，用于使用同一类型的现有对象初始化一个对象。在拷贝构造函数执行后，新创建的对象应该是作为初始化器传入的对象的副本。
隐式拷贝构造函数
如果你不为你的类提供拷贝构造函数，C++会为你创建一个公共的
隐式拷贝构造函数
。在上面的例子中，语句
Fraction fCopy { f };
正在调用隐式拷贝构造函数来用
f
初始化
fCopy
。
默认情况下，隐式拷贝构造函数将进行成员初始化。这意味着每个成员都将使用作为初始化器传入的类的相应成员进行初始化。在上面的例子中，
fCopy.m_numerator
使用
f.m_numerator
（值为
5
）初始化，而
fCopy.m_denominator
使用
f.m_denominator
（值为
3
）初始化。
拷贝构造函数执行后，
f
和
fCopy
的成员具有相同的值，因此
fCopy
是
f
的副本。因此，对两者调用
print()
会产生相同的结果。
定义你自己的拷贝构造函数
我们也可以显式定义自己的拷贝构造函数。在本课中，我们将使我们的拷贝构造函数打印一条消息，这样我们就可以向您展示它在创建副本时确实正在执行。
拷贝构造函数看起来就像你预期的那样
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // Default constructor
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // Copy constructor
    Fraction(const Fraction& fraction)
        // Initialize our members using the corresponding member of the parameter
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "Copy constructor called\n"; // just to prove it works
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };  // Calls Fraction(int, int) constructor
    Fraction fCopy { f }; // Calls Fraction(const Fraction&) copy constructor

    f.print();
    fCopy.print();

    return 0;
}
当这个程序运行时，你会得到
Copy constructor called
Fraction(5, 3)
Fraction(5, 3)
我们上面定义的拷贝构造函数在功能上等同于我们默认获得的拷贝构造函数，只是我们添加了一个输出语句来证明拷贝构造函数确实被调用了。当
fCopy
用
f
初始化时，这个拷贝构造函数被调用。
提醒
访问控制是按类（而不是按对象）进行的。这意味着类的成员函数可以访问同类型任何类对象的私有成员（而不仅仅是隐式对象）。
我们在上面的
Fraction
拷贝构造函数中利用了这一点，以便直接访问
fraction
参数的私有成员。否则，我们将无法直接访问这些成员（除非添加访问函数，而我们可能不想这样做）。
拷贝构造函数除了复制对象之外不应该做任何事情。这是因为编译器在某些情况下可能会优化掉拷贝构造函数。如果你依赖拷贝构造函数实现除复制之外的某些行为，那么该行为可能发生也可能不发生。我们将在课程
14.15 -- 类初始化和拷贝省略
中进一步讨论这个问题。
最佳实践
拷贝构造函数除了复制之外不应有副作用。
优先使用隐式拷贝构造函数
与什么都不做（因此很少是我们想要的）的隐式默认构造函数不同，隐式拷贝构造函数执行的成员初始化通常正是我们想要的。因此，在大多数情况下，使用隐式拷贝构造函数完全没问题。
最佳实践
优先使用隐式拷贝构造函数，除非你有特定理由创建自己的拷贝构造函数。
当我们讨论动态内存分配时，我们会看到需要重写拷贝构造函数的情况（
21.13 -- 浅拷贝与深拷贝
）。
拷贝构造函数的参数必须是引用
拷贝构造函数的参数必须是左值引用或const左值引用。因为拷贝构造函数不应该修改参数，所以首选使用const左值引用。
最佳实践
如果你自己编写拷贝构造函数，参数应该是const左值引用。
按值传递和拷贝构造函数
当一个对象按值传递时，实参被复制到形参中。当实参和形参是相同的类类型时，通过隐式调用拷贝构造函数进行复制。
这在以下示例中得到了说明
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    // Default constructor
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }, m_denominator{ denominator }
    {
    }

    // Copy constructor
    Fraction(const Fraction& fraction)
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "Copy constructor called\n";
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

void printFraction(Fraction f) // f is pass by value
{
    f.print();
}

int main()
{
    Fraction f{ 5, 3 };

    printFraction(f); // f is copied into the function parameter using copy constructor

    return 0;
}
在作者的机器上，这个例子打印出
Copy constructor called
Fraction(5, 3)
在上面的例子中，对
printFraction(f)
的调用是按值传递
f
。调用拷贝构造函数将
f
从
main
复制到函数
printFraction()
的
f
参数中。
按值返回和拷贝构造函数
在课程
2.5 -- 局部作用域简介
中，我们指出按值返回会创建一个临时对象（持有返回值的副本），该对象被返回给调用者。当返回类型和返回值是相同的类类型时，临时对象通过隐式调用拷贝构造函数进行初始化。
例如
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    // Default constructor
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }, m_denominator{ denominator }
    {
    }

    // Copy constructor
    Fraction(const Fraction& fraction)
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "Copy constructor called\n";
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

void printFraction(Fraction f) // f is pass by value
{
    f.print();
}

Fraction generateFraction(int n, int d)
{
    Fraction f{ n, d };
    return f;
}

int main()
{
    Fraction f2 { generateFraction(1, 2) }; // Fraction is returned using copy constructor

    printFraction(f2); // f2 is copied into the function parameter using copy constructor

    return 0;
}
当
generateFraction
将一个
Fraction
返回给
main
时，会创建一个临时的
Fraction
对象并使用拷贝构造函数进行初始化。
因为这个临时对象用于初始化
Fraction f2
，所以这会再次调用拷贝构造函数，将临时对象复制到
f2
中。
当
f2
传递给
printFraction()
时，拷贝构造函数被第三次调用。
因此，在作者的机器上，这个例子打印出
Copy constructor called
Copy constructor called
Copy constructor called
Fraction(1, 2)
如果你编译并执行上面的例子，你可能会发现只发生了两次拷贝构造函数的调用。这是一种编译器优化，称为
拷贝省略
。我们将在课程
14.15 -- 类初始化和拷贝省略
中进一步讨论拷贝省略。
使用
= default
生成默认拷贝构造函数
如果一个类没有拷贝构造函数，编译器会隐式为我们生成一个。如果我们愿意，我们可以使用
= default
语法显式请求编译器为我们创建一个默认拷贝构造函数
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // Default constructor
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // Explicitly request default copy constructor
    Fraction(const Fraction& fraction) = default;

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };
    Fraction fCopy { f };

    f.print();
    fCopy.print();

    return 0;
}
使用
= delete
防止拷贝
有时我们会遇到不希望某个类的对象可拷贝的情况。我们可以通过使用
= delete
语法将拷贝构造函数标记为已删除来防止这种情况
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // Default constructor
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // Delete the copy constructor so no copies can be made
    Fraction(const Fraction& fraction) = delete;

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };
    Fraction fCopy { f }; // compile error: copy constructor has been deleted

    return 0;
}
在这个例子中，当编译器查找构造函数来用
f
初始化
fCopy
时，它会发现拷贝构造函数已被删除。这将导致它发出编译错误。
题外话…
你也可以通过将拷贝构造函数设为私有来阻止公共用户创建类对象的副本（因为私有函数不能被公共用户使用）。但是，私有拷贝构造函数仍然可以被类的其他成员使用，因此除非这是你想要的，否则不建议使用此解决方案。
致进阶读者
三法则
是一个著名的C++原则，它指出如果一个类需要用户定义的拷贝构造函数、析构函数或拷贝赋值运算符，那么它可能需要所有这三者。在C++11中，这被扩展为
五法则
，它将移动构造函数和移动赋值运算符添加到列表中。
不遵循三法则/五法则很可能导致代码出现故障。当我们讨论动态内存分配时，我们将重新讨论三法则和五法则。
我们将在课程
15.4 -- 析构函数简介
和
19.3 -- 析构函数
中讨论析构函数，并在课程
21.12 -- 重载赋值运算符
中讨论拷贝赋值。
小测验时间
问题 #1
在上面的课程中，我们指出拷贝构造函数的参数必须是（const）引用。为什么不允许我们使用按值传递？
显示提示
提示：想想当我们按值传递类类型实参时会发生什么。
显示答案
当我们按值传递类类型实参时，拷贝构造函数会隐式调用，将实参复制到形参中。
如果拷贝构造函数使用按值传递，那么拷贝构造函数需要调用自身来将初始化器实参复制到拷贝构造函数形参中。但是对拷贝构造函数的调用也将是按值传递的，因此拷贝构造函数将再次被调用以将实参复制到函数形参中。这将导致对拷贝构造函数的无限调用链。
下一课
14.15
类初始化和拷贝省略
返回目录
上一课
14.13
临时类对象