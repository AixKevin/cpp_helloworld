# 2.1 — 函数简介

2.1 — 函数简介
Alex
2007 年 5 月 31 日，下午 5:23 PDT
2024 年 9 月 28 日
在上一章中，我们将函数定义为按顺序执行的语句集合。虽然这确实没错，但这个定义并没有提供太多关于函数为何有用的见解。让我们更新一下定义：
函数
是旨在完成特定任务的可重用语句序列。
你已经知道每个可执行程序都必须有一个名为
main()
的函数（程序运行时从此处开始执行）。然而，随着程序变得越来越长，将所有代码都放在
main()
函数中变得越来越难以管理。函数为我们提供了一种将程序分成更小、更模块化的块的方法，这些块更容易组织、测试和使用。大多数程序都使用许多函数。C++ 标准库提供了大量已编写好的函数供你使用——然而，自己编写函数也同样常见。你自己编写的函数称为
用户定义函数
。
考虑一个现实生活中可能出现的情况：你在看书时，突然想起需要打个电话。你把书签夹在书里，打完电话后，回到你做标记的地方，从上次中断的地方继续看书。
C++ 程序可以以同样的方式工作（并借用一些相同的术语）。程序会在一个函数中顺序执行语句，当它遇到函数调用时。
函数调用
告诉 CPU 中断当前函数并执行另一个函数。CPU 实质上在当前执行点“放置一个书签”，执行函数调用中指定的函数，然后
返回
到它标记的点并恢复执行。
命名法
发起函数调用的函数是
调用者
，被
调用
（执行）的函数是
被调用者
。函数调用有时也称为
调用（invocation）
，调用者
调用（invoking）
被调用者。
用户定义函数的示例
首先，让我们从定义用户定义函数的最基本语法开始。在接下来的几课中，所有用户定义函数都将采用以下形式：
returnType functionName() // This is the function header (tells the compiler about the existence of the function)
{
    // This is the function body (tells the compiler what the function does)
}
第一行非正式地称为
函数头
，它告诉编译器函数的存在、函数的名称以及我们将在未来课程中介绍的一些其他信息（例如返回类型）。
在本课中，我们将使用
int
作为
returnType
（对于函数
main()
）或
void
（否则）。现在，不要担心这些，因为我们将在下一课中更多地讨论返回类型和返回值（
2.2 -- 函数返回值（返回值的函数）
）。
就像变量有名称一样，用户定义函数也有名称。
functionName
是你的用户定义函数的名称（标识符）。
标识符后面的括号告诉编译器我们正在定义一个函数。
花括号和中间的语句称为
函数体
。这是确定函数功能所用的语句所在的位置。
要调用函数，我们使用函数名称，后跟一对括号（例如
functionName()
调用名为
functionName
的函数）。通常，括号紧邻函数名称放置（它们之间没有空格）。
目前，函数必须在调用之前定义。我们将在
2.7 -- 前向声明和定义
课中讨论解决此问题的方法。
这是一个演示用户定义函数被定义和调用的示例程序：
#include <iostream> // for std::cout

// Definition of user-defined function doPrint()
// doPrint() is the called function in this example
void doPrint()
{
    std::cout << "In doPrint()\n";
}

// Definition of user-defined function main()
int main()
{
    std::cout << "Starting main()\n";
    doPrint();                        // Interrupt main() by making a function call to doPrint().  main() is the caller.
    std::cout << "Ending main()\n";   // This statement is executed after doPrint() ends

    return 0;
}
此程序生成以下输出：
Starting main()
In doPrint()
Ending main()
此程序从函数
main()
的顶部开始执行，执行的第一行是打印
Starting main()
。
main()
中的第二行是对函数
doPrint()
的函数调用。我们通过后面的括号知道这是一个函数调用。
警告
调用函数时，不要忘记函数名称后面的括号
()
。如果忘记括号，你的程序可能无法编译（如果编译了，函数也不会被调用）。
由于进行了函数调用，
main()
中语句的执行被挂起，执行跳转到被调用函数
doPrint()
的顶部。
doPrint()
中的第一行（也是唯一一行）打印
In doPrint()
。当
doPrint()
终止时，执行返回到调用者（
main()
）并从函数调用之后的点继续。因此，
main()
中执行的下一条语句打印
Ending main()
。
多次调用函数
函数的一个有用之处在于它们可以被多次调用。这是一个演示此功能的程序：
#include <iostream> // for std::cout

void doPrint()
{
    std::cout << "In doPrint()\n";
}

// Definition of function main()
int main()
{
    std::cout << "Starting main()\n";
    doPrint(); // doPrint() called for the first time
    doPrint(); // doPrint() called for the second time
    std::cout << "Ending main()\n";

    return 0;
}
此程序生成以下输出：
Starting main()
In doPrint()
In doPrint()
Ending main()
由于
doPrint()
被
main()
调用了两次，所以
doPrint()
执行了两次，并且
In doPrint()
被打印了两次（每次调用一次）。
函数可以调用调用其他函数的函数
你已经看到函数
main()
可以调用其他函数（例如上面示例中的函数
doPrint()
）。被
main()
调用的函数也可以调用其他函数（这些函数也可以调用函数，依此类推……）。在下面的程序中，函数
main()
调用函数
doA()
，而
doA()
又调用函数
doB()
：
#include <iostream> // for std::cout

void doB()
{
    std::cout << "In doB()\n";
}


void doA()
{
    std::cout << "Starting doA()\n";

    doB();

    std::cout << "Ending doA()\n";
}

// Definition of function main()
int main()
{
    std::cout << "Starting main()\n";

    doA();

    std::cout << "Ending main()\n";

    return 0;
}
此程序生成以下输出：
Starting main()
Starting doA()
In doB()
Ending doA()
Ending main()
不支持嵌套函数
定义放置在另一个函数内部的函数是
嵌套函数
。与某些其他编程语言不同，在 C++ 中，函数不能嵌套。以下程序不合法：
#include <iostream>

int main()
{
    void foo() // Illegal: this function is nested inside function main()
    {
        std::cout << "foo!\n";
    }

    foo(); // function call to foo()

    return 0;
}
编写上述程序的正确方法是：
#include <iostream>

void foo() // no longer inside of main()
{
    std::cout << "foo!\n";
}

int main()
{
    foo();

    return 0;
}
命名法
“foo”是一个无意义的词，在演示某个概念时，当名称不重要时，它通常用作函数或变量的占位符名称。这些词称为
元语法变量
（尽管在日常语言中它们通常被称为“占位符名称”，因为没有人能记住“元语法变量”这个术语）。C++ 中其他常见的元语法变量包括“bar”、“baz”以及以“oo”结尾的三个字母词，例如“goo”、“moo”和“boo”）。
对于对词源学（词语如何演变）感兴趣的人来说，
RFC 3092
是一篇有趣的阅读。
小测验时间
问题 #1
在函数定义中，花括号和中间的语句叫什么？
显示答案
函数体
问题 #2
以下程序打印什么？不要编译此程序，只需自行跟踪代码。
#include <iostream> // for std::cout

void doB()
{
    std::cout << "In doB()\n";
}

void doA()
{
    std::cout << "In doA()\n";

    doB();
}

// Definition of function main()
int main()
{
    std::cout << "Starting main()\n";

    doA();
    doB();

    std::cout << "Ending main()\n";

    return 0;
}
显示答案
Starting main()
In doA()
In doB()
In doB()
Ending main()
下一课
2.2
函数返回值（返回值的函数）
返回目录
上一课
1.x
第一章总结和测验