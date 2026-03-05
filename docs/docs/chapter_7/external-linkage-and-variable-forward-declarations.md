# 7.7 — 外部链接和变量前向声明

7.7 — 外部链接和变量前向声明
Alex
2020 年 1 月 3 日，太平洋标准时间上午 10:40
2024 年 12 月 11 日
在上一课（
7.6 -- 内部链接
）中，我们讨论了
内部链接
如何将标识符的使用限制在单个文件中。在本课中，我们将探讨
外部链接
的概念。
具有
外部链接
的标识符可以在定义它的文件中以及从其他代码文件（通过前向声明）中看到和使用。从这个意义上说，具有外部链接的标识符是真正“全局”的，因为它们可以在程序的任何地方使用！
关键见解
具有外部链接的标识符对链接器可见。这允许链接器执行两件事
将一个翻译单元中使用的标识符与另一个翻译单元中的相应定义连接起来。
消除内联标识符的重复，以便保留一个规范定义。我们将在
7.9 -- 内联函数和变量
中讨论内联变量和函数。
函数默认具有外部链接
在
2.8 -- 包含多个代码文件的程序
中，您了解到可以从一个文件调用在另一个文件中定义的函数。这是因为函数默认具有外部链接。
为了调用在另一个文件中定义的函数，您必须在任何其他希望使用该函数的代码文件中放置该函数的
前向声明
。前向声明告诉编译器该函数的存在，链接器将函数调用连接到实际的函数定义。
这是一个例子
a.cpp
#include <iostream>

void sayHi() // this function has external linkage, and can be seen by other files
{
    std::cout << "Hi!\n";
}
main.cpp
void sayHi(); // forward declaration for function sayHi, makes sayHi accessible in this file

int main()
{
    sayHi(); // call to function defined in another file, linker will connect this call to the function definition

    return 0;
}
上面的程序打印
Hi!
在上面的示例中，
main.cpp
中函数
sayHi()
的前向声明允许
main.cpp
访问在
a.cpp
中定义的
sayHi()
函数。前向声明满足了编译器，链接器能够将函数调用链接到函数定义。
如果函数
sayHi()
改为内部链接，链接器将无法将函数调用连接到函数定义，从而导致链接器错误。
具有外部链接的全局变量
具有外部链接的全局变量有时称为
外部变量
。为了使全局变量外部化（从而可由其他文件访问），我们可以使用
extern
关键字来实现
int g_x { 2 }; // non-constant globals are external by default (no need to use extern)

extern const int g_y { 3 }; // const globals can be defined as extern, making them external
extern constexpr int g_z { 3 }; // constexpr globals can be defined as extern, making them external (but this is pretty useless, see the warning in the next section)

int main()
{
    return 0;
}
非 const 全局变量默认是外部的，因此我们不需要将它们标记为
extern
。
通过 extern 关键字进行变量前向声明
要实际使用在另一个文件中定义的外部全局变量，您还必须在任何其他希望使用该变量的文件中放置该全局变量的
前向声明
。对于变量，创建前向声明也通过
extern
关键字（不带初始化值）完成。
这是一个使用变量前向声明的示例
main.cpp
#include <iostream>

extern int g_x;       // this extern is a forward declaration of a variable named g_x that is defined somewhere else
extern const int g_y; // this extern is a forward declaration of a const variable named g_y that is defined somewhere else

int main()
{
    std::cout << g_x << ' ' << g_y << '\n'; // prints 2 3

    return 0;
}
这是这些变量的定义
a.cpp
// global variable definitions
int g_x { 2 };              // non-constant globals have external linkage by default
extern const int g_y { 3 }; // this extern gives g_y external linkage
在上面的示例中，
a.cpp
和
main.cpp
都引用了名为
g_x
的相同全局变量。因此，即使
g_x
在
a.cpp
中定义并初始化，我们仍然可以通过
g_x
的前向声明在
main.cpp
中使用它的值。
请注意，
extern
关键字在不同的上下文中具有不同的含义。在某些上下文中，
extern
表示“赋予此变量外部链接”。在其他上下文中，
extern
表示“这是在其他地方定义的外部变量的前向声明”。是的，这令人困惑，所以我们在
7.12 -- 作用域、生命周期和链接总结
中总结了所有这些用法。
警告
如果您想定义一个未初始化的非 const 全局变量，请不要使用 extern 关键字，否则 C++ 会认为您正在尝试为该变量进行前向声明。
警告
尽管可以通过
extern
关键字赋予 constexpr 变量外部链接，但它们不能被前向声明为 constexpr。这是因为编译器需要在编译时知道 constexpr 变量的值。如果该值在其他文件中定义，编译器将无法看到该其他文件中定义的值。
但是，您可以将 constexpr 变量前向声明为 const，编译器会将其视为运行时 const。这并不是特别有用。
请注意，函数前向声明不需要
extern
关键字——编译器能够根据您是否提供函数体来判断您是在定义新函数还是在进行前向声明。变量前向声明
确实
需要
extern
关键字来帮助区分未初始化变量的定义和变量前向声明（它们看起来相同）
// non-constant 
int g_x;        // variable definition (no initializer)
int g_x { 1 };  // variable definition (w/ initializer)
extern int g_x; // forward declaration (no initializer)

// constant
extern const int g_y { 1 }; // variable definition (const requires initializers)
extern const int g_y;       // forward declaration (no initializer)
避免在带有初始化器的非 const 全局变量上使用
extern
以下两行在语义上是等效的
int g_x { 1 };        // extern by default
extern int g_x { 1 }; // explicitly extern (may cause compiler warning)
但是，您的编译器可能会对后一个语句发出警告，尽管它在技术上是有效的。
还记得我们说过编译器可以随意对它们认为可疑的事情发出诊断吗？这就是其中一种情况。通常，当我们想要前向声明时，
extern
应用于非 const 变量。但是，添加初始化器会使该语句变为定义。编译器告诉您似乎出了问题。要纠正它，要么删除初始化器（如果您打算进行前向声明），要么删除
extern
（如果您打算进行定义）。
最佳实践
仅将
extern
用于全局变量前向声明或 const 全局变量定义。
不要将
extern
用于非 const 全局变量定义（它们隐式为
extern
）。
快速总结
// Global variable forward declarations (extern w/ no initializer):
extern int g_y;                 // forward declaration for non-constant global variable
extern const int g_y;           // forward declaration for const global variable
extern constexpr int g_y;       // not allowed: constexpr variables can't be forward declared

// External global variable definitions (no extern)
int g_x;                        // defines non-initialized external global variable (zero initialized by default)
int g_x { 1 };                  // defines initialized external global variable

// External const global variable definitions (extern w/ initializer)
extern const int g_x { 2 };     // defines initialized const external global variable
extern constexpr int g_x { 3 }; // defines initialized constexpr external global variable
我们在
7.12 -- 作用域、生命周期和链接总结
中提供了全面的总结。
小测验时间
问题 #1
变量的作用域、生命周期和链接之间有什么区别？全局变量有什么样的作用域、生命周期和链接？
显示答案
作用域决定变量在哪里可访问。生命周期决定变量何时创建和销毁。链接决定变量是否可以导出到另一个文件。
全局变量具有全局作用域（又称文件作用域），这意味着它们可以从声明点到声明它们的文件末尾进行访问。
全局变量具有静态生命周期，这意味着它们在程序启动时创建，在程序结束时销毁。
全局变量可以通过 static 和 extern 关键字分别具有内部链接或外部链接。
下一课
7.8
为什么（非 const）全局变量是邪恶的
返回目录
上一课
7.6
内部链接