# 14.16 — 转换构造函数和 explicit 关键字

14.16 — 转换构造函数和 explicit 关键字
Alex
2016年6月5日，上午10:50 PDT
2025年2月1日
在
10.1 — 隐式类型转换
课程中，我们介绍了类型转换和隐式类型转换的概念，即如果存在此类转换，编译器会根据需要将一种类型的值隐式转换为另一种类型的值。
这允许我们执行以下操作：
#include <iostream>

void printDouble(double d) // has a double parameter
{
    std::cout << d;
}

int main()
{
    printDouble(5); // we're supplying an int argument

    return 0;
}
在上面的示例中，我们的
printDouble
函数有一个
double
参数，但我们传入了一个
int
类型的实参。因为参数类型和实参类型不匹配，编译器将查看是否可以隐式地将实参类型转换为参数类型。在这种情况下，使用数字转换规则，int 值
5
将转换为 double 值
5.0
，并且由于我们是按值传递，参数
d
将使用此值进行拷贝初始化。
用户定义的转换
现在考虑以下类似示例：
#include <iostream>

class Foo
{
private:
    int m_x{};
public:
    Foo(int x)
        : m_x{ x }
    {
    }

    int getX() const { return m_x; }
};

void printFoo(Foo f) // has a Foo parameter
{
    std::cout << f.getX();
}

int main()
{
    printFoo(5); // we're supplying an int argument

    return 0;
}
在这个版本中，
printFoo
有一个
Foo
参数，但我们传入了一个
int
类型的实参。因为这些类型不匹配，编译器将尝试将 int 值
5
隐式转换为
Foo
对象，以便可以调用该函数。
与第一个示例不同，在第一个示例中，我们的参数和实参类型都是基本类型（因此可以使用内置的数字提升/转换规则进行转换），在这种情况下，我们的一种类型是程序定义的类型。C++ 标准没有具体的规则告诉编译器如何将值转换为（或从）程序定义的类型。
相反，编译器会查看我们是否定义了一些它可以用来执行此类转换的函数。这样的函数称为
用户定义的转换
。
转换构造函数
在上面的示例中，编译器将找到一个函数，允许它将 int 值
5
转换为
Foo
对象。该函数是
Foo(int)
构造函数。
到目前为止，我们通常使用构造函数来显式构造对象。
Foo x { 5 }; // Explicitly convert int value 5 to a Foo
思考一下这做了什么：我们提供一个
int
值（
5
），并返回一个
Foo
对象。
在函数调用的上下文中，我们正在尝试解决相同的问题：
printFoo(5); // Implicitly convert int value 5 into a Foo
我们提供一个
int
值（
5
），并且我们想要一个
Foo
对象作为回报。
Foo(int)
构造函数正是为此而设计的！
因此，在这种情况下，当调用
printFoo(5)
时，参数
f
使用
Foo(int)
构造函数，以
5
作为实参进行拷贝初始化！
题外话…
在 C++17 之前，当调用
printFoo(5)
时，
5
会使用
Foo(int)
构造函数隐式转换为一个临时
Foo
对象。然后，这个临时
Foo
对象会被拷贝构造到参数
f
中。
从 C++17 开始，强制省略拷贝。参数
f
会用值
5
进行拷贝初始化，不需要调用拷贝构造函数（即使拷贝构造函数被删除，它也能工作）。
可以用于执行隐式转换的构造函数称为
转换构造函数
。默认情况下，所有构造函数都是转换构造函数。
只能应用一个用户定义的转换
现在考虑以下示例：
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};

public:
    Employee(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
};

void printEmployee(Employee e) // has an Employee parameter
{
    std::cout << e.getName();
}

int main()
{
    printEmployee("Joe"); // we're supplying an string literal argument

    return 0;
}
在此版本中，我们将
Foo
类替换为
Employee
类。
printEmployee
有一个
Employee
参数，我们传入一个 C 风格的字符串字面量。我们还有一个转换构造函数：
Employee(std::string_view)
。
你可能会惊讶地发现这个版本无法编译。原因很简单：只能应用一个用户定义的转换来执行隐式转换，而此示例需要两个。首先，我们的 C 风格字符串字面量必须转换为
std::string_view
（使用
std::string_view
转换构造函数），然后我们的
std::string_view
必须转换为
Employee
（使用
Employee(std::string_view)
转换构造函数）。
有两种方法可以使此示例正常工作：
使用
std::string_view
字面量
int main()
{
    using namespace std::literals;
    printEmployee( "Joe"sv); // now a std::string_view literal

    return 0;
}
这之所以可行，是因为现在只需要一个用户定义的转换（从
std::string_view
到
Employee
）。
显式构造
Employee
而不是隐式创建
int main()
{
    printEmployee(Employee{ "Joe" });

    return 0;
}
这也有效，因为现在只需要一个用户定义的转换（从字符串字面量到用于初始化
Employee
对象的
std::string_view
）。将我们显式构造的
Employee
对象传递给函数不需要进行第二次转换。
后一个例子提出了一种有用的技术：将隐式转换转换为显式定义是微不足道的。在本课后面我们将看到更多这样的例子。
关键见解
通过使用直接列表初始化（或直接初始化），可以将隐式转换轻松地转换为显式定义。
转换构造函数出错时
考虑以下程序
#include <iostream>

class Dollars
{
private:
    int m_dollars{};

public:
    Dollars(int d)
        : m_dollars{ d }
    {
    }

    int getDollars() const { return m_dollars; }
};

void print(Dollars d)
{
    std::cout << "$" << d.getDollars();
}

int main()
{
    print(5);

    return 0;
}
当我们调用
print(5)
时，
Dollars(int)
转换构造函数将用于将
5
转换为
Dollars
对象。因此，此程序将打印：
$5
尽管这可能是调用者的意图，但很难判断，因为调用者没有提供任何迹象表明这是他们真正想要的。调用者完全有可能假设这会打印
5
，并且不希望编译器静默地隐式将我们的
int
值转换为
Dollars
对象，以便满足此函数调用。
虽然这个例子很简单，但在更大、更复杂的程序中，编译器执行一些你没有预料到的隐式转换，导致运行时出现意外行为，这是相当容易发生的。
如果我们的
print(Dollars)
函数只能用
Dollars
对象调用，而不是任何可以隐式转换为
Dollars
的值（特别是像
int
这样的基本类型），那就更好了。这将减少无意中发生错误的可能性。
explicit 关键字
为了解决此类问题，我们可以使用
explicit
关键字来告诉编译器构造函数不应作为转换构造函数使用。
将构造函数声明为
explicit
会产生两个显著后果：
显式构造函数不能用于拷贝初始化或拷贝列表初始化。
显式构造函数不能用于隐式转换（因为这会使用拷贝初始化或拷贝列表初始化）。
让我们将前面示例中的
Dollars(int)
构造函数更新为显式构造函数：
#include <iostream>

class Dollars
{
private:
    int m_dollars{};

public:
    explicit Dollars(int d) // now explicit
        : m_dollars{ d }
    {
    }

    int getDollars() const { return m_dollars; }
};

void print(Dollars d)
{
    std::cout << "$" << d.getDollars();
}

int main()
{
    print(5); // compilation error because Dollars(int) is explicit

    return 0;
}
因为编译器不能再将
Dollars(int)
用作转换构造函数，所以它无法找到将
5
转换为
Dollars
的方法。因此，它将生成一个编译错误。
对于具有单独声明（在类内部）和定义（在类外部）的构造函数，
explicit
关键字仅用于声明。
显式构造函数可用于直接初始化和直接列表初始化
显式构造函数仍然可以用于直接初始化和直接列表初始化
// Assume Dollars(int) is explicit
int main()
{
    Dollars d1(5); // ok
    Dollars d2{5}; // ok
}
现在，让我们回到前面的例子，在那里我们把
Dollars(int)
构造函数设为显式的，因此下面的代码会产生一个编译错误：
print(5); // compilation error because Dollars(int) is explicit
如果我们确实想用
int
值
5
调用
print()
，但构造函数是显式的，该怎么办？解决方法很简单：我们可以显式地定义
Dollars
对象，而不是让编译器隐式地将
5
转换为可以传递给
print()
的
Dollars
：
print(Dollars{5}); // ok: explicitly create a Dollars
这是允许的，因为我们仍然可以使用显式构造函数来列表初始化对象。而且由于我们现在已经显式地构造了一个
Dollars
，参数类型与形参类型匹配，所以不需要进行转换！
这不仅能够编译和运行，还能更好地记录我们的意图，因为它明确表明我们打算用
Dollars
对象调用此函数。
请注意，
static_cast
返回一个直接初始化的对象，因此它在执行转换时会考虑显式构造函数
print(static_cast<Dollars>(5)); // ok: static_cast will use explicit constructors
按值返回和显式构造函数
当我们从函数返回一个值时，如果该值与函数的返回类型不匹配，就会发生隐式转换。就像按值传递一样，这种转换不能使用显式构造函数。
以下程序展示了返回值的一些变体及其结果：
#include <iostream>

class Foo
{
public:
    explicit Foo() // note: explicit (just for sake of example)
    {
    }

    explicit Foo(int x) // note: explicit
    {
    }
};

Foo getFoo()
{
    // explicit Foo() cases
    return Foo{ };   // ok
    return { };      // error: can't implicitly convert initializer list to Foo

    // explicit Foo(int) cases
    return 5;        // error: can't implicitly convert int to Foo
    return Foo{ 5 }; // ok
    return { 5 };    // error: can't implicitly convert initializer list to Foo
}

int main()
{
    return 0;
}
或许令人惊讶的是，
return { 5 }
被认为是一种转换。
使用
explicit
的最佳实践
现代的最佳实践是默认将接受单个参数的任何构造函数声明为
explicit
。这包括具有多个参数（其中大多数或所有参数都有默认值）的构造函数。这将阻止编译器将该构造函数用于隐式转换。如果需要隐式转换，则只会考虑非显式构造函数。如果找不到执行转换的非显式构造函数，编译器将报错。
如果在特定情况下确实需要这种转换，那么通过直接列表初始化将隐式转换转换为显式定义是微不足道的。
以下
不应
显式声明：
拷贝（和移动）构造函数（因为它们不执行转换）。
以下
通常不
显式声明：
没有参数的默认构造函数（因为这些构造函数只用于将
{}
转换为默认对象，这通常是我们不需要限制的）。
只接受多个参数的构造函数（因为这些构造函数通常无论如何都不是转换的候选者）。
但是，如果你愿意，可以将上述标记为
explicit
，以防止使用空和多参数列表进行隐式转换。
以下
通常应
显式声明：
接受单个参数的构造函数。
在某些情况下，将单参数构造函数设为非显式是有意义的。当以下所有条件都为真时，这会很有用：
构造的对象在语义上等同于实参值。
转换性能良好。
例如，接受 C 风格字符串参数的
std::string_view
构造函数不是显式的，因为不太可能出现我们不愿意将 C 风格字符串视为
std::string_view
的情况。相反，接受
std::string_view
的
std::string
构造函数被标记为显式的，因为虽然
std::string
值在语义上等同于
std::string_view
值，但构造
std::string
的性能不佳。
最佳实践
默认情况下，将任何接受单个参数的构造函数声明为
explicit
。如果类型之间的隐式转换在语义上等价且性能良好，你可以考虑将构造函数声明为非
explicit
。
不要将拷贝或移动构造函数声明为显式，因为它们不执行转换。
下一课
14.17
Constexpr 聚合和类
返回目录
上一课
14.15
类初始化和拷贝省略