# 1.4 — 变量赋值和初始化

1.4 — 变量赋值和初始化
Alex
2019 年 2 月 1 日，上午 9:49 PST
2025 年 3 月 6 日
在上一课（
1.3 -- 对象和变量简介
）中，我们介绍了如何定义一个可以用来存储值的变量。在本课中，我们将探讨如何将值实际放入变量中。
提醒一下，这是一个简短的程序，首先分配一个名为
x
的整数变量，然后分配另外两个名为
y
和
z
的整数变量
int main()
{
    int x;    // define an integer variable named x (preferred)
    int y, z; // define two integer variables, named y and z

    return 0;
}
提醒一下，最好每行定义一个变量。我们将在本课后面回到定义多个变量的情况。
变量赋值
变量定义后，您可以使用
=
运算符在单独的语句中为其赋值。这个过程称为
赋值
，
=
运算符称为
赋值运算符
。
int width; // define an integer variable named width
width = 5; // assignment of value 5 into variable width

// variable width now has value 5
默认情况下，赋值会将
= 运算符
右侧的值复制到运算符左侧的变量中。这称为
复制赋值
。
一旦变量被赋值，该变量的值就可以通过
std::cout
和
<<
运算符打印出来。
赋值可以在我们想要更改变量所持有的值时使用。这是一个我们使用赋值两次的示例
#include <iostream>

int main()
{
	int width; // define a variable named width
	width = 5; // copy assignment of value 5 into variable width

	std::cout << width; // prints 5

	width = 7; // change value stored in variable width to 7

	std::cout << width; // prints 7

	return 0;
}
这会打印
57
程序运行时，执行从
main
函数的顶部开始，并按顺序进行。首先，为变量
width
分配内存。然后我们将
width
赋值为
5
。当我们输出
width
的值时，它会向控制台打印
5
。当我们再将值
7
赋值给
width
时，任何先前的值（在此示例中为
5
）都将被覆盖。因此，当我们再次输出
width
时，这次它会打印
7
。
普通变量一次只能保存一个值。
警告
新程序员最常见的错误之一是混淆赋值运算符（
=
）和相等运算符（
==
）。赋值（
=
）用于为变量赋值。相等（
==
）用于测试两个操作数的值是否相等。
变量初始化
赋值的一个缺点是，为刚定义的对象赋值需要两条语句：一条用于定义变量，另一条用于赋值。
这两个步骤可以合并。定义对象时，您可以选择为对象提供一个初始值。为对象指定初始值的过程称为
初始化
，用于初始化对象的语法称为
初始化器
。非正式地，初始值也通常被称为“初始化器”。
例如，以下语句既定义了一个名为
width
（类型为
int
）的变量，并将其初始化为值
5
#include <iostream>

int main()
{
    int width { 5 };    // define variable width and initialize with initial value 5
    std::cout << width; // prints 5

    return 0;
}
在上述变量
width
的初始化中，
{ 5 }
是初始化器，
5
是初始值。
关键见解
初始化为变量提供一个初始值。想一想“初始-化”。
不同形式的初始化
与赋值（通常直截了当）不同，C++ 中的初始化非常复杂。因此，我们在这里提供一个简化的视图，以便入门。
C++ 中有 5 种常见的初始化形式
int a;         // default-initialization (no initializer)

// Traditional initialization forms:
int b = 5;     // copy-initialization (initial value after equals sign)
int c ( 6 );   // direct-initialization (initial value in parenthesis)

// Modern initialization forms (preferred):
int d { 7 };   // direct-list-initialization (initial value in braces)
int e {};      // value-initialization (empty braces)
您可能会看到上述形式以不同的间距书写（例如
int b=5;
int c(6);
、
int d{7};
、
int e{};
）。是否使用额外的空格以提高可读性是个人的偏好问题。
从 C++17 开始，复制初始化、直接初始化和直接列表初始化在大多数情况下行为相同。我们将在下面介绍它们最相关的区别情况。
相关内容
我们将在课程
14.15 -- 类初始化和复制消除
中介绍复制初始化、直接初始化和列表初始化之间的其余差异。
致进阶读者
其他初始化形式包括
聚合初始化（参见
13.8 -- 结构体聚合初始化
）。
复制列表初始化（下面讨论）。
引用初始化（参见
12.3 -- 左值引用
）。
静态初始化、常量初始化和动态初始化（参见
7.8 -- 为什么（非 const）全局变量是邪恶的
）。
零初始化（下面讨论）。
默认初始化
当没有提供初始化器时（例如上面的变量
a
），这称为
默认初始化
。在许多情况下，默认初始化不执行任何初始化，并使变量具有不确定值（一个不可预测的值，有时称为“垃圾值”）。
我们将在课程（
1.6 -- 未初始化变量和未定义行为
）中进一步讨论这种情况。
复制初始化
当等号后提供初始值时，这称为
复制初始化
。这种形式的初始化继承自 C 语言。
int width = 5; // copy-initialization of value 5 into variable width
就像复制赋值一样，它将等号右侧的值复制到左侧正在创建的变量中。在上面的代码片段中，变量
width
将被初始化为值
5
。
复制初始化在现代 C++ 中曾一度失宠，因为它对于某些复杂类型来说效率低于其他形式的初始化。然而，C++17 解决了这些问题的大部分，复制初始化现在正在获得新的倡导者。您也会在旧代码（尤其是从 C 移植的代码）或那些简单认为它看起来更自然且更易于阅读的开发人员中找到它。
致进阶读者
复制初始化也用于隐式复制值的情况，例如按值将参数传递给函数、按值从函数返回或按值捕获异常。
直接初始化
当括号内提供初始值时，这称为
直接初始化
。
int width ( 5 ); // direct initialization of value 5 into variable width
直接初始化最初是为了允许更有效地初始化复杂对象（具有类类型的对象，我们将在未来的章节中介绍）。就像复制初始化一样，直接初始化在现代 C++ 中也曾一度失宠，主要是因为它被直接列表初始化取代。然而，直接列表初始化也有一些自己的怪癖，因此直接初始化在某些情况下再次得到使用。
致进阶读者
当值被显式转换为另一种类型时（例如通过
static_cast
），也使用直接初始化。
列表初始化
在 C++ 中初始化对象的现代方式是使用一种利用花括号的初始化形式。这称为
列表初始化
（或
统一初始化
或
大括号初始化
）。
列表初始化有两种形式
int width { 5 };    // direct-list-initialization of initial value 5 into variable width (preferred)
int height = { 6 }; // copy-list-initialization of initial value 6 into variable height (rarely used)
在 C++11 之前，某些类型的初始化需要使用复制初始化，而其他类型的初始化需要使用直接初始化。复制初始化很难与复制赋值区分开来（因为两者都使用
=
）。直接初始化也可能难以与函数相关操作区分开来（因为两者都使用括号）。
引入列表初始化是为了提供一种几乎适用于所有情况、行为一致且具有明确语法的初始化语法，从而可以轻松判断我们何时正在初始化对象。
关键见解
当我们看到花括号时，我们知道我们正在列表初始化一个对象。
此外，列表初始化还提供了一种使用值列表而不是单个值初始化对象的方法（这就是它被称为“列表初始化”的原因）。我们将在课程
16.2 -- std::vector 和列表构造函数简介
中展示一个示例。
列表初始化禁止窄化转换
列表初始化对新的 C++ 程序员的主要好处之一是“窄化转换”是不允许的。这意味着如果您尝试使用变量无法安全保存的值列表初始化变量，编译器需要生成诊断（编译错误或警告）来通知您。例如
int main()
{
    // An integer can only hold non-fractional values.
    // Initializing an int with fractional value 4.5 requires the compiler to convert 4.5 to a value an int can hold.
    // Such a conversion is a narrowing conversion, since the fractional part of the value will be lost.

    int w1 { 4.5 }; // compile error: list-init does not allow narrowing conversion

    int w2 = 4.5;   // compiles: w2 copy-initialized to value 4
    int w3 (4.5);   // compiles: w3 direct-initialized to value 4

    return 0;
}
在上面程序的第 7 行，我们使用一个带有小数部分（
.5
）的值（
4.5
）来列表初始化一个整数变量（只能保存非小数部分的值）。由于这是一个窄化转换，因此在这种情况下，编译器需要生成诊断。
复制初始化（第 9 行）和直接初始化（第 10 行）都默默地丢弃
.5
并用值
4
初始化变量（这可能不是我们想要的）。您的编译器可能会警告您这一点（因为数据丢失很少是期望的），但它也可能不会。
请注意，这种对窄化转换的限制仅适用于列表初始化，不适用于对变量的任何后续赋值
int main()
{
    int w1 { 4.5 }; // compile error: list-init does not allow narrowing conversion of 4.5 to 4

    w1 = 4.5;       // okay: copy-assignment allows narrowing conversion of 4.5 to 4

    return 0;
}
值初始化和零初始化
当使用一组空的花括号初始化变量时，会发生一种特殊的列表初始化形式，称为
值初始化
。在大多数情况下，值初始化会隐式将变量初始化为零（或给定类型最接近零的值）。在发生置零的情况下，这称为
零初始化
。
int width {}; // value-initialization / zero-initialization to value 0
致进阶读者
对于类类型，值初始化（和默认初始化）可能会将对象初始化为预定义的默认值，这些值可能不是零。
列表初始化是现代 C++ 中首选的初始化形式
列表初始化（包括值初始化）通常优于其他初始化形式，因为它在大多数情况下都有效（因此最一致），它禁止窄化转换（我们通常不希望这样），并且它支持使用值列表进行初始化（我们将在未来的课程中介绍）。
最佳实践
首选直接列表初始化或值初始化来初始化您的变量。
作者注
Bjarne Stroustrup（C++ 创建者）和 Herb Sutter（C++ 专家）也建议
使用列表初始化
来初始化您的变量。
在现代 C++ 中，在某些情况下，列表初始化无法按预期工作。我们将在课程
16.2 -- std::vector 和列表构造函数简介
中介绍其中一种情况。由于这些怪癖，一些经验丰富的开发人员现在倡导根据具体情况混合使用复制、直接和列表初始化。一旦您对语言足够熟悉，能够理解每种初始化类型的细微差别以及这些建议背后的原因，您就可以自行评估这些论点是否具有说服力。
问：我应该用 { 0 } 还是 {} 来初始化？
当您实际使用初始值时，使用直接列表初始化
int x { 0 };    // direct-list-initialization with initial value 0
std::cout << x; // we're using that 0 value here
当对象的值是临时的并且将被替换时，使用值初始化
int x {};      // value initialization
std::cin >> x; // we're immediately replacing that value so an explicit 0 would be meaningless
初始化您的变量
在创建变量时对其进行初始化。您最终可能会发现出于特定原因（例如，使用大量变量的性能关键代码部分）而希望忽略此建议的情况，这没关系，只要选择是经过深思熟虑的。
相关内容
有关此主题的更多讨论，Bjarne Stroustrup（C++ 创建者）和 Herb Sutter（C++ 专家）
在此处
提出了此建议。
我们将在课程
1.6 -- 未初始化变量和未定义行为
中探讨如果您尝试使用没有明确定义值的变量会发生什么。
最佳实践
在创建变量时对其进行初始化。
实例化
术语
实例化
是一个花哨的词，意思是变量已经创建（分配）和初始化（包括默认初始化）。一个实例化对象有时称为一个
实例
。通常，这个术语应用于类类型对象，但偶尔也应用于其他类型的对象。
初始化多个变量
在上一节中，我们注意到可以通过用逗号分隔名称来在单个语句中定义多个
相同类型
的变量
int a, b; // create variables a and b, but do not initialize them
我们还注意到，最佳实践是完全避免这种语法。然而，由于您可能会遇到使用这种风格的其他代码，因此仍然有必要稍微谈论一下它，如果不是为了其他原因，只是为了强化您应该避免它的一些原因。
您可以初始化在同一行上定义的多个变量
int a = 5, b = 6;          // copy-initialization
int c ( 7 ), d ( 8 );      // direct-initialization
int e { 9 }, f { 10 };     // direct-list-initialization
int i {}, j {};            // value-initialization
不幸的是，这里有一个常见的陷阱，当程序员错误地尝试使用一个初始化语句来初始化两个变量时，可能会发生这种情况
int a, b = 5;     // wrong: a is not initialized to 5!
int a = 5, b = 5; // correct: a and b are initialized to 5
在上面的语句中，变量
a
将未被初始化，编译器可能会或可能不会抱怨。如果它不抱怨，这是导致您的程序间歇性崩溃或产生零星结果的好方法。我们很快将讨论如果您使用未初始化变量会发生什么。
记住这是错误的最佳方法是注意每个变量只能由其自己的初始化器初始化
int a = 4, b = 5; // correct: a and b both have initializers
int a, b = 5;     // wrong: a doesn't have its own initializer
未使用的已初始化变量警告
现代编译器通常会在变量已初始化但未使用时生成警告（因为这很少是期望的）。如果启用了“将警告视为错误”，这些警告将被提升为错误并导致编译失败。
考虑以下看似无害的程序
int main()
{
    int x { 5 }; // variable x defined

    // but not used anywhere

    return 0;
}
当使用 GCC 编译并启用“将警告视为错误”时，会生成以下错误
prog.cc: In function 'int main()':
prog.cc:3:9: error: unused variable 'x' [-Werror=unused-variable]
并且程序编译失败。
有几种简单的方法可以解决这个问题。
如果变量确实未使用且您不需要它，那么最简单的选择是删除
x
的定义（或将其注释掉）。毕竟，如果它未使用，那么删除它不会影响任何东西。
另一种选择是简单地在某个地方使用变量
#include <iostream>

int main()
{
    int x { 5 };

    std::cout << x; // variable now used somewhere

    return 0;
}
但这需要付出一些努力来编写使用它的代码，并且可能会改变程序的行为。
[[maybe_unused]]
属性
C++17
在某些情况下，上述两种选项都不可取。考虑这样一种情况：我们有一组在许多不同程序中使用的数学/物理值
#include <iostream>

int main()
{
    // Here's some math/physics values that we copy-pasted from elsewhere
    double pi { 3.14159 };
    double gravity { 9.8 };
    double phi { 1.61803 };

    std::cout << pi << '\n';  // pi is used
    std::cout << phi << '\n'; // phi is used

    // The compiler will likely complain about gravity being defined but unused

    return 0;
}
如果我们经常使用这些值，我们可能已将它们保存到某个地方并一起复制/粘贴/导入。
然而，在任何我们不使用
所有
这些值的程序中，编译器很可能会抱怨每个未实际使用的变量。在上面的示例中，我们可以很容易地删除
gravity
的定义。但是如果有 20 或 30 个变量而不是 3 个呢？如果我们多次使用它们呢？逐个变量地删除/注释掉未使用的变量需要时间和精力。如果以后我们需要一个我们以前删除的变量，我们将不得不花费更多的时间和精力来重新添加/取消注释它。
为了解决此类情况，C++17 引入了
[[maybe_unused]]
属性，它允许我们告诉编译器，我们不介意变量未使用。编译器不会为此类变量生成未使用变量警告。
以下程序应该不会生成任何警告/错误
#include <iostream>

int main()
{
    [[maybe_unused]] double pi { 3.14159 };  // Don't complain if pi is unused
    [[maybe_unused]] double gravity { 9.8 }; // Don't complain if gravity is unused
    [[maybe_unused]] double phi { 1.61803 }; // Don't complain if phi is unused

    std::cout << pi << '\n';
    std::cout << phi << '\n';

    // The compiler will no longer warn about gravity not being used

    return 0;
}
此外，编译器很可能会将这些变量从程序中优化掉，因此它们不会对性能产生影响。
[[maybe_unused]]
属性只应有选择地应用于有特定且正当理由未使用的变量（例如，因为您需要一个命名值列表，但特定程序中实际使用的特定值可能有所不同）。否则，未使用的变量应从程序中删除。
作者注
在未来的课程中，我们通常会定义不再使用的变量，以演示某些概念的语法。使用
[[maybe_unused]]
允许我们这样做而不会出现编译警告/错误。
小测验时间
问题 #1
初始化和赋值有什么区别？
显示答案
初始化在变量创建时为其提供初始值。赋值在变量创建后某个时刻为其赋值。
问题 #2
当您想用特定值初始化变量时，应该首选哪种形式的初始化？
显示答案
直接列表初始化（也称为直接大括号初始化）。
问题 #3
什么是默认初始化和值初始化？它们的行为分别是什么？您应该首选哪一个？
显示答案
默认初始化是指变量初始化没有初始化器（例如
int x;
）。在大多数情况下，变量会保留一个不确定的值。
值初始化是指变量初始化具有空大括号初始化器（例如
int x{};
）。在大多数情况下，这将执行零初始化。
您应该首选值初始化，因为它将变量初始化为一致的值。
下一课
1.5
iostream 简介：cout、cin 和 endl
返回目录
上一课
1.3
对象和变量简介