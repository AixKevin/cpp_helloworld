# 17.2 — std::array 的长度和索引

17.2 — std::array 的长度和索引
Alex
2023年9月11日，下午3:32 PDT
2024年8月15日
在课程
16.3 -- std::vector 和无符号长度及下标问题
中，我们讨论了标准库容器类使用无符号值表示长度和索引的糟糕决定。因为
std::array
是一个标准库容器类，它也存在同样的问题。
在本课中，我们将回顾索引和获取
std::array
长度的方法。由于
std::vector
和
std::array
具有相似的接口，这将与我们对
std::vector
的讲解并行。但是由于只有
std::array
完全支持 constexpr，我们将更多地关注这一点。
在继续之前，现在是时候回顾一下“有符号转换是缩小转换，除非是 constexpr”了（请参阅
16.3 -- std::vector 和无符号长度及下标问题
）。
std::array
的长度类型为
std::size_t
std::array
的实现是一个模板结构体，其声明如下：
template<typename T, std::size_t N> // N is a non-type template parameter
struct array;
如您所见，表示数组长度的非类型模板参数（
N
）的类型是
std::size_t
。而您现在可能已经知道，
std::size_t
是一个大型无符号整型。
相关内容
我们在课程
13.13 -- 类模板
中介绍了类模板（包括结构体模板），在课程
11.9 -- 非类型模板参数
中介绍了非类型模板参数。
因此，当我们定义一个
std::array
时，长度非类型模板实参的类型必须是
std::size_t
，或者可以转换为
std::size_t
类型的值。因为这个值必须是 constexpr，所以当我们使用有符号整型值时，我们不会遇到符号转换问题，因为编译器会很乐意在编译时将有符号整型值转换为
std::size_t
，而不会将其视为缩小转换。
题外话…
在 C++23 之前，C++ 甚至没有
std::size_t
的字面量后缀，因为从
int
到
std::size_t
的隐式编译时转换通常足以满足我们需要 constexpr
std::size_t
的情况。
添加后缀主要是为了类型推导的目的，因为
constexpr auto x { 0 }
会给你一个
int
而不是
std::size_t
。在这种情况下，能够区分
0
(
int
) 和
0UZ
(
std::size_t
) 而无需使用显式
static_cast
是很有用的。
std::array
的长度和索引的类型为
size_type
，它总是
std::size_t
就像
std::vector
一样，
std::array
定义了一个名为
size_type
的嵌套 typedef 成员，它是容器长度（和索引，如果支持）所用类型的别名。在
std::array
的情况下，
size_type
总是
std::size_t
的别名。
请注意，定义
std::array
长度的非类型模板参数被显式定义为
std::size_t
而不是
size_type
。这是因为
size_type
是
std::array
的成员，并且在该点尚未定义。这是唯一明确使用
std::size_t
的地方——其他所有地方都使用
size_type
。
获取
std::array
的长度
获取
std::array
对象的长度有三种常用方法。
首先，我们可以使用
size()
成员函数（它返回长度作为无符号
size_type
）向
std::array
对象查询其长度。
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 9.0, 7.2, 5.4, 3.6, 1.8 };
    std::cout << "length: " << arr.size() << '\n'; // returns length as type `size_type` (alias for `std::size_t`)
    return 0;
}
这会打印
length: 5
与
std::string
和
std::string_view
不同，它们既有
length()
成员函数又有
size()
成员函数（执行相同的操作），
std::array
（和 C++ 中的大多数其他容器类型）只有
size()
。
其次，在 C++17 中，我们可以使用
std::size()
非成员函数（对于
std::array
，它只是调用
size()
成员函数，因此将长度作为无符号
size_type
返回）。
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr{ 9, 7, 5, 3, 1 };
    std::cout << "length: " << std::size(arr); // C++17, returns length as type `size_type` (alias for `std::size_t`)

    return 0;
}
最后，在 C++20 中，我们可以使用
std::ssize()
非成员函数，它将长度作为大型
有符号
整型（通常是
std::ptrdiff_t
）返回。
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 9, 7, 5, 3, 1 };
    std::cout << "length: " << std::ssize(arr); // C++20, returns length as a large signed integral type

    return 0;
}
这是这三个函数中唯一一个将长度作为有符号类型返回的函数。
将
std::array
的长度作为 constexpr 值获取
由于
std::array
的长度是 constexpr，上述每个函数都将
std::array
的长度作为 constexpr 值返回（即使在非 constexpr
std::array
对象上调用也是如此）！这意味着我们可以在常量表达式中使用这些函数中的任何一个，并且返回的长度可以隐式转换为
int
而不会导致缩小转换。
#include <array>
#include <iostream>

int main()
{
    std::array arr { 9, 7, 5, 3, 1 }; // note: not constexpr for this example
    constexpr int length{ std::size(arr) }; // ok: return value is constexpr std::size_t and can be converted to int, not a narrowing conversion

    std::cout << "length: " << length << '\n';

    return 0;
}
对于 Visual Studio 用户
Visual Studio 对上述示例错误地触发了警告 C4365。该问题已
报告给微软
。
警告
由于语言缺陷，当在通过（const）引用传递的
std::array
函数参数上调用时，上述函数将返回非 constexpr 值。
#include <array>
#include <iostream>

void printLength(const std::array<int, 5> &arr)
{
    constexpr int length{ std::size(arr) }; // compile error!
    std::cout << "length: " << length << '\n';
}

int main()
{
    std::array arr { 9, 7, 5, 3, 1 };
    constexpr int length{ std::size(arr) }; // works just fine
    std::cout << "length: " << length << '\n';

    printLength(arr);

    return 0;
}
此缺陷已在 C++23 中通过
P2280
解决。在撰写本文时，很少有编译器目前
支持
此功能。
一个解决方法是将
foo()
设为一个函数模板，其中数组长度是一个非类型模板参数。然后可以在函数内部使用此非类型模板参数。我们将在课程
17.3 -- 传递和返回 std::array
中进一步讨论这个问题。
template <auto Length>
void printLength(const std::array<int, Length> &arr)
{
    std::cout << "length: " << Length << '\n';
}
使用
operator[]
或
at()
成员函数对
std::array
进行下标操作
在上一课
17.1 -- std::array 简介
中，我们介绍了索引
std::array
最常用的方法是使用下标运算符（
operator[]
）。在这种情况下不进行边界检查，传入无效索引将导致未定义行为。
就像
std::vector
一样，
std::array
也有一个
at()
成员函数，它在运行时进行下标和边界检查。我们建议避免使用此函数，因为我们通常希望在索引之前进行边界检查，或者我们希望进行编译时边界检查。
这两个函数都期望索引的类型为
size_type
(
std::size_t
)。
如果其中任何一个函数是用 constexpr 值调用的，编译器将进行 constexpr 转换为
std::size_t
。这不被认为是缩小转换，所以你不会在这里遇到符号问题。
然而，如果这些函数中的任何一个用非 constexpr 有符号整型值调用，转换为
std::size_t
被认为是缩小转换，并且您的编译器可能会发出警告。我们在课程
16.3 -- std::vector 和无符号长度及下标问题
中进一步讨论这种情况（使用
std::vector
）。
std::get()
对 constexpr 索引进行编译时边界检查
由于
std::array
的长度是 constexpr，如果我们的索引也是一个 constexpr 值，那么编译器应该能够在编译时验证我们的 constexpr 索引是否在数组的边界内（如果 constexpr 索引超出边界则停止编译）。
然而，
operator[]
按定义不进行边界检查，而
at()
成员函数只进行运行时边界检查。并且函数参数不能是 constexpr（即使对于 constexpr 或 consteval 函数），那么我们如何传递 constexpr 索引呢？
为了在有 constexpr 索引时进行编译时边界检查，我们可以使用
std::get()
函数模板，它将索引作为非类型模板参数：
#include <array>
#include <iostream>

int main()
{
    constexpr std::array prime{ 2, 3, 5, 7, 11 };

    std::cout << std::get<3>(prime); // print the value of element with index 3
    std::cout << std::get<9>(prime); // invalid index (compile error)

    return 0;
}
在
std::get()
的实现内部，有一个
static_assert
检查以确保非类型模板参数小于数组长度。如果不是，则
static_assert
将停止编译过程并引发编译错误。
由于模板参数必须是 constexpr，因此
std::get()
只能与 constexpr 索引一起调用。
小测验时间
问题 #1
使用以下值初始化
std::array
：'h'、'e'、'l'、'l'、'o'。打印数组的长度，然后使用
operator[]
、
at()
和
std::get()
打印索引为 1 的元素的值。
程序应打印
The length is 5
eee
显示答案
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 'h', 'e', 'l', 'l', 'o' };
    std::cout << "The length is " << std::size(arr) << '\n';
    std::cout << arr[1] << arr.at(1) << std::get<1>(arr) << '\n';

    return 0;
}
下一课
17.3
传递和返回 std::array
返回目录
上一课
17.1
std::array 简介