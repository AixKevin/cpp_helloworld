# 27.3 — 异常、函数和堆栈展开

27.3 — 异常、函数和堆栈展开
Alex
2008年10月5日，太平洋夏令时上午11:25
2024年9月29日
在上一节关于
27.2 -- 基本异常处理
的课程中，我们解释了 throw、try 和 catch 如何协同工作以实现异常处理。在本节中，我们将讨论异常处理如何与函数交互。
从被调用函数中抛出异常
在上一节中，我们提到：“try 块检测 try 块内语句抛出的任何异常”。在相应的示例中，我们的 throw 语句位于 try 块内，并由关联的 catch 块捕获，所有这些都发生在同一个函数中。在单个函数中既抛出又捕获异常的价值有限。
更有趣的是，如果 try 块内的语句是一个函数调用，并且被调用的函数抛出了异常，会发生什么。try 块会检测到从 try 块内调用的函数抛出的异常吗？
幸运的是，答案是肯定的！
异常处理最有用的特性之一是 throw 语句不必直接放在 try 块内。相反，异常可以从函数中的任何位置抛出，并且这些异常可以由调用者（或调用者的调用者等）的 try 块捕获。当以这种方式捕获异常时，执行会从抛出异常的点跳转到处理异常的 catch 块。
关键见解
Try 块不仅捕获 try 块内语句的异常，还捕获 try 块内调用的函数的异常。
这使我们能够以更模块化的方式使用异常处理。我们将通过重写上一节中的平方根程序来演示这一点，以使用模块化函数。
#include <cmath> // for sqrt() function
#include <iostream>

// A modular square root function
double mySqrt(double x)
{
    // If the user entered a negative number, this is an error condition
    if (x < 0.0)
        throw "Can not take sqrt of negative number"; // throw exception of type const char*

    return std::sqrt(x);
}

int main()
{
    std::cout << "Enter a number: ";
    double x {};
    std::cin >> x;

    try // Look for exceptions that occur within try block and route to attached catch block(s)
    {
        double d = mySqrt(x);
        std::cout << "The sqrt of " << x << " is " << d << '\n';
    }
    catch (const char* exception) // catch exceptions of type const char*
    {
        std::cerr << "Error: " << exception << std::endl;
    }

    return 0;
}
在这个程序中，我们将检查异常并计算平方根的代码放入了一个名为 mySqrt() 的模块化函数中。然后我们从 try 块内部调用了这个 mySqrt() 函数。让我们验证它是否仍然按预期工作
Enter a number: -4
Error: Can not take sqrt of negative number
确实如此！当异常在 mySqrt() 内部抛出时，mySqrt() 中没有处理该异常的处理器。然而，对 mySqrt() 的调用（在 main() 中）位于一个具有关联匹配异常处理程序的 try 块内。因此，执行从 mySqrt() 中的 throw 语句跳转到 main() 中 catch 块的顶部，然后继续执行。
上述程序最有趣的部分是 mySqrt() 函数可以抛出异常，但它本身不处理此异常！这本质上意味着 mySqrt() 愿意说“嘿，有问题！”，但不愿意自己处理问题。它本质上是将处理异常的责任委托给它的调用者（这类似于使用返回码将处理错误的责任传递回函数的调用者）。
此时，你们中的一些人可能想知道为什么将错误传递回调用者是一个好主意。为什么不让 MySqrt() 自己处理它的错误呢？问题在于不同的应用程序可能希望以不同的方式处理错误。控制台应用程序可能希望打印文本消息。Windows 应用程序可能希望弹出错误对话框。在一个应用程序中，这可能是致命错误，而在另一个应用程序中则可能不是。通过将错误传递出函数，每个应用程序都可以以对其最适合的上下文方式处理来自 mySqrt() 的错误！最终，这使 mySqrt() 尽可能模块化，并且错误处理可以放在代码中不那么模块化的部分。
异常处理和堆栈展开
在本节中，我们将看看当涉及多个函数时，异常处理是如何实际工作的。
相关内容
在继续之前，如果您需要刷新调用堆栈和堆栈展开的知识，请参阅
20.2 -- 堆栈和堆
课程。
当抛出异常时，程序首先查看是否可以在当前函数内部立即处理该异常（这意味着异常在当前函数内的 try 块内抛出，并且存在相应的 catch 块）。如果当前函数可以处理该异常，它就会处理。
如果不能，程序接下来检查函数的调用者（调用堆栈中上一个函数）是否可以处理该异常。为了让函数的调用者处理异常，对当前函数的调用必须在 try 块内，并且必须关联一个匹配的 catch 块。如果没有找到匹配项，则检查调用者的调用者（调用堆栈中再上两个函数）。类似地，为了让调用者的调用者处理异常，对调用者的调用必须在 try 块内，并且必须关联一个匹配的 catch 块。
检查调用堆栈中每个函数的过程会一直持续，直到找到处理程序，或者检查完调用堆栈上的所有函数并且没有找到处理程序。
如果找到匹配的异常处理程序，则执行从抛出异常的点跳转到匹配的 catch 块的顶部。这需要根据需要多次展开堆栈（从调用堆栈中移除当前函数），以使处理异常的函数成为调用堆栈上的顶部函数。
如果没有找到匹配的异常处理程序，堆栈可能会或可能不会展开。我们将在下一节（
27.4 -- 未捕获的异常和全捕获处理程序
）中详细讨论这种情况。
当当前函数从调用堆栈中移除时，所有局部变量都会像往常一样被销毁，但不会返回任何值。
关键见解
展开堆栈会销毁被展开函数中的局部变量（这是好事，因为它确保它们的析构函数执行）。
另一个堆栈展开示例
为了说明上述内容，让我们看一个更复杂的示例，使用更大的堆栈。尽管这个程序很长，但它非常简单：main() 调用 A()，A() 调用 B()，B() 调用 C()，C() 调用 D()，D() 抛出异常。
#include <iostream>

void D() // called by C()
{
    std::cout << "Start D\n";
    std::cout << "D throwing int exception\n";

    throw - 1;

    std::cout << "End D\n"; // skipped over
}

void C() // called by B()
{
    std::cout << "Start C\n";
    D();
    std::cout << "End C\n";
}

void B() // called by A()
{
    std::cout << "Start B\n";

    try
    {
        C();
    }
    catch (double) // not caught: exception type mismatch
    {
        std::cerr << "B caught double exception\n";
    }

    try
    {
    }
    catch (int) // not caught: exception not thrown within try
    {
        std::cerr << "B caught int exception\n";
    }

    std::cout << "End B\n";
}

void A() // called by main()
{
    std::cout << "Start A\n";

    try
    {
        B();
    }
    catch (int) // exception caught here and handled
    {
        std::cerr << "A caught int exception\n";
    }
    catch (double) // not called because exception was handled by prior catch block
    {
        std::cerr << "A caught double exception\n";
    }

    // execution continues here after the exception is handled
    std::cout << "End A\n";
}

int main()
{
    std::cout << "Start main\n";

    try
    {
        A();
    }
    catch (int) // not called because exception was handled by A
    {
        std::cerr << "main caught int exception\n";
    }
    std::cout << "End main\n";

    return 0;
}
仔细查看这个程序，看看你是否能弄清楚它运行时会打印什么，什么不会打印。答案如下
Start main
Start A
Start B
Start C
Start D
D throwing int exception
A caught int exception
End A
End main
让我们来看看在这种情况下会发生什么。“Start”语句的打印是直接的，不需要进一步解释。函数 D() 打印“D throwing int exception”，然后抛出一个 int 异常。这就是事情开始变得有趣的地方。
因为 D() 不处理异常本身，所以会检查它的调用者（调用堆栈中的函数）看它们中是否有能处理异常的。函数 C() 不处理任何异常，因此在那里没有找到匹配项。
函数 B() 有两个独立的 try 块。包含对 C() 调用的 try 块有一个处理 double 类型异常的处理程序，但这与我们的 int 类型异常不匹配（并且异常不做类型转换），因此没有找到匹配项。空的 try 块确实有一个处理 int 类型异常的异常处理程序，但是这个 catch 块不被认为是匹配项，因为对 C() 的调用不在关联的 try 块内。
A() 也有一个 try 块，并且对 B() 的调用在其内部，因此程序会查看是否有针对 int 异常的 catch 处理程序。有！因此，A() 处理异常，并打印“A caught int exception”。
由于异常现在已经处理，控制在 A() 中的 catch 块之后正常继续。这意味着 A() 打印“End A”，然后正常终止。
控制返回到 main()。尽管 main() 有一个针对 int 的异常处理程序，但我们的异常已被 A() 处理，因此 main() 中的 catch 块不会执行。main() 只是打印“End main”，然后正常终止。
这个程序说明了相当多有趣的原则
首先，抛出异常的函数的直接调用者如果不想处理异常，不必处理。在这种情况下，C() 没有处理 D() 抛出的异常。它将该责任委托给堆栈中它的一个调用者。
其次，如果一个 try 块没有针对正在抛出异常类型的 catch 处理程序，那么堆栈展开会像根本没有 try 块一样发生。在这种情况下，B() 也没有处理异常，因为它没有正确的 catch 块类型。
第三，如果一个函数有一个匹配的 catch 块，但对当前函数的调用没有发生在关联的 try 块内，那么该 catch 块将不会被使用。我们在 B() 中也看到了这一点。
最后，一旦匹配的 catch 块执行，控制流将正常进行，从最后一个 catch 块后的第一条语句开始。这由 A() 处理错误，然后继续打印“End A”，然后返回到调用者所演示。当程序返回到 main() 时，异常已经抛出并处理了——main() 根本不知道有异常！
正如你所看到的，堆栈展开为我们提供了一些非常有用的行为——如果一个函数不想处理异常，它就不必处理。异常会沿着堆栈传播，直到找到会处理它的人！这使我们能够决定在调用堆栈的哪个位置最适合处理可能发生的任何错误。
在下一课中，我们将探讨未捕获异常时会发生什么，以及防止这种情况发生的方法。
下一课
27.4
未捕获的异常和全捕获处理程序
返回目录
上一课
27.2
基本异常处理