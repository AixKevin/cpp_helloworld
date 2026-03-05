# 27.9 — 异常规范和 noexcept

27.9 — 异常规范和 noexcept
Alex
2020年8月11日，太平洋时间晚上9:16
2024年10月31日
（感谢读者 Koe 提供了这节课的初稿！）
查看一个典型的函数声明，无法确定函数是否会抛出异常
int doSomething(); // can this function throw an exception or not?
在上面的例子中，`doSomething()` 会抛出异常吗？不清楚。但在某些情况下，答案很重要。在第
27.8 课 -- 异常的危险和缺点
中，我们描述了在栈展开过程中从析构函数抛出的异常会导致程序停止。如果 `doSomething()` 可以抛出异常，那么从析构函数（或任何其他不希望抛出异常的地方）调用它是有风险的。虽然我们可以让析构函数处理 `doSomething()` 抛出的异常（这样这些异常就不会从析构函数中传播出去），但我们必须记住这样做，并且必须确保我们涵盖了所有可能抛出的不同类型的异常。
虽然注释可能有助于列举函数是否抛出异常（如果抛出，抛出哪种异常），但文档可能会过时，并且编译器不强制执行注释。
异常规范
是一种语言机制，最初设计用于记录函数作为函数规范的一部分可能抛出哪种异常。虽然大多数异常规范现已弃用或删除，但作为替代，添加了一个有用的异常规范，我们将在本课中介绍。
noexcept 说明符
在 C++ 中，所有函数都被归类为
不抛出异常
或
可能抛出异常
。
不抛出异常函数
是指承诺不向调用者抛出可见异常的函数。
可能抛出异常函数
可能会向调用者抛出可见异常。
要将函数定义为不抛出异常，我们可以使用
noexcept 说明符
。为此，我们在函数声明中使用 `noexcept` 关键字，放在函数参数列表的右侧
void doSomething() noexcept; // this function is specified as non-throwing
请注意，`noexcept` 实际上并不会阻止函数抛出异常或调用其他可能抛出异常的函数。只要 noexcept 函数在内部捕获并处理这些异常，并且这些异常不会退出 noexcept 函数，这是允许的。
如果未处理的异常将退出 noexcept 函数，则会调用 `std::terminate`（即使堆栈上某处有异常处理程序可以处理此类异常）。如果从 noexcept 函数内部调用 `std::terminate`，栈展开可能会或可能不会发生（取决于实现和优化），这意味着您的对象在终止之前可能无法正确销毁。
关键见解
noexcept 函数承诺不向调用者抛出可见异常是一种契约承诺，而不是编译器强制的承诺。因此，虽然调用 noexcept 函数应该是安全的，但 noexcept 函数中导致契约被破坏的任何异常处理错误都将导致程序终止！这不应该发生，但错误也不应该发生。
因此，最好 noexcept 函数根本不处理异常，或者不调用可能引发异常的潜在抛出函数。如果一开始就不可能引发异常，noexcept 函数就不会有异常处理错误！
就像仅返回值不同的函数不能重载一样，仅异常规范不同的函数也不能重载。
说明 noexcept 函数和异常的行为
以下程序说明了 noexcept 函数和异常在各种情况下的行为
// h/t to reader yellowEmu for the first draft of this program
#include <iostream>

class Doomed
{
public:
    ~Doomed()
    {
        std::cout << "Doomed destructed\n";
    }
};

void thrower()
{
    std::cout << "Throwing exception\n";
    throw 1;
}

void pt()
{
    std::cout << "pt (potentally throwing) called\n";
    //This object will be destroyed during stack unwinding (if it occurs)
    Doomed doomed{};
    thrower();
    std::cout << "This never prints\n";
}

void nt() noexcept
{
    std::cout << "nt (noexcept) called\n";
    //This object will be destroyed during stack unwinding (if it occurs)
    Doomed doomed{};
    thrower();
    std::cout << "this never prints\n";
}

void tester(int c) noexcept
{
    std::cout << "tester (noexcept) case " << c << " called\n";
    try
    {
        (c == 1) ? pt() : nt();
    }
    catch (...)
    {
        std::cout << "tester caught exception\n";
    }
}

int main()
{
    std::cout << std::unitbuf; // flush buffer after each insertion
    std::cout << std::boolalpha; // print boolean as true/false
    tester(1);
    std::cout << "Test successful\n\n";
    tester(2);
    std::cout << "Test successful\n";

    return 0;
}
在作者的机器上，此程序打印
tester (noexcept) case 1 called
pt (potentially throwing) called
Throwing exception
Doomed destructed
tester caught exception
Test successful

tester (noexcept) case 2 called
nt (noexcept) called
throwing exception
terminate called after throwing an instance of 'int'
然后程序中止。
让我们更详细地探讨这里发生的事情。请注意，`tester` 是一个 noexcept 函数，因此承诺不向调用者（`main`）暴露任何异常。
第一个案例说明 noexcept 函数可以调用潜在抛出函数，甚至可以处理这些函数抛出的任何异常。首先，调用 `tester(1)`，它调用潜在抛出函数 `pt`，后者调用 `thrower`，它抛出异常。此异常的第一个处理程序在 `tester` 中，因此异常展开堆栈（在此过程中销毁局部变量 `doomed`），并且异常在 `tester` 中被捕获和处理。因为 `tester` 没有将此异常暴露给调用者（`main`），所以此处没有违反 noexcept，并且控制权返回到 `main`。
第二个案例说明当 noexcept 函数尝试将异常传回其调用者时会发生什么。首先，调用 `tester(2)`，它调用非抛出函数 `nt`，后者调用 `thrower`，它抛出异常。此异常的第一个处理程序在 `tester` 中。但是，`nt` 是 noexcept，并且要到达 `tester` 中的处理程序，异常必须传播到 `nt` 的调用者。这违反了 `nt` 的 noexcept，因此调用 `std::terminate`，并且我们的程序立即中止。在作者的机器上，堆栈没有展开（如 `doomed` 未被销毁所示）。
带有布尔参数的 noexcept 说明符
`noexcept` 说明符有一个可选的布尔参数。`noexcept(true)` 等同于 `noexcept`，意味着函数是不抛出异常的。`noexcept(false)` 意味着函数是潜在抛出异常的。这些参数通常只用于模板函数中，以便模板函数可以根据某些参数化值动态创建为不抛出异常或潜在抛出异常。
哪些函数是不抛出异常的和潜在抛出异常的
隐式不抛出异常的函数
析构函数
对于隐式声明或默认函数，默认情况下不抛出异常的函数
构造函数：默认、复制、移动
赋值：复制、移动
比较运算符（从 C++20 开始）
但是，如果这些函数中的任何一个（显式或隐式）调用另一个潜在抛出异常的函数，那么列出的函数也将被视为潜在抛出异常。例如，如果一个类有一个数据成员，其构造函数是潜在抛出异常的，那么该类的构造函数也将被视为潜在抛出异常。再例如，如果一个复制赋值运算符调用一个潜在抛出异常的赋值运算符，那么复制赋值也将是潜在抛出异常的。
潜在抛出异常的函数（如果不是隐式声明或默认的）
普通函数
用户定义的构造函数
用户定义的运算符
noexcept 运算符
noexcept 运算符也可以在表达式内部使用。它接受一个表达式作为参数，如果编译器认为它会抛出异常，则返回 `true` 或 `false`。noexcept 运算符在编译时静态检查，并且实际上不评估输入表达式。
void foo() {throw -1;}
void boo() {};
void goo() noexcept {};
struct S{};

constexpr bool b1{ noexcept(5 + 3) }; // true; ints are non-throwing
constexpr bool b2{ noexcept(foo()) }; // false; foo() throws an exception
constexpr bool b3{ noexcept(boo()) }; // false; boo() is implicitly noexcept(false)
constexpr bool b4{ noexcept(goo()) }; // true; goo() is explicitly noexcept(true)
constexpr bool b5{ noexcept(S{}) };   // true; a struct's default constructor is noexcept by default
noexcept 运算符可用于根据代码是否潜在抛出异常来有条件地执行代码。这对于满足某些
异常安全保证
是必需的，我们将在下一节中讨论。
异常安全保证
异常安全保证
是关于函数或类在发生异常时将如何表现的契约指南。异常安全保证有四个级别
无保证 -- 如果抛出异常，则不保证会发生什么（例如，类可能会处于不可用状态）
基本保证 -- 如果抛出异常，不会发生内存泄漏，并且对象仍然可用，但程序可能处于修改状态。
强保证 -- 如果抛出异常，不会发生内存泄漏，并且程序状态不会改变。这意味着函数必须完全成功，否则如果失败则没有副作用。如果失败发生在任何修改之前，这很容易实现，但也可以通过回滚任何更改来使程序恢复到失败前的状态来实现。
不抛出 / 不失败保证 -- 函数将始终成功（不失败）或失败而不向调用者抛出异常（不抛出）。如果未暴露，异常可能会在内部抛出。`noexcept` 说明符映射到此级别的异常安全保证。
让我们更详细地看看不抛出/不失败保证
不抛出保证：如果函数失败，则不会抛出异常。相反，它将返回错误代码或忽略问题。在异常已经处理时，栈展开期间需要不抛出保证；例如，所有析构函数都应该具有不抛出保证（以及这些析构函数调用的任何函数）。应为不抛出的代码示例
析构函数和内存释放/清理函数
更高级别的不抛出函数需要调用的函数
不失败保证：函数将始终成功地完成其尝试做的事情（因此永远不需要抛出异常，因此，不失败是比不抛出稍强的形式）。应为不失败的代码示例
移动构造函数和移动赋值（移动语义，在
第 22 章
中介绍）
交换函数
容器上的 clear/erase/reset 函数
std::unique_ptr 上的操作（也在
第 22 章
中介绍）
更高级别的不失败函数需要调用的函数
何时使用 noexcept
仅仅因为您的代码没有显式抛出任何异常，并不意味着您应该开始在代码中随意添加 `noexcept`。默认情况下，大多数函数都是潜在抛出异常的，因此如果您的函数调用其他函数，很有可能它会调用一个潜在抛出异常的函数，因此它本身也是潜在抛出异常的。
有几个充分的理由将函数标记为不抛出异常
不抛出异常的函数可以安全地从非异常安全的函数中调用，例如析构函数
noexcept 函数可以使编译器执行一些否则无法获得的优化。因为 noexcept 函数不能在函数外部抛出异常，所以编译器不必担心保持运行时堆栈处于可展开状态，这可以使其生成更快的代码。
在某些重要情况下，知道一个函数是 noexcept 允许我们在自己的代码中生成更高效的实现：标准库容器（如 `std::vector`）是 noexcept 感知的，并且会在某些地方使用 noexcept 运算符来确定是使用 `移动语义`（更快）还是 `复制语义`（更慢）。我们在
第 22 章
中介绍了移动语义，并在
27.10 课 -- std::move_if_noexcept
中介绍了这种优化。
标准库的策略是仅在“不得”抛出或失败的函数上使用 `noexcept`。潜在抛出异常但实际上不抛出异常的函数（由于实现原因）通常不标记为 `noexcept`。
对于您自己的代码，始终将以下内容标记为 `noexcept`
移动构造函数
移动赋值运算符
交换函数
对于您的代码，考虑将以下内容标记为 `noexcept`
您希望表达不抛出或不失败保证的函数（例如，记录它们可以安全地从析构函数或其他 noexcept 函数中调用）
不抛出异常的复制构造函数和复制赋值运算符（以利用优化）。
析构函数。只要所有成员都有 noexcept 析构函数，析构函数就是隐式 noexcept 的
最佳实践
始终将移动构造函数、移动赋值和交换函数设置为 `noexcept`。
尽可能将复制构造函数和复制赋值运算符设置为 `noexcept`。
在其他函数上使用 `noexcept` 以表达不失败或不抛出保证。
最佳实践
如果您不确定函数是否应具有不失败/不抛出保证，请谨慎行事，不要用 `noexcept` 标记它。撤销使用 noexcept 的决定会违反向用户做出的关于函数行为的接口承诺，并可能破坏现有代码。通过稍后向最初不是 noexcept 的函数添加 noexcept 来加强保证被认为是安全的。
动态异常规范
选读
在 C++11 之前，直到 C++17，
动态异常规范
取代了 `noexcept`。
动态异常规范
语法使用 `throw` 关键字列出函数可能直接或间接抛出的异常类型
int doSomething() throw(); // does not throw exceptions
int doSomething() throw(std::out_of_range, int*); // may throw either std::out_of_range or a pointer to an integer
int doSomething() throw(...); // may throw anything
由于不完整的编译器实现、与模板函数的一些不兼容、对它们如何工作的常见误解以及标准库大多不使用它们等因素，动态异常规范在 C++11 中被弃用，并在 C++17 和 C++20 中从语言中删除。有关更多上下文，请参阅
本文
。
下一课
27.10
std::move_if_noexcept
返回目录
上一课
27.8
异常的危险和缺点