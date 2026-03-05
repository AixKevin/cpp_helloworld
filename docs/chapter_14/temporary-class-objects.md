# 14.13 — 临时类对象

14.13 — 临时类对象
Alex
2007 年 12 月 27 日，太平洋标准时间上午 9:32
2024 年 12 月 20 日
考虑以下示例
#include <iostream>

int add(int x, int y)
{
    int sum{ x + y }; // stores x + y in a variable
    return sum;       // returns value of that variable
}

int main()
{
    std::cout << add(5, 3) << '\n';

    return 0;
}
在
add()
函数中，变量
sum
用于存储表达式
x + y
的结果。然后，在返回语句中评估此变量，以生成要返回的值。虽然这偶尔对调试可能有用（这样如果需要，我们可以检查
sum
的值），但它实际上通过定义一个仅使用一次的对象，使函数比需要的更复杂。
在大多数情况下，如果一个变量只使用一次，我们实际上不需要一个变量。相反，我们可以在使用变量的地方替换用于初始化变量的表达式。下面是这样重写的
add()
函数
#include <iostream>

int add(int x, int y)
{
    return x + y; // just return x + y directly
}

int main()
{
    std::cout << add(5, 3) << '\n';

    return 0;
}
这不仅适用于返回值，也适用于大多数函数参数。例如，而不是这样
#include <iostream>

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    int sum{ 5 + 3 };
    printValue(sum);

    return 0;
}
我们可以这样写
#include <iostream>

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    printValue(5 + 3);

    return 0;
}
注意这使我们的代码多么简洁。我们不必定义和命名变量。而且我们不必扫描整个函数来确定该变量是否在其他地方实际使用。因为
5 + 3
是一个表达式，我们知道它只在那一行中使用。
请注意，这仅适用于接受右值表达式的情况。在需要左值表达式的情况下，我们必须有一个对象
#include <iostream>

void addOne(int& value) // pass by non-const references requires lvalue
{
    ++value;
}

int main()
{
    int sum { 5 + 3 };
    addOne(sum);   // okay, sum is an lvalue

    addOne(5 + 3); // compile error: not an lvalue

    return 0;
}
临时类对象
同样的问题也适用于类类型。
作者注
我们这里将使用一个类，但本课程中所有使用列表初始化的内容同样适用于使用聚合初始化初始化的结构体。
以下示例与上面的示例相似，但使用程序定义的类类型
IntPair
而不是
int
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const { return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}
        
int main()
{
    // Case 1: Pass variable
    IntPair p { 3, 4 };
    print(p); // prints (3, 4)
    
    return 0;
}
在案例 1 中，我们实例化变量
IntPair p
，然后将
p
传递给函数
print()
。
然而，
p
只使用一次，并且函数
print()
将接受右值，因此这里确实没有理由定义一个变量。所以让我们摆脱
p
。
我们可以通过传递一个临时对象而不是一个命名变量来做到这一点。
临时对象
（有时称为
匿名对象
或
未命名对象
）是一个没有名称且仅在单个表达式的持续时间内存在的对象。
有两种常见的方法来创建临时类类型对象
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const{ return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}
        
int main()
{
    // Case 1: Pass variable
    IntPair p { 3, 4 };
    print(p);

    // Case 2: Construct temporary IntPair and pass to function
    print(IntPair { 5, 6 } );

    // Case 3: Implicitly convert { 7, 8 } to a temporary Intpair and pass to function
    print( { 7, 8 } );
    
    return 0;
}
在案例 2 中，我们告诉编译器构造一个
IntPair
对象，并用
{ 5, 6 }
初始化它。因为这个对象没有名字，所以它是一个临时对象。然后将临时对象传递给函数
print()
的参数
p
。当函数调用返回时，临时对象被销毁。
在案例 3 中，我们还创建了一个临时
IntPair
对象以传递给函数
print()
。但是，由于我们没有明确指定要构造的类型，编译器将从函数参数中推断出所需的类型（
IntPair
），然后隐式地将
{ 7, 8 }
转换为
IntPair
对象。
总结一下
IntPair p { 1, 2 }; // create named object p initialized with { 1, 2 }
IntPair { 1, 2 };   // create temporary object initialized with { 1, 2 }
{ 1, 2 };           // compiler will try to convert { 1, 2 } to temporary object matching expected type (typically a parameter or return type)
我们将在课程
14.16 -- 转换构造函数和 explicit 关键字
中更详细地讨论最后一种情况。
更多示例
std::string { "Hello" }; // create a temporary std::string initialized with "Hello"
std::string {};          // create a temporary std::string using value initialization / default constructor
通过直接初始化创建临时对象
可选
既然我们可以通过直接列表初始化创建临时对象，您可能想知道是否可以通过其他初始化形式创建临时对象。没有语法可以通过复制初始化创建临时对象。
但是，您可以使用直接初始化创建临时对象。例如
Foo (1, 2); //  temporary Foo, direct-initialized with (1, 2) (similar to `Foo { 1, 2 }`)
抛开它乍一看像函数调用的事实不谈，这产生了与
Foo { 1, 2 }
相同的结果（只是没有收窄转换预防）。很正常对吗？
我们现在将花费本节的其余部分向您展示为什么您可能不应该这样做。
作者注
这主要供您阅读，而不是您需要消化、记忆和能够解释的东西。
即使您阅读起来没有那么有趣，它也可能帮助您理解为什么现代 C++ 中首选列表初始化！
现在让我们看看没有任何参数的情况
Foo();     // temporary Foo, value-initialized (identical to `Foo {}`)
您可能没想到
Foo()
会像
Foo {}
一样创建一个值初始化的临时对象。这可能是因为当与命名变量一起使用时，这种语法具有完全不同的含义！
Foo bar{}; // definition of variable bar, value-initialized
Foo bar(); // declaration of function bar that has no parameters and returns a Foo (inconsistent with `Foo bar{}` and `Foo()`)
准备好变得真正奇怪了吗？！？
Foo(1);    // Function-style cast of literal 1, returns temporary Foo (similar to `Foo { 1 }`)
Foo(bar);  // Defines variable bar of type Foo (inconsistent with `Foo { bar }` and `Foo(1)`)
等等，什么？
括号中带字面量
1
的版本与所有其他创建临时对象的此语法版本保持一致。
括号中带标识符
bar
的版本定义了一个名为
bar
的变量（与
Foo bar;
相同）。如果
bar
已经定义，这将导致重定义编译错误。
编译器知道字面量不能用作变量的标识符，因此它能够使该情况与其他情况保持一致。
题外话…
如果您想知道为什么
Foo(bar);
的行为与
Foo bar;
完全相同……
括号最常见的用途之一是分组。例如，在数学中：
(1 + 2) * 3
产生结果
9
，这与
1 + 2 * 3
不同，后者产生结果
7
。如果我们能做
(1 + 2) * 3
，就没有理由不能做
(3) * 3
。
出于类似的原因，声明语法允许基于括号的分组，并且这些组中可以只有一个事物。
Foo(bar)
被解释为由类型
Foo
后跟仅由标识符
bar
组成的组组成的变量定义。这看起来很奇怪，主要是因为括号在这种情况下没有任何有用的目的。但没有令人信服的理由禁止这样做（因为那只会使语言的语法更加复杂）。
致进阶读者
让我们看一个稍微复杂一点的例子。考虑语句
Foo * bar();
。通过使用（或不使用）括号，我们可以完全改变此语句的含义
Foo * bar();
（不带额外括号）默认将
*
与
Foo
分组。
Foo* bar();
是一个名为
bar
的函数的声明，该函数没有参数并返回一个
Foo*
。
Foo (*bar)();
明确将
*
与
bar
分组。这定义了一个名为
bar
的函数指针，它保存了一个不带参数并返回
Foo
的函数的地址。
Foo (* bar());
与
Foo * bar();
相同——在这种情况下括号是多余的。
最后
(Foo *) bar();
。您可能期望这与
Foo* bar()
相同，但这实际上是一个表达式语句，它调用函数
bar()
，将返回值 C 风格地转换为类型
Foo*
，然后将其丢弃！
C++ 有时就是这么奇怪。
关键见解
括号很复杂，因为它们被严重重载，并用于各种不同事物的语法中。这包括函数调用、对象的直接初始化、临时对象的值初始化、C 风格强制转换、符号/标识符的分组以及变量定义。因此，当您在某些语法中看到括号时……您将得到什么并不总是显而易见的！
另一方面，如果我们看到花括号，我们知道我们正在处理对象。
好了，好玩结束。回到无聊的事情上。
临时对象和按值返回
当函数按值返回时，返回的对象是一个临时对象（使用返回语句中标识的值或对象进行初始化）。
以下是一些示例
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const { return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}

// Case 1: Create named variable and return
IntPair ret1()
{
    IntPair p { 3, 4 };
    return p; // returns temporary object (initialized using p)
}

// Case 2: Create temporary IntPair and return
IntPair ret2()
{
    return IntPair { 5, 6 }; // returns temporary object (initialized using another temporary object)
}

// Case 3: implicitly convert { 7, 8 } to IntPair and return
IntPair ret3()
{
    return { 7, 8 }; // returns temporary object (initialized using another temporary object)
}
     
int main()
{
    print(ret1());
    print(ret2());
    print(ret3());

    return 0;
}
在案例 1 中，当我们
return p
时，会创建一个临时对象并使用
p
进行初始化。
此示例中的案例与先前示例中的案例类似。
几点说明
首先，就像
int
的情况一样，当在表达式中使用时，临时类对象是一个右值。因此，此类对象只能在接受右值表达式的地方使用。
其次，临时对象在定义点创建，并在定义它们的完整表达式结束时销毁。完整表达式是不是子表达式的表达式。
static_cast
与临时对象的显式实例化
在需要将值从一种类型转换为另一种类型但没有涉及收窄转换的情况下，我们通常可以选择使用
static_cast
或临时对象的显式实例化。
例如
#include <iostream>

int main()
{
    char c { 'a' };

    std::cout << static_cast<int>( c ) << '\n'; // static_cast returns a temporary int direct-initialized with value of c
    std::cout << int { c } << '\n';             // explicitly creates a temporary int list-initialized with value c

    return 0;
}
static_cast
(c)
返回一个临时
int
，它直接用
c
的值初始化。
int { c }
创建一个临时
int
，它用
c
的值进行列表初始化。无论哪种方式，我们都会得到一个用
c
的值初始化的临时 int，这正是我们想要的。
让我们展示一个稍微复杂一点的例子
printString.h
#include <string>
void printString(const std::string &s)
{
    std::cout << s << '\n';
}
main.cpp
#include "printString.h"
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view sv { "Hello" };

    // We want to print sv using the printString() function
    
//    printString(sv); // compile error: a std::string_view won't implicitly convert to a std::string

    printString( static_cast<std::string>(sv) ); // Case 1: static_cast returns a temporary std::string direct-initialized with sv
    printString( std::string { sv } );           // Case 2: explicitly creates a temporary std::string list-initialized with sv
    printString( std::string ( sv ) );           // Case 3: C-style cast returns temporary std::string direct-initialized with sv (avoid this one!)

    return 0;
}
假设头文件
printString.h
中的代码是我们无法修改的（例如，因为它随我们正在使用的某个第三方库一起分发，并且已编写为与 C++11 兼容，而 C++11 不支持
std::string_view
）。那么我们如何用
sv
调用
printString()
呢？由于
std::string_view
不会隐式转换为
std::string
（出于效率原因），我们不能简单地将
sv
用作参数。我们必须使用某种显式转换形式。
在案例 1 中，
static_cast
(sv)
调用 static_cast 运算符将
sv
转换为
std::string
。这返回一个临时
std::string
，它已使用
sv
进行直接初始化，然后将其用作函数调用的参数。
在案例 2 中，
std::string { sv }
创建一个临时
std::string
，它使用
sv
进行列表初始化。由于这是显式构造，因此允许转换。然后将此临时对象用作函数调用的参数。
在案例 3 中，
std::string ( sv )
使用 C 风格强制转换将
sv
强制转换为
std::string
。虽然这在这里有效，但 C 风格强制转换通常可能很危险，应避免使用。请注意这与前一个案例多么相似！
最佳实践
一个快速经验法则：在转换为基本类型时首选
static_cast
，在转换为类类型时首选列表初始化的临时对象。
在以下任何情况为真时，首选
static_cast
来创建临时对象：
我们需要执行收窄转换。
我们想明确表明我们正在转换为会导致不同行为的类型（例如，将
char
转换为
int
）。
出于某种原因，我们想使用直接初始化（例如，为了避免列表构造函数优先）。
在以下任何情况为真时，首选创建新对象（使用列表初始化）来创建临时对象：
我们想使用列表初始化（例如，为了防止收窄转换，或者因为我们需要调用列表构造函数）。
我们需要向构造函数提供额外的参数以促进转换。
相关内容
我们在课程
16.2 -- std::vector 和列表构造函数简介
中介绍了列表构造函数。
下一课
14.14
复制构造函数简介
返回目录
上一课
14.12
委托构造函数