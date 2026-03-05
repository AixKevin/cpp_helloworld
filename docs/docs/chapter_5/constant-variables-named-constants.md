# 5.1 — 常量变量（命名常量）

5.1 — 常量变量（命名常量）
Alex
2015 年 2 月 23 日，下午 5:13（太平洋标准时间）
2024 年 10 月 17 日
常量简介
在编程中，
常量
是指在程序执行期间不能更改的值。
C++ 支持两种不同类型的常量
命名常量
是与标识符关联的常量值。这些有时也称为
符号常量
。
字面量常量
是未与标识符关联的常量值。
我们将从命名常量开始介绍常量。然后我们将介绍字面量常量（在即将到来的课程
5.2 -- 字面量
中）。
命名常量的类型
在 C++ 中定义命名常量有三种方法
常量变量（本课涵盖）。
带有替换文本的类对象宏（在课程
2.10 -- 预处理器简介
中介绍，本课中还有额外内容）。
枚举常量（在课程
13.2 -- 无作用域枚举
中涵盖）。
常量变量是最常见的命名常量类型，所以我们从这里开始。
常量变量
到目前为止，我们看到的所有变量都是非常量变量——也就是说，它们的值可以随时更改（通常通过赋值新值）。例如
int main()
{
    int x { 4 }; // x is a non-constant variable
    x = 5; // change value of x to 5 using assignment operator

    return 0;
}
然而，在许多情况下，定义值不能更改的变量很有用。例如，考虑地球（接近地表）的重力：9.8 米/秒
2
。这不太可能很快改变（如果真的改变了，你可能面临比学习 C++ 更大的问题）。将此值定义为常量有助于确保此值不会意外更改。常量还有其他好处，我们将在后续课程中探讨。
尽管它是一个众所周知的矛盾修辞法，但初始化后不能更改其值的变量称为
常量变量
。
声明 const 变量
要声明一个常量变量，我们将
const
关键字（称为“const 限定符”）放在对象的类型旁边
const double gravity { 9.8 };  // preferred use of const before type
int const sidesInSquare { 4 }; // "east const" style, okay but not preferred
尽管 C++ 允许将 const 限定符放在类型之前或之后，但更常见的是将
const
放在类型之前，因为它更符合标准英语语言习惯，其中修饰语位于被修饰对象之前（例如“a green ball”，而不是“a ball green”）。
题外话…
由于编译器解析更复杂声明的方式，一些开发人员更喜欢将
const
放在类型之后（因为它稍微更一致）。这种风格被称为“east const”。虽然这种风格有一些支持者（以及一些合理的观点），但它尚未得到广泛采用。
最佳实践
将
const
放在类型之前（因为这样做更符合惯例）。
关键见解
对象的类型包括 const 限定符，所以当我们定义
const double gravity { 9.8 };
时，
gravity
的类型是
const double
。
const 变量必须初始化
const 变量在定义时
必须
初始化，然后该值不能通过赋值更改
int main()
{
    const double gravity; // error: const variables must be initialized
    gravity = 9.9;        // error: const variables can not be changed

    return 0;
}
请注意，const 变量可以从其他变量（包括非 const 变量）初始化
#include <iostream>

int main()
{ 
    std::cout << "Enter your age: ";
    int age{};
    std::cin >> age;

    const int constAge { age }; // initialize const variable using non-const value

    age = 5;      // ok: age is non-const, so we can change its value
    constAge = 6; // error: constAge is const, so we cannot change its value

    return 0;
}
在上面的例子中，我们使用非 const 变量
age
初始化 const 变量
constAge
。因为
age
仍然是非 const 的，我们可以改变它的值。然而，因为
constAge
是 const 的，我们不能改变它初始化后的值。
关键见解
const 变量的初始化器可以是一个非常量值。
命名 const 变量
常量变量有许多不同的命名约定。
从 C 语言过渡而来的程序员通常更喜欢使用带下划线的大写名称作为常量变量（例如
EARTH_GRAVITY
）。在 C++ 中更常见的是使用带有“k”前缀的驼峰式命名（例如
kEarthGravity
）。
然而，由于常量变量的行为与普通变量类似（除了不能赋值），因此它们没有理由需要特殊的命名约定。因此，我们更喜欢使用与非常量变量相同的命名约定（例如
earthGravity
）。
const 函数参数
函数参数可以通过
const
关键字设置为常量
#include <iostream>

void printInt(const int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(5); // 5 will be used as the initializer for x
    printInt(6); // 6 will be used as the initializer for x

    return 0;
}
请注意，我们没有为我们的 const 参数
x
提供显式初始化器——函数调用中参数的值将用作
x
的初始化器。
将函数参数设置为常量有助于编译器确保参数的值在函数内部不会被更改。然而，在现代 C++ 中，我们不会将值参数设置为
const
，因为我们通常不关心函数是否更改参数的值（因为它只是一个副本，无论如何都会在函数结束时被销毁）。
const
关键字还会给函数原型增加少量不必要的冗余。
最佳实践
不要对值参数使用
const
。
在本教程系列的稍后部分，我们将讨论将参数传递给函数的另外两种方式：按引用传递和按地址传递。使用这两种方法时，正确使用
const
非常重要。
const 返回值
函数的返回值也可以是 const
#include <iostream>

const int getValue()
{
    return 5;
}

int main()
{
    std::cout << getValue() << '\n';

    return 0;
}
对于基本类型，返回类型上的
const
限定符会被忽略（您的编译器可能会生成警告）。
对于其他类型（我们将在稍后介绍），按值返回 const 对象通常没有意义，因为它们是临时副本，无论如何都会被销毁。返回 const 值还会阻碍某些类型的编译器优化（涉及移动语义），从而导致性能下降。
最佳实践
按值返回时不要使用
const
。
为什么变量应该声明为常量
如果一个变量可以被声明为常量，那么它通常应该被声明为常量。这很重要，原因如下：
它减少了出现 bug 的机会。通过将变量设为常量，您可以确保其值不会意外更改。
它为编译器提供了更多优化程序的机会。当编译器可以假定一个值不会改变时，它就能够利用更多的技术来优化程序，从而使编译后的程序更小、更快。我们将在本章的后面进一步讨论这个问题。
最重要的是，它降低了我们程序的整体复杂性。在尝试确定一段代码正在做什么或尝试调试问题时，我们知道常量变量的值不能更改，所以我们不必担心它的值是否真的在改变、改变成了什么值以及新值是否正确。
关键见解
系统中的每个活动部件都会增加复杂性以及缺陷或故障的风险。非常量变量是活动部件，而常量变量则不是。
最佳实践
尽可能将变量声明为常量。例外情况包括按值传递的函数参数和按值返回的类型，它们通常不应该声明为常量。
带有替换文本的类对象宏
在课程
2.10 -- 预处理器简介
中，我们讨论了带有替换文本的类对象宏。例如
#include <iostream>

#define MY_NAME "Alex"

int main()
{
    std::cout << "My name is: " << MY_NAME << '\n';

    return 0;
}
当预处理器处理包含此代码的文件时，它会将
MY_NAME
（第 7 行）替换为
"Alex"
。请注意，
MY_NAME
是一个名称，替换文本是一个常量值，因此带有替换文本的类对象宏也是命名常量。
优先使用常量变量而不是预处理器宏
那为什么不为命名常量使用预处理器宏呢？至少有三个主要问题。
最大的问题是宏不遵循正常的 C++ 作用域规则。一旦宏被 #定义，该宏名称在当前文件中的所有后续出现都将被替换。如果该名称在其他地方使用，您将在不需要的地方进行宏替换。这最有可能导致奇怪的编译错误。例如
#include <iostream>

void someFcn()
{
// Even though gravity is defined inside this function
// the preprocessor will replace all subsequent occurrences of gravity in the rest of the file
#define gravity 9.8
}

void printGravity(double gravity) // including this one, causing a compilation error
{
    std::cout << "gravity: " << gravity << '\n';
}

int main()
{
    printGravity(3.71);

    return 0;
}
编译时，GCC 产生了以下令人困惑的错误
prog.cc:7:17: error: expected ',' or '...' before numeric constant
    5 | #define gravity 9.8
      |                 ^~~
prog.cc:10:26: note: in expansion of macro 'gravity'
其次，使用宏的代码通常更难调试。虽然您的源代码将包含宏的名称，但编译器和调试器永远不会看到宏，因为它在它们运行之前就已经被替换了。许多调试器无法检查宏的值，并且在处理宏时通常功能有限。
第三，宏替换的行为与 C++ 中的其他一切都不同。因此很容易无意中犯错。
常量变量没有这些问题：它们遵循正常的作用域规则，可以被编译器和调试器看到，并且行为一致。
最佳实践
优先使用常量变量而不是带有替换文本的类对象宏。
在多文件程序中使用常量变量
在许多应用程序中，某个命名常量需要在您的代码中（不仅仅在一个文件中）普遍使用。这可能包括不改变的物理或数学常数（例如 pi 或阿伏伽德罗常数），或特定于应用程序的“调整”值（例如摩擦力或重力系数）。与其每次需要时都重新定义这些值，不如将它们集中在一个地方声明一次，并在需要的地方使用它们。这样，如果您需要更改它们，只需在一个地方更改即可。
C++ 中有多种方法可以实现这一点——我们将在课程
7.10 -- 在多个文件之间共享全局常量（使用内联变量）
中详细介绍此主题。
术语：类型限定符
类型限定符
（有时简称为
限定符
）是应用于类型以修改该类型行为方式的关键字。用于声明常量变量的
const
称为
const 类型限定符
（或简称为
const 限定符
）。
截至 C++23，C++ 只有两种类型限定符：
const
和
volatile
。
选读
volatile
限定符用于告诉编译器对象的值可能随时发生变化。这个不常用的限定符会禁用某些类型的优化。
在技术文档中，
const
和
volatile
限定符通常被称为
cv-限定符
。C++ 标准中还使用了以下术语
cv-非限定
类型是没有类型限定符的类型（例如
int
）。
cv-限定
类型是应用了一个或多个类型限定符的类型（例如
const int
）。
可能 cv-限定
类型是可能是 cv-非限定或 cv-限定的类型。
这些术语在技术文档之外很少使用，因此此处列出它们是为了参考，而不是您需要记住的内容。
但至少现在你可以欣赏来自
JF Bastien
的这个笑话了
问：你怎么知道 C++ 开发者是否合格？
答：你看他们的简历（CV）。
下一课
5.2
字面量
返回目录
上一课
4.x
第 4 章总结与测验