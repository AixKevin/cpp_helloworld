# 8.12 — 终止（提前退出程序）

8.12 — 终止（提前退出程序）
Alex
2020 年 12 月 21 日，太平洋标准时间上午 11:26
2024 年 12 月 28 日
我们将在此章中介绍的最后一类流程控制语句是停止。
停止
是一种终止程序的流程控制语句。在 C++ 中，停止被实现为函数（而不是关键字），因此我们的停止语句将是函数调用。
让我们简要地绕个弯，回顾一下程序正常退出时会发生什么。当
main()
函数返回时（通过到达函数末尾，或通过
return 语句
），会发生许多不同的事情。
首先，因为我们正在离开函数，所有局部变量和函数参数都被销毁（一如既往）。
接下来，会调用一个名为
std::exit()
的特殊函数，并将
main()
的返回值（
状态码
）作为参数传递。那么
std::exit()
是什么呢？
std::exit() 函数
std::exit()
是一个导致程序正常终止的函数。
正常终止
意味着程序以预期的方式退出。请注意，术语
正常终止
并不表示程序是否成功（这是
状态码
的作用）。例如，假设您正在编写一个程序，您期望用户输入一个文件名进行处理。如果用户输入了无效的文件名，您的程序可能会返回一个非零的
状态码
来指示失败状态，但它仍然是
正常终止
。
std::exit()
执行许多清理功能。首先，具有静态存储持续时间的对象被销毁。然后，如果使用了任何文件，还会进行一些其他的杂项文件清理。最后，控制权返回给操作系统，传递给
std::exit()
的参数用作
状态码
。
显式调用 std::exit()
尽管
std::exit()
在函数
main()
返回后被隐式调用，但
std::exit()
也可以被显式调用以在程序正常终止之前停止程序。以这种方式调用
std::exit()
时，您需要包含
cstdlib
头文件。
关键见解
当
main()
返回时，
std::exit
会被隐式调用。
这是一个显式使用
std::exit()
的示例
#include <cstdlib> // for std::exit()
#include <iostream>

void cleanup()
{
    // code here to do any kind of cleanup required
    std::cout << "cleanup!\n";
}

int main()
{
    std::cout << 1 << '\n';
    cleanup();

    std::exit(0); // terminate and return status code 0 to operating system

    // The following statements never execute
    std::cout << 2 << '\n';

    return 0;
}
这个程序打印
1
cleanup!
请注意，调用
std::exit()
之后的语句永远不会执行，因为程序已经终止。
尽管在上面的程序中我们从函数
main()
调用
std::exit()
，但
std::exit()
可以从任何函数调用以在该点终止程序。
std::exit() 不清理局部变量
关于显式调用
std::exit()
的一个重要注意事项：
std::exit()
不会清理任何局部变量（无论是在当前函数中，还是在调用堆栈上的函数中）。这意味着如果您的程序依赖于任何局部变量自行清理，调用
std::exit()
可能会很危险。
警告
std::exit()
函数不清理当前函数或调用堆栈上的局部变量。
std::atexit
因为
std::exit()
会立即终止程序，您可能希望在终止之前手动进行一些清理工作。在这种情况下，清理意味着关闭数据库或网络连接、释放已分配的任何内存、将信息写入日志文件等……
题外话…
当应用程序退出时，现代操作系统通常会清理应用程序未自行正确清理的任何内存。这就引出了一个问题，“那为什么还要费心在退出时进行清理呢？”。至少有两个原因：
清理已分配的内存是一个“好习惯”，您需要使用它来避免应用程序运行时出现内存泄漏。在某些情况下清理而在另一些情况下不清理是不一致的，并且可能导致错误。不正确地清理内存还会影响某些工具（如内存分析器）的行为（它们可能无法区分您无意中未清理的内存和您故意未清理的内存，因为您不必清理）。
还有其他类型的清理可能对您的程序按预期运行是必要的。例如，如果您将数据写入文件然后意外退出，该数据可能尚未刷新到文件，并且在程序退出时可能会丢失。在关闭之前关闭文件有助于确保所有缓存数据将首先被写入。或者您可能希望在实际关闭之前将有关用户会话或程序关闭原因的数据发送到服务器。
在上面的示例中，我们调用了
cleanup()
函数来处理我们的清理任务。然而，记住在每次调用
exit()
之前手动调用清理函数会增加程序员的负担，并且是错误的根源。
为了解决这个问题，C++ 提供了
std::atexit()
函数，它允许您指定一个函数，该函数将在通过
std::exit()
终止程序时自动调用。
相关内容
我们在
20.1 -- 函数指针
课程中讨论将函数作为参数传递。
这是一个例子
#include <cstdlib> // for std::exit()
#include <iostream>

void cleanup()
{
    // code here to do any kind of cleanup required
    std::cout << "cleanup!\n";
}

int main()
{
    // register cleanup() to be called automatically when std::exit() is called
    std::atexit(cleanup); // note: we use cleanup rather than cleanup() since we're not making a function call to cleanup() right now

    std::cout << 1 << '\n';

    std::exit(0); // terminate and return status code 0 to operating system

    // The following statements never execute
    std::cout << 2 << '\n';

    return 0;
}
此程序与之前的示例具有相同的输出
1
cleanup!
请注意，当我们将
cleanup()
函数作为参数传递时，我们使用
cleanup
（函数名），而不是
cleanup()
（这实际上会调用函数）。
std::atexit()
的好处是，我们只需调用一次（可能在
main()
函数内部）。由于
std::atexit()
将在退出时自动调用，因此我们不必记住在调用
std::exit()
之前调用任何东西。
关于
std::atexit()
和清理函数有几点注意事项：首先，因为当
main()
终止时
std::exit()
会被隐式调用，所以如果程序以这种方式退出，这将调用任何通过
std::atexit()
注册的函数。其次，被注册的函数必须不带参数且没有返回值。最后，如果您愿意，可以使用
std::atexit()
注册多个清理函数，它们将以注册的相反顺序调用（最后注册的将首先调用）。
致进阶读者
在多线程程序中，调用
std::exit()
可能会导致程序崩溃（因为调用
std::exit()
的线程将清理可能仍被其他线程访问的静态对象）。因此，C++ 引入了另一对与
std::exit()
和
std::atexit()
类似的功能的函数，名为
std::quick_exit()
和
std::at_quick_exit()
。
std::quick_exit()
正常终止程序，但不清理静态对象，并且可能进行或不进行其他类型的清理。
std::at_quick_exit()
对于用
std::quick_exit()
终止的程序执行与
std::atexit()
相同的作用。
std::abort 和 std::terminate
C++ 包含另外两个与停止相关的函数。
std::abort()
函数导致程序异常终止。
异常终止
意味着程序发生了某种不寻常的运行时错误，程序无法继续运行。例如，尝试除以 0 将导致异常终止。
std::abort()
不进行任何清理。
#include <cstdlib> // for std::abort()
#include <iostream>

int main()
{
    std::cout << 1 << '\n';
    std::abort();

    // The following statements never execute
    std::cout << 2 << '\n';

    return 0;
}
我们将在未来的课程
9.6 -- Assert 和 static_assert
中看到
std::abort
被隐式调用的情况。
std::terminate()
函数通常与
异常
结合使用（我们将在后面的章节中介绍异常）。尽管
std::terminate
可以显式调用，但它更常在异常未处理时（以及其他一些与异常相关的情况）隐式调用。默认情况下，
std::terminate()
调用
std::abort()
。
何时应该使用停止？
简短的答案是“几乎从不”。销毁局部对象是 C++ 的一个重要组成部分（特别是当我们接触到类时），并且上述所有函数都不会清理局部变量。异常是处理错误情况更好、更安全的机制。
最佳实践
仅当无法安全或合理地从主函数正常返回时才使用停止。如果您尚未禁用异常，则优先使用异常来安全地处理错误。
提示
尽管应尽量减少停止的显式使用，但程序仍有许多其他方式会意外关闭。例如：
应用程序可能因 bug 而崩溃（在这种情况下，操作系统将关闭它）。
用户可能以各种方式终止应用程序。
用户可能关闭（或失去）计算机电源。
太阳可能会发生超新星爆发，将地球吞噬在一个巨大的火球中。
一个设计良好的程序应该能够以最小的后果处理在任何时候被关闭。
作为一个常见的例子，现代游戏通常会定期自动保存游戏状态和用户设置，这样如果游戏意外关闭而未保存，用户可以稍后继续（使用之前的自动保存）而不会丢失太多进度。
下一课
8.13
随机数生成简介
返回目录
上一课
8.11
Break 和 continue