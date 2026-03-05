# 12.6 — 按 const 左值引用传递

12.6 — 按 const 左值引用传递
Alex
2023 年 7 月 26 日，太平洋夏令时间下午 4:26
2024 年 11 月 21 日
与非 const 引用（只能绑定到可修改的左值）不同，const 引用可以绑定到可修改的左值、不可修改的左值和右值。因此，如果我们将引用参数设为 const，它就能够绑定到任何类型的实参
#include <iostream>

void printRef(const int& y) // y is a const reference
{
    std::cout << y << '\n';
}

int main()
{
    int x { 5 };
    printRef(x);   // ok: x is a modifiable lvalue, y binds to x

    const int z { 5 };
    printRef(z);   // ok: z is a non-modifiable lvalue, y binds to z

    printRef(5);   // ok: 5 is rvalue literal, y binds to temporary int object

    return 0;
}
通过 const 引用传递提供与通过非 const 引用传递相同的首要优点（避免复制实参），同时还保证函数无法更改被引用的值。
例如，以下是不允许的，因为
ref
是 const
void addOne(const int& ref)
{
    ++ref; // not allowed: ref is const
}
在大多数情况下，我们不希望函数修改实参的值。
最佳实践
优先使用 const 引用传递，而不是非 const 引用传递，除非你有特殊原因需要这样做（例如，函数需要更改实参的值）。
现在我们可以理解允许 const 左值引用绑定到右值的动机：如果没有这个能力，就无法将字面量（或其他右值）传递给使用引用传递的函数！
将不同类型的实参传递给 const 左值引用参数
在
12.4 -- Const 的左值引用
这一课中，我们提到 const 左值引用可以绑定到不同类型的值，只要该值可以转换为引用的类型。这种转换会创建一个临时对象，引用参数随后可以绑定到该对象。
允许这样做的主要动机是，我们可以以完全相同的方式将值作为实参传递给值参数或 const 引用参数
#include <iostream>

void printVal(double d)
{
    std::cout << d << '\n';
}

void printRef(const double& d)
{
    std::cout << d << '\n';
}

int main()
{
    printVal(5); // 5 converted to temporary double, copied to parameter d
    printRef(5); // 5 converted to temporary double, bound to parameter d
    
    return 0;
}
通过值传递时，我们期望会进行复制，所以如果首先发生转换（导致额外的复制），这很少是一个问题（并且编译器可能会优化掉其中一个复制）。
然而，当我们不希望进行复制时，我们经常使用通过引用传递。如果首先发生转换，这通常会导致进行（可能开销很大的）复制，这可能不是最佳的。
警告
通过引用传递时，请确保实参的类型与引用的类型匹配，否则将导致意外的（并且可能开销很大的）转换。
混合使用值传递和引用传递
具有多个参数的函数可以单独确定每个参数是按值传递还是按引用传递。
例如
#include <string>

void foo(int a, int& b, const std::string& c)
{
}

int main()
{
    int x { 5 };
    const std::string s { "Hello, world!" };

    foo(5, x, s);

    return 0;
}
在上面的例子中，第一个实参按值传递，第二个按引用传递，第三个按 const 引用传递。
何时使用值传递与引用传递
对于大多数 C++ 初学者来说，选择使用值传递还是引用传递并不是很明显。幸运的是，有一个简单的经验法则可以在大多数情况下很好地为您服务。
基本类型和枚举类型复制成本低，因此通常按值传递。
类类型复制成本可能很高（有时非常高），因此通常按 const 引用传递。
最佳实践
作为经验法则，基本类型按值传递，类类型按 const 引用传递。
如果您不确定该怎么做，请使用 const 引用传递，因为您不太可能遇到意外行为。
提示
以下是其他一些有趣案例的部分列表
以下通常按值传递（因为它更高效）
枚举类型（无作用域和有作用域枚举）。
视图和 Span（例如
std::string_view
,
std::span
）。
模拟引用或（非拥有）指针的类型（例如迭代器，
std::reference_wrapper
）。
具有值语义且复制开销低的类类型（例如，元素为基本类型的
std::pair
，
std::optional
，
std::expected
）。
以下情况应使用引用传递
需要由函数修改的实参。
不可复制的类型（例如
std::ostream
）。
复制具有我们希望避免的所有权含义的类型（例如
std::unique_ptr
，
std::shared_ptr
）。
具有虚函数或可能被继承的类型（由于对象切片问题，详见
25.9 -- 对象切片
课程）。
按值传递与按引用传递的成本
高级
并非所有类类型都需要按引用传递（例如
std::string_view
，通常按值传递）。您可能想知道为什么我们不直接将所有内容都按引用传递。在本节（可选阅读）中，我们将讨论按值传递与按引用传递的成本，并完善我们何时使用它们的最佳实践。
首先，我们需要考虑初始化函数参数的成本。对于按值传递，初始化意味着进行复制。复制对象的成本通常与两件事成正比
对象的大小。占用更多内存的对象需要更长的时间复制。
任何额外的设置成本。某些类类型在实例化时会进行额外的设置（例如，打开文件或数据库，或分配一定量的动态内存以容纳可变大小的对象）。这些设置成本在每次复制对象时都必须支付。
另一方面，将引用绑定到对象总是很快的（大约与复制基本类型的速度相同）。
其次，我们需要考虑使用函数参数的成本。在设置函数调用时，编译器可以通过将传递值参数的引用或副本（如果大小很小）放入 CPU 寄存器（访问速度快）而不是 RAM（访问速度慢）来优化。
每次使用值参数时，运行程序可以直接访问复制实参的存储位置（CPU 寄存器或 RAM）。然而，当使用引用参数时，通常会有一个额外的步骤。运行程序必须首先直接访问分配给引用的存储位置（CPU 寄存器或 RAM），以确定正在引用哪个对象。只有这样才能访问被引用对象的存储位置（在 RAM 中）。
因此，每次使用值参数都是一次 CPU 寄存器或 RAM 访问，而每次使用引用参数都是一次 CPU 寄存器或 RAM 访问加上第二次 RAM 访问。
第三，编译器有时可以比使用引用传递的代码更有效地优化使用值传递的代码。特别是，当存在任何**别名**的可能性时，优化器必须保守（当两个或多个指针或引用可以访问同一个对象时）。由于按值传递会复制实参值，因此不会发生别名，从而允许优化器更加激进。
我们现在可以回答为什么不将所有内容都按引用传递的问题
对于复制开销小的对象，复制的开销与绑定的开销相似，但访问对象更快，并且编译器可能能够更好地优化。
对于复制开销大的对象，复制的开销主导其他性能考虑因素。
那么最后一个问题是，我们如何定义“复制开销小”？这里没有绝对的答案，因为这因编译器、用例和架构而异。但是，我们可以制定一个很好的经验法则：如果对象使用 2 个或更少“字”的内存（其中“字”近似于内存地址的大小）并且没有设置成本，则它复制开销小。
以下程序定义了一个函数式宏，可用于相应地确定类型（或对象）是否复制开销小
#include <iostream>

// Function-like macro that evaluates to true if the type (or object) is equal to or smaller than
// the size of two memory addresses
#define isSmall(T) (sizeof(T) <= 2 * sizeof(void*))

struct S
{
    double a;
    double b;
    double c;
};

int main()
{
    std::cout << std::boolalpha; // print true or false rather than 1 or 0
    std::cout << isSmall(int) << '\n'; // true

    double d {};
    std::cout << isSmall(d) << '\n'; // true
    std::cout << isSmall(S) << '\n'; // false

    return 0;
}
题外话…
我们在这里使用预处理器函数式宏，以便我们可以提供对象或类型名称作为参数（因为 C++ 函数不允许将类型作为参数传递）。
然而，很难知道类类型对象是否有设置成本。最好假设大多数标准库类都有设置成本，除非您另有了解它们没有。
提示
如果
sizeof(T) <= 2 * sizeof(void*)
且没有额外的设置成本，则类型 T 的对象复制开销小。
对于函数参数，在大多数情况下，首选
std::string_view
而非
const std::string&
在现代 C++ 中经常出现一个问题：在编写具有字符串参数的函数时，参数的类型应该是
const std::string&
还是
std::string_view
？
在大多数情况下，
std::string_view
是更好的选择，因为它可以高效地处理更广泛的参数类型。
std::string_view
参数还允许调用者传入子字符串，而无需首先将该子字符串复制到自己的字符串中。
void doSomething(const std::string&);
void doSomething(std::string_view);   // prefer this in most cases
在少数情况下，使用
const std::string&
参数可能更合适
如果您使用的是 C++14 或更早版本，则
std::string_view
不可用。
如果您的函数需要调用其他接受 C 风格字符串或
std::string
参数的函数，则
const std::string&
可能是一个更好的选择，因为
std::string_view
不保证以 null 结尾（C 风格字符串函数期望的）并且不能高效地转换回
std::string
。
最佳实践
首选使用
std::string_view
（按值）传递字符串，而不是
const std::string&
，除非您的函数调用其他需要 C 风格字符串或
std::string
参数的函数。
为什么
std::string_view
参数比
const std::string&
更高效
高级
在 C++ 中，字符串参数通常是
std::string
、
std::string_view
或 C 风格字符串/字符串字面量。
提醒：
如果实参的类型与相应参数的类型不匹配，编译器将尝试隐式转换实参以匹配参数的类型。
转换值会创建转换类型的临时对象。
创建（或复制）
std::string_view
的成本很低，因为
std::string_view
不会复制它正在查看的字符串。
创建（或复制）
std::string
的成本可能很高，因为每个
std::string
对象都会复制字符串。
下表显示了当我们尝试传递每种类型时会发生什么
参数类型
std::string_view 参数
const std::string& 参数
std::string
开销低的转换
开销低的引用绑定
std::string_view
开销低的复制
开销大的显式转换为
std::string
C 风格字符串 / 字面量
开销低的转换
开销大的转换
带有
std::string_view
值参数
如果我们传入
std::string
参数，编译器会将
std::string
转换为
std::string_view
，这开销低，所以没问题。
如果我们传入
std::string_view
参数，编译器会将参数复制到参数中，这开销低，所以没问题。
如果我们传入 C 风格字符串或字符串字面量，编译器会将它们转换为
std::string_view
，这开销低，所以没问题。
正如您所看到的，
std::string_view
可以廉价地处理所有三种情况。
带有
const std::string&
引用参数
如果我们传入
std::string
参数，参数将引用绑定到参数，这开销低，所以没问题。
如果我们传入
std::string_view
参数，编译器将拒绝进行隐式转换，并产生编译错误。我们可以使用
static_cast
进行显式转换（转换为
std::string
），但这种转换开销大（因为
std::string
将复制正在查看的字符串）。一旦转换完成，参数将引用绑定到结果，这开销低。但我们为了进行转换而进行了开销大的复制，所以这并不理想。
如果我们传入 C 风格字符串或字符串字面量，编译器将隐式将其转换为
std::string
，这开销大。所以这也不理想。
因此，
const std::string&
参数只能廉价地处理
std::string
参数。
同样，以代码形式
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view sv)
{
    std::cout << sv << '\n';
}

void printS(const std::string& s)
{
    std::cout << s << '\n';
}

int main()
{
    std::string s{ "Hello, world" };
    std::string_view sv { s };

    // Pass to `std::string_view` parameter
    printSV(s);              // ok: inexpensive conversion from std::string to std::string_view
    printSV(sv);             // ok: inexpensive copy of std::string_view
    printSV("Hello, world"); // ok: inexpensive conversion of C-style string literal to std::string_view

    // pass to `const std::string&` parameter
    printS(s);              // ok: inexpensive bind to std::string argument
    printS(sv);             // compile error: cannot implicit convert std::string_view to std::string
    printS(static_cast<std::string>(sv)); // bad: expensive creation of std::string temporary
    printS("Hello, world"); // bad: expensive creation of std::string temporary

    return 0;
}
此外，我们需要考虑在函数内部访问参数的成本。由于
std::string_view
参数是普通对象，因此可以直接访问正在查看的字符串。访问
std::string&
参数需要额外的步骤才能访问被引用对象，然后才能访问字符串。
最后，如果我们想传入现有字符串（任何类型）的子字符串，创建
std::string_view
子字符串的成本相对较低，然后可以廉价地将其传递给
std::string_view
参数。相比之下，将子字符串传递给
const std::string&
的成本更高，因为子字符串必须在某个时候复制到引用参数绑定的
std::string
中。
下一课
12.7
指针简介
返回目录
上一课
12.5
按左值引用传递