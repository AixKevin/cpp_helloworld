# 16.3 — std::vector 和无符号长度及下标问题

16.3 — std::vector 和无符号长度及下标问题
Alex
2023 年 9 月 11 日下午 2:28 PDT
2024 年 11 月 11 日
在上一课
16.2 -- std::vector 和列表构造函数简介
中，我们介绍了
operator[]
，它可以用于下标数组以访问元素。
在本课中，我们将探讨访问数组元素的其他方法，以及获取容器类长度（容器类中当前元素的数量）的几种不同方法。
但在此之前，我们需要讨论 C++ 设计者犯的一个重大错误，以及它如何影响 C++ 标准库中的所有容器类。
容器长度符号问题
我们先提出一个论断：用于数组下标的数据类型应与用于存储数组长度的数据类型匹配。这样才能索引到最长数组中的所有元素，不多不少。
正如 Bjarne Stroustrup
回忆
的那样，当 C++ 标准库中的容器类设计时（大约 1997 年），设计者必须选择是将长度（和数组下标）设置为有符号还是无符号。他们选择将其设置为无符号。
给出这样选择的原因是：标准库数组类型的下标不能为负数；使用无符号类型允许数组拥有更大的长度，因为它多了一个位（这在 16 位时代很重要）；以及范围检查下标只需要一次条件检查，而不是两次（因为不需要检查索引是否小于 0）。
回想起来，这通常被认为是错误的选择。我们现在明白，由于隐式转换规则，使用无符号值来强制非负性不起作用（因为负的有符号整数只会隐式转换为大的无符号整数，产生垃圾结果），在 32 位或 64 位系统上通常不需要额外的位范围（因为您可能不会创建超过 20 亿个元素的数组），并且常用的
operator[]
无论如何也不进行范围检查。
在课程
4.5 -- 无符号整数以及为何避免使用它们
中，我们讨论了为什么我们更喜欢使用有符号值来保存数量。我们还注意到，混合使用有符号和无符号值是导致意外行为的原因。因此，标准库容器类使用无符号值作为长度（和索引）是存在问题的，因为它使得在使用这些类型时无法避免使用无符号值。
目前，我们不得不接受这个选择以及它所带来的不必要的复杂性。
回顾：符号转换是窄化转换，除了 constexpr
在继续之前，我们快速回顾一下课程
10.4 -- 窄化转换、列表初始化和 constexpr 初始化器
中关于符号转换（从有符号到无符号或反之的整型转换）的一些内容，因为我们将在本章中大量讨论这些内容。
符号转换被认为是窄化转换，因为有符号或无符号类型无法容纳对立类型范围内的所有值。当这种转换在运行时执行时，编译器将在不允许窄化转换的上下文中（例如在列表初始化中）发出错误，并且在执行这种转换的其他上下文中，可能会或可能不会发出警告。
例如
#include <iostream>

void foo(unsigned int)
{
}

int main()
{
    int s { 5 };
    
    [[maybe_unused]] unsigned int u { s }; // compile error: list initialization disallows narrowing conversion
    foo(s);                                // possible warning: copy initialization allows narrowing conversion

    return 0;
}
在上面的示例中，变量
u
的初始化导致编译错误，因为在列表初始化时不允许窄化转换。对
foo()
的调用执行了拷贝初始化，它允许窄化转换，并且可能会或可能不会生成警告，具体取决于编译器在生成符号转换警告方面的激进程度。例如，当使用编译器标志
-Wsign-conversion
时，GCC 和 Clang 都会在这种情况下生成警告。
但是，如果要进行符号转换的值是 constexpr 并且可以转换为对立类型中的等效值，则该符号转换
不
被认为是窄化转换。这是因为编译器可以保证转换是安全的，或者终止编译过程。
#include <iostream>

void foo(unsigned int)
{
}

int main()
{
    constexpr int s { 5 };                 // now constexpr
    [[maybe_unused]] unsigned int u { s }; // ok: s is constexpr and can be converted safely, not a narrowing conversion
    foo(s);                                // ok: s is constexpr and can be converted safely, not a narrowing conversion

    return 0;
}
在这种情况下，由于
s
是 constexpr 且要转换的值 (
5
) 可以表示为无符号值，因此转换不被视为窄化转换，可以隐式执行而不会出现问题。
这种非窄化 constexpr 转换（从
constexpr int
到
constexpr std::size_t
）将是我们大量使用的内容。
std::vector
的长度和索引的类型为
size_type
在课程
10.7 -- 类型定义和类型别名
中，我们提到 typedef 和类型别名通常用于需要为可能变化的类型（例如，因为它是由实现定义的）命名的情况。例如
std::size_t
是某种大型无符号整型（通常是
unsigned long
或
unsigned long long
）的 typedef。
每个标准库容器类都定义了一个名为
size_type
的嵌套 typedef 成员（有时写为
T::size_type
），它是用于容器长度（以及索引，如果支持）的类型的别名。
您通常会在文档和编译器警告/错误消息中看到
size_type
。例如，
std::vector
的
size()
成员函数的此文档
表明
size()
返回
size_type
类型的值。
相关内容
我们将在课程
15.3 -- 嵌套类型（成员类型）
中介绍嵌套 typedef。
size_type
几乎总是
std::size_t
的别名，但（在极少数情况下）可以被覆盖以使用不同的类型。
关键见解
size_type
是标准库容器类中定义的嵌套 typedef，用作容器类长度（如果支持，也包括索引）的类型。
size_type
默认为
std::size_t
，由于这几乎从不更改，我们可以合理地假设
size_type
是
std::size_t
的别名。
致进阶读者
除
std::array
之外的所有标准库容器都使用
std::allocator
来分配内存。对于这些容器，
T::size_type
派生自所用分配器的
size_type
。由于
std::allocator
最多可以分配
std::size_t
字节的内存，因此
std::allocator
::size_type
定义为
std::size_t
。因此，
T::size_type
默认为
std::size_t
。
只有当自定义分配器的
T::size_type
被定义为非
std::size_t
的类型时，容器的
T::size_type
才会不同于
std::size_t
。这种情况很少见，而且是根据每个应用程序进行的，因此通常可以安全地假设
T::size_type
将是
std::size_t
，除非您的应用程序正在使用此类自定义分配器（并且您会知道这种情况）。
当访问容器类的
size_type
成员时，我们必须使用容器类的完整模板化名称来限定它的作用域。例如，
std::vector
::size_type
。
使用
size()
成员函数或
std::size()
获取
std::vector
的长度
我们可以使用
size()
成员函数（它返回无符号
size_type
类型的长度）来询问容器类对象的长度
#include <iostream>
#include <vector>

int main()
{
    std::vector prime { 2, 3, 5, 7, 11 };
    std::cout << "length: " << prime.size() << '\n'; // returns length as type `size_type` (alias for `std::size_t`)
    return 0;
}
这会打印
length: 5
与
std::string
和
std::string_view
不同，它们都有
length()
和
size()
成员函数（功能相同），
std::vector
（和 C++ 中的大多数其他容器类型）只有
size()
。现在您明白了为什么容器的长度有时被模糊地称为其“大小”。
在 C++17 中，我们还可以使用
std::size()
非成员函数（对于容器类，它只是调用
size()
成员函数）。
#include <iostream>
#include <vector>

int main()
{
    std::vector prime { 2, 3, 5, 7, 11 };
    std::cout << "length: " << std::size(prime); // C++17, returns length as type `size_type` (alias for `std::size_t`)

    return 0;
}
致进阶读者
因为
std::size()
也可以用于未衰退的 C 风格数组，所以这种方法有时比使用
size()
成员函数更受欢迎（特别是在编写函数模板时，可以接受容器类或未衰退的 C 风格数组参数）。
我们在课程
17.8 -- C 风格数组衰退
中讨论 C 风格数组衰退。
如果我们要使用上述任何一种方法将长度存储在有符号类型的变量中，这可能会导致有符号/无符号转换警告或错误。最简单的做法是将其结果静态转换为所需类型
#include <iostream>
#include <vector>

int main()
{
    std::vector prime { 2, 3, 5, 7, 11 };
    int length { static_cast<int>(prime.size()) }; // static_cast return value to int
    std::cout << "length: " << length ;

    return 0;
}
使用
std::ssize()
获取
std::vector
的长度
C++20
C++20 引入了
std::ssize()
非成员函数，它将长度返回为大型
有符号
整型（通常是
std::ptrdiff_t
，这是通常用作
std::size_t
有符号对应类型的类型）
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };
    std::cout << "length: " << std::ssize(prime); // C++20, returns length as a large signed integral type

    return 0;
}
这是这三个函数中唯一一个返回有符号类型长度的函数。
如果您想使用此方法将长度存储在有符号类型的变量中，您有几个选择。
首先，因为
int
类型可能小于
std::ssize()
返回的有符号类型，如果您要将长度分配给
int
变量，您应该将结果
static_cast
为
int
以明确此类转换（否则您可能会收到窄化转换警告或错误）
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };
    int length { static_cast<int>(std::ssize(prime)) }; // static_cast return value to int
    std::cout << "length: " << length;

    return 0;
}
或者，您可以使用
auto
让编译器推断出变量要使用的正确有符号类型
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };
    auto length { std::ssize(prime) }; // use auto to deduce signed type, as returned by std::ssize()
    std::cout << "length: " << length;

    return 0;
}
使用
operator[]
访问数组元素不进行边界检查
在上一课中，我们介绍了下标运算符（
operator[]
）
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::cout << prime[3];  // print the value of element with index 3 (7)
    std::cout << prime[9]; // invalid index (undefined behavior)

    return 0;
}
operator[]
不进行边界检查。
operator[]
的索引可以是非 const。我们将在后面的部分进一步讨论这个问题。
使用
at()
成员函数访问数组元素会进行运行时边界检查
数组容器类支持另一种访问数组的方法。
at()
成员函数可以用于进行带有运行时边界检查的数组访问
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::cout << prime.at(3); // print the value of element with index 3
    std::cout << prime.at(9); // invalid index (throws exception)

    return 0;
}
在上面的示例中，对
prime.at(3)
的调用会检查以确保索引 3 是有效的，因为它有效，所以它返回对数组元素 3 的引用。然后我们可以打印这个值。然而，对
prime.at(9)
的调用失败了（在运行时），因为 9 不是此数组的有效索引。
at()
函数没有返回引用，而是生成一个错误，终止程序。
致进阶读者
当
at()
成员函数遇到越界索引时，它实际上会抛出
std::out_of_range
类型的异常。如果异常未处理，程序将被终止。我们在
第 27 章
中介绍异常以及如何处理它们。
与
operator[]
一样，传递给
at()
的索引可以是非 const。
因为它在每次调用时都进行运行时边界检查，所以
at()
比
operator[]
慢（但更安全）。尽管安全性较低，
operator[]
通常比
at()
更常用，主要是因为最好在索引之前进行边界检查，这样我们一开始就不会尝试使用无效索引。
用 constexpr 有符号整型索引
std::vector
当用 constexpr (有符号) int 索引
std::vector
时，我们可以让编译器将其隐式转换为
std::size_t
，而不会造成窄化转换
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::cout << prime[3] << '\n';     // okay: 3 converted from int to std::size_t, not a narrowing conversion
 
    constexpr int index { 3 };         // constexpr
    std::cout << prime[index] << '\n'; // okay: constexpr index implicitly converted to std::size_t, not a narrowing conversion
   
    return 0;
}
用非 constexpr 值索引
std::vector
用于数组索引的下标可以是非 const
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::size_t index { 3 };           // non-constexpr
    std::cout << prime[index] << '\n'; // operator[] expects an index of type std::size_t, no conversion required
   
    return 0;
}
然而，根据我们的最佳实践（
4.5 -- 无符号整数以及为何避免使用它们
），我们通常希望避免使用无符号类型来保存数量。
当我们的下标是非 constexpr 有符号值时，我们会遇到问题
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    int index { 3 };                   // non-constexpr
    std::cout << prime[index] << '\n'; // possible warning: index implicitly converted to std::size_t, narrowing conversion
   
    return 0;
}
在此示例中，
index
是一个非 constexpr 有符号整数。
std::vector
中定义的
operator[]
的下标类型为
size_type
（
std::size_t
的别名）。因此，当我们调用
prime[index]
时，我们的有符号整数必须转换为
std::size_t
。
这种转换不应该危险（因为
std::vector
的索引预期是非负的，并且非负的有符号值将安全地转换为无符号值）。但是当在运行时执行时，这被认为是窄化转换，您的编译器应该会发出关于此不安全转换的警告（如果它没有，您应该考虑修改您的警告设置，使其能够发出）。
由于数组下标很常见，并且每次这样的转换都会生成警告，这很容易用虚假警告淹没您的编译日志。或者，如果您启用了“将警告视为错误”，它将停止您的编译。
有许多可能的方法可以避免这个问题（例如，每次索引数组时将您的
int
static_cast
到
std::size_t
），但所有方法都不可避免地以某种方式使您的代码混乱或复杂。在这种情况下最简单的做法是使用
std::size_t
类型的变量作为您的索引，并且除了索引之外不要将此变量用于任何其他目的。这样，您一开始就可以避免任何非 constexpr 转换。
提示
另一个不错的替代方法是，不直接索引
std::vector
，而是索引
data()
成员函数的结果
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    int index { 3 };                          // non-constexpr signed value
    std::cout << prime.data()[index] << '\n'; // okay: no sign conversion warnings
   
    return 0;
}
在底层，
std::vector
将其元素存储在 C 风格数组中。
data()
成员函数返回指向此底层 C 风格数组的指针，然后我们可以对其进行索引。由于 C 风格数组允许使用有符号和无符号类型进行索引，因此我们不会遇到任何符号转换问题。我们将在课程
17.7 -- C 风格数组简介
和
17.8 -- C 风格数组衰退
中进一步讨论 C 风格数组。
作者注
我们将在课程
16.7 -- 数组、循环和符号挑战解决方案
中讨论解决此类索引挑战的其他选项。
小测验时间
问题 #1
使用以下值初始化
std::vector
：'h'、'e'、'l'、'l'、'o'。然后打印数组的长度（使用
std::size()
）。最后，使用下标运算符和
at()
成员函数打印索引为 1 的元素的值。
程序应输出以下内容
The array has 5 elements.
ee
显示答案
#include <iostream>
#include <vector>

int main()
{
    std::vector arr { 'h', 'e', 'l', 'l', 'o' };
    std::cout << "The array has " << std::size(arr) << " elements.\n";
    std::cout << arr[1] << arr.at(1) << '\n';

    return 0;
}
问题 #2
a) 什么是
size_type
，它的用途是什么？
显示答案
size_type
是一个嵌套的 typedef，它是用于存储标准库容器的长度（如果支持，也包括索引）的类型的别名。
b)
size_type
默认是什么类型？它是有符号还是无符号？
显示答案
std::size_t
，它是一个无符号类型。
c) 获取容器长度的哪些函数返回
size_type
？
显示答案
size()
成员函数和
std::size
都返回
size_type
。
下一课
16.4
传递 std::vector
返回目录
上一课
16.2
std::vector 和列表构造函数简介