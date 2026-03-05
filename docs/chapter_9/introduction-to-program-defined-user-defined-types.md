# 13.1 — 程序定义（用户定义）类型简介

13.1 — 程序定义（用户定义）类型简介
Alex
2022年1月18日，太平洋标准时间上午10:17
2025年2月24日
因为基本类型是C++核心语言的一部分，所以它们可以直接使用。例如，如果我们要定义一个
int
或
double
类型的变量，我们可以直接这样做
int x; // define variable of fundamental type 'int'
double d; // define variable of fundamental type 'double'
这对于作为基本类型简单扩展的复合类型（包括函数、指针、引用和数组）也是如此。
void fcn(int) {}; // define a function of type void(int)
int* ptr; // define variable of compound type 'pointer to int'
int& ref { x }; // define variable of compound type 'reference to int' (initialized with x)
int arr[5]; // define an array of 5 integers of type int[5] (we'll cover this in a future chapter)
这之所以有效，是因为C++语言已经知道这些类型的类型名称（和符号）的含义——我们不需要提供或导入任何定义。
然而，考虑类型别名（在课程
10.7 -- Typedefs和类型别名
中介绍）的情况，它允许我们为现有类型定义一个新名称。因为类型别名向程序中引入了一个新的标识符，所以类型别名必须在使用前定义
#include <iostream>

using Length = int; // define a type alias with identifier 'Length'

int main()
{
    Length x { 5 }; // we can use 'length' here since we defined it above
    std::cout << x << '\n';

    return 0;
}
如果我们省略`Length`的定义，编译器将不知道`Length`是什么，并在我们尝试使用该类型定义变量时报错。`Length`的定义不会创建对象——它只是告诉编译器`Length`是什么，以便以后可以使用它。
什么是用户定义/程序定义类型？
回到前一章的介绍（
12.1 -- 复合数据类型介绍
），我们介绍了想要存储一个分数的挑战，该分数具有在概念上相互关联的分子和分母。在该课程中，我们讨论了使用两个单独的整数来独立存储分数的分子和分母的一些挑战。
如果 C++ 有内置的分数类型，那将是完美的——但它没有。而且还有数百种其他可能有用的类型，C++ 没有包含它们，因为它不可能预料到所有人都可能需要的东西（更不用说实现和测试这些东西了）。
相反，C++ 以不同的方式解决此类问题：通过允许创建全新的自定义类型，我们可以在程序中使用它们！此类类型称为**用户定义类型**。然而，正如我们将在本课后面讨论的那样，我们将更喜欢**程序定义类型**这一术语，用于我们为在自己的程序中使用而创建的任何此类类型。
C++ 有两类复合类型可用于创建程序定义类型
枚举类型（包括无作用域枚举和有作用域枚举）
类类型（包括结构体、类和联合体）。
定义程序定义的类型
就像类型别名一样，程序定义的类型也必须在使用前被定义并给定一个名称。程序定义的类型的定义被称为**类型定义**。
关键见解
程序定义的类型在使用前必须有一个名称和一个定义。其他复合类型则不需要。
函数不被视为用户定义类型（即使它们在使用前需要一个名称和一个定义），因为被赋予名称和定义的是函数本身，而不是函数的类型。我们自己定义的函数被称为用户定义函数。
尽管我们尚未介绍什么是结构体，但这里有一个示例，展示了自定义 `Fraction` 类型的定义以及使用该类型实例化对象的过程
// Define a program-defined type named Fraction so the compiler understands what a Fraction is
// (we'll explain what a struct is and how to use them later in this chapter)
// This only defines what a Fraction type looks like, it doesn't create one
struct Fraction
{
	int numerator {};
	int denominator {};
};

// Now we can make use of our Fraction type
int main()
{
	Fraction f { 3, 4 }; // this actually instantiates a Fraction object named f

	return 0;
}
在此示例中，我们使用 `struct` 关键字定义了一个名为 `Fraction` 的新程序定义类型（在全局作用域中，因此可以在文件的其余部分中的任何位置使用）。这不会分配任何内存——它只是告诉编译器 `Fraction` 的样子，以便我们以后可以分配 `Fraction` 类型的对象。然后，在 `main()` 内部，我们实例化（并初始化）一个名为 `f` 的 `Fraction` 类型的变量。
程序定义的类型定义必须以分号结尾。未能包含分号是程序员常见的错误，并且可能难以调试，因为编译器可能会在类型定义**之后**的行上报错。
警告
不要忘记在类型定义末尾加上分号。
我们将在下一课（
13.2 -- 无作用域枚举
）中展示更多定义和使用程序定义类型的示例，我们将从课程
13.7 -- 结构体、成员和成员选择简介
开始介绍结构体。
命名程序定义的类型
按照惯例，程序定义的类型名称以大写字母开头，并且不使用后缀（例如 `Fraction`，而不是 `fraction`、`fraction_t` 或 `Fraction_t`）。
最佳实践
您的程序定义类型应以大写字母开头命名，并且不使用后缀。
新程序员有时会发现以下变量定义令人困惑，因为类型名称和变量名称相似
Fraction fraction {}; // Instantiates a variable named fraction of type Fraction
这与任何其他变量定义无异：类型（`Fraction`）在前（因为 `Fraction` 大写，我们知道它是一个程序定义的类型），然后是变量名（`fraction`），然后是可选的初始化器。由于 C++ 区分大小写，这里没有命名冲突！
在多文件程序中使用程序定义的类型
使用程序定义类型的每个代码文件在使用该类型之前都需要看到完整的类型定义。前向声明是不够的。这是必需的，以便编译器知道为该类型的对象分配多少内存。
为了将类型定义传播到需要它们的代码文件中，程序定义的类型通常定义在头文件中，然后通过`#include`指令引入到任何需要该类型定义的代码文件中。这些头文件通常与程序定义的类型同名（例如，名为`Fraction`的程序定义类型将定义在`Fraction.h`中）。
最佳实践
仅在一个代码文件中使用的程序定义类型应在该代码文件中定义，并尽可能靠近第一次使用点。
在多个代码文件中使用的程序定义类型应定义在与程序定义类型同名的头文件中，然后根据需要`#include`到每个代码文件中。
以下是如果我们将 `Fraction` 类型移到头文件（名为 `Fraction.h`）中，以便它可以包含在多个代码文件中时的样子
Fraction.h
#ifndef FRACTION_H
#define FRACTION_H

// Define a new type named Fraction
// This only defines what a Fraction looks like, it doesn't create one
// Note that this is a full definition, not a forward declaration
struct Fraction
{
	int numerator {};
	int denominator {};
};

#endif
Fraction.cpp
#include "Fraction.h" // include our Fraction definition in this code file

// Now we can make use of our Fraction type
int main()
{
	Fraction f{ 3, 4 }; // this actually creates a Fraction object named f

	return 0;
}
类型定义部分豁免于单一定义规则 (ODR)
在课程
2.7 -- 前向声明和定义
中，我们讨论了单一定义规则如何要求每个函数和全局变量在每个程序中只能有一个定义。要在不包含定义的文件中使用给定的函数或全局变量，我们需要一个前向声明（我们通常通过头文件传播）。这之所以有效，是因为对于函数和非 constexpr 变量，声明足以满足编译器，链接器可以连接所有内容。
然而，以类似方式使用前向声明对类型不起作用，因为编译器通常需要看到完整的定义才能使用给定的类型。我们必须能够将完整的类型定义传播到每个需要它的代码文件。
为了允许这种情况，类型部分豁免于单一定义规则：允许在多个代码文件中定义给定类型。
您已经使用了此功能（可能没有意识到）：如果您的程序有两个都 `#include
` 的代码文件，您正在将所有输入/输出类型定义导入到这两个文件中。
有两个值得注意的注意事项。首先，每个代码文件仍然只能有一个类型定义（这通常不是问题，因为头文件保护会阻止这种情况发生）。其次，给定类型的所有类型定义必须完全相同，否则将导致未定义行为。
术语：用户定义类型 vs 程序定义类型
“用户定义类型”一词有时会在日常对话中出现，也曾在 C++ 语言标准中被提及（但未定义）。在日常对话中，该术语通常指“在您自己的程序中定义的类型”（例如上面提到的 `Fraction` 类型）。
C++语言标准以非传统方式使用“用户定义类型”一词。在语言标准中，“用户定义类型”是您、标准库或实现（例如，编译器为支持语言扩展而定义的类型）定义的任何类类型或枚举类型。可能有些反直觉的是，这意味着`std::string`（标准库中定义的类类型）被认为是用户定义类型！
为了提供额外的区分，C++20 语言标准明确定义了“程序定义类型”一词，指代并非作为标准库、实现或核心语言一部分定义的类类型和枚举类型。换句话说，“程序定义类型”只包括我们（或第三方库）定义的类类型和枚举类型。
因此，当我们只谈论为在自己的程序中使用而定义的类类型和枚举类型时，我们将更倾向于使用“程序定义”一词，因为它具有更精确的定义。
类型
含义
示例
基本类型
内置于 C++ 核心语言中的基本类型
int, std::nullptr_t
复合
根据其他类型定义的类型
int&, double*, std::string, Fraction
用户自定义
类类型或枚举类型
（包括在标准库或实现中定义的）
（在日常使用中，通常指程序定义类型）
std::string, Fraction
程序定义
类类型或枚举类型
（不包括标准库或实现中定义的）
分数
下一课
13.2
无作用域枚举
返回目录
上一课
12.x
第12章总结和测验