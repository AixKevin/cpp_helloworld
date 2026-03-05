# 7.8 — 为什么（非 const）全局变量是邪恶的

7.8 — 为什么（非 const）全局变量是邪恶的
Alex
2015年3月23日，下午3:59 PDT
2025年1月29日
如果你向一位经验丰富的程序员请教关于良好编程实践的“一条”建议，经过一番思考，最可能的答案会是：“避免使用全局变量！”。这有充分的理由：全局变量是语言中历史上最常被滥用的概念之一。尽管它们在小型学术程序中看似无害，但在大型程序中常常会引发问题。
新程序员经常被诱惑使用大量全局变量，因为它们易于使用，尤其是在涉及对不同函数的多次调用时（通过函数参数传递数据很麻烦）。然而，这通常是一个坏主意。许多开发者认为应该完全避免使用非 const 全局变量！
但在我们探讨原因之前，我们应该先澄清一点。当开发者告诉你全局变量是邪恶的时候，他们通常不是指所有全局变量。他们大多是指非 const 全局变量。
为什么（非 const）全局变量是邪恶的
非 const 全局变量危险的最大原因在于它们的值可以被**任何**被调用的函数更改，而且程序员很难知道这会发生。考虑以下程序：
#include <iostream>

int g_mode; // declare global variable (will be zero-initialized by default)

void doSomething()
{
    g_mode = 2; // set the global g_mode variable to 2
}

int main()
{
    g_mode = 1; // note: this sets the global g_mode variable to 1.  It does not declare a local g_mode variable!

    doSomething();

    // Programmer still expects g_mode to be 1
    // But doSomething changed it to 2!

    if (g_mode == 1)
    {
        std::cout << "No threat detected.\n";
    }
    else
    {
        std::cout << "Launching nuclear missiles...\n";
    }

    return 0;
}
请注意，程序员将变量 `g_mode` 设置为 `1`，然后调用了 `doSomething()`。除非程序员明确知道 `doSomething()` 会更改 `g_mode` 的值，否则他或她可能没有预料到 `doSomething()` 会更改该值！因此，`main()` 的其余部分没有按照程序员的预期工作（世界被摧毁了）。
简而言之，全局变量使程序的状态变得不可预测。每次函数调用都可能变得危险，而程序员无法轻易知道哪些是危险的，哪些不是！局部变量要安全得多，因为其他函数无法直接影响它们。
不使用非 const 全局变量还有很多其他充分的理由。
使用全局变量时，代码中不乏如下所示的片段：
void someFunction()
{
    // useful code

    if (g_mode == 4)
    {
        // do something good
    }
}
调试后，你确定你的程序没有正常工作，因为 `g_mode` 的值为 `3`，而不是 `4`。你该如何修复它？现在你需要找到所有可能将 `g_mode` 设置为 `3` 的地方，并追溯它最初是如何被设置的。这可能发生在一个完全不相关的代码段中！
将局部变量声明在尽可能靠近使用它们的地方的关键原因之一是，这样做可以最大限度地减少你需要查看的代码量，以便理解变量的作用。全局变量则处于光谱的另一端——因为它们可以在任何地方访问，你可能需要查看整个程序才能理解它们的用法。在小型程序中，这可能不是问题。在大型程序中，这将是一个问题。
例如，你可能会发现在你的程序中 `g_mode` 被引用了 442 次。除非 `g_mode` 有良好的文档，否则你可能需要查看 `g_mode` 的每次使用，才能了解它在不同情况下的使用方式，其有效值是什么，以及它的总体功能是什么。
全局变量还会降低程序的模块化和灵活性。一个只利用其参数且没有副作用的函数是完全模块化的。模块化有助于理解程序的功能以及提高可重用性。全局变量会显著降低模块化。
尤其要避免将全局变量用于重要的“决策点”变量（例如，在条件语句中使用的变量，如上述示例中的 `g_mode` 变量）。如果保存信息值的全局变量发生变化（例如，用户的姓名），你的程序不太可能崩溃。但如果更改影响程序实际**如何**运行的全局变量，则更有可能崩溃。
最佳实践
尽可能使用局部变量而非全局变量。
全局变量的初始化顺序问题
静态变量（包括全局变量）的初始化是程序启动的一部分，在 `main` 函数执行之前进行。这分为两个阶段。
第一阶段称为**静态初始化**。静态初始化分为两个阶段：
带有 constexpr 初始化器（包括字面量）的全局变量被初始化为这些值。这被称为**常量初始化**。
没有初始化器的全局变量被零初始化。零初始化被认为是静态初始化的一种形式，因为 `0` 是一个 constexpr 值。
第二阶段称为**动态初始化**。这个阶段更复杂和微妙，但其要点是，带有非 constexpr 初始化器的全局变量会被初始化。
这是一个非 constexpr 初始化器的例子：
int init()
{
    return 5;
}

int g_something{ init() }; // non-constexpr initialization
在单个文件中，对于每个阶段，全局变量通常按定义顺序初始化（动态初始化阶段对此规则有一些例外）。鉴于此，你需要小心，不要让变量依赖于其他变量的初始化值，而这些变量要等到后面才会被初始化。例如：
#include <iostream>

int initX();  // forward declaration
int initY();  // forward declaration

int g_x{ initX() }; // g_x is initialized first
int g_y{ initY() };

int initX()
{
    return g_y; // g_y isn't initialized when this is called
}

int initY()
{
    return 5;
}

int main()
{
    std::cout << g_x << ' ' << g_y << '\n';
}
这会打印
0 5
一个更大的问题是，不同翻译单元中静态对象的初始化顺序是不明确的。
给定两个文件，_a.cpp_ 和 _b.cpp_，任一个文件的全局变量都可能首先被初始化。如果在 _a.cpp_ 中某个具有静态生命周期的变量使用在 _b.cpp_ 中定义的具有静态生命周期的变量进行初始化，那么 _b.cpp_ 中的变量有 50% 的几率尚未初始化。
命名法
不同翻译单元中具有静态存储期的对象初始化顺序的模糊性通常被称为
静态初始化顺序混乱
。
警告
避免使用来自不同翻译单元的具有静态生命周期的其他对象来初始化具有静态生命周期的对象。
全局变量的动态初始化也容易出现初始化顺序问题，应尽可能避免。
那么，使用非 const 全局变量有哪些很好的理由呢？
不多。在大多数情况下，使用局部变量并将它们作为参数传递给其他函数是更好的选择。但在某些情况下，审慎地使用非 const 全局变量**确实**可以降低程序复杂性，在这些罕见的情况下，使用它们可能比替代方案更好。
一个很好的例子是日志文件，你可以在其中倾倒错误或调试信息。将其定义为全局变量可能是有意义的，因为你的程序中可能只有一个这样的日志，并且它很可能会在程序的各个地方使用。另一个很好的例子是随机数生成器（我们在课程
8.15 -- 全局随机数 (Random.h)
中展示了这样的例子）。
顺便一提，std::cout 和 std::cin 对象是作为全局变量（在 std 命名空间内）实现的。
根据经验法则，任何全局变量的使用都应至少满足以下两个标准：在程序中该变量所代表的事物应该只有一个，并且它的使用应该遍及程序的各个部分。
许多新程序员犯的错误是认为某个东西可以实现为全局变量，仅仅因为“现在”只需要一个。例如，你可能认为因为你正在实现一个单人游戏，所以你只需要一个玩家。但是，当你以后想添加多人模式（对抗或热座）时会发生什么呢？
保护自己免受全球性破坏
如果你确实找到了非 const 全局变量的好用途，一些有用的建议将最大限度地减少你可能遇到的麻烦。这些建议不仅适用于非 const 全局变量，也适用于所有全局变量。
首先，所有非命名空间的全局变量都应以“g”或“g_”为前缀，或者更好的是，将它们放入命名空间（在课程
7.2 -- 用户自定义命名空间和作用域解析运算符
中讨论），以减少命名冲突的机会。
例如，而不是这样：
#include <iostream>

constexpr double gravity { 9.8 }; // risk of collision with some other global variable named gravity

int main()
{
    std::cout << gravity << '\n'; // unclear if this is a local or global variable from the name

    return 0;
}
这样做：
#include <iostream>

namespace constants
{
    constexpr double gravity { 9.8 }; // will not collide with other global variables named gravity
}

int main()
{
    std::cout << constants::gravity << '\n'; // clear this is a global variable (since namespaces are global)

    return 0;
}
其次，与其直接访问全局变量，不如“封装”变量。确保变量只能从声明它的文件内部访问，例如通过将变量设为静态或 const，然后提供外部全局“访问函数”来操作变量。这些函数可以确保维护适当的使用（例如，进行输入验证、范围检查等）。此外，如果你决定更改底层实现（例如，从一个数据库迁移到另一个数据库），你只需更新访问函数，而不是直接使用全局变量的每一段代码。
例如，而不是这样：
constants.cpp
namespace constants
{
    extern const double gravity { 9.8 }; // has external linkage, can be accessed by other files
}
main.cpp
#include <iostream>

namespace constants
{
    extern const double gravity; // forward declaration
}

int main()
{
    std::cout << constants::gravity << '\n'; // direct access to global variable

    return 0;
}
这样做：
contants.cpp
namespace constants
{
    constexpr double gravity { 9.8 }; // has internal linkage, is accessible only within this file
}

double getGravity() // has external linkage, can be accessed by other files
{
    // We could add logic here if needed later
    // or change the implementation transparently to the callers
    return constants::gravity;
}
main.cpp
#include <iostream>

double getGravity(); // forward declaration

int main()
{
    std::cout << getGravity() << '\n';

    return 0;
}
提醒
全局 `const` 变量默认具有内部链接，`gravity` 不需要是 `static`。
第三，在编写原本独立但使用全局变量的函数时，不要在函数体中直接使用该变量。而是将其作为参数传入。这样，如果你的函数在某些情况下需要使用不同的值，你可以简单地改变参数。这有助于保持模块化。
而不是：
#include <iostream>

namespace constants
{
    constexpr double gravity { 9.8 };
}

// This function is only useful for calculating your instant velocity based on the global gravity
double instantVelocity(int time)
{
    return constants::gravity * time;
}

int main()
{
    std::cout << instantVelocity(5) << '\n';

    return 0;

}
这样做：
#include <iostream>

namespace constants
{
    constexpr double gravity { 9.8 };
}

// This function can calculate the instant velocity for any gravity value (more useful)
double instantVelocity(int time, double gravity)
{
    return gravity * time;
}

int main()
{
    std::cout << instantVelocity(5, constants::gravity) << '\n'; // pass our constant to the function as a parameter

    return 0;
}
一个 C++ 笑话
全局变量的最佳命名前缀是什么？
答案：//
这个笑话值得所有评论。
下一课
7.9
内联函数和变量
返回目录
上一课
7.7
外部链接和变量前向声明