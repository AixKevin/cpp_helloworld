# 9.6 — Assert 和 static_assert

9.6 — Assert 和 static_assert
Alex
2017 年 5 月 14 日，下午 2:57 PDT
2024 年 11 月 2 日
在接受参数的函数中，调用者可能会传入语法有效但语义上无意义的实参。例如，在上一课（
9.4 -- 检测和处理错误
）中，我们展示了以下示例函数
void printDivision(int x, int y)
{
    if (y != 0)
        std::cout << static_cast<double>(x) / y;
    else
        std::cerr << "Error: Could not divide by zero\n";
}
该函数进行显式检查以查看
y
是否为
0
，因为除以零是语义错误，如果执行将导致程序崩溃。
在之前的课程中，我们讨论了几种处理此类问题的方法，包括中止程序或跳过违规语句。
但是，这两种选项都有问题。如果程序由于错误而跳过语句，那么它基本上是静默失败。尤其是在我们编写和调试程序时，静默失败是不好的，因为它们会掩盖实际问题。即使我们打印错误消息，该错误消息也可能在其他程序输出中丢失，并且可能不清楚错误消息是在哪里生成的，或者触发错误消息的条件是如何发生的。某些函数可能会被调用数十或数百次，如果其中只有一个案例产生了问题，则很难知道是哪一个。
如果程序终止（通过
std::exit
），那么我们将丢失调用栈和任何可能帮助我们隔离问题的调试信息。
std::abort
在这种情况下是一个更好的选择，因为通常会给开发人员提供在程序中止时开始调试的选项。
前置条件、不变式和后置条件
在编程中，
前置条件
是代码的某个部分（通常是函数体）执行之前必须为真的任何条件。在前面的示例中，我们检查
y != 0
是一个前置条件，它确保在除以
y
之前
y
具有非零值。
函数的前置条件最好放在函数的顶部，如果前置条件不满足，则使用早期返回以返回给调用者。例如
void printDivision(int x, int y)
{
    if (y == 0) // handle 
    {
        std::cerr << "Error: Could not divide by zero\n";
        return; // bounce the user back to the caller
    }

    // We now know that y != 0
    std::cout << static_cast<double>(x) / y;
}
选读
这有时被称为“保镖模式”，因为当检测到错误时，您会立即被从函数中弹出去。
保镖模式有两个主要优点
所有测试用例都在前面，并且测试用例和处理错误的代码在一起。
嵌套更少。
这是非保镖版本的样子
void printDivision(int x, int y)
{
    if (y != 0)
    {
        std::cout << static_cast<double>(x) / y;
    }
    else
    {
        std::cerr << "Error: Could not divide by zero\n";
        return; // bounce the user back to the caller
    }
}
此版本严格来说更差，因为测试用例和处理错误的代码更加分离，并且嵌套更多。
不变式
是代码的某个部分执行时必须为真的条件。这通常与循环一起使用，其中循环体只在不变式为真时执行。
致进阶读者
我们在第
14.2 -- 类介绍
课中讨论了一种常见的不变式，称为“类不变式”。
类似地，
后置条件
是代码的某个部分执行后必须为真的条件。我们的函数没有任何后置条件。
断言
使用条件语句检测无效参数（或验证其他类型的假设），以及打印错误消息和终止程序，是检测问题的常见方法，以至于 C++ 提供了一种快捷方式来执行此操作。
断言
是一个表达式，除非程序中存在错误，否则它将为真。如果表达式评估为
true
，则断言语句不执行任何操作。如果条件表达式评估为
false
，则显示错误消息并终止程序（通过
std::abort
）。此错误消息通常包含失败的表达式文本，以及代码文件名称和断言的行号。这使得不仅可以很容易地判断问题是什么，还可以判断问题发生在代码的哪个位置。这可以极大地帮助调试工作。
关键见解
断言用于在开发和调试期间检测错误。
当断言评估为 false 时，您的程序会立即停止。这使您有机会使用调试工具检查程序的状态并确定断言失败的原因。通过回溯，您可以快速找到并修复问题。
如果没有断言来检测错误并失败，此类错误可能会导致您的程序稍后出现故障。在这种情况下，很难确定哪里出了问题，或者问题的根本原因究竟是什么。
在 C++ 中，运行时断言通过
assert
预处理器宏实现，该宏位于 <cassert> 头文件中。
#include <cassert> // for assert()
#include <cmath> // for std::sqrt
#include <iostream>

double calculateTimeUntilObjectHitsGround(double initialHeight, double gravity)
{
  assert(gravity > 0.0); // The object won't reach the ground unless there is positive gravity.
 
  if (initialHeight <= 0.0)
  {
    // The object is already on the ground. Or buried.
    return 0.0;
  }
 
  return std::sqrt((2.0 * initialHeight) / gravity);
}

int main()
{
  std::cout << "Took " << calculateTimeUntilObjectHitsGround(100.0, -9.8) << " second(s)\n";

  return 0;
}
当程序调用
calculateTimeUntilObjectHitsGround(100.0, -9.8)
时，
assert(gravity > 0.0)
将评估为
false
，这将触发断言。这将打印一条类似以下内容的消息
dropsimulator: src/main.cpp:6: double calculateTimeUntilObjectHitsGround(double, double): Assertion 'gravity > 0.0' failed.
实际消息因您使用的编译器而异。
尽管断言最常用于验证函数参数，但它们可以在您希望验证某些事物为真的任何地方使用。
尽管我们之前告诉您要避免使用预处理器宏，但断言是少数被认为是可接受的预处理器宏之一。我们鼓励您在代码中大量使用断言语句。
关键见解
断言优于注释，因为它们既可以文档化又可以强制执行条件。当代码更改而注释未更新时，注释可能会过时。过时的断言是代码正确性问题，因此开发人员不太可能让它们被忽视。
使您的断言语句更具描述性
有时断言表达式的描述性不强。考虑以下语句
assert(found);
如果此断言被触发，断言将显示
Assertion failed: found, file C:\\VCProjects\\Test.cpp, line 34
这到底是什么意思？显然
found
是
false
（因为断言触发了），但是什么没有找到？您必须查看代码才能确定这一点。
幸运的是，有一个小技巧可以使您的断言语句更具描述性。只需添加一个通过逻辑 AND 连接的字符串文字
assert(found && "Car could not be found in database");
这就是它工作的原因：字符串字面量总是评估为布尔
true
。因此，如果
found
是
false
，则
false && true
是
false
。如果
found
是
true
，则
true && true
是
true
。因此，对字符串字面量进行逻辑 AND 操作不会影响断言的评估。
但是，当断言触发时，字符串字面量将包含在断言消息中
Assertion failed: found && "Car could not be found in database", file C:\\VCProjects\\Test.cpp, line 34
这为您提供了一些关于出了什么问题的额外上下文。
将断言用于未实现的功能
断言有时也用于记录程序员编写代码时不需要而未实现的情况
assert(moved && "Need to handle case where student was just moved to another classroom");
这样，如果开发人员遇到需要此情况的情况，代码将因有用的错误消息而失败，然后程序员可以确定如何实现该情况。
NDEBUG
assert
宏每次检查断言条件时都会产生很小的性能开销。此外，断言（理想情况下）绝不应在生产代码中遇到（因为您的代码应该已经经过彻底测试）。因此，大多数开发人员更喜欢断言仅在调试版本中处于活动状态。C++ 提供了一种内置方法来关闭生产代码中的断言：如果定义了预处理器宏
NDEBUG
，则断言宏将被禁用。
大多数 IDE 默认将
NDEBUG
设置为发布配置的项目设置的一部分。例如，在 Visual Studio 中，项目级别设置了以下预处理器定义：
WIN32;NDEBUG;_CONSOLE
。如果您使用 Visual Studio 并希望您的断言在发布版本中触发，则需要从此设置中删除
NDEBUG
。
如果您使用的 IDE 或构建系统未在发布配置中自动定义
NDEBUG
，则需要手动将其添加到项目或编译设置中。
提示
出于测试目的，您可以在给定翻译单元中启用或禁用断言。为此，请在任何 #includes
之前
将以下内容之一放在单独的行上：
#define NDEBUG
（禁用断言）或
#undef NDEBUG
（启用断言）。确保行尾没有分号。
例如
#define NDEBUG // disable asserts (must be placed before any #includes)
#include <cassert>
#include <iostream>

int main()
{
    assert(false); // won't trigger since asserts have been disabled in this translation unit
    std::cout << "Hello, world!\n";

    return 0;
}
static_assert
C++ 还有另一种断言类型，称为
static_assert
。
static_assert
是在编译时而不是运行时检查的断言，失败的
static_assert
会导致编译错误。与在 <cassert> 头文件中声明的 assert 不同，static_assert 是一个关键字，因此无需包含任何头文件即可使用它。
static_assert
采用以下形式
static_assert(condition, diagnostic_message)
如果条件不为真，则打印诊断消息。这是一个使用 static_assert 确保类型具有特定大小的示例
static_assert(sizeof(long) == 8, "long must be 8 bytes");
static_assert(sizeof(int) >= 4, "int must be at least 4 bytes");

int main()
{
	return 0;
}
在作者的机器上，编译时，编译器会报错
1>c:\consoleapplication1\main.cpp(19): error C2338: long must be 8 bytes
关于
static_assert
的一些有用说明
由于
static_assert
由编译器评估，因此条件必须是常量表达式。
static_assert
可以放置在代码文件中的任何位置（甚至在全局命名空间中）。
static_assert
不会在发布版本中禁用（与普通
assert
不同）。
由于编译器执行评估，
static_assert
没有运行时开销。
在 C++17 之前，诊断消息必须作为第二个参数提供。自 C++17 以来，提供诊断消息是可选的。
最佳实践
尽可能优先使用
static_assert
而不是
assert()
。
断言与错误处理
断言和错误处理足够相似，以至于它们的用途可能会混淆，因此让我们澄清一下。
断言用于在开发过程中通过记录对不应该发生的事情的假设来检测
编程错误
。如果它们确实发生了，那是程序员的错。断言不允许从错误中恢复（毕竟，如果某些事情不应该发生，就没有必要从中恢复）。由于断言通常在发布版本中被编译掉，因此您可以大量使用它们而无需担心性能，因此几乎没有理由不大量使用它们。
错误处理用于当我们需要在发布版本中优雅地处理可能发生（无论多么罕见）的情况。这些可能是可恢复的问题（程序可以继续运行），也可能是不可恢复的问题（程序必须关闭，但我们至少可以显示一条友好的错误消息并确保所有内容都已正确清理）。错误检测和处理既有运行时性能开销，也有开发时间开销。
在某些情况下，我们应该做什么不太清楚。考虑这样的函数
double getInverse(double x)
{
    return 1.0 / x;
}
如果
x
为
0.0
，此函数将出现错误，我们需要对此进行防范。我们应该使用断言还是错误处理？最好的答案可能是“两者”。
在调试期间，如果此函数在
x
为
0.0
时被调用，则表示我们的代码中某处存在错误，我们希望立即知道。因此断言绝对是合适的。
但是，这在发布版本中也可能合理发生（例如，沿着我们未测试的模糊路径）。如果断言被编译掉而我们没有错误处理，那么此函数将返回一些意外的值并出现错误。在这种情况下，最好检测并处理这种情况。
我们最终的函数可能看起来像这样
double getInverse(double x)
{
    assert(x != 0.0);
    if (x == 0.0)
       // handle error somehow (e.g. throw an exception)

    return 1.0 / x;
}
提示
鉴于此，我们建议如下
使用断言来检测编程错误、不正确的假设或在正确代码中不应该出现的条件。解决这些问题是程序员的责任，因此我们希望尽早发现它们。
将错误处理用于我们预计在程序正常运行期间会发生的问题。
在某些事情不应该发生但我们希望在发生时优雅地失败的情况下，两者都使用。
一些断言限制和警告
断言有一些陷阱和限制。首先，断言本身可能编写不正确。如果发生这种情况，断言将报告不存在的错误，或者未能报告存在的错误。
其次，您的
assert()
表达式不应有副作用，因为当定义
NDEBUG
时，断言表达式将不会被评估（因此副作用将不会应用）。否则，您在调试配置中测试的内容将与发布配置中测试的内容不同（假设您随 NDEBUG 发布）。
另请注意，
abort()
函数会立即终止程序，没有机会执行任何进一步的清理（例如关闭文件或数据库）。因此，断言只能用于程序意外终止时不太可能发生损坏的情况。
下一课
9.x
第 9 章总结和测验
返回目录
上一课
9.5
std::cin 和处理无效输入