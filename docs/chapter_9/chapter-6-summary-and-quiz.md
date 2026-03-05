# 6.x — 第 6 章总结和测验

6.x — 第 6 章总结和测验
Alex
2011 年 9 月 11 日下午 5:02 PDT
2024 年 12 月 2 日
快速回顾
如果对运算符的优先级有任何疑问或可能造成混淆，请始终使用括号来消除歧义。
算术运算符都像在普通数学中一样工作。余数 (%) 运算符返回整数除法的余数。
增量和减量运算符可用于轻松增加或减少数字。尽可能避免使用这些运算符的后缀版本。
请注意副作用，特别是函数参数的评估顺序。不要在给定的语句中多次使用具有副作用的变量。
逗号运算符可以将多个语句压缩为一个。通常，将语句分开编写会更好。
条件运算符
(
?:
)（有时也称为
算术 if
运算符）是一个三元运算符（一个接受 3 个操作数的运算符）。给定形式为
c ? x : y
的条件运算，如果条件
c
评估为
true
，则
x
将被评估，否则
y
将被评估。条件运算符通常需要像这样用括号括起来
在复合表达式（包含其他运算符的表达式）中使用时，将整个条件运算符用括号括起来。
为了可读性，如果条件包含任何运算符（除了函数调用运算符），则将条件用括号括起来。
关系运算符可用于比较浮点数。注意避免对浮点数使用相等和不相等比较。
逻辑运算符允许我们形成复合条件语句。
小测验时间
完成以下程序
#include <iostream>

// Write the function getQuantityPhrase() here

// Write the function getApplesPluralized() here

int main()
{
    constexpr int maryApples { 3 };
    std::cout << "Mary has " << getQuantityPhrase(maryApples) << ' ' << getApplesPluralized(maryApples) << ".\n";

    std::cout << "How many apples do you have? ";
    int numApples{};
    std::cin >> numApples;

    std::cout << "You have " << getQuantityPhrase(numApples) << ' ' << getApplesPluralized(numApples) << ".\n";
 
    return 0;
}
样本输出
Mary has a few apples.
How many apples do you have? 1
You have a single apple.
getQuantityPhrase()
应该接受一个表示某物数量的单个 int 参数，并返回以下描述符
< 0 = “负数”
0 = “无”
1 = “一个”
2 = “几个”
3 = “一些”
> 3 = “许多”
getApplesPluralized()
应该接受一个表示苹果数量的单个 int 参数，并返回以下内容
1 = “apple”
否则 = “apples”
此函数应使用条件运算符。
显示提示
提示：从函数返回 C 风格字符串字面量作为
std::string_view
是可以的。
显示答案
#include <iostream>
#include <string_view>

std::string_view getQuantityPhrase(int num)
{
    if (num < 0)
        return "negative";
    if (num == 0)
        return "no";
    if (num == 1)
        return "a single";
    if (num == 2)
        return "a couple of";
    if (num == 3)
        return "a few";
    return "many";
}

std::string_view getApplesPluralized(int num)
{
    return (num == 1) ? "apple" : "apples";
}

int main()
{
    constexpr int maryApples { 3 };
    std::cout << "Mary has " << getQuantityPhrase(maryApples) << ' ' << getApplesPluralized(maryApples) << ".\n";

    std::cout << "How many apples do you have? ";
    int numApples{};
    std::cin >> numApples;

    std::cout << "You have " << getQuantityPhrase(numApples) << ' ' << getApplesPluralized(numApples) << ".\n";
 
    return 0;
}
下一课
O.1
使用 std::bitset 进行位标志和位操作
返回目录
上一课
6.8
逻辑运算符