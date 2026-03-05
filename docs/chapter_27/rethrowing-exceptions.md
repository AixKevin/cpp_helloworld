# 27.6 — 重新抛出异常

27.6 — 重新抛出异常
Alex
2017年2月5日，下午2:10（太平洋标准时间）
2024年8月15日
有时你可能会遇到这样一种情况：你想捕获一个异常，但又不想（或无法）在捕获它的地方完全处理它。当你想要记录错误，但又想将问题传递给调用者实际处理时，这种情况很常见。
当函数可以使用返回代码时，这很简单。考虑以下示例
Database* createDatabase(std::string filename)
{
    Database* d {};

    try
    {
        d = new Database{};
        d->open(filename); // assume this throws an int exception on failure
        return d;
    }
    catch (int exception)
    {
        // Database creation failed
        delete d;
        // Write an error to some global logfile
        g_log.logError("Creation of Database failed");
    }

    return nullptr;
}
在上面的代码片段中，函数负责创建数据库对象、打开数据库并返回数据库对象。如果出现问题（例如，传递了错误的文件名），异常处理程序会记录错误，然后合理地返回一个空指针。
现在考虑以下函数
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // throws int exception on failure
    }
    catch (int exception)
    {
        // Write an error to some global logfile
        g_log.logError("getIntValueFromDatabase failed");

        // However, we haven't actually handled this error
        // So what do we do here?
    }
}
如果此函数成功，它会返回一个整数值——任何整数值都可能是有效值。
但是，如果 `getIntValue()` 出现问题怎么办？在这种情况下，`getIntValue()` 将抛出一个整数异常，该异常将被 `getIntValueFromDatabase()` 中的 `catch` 块捕获，并记录错误。但是，我们如何告诉 `getIntValueFromDatabase()` 的调用者出现了问题呢？与上面的示例不同，这里没有好的返回代码可以使用（因为任何整数返回值都可能是有效值）。
抛出新异常
一个显而易见的解决方案是抛出新异常。
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // throws int exception on failure
    }
    catch (int exception)
    {
        // Write an error to some global logfile
        g_log.logError("getIntValueFromDatabase failed");

        // Throw char exception 'q' up the stack to be handled by caller
        throw 'q'; 
    }
}
在上面的示例中，程序捕获了来自 `getIntValue()` 的 int 异常，记录了错误，然后抛出了一个带有 char 值 'q' 的新异常。尽管从 `catch` 块中抛出异常可能看起来很奇怪，但这是允许的。请记住，只有在 `try` 块中抛出的异常才能被捕获。这意味着在 `catch` 块中抛出的异常不会被它所在的 `catch` 块捕获。相反，它将沿着栈向上传播给调用者。
从 `catch` 块中抛出的异常可以是任何类型的异常——它不必与刚捕获的异常类型相同。
重新抛出异常（错误的方式）
另一种选择是重新抛出相同的异常。一种方法如下
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // throws int exception on failure
    }
    catch (int exception)
    {
        // Write an error to some global logfile
        g_log.logError("getIntValueFromDatabase failed");

        throw exception;
    }
}
尽管这可行，但这种方法有几个缺点。首先，这不会抛出与捕获的异常完全相同的异常——相反，它会抛出变量异常的拷贝初始化副本。尽管编译器可以自由地省略拷贝，但它可能不会，因此这可能会降低性能。
但更重要的是，考虑以下情况会发生什么
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // throws Derived exception on failure
    }
    catch (Base& exception)
    {
        // Write an error to some global logfile
        g_log.logError("getIntValueFromDatabase failed");

        throw exception; // Danger: this throws a Base object, not a Derived object
    }
}
在这种情况下，`getIntValue()` 抛出 `Derived` 对象，但 `catch` 块捕获 `Base` 引用。这没问题，因为我们知道我们可以将 `Base` 引用指向 `Derived` 对象。但是，当我们抛出异常时，抛出的异常是使用变量异常拷贝初始化的。变量异常的类型是 `Base`，因此拷贝初始化的异常的类型也是 `Base`（而不是 `Derived`！）。换句话说，我们的 `Derived` 对象被“切片”了！
你可以在以下程序中看到这一点
#include <iostream>
class Base
{
public:
    Base() {}
    virtual void print() { std::cout << "Base"; }
};

class Derived: public Base
{
public:
    Derived() {}
    void print() override { std::cout << "Derived"; }
};

int main()
{
    try
    {
        try
        {
            throw Derived{};
        }
        catch (Base& b)
        {
            std::cout << "Caught Base b, which is actually a ";
            b.print();
            std::cout << '\n';
            throw b; // the Derived object gets sliced here
        }
    }
    catch (Base& b)
    {
        std::cout << "Caught Base b, which is actually a ";
        b.print();
        std::cout << '\n';
    }

    return 0;
}
这会打印
Caught Base b, which is actually a Derived
Caught Base b, which is actually a Base
第二行表明 `Base` 实际上是 `Base` 而不是 `Derived`，这证明了 `Derived` 对象被切片了。
重新抛出异常（正确的方式）
幸运的是，C++ 提供了一种方法来重新抛出与刚捕获的异常完全相同的异常。为此，只需在 `catch` 块中使用 `throw` 关键字（不带任何关联变量），如下所示
#include <iostream>
class Base
{
public:
    Base() {}
    virtual void print() { std::cout << "Base"; }
};

class Derived: public Base
{
public:
    Derived() {}
    void print() override { std::cout << "Derived"; }
};

int main()
{
    try
    {
        try
        {
            throw Derived{};
        }
        catch (Base& b)
        {
            std::cout << "Caught Base b, which is actually a ";
            b.print();
            std::cout << '\n';
            throw; // note: We're now rethrowing the object here
        }
    }
    catch (Base& b)
    {
        std::cout << "Caught Base b, which is actually a ";
        b.print();
        std::cout << '\n';
    }

    return 0;
}
这会打印
Caught Base b, which is actually a Derived
Caught Base b, which is actually a Derived
这个看起来没有抛出任何特定内容的 `throw` 关键字实际上重新抛出了刚刚捕获的异常。没有进行拷贝，这意味着我们不必担心性能下降的拷贝或切片问题。
如果需要重新抛出异常，应优先使用此方法，而不是其他替代方法。
规则
重新抛出相同的异常时，单独使用 `throw` 关键字
下一课
27.7
函数 try 块
返回目录
上一课
27.5
异常、类和继承