# 2.11 — 头文件

2.11 — 头文件
Alex
2007 年 6 月 3 日，上午 9:29 PDT
2025 年 2 月 27 日
在课程
2.8 -- 包含多个代码文件的程序
中，我们讨论了程序如何分割成多个文件。我们还讨论了如何使用前向声明来允许一个文件中的代码访问在另一个文件中定义的内容。
当程序只包含少量文件时，手动在每个文件顶部添加几个前向声明并不会太麻烦。然而，随着程序变得越来越大（并使用更多的文件和函数），不得不手动在每个文件顶部添加大量（可能不同）的前向声明会变得非常繁琐。例如，如果你的程序有 5 个文件，每个文件需要 10 个前向声明，那么你将不得不复制/粘贴 50 个前向声明。现在考虑一下你有 100 个文件，每个文件需要 100 个前向声明的情况。这简直无法扩展！
为了解决这个问题，C++ 程序通常采用不同的方法。
头文件
C++ 代码文件（扩展名为 .cpp）并不是 C++ 程序中常见的唯一文件。另一种类型的文件称为
头文件
。头文件通常使用 .h 扩展名，但偶尔你也会看到它们使用 .hpp 扩展名或根本没有扩展名。
通常，头文件用于将一批相关的前向声明传播到代码文件中。
关键见解
头文件允许我们将声明放在一个地方，然后在需要它们的地方导入它们。这在多文件程序中可以节省大量打字工作。
使用标准库头文件
考虑以下程序
#include <iostream>

int main()
{
    std::cout << "Hello, world!";
    return 0;
}
此程序使用
std::cout
将“Hello, world!”打印到控制台。然而，此程序从未为
std::cout
提供定义或声明，那么编译器如何知道
std::cout
是什么？
答案是
std::cout
已在“iostream”头文件中前向声明。当我们
#include <iostream>
时，我们要求预处理器将名为“iostream”文件中的所有内容（包括 std::cout 的前向声明）复制到执行 #include 的文件中。
关键见解
当你
#include
一个文件时，被包含文件的内容会插入到包含点。这提供了一种从另一个文件引入声明的有用方法。
考虑如果
iostream
头文件不存在会发生什么。无论你在哪里使用
std::cout
，你都必须手动输入或复制所有与
std::cout
相关的声明到每个使用
std::cout
的文件顶部！这将需要大量关于
std::cout
如何声明的知识，并且会是一项繁重的工作。更糟糕的是，如果函数原型被添加或更改，我们必须手动更新所有前向声明。
只需
#include <iostream>
即可轻松解决！
使用头文件传播前向声明
现在让我们回到我们上一课中讨论的例子。我们当时有两个文件，
add.cpp
和
main.cpp
，它们看起来像这样
add.cpp
int add(int x, int y)
{
    return x + y;
}
main.cpp
#include <iostream>

int add(int x, int y); // forward declaration using function prototype

int main()
{
    std::cout << "The sum of 3 and 4 is " << add(3, 4) << '\n';
    return 0;
}
（如果你从头开始重新创建此示例，请不要忘记将
add.cpp
添加到你的项目中以便它被编译）。
在此示例中，我们使用了一个前向声明，以便编译器在编译
main.cpp
时知道标识符
add
是什么。如前所述，手动为每个你想使用的、位于另一个文件中的函数添加前向声明会很快变得繁琐。
让我们编写一个头文件来减轻这个负担。编写头文件出奇地容易，因为头文件只包含两部分
一个
头文件保护
，我们将在下一课中更详细地讨论它（
2.12 -- 头文件保护
）。
头文件的实际内容，它应该是所有我们希望其他文件能够看到的标识符的前向声明。
将头文件添加到项目的工作方式类似于添加源文件（在课程
2.8 -- 包含多个代码文件的程序
中介绍）。
如果使用 IDE，请执行相同的步骤并在询问时选择“Header”而不是“Source”。头文件应作为项目的一部分出现。
如果使用命令行，只需在你喜欢的编辑器中，在与源 (.cpp) 文件相同的目录中创建一个新文件。与源文件不同，头文件不应添加到你的编译命令中（它们通过 #include 语句隐式包含并作为源文件的一部分编译）。
最佳实践
在命名头文件时首选 .h 后缀（除非你的项目已经遵循其他约定）。
这是 C++ 头文件的长期约定，大多数 IDE 仍然默认使用 .h 而不是其他选项。
头文件通常与代码文件配对，头文件为相应的代码文件提供前向声明。由于我们的头文件将包含在
add.cpp
中定义的函数的前向声明，因此我们将新头文件命名为
add.h
。
最佳实践
如果头文件与代码文件配对（例如 add.h 与 add.cpp），它们都应该具有相同的基本名称（add）。
这是我们完成的头文件
add.h
// We really should have a header guard here, but will omit it for simplicity (we'll cover header guards in the next lesson)

// This is the content of the .h file, which is where the declarations go
int add(int x, int y); // function prototype for add.h -- don't forget the semicolon!
为了在 main.cpp 中使用此头文件，我们必须 #include 它（使用引号，而不是尖括号）。
main.cpp
#include "add.h" // Insert contents of add.h at this point.  Note use of double quotes here.
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is " << add(3, 4) << '\n';
    return 0;
}
add.cpp
#include "add.h" // Insert contents of add.h at this point.  Note use of double quotes here.

int add(int x, int y)
{
    return x + y;
}
当预处理器处理
#include "add.h"
行时，它会将 add.h 的内容复制到当前文件中该点。因为我们的
add.h
包含函数
add()
的前向声明，所以该前向声明将被复制到
main.cpp
中。最终结果是程序在功能上与我们手动将前向声明添加到
main.cpp
顶部时的程序相同。
因此，我们的程序将正确编译和链接。
注意：在上面的图中，“Standard Runtime Library”应标记为“C++ Standard Library”。
在头文件中包含定义如何导致违反单一定义规则
目前，你应该避免在头文件中放置函数或变量定义。这样做通常会导致在头文件包含到多个源文件中的情况下违反单一定义规则（ODR）。
相关内容
我们在课程
2.7 -- 前向声明和定义
中介绍了单一定义规则（ODR）。
让我们说明这是如何发生的
add.h
// We really should have a header guard here, but will omit it for simplicity (we'll cover header guards in the next lesson)

// definition for add() in header file -- don't do this!
int add(int x, int y)
{
    return x + y;
}
main.cpp
#include "add.h" // Contents of add.h copied here
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is " << add(3, 4) << '\n';

    return 0;
}
add.cpp
#include "add.h" // Contents of add.h copied here
当
main.cpp
被编译时，
#include "add.h"
将被
add.h
的内容替换，然后进行编译。因此，编译器将编译如下所示的内容
main.cpp (预处理后)
// from add.h:
int add(int x, int y)
{
    return x + y;
}

// contents of iostream header here

int main()
{
    std::cout << "The sum of 3 and 4 is " << add(3, 4) << '\n';

    return 0;
}
这将正常编译。
当编译器编译
add.cpp
时，
#include "add.h"
将被
add.h
的内容替换，然后进行编译。因此，编译器将编译如下所示的内容
add.cpp (预处理后)
int add(int x, int y)
{
    return x + y;
}
这也将正常编译。
最后，链接器将运行。链接器将看到函数
add()
现在有两个定义：一个在 main.cpp 中，一个在 add.cpp 中。这违反了 ODR 第 2 部分，该部分规定：“在一个给定的程序中，一个变量或普通函数只能有一个定义。”
最佳实践
（目前）不要在头文件中放置函数和变量定义。
如果在头文件中定义这些内容，并且该头文件被 #include 到多个源 (.cpp) 文件中，则很可能导致违反单一定义规则 (ODR)。
作者注
在未来的课程中，我们将遇到其他类型的定义，它们可以安全地定义在头文件中（因为它们不受 ODR 的限制）。这包括内联函数、内联变量、类型和模板的定义。我们将在介绍这些内容时进一步讨论。
源文件应包含其配对的头文件
在 C++ 中，最佳实践是代码文件应 #include 其配对的头文件（如果存在）。这允许编译器在编译时而不是链接时捕获某些类型的错误。例如
add.h
// We really should have a header guard here, but will omit it for simplicity (we'll cover header guards in the next lesson)

int add(int x, int y);
main.cpp
#include "add.h"
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is " << add(3, 4) << '\n';
    return 0;
}
add.cpp
#include "add.h"         // copies forward declaration from add.h here

double add(int x, int y) // oops, return type is double instead of int
{
    return x + y;
}
当
add.cpp
被编译时，前向声明
int add(int x, int y)
将在 #include 处复制到
add.cpp
中。当编译器遇到定义
double add(int x, int y)
时，它将注意到前向声明和定义的返回类型不匹配。由于函数不能仅通过返回类型不同，编译器将报错并立即中止编译。在大型项目中，这可以节省大量时间并帮助找出问题所在。
题外话…
不幸的是，如果参数类型不同而不是返回类型，则此方法不起作用。这是因为 C++ 支持重载函数（同名但参数类型不同的函数），因此编译器会假定参数类型不匹配的函数是不同的重载。不可能全部都赢。
如果不存在
#include "add.h"
，编译器将不会捕获该问题，因为它看不到不匹配。我们必须等到链接时才能发现该问题。
我们还将在未来的课程中看到许多示例，其中源文件所需的内容是在配对的头文件中定义的。在这种情况下，包含头文件是必要的。
最佳实践
源文件应 #include 其配对的头文件（如果存在）。
不要 #include .cpp 文件
尽管预处理器会很乐意这样做，但你通常不应该
#include
.cpp 文件。这些文件应该添加到你的项目并进行编译。
这有几个原因
这样做可能会导致源文件之间的命名冲突。
在大型项目中，很难避免单一定义规则 (ODR) 问题。
对这样的 .cpp 文件的任何更改都将导致 .cpp 文件和任何包含它的其他 .cpp 文件重新编译，这可能需要很长时间。头文件通常比源文件更改的频率低。
这样做是不符合惯例的。
最佳实践
避免 #include .cpp 文件。
提示
如果你的项目不 #include .cpp 文件就无法编译，这意味着这些 .cpp 文件没有作为你项目的一部分进行编译。将它们添加到你的项目或命令行中，以便它们被编译。
故障排除
如果你收到编译器错误，指出找不到
add.h
，请确保文件确实名为
add.h
。根据你创建和命名它的方式，文件可能被命名为
add
（无扩展名）或
add.h.txt
或
add.hpp
。还要确保它与你的其余代码文件位于同一目录中。
如果你收到链接器错误，指出函数
add
未定义，请确保你已将
add.cpp
包含在你的项目中，以便函数
add
的定义可以链接到程序中。
尖括号 vs 双引号
你可能很好奇为什么我们对
iostream
使用尖括号，而对
add.h
使用双引号。这可能是因为在多个目录中可能存在同名的头文件。我们使用尖括号与双引号有助于为预处理器提供关于它应该在哪里查找头文件的线索。
当我们使用尖括号时，我们告诉预处理器这是一个我们没有自己编写的头文件。预处理器将仅在
include directories
指定的目录中搜索头文件。
include directories
是作为您的项目/IDE 设置/编译器设置的一部分进行配置的，通常默认为包含您的编译器和/或操作系统附带的头文件的目录。预处理器将不会在您的项目源代码目录中搜索头文件。
当我们使用双引号时，我们告诉预处理器这是一个我们自己编写的头文件。预处理器将首先在当前目录中搜索头文件。如果它在那里找不到匹配的头文件，它将接着搜索
include directories
。
规则
使用双引号来包含你编写的或预计在当前目录中找到的头文件。使用尖括号来包含你的编译器、操作系统或你安装在系统其他位置的第三方库所附带的头文件。
为什么 iostream 没有 .h 扩展名？
另一个常见问题是“为什么 iostream（或任何其他标准库头文件）没有 .h 扩展名？”。答案是
iostream.h
与
iostream
是不同的头文件！解释这需要简短的历史课。
C++ 最初创建时，标准库中的所有头文件都以
.h
后缀结尾。这些头文件包括
头文件类型
命名约定
示例
放置在命名空间中的标识符
C++ 特有
<xxx.h>
iostream.h
全局命名空间
C 兼容性
<xxx.h>
stddef.h
全局命名空间
cout 和 cin 的原始版本是在
iostream.h
中声明在全局命名空间中的。生活是一致的，而且很好。
当语言被 ANSI 委员会标准化时，他们决定将标准库中使用的所有名称移到
std
命名空间中，以帮助避免与用户声明的标识符发生命名冲突。然而，这带来了一个问题：如果他们将所有名称移到
std
命名空间中，所有旧程序（包含 iostream.h）将不再工作！
为了解决这个问题，C++ 引入了不带
.h
扩展名的新头文件。这些新头文件在
std
命名空间内声明所有名称。这样，包含
#include <iostream.h>
的旧程序无需重写，而新程序可以
#include <iostream>
。
现代 C++ 现在包含 4 组头文件
头文件类型
命名约定
示例
放置在命名空间中的标识符
C++ 特有（新）
<xxx>
iostream
std
命名空间
C 兼容性（新）
<cxxx>
cstddef
std
命名空间（必需）
全局命名空间（可选）
C++ 特有（旧）
<xxx.h>
iostream.h
全局命名空间
C 兼容性（旧）
<xxx.h>
stddef.h
全局命名空间（必需）
std
命名空间（可选）
警告
新的 C 兼容头文件 <cxxx> 可选择在全局命名空间中声明名称，而旧的 C 兼容头文件 <xxx.h> 可选择在
std
命名空间中声明名称。应避免在这些位置使用名称，因为这些名称可能不会在其他实现中声明。
最佳实践
使用不带 .h 扩展名的标准库头文件。用户定义的头文件仍应使用 .h 扩展名。
包含其他目录中的头文件
另一个常见问题是如何包含其他目录中的头文件。
一种（不好）的方法是在 #include 行中包含要包含的头文件的相对路径。例如
#include "headers/myHeader.h"
#include "../moreHeaders/myOtherHeader.h"
虽然这可以编译（假设文件存在于这些相对目录中），但这种方法的缺点是它要求你在代码中反映你的目录结构。如果你更新了目录结构，你的代码将不再起作用。
更好的方法是告诉你的编译器或 IDE，你在一​​些其他位置有一堆头文件，这样当它在当前目录中找不到它们时，它就会在那里查找。这通常可以通过在你的 IDE 项目设置中设置
include path
或
search directory
来完成。
对于 Visual Studio 用户
在“解决方案资源管理器”中右键单击你的项目，然后选择“属性”，接着是“VC++ 目录”选项卡。在这里，你将看到一行名为“包含目录”。在这里添加你希望编译器搜索额外头文件的目录。
对于 Code::Blocks 用户
在 Code::Blocks 中，转到“项目”菜单并选择“构建选项”，然后选择“搜索目录”选项卡。在那里添加你希望编译器搜索额外头文件的目录。
对于 gcc 用户
使用 g++，你可以使用 -I 选项指定另一个包含目录
g++ -o main -I./source/includes main.cpp
-I
后面没有空格。对于完整路径（而不是相对路径），删除
-I
后面的
.
。
对于 VS Code 用户
在你的
tasks.json
配置文件中，在
“Args”
部分添加新行
"-I./source/includes",
-I
后面没有空格。对于完整路径（而不是相对路径），删除
-I
后面的
.
。
这种方法的好处是，如果你更改了目录结构，你只需更改一个编译器或 IDE 设置，而无需更改每个代码文件。
头文件可能包含其他头文件
头文件的内容通常会使用在另一个头文件中声明（或定义）的内容。发生这种情况时，头文件应 #include 包含其所需声明（或定义）的其他头文件。
Foo.h
#include <string_view> // required to use std::string_view

std::string_view getApplicationName(); // std::string_view used here
传递包含
当你的源 (.cpp) 文件 #include 一个头文件时，你也会得到该头文件 #include 的任何其他头文件（以及这些头文件包含的任何头文件，依此类推）。这些额外的头文件有时被称为
传递包含
，因为它们是隐式而不是显式包含的。
这些传递包含的内容可用于你的代码文件中。然而，你通常不应该依赖于传递包含的头文件的内容（除非参考文档表明这些传递包含是必需的）。头文件的实现可能会随时间变化，或者在不同的系统上有所不同。如果发生这种情况，你的代码可能只能在某些系统上编译，或者现在可以编译但将来不行。通过显式包含你的代码文件所需的所有头文件，可以轻松避免这种情况。
最佳实践
每个文件都应显式 #include 所有编译所需头文件。不要依赖通过其他头文件传递包含的头文件。
不幸的是，目前没有简单的方法可以检测你的代码文件何时意外地依赖于已被其他头文件包含的头文件的内容。
问：我没有包含 <someheader>，但我的程序仍然可以运行！为什么？
这是本网站上最常见的问题之一。答案是：它很可能有效，因为你包含了其他一些头文件（例如 <iostream>），而该头文件本身又包含了 <someheader>。尽管你的程序会编译，但根据上述最佳实践，你不应该依赖于此。对你而言可以编译的代码，可能无法在朋友的机器上编译。
头文件的包含顺序
如果你的头文件编写得当，并且 #include 了所有需要的东西，那么包含顺序应该无关紧要。
现在考虑以下场景：假设头文件 A 需要头文件 B 中的声明，但忘记包含它。在我们的代码文件中，如果我们在头文件 A 之前包含头文件 B，我们的代码仍然会编译！这是因为编译器会在编译 A 中依赖 B 的声明的代码之前，先编译 B 中的所有声明。
然而，如果我们先包含头文件 A，那么编译器会抱怨，因为 A 中的代码会在编译器看到 B 中的声明之前被编译。这实际上是更可取的，因为错误已经浮现，我们可以修复它。
最佳实践
为了最大限度地提高编译器标记缺失包含的可能性，请按以下顺序（跳过不相关的任何）排列你的 #include：
此代码文件的配对头文件（例如
add.cpp
应
#include "add.h"
）
来自同一项目的其他头文件（例如
#include "mymath.h"
）
第三方库头文件（例如
#include <boost/tuple/tuple.hpp>
）
标准库头文件（例如
#include <iostream>
）
每个分组的头文件应按字母顺序排序（除非第三方库的文档另有指示）。
这样，如果你的某个用户定义的头文件缺少对第三方库或标准库头文件的 #include，则更有可能导致编译错误，以便你可以修复它。
头文件最佳实践
以下是关于创建和使用头文件的更多建议。
始终包含头文件保护（我们将在下一课中介绍）。
（目前）不要在头文件中定义变量和函数。
给头文件与它关联的源文件相同的名称（例如，
grades.h
与
grades.cpp
配对）。
每个头文件都应该有一个特定的任务，并且尽可能独立。例如，你可以将所有与功能 A 相关的声明放在 A.h 中，将所有与功能 B 相关的声明放在 B.h 中。这样，如果你以后只关心 A，你就可以只包含 A.h，而不会引入任何与 B 相关的内容。
请注意你的代码文件中需要显式包含哪些头文件才能使用其功能，以避免无意中引入传递包含。
头文件应 #include 包含其所需功能的任何其他头文件。当它被单独 #include 到 .cpp 文件中时，这样的头文件应该能成功编译。
只 #include 你需要的东西（不要仅仅因为可以就包含所有东西）。
不要 #include .cpp 文件。
优先将有关某个功能的作用或使用方法的文档放在头文件中。这样更容易被看到。描述某个功能如何工作的文档应保留在源文件中。
下一课
2.12
头文件保护
返回目录
上一课
2.10
预处理器简介