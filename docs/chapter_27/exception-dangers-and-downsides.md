# 27.8 — 异常的危险和缺点

27.8 — 异常的危险和缺点
Alex
2008 年 10 月 26 日，太平洋夏令时 12:27
2024 年 10 月 31 日
正如几乎所有有益的事物一样，异常也有一些潜在的缺点。本文无意全面介绍，只指出在使用异常（或决定是否使用异常）时应考虑的一些主要问题。
清理资源
新程序员在使用异常时遇到的最大问题之一是异常发生时资源清理的问题。考虑以下示例
#include <iostream>

try
{
    openFile(filename);
    writeFile(filename, data);
    closeFile(filename);
}
catch (const FileException& exception)
{
    std::cerr << "Failed to write to file: " << exception.what() << '\n';
}
如果 WriteFile() 失败并抛出 FileException 会发生什么？此时，我们已经打开了文件，现在控制流跳转到 FileException 处理器，它会打印错误并退出。请注意，文件从未关闭！这个示例应该重写如下
#include <iostream>

try
{
    openFile(filename);
    writeFile(filename, data);
}
catch (const FileException& exception)
{
    std::cerr << "Failed to write to file: " << exception.what() << '\n';
}

// Make sure file is closed
closeFile(filename);
这种错误在处理动态分配的内存时经常以另一种形式出现
#include <iostream>

try
{
    auto* john { new Person{ "John", 18, PERSON_MALE } };
    processPerson(john);
    delete john;
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}
如果 processPerson() 抛出异常，控制流将跳转到 catch 处理器。结果，john 从未被释放！这个示例比上一个更棘手——因为 john 是 try 块的局部变量，当 try 块退出时它会超出范围。这意味着异常处理器根本无法访问 john（它已经被销毁了），所以无法释放内存。
然而，有两种相对简单的方法可以解决这个问题。首先，在 try 块外部声明 john，这样当 try 块退出时它就不会超出范围
#include <iostream>

Person* john{ nullptr };

try
{
    john = new Person("John", 18, PERSON_MALE);
    processPerson(john);
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}

delete john;
因为 john 是在 try 块外部声明的，所以它在 try 块内部和 catch 处理器中都可以访问。这意味着 catch 处理器可以正确地进行清理。
第二种方法是使用一个类的局部变量，该类在超出范围时知道如何清理自身（通常称为“智能指针”）。标准库提供了一个名为 std::unique_ptr 的类，可用于此目的。
std::unique_ptr
是一个模板类，它持有一个指针，并在超出范围时释放它。
#include <iostream>
#include <memory> // for std::unique_ptr

try
{
    auto* john { new Person("John", 18, PERSON_MALE) };
    std::unique_ptr<Person> upJohn { john }; // upJohn now owns john

    ProcessPerson(john);

    // when upJohn goes out of scope, it will delete john
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}
相关内容
我们在第
22.5 — std::unique_ptr
课中介绍
std::unique_ptr
。
最好的选择（只要可能）是优先堆栈分配实现 RAII（在构造时自动分配资源，在析构时释放资源）的对象。这样，当管理资源的对象因任何原因超出范围时，它将自动适当地释放，我们就不必担心这些事情了！
异常和析构函数
与构造函数不同，在构造函数中抛出异常是表示对象创建未成功的有用方式，但在析构函数中
绝不
应该抛出异常。
当在堆栈展开过程中从析构函数抛出异常时，问题就会发生。如果发生这种情况，编译器会陷入一种不知道是继续堆栈展开过程还是处理新异常的情况。最终结果是您的程序将立即终止。
因此，最好的做法是完全避免在析构函数中使用异常。而是将消息写入日志文件。
规则
如果在堆栈展开期间从析构函数抛出异常，程序将停止。
性能问题
异常确实会带来一些性能代价。它们会增加可执行文件的大小，并且由于必须执行额外的检查，它们也可能导致运行速度变慢。然而，异常的主要性能损失发生在实际抛出异常时。在这种情况下，必须展开堆栈并找到适当的异常处理程序，这是一个相对昂贵的操作。
值得注意的是，一些现代计算机架构支持一种称为零成本异常的异常模型。如果支持零成本异常，则在非错误情况下（这是我们最关心性能的情况）没有额外的运行时成本。但是，在发现异常的情况下，它们会带来更大的惩罚。
那么我应该什么时候使用异常呢？
当以下所有条件都满足时，异常处理是最好的选择
所处理的错误极少发生。
错误很严重，否则无法继续执行。
错误无法在其发生的地方处理。
没有其他好的方法可以将错误代码返回给调用者。
举例来说，让我们考虑这样一种情况：您编写了一个函数，该函数期望用户传入磁盘上文件的名称。您的函数将打开此文件，读取一些数据，关闭文件，并将一些结果传回给调用者。现在，假设用户传入了一个不存在的文件名或一个空字符串。这是一个适合使用异常的情况吗？
在这种情况下，上面的前两点很容易满足——这不会经常发生，而且您的函数在没有数据可处理时无法计算结果。该函数也无法处理错误——重新提示用户输入新文件名不是函数的工作，而且根据您的程序设计方式，这甚至可能不合适。第四点是关键——有没有其他好的方法可以将错误代码返回给调用者？这取决于您程序的具体细节。如果可以（例如，您可以返回空指针，或状态码表示失败），那可能是更好的选择。如果不能，那么异常是合理的。
下一课
27.9
异常规范和 noexcept
返回目录
上一课
27.7
函数 try 块