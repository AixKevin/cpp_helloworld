# 2.12 — 头文件保护

2.12 — 头文件保护
Alex
2016年4月5日，太平洋夏令时上午11:41
2024年6月12日
重复定义问题
在课程
2.7 -- 前向声明和定义
中，我们提到变量或函数标识符只能有一个定义（one definition rule，即一个定义规则）。因此，如果一个程序多次定义一个变量标识符，将导致编译错误。
int main()
{
    int x; // this is a definition for variable x
    int x; // compile error: duplicate definition

    return 0;
}
同样，如果一个程序多次定义一个函数，也会导致编译错误。
#include <iostream>

int foo() // this is a definition for function foo
{
    return 5;
}

int foo() // compile error: duplicate definition
{
    return 5;
}

int main()
{
    std::cout << foo();
    return 0;
}
虽然这些程序很容易修复（删除重复的定义），但是在使用头文件时，很容易出现头文件中的定义被多次包含的情况。当一个头文件 #包含 另一个头文件时（这很常见），就可能发生这种情况。
作者注
在接下来的例子中，我们将在头文件中定义一些函数。通常你不应该这样做。
我们这样做是因为它是使用我们已经涵盖的功能来演示一些概念的最有效方法。
考虑以下学术示例
square.h
int getSquareSides()
{
    return 4;
}
wave.h
#include "square.h"
main.cpp
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
这个看似无害的程序将无法编译！以下是发生的情况。首先，
main.cpp
#包含
square.h
，这将函数
getSquareSides
的定义复制到
main.cpp
中。然后
main.cpp
#包含
wave.h
，而
wave.h
本身 #包含
square.h
。这会将
square.h
的内容（包括函数
getSquareSides
的定义）复制到
wave.h
中，然后这些内容又被复制到
main.cpp
中。
因此，在解析所有 #include 指令后，
main.cpp
最终看起来像这样
int getSquareSides()  // from square.h
{
    return 4;
}

int getSquareSides() // from wave.h (via square.h)
{
    return 4;
}

int main()
{
    return 0;
}
重复定义和编译错误。每个文件单独来看都是正常的。但是，由于
main.cpp
最终两次 #包含了
square.h
的内容，我们遇到了问题。如果
wave.h
需要
getSquareSides()
，并且
main.cpp
需要
wave.h
和
square.h
，你将如何解决这个问题？
头文件卫士
好消息是我们可以通过一种叫做
头文件卫士
（也叫
包含卫士
）的机制来避免上述问题。头文件卫士是条件编译指令，其形式如下：
#ifndef SOME_UNIQUE_NAME_HERE
#define SOME_UNIQUE_NAME_HERE

// your declarations (and certain types of definitions) here

#endif
当这个头文件被 #包含时，预处理器会检查
SOME_UNIQUE_NAME_HERE
是否已经在当前翻译单元中被定义过。如果这是我们第一次包含这个头文件，
SOME_UNIQUE_NAME_HERE
将没有被定义。因此，它会 #定义
SOME_UNIQUE_NAME_HERE
并包含文件的内容。如果这个头文件在同一个文件中再次被包含，
SOME_UNIQUE_NAME_HERE
将已经在第一次包含头文件内容时被定义了，并且头文件的内容将被忽略（多亏了 #ifndef）。
所有你的头文件都应该有头文件卫士。
SOME_UNIQUE_NAME_HERE
可以是任何你想要的名字，但按照约定，它被设置为头文件的完整文件名，全部大写，用下划线代替空格或标点符号。例如，
square.h
会有头文件卫士
square.h
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
即使是标准库头文件也使用头文件卫士。如果你查看 Visual Studio 中的 iostream 头文件，你会看到
#ifndef _IOSTREAM_
#define _IOSTREAM_

// content here

#endif
致进阶读者
在大型程序中，可能会有两个独立的头文件（从不同的目录包含）最终具有相同的文件名（例如 directoryA\config.h 和 directoryB\config.h）。如果只使用文件名作为包含卫士（例如 CONFIG_H），这两个文件最终可能会使用相同的卫士名称。如果发生这种情况，任何直接或间接包含这两个 config.h 文件的文件将不会接收第二个包含文件中的内容。这可能会导致编译错误。
由于可能发生卫士名称冲突，许多开发人员建议在头文件卫士中使用更复杂/唯一的名称。一些好的建议是 PROJECT_PATH_FILE_H、FILE_LARGE-RANDOM-NUMBER_H 或 FILE_CREATION-DATE_H 这样的命名约定。
使用头文件卫士更新我们之前的示例
让我们回到
square.h
的例子，使用带有头文件卫士的
square.h
。为了规范，我们也将头文件卫士添加到
wave.h
中。
square.h
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
wave.h
#ifndef WAVE_H
#define WAVE_H

#include "square.h"

#endif
main.cpp
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
在预处理器解析所有 #include 指令后，这个程序看起来像这样
main.cpp
// Square.h included from main.cpp
#ifndef SQUARE_H // square.h included from main.cpp
#define SQUARE_H // SQUARE_H gets defined here

// and all this content gets included
int getSquareSides()
{
    return 4;
}

#endif // SQUARE_H

#ifndef WAVE_H // wave.h included from main.cpp
#define WAVE_H
#ifndef SQUARE_H // square.h included from wave.h, SQUARE_H is already defined from above
#define SQUARE_H // so none of this content gets included

int getSquareSides()
{
    return 4;
}

#endif // SQUARE_H
#endif // WAVE_H

int main()
{
    return 0;
}
我们来看看这是如何评估的。
首先，预处理器评估
#ifndef SQUARE_H
。
SQUARE_H
尚未定义，因此从
#ifndef
到随后的
#endif
的代码被包含用于编译。这段代码定义了
SQUARE_H
，并包含
getSquareSides
函数的定义。
稍后，下一个
#ifndef SQUARE_H
被评估。这次，
SQUARE_H
已经被定义了（因为它在上面被定义了），所以从
#ifndef
到随后的
#endif
的代码被排除在编译之外。
头文件卫士阻止重复包含，因为当第一次遇到卫士时，卫士宏未定义，因此包含受保护的内容。在此之后，卫士宏已定义，因此任何后续的受保护内容副本都会被排除。
头文件卫士不能阻止头文件被包含一次到不同的代码文件中
请注意，头文件卫士的目标是防止代码文件接收到受保护头文件的多个副本。根据设计，头文件卫士并**不**阻止给定的头文件被（一次）包含到单独的代码文件中。这也会导致意想不到的问题。考虑
square.h
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

int getSquarePerimeter(int sideLength); // forward declaration for getSquarePerimeter

#endif
square.cpp
#include "square.h"  // square.h is included once here

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
main.cpp
#include "square.h" // square.h is also included once here
#include <iostream>

int main()
{
    std::cout << "a square has " << getSquareSides() << " sides\n";
    std::cout << "a square of length 5 has perimeter length " << getSquarePerimeter(5) << '\n';

    return 0;
}
请注意，
square.h
既从
main.cpp
包含，也从
square.cpp
包含。这意味着
square.h
的内容将一次包含到
square.cpp
中，一次包含到
main.cpp
中。
让我们更详细地研究一下为什么会发生这种情况。当
square.h
从
square.cpp
包含时，
SQUARE_H
在
square.cpp
结束之前都会被定义。这个定义阻止了
square.h
第二次包含到
square.cpp
中（这是头文件卫士的目的）。然而，一旦
square.cpp
完成，
SQUARE_H
就不再被认为是定义的了。这意味着当预处理器在
main.cpp
上运行时，
SQUARE_H
最初在
main.cpp
中并未定义。
最终结果是
square.cpp
和
main.cpp
都得到了
getSquareSides
定义的副本。这个程序会编译，但是链接器会抱怨你的程序对标识符
getSquareSides
有多个定义！
解决这个问题的最佳方法是简单地将函数定义放在其中一个 .cpp 文件中，这样头文件只包含一个前向声明
square.h
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides(); // forward declaration for getSquareSides
int getSquarePerimeter(int sideLength); // forward declaration for getSquarePerimeter

#endif
square.cpp
#include "square.h"

int getSquareSides() // actual definition for getSquareSides
{
    return 4;
}

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
main.cpp
#include "square.h" // square.h is also included once here
#include <iostream>

int main()
{
    std::cout << "a square has " << getSquareSides() << " sides\n";
    std::cout << "a square of length 5 has perimeter length " << getSquarePerimeter(5) << '\n';

    return 0;
}
现在当程序编译时，函数
getSquareSides
将只有一个定义（通过
square.cpp
），因此链接器会很高兴。文件
main.cpp
能够调用此函数（即使它位于
square.cpp
中），因为它包含
square.h
，其中包含该函数的前向声明（链接器会将
main.cpp
中对
getSquareSides
的调用连接到
square.cpp
中
getSquareSides
的定义）。
我们不能只是避免在头文件中定义吗？
我们通常告诉您不要在头文件中包含函数定义。所以您可能想知道，如果您不应该这样做，为什么还要包含头文件卫士。
将来我们会向您展示很多情况，在这些情况下需要在头文件中放置非函数定义。例如，C++ 允许您创建自己的类型。这些自定义类型通常在头文件中定义，以便类型定义可以传播到需要使用它们的代码文件中。如果没有头文件卫士，一个代码文件最终可能会有给定类型的多个（相同）副本定义，编译器会将其标记为错误。
所以，即使在本系列教程的这一点上，头文件卫士并非严格必要，但我们现在正在养成良好的习惯，这样您以后就不必改掉坏习惯。
#pragma once
现代编译器支持使用
#pragma
预处理器指令的更简单、替代形式的头文件卫士
#pragma once

// your code here
#pragma once
的作用与头文件卫士相同：避免头文件被多次包含。对于传统的头文件卫士，开发者负责保护头文件（通过使用预处理器指令
#ifndef
、
#define
和
#endif
）。而使用
#pragma once
，我们是在请求编译器保护头文件。它具体如何实现这是一个与实现相关的细节。
致进阶读者
有一种已知情况是
#pragma once
通常会失效。如果一个头文件被复制，使其存在于文件系统中的多个位置，并且如果这两个头文件的副本都被包含，头文件卫士将成功地去除重复的相同头文件，但是
#pragma once
不会（因为编译器不会意识到它们实际上是相同的内容）。
对于大多数项目来说，
#pragma once
运行良好，许多开发者现在更喜欢它，因为它更容易且不易出错。许多 IDE 也会在通过 IDE 生成的新头文件的顶部自动包含
#pragma once
。
警告
#pragma
指令是为编译器实现者设计的，用于他们想要的任何目的。因此，支持哪些 pragma 以及这些 pragma 的含义完全取决于实现。除了
#pragma once
，不要指望在一个编译器上有效的 pragma 会被另一个编译器支持。
由于
#pragma once
未由 C++ 标准定义，因此某些编译器可能不会实现它。因此，一些开发公司（如 Google）建议使用传统的头文件卫士。在本教程系列中，我们将偏爱头文件卫士，因为它们是保护头文件最传统的方式。然而，目前对
#pragma once
的支持已经相当普遍，如果您希望改用
#pragma once
，这在现代 C++ 中通常也是可以接受的。
总结
头文件卫士旨在确保给定头文件的内容不会被复制到任何单个文件中多次，以防止重复定义。
重复的*声明*是可以的——但即使你的头文件全部由声明组成（没有定义），包含头文件卫士仍然是一种最佳实践。
请注意，头文件卫士**不**阻止头文件的内容被（一次）复制到单独的项目文件中。这是一件好事，因为我们经常需要从不同的项目文件中引用给定头文件的内容。
小测验时间
问题 #1
将头文件卫士添加到此头文件中
add.h
int add(int x, int y);
显示答案
#ifndef ADD_H
#define ADD_H

int add(int x, int y);

#endif
下一课
2.13
如何设计你的第一个程序
返回目录
上一课
2.11
头文件