# 2.9 — 命名冲突和命名空间简介

2.9 — 命名冲突和命名空间简介
Alex
2016 年 11 月 6 日，太平洋标准时间晚上 10:42
2025 年 2 月 18 日
假设你第一次开车去朋友家，地址是 Mill City 的 Front Street 245 号。到达 Mill City 后，你拿出地图，却发现 Mill City 实际上有两条不同的 Front Street，分处城镇两端！你会去哪一条？除非有额外的线索帮助你决定（例如，你记得朋友家在河边），否则你必须打电话给你的朋友寻求更多信息。因为这会造成混淆和低效（特别是对你的邮件递送员而言），所以在大多数国家，城市内的所有街道名称和门牌地址都必须是唯一的。
同样，C++ 要求所有标识符都不能有歧义。如果以编译器或链接器无法区分的方式将两个相同的标识符引入到同一个程序中，编译器或链接器将产生错误。此错误通常称为
命名冲突
（或
命名冲突
）。
如果冲突的标识符引入到同一个文件中，结果将是编译器错误。如果冲突的标识符引入到属于同一个程序的单独文件中，结果将是链接器错误。
命名冲突的示例
a.cpp
#include <iostream>

void myFcn(int x)
{
    std::cout << x;
}
main.cpp
#include <iostream>

void myFcn(int x)
{
    std::cout << 2 * x;
}

int main()
{
    return 0;
}
当编译器编译此程序时，它将独立编译
a.cpp
和
main.cpp
，并且每个文件都将顺利编译。
然而，当链接器执行时，它将链接
a.cpp
和
main.cpp
中的所有定义，并发现函数
myFcn()
的冲突定义。链接器将因此中止并报错。请注意，即使从未调用
myFcn()
，也会发生此错误！
大多数命名冲突发生在两种情况下
将两个（或更多）同名函数（或全局变量）引入到属于同一程序的单独文件中。这将导致链接器错误，如上所示。
将两个（或更多）同名函数（或全局变量）引入到同一个文件中。这将导致编译器错误。
随着程序变得越来越大，使用更多的标识符，引入命名冲突的可能性会显著增加。好消息是 C++ 提供了许多避免命名冲突的机制。局部作用域就是其中一种机制，它可以防止函数内部定义的局部变量相互冲突。但是局部作用域不适用于函数名。那么我们如何防止函数名相互冲突呢？
作用域区域
回到我们的地址类比，有两个 Front Street 之所以有问题，是因为这些街道位于同一个城市中。另一方面，如果你必须向两个地址递送邮件，一个在 Mill City 的 Front Street 245 号，另一个在 Jonesville 的 Front Street 245 号，那么就不会混淆去哪里。换句话说，城市提供了分组，使我们能够消除可能相互冲突的地址的歧义。
作用域区域
是源代码的一个区域，其中所有声明的标识符都被认为与在其他作用域中声明的名称不同（就像我们类比中的城市一样）。两个同名标识符可以在单独的作用域区域中声明，而不会导致命名冲突。但是，在给定作用域区域内，所有标识符必须是唯一的，否则将导致命名冲突。
函数体是作用域区域的一个示例。两个同名标识符可以在单独的函数中定义而不会出现问题——因为每个函数都提供一个单独的作用域区域，所以没有冲突。但是，如果您尝试在同一个函数中定义两个同名标识符，则会发生命名冲突，并且编译器会报错。
命名空间
命名空间
提供了另一种作用域区域（称为
命名空间作用域
），允许您在其中声明或定义名称以消除歧义。在命名空间中声明的名称与在其他作用域中声明的名称隔离，允许这些名称无冲突地存在。
关键见解
在作用域区域（例如命名空间）内声明的名称与在另一个作用域中声明的任何相同名称都是不同的。
例如，两个具有相同声明的函数可以在不同的命名空间中定义，并且不会发生命名冲突或歧义。
命名空间只能包含声明和定义（例如变量和函数）。除非是定义的一部分（例如在函数内部），否则不允许可执行语句。
关键见解
命名空间只能包含声明和定义。可执行语句只允许作为定义的一部分（例如，函数的定义）。
命名空间通常用于在大型项目中将相关的标识符分组，以帮助确保它们不会无意中与其他标识符冲突。例如，如果将所有数学函数放在名为
math
的命名空间中，那么您的数学函数就不会与
math
命名空间之外的同名函数冲突。
我们将在以后的课程中讨论如何创建自己的命名空间。
全局命名空间
在 C++ 中，任何未在类、函数或命名空间中定义的名称都被视为隐式定义的
全局命名空间
（有时也称为
全局作用域
）的一部分。
在本课程开头的示例中，函数
main()
和两个版本的
myFcn()
都定义在全局命名空间中。示例中遇到的命名冲突发生的原因是两个版本的
myFcn()
都最终在全局命名空间中，这违反了作用域区域中所有名称必须唯一的规则。
我们在课程
7.4 -- 全局变量简介
中更详细地讨论全局命名空间。
目前，您应该知道两件事
在全局作用域中声明的标识符从声明点到文件末尾都在作用域内。
尽管可以在全局命名空间中定义变量，但这通常应避免（我们在课程
7.8 -- 为什么（非 const）全局变量是邪恶的
中讨论原因）。
例如
#include <iostream> // imports the declaration of std::cout into the global scope

// All of the following statements are part of the global namespace

void foo();    // okay: function forward declaration
int x;         // compiles but strongly discouraged: non-const global variable definition (without initializer)
int y { 5 };   // compiles but strongly discouraged: non-const global variable definition (with initializer)
x = 5;         // compile error: executable statements are not allowed in namespaces

int main()     // okay: function definition
{
    return 0;
}

void goo();    // okay: A function forward declaration
std 命名空间
C++ 最初设计时，C++ 标准库中的所有标识符（包括 std::cin 和 std::cout）都可以不带
std::
前缀使用（它们是全局命名空间的一部分）。然而，这意味着标准库中的任何标识符都可能与您为自己的标识符选择的任何名称（也定义在全局命名空间中）发生冲突。曾经正常工作的代码在包含标准库的不同部分时可能会突然出现命名冲突。更糟的是，在一个 C++ 版本下编译的代码可能在下一个 C++ 版本下无法编译，因为引入到标准库中的新标识符可能与已编写的代码发生命名冲突。因此，C++ 将标准库中的所有功能都移到了一个名为
std
（“标准”的缩写）的命名空间中。
原来
std::cout
的名字并不是真正的
std::cout
。它实际上只是
cout
，而
std
是标识符
cout
所属的命名空间的名称。因为
cout
定义在
std
命名空间中，所以名称
cout
不会与我们在
std
命名空间之外（例如在全局命名空间中）创建的任何名为
cout
的对象或函数冲突。
关键见解
当您使用定义在非全局命名空间（例如
std
命名空间）中的标识符时，您需要告诉编译器该标识符存在于该命名空间中。”
有几种不同的方法可以做到这一点。
显式命名空间限定符 std:
告诉编译器我们要使用
std
命名空间中的
cout
的最直接方法是显式使用
std::
前缀。例如
#include <iostream>

int main()
{
    std::cout << "Hello world!"; // when we say cout, we mean the cout defined in the std namespace
    return 0;
}
::
符号是一个运算符，称为
作用域解析运算符
。
::
符号左侧的标识符标识了
::
符号右侧的名称所包含的命名空间。如果未提供
::
符号左侧的标识符，则假定为全局命名空间。
所以当我们说
std::cout
时，我们说的是“在命名空间
std
中声明的
cout
”。
这是使用
cout
最安全的方式，因为我们引用的
cout
是哪个（
std
命名空间中的那个）没有任何歧义。
最佳实践
使用显式命名空间前缀访问命名空间中定义的标识符。
当标识符包含命名空间前缀时，该标识符称为
限定名
。
使用命名空间 std（以及为何避免使用它）
访问命名空间中标识符的另一种方法是使用 using-directive 语句。这是我们带有 using-directive 的原始“Hello world”程序
#include <iostream>

using namespace std; // this is a using-directive that allows us to access names in the std namespace with no namespace prefix

int main()
{
    cout << "Hello world!";
    return 0;
}
using 指令
允许我们访问命名空间中的名称而无需使用命名空间前缀。因此，在上面的示例中，当编译器确定标识符
cout
是什么时，它将与
std::cout
匹配，由于 using 指令，
std::cout
可以直接作为
cout
访问。
许多教材、教程甚至一些 IDE 都推荐或在程序顶部使用 using-directive。但是，以这种方式使用，这是一种不好的做法，强烈不鼓励。
考虑以下程序
#include <iostream> // imports the declaration of std::cout into the global scope

using namespace std; // makes std::cout accessible as "cout"
 
int cout() // defines our own "cout" function in the global namespace
{
    return 5;
}
 
int main()
{
    cout << "Hello, world!"; // Compile error!  Which cout do we want here?  The one in the std namespace or the one we defined above?
 
    return 0;
}
上面的程序无法编译，因为编译器现在无法区分我们要的是我们定义的
cout
函数，还是
std::cout
。
以这种方式使用 using-directive 时，我们定义的
任何
标识符都可能与
std
命名空间中
任何
同名标识符冲突。更糟糕的是，虽然标识符名称今天可能不冲突，但它可能与未来语言修订版中添加到 std 命名空间的新标识符冲突。这正是最初将标准库中的所有标识符移到
std
命名空间中的全部目的！
警告
避免在程序的顶部或头文件中使用 using 指令（例如
using namespace std;
）。它们违反了最初添加命名空间的原因。
相关内容
我们将在课程
7.13 -- 使用声明和使用指令
中更详细地讨论 using 声明和 using 指令（以及如何负责任地使用它们）。
花括号和缩进代码
在 C++ 中，花括号通常用于划定嵌套在另一个作用域区域内的作用域区域（花括号也用于一些与作用域无关的用途，例如列表初始化）。例如，在全局作用域区域中定义的函数使用花括号将函数的作用域区域与全局作用域分离。
在某些情况下，在花括号外定义的标识符可能仍属于花括号定义的作用域，而不是周围的作用域——函数参数就是一个很好的例子。
例如
#include <iostream> // imports the declaration of std::cout into the global scope

void foo(int x) // foo is defined in the global scope, x is defined within scope of foo()
{ // braces used to delineate nested scope region for function foo()
    std::cout << x << '\n';
} // x goes out of scope here

int main()
{ // braces used to delineate nested scope region for function main()
    foo(5);

    int x { 6 }; // x is defined within the scope of main()
    std::cout << x << '\n';
 
    return 0;
} // x goes out of scope here
// foo and main (and std::cout) go out of scope here (the end of the file)
嵌套作用域区域内的代码通常缩进一级，既为了可读性，也为了帮助表明它存在于一个单独的作用域区域内。
#include
以及
foo()
和
main()
的函数定义存在于全局作用域区域中，因此它们不缩进。每个函数内的语句存在于函数的嵌套作用域区域中，因此它们缩进一级。
下一课
2.10
预处理器简介
返回目录
上一课
2.8
包含多个代码文件的程序