# 27.4 — 未捕获异常和万能处理程序

27.4 — 未捕获异常和万能处理程序
Alex
2008 年 10 月 25 日，太平洋夏令时 12:07
2024 年 9 月 12 日
到目前为止，您应该对异常的工作方式有一个合理的了解。在本课中，我们将介绍一些更有趣的异常情况。
未捕获异常
当一个函数抛出它自己不处理的异常时，它会假设调用堆栈中的某个函数将处理该异常。在下面的示例中，mySqrt() 假设会有人处理它抛出的异常——但是如果实际上没有人处理呢？
这是我们的平方根程序，不包含 main() 中的 try 块
#include <iostream>
#include <cmath> // for sqrt() function

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
    double x;
    std::cin >> x;

    // Look ma, no exception handler!
    std::cout << "The sqrt of " << x << " is " << mySqrt(x) << '\n';

    return 0;
}
现在，假设用户输入 -4，mySqrt(-4) 抛出异常。函数 mySqrt() 不处理该异常，因此程序会查找调用堆栈中是否有函数会处理该异常。main() 也没有该异常的处理程序，因此找不到任何处理程序。
当找不到函数的异常处理程序时，会调用 std::terminate()，并且应用程序终止。在这种情况下，调用堆栈可能展开也可能不展开！如果堆栈未展开，则局部变量将不会被销毁，并且销毁这些变量时预期的任何清理都不会发生！
警告
如果异常未处理，调用堆栈可能展开也可能不展开。
如果堆栈未展开，则局部变量将不会被销毁，如果这些变量具有非平凡的析构函数，则可能会导致问题。
题外话…
尽管在这种情况下不展开堆栈似乎很奇怪，但有充分的理由不这样做。未处理的异常通常是您无论如何都想避免的。如果堆栈被展开，那么所有关于导致未处理异常抛出的堆栈状态的调试信息都将丢失！通过不展开，我们保留了这些信息，从而更容易确定未处理异常是如何抛出的，并修复它。
当异常未处理时，操作系统通常会通知您发生了未处理的异常错误。它如何做到这一点取决于操作系统，但可能性包括打印错误消息、弹出错误对话框或直接崩溃。有些操作系统不如其他操作系统优雅。通常这是您想避免的事情！
万能处理程序
现在我们陷入了两难境地
函数可能会抛出任何数据类型（包括程序定义的数据类型）的异常，这意味着有无限多种可能的异常类型可供捕获。
如果异常未被捕获，您的程序将立即终止（并且堆栈可能不会展开，因此您的程序甚至可能无法正确清理自身）。
为每种可能的类型添加显式捕获处理程序是繁琐的，特别是对于那些预期只在异常情况下才会遇到的类型！
幸运的是，C++ 还为我们提供了一种捕获所有类型异常的机制。这被称为**万能处理程序**。万能处理程序的工作方式与普通 catch 块完全相同，不同之处在于它不使用特定类型进行捕获，而是使用省略号运算符 (...) 作为要捕获的类型。因此，万能处理程序有时也称为“省略号捕获处理程序”。
如果您还记得第
20.5 课 — 省略号（以及为何要避免它们）
，省略号以前用于将任何类型的参数传递给函数。在此上下文中，它们表示任何数据类型的异常。这是一个简单的示例
#include <iostream>

int main()
{
	try
	{
		throw 5; // throw an int exception
	}
	catch (double x)
	{
		std::cout << "We caught an exception of type double: " << x << '\n';
	}
	catch (...) // catch-all handler
	{
		std::cout << "We caught an exception of an undetermined type\n";
	}
}
由于没有针对 int 类型的特定异常处理程序，因此万能处理程序会捕获此异常。此示例产生以下结果
We caught an exception of an undetermined type
万能处理程序必须放置在 catch 块链的最后。这是为了确保如果存在针对特定数据类型定制的异常处理程序，则异常可以被这些处理程序捕获。
通常，万能处理程序块是空的
catch(...) {} // ignore any unanticipated exceptions
这将捕获任何意外的异常，确保堆栈展开到此点并防止程序终止，但不会进行特定的错误处理。
使用万能处理程序包装 main()
万能处理程序的一个用途是包装 main() 的内容
#include <iostream>

struct GameSession
{
    // Game session data here
};

void runGame(GameSession&)
{
    throw 1;
}

void saveGame(GameSession&)
{
    // Save user's game here
}

int main()
{
    GameSession session{};

    try
    {
        runGame(session);
    }
    catch(...)
    {
        std::cerr << "Abnormal termination\n";
    }

    saveGame(session); // save the user's game (even if catch-all handler was hit)

    return 0;
}
在这种情况下，如果 runGame() 或它调用的任何函数抛出未处理的异常，它将被此万能处理程序捕获。堆栈将以有序的方式展开（确保局部变量的销毁）。这还将防止程序立即终止，使我们有机会打印我们选择的错误并在退出之前保存用户的状态。
提示
如果您的程序使用异常，请考虑在 main 中使用万能处理程序，以帮助确保在发生未处理异常时行为有序。
如果异常被万能处理程序捕获，您应该假定程序现在处于某种不确定状态，立即执行清理，然后终止。
调试未处理异常
未处理的异常表明发生了意想不到的事情，我们可能需要诊断为什么会抛出未处理的异常。许多调试器将（或可以配置为）在未处理的异常上中断，允许我们在抛出未处理异常的点查看堆栈。但是，如果我们有一个万能处理程序，那么所有异常都将被处理，并且（因为堆栈已展开）我们丢失了有用的诊断信息。
因此，在调试版本中，禁用万能处理程序可能很有用。我们可以通过条件编译指令来做到这一点。
这是一种方法
#include <iostream>

struct GameSession
{
    // Game session data here
};

void runGame(GameSession&)
{
    throw 1;
}

void saveGame(GameSession&)
{
    // Save user's game here
}

class DummyException // a dummy class that can't be instantiated
{
    DummyException() = delete;
}; 

int main()
{
    GameSession session {}; 

    try
    {
        runGame(session);
    }
#ifndef NDEBUG // if we're in release node
    catch(...) // compile in the catch-all handler
    {
        std::cerr << "Abnormal termination\n";
    }
#else // in debug mode, compile in a catch that will never be hit (for syntactic reasons)
    catch(DummyException)
    {
    }
#endif

    saveGame(session); // save the user's game (even if catch-all handler was hit)

    return 0;
}
从语法上讲，try 块至少需要一个关联的 catch 块。因此，如果万能处理程序被条件编译出，我们需要条件编译出 try 块，或者我们需要条件编译进另一个 catch 块。后一种做法更简洁。
为此，我们创建了
DummyException
类，它无法实例化，因为它有一个已删除的默认构造函数，并且没有其他构造函数。当定义了
NDEBUG
时，我们编译一个 catch 处理程序来捕获
DummyException
类型的异常。由于我们无法创建
DummyException
，因此此 catch 处理程序永远不会捕获任何内容。因此，任何到达此点的异常都将未处理。
下一课
27.5
异常、类和继承
返回目录
上一课
27.3
异常、函数和堆栈展开