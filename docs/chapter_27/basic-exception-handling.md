# 27.2 — 基本异常处理

27.2 — 基本异常处理
Alex
2008年10月4日，太平洋夏令时下午1:29
2025年1月6日
在上一节关于
异常的必要性
的课程中，我们讨论了使用返回码如何导致控制流和错误流相互混淆，从而限制两者。C++ 中的异常是使用三个协同工作的关键字实现的：
throw
、
try
和
catch
。
抛出异常
在现实生活中，我们经常使用信号来表示特定事件的发生。例如，在美式足球比赛中，如果一名球员犯规，裁判会扔下一面旗子并吹哨终止比赛。然后进行判罚并执行。一旦判罚处理完毕，比赛通常会恢复正常。
在 C++ 中，
throw 语句
用于表示异常或错误情况已发生（想象一下扔出犯规旗）。表示异常已发生也通常被称为
引发
异常。
要使用 throw 语句，只需使用 throw 关键字，后跟您希望用于表示错误已发生的任何数据类型的值。通常，此值将是错误代码、问题描述或自定义异常类。
以下是一些示例
throw -1; // throw a literal integer value
throw ENUM_INVALID_INDEX; // throw an enum value
throw "Can not take square root of negative number"; // throw a literal C-style (const char*) string
throw dX; // throw a double variable that was previously defined
throw MyException("Fatal Error"); // Throw an object of class MyException
这些语句中的每一个都作为一个信号，表示某种需要处理的问题已经发生。
查找异常
抛出异常只是异常处理过程的一部分。让我们回到美式足球的比喻：一旦裁判扔出犯规旗，接下来会发生什么？球员们注意到犯规发生并停止比赛。足球比赛的正常流程被打断了。
在 C++ 中，我们使用
try
关键字来定义一个语句块（称为
try 块
）。try 块充当观察者，查找 try 块中任何语句抛出的任何异常。
这是一个 try 块的示例
try
{
    // Statements that may throw exceptions you want to handle go here
    throw -1; // here's a trivial throw statement
}
请注意，try 块没有定义我们如何处理异常。它只是告诉程序：“嘿，如果这个 try 块内的任何语句抛出异常，请捕获它！”
处理异常
最后，我们美式足球比喻的结尾：在判罚发出并且比赛停止后，裁判评估并执行判罚。换句话说，在正常比赛恢复之前，必须处理判罚。
实际处理异常是 catch 块的工作。
catch
关键字用于定义一个代码块（称为
catch 块
），该代码块处理单一数据类型的异常。
这是一个捕获整数异常的 catch 块示例
catch (int x)
{
    // Handle an exception of type int here
    std::cerr << "We caught an int exception with value" << x << '\n';
}
try 块和 catch 块协同工作——try 块检测 try 块内语句抛出的任何异常，并将它们路由到具有匹配类型的 catch 块进行处理。一个 try 块后面必须至少有一个 catch 块紧随其后，但可以有多个 catch 块按顺序排列。
一旦异常被 try 块捕获并路由到匹配的 catch 块进行处理，该异常就被认为是已处理。匹配的 catch 块执行后，执行照常恢复，从最后一个 catch 块之后的第一个语句开始。
catch 参数的工作方式与函数参数类似，参数在随后的 catch 块中可用。基本类型的异常可以通过值捕获，但非基本类型的异常应该通过 const 引用捕获，以避免不必要的复制（在某些情况下，还可以防止切片）。
就像函数一样，如果参数在 catch 块中不使用，变量名可以省略
catch (double) // note: no variable name since we don't use it in the catch block below
{
    // Handle exception of type double here
    std::cerr << "We caught an exception of type double\n";
}
这有助于防止编译器关于未使用变量的警告。
异常不进行类型转换（因此 int 异常不会转换为匹配带有 double 参数的 catch 块）。
将 throw、try 和 catch 组合在一起
这是一个使用 throw、try 和多个 catch 块的完整程序
#include <iostream>
#include <string>

int main()
{
    try
    {
        // Statements that may throw exceptions you want to handle go here
        throw -1; // here's a trivial example
    }
    catch (double) // no variable name since we don't use the exception itself in the catch block below
    {
        // Any exceptions of type double thrown within the above try block get sent here
        std::cerr << "We caught an exception of type double\n";
    }
    catch (int x)
    {
        // Any exceptions of type int thrown within the above try block get sent here
        std::cerr << "We caught an int exception with value: " << x << '\n';
    }
    catch (const std::string&) // catch classes by const reference
    {
        // Any exceptions of type std::string thrown within the above try block get sent here
        std::cerr << "We caught an exception of type std::string\n";
    }

    // Execution continues here after the exception has been handled by any of the above catch blocks
    std::cout << "Continuing on our merry way\n";

    return 0;
}
在作者的机器上，运行上述 try/catch 块会产生以下结果
We caught an int exception with value -1
Continuing on our merry way
throw 语句用于引发值为 -1 的异常，该异常的类型为 int。然后，该 throw 语句被包含的 try 块捕获，并路由到处理 int 类型异常的相应 catch 块。此 catch 块打印了相应的错误消息。
异常处理完毕后，程序在 catch 块之后继续正常执行，打印“Continuing on our merry way”。
异常处理回顾
异常处理实际上相当简单，以下两段内容涵盖了您需要记住的大部分内容
当异常被引发（使用
throw
）时，正在运行的程序会找到最近的 enclosing
try
块（如有必要，沿堆栈向上查找 enclosing try 块——我们将在下一课中详细讨论这一点），以查看附加到该 try 块的任何
catch
处理器是否可以处理该类型的异常。如果是，执行会跳转到 catch 块的顶部，异常被认为是已处理。
如果在最近的 enclosing try 块中没有找到合适的 catch 处理器，程序会继续在随后的 enclosing try 块中查找 catch 处理器。如果在程序结束前仍未找到合适的 catch 处理器，程序将因运行时异常错误而失败。
请注意，程序在将异常与 catch 块匹配时不会执行隐式转换或提升！例如，一个 char 异常不会与一个 int catch 块匹配。一个 int 异常不会与一个 float catch 块匹配。然而，会执行从派生类到其父类之一的转换。
这确实就是所有内容。本章的其余部分将致力于展示这些原则在工作中的示例。
异常立即处理
这是一个演示异常如何立即处理的简短程序
#include <iostream>

int main()
{
    try
    {
        throw 4.5; // throw exception of type double
        std::cout << "This never prints\n";
    }
    catch (double x) // handle exception of type double
    {
        std::cerr << "We caught a double of value: " << x << '\n';
    }

    return 0;
}
这个程序再简单不过了。以下是发生的情况：throw 语句是第一个被执行的语句——这导致引发一个 double 类型的异常。执行立即转移到最近的 enclosing try 块，这是本程序中唯一的 try 块。然后检查 catch 处理器以查看是否有任何处理器匹配。我们的异常是 double 类型，所以我们正在寻找一个 double 类型的 catch 处理器。我们有一个，所以它执行。
因此，该程序的结果如下
We caught a double of value: 4.5
请注意，“This never prints”从不打印，因为异常导致执行路径立即跳转到 double 类型的异常处理程序。
一个更真实的例子
让我们看一个不那么学术的例子
#include <cmath> // for sqrt() function
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    double x {};
    std::cin >> x;

    try // Look for exceptions that occur within try block and route to attached catch block(s)
    {
        // If the user entered a negative number, this is an error condition
        if (x < 0.0)
            throw "Can not take sqrt of negative number"; // throw exception of type const char*

        // Otherwise, print the answer
        std::cout << "The sqrt of " << x << " is " << std::sqrt(x) << '\n';
    }
    catch (const char* exception) // catch exceptions of type const char*
    {
        std::cerr << "Error: " << exception << '\n';
    }
}
在这段代码中，系统会要求用户输入一个数字。如果用户输入一个正数，if 语句不会执行，不会抛出异常，并且会打印该数字的平方根。在这种情况下，因为没有抛出异常，catch 块中的代码永远不会执行。结果会是这样：
Enter a number: 9
The sqrt of 9 is 3
如果用户输入一个负数，我们抛出 const char* 类型的异常。由于我们处于一个 try 块中并且找到了匹配的异常处理程序，控制立即转移到 const char* 异常处理程序。结果是
Enter a number: -4
Error: Can not take sqrt of negative number
到现在为止，您应该已经掌握了异常的基本概念。在下一课中，我们将提供更多示例来展示异常的灵活性。
catch 块通常做什么
如果异常被路由到 catch 块，即使 catch 块为空，它也被认为是“已处理”。然而，通常您会希望您的 catch 块做一些有用的事情。当 catch 块捕获到异常时，有四种常见的事情：
首先，catch 块可以打印错误（到控制台或日志文件），然后允许函数继续执行。
其次，catch 块可以将值或错误代码返回给调用者。
第三，catch 块可以抛出另一个异常。因为 catch 块在 try 块之外，所以这种情况下新抛出的异常不会被前面的 try 块处理——它会被下一个 enclosing try 块处理。
第四，main() 中的 catch 块可以用于捕获致命错误并以一种干净的方式终止程序。
下一课
27.3
异常、函数和堆栈展开
返回目录
上一课
27.1
异常的必要性