# 7.2 — 用户自定义命名空间和作用域解析运算符

7.2 — 用户自定义命名空间和作用域解析运算符
Alex
2007 年 8 月 17 日，下午 6:09 PDT
2024 年 6 月 28 日
在
2.9 课 -- 命名冲突和命名空间简介
中，我们介绍了
命名冲突
和
命名空间
的概念。提醒一下，当两个相同的标识符被引入到同一作用域中时，就会发生命名冲突，编译器无法区分应该使用哪一个。发生这种情况时，编译器或链接器会产生错误，因为它们没有足够的信息来解决歧义。
关键见解
随着程序的规模变大，标识符的数量也会增加，这反过来会导致命名冲突发生的概率显著增加。因为给定作用域中的每个名称都可能与同一作用域中的其他所有名称发生冲突，所以标识符的线性增加将导致潜在冲突的指数级增加！这是在最小可能作用域中定义标识符的关键原因之一。
让我们重新审视一个命名冲突的例子，然后展示我们如何使用命名空间来改进它。在以下示例中，
foo.cpp
和
goo.cpp
是包含执行不同操作但具有相同名称和参数的函数的源文件。
foo.cpp
// This doSomething() adds the value of its parameters
int doSomething(int x, int y)
{
    return x + y;
}
goo.cpp
// This doSomething() subtracts the value of its parameters
int doSomething(int x, int y)
{
    return x - y;
}
main.cpp
#include <iostream>

int doSomething(int x, int y); // forward declaration for doSomething

int main()
{
    std::cout << doSomething(4, 3) << '\n'; // which doSomething will we get?
    return 0;
}
如果此项目只包含
foo.cpp
或
goo.cpp
（但不能同时包含），它将编译并运行而不会出现任何问题。然而，通过将两者编译到同一个程序中，我们现在将两个具有相同名称和参数的不同函数引入到同一作用域（全局作用域）中，这会导致命名冲突。结果，链接器将发出错误
goo.cpp:3: multiple definition of `doSomething(int, int)'; foo.cpp:3: first defined here
请注意，此错误发生在重定义处，因此无论函数
doSomething
是否被调用，都无关紧要。
解决此问题的一种方法是重命名其中一个函数，这样名称就不会再冲突了。但这还需要更改所有函数调用的名称，这可能很麻烦，并且容易出错。避免冲突的更好方法是将您的函数放入您自己的命名空间中。因此，标准库被移到了
std
命名空间中。
定义您自己的命名空间
C++ 允许我们通过
namespace
关键字定义我们自己的命名空间。您在自己的程序中创建的命名空间通常称为
用户自定义命名空间
（尽管更准确的说法是
程序定义命名空间
）。
命名空间的语法如下
namespace NamespaceIdentifier
{
    // content of namespace here
}
我们以
namespace
关键字开头，后跟命名空间的标识符，然后是大括号，其中包含命名空间的内容。
历史上，命名空间名称没有大写，许多风格指南仍然推荐这种约定。
致进阶读者
偏爱以大写字母开头的命名空间名称的一些原因
程序定义的类型通常以大写字母开头命名。对程序定义的命名空间使用相同的约定是一致的（尤其是在使用限定名称（例如
Foo::x
）时，其中
Foo
可以是命名空间或类类型）。
它有助于防止与系统提供或库提供的其他小写名称发生命名冲突。
C++20 标准文档使用此样式。
C++ 核心指南文档使用此样式。
我们建议命名空间名称以大写字母开头。然而，两种样式都应该被认为是可接受的。
命名空间必须定义在全局作用域中，或定义在另一个命名空间中。与函数内容类似，命名空间内容通常缩进一级。您偶尔会看到在命名空间的右大括号后放置一个可选的分号。
这是前面示例中文件使用命名空间重写的示例
foo.cpp
namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}
goo.cpp
namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}
现在
foo.cpp
中的
doSomething()
在
Foo
命名空间中，而
goo.cpp
中的
doSomething()
在
Goo
命名空间中。让我们看看重新编译程序时会发生什么。
main.cpp
int doSomething(int x, int y); // forward declaration for doSomething

int main()
{
    std::cout << doSomething(4, 3) << '\n'; // which doSomething will we get?
    return 0;
}
答案是现在我们得到了另一个错误！
ConsoleApplication1.obj : error LNK2019: unresolved external symbol "int __cdecl doSomething(int,int)" (?doSomething@@YAHHH@Z) referenced in function _main
在这种情况下，编译器满意（通过我们的前向声明），但链接器无法在全局命名空间中找到
doSomething
的定义。这是因为我们的两个版本的
doSomething
都不再在全局命名空间中！它们现在位于各自命名空间的作用域中！
有两种不同的方法可以告诉编译器使用哪个版本的
doSomething()
，通过
作用域解析运算符
，或通过
using 语句
（我们将在本章的后续课程中讨论）。
对于后续示例，为了便于阅读，我们将示例缩减为单文件解决方案。
使用作用域解析运算符 (::) 访问命名空间
告诉编译器在特定命名空间中查找标识符的最佳方法是使用
作用域解析运算符
(::)。作用域解析运算符告诉编译器，右侧操作数指定的标识符应在左侧操作数的作用域中查找。
这是使用作用域解析运算符告诉编译器我们明确要使用
Foo
命名空间中
doSomething()
版本的示例
#include <iostream>

namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Foo
    return 0;
}
这产生了预期的结果
7
如果我们想改用
Goo
中
doSomething()
的版本
#include <iostream>

namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Goo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Goo
    return 0;
}
这会产生结果
1
作用域解析运算符很棒，因为它允许我们
显式
选择要查找的命名空间，因此没有潜在的歧义。我们甚至可以这样做
#include <iostream>

namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Foo
    std::cout << Goo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Goo
    return 0;
}
这会产生结果
7
1
使用不带名称前缀的作用域解析运算符
作用域解析运算符也可以在标识符前面使用，而不提供命名空间名称（例如
::doSomething
）。在这种情况下，标识符（例如
doSomething
）将在全局命名空间中查找。
#include <iostream>

void print() // this print() lives in the global namespace
{
	std::cout << " there\n";
}

namespace Foo
{
	void print() // this print() lives in the Foo namespace
	{
		std::cout << "Hello";
	}
}

int main()
{
	Foo::print(); // call print() in Foo namespace
	::print();    // call print() in global namespace (same as just calling print() in this case)

	return 0;
}
在上面的示例中，
::print()
的执行与我们调用不带作用域解析的
print()
相同，因此在这种情况下使用作用域解析运算符是多余的。但下一个示例将展示一个不带命名空间的作用域解析运算符可能很有用的情况。
命名空间内的标识符解析
如果在命名空间内使用标识符且未提供作用域解析，则编译器将首先尝试在该命名空间中查找匹配的声明。如果未找到匹配的标识符，编译器将按顺序检查每个包含的命名空间，以查看是否找到匹配项，最后检查全局命名空间。
#include <iostream>

void print() // this print() lives in the global namespace
{
	std::cout << " there\n";
}

namespace Foo
{
	void print() // this print() lives in the Foo namespace
	{
		std::cout << "Hello";
	}

	void printHelloThere()
	{
		print();   // calls print() in Foo namespace
		::print(); // calls print() in global namespace
	}
}

int main()
{
	Foo::printHelloThere();

	return 0;
}
这会打印
Hello there
在上面的示例中，调用
print()
时未提供作用域解析。因为
print()
的此用法在
Foo
命名空间内，所以编译器将首先查看是否可以找到
Foo::print()
的声明。由于存在一个，因此调用
Foo::print()
。
如果未找到
Foo::print()
，编译器将检查包含命名空间（在此例中为全局命名空间），以查看是否可以在其中匹配
print()
。
请注意，我们还使用不带命名空间的作用域解析运算符 (
::print()
) 来显式调用全局版本的
print()
。
命名空间内容的向前声明
在
2.11 课 -- 头文件
中，我们讨论了如何使用头文件来传播前向声明。对于命名空间内的标识符，这些前向声明也需要位于相同的命名空间内
add.h
#ifndef ADD_H
#define ADD_H

namespace BasicMath
{
    // function add() is part of namespace BasicMath
    int add(int x, int y);
}

#endif
add.cpp
#include "add.h"

namespace BasicMath
{
    // define the function add() inside namespace BasicMath
    int add(int x, int y)
    {
        return x + y;
    }
}
main.cpp
#include "add.h" // for BasicMath::add()

#include <iostream>

int main()
{
    std::cout << BasicMath::add(4, 3) << '\n';

    return 0;
}
如果
add()
的前向声明没有放在命名空间
BasicMath
中，那么
add()
将在全局命名空间中声明，编译器会抱怨它没有看到对
BasicMath::add(4, 3)
调用的声明。如果函数
add()
的定义不在命名空间
BasicMath
中，链接器会抱怨它找不到对
BasicMath::add(4, 3)
调用的匹配定义。
允许多个命名空间块
在多个位置（无论是跨多个文件，还是在同一个文件中的多个位置）声明命名空间块是合法的。命名空间内的所有声明都被视为命名空间的一部分。
circle.h
#ifndef CIRCLE_H
#define CIRCLE_H

namespace BasicMath
{
    constexpr double pi{ 3.14 };
}

#endif
growth.h
#ifndef GROWTH_H
#define GROWTH_H

namespace BasicMath
{
    // the constant e is also part of namespace BasicMath
    constexpr double e{ 2.7 };
}

#endif
main.cpp
#include "circle.h" // for BasicMath::pi
#include "growth.h" // for BasicMath::e

#include <iostream>

int main()
{
    std::cout << BasicMath::pi << '\n';
    std::cout << BasicMath::e << '\n';

    return 0;
}
这完全符合您的预期
3.14
2.7
标准库广泛使用了此特性，因为每个标准库头文件都包含在该头文件中的
namespace std
块中的声明。否则，整个标准库都必须在一个头文件中定义！
请注意，此功能也意味着您可以将自己的功能添加到
std
命名空间。这样做通常会导致未定义的行为，因为
std
命名空间有一个特殊规则，禁止用户代码扩展。
警告
不要将自定义功能添加到 std 命名空间。
嵌套命名空间
命名空间可以嵌套在其他命名空间中。例如
#include <iostream>

namespace Foo
{
    namespace Goo // Goo is a namespace inside the Foo namespace
    {
        int add(int x, int y)
        {
            return x + y;
        }
    }
}

int main()
{
    std::cout << Foo::Goo::add(1, 2) << '\n';
    return 0;
}
请注意，因为命名空间
Goo
在命名空间
Foo
内部，所以我们将其访问为
Foo::Goo::add
。
从 C++17 开始，嵌套命名空间也可以这样声明
#include <iostream>

namespace Foo::Goo // Goo is a namespace inside the Foo namespace (C++17 style)
{
    int add(int x, int y)
    {
        return x + y;
    }
}

int main()
{
    std::cout << Foo::Goo::add(1, 2) << '\n';
    return 0;
}
这与前面的示例等效。
如果您以后需要向
Foo
命名空间（仅）添加声明，您可以定义一个单独的
Foo
命名空间来这样做
#include <iostream>

namespace Foo::Goo // Goo is a namespace inside the Foo namespace (C++17 style)
{
    int add(int x, int y)
    {
        return x + y;
    }
}

namespace Foo
{
     void someFcn() {} // This function is in Foo only
}

int main()
{
    std::cout << Foo::Goo::add(1, 2) << '\n';
    return 0;
}
无论是保留单独的
Foo::Goo
定义还是将
Goo
嵌套在
Foo
中，都是一种风格选择。
命名空间别名
由于在嵌套命名空间中键入变量或函数的限定名可能很麻烦，C++ 允许您创建
命名空间别名
，这允许我们暂时将长序列的命名空间缩短
#include <iostream>

namespace Foo::Goo
{
    int add(int x, int y)
    {
        return x + y;
    }
}

int main()
{
    namespace Active = Foo::Goo; // active now refers to Foo::Goo

    std::cout << Active::add(1, 2) << '\n'; // This is really Foo::Goo::add()

    return 0;
} // The Active alias ends here
命名空间别名的一个优点：如果您想将
Foo::Goo
中的功能移动到不同的位置，您只需更新
Active
别名以反映新的目的地，而无需查找/替换
Foo::Goo
的每个实例。
#include <iostream>
 
namespace Foo::Goo
{
}

namespace V2
{
    int add(int x, int y)
    {
        return x + y;
    }
}
 
int main()
{
    namespace Active = V2; // active now refers to V2
 
    std::cout << Active::add(1, 2) << '\n'; // We don't have to change this
 
    return 0;
}
如何使用命名空间
值得注意的是，C++ 中的命名空间最初并不是为了实现信息层次结构而设计的——它们主要是作为防止命名冲突的机制而设计的。作为证据，请注意整个标准库都位于单个顶级命名空间
std
下。引入大量名称的较新标准库功能已开始使用嵌套命名空间（例如
std::ranges
）来避免
std
命名空间内的命名冲突。
为自己使用而开发的小型应用程序通常不需要放在命名空间中。但是，对于包含大量第三方库的较大型个人项目，对代码进行命名空间处理有助于防止与未正确命名空间的库发生命名冲突。
作者注
这些教程中的示例通常不会进行命名空间处理，除非我们正在说明有关命名空间的特定内容，以帮助保持示例简洁。
任何将分发给其他人的代码都应明确进行命名空间处理，以防止与集成到其中的代码发生冲突。通常一个顶级命名空间就足够了（例如
Foologger
）。作为一个额外的好处，将库代码放在命名空间中还允许用户通过使用其编辑器的自动完成和建议功能来查看您的库内容（例如，如果您键入
Foologger
，自动完成将显示
Foologger
中的所有名称）。
在多团队组织中，通常使用两级甚至三级命名空间来防止不同团队生成的代码之间的命名冲突。这些通常采用以下形式之一
项目或库 :: 模块（例如
Foologger::Lang
）
公司或组织 :: 项目或库（例如
Foosoft::Foologger
）
公司或组织 :: 项目或库 :: 模块（例如
Foosoft::Foologger::Lang
）
使用模块级命名空间有助于将将来可能可重用的代码与不可重用的应用程序特定代码分开。例如，物理和数学函数可以放入一个命名空间（例如
Math::
）。语言和本地化函数可以放入另一个命名空间（例如
Lang::
）。但是，目录结构也可以用于此目的（项目目录树中的应用程序特定代码，以及单独的共享目录树中的可重用代码）。
通常，您应该避免深度嵌套的命名空间（超过 3 级）。
相关内容
C++ 提供了其他有用的命名空间功能。我们将在本章后面的
7.14 课 -- 未命名和内联命名空间
中介绍未命名命名空间和内联命名空间。
下一课
7.3
局部变量
返回目录
上一课
7.1
复合语句（块）