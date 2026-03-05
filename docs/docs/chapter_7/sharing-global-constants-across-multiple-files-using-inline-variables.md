# 7.10 — 在多个文件间共享全局常量（使用内联变量）

7.10 — 在多个文件间共享全局常量（使用内联变量）
Alex
2020年1月3日，太平洋标准时间上午10:41
2024年12月14日
在某些应用程序中，可能需要在整个代码中（而不仅仅是在一个位置）使用某些符号常量。这些常量可以包括不变的物理或数学常数（例如 pi 或阿伏伽德罗常数），或者特定于应用程序的“调整”值（例如摩擦或重力系数）。与其在每个需要这些常量的文件中重新定义它们（这违反了“不要重复自己”的规则），不如将它们在中心位置声明一次，并在需要的地方使用它们。这样，如果需要更改它们，只需在一个地方更改，这些更改就可以传播出去。
本课程讨论了最常见的实现方法。
作为内部变量的全局常量
在 C++17 之前，以下是最简单和最常见的解决方案
创建一个头文件来保存这些常量
在该头文件内部，定义一个命名空间（在
7.2 -- 用户定义的命名空间和作用域解析运算符
课程中讨论）
将所有常量添加到命名空间内部（确保它们是
constexpr
）
在需要的地方 #include 头文件
例如
constants.h
#ifndef CONSTANTS_H
#define CONSTANTS_H

// Define your own namespace to hold constants
namespace constants
{
    // Global constants have internal linkage by default
    constexpr double pi { 3.14159 };
    constexpr double avogadro { 6.0221413e23 };
    constexpr double myGravity { 9.2 }; // m/s^2 -- gravity is light on this planet
    // ... other related constants
}
#endif
然后使用作用域解析运算符 (::)，左边是命名空间名称，右边是变量名称，以便在 .cpp 文件中访问您的常量
main.cpp
#include "constants.h" // include a copy of each constant in this file

#include <iostream>

int main()
{
    std::cout << "Enter a radius: ";
    double radius{};
    std::cin >> radius;

    std::cout << "The circumference is: " << 2 * radius * constants::pi << '\n';

    return 0;
}
当这个头文件被 #included 到 .cpp 文件中时，头文件中定义的每个变量都将在包含点复制到该代码文件中。由于这些变量存在于函数外部，它们在包含它们的文件中被视为全局变量，这就是为什么您可以在该文件中的任何位置使用它们。
因为 const 全局变量具有内部链接，所以每个 .cpp 文件都会获得一个独立的全局变量版本，链接器无法看到。在大多数情况下，由于这些是 constexpr，编译器会简单地优化掉这些变量。
虽然这很简单（对于较小的程序来说没问题），但每次
constants.h
被 #included 到不同的代码文件中时，这些变量都会被复制到包含代码文件中。因此，如果 constants.h 被包含到 20 个不同的代码文件中，每个变量都会被复制 20 次。头文件保护不会阻止这种情况发生，因为它们只防止头文件被包含到单个包含文件中多次，而不是被包含到多个不同的代码文件中一次。这引入了两个挑战
更改单个常量值将需要重新编译所有包含常量头文件的文件，这可能导致大型项目的漫长重建时间。
如果常量尺寸较大且无法优化掉，这可能会占用大量内存。
优点
在 C++17 之前有效。
可以在任何包含它们的翻译单元的常量表达式中使用。
缺点
更改头文件中的任何内容都需要重新编译包含该头文件的文件。
每个包含头文件的翻译单元都会获得变量的自己的副本。
作为外部变量的全局常量
如果您正在积极更改值或添加新常量，那么之前的解决方案可能会有问题，至少在事情稳定下来之前。
避免这些问题的一种方法是将这些常量转换为外部变量，因为这样我们可以拥有一个在所有文件之间共享的单个变量（只初始化一次）。在这种方法中，我们将在 .cpp 文件中定义常量（以确保定义只存在于一个位置），并将前向声明放在头文件中（这将由其他文件包含）。
constants.cpp
#include "constants.h"

namespace constants
{
    // We use extern to ensure these have external linkage
    extern constexpr double pi { 3.14159 };
    extern constexpr double avogadro { 6.0221413e23 };
    extern constexpr double myGravity { 9.2 }; // m/s^2 -- gravity is light on this planet
}
constants.h
#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace constants
{
    // Since the actual variables are inside a namespace, the forward declarations need to be inside a namespace as well
    // We can't forward declare variables as constexpr, but we can forward declare them as (runtime) const
    extern const double pi;
    extern const double avogadro;
    extern const double myGravity;
}

#endif
在代码文件中的使用保持不变
main.cpp
#include "constants.h" // include all the forward declarations

#include <iostream>

int main()
{
    std::cout << "Enter a radius: ";
    double radius{};
    std::cin >> radius;

    std::cout << "The circumference is: " << 2 * radius * constants::pi << '\n';

    return 0;
}
现在符号常量将只实例化一次（在
constants.cpp
中），而不是在每个 #included
constants.h
的代码文件中，并且这些常量的所有使用都将链接到在
constants.cpp
中实例化的版本。对
constants.cpp
所做的任何更改都将只需要重新编译
constants.cpp
。
但是，这种方法有几个缺点。首先，因为只有变量定义是 constexpr（前向声明不是，也不能是），所以这些常量只在它们实际定义的文件中（
constants.cpp
）是常量表达式。在其他文件中，编译器只会看到前向声明，它不定义 constexpr 值（并且必须由链接器解析）。这意味着在它们定义的 文件之外，这些变量不能用于常量表达式。其次，因为常量表达式通常比运行时表达式可以优化得更多，编译器可能无法对它们进行尽可能多的优化。
关键见解
为了使变量可以在编译时上下文中使用，例如数组大小，编译器必须看到变量的定义（而不仅仅是前向声明）。
因为编译器单独编译每个源文件，所以它只能看到正在编译的源文件中出现的变量定义（包括任何包含的头文件）。例如，当编译器编译
main.cpp
时，
constants.cpp
中的变量定义是不可见的。因此，constexpr 变量不能分成头文件和源文件，它们必须在头文件中定义。
考虑到上述缺点，最好在头文件中定义您的常量（根据前一节或下一节）。如果您发现常数值经常变化（例如，因为您正在调整程序），并且这导致编译时间过长，您可以根据需要暂时将有问题的常量移动到 .cpp 文件中（使用此方法）。
优点
在 C++17 之前有效。
每个变量只需要一个副本。
如果常量值更改，只需要重新编译一个文件。
缺点
前向声明和变量定义在单独的文件中，并且必须保持同步。
变量不能在其定义文件之外的常量表达式中使用。
作为内联变量的全局常量
C++17
在
7.9 -- 内联函数和变量
课程中，我们介绍了内联变量，这些变量可以有多个定义，只要这些定义是相同的。通过将我们的 constexpr 变量内联，我们可以在头文件中定义它们，然后将它们 #include 到任何需要它们的 .cpp 文件中。这避免了 ODR 违规和重复变量的缺点。
提醒
Constexpr 函数是隐式内联的，但 constexpr 变量不是隐式内联的。如果您想要一个内联 constexpr 变量，您必须显式地将其标记为
inline
。
关键见解
内联变量默认具有外部链接，因此链接器可见。这是必要的，以便链接器可以去重定义。
非内联 constexpr 变量具有内部链接。如果包含到多个翻译单元中，每个翻译单元将获得变量的自己的副本。这不是 ODR 违规，因为它们不暴露给链接器。
constants.h
#ifndef CONSTANTS_H
#define CONSTANTS_H

// define your own namespace to hold constants
namespace constants
{
    inline constexpr double pi { 3.14159 }; // note: now inline constexpr
    inline constexpr double avogadro { 6.0221413e23 };
    inline constexpr double myGravity { 9.2 }; // m/s^2 -- gravity is light on this planet
    // ... other related constants
}
#endif
main.cpp
#include "constants.h"

#include <iostream>

int main()
{
    std::cout << "Enter a radius: ";
    double radius{};
    std::cin >> radius;

    std::cout << "The circumference is: " << 2 * radius * constants::pi << '\n';

    return 0;
}
我们可以将
constants.h
包含到任意数量的代码文件中，但这些变量只会实例化一次，并在所有代码文件之间共享。
如果任何常量值发生更改，此方法确实保留了需要重新编译所有包含常量头文件的文件的缺点。
优点
可以在任何包含它们的翻译单元的常量表达式中使用。
每个变量只需要一个副本。
缺点
仅适用于 C++17 及更高版本。
更改头文件中的任何内容都需要重新编译包含该头文件的文件。
最佳实践
如果您需要全局常量并且您的编译器支持 C++17，请优先在头文件中定义内联 constexpr 全局变量。
提醒
对于
constexpr
字符串，请使用
std::string_view
。我们在
5.8 -- std::string_view 简介
课程中介绍了这一点。
相关内容
我们在
7.12 -- 作用域、持续时间和链接总结
课程中总结了各种类型变量的作用域、持续时间和链接。
下一课
7.11
静态局部变量
返回目录
上一课
7.9
内联函数和变量