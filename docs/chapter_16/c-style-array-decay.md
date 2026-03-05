# 17.8 — C 风格数组衰减

17.8 — C 风格数组衰减
Alex
2007 年 7 月 11 日下午 6:20 PDT
2025 年 1 月 17 日
C 风格数组传递的挑战
C 语言的设计者曾面临一个问题。考虑以下简单的程序：
#include <iostream>

void print(int val)
{
    std::cout << val;
}

int main()
{
    int x { 5 };
    print(x);

    return 0;
}
当调用
print(x)
时，参数
x
的值（
5
）被复制到形参
val
中。在函数体内，
val
的值（
5
）被打印到控制台。由于
x
复制成本很低，这里没有问题。
现在考虑以下类似的程序，它使用一个 1000 元素的 C 风格 int 数组，而不是单个 int：
#include <iostream>

void printElementZero(int arr[1000])
{
    std::cout << arr[0]; // print the value of the first element
}

int main()
{
    int x[1000] { 5 };   // define an array with 1000 elements, x[0] is initialized to 5
    printElementZero(x);

    return 0;
}
该程序也能编译，并向控制台打印预期值（
5
）。
虽然此示例中的代码与上一个示例中的代码相似，但其机制的工作方式可能与您预期有些不同（我们将在下面解释）。这归因于 C 语言设计者为解决两个主要挑战而提出的解决方案。
首先，每次函数调用都复制一个 1000 元素的数组成本很高（如果元素是复制成本很高的类型，则成本更高），所以我们想避免这种情况。但如何避免呢？C 没有引用，因此使用传引用来避免复制函数参数并非一个选项。
其次，我们希望能够编写一个函数，它能接受不同长度的数组参数。理想情况下，上面示例中的
printElementZero()
函数应该能够处理任何长度的数组参数（因为元素 0 保证存在）。我们不希望为每个可能用作参数的数组长度都编写一个不同的函数。但如何实现呢？C 没有指定“任何长度”数组的语法，也不支持模板，并且一种长度的数组不能转换为另一种长度的数组（大概是因为这样做会涉及昂贵的复制）。
C 语言的设计者想出了一个巧妙的解决方案（C++ 为了兼容性而继承了它），它解决了这两个问题：
#include <iostream>

void printElementZero(int arr[1000]) // doesn't make a copy
{
    std::cout << arr[0]; // print the value of the first element
}

int main()
{
    int x[7] { 5 };      // define an array with 7 elements
    printElementZero(x); // somehow works!

    return 0;
}
不知何故，上面的示例将一个 7 元素的数组传递给一个期望 1000 元素的函数，而没有进行任何复制。在本课中，我们将探讨其工作原理。
我们还将探讨 C 设计者选择的解决方案为何危险，以及为何不适合在现代 C++ 中使用。
但首先，我们需要涵盖两个子主题。
数组到指针的转换（数组衰减）
在大多数情况下，当 C 风格数组在表达式中使用时，数组将被隐式转换为指向元素类型的指针，并用第一个元素（索引为 0）的地址进行初始化。通俗地说，这称为
数组衰减
（或简称为
衰减
）。
您可以在以下程序中看到这一点：
#include <iomanip> // for std::boolalpha
#include <iostream>

int main()
{
    int arr[5]{ 9, 7, 5, 3, 1 }; // our array has elements of type int

    // First, let's prove that arr decays into an int* pointer

    auto ptr{ arr }; // evaluation causes arr to decay, type deduction should deduce type int*
    std::cout << std::boolalpha << (typeid(ptr) == typeid(int*)) << '\n'; // Prints true if the type of ptr is int*

    // Now let's prove that the pointer holds the address of the first element of the array

    std::cout << std::boolalpha << (&arr[0] == ptr) << '\n';

    return 0;
}
在作者的机器上，这打印出来
true
true
数组衰减成的指针没有什么特别之处。它是一个普通的指针，保存着第一个元素的地址。
同样，一个 const 数组（例如
const int arr[5]
）会衰减为指向 const 的指针（
const int*
）。
提示
在 C++ 中，在以下几种常见情况下，C 风格数组不会衰减：
当作为
sizeof()
或
typeid()
的参数时。
当使用
operator&
获取数组的地址时。
当作为类类型的成员传递时。
当通过引用传递时。
由于 C 风格数组在大多数情况下会衰减为指针，因此人们普遍错误地认为数组
就是
指针。事实并非如此。数组对象是一系列元素，而指针对象只是保存一个地址。
数组和衰减数组的类型信息是不同的。在上面的例子中，数组
arr
的类型是
int[5]
，而衰减数组的类型是
int*
。值得注意的是，数组类型
int[5]
包含长度信息，而衰减数组指针类型
int*
不包含。
关键见解
一个衰减的数组指针不知道它指向的数组有多长。“衰减”一词表示这种长度类型信息的丢失。
对 C 风格数组进行下标操作实际上是将
operator[]
应用于衰减的指针
因为 C 风格数组在求值时会衰减为指针，所以当 C 风格数组被下标时，下标操作实际上是在对衰减的数组指针进行操作。
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    std::cout << arr[2]; // subscript decayed array to get element 2, prints 5

    return 0;
}
我们也可以直接在指针上使用
operator[]
。如果该指针保存着第一个元素的地址，结果将是相同的：
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    
    const int* ptr{ arr };  // arr decays into a pointer
    std::cout << ptr[2];    // subscript ptr to get element 2, prints 5

    return 0;
}
我们将在稍后看到这在哪里很方便，并在下一课
17.9 -- 指针算术和下标
中更深入地探讨其工作原理（以及当指针保存的不是第一个元素的地址时会发生什么）。
数组衰减解决了我们的 C 风格数组传递问题
数组衰减解决了本课开头遇到的两个挑战。
当 C 风格数组作为参数传递时，数组会衰减为指针，并且持有数组第一个元素地址的指针会被传递给函数。所以，尽管看起来我们是通过值传递 C 风格数组，但我们实际上是通过地址传递！这就是避免复制 C 风格数组参数的方法。
关键见解
C 风格数组是按地址传递的，即使看起来是按值传递的。
现在考虑两个具有相同元素类型但长度不同的数组（例如
int[5]
和
int[7]
）。它们是不同的类型，彼此不兼容。然而，它们都会衰减为相同的指针类型（例如
int*
）。它们的衰减版本可以互换！从类型中删除长度信息允许我们传递不同长度的数组而不会出现类型不匹配。
关键见解
两个具有相同元素类型但不同长度的 C 风格数组会衰减为相同的指针类型。
在下面的示例中，我们将说明两件事：
我们可以将不同长度的数组传递给单个函数（因为两者都衰减为相同的指针类型）。
接收数组的函数参数可以是数组元素类型的（const）指针。
#include <iostream>

void printElementZero(const int* arr) // pass by const address
{
    std::cout << arr[0];
}

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };
    const int squares[] { 1, 4, 9, 25, 36, 49, 64, 81 };

    printElementZero(prime);   // prime decays to an const int* pointer
    printElementZero(squares); // squares decays to an const int* pointer

    return 0;
}
这个例子运行良好，并打印出：
2
1
在
main()
中，当我们调用
printElementZero(prime)
时，
prime
数组从
const int[5]
类型衰减为
const int*
类型，其中保存了
prime
的第一个元素的地址。同样，当我们调用
printElementZero(squares)
时，
squares
从
const int[8]
类型衰减为
const int*
类型，其中保存了
squares
的第一个元素的地址。这些
const int*
类型的指针就是实际作为参数传递给函数的值。
由于我们传递的是
const int*
类型的指针，因此我们的
printElementZero()
函数需要有一个相同指针类型 (
const int*
) 的参数。
在这个函数中，我们正在对指针进行下标操作以访问选定的数组元素。
因为 C 风格数组是按地址传递的，所以函数可以直接访问传入的数组（而不是副本）并修改其元素。因此，如果您的函数不打算修改数组元素，最好确保您的函数参数是 const。
C 风格数组函数参数语法
将函数参数声明为
int* arr
的一个问题是，不清楚
arr
应该是指向值数组的指针，而不是指向单个整数的指针。因此，在传递 C 风格数组时，最好使用备用声明形式
int arr[]
。
#include <iostream>

void printElementZero(const int arr[]) // treated the same as const int*
{
    std::cout << arr[0];
}

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };
    const int squares[] { 1, 4, 9, 25, 36, 49, 64, 81 };

    printElementZero(prime);  // prime decays to a pointer
    printElementZero(squares); // squares decays to a pointer

    return 0;
}
这个程序与前一个程序的行为完全相同，因为编译器会将函数参数
const int arr[]
解释为与
const int*
相同。然而，这样做的好处是向调用者表明
arr
预期是一个衰减的 C 风格数组，而不是指向单个值的指针。请注意，方括号之间不需要长度信息（反正也不使用）。如果提供了长度，它将被忽略。
最佳实践
期望 C 风格数组类型的函数参数应使用数组语法（例如
int arr[]
），而不是指针语法（例如
int *arr
）。
使用这种语法的缺点是，它使
arr
已经衰减变得不那么明显（而使用指针语法则非常清楚），因此您需要格外小心，不要做任何在衰减数组中无法按预期工作的事情（我们稍后将介绍其中一些）。
数组衰减的问题
尽管数组衰减是一个巧妙的解决方案，可以确保不同长度的 C 风格数组可以在不进行昂贵复制的情况下传递给函数，但数组长度信息的丢失使得容易出现多种类型的错误。
首先，
sizeof()
对数组和衰减数组返回不同的值
#include <iostream>

void printArraySize(int arr[])
{
    std::cout << sizeof(arr) << '\n'; // prints 4 (assuming 32-bit addresses)
}

int main()
{
    int arr[]{ 3, 2, 1 };

    std::cout << sizeof(arr) << '\n'; // prints 12 (assuming 4 byte ints)

    printArraySize(arr);

    return 0;
}
这意味着对 C 风格数组使用
sizeof()
可能是危险的，因为您必须确保只在可以访问实际数组对象时使用它，而不是衰减数组或指针。
在上一课 (
17.7 -- C 风格数组简介
) 中，我们提到
sizeof(arr)/sizeof(*arr)
历史上被用作获取 C 风格数组大小的技巧。这个技巧很危险，因为如果
arr
已经衰减，
sizeof(arr)
将返回指针的大小而不是数组的大小，从而产生错误的数组长度，可能导致程序故障。
幸运的是，C++17 中更好的替代品
std::size()
（以及 C++20 中的
std::ssize()
）在传入指针值时将无法编译：
#include <iostream>

int printArrayLength(int arr[])
{
    std::cout << std::size(arr) << '\n'; // compile error: std::size() won't work on a pointer
}

int main()
{
    int arr[]{ 3, 2, 1 };

    std::cout << std::size(arr) << '\n'; // prints 3

    printArrayLength(arr);

    return 0;
}
其次，或许最重要的是，数组衰减会使重构（将长函数分解为更短、更模块化的函数）变得困难。对于未衰减数组可以按预期工作的代码，在使用衰减数组时可能无法编译（或者更糟，可能默默地出现故障）。
第三，缺乏长度信息会带来几个编程挑战。如果没有长度信息，就难以对数组长度进行健全性检查。用户可以轻易传入比预期短的数组（甚至是指向单个值的指针），这将导致在使用无效索引进行下标操作时出现未定义行为。
#include <iostream>

void printElement2(int arr[])
{
    // How do we ensure that arr has at least three elements?
    std::cout << arr[2] << '\n';
}

int main()
{
    int a[]{ 3, 2, 1 };
    printElement2(a);  // ok

    int b[]{ 7, 6 };
    printElement2(b);  // compiles but produces undefined behavior

    int c{ 9 };
    printElement2(&c); // compiles but produces undefined behavior

    return 0;
}
没有数组长度也给遍历数组带来了挑战——我们怎么知道何时到达末尾？
这些问题有解决方案，但这些解决方案会增加程序的复杂性和脆弱性。
解决数组长度问题
历史上，程序员通过以下两种方法之一来解决缺少数组长度信息的问题。
首先，我们可以将数组和数组长度作为单独的参数传入：
#include <cassert>
#include <iostream>

void printElement2(const int arr[], int length)
{
    assert(length > 2 && "printElement2: Array too short"); // can't static_assert on length

    std::cout << arr[2] << '\n';
}

int main()
{
    constexpr int a[]{ 3, 2, 1 };
    printElement2(a, static_cast<int>(std::size(a)));  // ok

    constexpr int b[]{ 7, 6 };
    printElement2(b, static_cast<int>(std::size(b)));  // will trigger assert

    return 0;
}
然而，这仍然存在一些问题：
调用者需要确保数组和数组长度是成对的——如果传入错误的长度值，函数仍然会出错。
如果您使用
std::size()
或返回长度为
std::size_t
的函数，可能会出现符号转换问题。
运行时断言只在运行时遇到时才触发。如果我们的测试路径没有覆盖所有函数调用，那么向客户交付的程序存在风险，当客户执行我们未明确测试的操作时，程序将断言。在现代 C++ 中，我们希望使用
static_assert
对 constexpr 数组的数组长度进行编译时验证，但没有简单的方法可以做到这一点（因为函数参数不能是 constexpr，即使在 constexpr 或 consteval 函数中也是如此！）。
这种方法仅在我们进行显式函数调用时才有效。如果函数调用是隐式的（例如，我们正在使用数组作为操作数调用运算符），那么就没有机会传入长度。
其次，如果存在一个语义无效的元素值（例如，测试分数为
-1
），我们可以用该值的一个元素来标记数组的末尾。这样，可以通过计算数组开头和这个终止元素之间有多少个元素来计算数组的长度。数组也可以通过从开头迭代直到遇到终止元素来遍历。这种方法的好处是它甚至适用于隐式函数调用。
关键见解
C 风格字符串（即 C 风格数组）使用空终止符来标记字符串的结尾，以便即使它们已经衰减，也可以遍历它们。
但这种方法也有一些问题：
如果终止元素不存在，遍历将超出数组末尾，导致未定义行为。
遍历数组的函数需要对终止元素进行特殊处理（例如，C 风格字符串打印函数需要知道不要打印终止元素）。
实际数组长度和语义有效元素数量之间存在不匹配。如果使用错误的长度，语义无效的终止元素可能会被“处理”。
这种方法仅在存在语义无效值的情况下才有效，而这通常不是情况。
在大多数情况下应避免使用 C 风格数组
由于非标准的传递语义（使用按地址传递而不是按值传递）以及与衰减数组丢失长度信息相关的风险，C 风格数组已普遍失宠。我们建议尽可能避免使用它们。
最佳实践
在实际可行的情况下，避免使用 C 风格数组。
对于只读字符串（字符串字面量符号常量和字符串参数），首选
std::string_view
。
对于可修改的字符串，首选
std::string
。
对于非全局 constexpr 数组，首选
std::array
。
对于非 constexpr 数组，首选
std::vector
。
可以为全局 constexpr 数组使用 C 风格数组。我们稍后将讨论这一点。
题外话…
在 C++ 中，数组可以通过引用传递，在这种情况下，数组参数在传递给函数时不会衰减（但数组的引用在求值时仍然会衰减）。然而，很容易忘记始终如一地应用这一点，一个漏掉的引用将导致参数衰减。此外，数组引用参数必须具有固定长度，这意味着函数只能处理特定长度的数组。如果我们想要一个能够处理不同长度数组的函数，那么我们还必须使用函数模板。但是，如果您打算做这两件事来“修复” C 风格数组，那么您不妨直接使用
std::array
！
那么在现代 C++ 中，C 风格数组何时使用呢？
在现代 C++ 中，C 风格数组通常用于两种情况：
用于存储 constexpr 全局（或 constexpr 静态局部）程序数据。由于此类数组可以从程序中的任何位置直接访问，因此我们无需传递数组，从而避免了与衰减相关的问题。定义 C 风格数组的语法可能比
std::array
稍微不那么奇怪。更重要的是，索引此类数组没有像标准库容器类那样存在符号转换问题。
作为函数或类的参数，这些函数或类希望直接处理非 constexpr C 风格字符串参数（而不是要求转换为
std::string_view
）。这有两个可能的原因：首先，将非 constexpr C 风格字符串转换为
std::string_view
需要遍历 C 风格字符串以确定其长度。如果函数在性能关键的代码段中，并且不需要长度（例如，因为函数无论如何都会遍历字符串），那么避免转换可能很有用。其次，如果函数（或类）调用期望 C 风格字符串的其他函数，则转换为
std::string_view
只是为了转换回来可能不是最佳的（除非您有其他原因需要
std::string_view
）。
小测验时间
问题 #1
什么是数组衰减，它为什么是个问题？
显示答案
当 C 风格数组被求值时，在大多数情况下，它将被隐式转换为指向数组元素类型的指针。
衰减的数组会丢失其长度信息，这使得程序更容易出现与长度相关的错误。
问题 #2
C 风格字符串（即 C 风格数组）为什么使用空终止符？
显示答案
当 C 风格数组传递给函数时，它会衰减并丢失其长度信息。如果 C 风格字符串没有空终止符，函数将无法确定字符串的长度。
问题 #3
额外加分：为什么 C 风格字符串使用空终止符，而不是要求将衰减的 C 风格字符串和显式长度信息都传递给函数？
显示答案
这个问题可能有很多答案，但以下是一些：
人机工程学将很糟糕，因为我们到处都会有额外的参数和魔术数字（例如
printString("Hello", 5)
）。
字符串和提供的字符串长度很容易不匹配。字符串长度本质上是字符串本身的固有属性。依赖用户来维护这个属性将不可避免地导致错误（例如
printString("Hello", 6)
）。
额外加分 #2：即使 C++ 想实现传递显式长度信息，为什么它行不通？
显示提示
提示：考虑使用
std::cout
打印字符串的情况。
显示答案
同时传递 C 风格字符串和显式长度信息仅在显式调用函数时才可能。如果隐式调用函数，则无法传递长度信息。
考虑像
std::cout << cstr
这样的语句。二元
operator<<
只能接受两个操作数：
std::cout
和
cstr
。无法传递另一个代表长度信息的参数。空终止符方法没有这个问题。
下一课
17.9
指针算术和下标
返回目录
上一课
17.7
C 风格数组简介