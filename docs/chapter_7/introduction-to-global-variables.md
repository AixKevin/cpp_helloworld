# 7.4 — 全局变量简介

7.4 — 全局变量简介
Alex
2007 年 6 月 19 日，上午 8:22 PDT
2024 年 6 月 9 日
在课程
7.3 -- 局部变量
中，我们讲到局部变量是在函数体内部定义的变量。局部变量具有块作用域（只在其声明的块内可见），并且具有自动存储期（它们在定义时创建，在块退出时销毁）。
在 C++ 中，变量也可以在函数
外部
声明。这类变量称为
全局变量
。
声明全局变量
按照惯例，全局变量在文件顶部、`include` 语句下方、全局命名空间中声明。下面是一个全局变量定义的例子：
#include <iostream>

// Variables declared outside of a function are global variables
int g_x {}; // global variable g_x

void doSomething()
{
    // global variables can be seen and used everywhere in the file
    g_x = 3;
    std::cout << g_x << '\n';
}

int main()
{
    doSomething();
    std::cout << g_x << '\n';

    // global variables can be seen and used everywhere in the file
    g_x = 5;
    std::cout << g_x << '\n';

    return 0;
}
// g_x goes out of scope here
上面的例子打印：
3
3
5
全局变量的作用域
在全局命名空间中声明的标识符具有
全局命名空间作用域
（通常称为
全局作用域
，有时非正式地称为
文件作用域
），这意味着它们从声明点开始直到声明它们的
文件
结束都可见。
一旦声明，全局变量就可以在该文件的任何地方使用！在上面的例子中，全局变量 `g_x` 在 `doSomething()` 和 `main()` 两个函数中都使用了。
全局变量也可以在用户定义的命名空间内定义。下面是与上面相同的例子，但 `g_x` 已从全局作用域移动到用户定义的命名空间 `Foo` 中：
#include <iostream>

namespace Foo // Foo is defined in the global scope
{
    int g_x {}; // g_x is now inside the Foo namespace, but is still a global variable
}

void doSomething()
{
    // global variables can be seen and used everywhere in the file
    Foo::g_x = 3;
    std::cout << Foo::g_x << '\n';
}

int main()
{
    doSomething();
    std::cout << Foo::g_x << '\n';

    // global variables can be seen and used everywhere in the file
    Foo::g_x = 5;
    std::cout << Foo::g_x << '\n';

    return 0;
}
尽管标识符 `g_x` 现在被限制在 `namespace Foo` 的作用域内，但该名称仍然是全局可访问的（通过 `Foo::g_x`），并且 `g_x` 仍然是一个全局变量。
关键见解
在命名空间内部声明的变量也是全局变量。
最佳实践
优先在命名空间内定义全局变量，而不是在全局命名空间中。
全局变量具有静态存储期
全局变量在程序启动时（`main()` 开始执行之前）创建，并在程序结束时销毁。这称为
静态存储期
。具有
静态存储期
的变量有时称为
静态变量
。
命名全局变量
按照惯例，一些开发人员在全局变量标识符前加上“g”或“g_”前缀，以表明它们是全局变量。此前缀有几个目的：
它有助于避免与全局命名空间中的其他标识符命名冲突。
它有助于防止无意的名称遮蔽（我们将在课程
7.5 -- 变量遮蔽（名称隐藏）
中进一步讨论这一点）。
它有助于表明带前缀的变量在函数作用域之外仍然存在，因此我们对其进行的任何更改都将持续存在。
在用户定义命名空间中定义的全局变量通常会省略前缀（因为上面列表中的前两点在这种情况下不是问题，并且当我们看到预置的命名空间名称时，我们可以推断出一个变量是全局的）。但是，如果你想保留前缀作为第三点的更明显的提醒，也无妨。
最佳实践
考虑在使用全局变量命名时（特别是那些在全局命名空间中定义的变量）使用“g”或“g_”前缀，以帮助将它们与局部变量和函数参数区分开来。
作者注
我们有时会收到读者的反馈，询问 `g_` 这样的前缀是否可以，因为他们被告知前缀是
匈牙利命名法
的一种形式，而“匈牙利命名法很糟糕”。
对匈牙利命名法的反对主要来自于使用匈牙利命名法在变量名中编码变量的
类型
。例如，`nAge`，其中 `n` 表示 `int`。这在现代 C++ 中并没有那么有用。
然而，使用前缀（通常是 `g` / `g_`、`s` / `s_` 和 `m` / `m_`）来表示变量的
作用域
或
存储期
确实增加了价值，原因已在本节中指出。
全局变量初始化
与默认未初始化的局部变量不同，具有静态存储期的变量默认情况下是零初始化的。
非常量全局变量可以可选地初始化：
int g_x;       // no explicit initializer (zero-initialized by default)
int g_y {};    // value initialized (resulting in zero-initialization)
int g_z { 1 }; // list initialized with specific value
常量全局变量
与局部变量一样，全局变量可以是常量。与所有常量一样，常量全局变量必须被初始化。
#include <iostream>

const int g_x;     // error: constant variables must be initialized
constexpr int g_w; // error: constexpr variables must be initialized

const int g_y { 1 };     // const global variable g_y, initialized with a value
constexpr int g_z { 2 }; // constexpr global variable g_z, initialized with a value

void doSomething()
{
    // global variables can be seen and used everywhere in the file
    std::cout << g_y << '\n';
    std::cout << g_z << '\n';
}

int main()
{
    doSomething();

    // global variables can be seen and used everywhere in the file
    std::cout << g_y << '\n';
    std::cout << g_z << '\n';

    return 0;
}
// g_y and g_z goes out of scope here
相关内容
我们将在课程
7.10 -- 跨多个文件共享全局常量（使用内联变量）
中更详细地讨论全局常量。
关于（非常量）全局变量的注意事项
新程序员经常会倾向于使用大量的全局变量，因为它们无需显式传递给每个需要它们的函数即可使用。然而，通常应完全避免使用非常量全局变量！我们将在即将到来的课程
7.8 -- 为什么（非常量）全局变量是邪恶的
中讨论原因。
快速总结
// Non-constant global variables
int g_x;                 // defines non-initialized global variable (zero initialized by default)
int g_x {};              // defines explicitly value-initialized global variable
int g_x { 1 };           // defines explicitly initialized global variable

// Const global variables
const int g_y;           // error: const variables must be initialized
const int g_y { 2 };     // defines initialized global const

// Constexpr global variables
constexpr int g_y;       // error: constexpr variables must be initialized
constexpr int g_y { 3 }; // defines initialized global constexpr
下一课
7.5
变量遮蔽（名称隐藏）
返回目录
上一课
7.3
局部变量