# 2.10 — 预处理器简介

2.10 — 预处理器简介
Alex
2007 年 6 月 3 日，太平洋夏令时 12:57
2025 年 3 月 5 日
当您编译项目时，您可能期望编译器会完全按照您编写的方式编译每个代码文件。事实并非如此。
相反，在编译之前，每个代码 (.cpp) 文件都会经过一个
预处理
阶段。在此阶段，一个名为
预处理器
的程序会对代码文件的文本进行各种更改。预处理器实际上不会以任何方式修改原始代码文件——相反，预处理器所做的所有更改都暂时发生在内存中或使用临时文件。
题外话…
历史上，预处理器是一个独立于编译器的程序，但在现代编译器中，预处理器可能内置在编译器本身中。
预处理器所做的大部分工作都相当无趣。例如，它会去除注释，并确保每个代码文件都以换行符结尾。然而，预处理器确实有一个非常重要的作用：它处理
#include
指令（我们稍后会详细讨论）。
当预处理器处理完代码文件后，结果称为
翻译单元
。然后，这个翻译单元由编译器编译。
相关内容
预处理、编译和链接的整个过程称为
翻译
。
如果您好奇，这里是
翻译阶段
的列表。截至撰写本文时，预处理包括阶段 1 到 4，编译是阶段 5 到 7。
预处理器指令
当预处理器运行时，它会扫描代码文件（从上到下），寻找预处理器指令。
预处理器指令
（通常简称为
指令
）是以
#
符号开头并以换行符（不是分号）结尾的指令。这些指令告诉预处理器执行某些文本操作任务。请注意，预处理器不理解 C++ 语法——相反，这些指令有自己的语法（在某些情况下类似于 C++ 语法，而在其他情况下则不然）。
关键见解
预处理器的最终输出不包含任何指令——只有已处理指令的输出才会传递给编译器。
题外话…
Using directives
（在课程
2.9 -- 命名冲突与命名空间简介
中介绍）不是预处理器指令（因此不被预处理器处理）。所以，尽管术语
directive
通常
指
preprocessor directive
，但并非总是如此。
#Include
您已经看到过
#include
指令的作用（通常是#include <iostream>）。当您
#include
一个文件时，预处理器会将#include指令替换为所包含文件的内容。然后，所包含的内容会被预处理（这可能会导致额外的#includes被递归预处理），然后文件的其余部分会被预处理。
考虑以下程序
#include <iostream>

int main()
{
    std::cout << "Hello, world!\n";
    return 0;
}
当预处理器在此程序上运行时，预处理器会将
#include <iostream>
替换为名为“iostream”的文件的内容，然后预处理所包含的内容和文件的其余部分。
由于
#include
几乎专门用于包含头文件，因此我们将在下一课中（当我们讨论头文件时）更详细地讨论
#include
。
关键见解
每个翻译单元通常由一个代码 (.cpp) 文件及其#include 的所有头文件组成（递归应用，因为头文件可以#include 其他头文件）。
宏定义
#define
指令可用于创建宏。在 C++ 中，
宏
是定义输入文本如何转换为替换输出文本的规则。
宏有两种基本类型：
类对象宏
和
类函数宏
。
类函数宏
像函数一样，起着类似的作用。它们的使用通常被认为是不安全的，并且它们几乎所有能做的事情都可以通过普通函数来完成。
类对象宏
可以通过两种方式定义
#define IDENTIFIER
#define IDENTIFIER substitution_text
顶部定义没有替换文本，而底部定义有。因为这些是预处理器指令（不是语句），所以请注意两种形式都不能以分号结尾。
宏的标识符使用与普通标识符相同的命名规则：它们可以使用字母、数字和下划线，不能以数字开头，并且不应以下划线开头。按照惯例，宏名称通常全大写，并用下划线分隔。
最佳实践
宏名称应以大写字母书写，单词之间用下划线分隔。
带有替换文本的类对象宏
当预处理器遇到此指令时，会在宏标识符和
substitution_text
之间建立关联。宏标识符的所有后续出现（在其他预处理器命令中使用除外）都将替换为
substitution_text
。
考虑以下程序
#include <iostream>

#define MY_NAME "Alex"

int main()
{
    std::cout << "My name is: " << MY_NAME << '\n';

    return 0;
}
预处理器将上述内容转换为以下内容
// The contents of iostream are inserted here

int main()
{
    std::cout << "My name is: " << "Alex" << '\n';

    return 0;
}
运行时，输出
My name is: Alex
。
带有替换文本的类对象宏在 C 语言中曾用于为字面量命名。现在不再需要了，因为 C++ 中有更好的方法（参见
7.10 -- 使用内联变量在多个文件之间共享全局常量
）。带有替换文本的类对象宏现在主要出现在遗留代码中，我们建议尽可能避免使用它们。
最佳实践
除非没有可行的替代方案，否则请避免使用带有替换文本的宏。
不带替换文本的类对象宏
类对象宏
也可以不带替换文本定义。
例如
#define USE_YEN
这种形式的宏按您期望的方式工作：标识符的大部分后续出现都将被移除并替换为空！
这看起来可能没什么用，而且对于文本替换来说确实
没什么用
。然而，这不是这种形式的指令通常的用途。我们稍后将讨论这种形式的用途。
与带有替换文本的类对象宏不同，这种形式的宏通常被认为是可接受的。
条件编译
条件编译
预处理器指令允许您指定在什么条件下编译或不编译某些内容。条件编译指令有很多种，但我们只介绍一些最常用的：
#ifdef
、
#ifndef
和
#endif
。
#ifdef
预处理器指令允许预处理器检查标识符是否已通过#define进行过定义。如果是，则编译
#ifdef
和匹配的
#endif
之间的代码。如果不是，则忽略代码。
考虑以下程序
#include <iostream>

#define PRINT_JOE

int main()
{
#ifdef PRINT_JOE
    std::cout << "Joe\n"; // will be compiled since PRINT_JOE is defined
#endif

#ifdef PRINT_BOB
    std::cout << "Bob\n"; // will be excluded since PRINT_BOB is not defined
#endif

    return 0;
}
由于 PRINT_JOE 已被 #define，因此行
std::cout << "Joe\n"
将被编译。由于 PRINT_BOB 未被 #define，因此行
std::cout << "Bob\n"
将被忽略。
#ifndef
与
#ifdef
相反，它允许您检查标识符是否
尚未
被
#define
。
#include <iostream>

int main()
{
#ifndef PRINT_BOB
    std::cout << "Bob\n";
#endif

    return 0;
}
此程序打印“Bob”，因为 PRINT_BOB 从未被
#define
过。
在
#ifdef PRINT_BOB
和
#ifndef PRINT_BOB
的位置，您还会看到
#if defined(PRINT_BOB)
和
#if !defined(PRINT_BOB)
。它们的作用相同，但使用略微更具 C++ 风格的语法。
您可以在课程
0.13 -- 我的编译器使用的是什么语言标准？
中看到此功能的实际应用。
#if 0
条件编译的另一个常见用法是使用
#if 0
来排除一段代码不被编译（就像它在一个注释块中一样）
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 0 // Don't compile anything starting here
    std::cout << "Bob\n";
    std::cout << "Steve\n";
#endif // until this point

    return 0;
}
上述代码只打印“Joe”，因为“Bob”和“Steve”被
#if 0
预处理器指令排除在编译之外。
这提供了一种方便的方法来“注释掉”包含多行注释的代码（由于多行注释不能嵌套，因此不能使用另一个多行注释来注释掉）
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 0 // Don't compile anything starting here
    std::cout << "Bob\n";
    /* Some
     * multi-line
     * comment here
     */
    std::cout << "Steve\n";
#endif // until this point

    return 0;
}
要暂时重新启用已包含在
#if 0
中的代码，您可以将
#if 0
更改为
#if 1
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 1 // always true, so the following code will be compiled
    std::cout << "Bob\n";
    /* Some
     * multi-line
     * comment here
     */
    std::cout << "Steve\n";
#endif

    return 0;
}
在其他预处理器命令中的宏替换
现在您可能想知道，给定以下代码
#define PRINT_JOE

int main()
{
#ifdef PRINT_JOE
    std::cout << "Joe\n"; // will be compiled since PRINT_JOE is defined
#endif

    return 0;
}
既然我们将
PRINT_JOE
定义为空，为什么预处理器没有在
#ifdef PRINT_JOE
中将
PRINT_JOE
替换为空并排除输出语句的编译呢？
在大多数情况下，当宏标识符在另一个预处理器命令中使用时，不会发生宏替换。
题外话…
此规则至少有一个例外：大多数形式的
#if
和
#elif
在预处理器命令中进行宏替换。
作为另一个例子
#define FOO 9 // Here's a macro substitution

#ifdef FOO // This FOO does not get replaced with 9 because it’s part of another preprocessor directive
    std::cout << FOO << '\n'; // This FOO gets replaced with 9 because it's part of the normal code
#endif
#defines 的作用域
指令在编译之前，以文件为单位从上到下解析。
考虑以下程序
#include <iostream>

void foo()
{
#define MY_NAME "Alex"
}

int main()
{
	std::cout << "My name is: " << MY_NAME << '\n';

	return 0;
}
尽管看起来
#define MY_NAME “Alex”
是在函数
foo
内部定义的，但预处理器不理解像函数这样的 C++ 概念。因此，此程序的行为与
#define MY_NAME “Alex”
在函数
foo
之前或紧随其后定义的程序行为相同。为避免混淆，您通常会希望在函数外部#define 标识符。
因为 #include 指令会将 #include 指令替换为所包含文件的内容，所以 #include 可以将所包含文件中的指令复制到当前文件中。然后这些指令将按顺序处理。
例如，以下示例也与之前的示例行为相同
Alex.h
#define MY_NAME "Alex"
main.cpp
#include "Alex.h" // copies #define MY_NAME from Alex.h here
#include <iostream>

int main()
{
	std::cout << "My name is: " << MY_NAME << '\n'; // preprocessor replaces MY_NAME with "Alex"

	return 0;
}
预处理器完成后，该文件中所有已定义的标识符都将被丢弃。这意味着指令仅从定义点到定义它们的文件末尾有效。在一个文件中定义的指令对其他文件没有任何影响（除非它们被#included 到另一个文件中）。例如
function.cpp
#include <iostream>

void doSomething()
{
#ifdef PRINT
    std::cout << "Printing!\n";
#endif
#ifndef PRINT
    std::cout << "Not printing!\n";
#endif
}
main.cpp
void doSomething(); // forward declaration for function doSomething()

#define PRINT

int main()
{
    doSomething();

    return 0;
}
以上程序将打印
Not printing!
尽管 PRINT 在
main.cpp
中定义，但这不会对
function.cpp
中的任何代码产生影响（PRINT 仅从定义点到 main.cpp 的末尾被#define）。这将在我们未来讨论头文件卫士时产生影响。
下一课
2.11
头文件
返回目录
上一课
2.9
命名冲突与命名空间简介