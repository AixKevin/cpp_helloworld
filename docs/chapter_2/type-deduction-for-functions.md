# 10.9 — 函数的类型推导

10.9 — 函数的类型推导
Alex
2021年6月17日，太平洋夏令时下午5:42
2024年12月18日
考虑以下程序
int add(int x, int y)
{
    return x + y;
}
当这个函数被编译时，编译器会确定
x + y
的计算结果为
int
类型，然后确保返回值的类型与函数声明的返回类型匹配（或者返回值类型可以转换为声明的返回类型）。
使用
auto
进行返回类型推导
由于编译器已经需要从返回语句推导出返回类型（以确保该值可以转换为函数声明的返回类型），在C++14中，
auto
关键字被扩展以执行函数返回类型推导。这通过使用
auto
关键字代替函数的返回类型来实现。
例如
auto add(int x, int y)
{
    return x + y;
}
因为返回语句返回一个
int
值，编译器会推导出这个函数的返回类型是
int
。
当使用
auto
返回类型时，函数内的所有返回语句必须返回相同类型的值，否则会出错。例如：
auto someFcn(bool b)
{
    if (b)
        return 5; // return type int
    else
        return 6.7; // return type double
}
在上面的函数中，两个返回语句返回了不同类型的值，因此编译器会报错。
如果出于某种原因需要这种情况，你可以显式地为函数指定返回类型（在这种情况下，编译器会尝试将任何不匹配的返回表达式隐式转换为显式返回类型），或者你可以显式地将所有返回语句转换为相同的类型。在上面的例子中，后者可以通过将
5
更改为
5.0
来实现，但
static_cast
也可以用于非字面量类型。
返回类型推导的优点
返回类型推导的最大优点是，让编译器推导函数的返回类型可以消除返回类型不匹配的风险（防止意外的转换）。
当函数的返回类型是脆弱的（如果实现改变，返回类型很可能改变的情况）时，这尤其有用。在这种情况下，显式指定返回类型意味着当实现发生影响性改变时，必须更新所有相关的返回类型。如果幸运的话，编译器会在我们更新相关返回类型之前报错。如果不幸运，我们会在不希望的地方得到隐式转换。
在其他情况下，函数的返回类型可能很长很复杂，或者不那么明显。在这种情况下，可以使用
auto
来简化
// let compiler determine the return type of unsigned short + char
auto add(unsigned short x, char y)
{
    return x + y;
}
我们在课程
11.8 -- 具有多个模板类型的函数模板
中会更多地讨论这种情况（以及如何表达此类函数的实际返回类型）。
返回类型推导的缺点
返回类型推导主要有两个缺点
使用
auto
返回类型的函数必须在使用前完全定义（前向声明不足）。例如
#include <iostream>

auto foo();

int main()
{
    std::cout << foo() << '\n'; // the compiler has only seen a forward declaration at this point

    return 0;
}

auto foo()
{
    return 5;
}
在作者的机器上，这会产生以下编译错误：
error C3779: 'foo': a function that returns 'auto' cannot be used before it is defined.
这很有道理：前向声明没有足够的信息让编译器推导出函数的返回类型。这意味着返回
auto
的普通函数通常只能在它们被定义的文件内调用。
当使用对象类型推导时，初始化器总是作为同一语句的一部分存在，所以确定推导出的类型通常不会过于繁重。但函数类型推导并非如此——函数的原型没有指出函数实际返回什么类型。一个好的编程 IDE 应该清楚地显示函数推导出的类型，但如果没有这个功能，用户必须深入到函数体本身来确定函数返回的类型。犯错的可能性更高。一般来说，我们更倾向于显式地指定作为接口一部分的类型（函数的声明就是一个接口）。
与对象类型推导不同，关于函数返回类型推导的最佳实践并没有那么多共识。我们建议通常避免使用函数返回类型推导。
最佳实践
优先使用显式返回类型而不是返回类型推导（除非返回类型不重要、难以表达或脆弱）。
尾部返回类型语法
auto
关键字也可以用于使用
尾部返回类型语法
声明函数，其中返回类型在函数原型其余部分之后指定。
考虑以下函数
int add(int x, int y)
{
  return (x + y);
}
使用尾部返回类型语法，这可以等效地写成：
auto add(int x, int y) -> int
{
  return (x + y);
}
在这种情况下，
auto
不执行类型推导——它只是使用尾部返回类型语法的一部分。
为什么要使用它？有以下几个原因：
对于具有复杂返回类型的函数，尾部返回类型可以使函数更易于阅读
#include <type_traits> // for std::common_type

std::common_type_t<int, double> compare(int, double);         // harder to read (where is the name of the function in this mess?)
auto compare(int, double) -> std::common_type_t<int, double>; // easier to read (we don't have to read the return type unless we care)
尾部返回类型语法可以用于对齐函数的名称，这使得连续的函数声明更易于阅读
auto add(int x, int y) -> int;
auto divide(double x, double y) -> double;
auto printSomething() -> void;
auto generateSubstring(const std::string &s, int start, int len) -> std::string;
致进阶读者
如果一个函数的返回类型必须根据函数参数的类型推导，普通的返回类型将不足够，因为在那个时候编译器还没有看到参数。
#include <type_traits>
// note: decltype(x) evaluates to the type of x

std::common_type_t<decltype(x), decltype(y)> add(int x, double y);         // Compile error: compiler hasn't seen definitions of x and y yet
auto add(int x, double y) -> std::common_type_t<decltype(x), decltype(y)>; // ok
尾部返回语法对于C++的一些高级特性也是必需的，例如lambda（我们将在课程
20.6 -- lambda（匿名函数）介绍
中介绍）。
目前，我们建议继续使用传统的函数返回语法，除非情况需要使用尾部返回语法。
函数参数类型不能使用类型推导
许多学习类型推导的新程序员会尝试这样做：
#include <iostream>

void addAndPrint(auto x, auto y)
{
    std::cout << x + y << '\n';
}

int main()
{
    addAndPrint(2, 3); // case 1: call addAndPrint with int parameters
    addAndPrint(4.5, 6.7); // case 2: call addAndPrint with double parameters

    return 0;
}
不幸的是，类型推导不适用于函数参数，在C++20之前，上述程序不会编译（你会收到关于函数参数不能具有 auto 类型的错误）。
在C++20中，
auto
关键字被扩展，使得上述程序能够编译并正确运行——但是，在这种情况下
auto
并不是在调用类型推导。相反，它触发了一个名为
函数模板
的不同特性，该特性旨在实际处理此类情况。
相关内容
我们在课程
11.6 -- 函数模板
中介绍了函数模板，并在课程
11.8 -- 具有多个模板类型的函数模板
中讨论了在函数模板中使用
auto
。
下一课
10.x
第10章 总结和测验
返回目录
上一课
10.8
使用 auto 关键字进行对象的类型推导