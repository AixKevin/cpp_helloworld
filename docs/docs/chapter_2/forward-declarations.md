# 2.7 — 前向声明和定义

2.7 — 前向声明和定义
Alex
2007 年 6 月 2 日，太平洋夏令时下午 3:01
2025 年 1 月 3 日
看看这个看似无害的示例程序
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}

int add(int x, int y)
{
    return x + y;
}
你期望这个程序会产生以下结果
The sum of 3 and 4 is: 7
但实际上，它根本无法编译！Visual Studio 产生以下编译错误
add.cpp(5) : error C3861: 'add': identifier not found
这个程序无法编译的原因是编译器按顺序编译代码文件内容。当编译器到达
main
函数的第 5 行的函数调用
add()
时，它不知道
add
是什么，因为我们直到第 9 行才定义
add
！这就产生了错误：
未找到标识符
。
旧版本的 Visual Studio 会产生一个额外的错误
add.cpp(9) : error C2365: 'add'; : redefinition; previous definition was 'formerly unknown identifier'
这有点误导人，因为
add
从未被定义过。尽管如此，通常需要注意的是，单个错误产生许多冗余或相关错误或警告是相当常见的。有时很难判断第一个错误或警告之外的任何错误或警告是第一个问题导致的，还是需要单独解决的独立问题。
最佳实践
解决程序中的编译错误或警告时，请解决列出的第一个问题，然后再次编译。
为了解决这个问题，我们需要处理编译器不知道 add 是什么的事实。有两种常见的方法来解决这个问题。
选项 1：重新排序函数定义
解决这个问题的一种方法是重新排序函数定义，以便在
main
之前定义
add
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}
这样，当
main
调用
add
时，编译器就已经知道
add
是什么了。因为这是一个如此简单的程序，所以这种更改相对容易。然而，在一个更大的程序中，试图找出哪些函数调用了哪些其他函数（以及以什么顺序）以便它们可以按顺序声明可能会很繁琐。
此外，这个选项并非总是可行。假设我们正在编写一个包含两个函数
A
和
B
的程序。如果函数
A
调用函数
B
，而函数
B
调用函数
A
，那么就无法以使编译器满意的方式排列函数。如果你先定义
A
，编译器会抱怨它不知道
B
是什么。如果你先定义
B
，编译器会抱怨它不知道
A
是什么。
选项 2：使用前向声明
我们也可以通过使用前向声明来解决这个问题。
前向声明
允许我们在实际定义标识符之前告诉编译器标识符的存在。
对于函数而言，这允许我们在定义函数体之前告诉编译器函数的存在。这样，当编译器遇到对函数的调用时，它会理解我们正在进行函数调用，并且可以检查以确保我们正确调用函数，即使它还不知道函数是如何或在哪里定义的。
要为函数编写前向声明，我们使用
函数声明
语句（也称为
函数原型
）。函数声明由函数的返回类型、名称和参数类型组成，以分号结尾。参数的名称可以可选地包含。函数体不包含在声明中。
这是
add
函数的函数声明
int add(int x, int y); // function declaration includes return type, name, parameters, and semicolon.  No function body!
现在，这是我们原始的无法编译的程序，使用函数声明作为函数
add
的前向声明
#include <iostream>

int add(int x, int y); // forward declaration of add() (using a function declaration)

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n'; // this works because we forward declared add() above
    return 0;
}

int add(int x, int y) // even though the body of add() isn't defined until here
{
    return x + y;
}
现在，当编译器到达 main 中对
add
的调用时，它将知道
add
的样子（一个接受两个整数参数并返回一个整数的函数），并且它不会抱怨。
值得注意的是，函数声明不需要指定参数的名称（因为它们不被认为是函数声明的一部分）。在上面的代码中，你也可以像这样前向声明你的函数
int add(int, int); // valid function declaration
然而，我们更倾向于命名参数（使用与实际函数相同的名称）。这允许你只需查看声明即可理解函数参数是什么。例如，如果你看到声明
void doSomething(int, int, int)
，你可能会认为你记得每个参数代表什么，但你也可能会弄错。
此外，许多自动化文档生成工具会从头文件的内容生成文档，声明通常就放在那里。我们在课程
2.11 -- 头文件
中讨论头文件和声明。
最佳实践
在你的函数声明中保留参数名称。
提示
你可以通过复制/粘贴函数头并添加分号来轻松创建函数声明。
为什么使用前向声明？
你可能想知道，如果我们可以简单地重新排序函数来使我们的程序工作，为什么还要使用前向声明。
最常见的情况是，前向声明用于告诉编译器在不同代码文件中定义了某个函数。在这种情况下无法重新排序，因为调用者和被调用者完全在不同的文件中！我们将在下一课中更详细地讨论这一点（
2.8 -- 包含多个代码文件的程序
）。
前向声明还可以用于以与顺序无关的方式定义我们的函数。这允许我们以最大化组织性（例如，通过将相关函数分组）或读者理解的方式定义函数。
不常见的情况是，有时我们有两个函数互相调用。在这种情况下也无法重新排序，因为无法以使每个函数都在另一个函数之前的方式重新排序函数。前向声明为我们提供了一种解决此类循环依赖关系的方法。
忘记函数体
新程序员经常想知道如果他们前向声明一个函数但没有定义它会发生什么。
答案是：视情况而定。如果进行了前向声明，但从未使用过该函数，则程序将编译并正常运行。然而，如果进行了前向声明并且调用了该函数，但程序从未定义该函数，则程序将正常编译，但链接器会抱怨无法解析函数调用。
考虑以下程序
#include <iostream>

int add(int x, int y); // forward declaration of add()

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}

// note: No definition for function add
在这个程序中，我们前向声明了
add
，并且我们调用了
add
，但我们从未在任何地方定义
add
。当我们尝试编译这个程序时，Visual Studio 会产生以下消息
Compiling...
add.cpp
Linking...
add.obj : error LNK2001: unresolved external symbol "int __cdecl add(int,int)" (?add@@YAHHH@Z)
add.exe : fatal error LNK1120: 1 unresolved externals
如你所见，程序编译正常，但在链接阶段失败了，因为
int add(int, int)
从未定义。
其他类型的前向声明
前向声明最常用于函数。然而，前向声明也可以用于 C++ 中的其他标识符，例如变量和类型。变量和类型有不同的前向声明语法，所以我们将在未来的课程中介绍这些。
声明与定义
在 C++ 中，你经常会听到“声明”和“定义”这两个词，并且经常互换使用。它们是什么意思？你现在已经有了足够的知识来理解两者之间的区别。
声明
告诉
编译器
标识符的
存在
及其相关的类型信息。以下是一些声明的例子
int add(int x, int y); // tells the compiler about a function named "add" that takes two int parameters and returns an int.  No body!
int x;                 // tells the compiler about an integer variable named x
定义
是实际实现（对于函数和类型）或实例化（对于变量）标识符的声明。
以下是一些定义的例子
// because this function has a body, it is an implementation of function add()
int add(int x, int y)
{
    int z{ x + y };   // instantiates variable z

    return z;
}

int x;                // instantiates variable x
在 C++ 中，所有定义都是声明。因此
int x;
既是定义也是声明。
反之，并非所有声明都是定义。不是定义的声明称为
纯声明
。纯声明的类型包括函数、变量和类型的前向声明。
命名法
在一般语言中，“声明”一词通常指“纯声明”，而“定义”一词指“同时作为声明的定义”。因此，我们通常称
int x;
为定义，即使它既是定义又是声明。
当编译器遇到一个标识符时，它会检查以确保该标识符的使用是有效的（例如，标识符在作用域内，它以语法有效的方式使用等）。
在大多数情况下，声明足以让编译器确保标识符被正确使用。例如，当编译器遇到函数调用
add(5, 6)
时，如果它已经看到了
add(int, int)
的声明，那么它可以验证
add
实际上是一个接受两个
int
参数的函数。它不需要实际看到函数
add
的定义（该定义可能存在于其他文件中）。
然而，在少数情况下，编译器必须能够看到完整的定义才能使用标识符（例如模板定义和类型定义，这两种我们将在未来的课程中讨论）。
以下是汇总表
术语
技术含义
示例
声明
告诉编译器一个标识符及其相关的类型信息。
void foo(); // 函数前向声明（无函数体）
void goo() {}; // 函数定义（有函数体）
int x; // 变量定义
定义
实现一个函数或实例化一个变量。
定义也是声明。
void foo() { } // 函数定义（有函数体）
int x; // 变量定义
纯声明
不是定义的声明。
void foo(); // 函数前向声明（无函数体）
初始化
为已定义的对象提供一个初始值。
int x { 2 }; // x 初始化为值 2
“声明”一词通常指“纯声明”，而“定义”一词用于指代既是定义又是声明的任何事物。我们在示例列的注释中使用了这种常用命名法。
一次定义规则 (ODR)
一次定义规则
（简称 ODR）是 C++ 中一条众所周知的规则。ODR 包含三个部分
在一个
文件
内，给定作用域内的每个函数、变量、类型或模板只能有一个定义。发生在不同作用域（例如，在不同函数内定义的局部变量，或在不同命名空间内定义的函数）的定义不违反此规则。
在一个
程序
内，给定作用域内的每个函数或变量只能有一个定义。此规则存在的原因是程序可以有多个文件（我们将在下一课中介绍）。链接器不可见的函数和变量不在此规则的范围内（在课程
7.6 -- 内部链接
中进一步讨论）。
类型、模板、内联函数和内联变量允许在不同文件中具有重复定义，只要每个定义都相同。我们还没有介绍这些东西中的大多数，所以现在不用担心——我们会在相关时再次提及。
相关内容
我们在以下课程中进一步讨论 ODR 第 3 部分豁免
类型 (
13.1 -- 程序定义（用户定义）类型简介
)。
函数模板 (
11.6 -- 函数模板
和
11.7 -- 函数模板实例化
)。
内联函数和变量 (
7.9 -- 内联函数和变量
)。
违反 ODR 第 1 部分将导致编译器发出重定义错误。违反 ODR 第 2 部分将导致链接器发出重定义错误。违反 ODR 第 3 部分将导致未定义行为。
这是一个违反第一部分的例子
int add(int x, int y)
{
     return x + y;
}

int add(int x, int y) // violation of ODR, we've already defined function add(int, int)
{
     return x + y;
}

int main()
{
    int x{};
    int x{ 5 }; // violation of ODR, we've already defined x
}
在此示例中，函数
add(int, int)
被定义了两次（在全局作用域中），局部变量
int x
被定义了两次（在
main()
的作用域中）。因此 Visual Studio 编译器会发出以下编译错误
project3.cpp(9): error C2084: function 'int add(int,int)' already has a body
project3.cpp(3): note: see previous definition of 'add'
project3.cpp(16): error C2086: 'int x': redefinition
project3.cpp(15): note: see declaration of 'x'
然而，对于
main()
来说，定义一个局部变量
int x
，而
add()
也定义一个函数参数
int x
，这并不违反 ODR 的第一部分。这些定义发生在不同的作用域（在各自函数的范围内），因此它们被认为是两个不同对象的独立定义，而不是同一对象的定义和重定义。
致进阶读者
共享同一标识符但具有不同参数集的函数也被认为是不同的函数，因此此类定义不违反 ODR。我们将在课程
11.1 -- 函数重载简介
中进一步讨论这一点。
小测验时间
问题 #1
什么是函数原型？
显示答案
函数原型是一个声明语句，包括函数的名称、返回类型、参数类型，以及可选的参数名称。它不包括函数体。它在函数定义之前告诉编译器函数的存在。
问题 #2
什么是前向声明？
显示答案
前向声明在标识符实际定义之前告诉编译器该标识符的存在。
问题 #3
我们如何为函数声明前向声明？
显示答案
对于函数，函数声明/原型作为前向声明。
问题 #4
为这个函数编写函数声明（使用带名称的推荐形式）
int doMath(int first, int second, int third, int fourth)
{
     return first + second * third / fourth;
}
显示答案
// Do not forget the semicolon at the end, since these are statements.
int doMath(int first, int second, int third, int fourth);
问题 #5
对于以下每个程序，说明它们是编译失败、链接失败，还是编译和链接成功。如果你不确定，请尝试编译它们！
a)
#include <iostream>
int add(int x, int y);

int main()
{
    std::cout << "3 + 4 + 5 = " << add(3, 4, 5) << '\n';
    return 0;
}

int add(int x, int y)
{
    return x + y;
}
显示答案
无法编译。编译器会抱怨找不到匹配的接受 3 个参数的
add()
函数。
add()
的前向声明只有两个参数。
b)
#include <iostream>
int add(int x, int y);

int main()
{
    std::cout << "3 + 4 + 5 = " << add(3, 4, 5) << '\n';
    return 0;
}

int add(int x, int y, int z)
{
    return x + y + z;
}
显示答案
无法编译。编译器会抱怨找不到匹配的接受 3 个参数的
add()
函数。
add()
的前向声明只有两个参数，并且接受 3 个参数的
add()
函数的定义尚未被看到。
c)
#include <iostream>
int add(int x, int y);

int main()
{
    std::cout << "3 + 4 = " << add(3, 4) << '\n';
    return 0;
}

int add(int x, int y, int z)
{
    return x + y + z;
}
显示答案
无法链接。编译器会将 add 的前向声明与 main() 中对 add() 的函数调用匹配。然而，从未实现接受两个参数的 add() 函数（我们只实现了一个接受 3 个参数的），所以链接器会抱怨。
d)
#include <iostream>
int add(int x, int y, int z);

int main()
{
    std::cout << "3 + 4 + 5 = " << add(3, 4, 5) << '\n';
    return 0;
}

int add(int z, int y, int x) // names don't match the declaration
{
    return x + y + z;
}
显示答案
编译和链接成功。对 add() 的函数调用中的类型与前向声明匹配，add() 的定义也匹配。名称与声明不匹配的事实无关紧要，因为声明中的名称是可选的（如果提供，则被编译器忽略）。
e)
#include <iostream>
int add(int, int, int); // no parameter names

int main()
{
    std::cout << "3 + 4 + 5 = " << add(3, 4, 5) << '\n';
    return 0;
}

int add(int x, int y, int z)
{
    return x + y + z;
}
显示答案
编译和链接成功。这与前一个案例相同。函数声明不需要指定参数的名称（尽管我们通常更喜欢包含它们）。
f)
#include <iostream>

int add(int x, int y);

int add(int x, int y, int z)
{
    return x + y + z;
}

int main()
{
    std::cout << "3 + 4 + 5 = " << add(3, 4, 5) << '\n';
    return 0;
}
显示答案
编译和链接成功。具有两个参数的 add() 的前向声明未被使用。
下一课
2.8
包含多个代码文件的程序
返回目录
上一课
2.6
函数为什么有用，以及如何有效地使用它们