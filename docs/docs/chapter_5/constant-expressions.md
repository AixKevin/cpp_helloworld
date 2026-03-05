# 5.5 — 常量表达式

5.5 — 常量表达式
Alex
2022 年 6 月 16 日，太平洋夏令时下午 2:19
2025 年 2 月 18 日
在课程
1.10 -- 表达式简介
中，我们介绍了表达式。默认情况下，表达式在运行时求值。在某些情况下，它们必须如此。
std::cin >> x;
std::cout << 5 << '\n';
由于输入和输出无法在编译时执行，因此上述表达式需要在运行时求值。
在之前的课程
5.4 -- as-if 规则和编译时优化
中，我们讨论了 as-if 规则，以及编译器如何通过将工作从运行时转移到编译时来优化程序。根据 as-if 规则，编译器可以选择在运行时还是编译时评估某些表达式。
const double x { 1.2 };
const double y { 3.4 };
const double z { x + y }; // x + y may evaluate at runtime or compile-time
表达式
x + y
通常在运行时求值，但由于
x
和
y
的值在编译时已知，编译器可以选择执行编译时求值，并用编译时计算的值
4.6
初始化
z
。
在其他一些情况下，C++ 语言要求表达式可以在编译时求值。例如，constexpr 变量需要一个可以在编译时求值的初始化器。
int main()
{
    constexpr int x { expr }; // Because variable x is constexpr, expr must be evaluatable at compile-time
}
在需要常量表达式但未提供的情况下，编译器将报错并停止编译。
我们将在下一课（
5.6 -- Constexpr 变量
）中讨论 constexpr 变量。
致进阶读者
需要编译时可求值表达式的常见情况
constexpr 变量的初始化器（
5.6 -- Constexpr 变量
）。
非类型模板参数（
11.9 -- 非类型模板参数
）。
std::array
（
17.1 -- std::array 简介
）或 C 风格数组（
17.7 -- C 风格数组简介
）的定义长度。
在本课中，我们将更深入地探讨 C++ 在编译时求值方面的能力，并研究 C++ 如何区分后一种情况与前两种情况。
编译时编程的优势
虽然 as-if 规则对于提高性能非常有用，但它让我们依赖于编译器的复杂性来实际确定什么可以在编译时求值。这意味着如果我们真的想在编译时执行一段代码，它可能行也可能不行。相同的代码在不同的平台，或使用不同的编译器，或使用不同的编译选项，或稍作修改，可能会产生不同的结果。由于 as-if 规则对我们是不可见的，我们无法从编译器那里获得关于它决定在编译时求值哪些代码以及原因的反馈。我们希望在编译时求值的代码甚至可能不符合条件（由于拼写错误或误解），我们可能永远不会知道。
为了改善这种情况，C++ 语言提供了明确指定我们希望在编译时执行的代码部分的方法。使用导致编译时求值的语言特性称为
编译时编程
。
这些特性可以在许多方面帮助改进软件
性能：编译时求值使我们的程序更小更快。我们能确保在编译时求值的代码越多，我们看到的性能优势就越大。
通用性：我们总能将此类代码用于需要编译时值的地方。依赖 as-if 规则在编译时求值的代码不能用于此类地方（即使编译器选择在编译时求值该代码）——之所以做出此决定，是为了让今天编译的代码不会在明天编译器决定以不同方式优化时停止编译。
可预测性：如果编译器确定代码无法在编译时执行，我们可以让它停止编译（而不是默默地选择让代码在运行时求值）。这使我们能够确保我们真正希望在编译时执行的代码部分能够执行。
质量：我们可以让编译器在编译时可靠地检测某些类型的编程错误，并在遇到这些错误时停止构建。这比在运行时尝试检测和优雅地处理相同的错误要有效得多。
质量：也许最重要的是，编译时不允许未定义行为。如果我们在编译时做了导致未定义行为的事情，编译器应该停止构建并要求我们修复它。请注意，这对编译器来说是一个难题，它们可能无法捕获所有情况。
总而言之，编译时求值使我们能够编写性能更高、质量更好（更安全、bug 更少）的程序！因此，虽然编译时求值确实增加了语言的一些额外复杂性，但其好处可能是巨大的。
以下 C++ 特性是编译时编程最基础的
Constexpr 变量（将在即将到来的课程
5.6 -- Constexpr 变量
中讨论）。
Constexpr 函数（将在即将到来的课程
F.1 -- Constexpr 函数
中讨论）。
模板（在课程
11.6 -- 函数模板
中介绍）。
static_assert（在课程
9.6 -- 断言和 static_assert
中讨论）。
所有这些特性都有一个共同点：它们都使用常量表达式。
常量表达式
也许令人惊讶的是，C++ 标准几乎没有提及“编译时”。相反，标准定义了一个“常量表达式”，它是一个必须在编译时可求值的表达式，并附带确定编译器应如何处理这些表达式的规则。常量表达式构成了 C++ 中编译时求值的骨干。
在课程
1.10 -- 表达式简介
中，我们将表达式定义为“字面量、变量、运算符和函数调用的非空序列”。
常量表达式
是字面量、常量变量、运算符和函数调用的非空序列，所有这些都必须在编译时可求值。关键区别在于，在常量表达式中，表达式的每个部分都必须在编译时可求值。
关键见解
在常量表达式中，表达式的每个部分都必须在编译时可求值。
不是常量表达式的表达式通常称为非常量表达式，并且可以非正式地称为
运行时表达式
（因为此类表达式通常在运行时求值）。
选读
C++20 语言标准（在 [expr.const] 部分）规定：“常量表达式可以在翻译期间求值”。正如我们在课程
2.10 -- 预处理器简介
中介绍的，翻译是构建程序的整个过程（包括预处理、编译和链接）。因此，在编译程序中，常量表达式可以作为编译过程的一部分进行求值。在解释程序中，翻译发生在运行时。
由于 C++ 程序通常是编译的，我们将假设常量表达式可以在编译时求值。
常量表达式中可以包含什么？
作者注
从技术角度来看，常量表达式相当复杂。在本节中，我们将更深入地探讨它们可以和不可以包含什么。您无需记住大部分内容。如果某处需要常量表达式而您未提供，编译器会很乐意指出您的错误，届时您可以修复它。
最常见的是，常量表达式包含以下内容
字面量（例如 '5', '1.2'）
大多数带有常量表达式操作符的运算符（例如
3 + 4
,
2 * sizeof(int)
）。
带有常量表达式初始化器的 const 整型变量（例如
const int x { 5 };
）。这是一个历史例外——在现代 C++ 中，constexpr 变量更受青睐。
Constexpr 变量（将在即将到来的课程
5.6 -- Constexpr 变量
中讨论）。
带有常量表达式参数的 constexpr 函数调用（参见
F.1 -- Constexpr 函数
）。
致进阶读者
常量表达式还可以包含
非类型模板参数（参见
11.9 -- 非类型模板参数
）。
枚举器（参见
13.2 -- 无作用域枚举
）。
类型特性（参见
cppreference 上的类型特性页面
）。
Constexpr lambda 表达式（参见
20.6 -- lambda 表达式（匿名函数）简介
）。
提示
值得注意的是，以下内容不能用于常量表达式中
非 const 变量。
const 非整型变量，即使它们具有常量表达式初始化器（例如
const double d { 1.2 };
）。要在常量表达式中使用此类变量，请改为将其定义为 constexpr 变量（参见课程
5.6 -- Constexpr 变量
）。
非 constexpr 函数的返回值（即使返回表达式是常量表达式）。
函数参数（即使函数是 constexpr）。
操作数不是常量表达式的运算符（例如，当
x
或
y
不是常量表达式时，
x + y
；或
std::cout << "hello\n"
，因为
std::cout
不是常量表达式）。
运算符
new
、
delete
、
throw
、
typeid
和
operator,
（逗号）。
包含上述任何内容的表达式都是运行时表达式。
相关内容
有关常量表达式的精确定义，请参见
cppreference 上的常量表达式页面
。请注意，常量表达式是通过它不是什么类型的表达式来定义的。这意味着我们只能推断它是什么。祝你好运！
命名法
在讨论常量表达式时，通常使用以下两种措辞之一
“X 可用于常量表达式”通常用于强调 X 是什么。例如，“
5
可用于常量表达式”强调字面量
5
可用于常量表达式。
“X 是一个常量表达式”有时用于强调整个表达式（由 X 组成）是一个常量表达式。例如，“
5
是一个常量表达式”强调表达式
5
是一个常量表达式。
当它被表述为“字面量是常量表达式”时，后者可能听起来很别扭（因为它们实际上是值）。但这仅仅意味着由字面量组成的表达式是一个常量表达式。
题外话…
当常量表达式被定义时，
const
整型类型被保留了下来，因为它们在语言中已经被视为常量表达式。
委员会讨论了带有常量表达式初始化器的
const
非整型类型是否也应被视为常量表达式（为了与
const
整型类型的情况保持一致）。最终，他们决定不这样做，以促进
constexpr
的更一致使用。
常量表达式和非常量表达式的示例
在以下程序中，我们查看了一些表达式语句，并指出每个表达式是常量表达式还是运行时表达式
#include <iostream>

int getNumber()
{
    std::cout << "Enter a number: ";
    int y{};
    std::cin >> y; // can only execute at runtime

    return y;      // this return expression is a runtime expression
}

// The return value of a non-constexpr function is a runtime expression
// even when the return expression is a constant expression
int five()
{
    return 5;      // this return expression is a constant expression
}

int main()
{
    // Literals can be used in constant expressions
    5;                           // constant expression            
    1.2;                         // constant expression
    "Hello world!";              // constant expression

    // Most operators that have constant expression operands can be used in constant expressions
    5 + 6;                       // constant expression
    1.2 * 3.4;                   // constant expression
    8 - 5.6;                     // constant expression (even though operands have different types)
    sizeof(int) + 1;             // constant expression (sizeof can be determined at compile-time)

    // The return values of non-constexpr functions can only be used in runtime expressions
    getNumber();                 // runtime expression
    five();                      // runtime expression (even though the return expression is a constant expression)

    // Operators without constant expression operands can only be used in runtime expressions
    std::cout << 5;              // runtime expression (std::cout isn't a constant expression operand)

    return 0;
}
在以下代码片段中，我们定义了一些变量，并指出它们是否可以在常量表达式中使用
// Const integral variables with a constant expression initializer can be used in constant expressions:
    const int a { 5 };           // a is usable in constant expressions
    const int b { a };           // b is usable in constant expressions (a is a constant expression per the prior statement)
    const long c { a + 2 };      // c is usable in constant expressions (operator+ has constant expression operands)

    // Other variables cannot be used in constant expressions (even when they have a constant expression initializer):
    int d { 5 };                 // d is not usable in constant expressions (d is non-const)
    const int e { d };           // e is not usable in constant expressions (initializer is not a constant expression)
    const double f { 1.2 };      // f is not usable in constant expressions (not a const integral variable)
常量表达式在编译时求值时
由于常量表达式总是能够在编译时求值，您可能已经假定常量表达式将始终在编译时求值。然而，这与直觉相反，情况并非如此。
编译器只在**要求**常量表达式的上下文中**要求**在编译时求值常量表达式。
命名法
必须在编译时求值的表达式的技术名称是
显式常量求值表达式
。您可能只会在技术文档中遇到此术语。
在不要求常量表达式的上下文中，编译器可以选择在编译时还是在运行时求值常量表达式。
const int x { 3 + 4 }; // constant expression 3 + 4 must be evaluated at compile-time
int y { 3 + 4 };       // constant expression 3 + 4 may be evaluated at compile-time or runtime
变量
x
的类型为
const int
，并带有常量表达式初始化器，
x
可用于常量表达式。其初始化器必须在编译时求值（否则
x
的值在编译时将未知，并且
x
将无法用于常量表达式）。另一方面，变量
y
是非 const 的，因此
y
无法用于常量表达式。即使其初始化器是常量表达式，编译器也可以决定在编译时或运行时求值初始化器。
即使不需要这样做，现代编译器在启用优化时通常会在编译时求值常量表达式。
关键见解
编译器只在**要求**常量表达式的上下文中**要求**在编译时求值常量表达式。在其他情况下，它可能会也可能不会这样做。
提示
表达式在编译时完全求值的可能性可分类如下
从不：编译器无法在编译时确定所有值的非常量表达式。
可能：编译器能够在编译时确定所有值的非常量表达式（根据 as-if 规则优化）。
可能：在不要求常量表达式的上下文中使用常量表达式。
总是：在要求常量表达式的上下文中使用常量表达式。
致进阶读者
那么，为什么 C++ 不要求所有常量表达式都在编译时求值呢？至少有两个很好的理由：
编译时求值使调试更加困难。如果我们的代码中存在在编译时求值的错误计算，我们诊断问题的工具有限。允许非必需的常量表达式在运行时求值（通常在优化关闭时）可以对我们的代码进行运行时调试。能够单步执行并检查程序运行时的状态可以更容易地找到错误。
为了让编译器能够灵活地根据需要进行优化（或受编译器选项的影响）。例如，编译器可能希望提供一个选项，将所有非必需的常量表达式求值推迟到运行时，以缩短开发人员的编译时间。
为什么编译时表达式必须是常量
可选
您可能想知道为什么编译时表达式只能包含常量对象（以及可以在编译时求值为常量的运算符和函数）。
考虑以下程序
#include <iostream>

int main()
{
    int x { 5 };
    // x is known to the compiler at this point

    std::cin >> x; // read in value of x from user
    // x is no longer known to the compiler

    return 0;
}
首先，
x
初始化值为
5
。此时
x
的值对编译器是已知的。但随后
x
被用户赋值。编译器无法在编译时知道用户会提供什么值，因此从这一点开始，
x
的值对编译器是未知的。因此，表达式
x
并非总是能在编译时求值，违反了此类表达式必须始终能在编译时求值的要求。
因为常量的值不能改变，所以一个其初始化器可以在编译时求值的常量变量，其值总是可以在编译时已知。这使得事情变得简单。
虽然语言设计者可以将编译时表达式定义为所有值在编译时当前已知的表达式（而不是一个必须始终能够在编译时求值的表达式），但这会给编译器增加显著的复杂性（因为编译器现在将负责确定每个变量何时可能更改为编译时未知的值）。添加一行代码（例如
std::cin >> x
）可能会在程序的其他地方破坏程序（如果
x
在任何需要编译时已知值的上下文中被使用）。
小测验时间
问题 #1
对于每个语句，识别
初始化器是常量表达式还是非常量表达式。
变量是常量表达式还是非常量表达式。
a)
char a { 'q' };
显示答案
'q'
是一个常量表达式，因为它是一个字面量。
a
是一个非常量表达式，因为它被定义为非 const。
b)
const int b { 0 };
显示答案
0
是一个常量表达式，因为它是一个字面量。
b
是一个常量表达式，因为它是一个带有常量表达式初始化器的
const
整型类型。
c)
const double c { 5.0 };
显示答案
'5.0'
是一个常量表达式，因为它是一个字面量。
c
是一个非常量表达式，因为它被定义为
const
但没有整型。
根据编译时常量的定义，只有带有常量表达式初始化器的 const **整型**变量才是编译时常量。
c
是一个 double 类型，它不是整型，因此不符合此定义。
d)
const int d { a * 2 }; // a defined as char a { 'q' };
显示答案
a
不是常量表达式，所以
a * 2
是一个非常量表达式。
d
是一个非常量表达式，因为初始化器不是常量表达式。
e)
int e { c + 1.0 }; // c defined as const double c { 5.0 };
显示答案
c
是一个非常量表达式，所以
c + 1.0
是一个非常量表达式。
e
是一个非常量表达式，因为它没有定义为
const
，并且它没有一个常量表达式初始化器。
f)
const int f { d * 2 }; // d defined as const int d { 0 };
显示答案
d
和
2
都是常量表达式，所以
d * 2
是一个常量表达式。
f
是一个常量表达式，因为它是一个带有常量表达式初始化器的
const
整型类型。
g)
const int g { getNumber() }; // getNumber returns an int by value
显示答案
getNumber()
返回一个非常量值，因此它是一个非常量表达式。
g
是一个非常量表达式，因为初始化器是一个非常量表达式。
h)
额外加分
const int h{};
显示答案
{}
调用值初始化。这里没有显式初始化器。
h
是一个常量表达式，因为它是一个带有常量表达式初始化器（值初始化将
h
初始化为
0
，这是一个常量表达式）的
const
整型类型。
下一课
5.6
Constexpr 变量
返回目录
上一课
5.4
as-if 规则和编译时优化