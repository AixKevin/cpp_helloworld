# 10.4 — 窄化转换、列表初始化和 constexpr 初始化式

10.4 — 窄化转换、列表初始化和 constexpr 初始化式
Alex
2023年5月5日，太平洋夏令时下午6:10
2024年2月16日
在上一课（
10.3 -- 数值转换
）中，我们介绍了数值转换，它涵盖了基本类型之间广泛的不同类型转换。
窄化转换
在 C++ 中，
窄化转换
是一种潜在不安全的数值转换，其中目标类型可能无法容纳源类型的所有值。
以下转换被定义为窄化转换：
从浮点类型到整型。
从浮点类型到更窄或更低排名的浮点类型，除非要转换的值是 constexpr 且在目标类型的范围内（即使目标类型没有足够的精度来存储数字的所有有效数字）。
从整型到浮点类型，除非要转换的值是 constexpr 且其值可以精确地存储在目标类型中。
从一种整型到另一种不能表示原始类型所有值的整型，除非要转换的值是 constexpr 且其值可以精确地存储在目标类型中。这涵盖了从更宽到更窄的整型转换，以及整型符号转换（有符号到无符号，反之亦然）。
在大多数情况下，隐式窄化转换会导致编译器警告，有符号/无符号转换除外（可能会或可能不会产生警告，具体取决于编译器的配置方式）。
应尽可能避免窄化转换，因为它们可能不安全，因此是潜在错误的来源。
最佳实践
因为它们可能不安全且是错误的来源，所以应尽可能避免窄化转换。
使有意为之的窄化转换显式化
窄化转换并非总是可以避免的——对于函数调用尤其如此，其中函数参数和实参可能类型不匹配并需要窄化转换。
在这种情况下，最好使用 `static_cast` 将隐式窄化转换转换为显式窄化转换。这样做有助于记录窄化转换是故意的，并将抑制否则可能产生的任何编译器警告或错误。
例如
void someFcn(int i)
{
}

int main()
{
    double d{ 5.0 };
    
    someFcn(d); // bad: implicit narrowing conversion will generate compiler warning

    // good: we're explicitly telling the compiler this narrowing conversion is intentional
    someFcn(static_cast<int>(d)); // no warning generated
    
    return 0;
}
最佳实践
如果您需要执行窄化转换，请使用 `static_cast` 将其转换为显式转换。
大括号初始化不允许窄化转换
使用大括号初始化时，不允许进行窄化转换（这是此初始化形式受到青睐的主要原因之一），尝试这样做会产生编译错误。
例如
int main()
{
    int i { 3.5 }; // won't compile

    return 0;
}
Visual Studio 产生以下错误：
error C2397: conversion from 'double' to 'int' requires a narrowing conversion
如果您确实想在大括号初始化中进行窄化转换，请使用 `static_cast` 将窄化转换转换为显式转换。
int main()
{
    double d { 3.5 };

    // static_cast<int> converts double to int, initializes i with int result
    int i { static_cast<int>(d) }; 

    return 0;
}
一些 constexpr 转换不被认为是窄化转换
当窄化转换的源值直到运行时才知道时，转换的结果也无法在运行时确定。在这种情况下，窄化转换是否保留值也无法在运行时确定。例如：
#include <iostream>

void print(unsigned int u) // note: unsigned
{
    std::cout << u << '\n';
}

int main()
{
    std::cout << "Enter an integral value: ";
    int n{};
    std::cin >> n; // enter 5 or -5
    print(n);      // conversion to unsigned may or may not preserve value

    return 0;
}
在上面的程序中，编译器不知道将为 `n` 输入什么值。当调用 `print(n)` 时，从 `int` 到 `unsigned int` 的转换将在那时执行，结果可能保留值，也可能不保留值，具体取决于为 `n` 输入的值。因此，启用有符号/无符号警告的编译器将为此情况发出警告。
然而，您可能已经注意到，大多数窄化转换定义都有一个以“除非要转换的值是 constexpr 且……”开头的例外条款。例如，当“从一种整型到另一种不能表示原始类型所有值的整型，除非要转换的值是 constexpr 且其值可以精确地存储在目标类型中”时，转换是窄化转换。
当窄化转换的源值是 constexpr 时，要转换的具体值必须为编译器所知。在这种情况下，编译器可以自己执行转换，然后检查值是否被保留。如果值未被保留，编译器可以停止编译并报错。如果值被保留，则该转换不被视为窄化转换（编译器可以将整个转换替换为转换后的结果，因为知道这样做是安全的）。
例如
#include <iostream>

int main()
{
    constexpr int n1{ 5 };   // note: constexpr
    unsigned int u1 { n1 };  // okay: conversion is not narrowing due to exclusion clause

    constexpr int n2 { -5 }; // note: constexpr
    unsigned int u2 { n2 };  // compile error: conversion is narrowing due to value change

    return 0;
}
让我们将规则“从一种整型到另一种不能表示原始类型所有值的整型，除非要转换的值是 constexpr 且其值可以精确地存储在目标类型中”应用于上面的两个转换。
在 `n1` 和 `u1` 的情况下，`n1` 是 `int`，`u1` 是 `unsigned int`，因此这是从一种整型到另一种不能表示原始类型所有值的整型的转换。然而，`n1` 是 constexpr，并且它的值 `5` 可以精确地表示在目标类型中（作为无符号值 `5`）。因此，这不被视为窄化转换，并且我们允许使用 `n1` 列表初始化 `u1`。
在 `n2` 和 `u2` 的情况下，情况类似。虽然 `n2` 是 constexpr，但它的值 `-5` 不能精确地表示在目标类型中，因此这被视为窄化转换，并且由于我们正在进行列表初始化，编译器将报错并停止编译。
奇怪的是，从浮点类型到整型的转换没有 constexpr 排除条款，因此即使要转换的值是 constexpr 且在目标类型的范围内，这些转换也始终被视为窄化转换。
int n { 5.0 }; // compile error: narrowing conversion
更奇怪的是，即使存在精度损失，从 constexpr 浮点类型到更窄浮点类型的转换也不被认为是窄化转换！
constexpr double d { 0.1 };
float f { d }; // not narrowing, even though loss of precision results
警告
从 constexpr 浮点类型到更窄浮点类型的转换，即使导致精度损失，也不被认为是窄化转换。
带 constexpr 初始化式的列表初始化
这些 constexpr 异常条款在列表初始化非 int/非 double 对象时非常有用，因为我们可以使用 int 或 double 字面量（或 constexpr 对象）初始化值。
这使我们能够避免：
在大多数情况下使用字面量后缀
使用 static_cast 扰乱我们的初始化
例如
int main()
{
    // We can avoid literals with suffixes
    unsigned int u { 5 }; // okay (we don't need to use `5u`)
    float f { 1.5 };      // okay (we don't need to use `1.5f`)

    // We can avoid static_casts
    constexpr int n{ 5 };
    double d { n };       // okay (we don't need a static_cast here)
    short s { 5 };        // okay (there is no suffix for short, we don't need a static_cast here)

    return 0;
}
这也适用于复制和直接初始化。
需要提及的一个注意事项：用 constexpr 值初始化更窄或更低排名的浮点类型是允许的，只要该值在目标类型的范围内，即使目标类型没有足够的精度来精确存储该值！
关键见解
浮点类型的排名顺序（从高到低）如下：
长双精度型
双精度型
浮点型
因此，像这样的操作是合法的，并且不会发出错误：
int main()
{
    float f { 1.23456789 }; // not a narrowing conversion, even though precision lost!

    return 0;
}
但是，在这种情况下，您的编译器可能仍会发出警告（如果使用 -Wconversion 编译标志，GCC 和 Clang 会这样做）。
下一课
10.5
算术转换
返回目录
上一课
10.3
数值转换