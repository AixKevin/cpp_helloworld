# 6.7 — 关系运算符和浮点数比较

6.7 — 关系运算符和浮点数比较
Alex
2007 年 6 月 15 日，太平洋时间上午 10:43
2025 年 1 月 21 日
关系运算符
是允许您比较两个值的运算符。共有 6 种关系运算符
运算符
符号
形式
操作
大于
>
x > y
如果 x 大于 y，则为 true；否则为 false
小于
<
x < y
如果 x 小于 y，则为 true；否则为 false
大于或等于
>=
x >= y
如果 x 大于或等于 y，则为 true；否则为 false
小于或等于
<=
x <= y
如果 x 小于或等于 y，则为 true；否则为 false
相等
==
x == y
如果 x 等于 y，则为 true；否则为 false
不相等
!=
x != y
如果 x 不等于 y，则为 true；否则为 false
您已经了解了这些运算符的工作原理，它们都非常直观。每个运算符都计算为布尔值 true (1) 或 false (0)。
以下是使用这些运算符和整数的一些示例代码
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    if (x == y)
        std::cout << x << " equals " << y << '\n';
    if (x != y)
        std::cout << x << " does not equal " << y << '\n';
    if (x > y)
        std::cout << x << " is greater than " << y << '\n';
    if (x < y)
        std::cout << x << " is less than " << y << '\n';
    if (x >= y)
        std::cout << x << " is greater than or equal to " << y << '\n';
    if (x <= y)
        std::cout << x << " is less than or equal to " << y << '\n';

    return 0;
}
以及示例运行的结果
Enter an integer: 4
Enter another integer: 5
4 does not equal 5
4 is less than 5
4 is less than or equal to 5
这些运算符在比较整数时使用起来非常直接。
布尔条件值
默认情况下，`if` 语句或条件运算符（以及其他一些地方）中的条件会计算为布尔值。
许多新程序员会编写以下语句
if (b1 == true) ...
这是多余的，因为 `== true` 实际上并没有为条件增加任何价值。相反，我们应该这样写
if (b1) ...
同样，以下语句
if (b1 == false) ...
最好写成
if (!b1) ...
最佳实践
不要在条件中添加不必要的 `==` 或 `!=`。它们会使代码更难阅读，而没有提供任何额外价值。
计算浮点值的比较可能存在问题
考虑以下程序
#include <iostream>

int main()
{
    constexpr double d1{ 100.0 - 99.99 }; // should equal 0.01 mathematically
    constexpr double d2{ 10.0 - 9.99 }; // should equal 0.01 mathematically

    if (d1 == d2)
        std::cout << "d1 == d2" << '\n';
    else if (d1 > d2)
        std::cout << "d1 > d2" << '\n';
    else if (d1 < d2)
        std::cout << "d1 < d2" << '\n';
    
    return 0;
}
变量 d1 和 d2 都应该有值 *0.01*。但是这个程序打印出意想不到的结果
d1 > d2
如果您在调试器中检查 d1 和 d2 的值，您可能会看到 d1 = 0.010000000000005116，d2 = 0.0099999999999997868。这两个数字都接近 0.01，但 d1 大于 0.01，d2 小于 0.01。
使用任何关系运算符比较浮点值都可能存在危险。这是因为浮点值不精确，浮点操作数中微小的舍入误差可能导致它们比预期略小或略大。这可能会使关系运算符失灵。
相关内容
我们在课程
4.8 -- 浮点数
中讨论了舍入误差。
浮点数的小于和大于
当小于 (<)、大于 (>)、小于等于 (<=) 和大于等于 (>=) 运算符与浮点值一起使用时，它们在大多数情况下会产生可靠的结果（当操作数的值不相似时）。但是，如果操作数几乎相同，则这些运算符应被视为不可靠。例如，在上面的示例中，`d1 > d2` 恰好产生 `true`，但如果数值误差走向不同的方向，也可能很容易产生 `false`。
如果操作数相似时得到错误结果的后果可以接受，那么使用这些运算符是可以接受的。这是一个特定于应用程序的决定。
例如，考虑一个游戏（如太空入侵者），您想确定两个移动物体（如导弹和外星人）是否相交。如果物体仍然相距很远，这些运算符将返回正确答案。如果两个物体非常靠近，您可能会得到两种答案。在这种情况下，错误的答案可能甚至不会被注意到（它看起来就像是擦肩而过，或者擦边球），游戏会继续进行。
浮点数的相等和不相等
相等运算符（== 和 !=）更麻烦。考虑运算符 ==，它仅当其操作数完全相等时才返回 true。由于即使是最小的舍入误差也会导致两个浮点数不相等，因此运算符 == 有很高的风险在预期为 true 时返回 false。运算符 != 也有类似的问题。
#include <iostream>

int main()
{
    std::cout << std::boolalpha << (0.3 == 0.2 + 0.1); // prints false

    return 0;
}
因此，通常应避免将这些运算符与浮点操作数一起使用。
警告
如果浮点值可能经过计算，请避免使用运算符 `==` 和运算符 `!=` 来比较它们。
上述情况有一个值得注意的例外：将浮点字面量与用相同类型的字面量初始化的相同类型的变量进行比较是安全的，只要每个字面量的有效数字位数不超过该类型的最小精度即可。Float 的最小精度为 6 位有效数字，double 的最小精度为 15 位有效数字。
我们在课程
4.8 -- 浮点数
中介绍了不同类型的精度。
例如，您可能会偶尔看到一个函数返回一个浮点文字（通常是 `0.0`，有时是 `1.0`）。在这种情况下，可以直接与相同类型的相同文字值进行比较，这是安全的
if (someFcn() == 0.0) // okay if someFcn() returns 0.0 as a literal only
    // do something
除了字面量，我们还可以比较一个用字面量值初始化的 const 或 constexpr 浮点变量
constexpr double gravity { 9.8 };
if (gravity == 9.8) // okay if gravity was initialized with a literal
    // we're on earth
比较不同类型的浮点字面量大多不安全。例如，比较 `9.8f` 和 `9.8` 将返回 false。
提示
将浮点字面量与用相同类型的字面量初始化的相同类型的变量进行比较是安全的，只要每个字面量的有效数字位数不超过该类型的最小精度即可。Float 的最小精度为 6 位有效数字，double 的最小精度为 15 位有效数字。
通常不安全比较不同类型的浮点文字。
浮点数比较（高级/可选阅读）
那么我们如何才能合理地比较两个浮点操作数以查看它们是否相等？
最常见的浮点数相等比较方法是使用一个函数，该函数会判断两个数字是否*几乎*相同。如果它们“足够接近”，那么我们称它们相等。用于表示“足够接近”的值传统上称为 **epsilon**。Epsilon 通常定义为一个小的正数（例如 0.00000001，有时写为 1e-8）。
新开发人员经常尝试编写自己的“足够接近”函数，如下所示
#include <cmath> // for std::abs()

// absEpsilon is an absolute value
bool approximatelyEqualAbs(double a, double b, double absEpsilon)
{
    // if the distance between a and b is less than or equal to absEpsilon, then a and b are "close enough"
    return std::abs(a - b) <= absEpsilon;
}
`std::abs()` 是 `
` 头文件中的一个函数，返回其参数的绝对值。因此，`std::abs(a - b) <= absEpsilon` 检查 *a* 和 *b* 之间的距离是否小于或等于表示“足够接近”的 epsilon 值。如果 *a* 和 *b* 足够接近，函数返回 true 表示它们相等。否则，返回 false。
虽然这个函数可以工作，但它并不完美。对于大约 *1.0* 的输入，0.00001 的 epsilon 值是好的；对于大约 *0.0000001* 的输入，它太大了；对于 *10,000* 这样的输入，它又太小了。
题外话…
如果我们说任何与另一个数字相差 0.00001 以内的数字都应视为相同，那么
1 和 1.0001 会不同，但 1 和 1.00001 会相同。这并非不合理。
0.0000001 和 0.00001 将是相同的。这似乎不太好，因为这些数字相差两个数量级。
10000 和 10000.0001 会不同。这似乎也不好，因为考虑到数字的量级，这些数字几乎没有差异。
这意味着每次我们调用这个函数时，我们都必须选择一个适合我们输入的 epsilon。如果我们知道必须根据输入的量级来缩放 epsilon，那么我们不妨修改函数来为我们完成这项工作。
著名的计算机科学家
Donald Knuth
在他的著作《计算机程序设计艺术，第二卷：半数值算法》（Addison-Wesley，1969）中提出了以下方法
#include <algorithm> // for std::max
#include <cmath>     // for std::abs

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}
在这种情况下，epsilon 不再是一个绝对数字，而是相对于 *a* 或 *b* 的大小。
让我们更详细地研究这个看似疯狂的函数是如何工作的。在 `<=` 运算符的左侧，`std::abs(a - b)` 告诉我们 *a* 和 *b* 之间的距离作为一个正数。
在 `<=` 运算符的右侧，我们需要计算我们愿意接受的“足够接近”的最大值。为此，算法选择 *a* 和 *b* 中较大的一个（作为数字总体量级的粗略指标），然后将其乘以 relEpsilon。在此函数中，relEpsilon 代表一个百分比。例如，如果我们想说“足够接近”意味着 *a* 和 *b* 在 *a* 和 *b* 较大者的 1% 以内，我们传入一个 0.01 的 relEpsilon（1% = 1/100 = 0.01）。relEpsilon 的值可以根据具体情况进行调整（例如，0.002 的 epsilon 意味着在 0.2% 以内）。
要实现不相等 (!=) 而不是相等，只需调用此函数并使用逻辑非运算符 (!) 来翻转结果
if (!approximatelyEqualRel(a, b, 0.001))
    std::cout << a << " is not equal to " << b << '\n';
请注意，虽然 `approximatelyEqualRel()` 函数在大多数情况下都能正常工作，但它并不完美，尤其是在数字接近零时。
#include <algorithm> // for std::max
#include <cmath>     // for std::abs
#include <iostream>

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}

int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };

    std::cout << std::boolalpha; // print true or false instead of 1 or 0
    
    // First, let's compare a (almost 1.0) to 1.0.
    std::cout << approximatelyEqualRel(a, 1.0, relEps) << '\n';
 
    // Second, let's compare a-1.0 (almost 0.0) to 0.0
    std::cout << approximatelyEqualRel(a-1.0, 0.0, relEps) << '\n';

    return 0;
}
也许令人惊讶的是，这返回
true
false
第二次调用没有按预期执行。在接近零时，数学运算会崩溃。
避免这种情况的一种方法是同时使用绝对 epsilon（如我们第一种方法中那样）和相对 epsilon（如我们在 Knuth 方法中那样）。
// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (std::abs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}
在这个算法中，我们首先检查 *a* 和 *b* 在绝对值上是否接近，这处理了 *a* 和 *b* 都接近零的情况。*absEpsilon* 参数应设置为一个非常小的值（例如 1e-12）。如果失败，我们则回退到 Knuth 的算法，使用相对 epsilon。
这是我们之前的代码，测试了两种算法
#include <algorithm> // for std::max
#include <cmath>     // for std::abs
#include <iostream>

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}

// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (std::abs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}

int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };

    std::cout << std::boolalpha; // print true or false instead of 1 or 0

    std::cout << approximatelyEqualRel(a, 1.0, relEps) << '\n';     // compare "almost 1.0" to 1.0
    std::cout << approximatelyEqualRel(a-1.0, 0.0, relEps) << '\n'; // compare "almost 0.0" to 0.0

    std::cout << approximatelyEqualAbsRel(a, 1.0, absEps, relEps) << '\n';     // compare "almost 1.0" to 1.0
    std::cout << approximatelyEqualAbsRel(a-1.0, 0.0, absEps, relEps) << '\n'; // compare "almost 0.0" to 0.0

    return 0;
}
true
false
true
true
您可以看到 `approximatelyEqualAbsRel()` 正确处理了小输入。
浮点数比较是一个难题，没有“一刀切”的算法适用于所有情况。然而，使用 `absEpsilon` 为 1e-12 和 `relEpsilon` 为 1e-8 的 `approximatelyEqualAbsRel()` 函数应该足以处理您遇到的大多数情况。
使 `approximatelyEqual` 函数成为 constexpr
高级
在 C++23 中，通过添加 `constexpr` 关键字，可以将两个 `approximatelyEqual` 函数变为 constexpr
// C++23 version
#include <algorithm> // for std::max
#include <cmath>     // for std::abs (constexpr in C++23)

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
constexpr bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}

// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
constexpr bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (std::abs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}
相关内容
我们在课程
F.1 -- Constexpr 函数
中介绍了 constexpr 函数。
然而，在 C++23 之前，我们会遇到一个问题。如果这些 constexpr 函数在常量表达式中被调用，它们会失败
int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };

    std::cout << std::boolalpha; // print true or false instead of 1 or 0

    constexpr bool same { approximatelyEqualAbsRel(a, 1.0, absEps, relEps) }; // compile error: must be initialized by a constant expression
    std::cout << same << '\n';

    return 0;
}
这是因为在常量表达式中使用的 constexpr 函数不能调用非 constexpr 函数，而 `std::abs` 直到 C++23 才被设为 constexpr。
不过，这很容易解决——我们可以放弃 `std::abs`，转而使用我们自己的 constexpr 绝对值实现。
// C++14/17/20 version
#include <algorithm> // for std::max
#include <iostream>

// Our own constexpr implementation of std::abs (for use in C++14/17/20)
// In C++23, use std::abs
// constAbs() can be called like a normal function, but can handle different types of values (e.g. int, double, etc...)
template <typename T>
constexpr T constAbs(T x)
{
    return (x < 0 ? -x : x);
}

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
constexpr bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
    return (constAbs(a - b) <= (std::max(constAbs(a), constAbs(b)) * relEpsilon));
}

// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
constexpr bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (constAbs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}

int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };

    std::cout << std::boolalpha; // print true or false instead of 1 or 0

    constexpr bool same { approximatelyEqualAbsRel(a, 1.0, absEps, relEps) };
    std::cout << same << '\n';

    return 0;
}
致进阶读者
上面版本的 `constAbs()` 是一个函数模板，它允许我们编写一个可以处理不同类型值的定义。我们在课程
11.6 -- 函数模板
中介绍了函数模板。
下一课
6.8
逻辑运算符
返回目录
上一课
6.6
条件运算符