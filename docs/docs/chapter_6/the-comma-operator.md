# 6.5 — 逗号运算符

6.5 — 逗号运算符
Alex
2007 年 6 月 14 日，太平洋夏令时上午 7:41
2023 年 10 月 24 日
运算符
符号
形式
操作
逗号
,
x, y
先计算 x，再计算 y，返回 y 的值
逗号运算符 (,)
允许你在允许单个表达式的地方计算多个表达式。逗号运算符计算左操作数，然后是右操作数，然后返回右操作数的结果。
例如
#include <iostream>

int main()
{
    int x{ 1 };
    int y{ 2 };

    std::cout << (++x, ++y) << '\n'; // increment x and y, evaluates to the right operand

    return 0;
}
首先计算逗号运算符的左操作数，这将使 *x* 从 *1* 递增到 *2*。接下来，计算右操作数，这将使 *y* 从 *2* 递增到 *3*。逗号运算符返回右操作数的结果 (*3*)，然后将其打印到控制台。
请注意，逗号的优先级是所有运算符中最低的，甚至低于赋值运算符。因此，以下两行代码执行不同的操作
z = (a, b); // evaluate (a, b) first to get result of b, then assign that value to variable z.
z = a, b; // evaluates as "(z = a), b", so z gets assigned the value of a, and b is evaluated and discarded.
这使得逗号运算符的使用有些危险。
在几乎所有情况下，使用逗号运算符编写的语句最好写成单独的语句。例如，上面的代码可以写成
#include <iostream>

int main()
{
    int x{ 1 };
    int y{ 2 };

    ++x;
    std::cout << ++y << '\n';

    return 0;
}
大多数程序员根本不使用逗号运算符，唯一的例外是在 *for 循环*内部，它的使用相当普遍。我们将在未来的课程
8.10 -- for 语句
中讨论 for 循环。
最佳实践
避免使用逗号运算符，除非在 *for 循环*中。
逗号作为分隔符
在 C++ 中，逗号符号通常用作分隔符，这些用法不调用逗号运算符。分隔符逗号的一些示例
void foo(int x, int y) // Separator comma used to separate parameters in function definition
{
    add(x, y); // Separator comma used to separate arguments in function call
    constexpr int z{ 3 }, w{ 5 }; // Separator comma used to separate multiple variables being defined on the same line (don't do this)
}
无需避免分隔符逗号（声明多个变量时除外，你不应该这样做）。
下一课
6.6
条件运算符
返回目录
上一课
6.4
递增/递减运算符和副作用