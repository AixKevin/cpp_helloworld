# 8.3 — 常见 if 语句问题

8.3 — 常见 if 语句问题
Alex
2020年12月21日，太平洋标准时间上午11:18
2024年12月29日
本课程是
8.2 -- If 语句和块
的延续。在本课程中，我们将探讨在使用 if 语句时常见的一些问题。
嵌套 if 语句和悬空 else 问题
可以在其他 if 语句中嵌套 if 语句
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0) // outer if statement
        // it is bad coding style to nest if statements this way
        if (x <= 20) // inner if statement
            std::cout << x << " is between 0 and 20\n";

    return 0;
}
现在考虑以下程序
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0) // outer if-statement
        // it is bad coding style to nest if statements this way
        if (x <= 20) // inner if-statement
            std::cout << x << " is between 0 and 20\n";

    // which if statement does this else belong to?
    else
        std::cout << x << " is negative\n";

    return 0;
}
上述程序引入了一个潜在的歧义来源，称为
悬空 else
问题。上述程序中的 else 语句是与外部 if 语句匹配还是与内部 if 语句匹配？
答案是 else 语句与同一块中最后一个未匹配的 if 语句配对。因此，在上面的程序中，else 语句与内部 if 语句匹配，就像程序是这样编写的一样
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0) // outer if statement
    {
        if (x <= 20) // inner if statement
            std::cout << x << " is between 0 and 20\n";
        else // attached to inner if statement
            std::cout << x << " is negative\n";
    }

    return 0;
}
这会导致上述程序产生不正确的输出
Enter a number: 21
21 is negative
为了避免嵌套 if 语句时的这种歧义，最好将内部 if 语句显式地用块括起来。这使得我们可以毫不含糊地将 else 语句附加到内部或外部 if 语句
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0)
    {
        if (x <= 20)
            std::cout << x << " is between 0 and 20\n";
        else // attached to inner if statement
            std::cout << x << " is greater than 20\n";
    }
    else // attached to outer if statement
        std::cout << x << " is negative\n";

    return 0;
}
块内的 else 语句附加到内部 if 语句，块外的 else 语句附加到外部 if 语句。
扁平化嵌套 if 语句
嵌套 if 语句通常可以通过重构逻辑或使用逻辑运算符（在
6.8 -- 逻辑运算符
课程中介绍）来扁平化。嵌套层级较少的代码更不容易出错。
例如，上面的例子可以扁平化如下
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x < 0)
        std::cout << x << " is negative\n";
    else if (x <= 20) // only executes if x >= 0
        std::cout << x << " is between 0 and 20\n";
    else // only executes if x > 20
        std::cout << x << " is greater than 20\n";

    return 0;
}
这是另一个使用逻辑运算符在单个 if 语句中检查多个条件的例子
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    if (x > 0 && y > 0) // && is logical and -- checks if both conditions are true
        std::cout << "Both numbers are positive\n";
    else if (x > 0 || y > 0) // || is logical or -- checks if either condition is true
        std::cout << "One of the numbers is positive\n";
    else
        std::cout << "Neither number is positive\n";

    return 0;
}
空语句
空语句
是仅包含一个分号的表达式语句
if (x > 10)
    ; // this is a null statement
空语句不做任何事情。它们通常在语言要求存在语句但程序员不需要时使用。为了可读性，空语句通常放在单独的行上。在本章后面，当我们介绍循环时，我们将看到有意使用空语句的例子。
空语句很少与 if 语句有意使用。然而，它们可能会无意中给新手（或粗心的）程序员带来问题。考虑以下代码片段
if (nuclearCodesActivated()); // note the semicolon at the end of this line
    blowUpTheWorld();
在上面的代码片段中，程序员不小心在 if 语句的末尾添加了一个分号（一个常见的错误，因为分号结束许多语句）。这个不起眼的错误编译得很好，并导致代码片段执行，就像它是这样编写的一样
if (nuclearCodesActivated())
    ; // the semicolon acts as a null statement
blowUpTheWorld(); // and this line always gets executed!
警告
请注意不要用分号“终止”if 语句，否则您希望有条件执行的语句将无条件执行（即使它们在块内）。
提示
在 Python 中，
pass
关键字充当空语句。它通常用作稍后将实现的占位符。因为它是单词而不是符号，所以
pass
更不容易被无意误用，并且更易于搜索（允许您稍后轻松找到这些占位符）。
for x in [0, 1, 2]:
  pass               # To be completed in the future
在 C++ 中，我们可以通过使用预处理器来模拟
pass
#define PASS

void foo(int x, int y)
{
    if (x > y)
        PASS;
    else
        PASS;
}

int main()
{
    foo(4, 7);

    return 0;
}
为了与其他 C++ 语句保持一致，我们的
PASS
需要一个尾随分号。
PASS
被预处理器移除，尾随分号被编译器解释为空语句。
条件中的 Operator== 与 Operator=
在您的条件中，您应该使用
operator==
进行相等性测试，而不是
operator=
（这是赋值）。考虑以下程序
#include <iostream>

int main()
{
    std::cout << "Enter 0 or 1: ";
    int x{};
    std::cin >> x;
    if (x = 0) // oops, we used an assignment here instead of a test for equality
        std::cout << "You entered 0\n";
    else
        std::cout << "You entered 1\n";

    return 0;
}
这个程序会编译并运行，但在某些情况下会产生错误的结果
Enter 0 or 1: 0
You entered 1
事实上，这个程序总是会产生结果
You entered 1
。这是因为
x = 0
首先将值
0
赋给
x
，然后计算
x
的值，现在是
0
，它是布尔
false
。由于条件始终为
false
，因此 else 语句始终执行。
下一课
8.4
Constexpr if 语句
返回目录
上一课
8.2
If 语句和块