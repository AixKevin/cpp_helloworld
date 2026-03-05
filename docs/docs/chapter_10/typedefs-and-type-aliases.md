# 10.7 — Typedefs 和类型别名

10.7 — Typedefs 和类型别名
Alex
2007年6月19日，太平洋夏令时晚上9:04
2024年2月11日
类型别名
在C++中，
using
是一个关键字，用于为现有数据类型创建别名。要创建这样的类型别名，我们使用
using
关键字，后跟类型别名的名称，然后是等号和现有数据类型。例如：
using Distance = double; // define Distance as an alias for type double
一旦定义，类型别名可以在任何需要类型的地方使用。例如，我们可以使用类型别名名称作为类型来创建变量：
Distance milesToDestination{ 3.4 }; // defines a variable of type double
当编译器遇到类型别名名称时，它将替换为别名类型。例如：
#include <iostream>

int main()
{
    using Distance = double; // define Distance as an alias for type double

    Distance milesToDestination{ 3.4 }; // defines a variable of type double

    std::cout << milesToDestination << '\n'; // prints a double value

    return 0;
}
这会打印
3.4
在上面的程序中，我们首先将
Distance
定义为
double
类型的别名。
接下来，我们定义了一个名为
milesToDestination
的变量，其类型别名为
Distance
。由于编译器知道
Distance
是一个类型别名，它将使用别名类型，即
double
。因此，变量
milesToDestination
实际上被编译为
double
类型的变量，并且在所有方面都将表现为
double
。
最后，我们打印
milesToDestination
的值，它以
double
值打印。
致进阶读者
类型别名也可以模板化。我们将在课程
13.14 -- 类模板参数推导 (CTAD) 和推导指南
中介绍。
类型别名命名
历史上，类型别名的命名方式并没有很多一致性。有三种常见的命名约定（你都会遇到）：
以“_t”后缀结尾的类型别名（“_t”是“type”的缩写）。此约定通常由标准库用于全局作用域类型名称（如
size_t
和
nullptr_t
）。
这个约定继承自C语言，过去在定义自己的类型别名（有时是其他类型）时最受欢迎，但在现代C++中已不再流行。请注意，
POSIX
保留“_t”后缀用于全局作用域类型名称，因此使用此约定可能会在POSIX系统上导致类型命名冲突。
以“_type”后缀结尾的类型别名。此约定被某些标准库类型（如
std::string
）用于命名嵌套类型别名（例如
std::string::size_type
）。
但是许多这样的嵌套类型别名根本不使用后缀（例如
std::string::iterator
），因此这种用法充其量是不一致的。
不使用后缀的类型别名。
在现代C++中，约定是为你自己定义的类型别名（或任何其他类型）命名时以大写字母开头，并且不使用后缀。大写字母有助于区分类型名称与变量和函数名称（它们以小写字母开头），并防止它们之间的命名冲突。
使用此命名约定时，通常会看到这种用法：
void printDistance(Distance distance); // Distance is some defined type
在这种情况下，
Distance
是类型，
distance
是参数名称。C++区分大小写，所以这没问题。
最佳实践
将你的类型别名以大写字母开头命名，并且不要使用后缀（除非你有特殊原因）。
作者注
本教程系列中未来的一些课程仍使用“_t”或“_type”后缀。请随时在这些课程上留下评论，以便我们使其与最佳实践保持一致。
类型别名不是不同的类型
别名实际上并不定义一个新的、不同的类型（一个被认为与其他类型分离的类型）——它只是为现有类型引入了一个新的标识符。类型别名与别名类型完全可互换。
这允许我们做一些语法上有效但语义上无意义的事情。例如：
int main()
{
    using Miles = long; // define Miles as an alias for type long
    using Speed = long; // define Speed as an alias for type long

    Miles distance { 5 }; // distance is actually just a long
    Speed mhz  { 3200 };  // mhz is actually just a long

    // The following is syntactically valid (but semantically meaningless)
    distance = mhz;

    return 0;
}
尽管概念上我们希望
Miles
和
Speed
具有不同的含义，但两者都只是
long
类型的别名。这实际上意味着
Miles
、
Speed
和
long
都可以互换使用。事实上，当我们把
Speed
类型的值赋给
Miles
类型的变量时，编译器只看到我们把
long
类型的值赋给
long
类型的变量，它不会报错。
由于编译器不会阻止类型别名的这种语义错误，我们说别名不是
类型安全
的。尽管如此，它们仍然有用。
警告
必须注意不要混淆语义上应区分的别名值。
题外话…
一些语言支持
强类型定义
（或强类型别名）的概念。强类型定义实际上会创建一个新类型，它具有原始类型的所有原始属性，但是如果你尝试混合使用别名类型和强类型定义的值，编译器将抛出错误。截至C++20，C++不直接支持强类型定义（尽管枚举类，在课程
13.6 -- 作用域枚举（枚举类）
中介绍，与之类似），但有相当多的第三方C++库实现了类似强类型定义的行为。
类型别名的作用域
由于作用域是标识符的属性，类型别名标识符遵循与变量标识符相同的作用域规则：在块内部定义的类型别名具有块作用域，并且只能在该块内使用；而在全局命名空间中定义的类型别名具有全局作用域，并且可以使用到文件末尾。在上面的示例中，
Miles
和
Speed
只能在
main()
函数中使用。
如果您需要在多个文件中使用一个或多个类型别名，可以将它们定义在头文件中，并 #include 到任何需要使用定义的代码文件中：
mytypes.h
#ifndef MYTYPES_H
#define MYTYPES_H

    using Miles = long;
    using Speed = long;

#endif
以这种方式 #include 的类型别名将被导入到全局命名空间，因此具有全局作用域。
Typedefs
typedef
（“类型定义”的缩写）是一种创建类型别名的旧方法。要创建 typedef 别名，我们使用
typedef
关键字：
// The following aliases are identical
typedef long Miles;
using Miles = long;
Typedefs 仍然存在于 C++ 中，是为了向后兼容性，但在现代 C++ 中它们已被类型别名取代。
Typedefs 有一些语法问题。首先，很容易忘记 typedef 的名称和要别名的类型的名称哪个在前。哪个是正确的？
typedef Distance double; // incorrect (typedef name first)
typedef double Distance; // correct (aliased type name first)
很容易弄反。幸运的是，在这种情况下，编译器会报错。
其次，对于更复杂的类型，typedef 的语法会变得很丑陋。例如，这是一个难以阅读的 typedef，以及一个等效的（并且稍微更容易阅读的）类型别名：
typedef int (*FcnType)(double, char); // FcnType hard to find
using FcnType = int(*)(double, char); // FcnType easier to find
在上面的 typedef 定义中，新类型的名称（
FcnType
）埋藏在定义的中间，而在类型别名中，新类型的名称和定义的其余部分由等号分隔。
第三，“typedef”这个名字暗示正在定义一个新类型，但这不属实。一个 typedef 只是一个别名。
最佳实践
优先使用类型别名而不是 typedef。
命名法
C++标准将 typedefs 和类型别名的名称都称为“typedef 名称”。
在常规语言中，“typedef”一词通常用来指“typedef 或类型别名”，因为它们实际上做的是同样的事情。
我们什么时候应该使用类型别名？
现在我们已经介绍了类型别名是什么，让我们来谈谈它们的用途。
使用类型别名进行平台无关编程
类型别名的主要用途之一是隐藏平台特定的细节。在某些平台上，一个
int
是 2 字节，而在另一些平台上是 4 字节。因此，在编写平台无关代码时，使用
int
存储超过 2 字节的信息可能存在潜在危险。
由于
char
、
short
、
int
和
long
没有指示它们的大小，因此跨平台程序通常使用类型别名来定义包含类型大小（以位为单位）的别名。例如，
int8_t
将是一个 8 位有符号整数，
int16_t
是一个 16 位有符号整数，而
int32_t
是一个 32 位有符号整数。以这种方式使用类型别名有助于防止错误，并更清楚地说明对变量大小做出了何种假设。
为了确保每个别名类型解析为正确大小的类型，此类类型别名通常与预处理器指令结合使用：
#ifdef INT_2_BYTES
using int8_t = char;
using int16_t = int;
using int32_t = long;
#else
using int8_t = char;
using int16_t = short;
using int32_t = int;
#endif
在整数仅为 2 字节的机器上，可以 #define
INT_2_BYTES
（作为编译器/预处理器设置），程序将使用顶部的一组类型别名进行编译。在整数为 4 字节的机器上，不定义
INT_2_BYTES
将导致使用底部的一组类型别名。通过这种方式，只要正确 #define 了
INT_2_BYTES
，
int8_t
将解析为 1 字节整数，
int16_t
将解析为 2 字节整数，
int32_t
将解析为 4 字节整数（使用
char
、
short
、
int
和
long
的组合，适用于程序编译的机器）。
固定宽度整数类型（如
std::int16_t
和
std::uint32_t
）和
size_t
类型（两者都在课程
4.6 -- 固定宽度整数和 size_t
中介绍）实际上只是各种基本类型的类型别名。
这也是为什么当您使用
std::cout
打印一个 8 位固定宽度整数时，您可能会得到一个字符值。例如：
#include <cstdint> // for fixed-width integers
#include <iostream>

int main()
{
    std::int8_t x{ 97 }; // int8_t is usually a typedef for signed char
    std::cout << x << '\n';

    return 0;
}
这个程序打印
a
因为
std::int8_t
通常是
signed char
的 typedef，所以变量
x
很可能会被定义为
signed char
。而字符类型会将其值打印为 ASCII 字符而不是整数值。
使用类型别名使复杂类型更易于阅读
尽管到目前为止我们只处理了简单的数据类型，但在高级C++中，类型可能很复杂且手动输入起来很长。例如，您可能会看到函数和变量定义如下：
#include <string> // for std::string
#include <vector> // for std::vector
#include <utility> // for std::pair

bool hasDuplicates(std::vector<std::pair<std::string, int>> pairlist)
{
    // some code here
    return false;
}

int main()
{
     std::vector<std::pair<std::string, int>> pairlist;

     return 0;
}
在所有需要使用该类型的地方都输入
std::vector<std::pair<std::string, int>>
既繁琐又容易打错。使用类型别名会方便得多：
#include <string> // for std::string
#include <vector> // for std::vector
#include <utility> // for std::pair

using VectPairSI = std::vector<std::pair<std::string, int>>; // make VectPairSI an alias for this crazy type

bool hasDuplicates(VectPairSI pairlist) // use VectPairSI in a function parameter
{
    // some code here
    return false;
}

int main()
{
     VectPairSI pairlist; // instantiate a VectPairSI variable

     return 0;
}
好多了！现在我们只需输入
VectPairSI
而不是
std::vector<std::pair<std::string, int>>
。
如果您还不了解
std::vector
、
std::pair
或所有这些奇怪的尖括号，请不要担心。您真正需要理解的是，类型别名允许您采用复杂类型并为其赋予一个更简单的名称，这使您的代码更易于阅读并节省了打字时间。
这可能是类型别名的最佳用途。
使用类型别名记录值的含义
类型别名也有助于代码文档和理解。
对于变量，我们有变量的标识符来帮助记录变量的用途。但考虑函数返回值的情况。像
char
、
int
、
long
、
double
和
bool
这样的数据类型描述了函数返回值的
类型
，但我们更常想知道返回值的
含义
。
例如，给定以下函数：
int gradeTest();
我们可以看到返回值是一个整数，但这个整数是什么意思呢？一个字母等级？错题的数量？学生的ID号？一个错误代码？谁知道呢！
int
的返回类型没有告诉我们太多。如果幸运的话，该函数的一些文档存在我们可以参考。如果运气不好，我们必须阅读代码并推断其目的。
现在让我们做一个等效的版本，使用类型别名：
using TestScore = int;
TestScore gradeTest();
TestScore
的返回类型使得函数返回一个表示测试分数的类型变得更明显。
根据我们的经验，仅仅为了记录单个函数的返回类型而创建类型别名是不值得的（而是使用注释）。但是，如果您有多个函数传递或返回这种类型，那么创建类型别名可能是值得的。
使用类型别名简化代码维护
类型别名还允许您更改对象的底层类型，而无需更新大量硬编码类型。例如，如果您曾经使用
short
来存储学生的 ID 号，但后来决定需要
long
，您将不得不遍历大量代码并将
short
替换为
long
。这可能很难弄清楚哪些
short
类型的对象用于存储 ID 号，哪些用于其他目的。
但是，如果您使用类型别名，那么更改类型就变得像更新类型别名一样简单（例如，从
using StudentId = short;
到
using StudentId = long;
）。
虽然这看起来是一个很好的优点，但更改类型时需要谨慎，因为程序的行为也可能随之改变。当将类型别名的类型更改为不同类型家族中的类型时（例如，整数更改为浮点值，或有符号更改为无符号值），这一点尤其如此！新类型可能存在旧类型没有的比较或整数/浮点除法问题，或其它问题。如果您将现有类型更改为其他类型，您的代码应该进行彻底的重新测试。
缺点与结论
虽然类型别名提供了一些好处，但它们也在你的代码中引入了另一个需要理解的标识符。如果这不能通过提高可读性或理解性来抵消，那么类型别名弊大于利。
一个使用不当的类型别名可以隐藏一个熟悉的类型（如
std::string
）在一个需要查找的自定义名称后面。在某些情况下（例如智能指针，我们将在未来的章节中介绍），模糊类型信息也可能有害于理解该类型应如何工作。
因此，类型别名应主要用于对代码可读性或代码维护有明显益处的情况。这既是一门艺术，也是一门科学。类型别名在代码中许多地方都可以使用时最有益，而不是在少数地方。
最佳实践
明智地使用类型别名，当它们能为代码可读性或代码维护带来明显好处时。
小测验时间
问题 #1
给定以下函数原型：
int printData();
将
int
返回值转换为名为
PrintError
的类型别名。包括类型别名语句和更新后的函数原型。
显示答案
using PrintError = int;

PrintError printData();
下一课
10.8
使用auto关键字的对象类型推断
返回目录
上一课
10.6
显式类型转换（casting）和static_cast