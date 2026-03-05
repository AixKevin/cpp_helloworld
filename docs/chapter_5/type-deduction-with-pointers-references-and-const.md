# 12.14 — 指针、引用和 const 的类型推导

12.14 — 指针、引用和 const 的类型推导
Alex
2022 年 2 月 2 日，太平洋标准时间下午 2:56
2025 年 1 月 21 日
在
10.8 课 —— 使用 auto 关键字的对象类型推导
中，我们讨论了如何使用
auto
关键字让编译器从初始化器中推导出变量的类型。
int main()
{
    int a { 5 };
    auto b { a }; // b deduced as an int

    return 0;
}
我们还注意到，默认情况下，类型推导会从类型中去除
const
。
int main()
{
    const double a { 7.8 }; // a has type const double
    auto b { a };           // b has type double (const dropped)

    constexpr double c { 7.8 }; // c has type const double (constexpr implicitly applies const)
    auto d { c };               // d has type double (const dropped)

    return 0;
}
可以通过向推导类型的定义添加
const
（或
constexpr
）限定符来重新应用 const（或 constexpr）。
int main()
{
    double a { 7.8 };    // a has type double
    const auto b { a };  // b has type const double (const applied)

    constexpr double c { 7.8 }; // c has type const double (constexpr implicitly applies const)
    const auto d { c };         // d is const double (const dropped, const reapplied)
    constexpr auto e { c };     // e is constexpr double (const dropped, constexpr reapplied)

    return 0;
}
类型推导会去除引用。
除了去除 const，类型推导还会去除引用。
#include <string>

std::string& getRef(); // some function that returns a reference

int main()
{
    auto ref { getRef() }; // type deduced as std::string (not std::string&)

    return 0;
}
在上面的示例中，变量
ref
使用类型推导。尽管函数
getRef()
返回
std::string&
，但引用限定符被去除了，因此
ref
的类型被推导为
std::string
。
就像被去除的
const
一样，如果你希望推导类型是引用，可以在定义时重新应用引用。
#include <string>

std::string& getRef(); // some function that returns a reference

int main()
{
    auto ref1 { getRef() };  // std::string (reference dropped)
    auto& ref2 { getRef() }; // std::string& (reference dropped, reference reapplied)

    return 0;
}
顶层 const 和底层 const
顶层 const
是应用于对象本身的 const 限定符。例如：
const int x;    // this const applies to x, so it is top-level
int* const ptr; // this const applies to ptr, so it is top-level
// references don't have a top-level const syntax, as they are implicitly top-level const
相反，
底层 const
是应用于被引用或被指向的对象的 const 限定符。
const int& ref; // this const applies to the object being referenced, so it is low-level
const int* ptr; // this const applies to the object being pointed to, so it is low-level
对 const 值的引用始终是底层 const。指针可以具有顶层、底层或两种 const。
const int* const ptr; // the left const is low-level, the right const is top-level
当我们说类型推导会去除 const 限定符时，它只会去除顶层 const。底层 const 不会被去除。我们稍后会看到示例。
类型推导和 const 引用
如果初始化器是对 const 的引用，则首先去除引用（如果适用则重新应用），然后从结果中去除任何顶层 const。
#include <string>

const std::string& getConstRef(); // some function that returns a reference to const

int main()
{
    auto ref1{ getConstRef() }; // std::string (reference dropped, then top-level const dropped from result)

    return 0;
}
在上面的示例中，由于
getConstRef()
返回
const std::string&
，因此首先去除引用，留下
const std::string
。此 const 现在是顶层 const，因此它也被去除，将推导类型保留为
std::string
。
关键见解
去除引用可能会将底层 const 更改为顶层 const：
const std::string&
是底层 const，但去除引用会产生
const std::string
，这是一个顶层 const。
我们可以重新应用引用和/或 const。
#include <string>

const std::string& getConstRef(); // some function that returns a const reference

int main()
{
    auto ref1{ getConstRef() };        // std::string (reference and top-level const dropped)
    const auto ref2{ getConstRef() };  // const std::string (reference dropped, const dropped, const reapplied)

    auto& ref3{ getConstRef() };       // const std::string& (reference dropped and reapplied, low-level const not dropped)
    const auto& ref4{ getConstRef() }; // const std::string& (reference dropped and reapplied, low-level const not dropped)

    return 0;
}
我们在前面的示例中讨论了
ref1
的情况。对于
ref2
，这与
ref1
的情况类似，只是我们重新应用了
const
限定符，因此推导类型是
const std::string
。
ref3
的情况更有趣。通常引用会首先被去除，但由于我们重新应用了引用，它没有被去除。这意味着类型仍然是
const std::string&
。由于此 const 是底层 const，因此它没有被去除。因此推导类型是
const std::string&
。
ref4
的情况与
ref3
类似，只是我们也重新应用了
const
限定符。由于类型已经推导为对 const 的引用，因此我们在这里重新应用
const
是多余的。也就是说，在这里使用
const
明确表明我们的结果将是 const（而在
ref3
的情况下，结果的 const 性是隐式的且不明显）。
最佳实践
如果你想要 const 引用，即使没有严格必要，也要重新应用
const
限定符，因为它使你的意图清晰并有助于防止错误。
constexpr 引用呢？
Constexpr 不是表达式类型的一部分，因此
auto
不会推导它。
提醒
当定义 const 引用（例如
const int&
）时，const 适用于被引用的对象，而不是引用本身。
当定义对 const 变量的 constexpr 引用（例如
constexpr const int&
）时，我们需要同时应用
constexpr
（适用于引用）和
const
（适用于被引用的类型）。
这在
12.4 课 —— 对 const 的左值引用
中有所介绍。
#include <string_view>
#include <iostream>

constexpr std::string_view hello { "Hello" };   // implicitly const

constexpr const std::string_view& getConstRef() // function is constexpr, returns a const std::string_view&
{
    return hello;
}

int main()
{
    auto ref1{ getConstRef() };                  // std::string_view (reference dropped and top-level const dropped)
    constexpr auto ref2{ getConstRef() };        // constexpr const std::string_view (reference dropped and top-level const dropped, constexpr applied, implicitly const)

    auto& ref3{ getConstRef() };                 // const std::string_view& (reference reapplied, low-level const not dropped)
    constexpr const auto& ref4{ getConstRef() }; // constexpr const std::string_view& (reference reapplied, low-level const not dropped, constexpr applied)
    
    return 0;
}
类型推导和指针
与引用不同，类型推导不会去除指针。
#include <string>

std::string* getPtr(); // some function that returns a pointer

int main()
{
    auto ptr1{ getPtr() }; // std::string*

    return 0;
}
我们还可以将星号与指针类型推导 (
auto*
) 结合使用，以使其更清楚推导类型是指针。
#include <string>

std::string* getPtr(); // some function that returns a pointer

int main()
{
    auto ptr1{ getPtr() };  // std::string*
    auto* ptr2{ getPtr() }; // std::string*

    return 0;
}
关键见解
引用在类型推导过程中被去除而指针不被去除的原因是引用和指针具有不同的语义。
当我们求值一个引用时，我们实际上是在求值被引用的对象。因此，在推导类型时，推导被引用对象的类型而不是引用本身的类型是合理的。此外，由于我们推导的是非引用类型，因此使用
auto&
很容易将其转换为引用。如果类型推导推导为引用，那么如果我们不想要引用，删除引用的语法会复杂得多。
另一方面，指针保存对象的地址。当我们求值一个指针时，我们求值的是指针，而不是被指向的对象（如果我们需要，可以解引用指针）。因此，推导指针的类型而不是被指向对象的类型是合理的。
auto 和 auto* 之间的区别
可选
当我们使用
auto
和指针类型初始化器时，为
auto
推导的类型包含指针。因此对于上面的
ptr1
，替换
auto
的类型是
std::string*
。
当我们使用
auto*
和指针类型初始化器时，为 auto 推导的类型
不
包含指针——指针在类型推导后重新应用。因此对于上面的
ptr2
，替换
auto
的类型是
std::string
，然后指针被重新应用。
在大多数情况下，实际效果是相同的（在上面的示例中，
ptr1
和
ptr2
都推导为
std::string*
）。
然而，
auto
和
auto*
在实践中存在一些差异。首先，
auto*
必须解析为指针初始化器，否则会导致编译错误。
#include <string>

std::string* getPtr(); // some function that returns a pointer

int main()
{
    auto ptr3{ *getPtr() };      // std::string (because we dereferenced getPtr())
    auto* ptr4{ *getPtr() };     // does not compile (initializer not a pointer)

    return 0;
}
这很合理：在
ptr4
的情况下，
auto
推导为
std::string
，然后重新应用指针。因此
ptr4
的类型是
std::string*
，我们不能用非指针的初始化器初始化
std::string*
。
其次，当我们在等式中引入
const
时，
auto
和
auto*
的行为存在差异。我们将在下面介绍。
类型推导和 const 指针
可选
由于指针不会被去除，所以我们不必担心这一点。但是对于指针，我们必须考虑 const 指针和指向 const 的指针两种情况，我们还有
auto
与
auto*
的区别。就像引用一样，在指针类型推导期间只去除顶层 const。底层 const 不会被去除。
让我们从一个简单的例子开始。
#include <string>

std::string* getPtr(); // some function that returns a pointer

int main()
{
    const auto ptr1{ getPtr() };  // std::string* const
    auto const ptr2 { getPtr() }; // std::string* const

    const auto* ptr3{ getPtr() }; // const std::string*
    auto* const ptr4{ getPtr() }; // std::string* const

    return 0;
}
当我们使用
auto const
或
const auto
时，我们说的是“使推导出的指针成为 const 指针”。因此在
ptr1
和
ptr2
的情况下，推导出的类型是
std::string*
，然后应用 const，使最终类型为
std::string* const
。这类似于
const int
和
int const
含义相同。
但是，当我们使用
auto*
时，const 限定符的顺序很重要。左侧的
const
意味着“使推导出的指针成为指向 const 的指针”，而右侧的
const
意味着“使推导出的指针类型成为 const 指针”。因此
ptr3
最终成为指向 const 的指针，而
ptr4
最终成为 const 指针。
现在我们来看一个初始化器是指向 const 的 const 指针的例子。
#include <string>

int main()
{
    std::string s{};
    const std::string* const ptr { &s };

    auto ptr1{ ptr };  // const std::string*
    auto* ptr2{ ptr }; // const std::string*

    auto const ptr3{ ptr };  // const std::string* const
    const auto ptr4{ ptr };  // const std::string* const

    auto* const ptr5{ ptr }; // const std::string* const
    const auto* ptr6{ ptr }; // const std::string*

    const auto const ptr7{ ptr };  // error: const qualifer can not be applied twice
    const auto* const ptr8{ ptr }; // const std::string* const

    return 0;
}
ptr1
和
ptr2
的情况很简单。顶层 const（指针本身的 const）被去除。指向对象的底层 const 不会被去除。因此在两种情况下，最终类型都是
const std::string*
。
ptr3
和
ptr4
的情况也很简单。顶层 const 被去除，但我们重新应用它。指向对象的底层 const 不会被去除。因此在两种情况下，最终类型都是
const std::string* const
。
ptr5
和
ptr6
的情况类似于我们上一个示例中展示的情况。在这两种情况下，顶层 const 都会被去除。对于
ptr5
，
auto* const
重新应用了顶层 const，因此最终类型是
const std::string* const
。对于
ptr6
，
const auto*
将 const 应用于被指向的类型（在本例中已经是 const），因此最终类型是
const std::string*
。
在
ptr7
的情况下，我们两次应用 const 限定符，这是不允许的，会导致编译错误。
最后，在
ptr8
的情况下，我们在指针的两侧应用 const（这是允许的，因为
auto*
必须是指针类型），所以结果类型是
const std::string* const
。
最佳实践
如果你想要一个 const 指针，指向 const 的指针，或指向 const 的 const 指针，即使没有严格必要，也要重新应用
const
限定符，因为它能清楚表达你的意图并有助于防止错误。
提示
推导指针类型时，考虑使用
auto*
。在这种情况下使用
auto*
可以更清楚地表明我们正在推导指针类型，并借助编译器的帮助确保我们不会推导出非指针类型，同时让你对 const 有更多控制。
总结
很抱歉您头疼。让我们快速回顾一下最重要的几点。
顶层 const 与底层 const
顶层 const 适用于对象本身（例如
const int x
或
int* const ptr
）。
底层 const 适用于通过引用或指针访问的对象（例如
const int& ref
、
const int* ptr
）。
类型推导推导出什么
类型推导首先去除任何引用（除非推导类型定义为引用）。对于 const 引用，去除引用将导致（底层）const 变为顶层 const。
类型推导然后去除任何顶层 const（除非推导类型定义为
const
或
constexpr
）。
Constexpr 不是类型系统的一部分，因此永远不会被推导。它必须始终明确应用于推导类型。
类型推导不会去除指针。
始终将推导类型明确定义为引用、
const
或
constexpr
（如适用），即使这些限定符是多余的，因为它们会被推导出来。这有助于防止错误并明确你的意图。
类型推导和指针
使用
auto
时，只有当初始化器是指针时，推导类型才会是指针。使用
auto*
时，即使初始化器不是指针，推导类型也始终是指针。
auto const
和
const auto
都使推导出的指针成为 const 指针。无法使用
auto
明确指定底层 const（指向 const 的指针）。
auto* const
也使推导出的指针成为 const 指针。
const auto*
使推导出的指针成为指向 const 的指针。如果这些很难记住，
int* const
是一个 const 指针（指向 int），所以
auto* const
必须是一个 const 指针。
const int*
是一个指向 const 的指针（int），所以
const auto*
必须是一个指向 const 的指针）。
在推导指针类型时，考虑使用
auto*
而不是
auto
，因为它允许你明确地重新应用顶层和底层 const，并且如果未推导出指针类型，则会出错。
下一课
12.15
std::optional
返回目录
上一课
12.13
输入和输出参数