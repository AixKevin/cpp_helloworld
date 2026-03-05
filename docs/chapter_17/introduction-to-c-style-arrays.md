# 17.7 — C 风格数组简介

17.7 — C 风格数组简介
Alex
2007 年 6 月 27 日，太平洋夏令时下午 5:20
2024 年 10 月 13 日
既然我们已经介绍了
std::vector
和
std::array
，我们将通过介绍最后一种数组类型：C 风格数组来完成对数组的介绍。
正如第
16.1 课 -- 容器和数组简介
中提到的，C 风格数组继承自 C 语言，并且内置于 C++ 的核心语言中（与其余数组类型不同，它们是标准库容器类）。这意味着我们不需要 #include 头文件即可使用它们。
题外话…
因为它们是语言原生支持的唯一数组类型，所以标准库数组容器类型（例如
std::array
和
std::vector
）通常使用 C 风格数组实现。
声明 C 风格数组
因为它们是核心语言的一部分，所以 C 风格数组有其特殊的声明语法。在 C 风格数组声明中，我们使用方括号 (
[]
) 来告诉编译器声明的对象是一个 C 风格数组。在方括号内，我们可以选择提供数组的长度，它是一个
std::size_t
类型的整型值，告诉编译器数组中有多少个元素。
以下定义创建一个名为
testScore
的 C 风格数组变量，其中包含 30 个
int
类型的元素
int main()
{
    int testScore[30] {};      // Defines a C-style array named testScore that contains 30 value-initialized int elements (no include required)

//  std::array<int, 30> arr{}; // For comparison, here's a std::array of 30 value-initialized int elements (requires #including <array>)

    return 0;
}
C 风格数组的长度必须至少为 1。如果数组长度为零、负数或非整型值，编译器将报错。
致进阶读者
动态分配在堆上的 C 风格数组允许长度为 0。
C 风格数组的数组长度必须是常量表达式
就像
std::array
一样，在声明 C 风格数组时，数组的长度必须是常量表达式（
std::size_t
类型，尽管这通常不重要）。
提示
一些编译器可能允许创建具有非 constexpr 长度的数组，以兼容 C99 的可变长度数组 (VLA) 功能。
可变长度数组在 C++ 中是无效的，不应在 C++ 程序中使用。如果您的编译器允许这些数组，您可能忘记禁用编译器扩展（请参阅
0.10 -- 配置您的编译器：编译器扩展
）。
C 风格数组的下标访问
与
std::array
一样，C 风格数组可以使用下标运算符 (
operator[]
) 进行索引
#include <iostream>

int main()
{
    int arr[5]; // define an array of 5 int values

    arr[1] = 7; // use subscript operator to index array element 1
    std::cout << arr[1]; // prints 7

    return 0;
}
与标准库容器类（只使用
std::size_t
类型的无符号索引）不同，C 风格数组的索引可以是任何整型类型（有符号或无符号）的值或非作用域枚举。这意味着 C 风格数组不受标准库容器类所有符号转换索引问题的影响！
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };

    int s { 2 };
    std::cout << arr[s] << '\n'; // okay to use signed index

    unsigned int u { 2 };
    std::cout << arr[u] << '\n'; // okay to use unsigned index

    return 0;
}
提示
C 风格数组将接受有符号或无符号索引（或非作用域枚举）。
operator[]
不执行任何边界检查，传入越界索引将导致未定义行为。
题外话…
在声明数组（例如
int arr[5]
）时，使用
[]
是声明语法的一部分，而不是下标运算符
operator[]
的调用。
C 风格数组的聚合初始化
与
std::array
一样，C 风格数组是聚合体，这意味着它们可以使用聚合初始化进行初始化。
简单回顾一下，聚合初始化允许我们直接初始化聚合体的成员。为此，我们提供一个初始化列表，它是一个用花括号括起来的逗号分隔的初始化值列表。
int main()
{
    int fibonnaci[6] = { 0, 1, 1, 2, 3, 5 }; // copy-list initialization using braced list
    int prime[5] { 2, 3, 5, 7, 11 };         // list initialization using braced list (preferred)

    return 0;
}
这些初始化形式都按顺序初始化数组成员，从元素 0 开始。
如果您不为 C 风格数组提供初始化器，元素将默认初始化。在大多数情况下，这将导致元素未初始化。因为我们通常希望元素被初始化，所以当定义时没有初始化器时，C 风格数组应该进行值初始化（使用空花括号）。
int main()
{
    int arr1[5];    // Members default initialized int elements are left uninitialized)
    int arr2[5] {}; // Members value initialized (int elements are zero uninitialized) (preferred)

    return 0;
}
如果在初始化列表中提供的初始化器多于定义的数组长度，编译器将报错。如果在初始化列表中提供的初始化器少于定义的数组长度，其余没有初始化器的元素将进行值初始化
int main()
{
    int a[4] { 1, 2, 3, 4, 5 }; // compile error: too many initializers
    int b[4] { 1, 2 };          // arr[2] and arr[3] are value initialized

    return 0;
}
使用 C 风格数组的一个缺点是必须显式指定元素的类型。CTAD 不起作用，因为 C 风格数组不是类模板。而且使用
auto
尝试从初始化器列表中推断数组的元素类型也行不通
int main()
{
    auto squares[5] { 1, 4, 9, 16, 25 }; // compile error: can't use type deduction on C-style arrays

    return 0;
}
省略长度
以下数组定义中存在一个微妙的冗余。看到了吗？
int main()
{
    const int prime[5] { 2, 3, 5, 7, 11 }; // prime has length 5

    return 0;
}
我们显式地告诉编译器数组长度为 5，然后我们还用 5 个元素对其进行初始化。当我们使用初始化列表初始化 C 风格数组时，我们可以省略长度（在数组定义中），让编译器从初始化器的数量推断数组的长度。
以下数组定义行为相同
int main()
{
    const int prime1[5] { 2, 3, 5, 7, 11 }; // prime1 explicitly defined to have length 5
    const int prime2[] { 2, 3, 5, 7, 11 };  // prime2 deduced by compiler to have length 5

    return 0;
}
这仅在为所有数组成员显式提供初始化器时才有效。
int main()
{
    int bad[] {}; // error: the compiler will deduce this to be a zero-length array, which is disallowed!

    return 0;
}
当使用初始化列表初始化 C 风格数组的所有元素时，最好省略长度，让编译器计算数组的长度。这样，如果添加或删除初始化器，数组的长度将自动调整，并且我们不会面临定义的数组长度与提供的初始化器数量不匹配的风险。
最佳实践
当明确地用一个值初始化每个数组元素时，最好省略 C 风格数组的长度。
const 和 constexpr C 风格数组
与
std::array
一样，C 风格数组可以是
const
或
constexpr
。就像其他 const 变量一样，const 数组必须初始化，并且之后元素的值不能更改。
#include <iostream>

namespace ProgramData
{
    constexpr int squares[5] { 1, 4, 9, 16, 25 }; // an array of constexpr int
}

int main()
{
    const int prime[5] { 2, 3, 5, 7, 11 }; // an array of const int
    prime[0] = 17; // compile error: can't change const int

    return 0;
}
C 风格数组的 sizeof
在前面的课程中，我们使用
sizeof()
运算符获取对象或类型以字节为单位的大小。应用于 C 风格数组，
sizeof()
返回整个数组使用的字节数
#include <iostream>

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 }; // the compiler will deduce prime to have length 5
    
    std::cout << sizeof(prime); // prints 20 (assuming 4 byte ints)

    return 0;
}
假设 int 占 4 字节，以上程序将打印
20
。
prime
数组包含 5 个
int
元素，每个 4 字节，所以 5 * 4 = 20 字节。
请注意，这里没有开销。C 风格数组对象只包含其元素，别无他物。
获取 C 风格数组的长度
在 C++17 中，我们可以使用
std::size()
（定义在
头文件中），它将数组长度作为无符号整型值（
std::size_t
类型）返回。在 C++20 中，我们还可以使用
std::ssize()
，它将数组长度作为有符号整型值（一种大的有符号整型，可能是
std::ptrdiff_t
）返回。
#include <iostream>
#include <iterator> // for std::size and std::ssize

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };   // the compiler will deduce prime to have length 5

    std::cout << std::size(prime) << '\n';  // C++17, returns unsigned integral value 5
    std::cout << std::ssize(prime) << '\n'; // C++20, returns signed integral value 5

    return 0;
}
提示
std::size()
和
std::ssize()
定义的规范头文件是
。然而，由于这些函数非常有用，许多其他头文件也提供了它们，包括
和
。当在 C 风格数组上使用
std::size()
或
std::ssize()
时，我们可能尚未包含其他任何头文件。在这种情况下，
头文件是通常包含的。
您可以在
cppreference size 函数文档
中查看定义这些函数的所有头文件列表。
获取 C 风格数组的长度（C++14 或更早版本）
在 C++17 之前，没有标准库函数来获取 C 风格数组的长度。
如果您使用的是 C++11 或 C++14，您可以使用此函数代替
#include <cstddef> // for std::size_t
#include <iostream>

template <typename T, std::size_t N>
constexpr std::size_t length(const T(&)[N]) noexcept
{
	return N;
}

int main() {

	int array[]{ 1, 1, 2, 3, 5, 8, 13, 21 };
	std::cout << "The array has: " << length(array) << " elements\n";

	return 0;
}
这使用了一个函数模板，它通过引用接收一个 C 风格数组，然后返回表示数组长度的非类型模板参数。
在更旧的代码库中，您可能会看到通过将整个数组的大小除以数组元素的大小来确定 C 风格数组的长度
#include <iostream>

int main()
{
    int array[8] {};
    std::cout << "The array has: " << sizeof(array) / sizeof(array[0]) << " elements\n";

    return 0;
}
这会打印
The array has: 8 elements
这是如何工作的？首先，请注意整个数组的大小等于数组长度乘以元素大小。更简洁地说：
数组大小 = 长度 * 元素大小
。
通过代数，我们可以重新排列这个等式：
长度 = 数组大小 / 元素大小
。我们通常使用
sizeof(array[0])
作为元素大小。因此，长度 =
sizeof(array) / sizeof(array[0])
。您偶尔也会看到它写成
sizeof(array) / sizeof(*array)
，这具有相同的效果。
然而，正如我们将在下一课中向您展示的那样，这个公式很容易失败（当传递一个退化数组时），导致程序意外崩溃。C++17 的
std::size()
和上面所示的
length()
函数模板在这种情况下都会导致编译错误，因此它们是安全的。
相关内容
我们将在下一课
17.8 -- C 风格数组退化
中介绍数组退化。
C 风格数组不支持赋值
也许令人惊讶的是，C++ 数组不支持赋值
int main()
{
    int arr[] { 1, 2, 3 }; // okay: initialization is fine
    arr[0] = 4;            // assignment to individual elements is fine
    arr = { 5, 6, 7 };     // compile error: array assignment not valid

    return 0;
}
从技术上讲，这不起作用，因为赋值要求左操作数是一个可修改的左值，而 C 风格数组不被认为是可修改的左值。
如果您需要将新的值列表赋值给 C 风格数组，最好改用
std::vector
。或者，您可以逐个元素地为 C 风格数组赋值，或者使用
std::copy
复制现有 C 风格数组
#include <algorithm> // for std::copy

int main()
{
    int arr[] { 1, 2, 3 };
    int src[] { 5, 6, 7 };

    // Copy src into arr
    std::copy(std::begin(src), std::end(src), std::begin(arr));

    return 0;
}
小测验时间
问题 #1
将以下
std::array
定义转换为等效的 constexpr C 风格数组定义
constexpr std::array<int, 3> a{}; // allocate 3 ints
显示答案
constexpr int a[3] {}; // allocate 3 ints
问题 #2
以下程序有什么三个错误？
#include <iostream>

int main()
{
    int length{ 5 };
    const int arr[length] { 9, 7, 5, 3, 1 };
    
    std::cout << arr[length];
    arr[0] = 4;
    
    return 0;
}
显示答案
定义数组时，长度必须是编译时常量。在上面的程序中，
length
是非 const 的，所以不允许定义
const int arr[length]
。
数组的索引范围是 0 到 length-1。因此，
arr[length]
是一个越界索引，将导致未定义行为。
数组元素的类型是“const int”，因此
arr[0]
不能通过赋值修改。
问题 #3
“完全平方数”是其平方根为整数的自然数。我们可以通过将一个自然数（包括零）乘以自身来得到完全平方数。前 4 个完全平方数是：0、1、4、9。
使用全局 constexpr C 风格数组来保存 0 到 9（包括 9）之间的完全平方数。反复要求用户输入一位整数，或输入 -1 退出。打印用户输入的数字是否是完全平方数。
输出应与以下内容匹配
Enter a single digit integer, or -1 to quit: 4
4 is a perfect square

Enter a single digit integer, or -1 to quit: 5
5 is not a perfect square

Enter a single digit integer, or -1 to quit: -1
Bye
提示：使用基于范围的 for 循环遍历 C 风格数组以查找匹配项。
显示答案
#include <iostream>

namespace ProgramData
{
    constexpr int squares[] { 0, 1, 4, 9 };
}

bool matchSquare(int input)
{
    for (const auto& e : ProgramData::squares)
    {
        if (input == e)
            return true;
    }

    return false;
}

int main()
{
    while (true)
    {
        std::cout << "Enter a single digit integer, or -1 to quit: ";
        int input{};
        std::cin >> input;

        if (input == -1)
            break;

        if (matchSquare(input))
            std::cout << input << " is a perfect square\n";
        else
            std::cout << input << " is not a perfect square\n";
    }

    std::cout << "Bye\n";

    return 0;
}
下一课
17.8
C 风格数组退化
返回目录
上一课
17.6
std::array 和枚举