# 6.6 — 条件运算符

6.6 — 条件运算符
Alex
2023 年 10 月 23 日，下午 1:42 PDT
2025 年 2 月 14 日
运算符
符号
形式
含义
条件
?:
c ? x : y
如果条件
c
为
true
，则计算
x
，否则计算
y
条件运算符
(
?:
)（有时也称为
算术 if
运算符）是一个三元运算符（接受 3 个操作数的运算符）。由于它历来是 C++ 唯一的三元运算符，因此有时也称为“三元运算符”。
?:
运算符提供了一种快捷方式，用于执行特定类型的 if-else 语句。
相关内容
我们在课程
4.10 -- if 语句介绍
中介绍了 if-else 语句。
回顾一下，if-else 语句采用以下形式
if (condition)
    statement1;
else
    statement2;
如果
condition
计算结果为
true
，则执行
statement1
，否则执行
statement2
。
else
和
statement2
是可选的。
?:
运算符采用以下形式
condition ? expression1 : expression2;
如果
condition
计算结果为
true
，则计算
expression1
，否则计算
expression2
。
:
和
expression2
不是可选的。
考虑一个如下所示的 if-else 语句
if (x > y)
    max = x;
else
    max = y;
这可以重写为
max = ((x > y) ? x : y);
在这种情况下，条件运算符有助于简化代码而不降低可读性。
一个例子
考虑以下示例
#include <iostream>

int getValue()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;
    return x;
}

int main()
{
    int x { getValue() };
    int y { getValue() };
    int max { (x > y) ? x : y };
    std::cout << "The max of " << x <<" and " << y << " is " << max << ".\n";

    return 0;
}
首先，我们输入
5
和
7
作为输入（因此
x
是
5
，
y
是
7
）。当
max
被初始化时，表达式
(5 > 7) ? 5 : 7
被求值。由于
5 > 7
为假，这会产生
false ? 5 : 7
，其求值为
7
。程序打印
The max of 5 and 7 is 7.
现在我们输入
7
和
5
作为输入（因此
x
是
7
，
y
是
5
）。在这种情况下，我们得到
(7 > 5) ? 7 : 5
，即
true ? 7 : 5
，其求值为
7
。程序打印
The max of 7 and 5 is 7.
条件运算符作为表达式的一部分进行求值
由于条件运算符作为表达式的一部分进行求值，因此它可以在任何接受表达式的地方使用。在条件运算符的操作数是常量表达式的情况下，条件运算符可以在常量表达式中使用。
这允许条件运算符在不能使用语句的地方使用。
例如，在初始化变量时
#include <iostream>

int main()
{
    constexpr bool inBigClassroom { false };
    constexpr int classSize { inBigClassroom ? 30 : 20 };
    std::cout << "The class size is: " << classSize << '\n';

    return 0;
}
没有直接的 if-else 替代方案。
你可能会尝试这样的事情
#include <iostream>

int main()
{
    constexpr bool inBigClassroom { false };

    if (inBigClassroom)
        constexpr int classSize { 30 };
    else
        constexpr int classSize { 20 }; 

    std::cout << "The class size is: " << classSize << '\n'; // Compile error: classSize not defined

    return 0;
}
然而，这不会编译，你会收到一个错误消息，指出
classSize
未定义。就像函数内部定义的变量在函数结束时消失一样，if 语句或 else 语句内部定义的变量在 if 语句或 else 语句结束时消失。因此，当我们尝试打印
classSize
时，它已经被销毁了。
如果你想使用 if-else，你必须这样做
#include <iostream>

int getClassSize(bool inBigClassroom)
{
    if (inBigClassroom)
        return 30;
    else
        return 20;
}

int main()
{
    const int classSize { getClassSize(false) };
    std::cout << "The class size is: " << classSize << '\n';

    return 0;
}
这个有效，因为
getClassSize(false)
是一个表达式，并且 if-else 逻辑在一个函数内部（我们可以使用语句）。但是当我们只需要使用条件运算符时，这会增加很多额外的代码。
条件运算符加括号
因为 C++ 优先于条件运算符的评估，大多数运算符的评估优先级更高，所以使用条件运算符编写的表达式很容易不按预期进行评估。
相关内容
我们将在未来的课程
6.1 -- 运算符优先级和结合性
中介绍 C++ 优先评估运算符的方式。
例如
#include <iostream>

int main()
{
    int x { 2 };
    int y { 1 };
    int z { 10 - x > y ? x : y };
    std::cout << z;
    
    return 0;
}
您可能期望它求值为
10 - (x > y ? x : y)
（求值为
8
），但它实际上求值为
(10 - x) > y ? x : y
（求值为
2
）。
这是另一个常见的错误示例
#include <iostream>

int main()
{
    int x { 2 };
    std::cout << (x < 0) ? "negative" : "non-negative";

    return 0;
}
你可能期望它打印
non-negative
，但它实际上打印
0
。
选读
在上面的示例中发生了以下情况。首先，
x < 0
求值为
false
。部分求值的表达式现在是
std::cout << false ? "negative" : "non-negative"
。因为
operator<<
具有比
operator?:
更高的优先级，所以这个表达式的求值方式就像它是
(std::cout << false) ? "negative" : "non-negative"
。因此
std::cout << false
被求值，它打印
0
（并返回
std::cout
）。
部分求值的表达式现在是
std::cout ? "negative" : "non-negative"
。由于条件中只剩下
std::cout
，编译器将尝试将其转换为
bool
，以便解析条件。或许令人惊讶的是，
std::cout
有一个定义的
bool
转换，它很可能返回
false
。假设它返回
false
，我们现在有
false ? "negative" : "non-negative"
，它求值为
"non-negative"
。因此我们完全求值的语句是
"non-negative";
。一个只是字面量（在这种情况下是字符串字面量）的表达式语句没有效果，所以我们完成了。
为避免此类评估优先级问题，条件运算符应按如下方式加括号
当在复合表达式（包含其他运算符的表达式）中使用时，将整个条件操作（包括操作数）加括号。
为了可读性，如果条件包含任何运算符（函数调用运算符除外），请考虑为其加括号。
条件运算符的操作数不需要加括号。
让我们看一些包含条件运算符的语句以及它们应该如何加括号
return isStunned ? 0 : movesLeft;           // not used in compound expression, condition contains no operators
int z { (x > y) ? x : y };                  // not used in compound expression, condition contains operators
std::cout << (isAfternoon() ? "PM" : "AM"); // used in compound expression, condition contains no operators (function call operator excluded)
std::cout << ((x > y) ? x : y);             // used in compound expression, condition contains operators
最佳实践
当在复合表达式中使用时，将整个条件操作（包括操作数）加括号。
为了可读性，如果条件包含任何运算符（函数调用运算符除外），请考虑为其加括号。
表达式的类型必须匹配或可转换
为遵守 C++ 的类型检查规则，以下之一必须为真
第二个和第三个操作数的类型必须匹配。
编译器必须能够找到一种方法将第二个和第三个操作数中的一个或两个转换为匹配的类型。编译器使用的转换规则相当复杂，在某些情况下可能会产生令人惊讶的结果。
致进阶读者
或者，第二个和第三个操作数中的一个或两个可以是一个 throw 表达式。我们在课程
27.2 -- 基本异常处理
中介绍了
throw
。
例如
#include <iostream>

int main()
{
    std::cout << (true ? 1 : 2) << '\n';    // okay: both operands have matching type int

    std::cout << (false ? 1 : 2.2) << '\n'; // okay: int value 1 converted to double

    std::cout << (true ? -1 : 2u) << '\n';  // surprising result: -1 converted to unsigned int, result out of range

    return 0;
}
假设是 4 字节整数，上面打印
1
2.2
4294967295
一般来说，混合使用基本类型操作数是可以的（不包括混合有符号和无符号值）。如果任一操作数不是基本类型，最好自己显式地将一个或两个操作数转换为匹配的类型，这样您就知道会得到什么。
相关内容
上面与混合有符号和无符号值相关的令人惊讶的情况是由于算术转换规则造成的，我们将在课程
10.5 -- 算术转换
中介绍。
如果编译器找不到将第二个和第三个操作数转换为匹配类型的方法，将导致编译错误
#include <iostream>

int main()
{
    constexpr int x{ 5 };
    std::cout << ((x != 5) ? x : "x is 5"); // compile error: compiler can't find common type for constexpr int and C-style string literal

    return 0;
}
在上面的示例中，其中一个表达式是整数，另一个是 C 风格的字符串字面量。编译器无法自行找到匹配的类型，因此将导致编译错误。
在这种情况下，您可以进行显式转换，或使用 if-else 语句
#include <iostream>
#include <string>

int main()
{
    int x{ 5 }; // intentionally non-constexpr for this example

    // We can explicitly convert the types to match
    std::cout << ((x != 5) ? std::to_string(x) : std::string{"x is 5"}) << '\n';

    // Or use an if-else statement
    if (x != 5)
        std::cout << x << '\n';
    else
        std::cout << "x is 5" << '\n';
    
    return 0;
}
致进阶读者
如果
x
是 constexpr，则条件
x != 5
是一个常量表达式。在这种情况下，应优先使用
if constexpr
而不是
if
，并且您的编译器可能会生成一个警告，表明这一点（如果您将警告视为错误，则该警告将升级为错误）。
由于我们还没有介绍
if constexpr
（我们将在课程
8.4 -- Constexpr if 语句
中介绍），为了避免潜在的编译器警告，本例中
x
是非 constexpr 的。
那么什么时候应该使用条件运算符呢？
条件运算符在执行以下操作之一时最有用
使用两个值之一初始化对象。
将两个值之一分配给对象。
将两个值之一传递给函数。
从函数返回两个值之一。
打印两个值之一。
复杂的表达式通常应避免使用条件运算符，因为它们容易出错且难以阅读。
最佳实践
在复杂表达式中尽量避免使用条件运算符。
下一课
6.7
关系运算符和浮点数比较
返回目录
上一课
6.5
逗号运算符