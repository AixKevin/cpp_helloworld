# 7.1 — 复合语句 (块)

7.1 — 复合语句 (块)
Alex
2007 年 6 月 18 日，太平洋时间晚上 10:06
2024 年 5 月 18 日
复合语句
（也称为
块
或
块语句
）是编译器视为单个语句的
零个或多个语句
的组。
块以
{
符号开头，以
}
符号结尾，要执行的语句置于两者之间。块可以用于允许单个语句的任何地方。块末尾不需要分号。
你已经在编写函数时看到过块的示例，因为函数体就是一个块。
int add(int x, int y)
{ // start block
    return x + y;
} // end block (no semicolon)

int main()
{ // start block

    // multiple statements
    int value {}; // this is initialization, not a block
    add(3, 4);

    return 0;

} // end block (no semicolon)
其他块内部的块
尽管函数不能嵌套在其他函数内部，但块
可以
嵌套在其他块内部。
int add(int x, int y)
{ // block
    return x + y;
} // end block

int main()
{ // outer block

    // multiple statements
    int value {};

    { // inner/nested block
        add(3, 4);
    } // end inner/nested block

    return 0;

} // end outer block
当块被嵌套时，包含块通常被称为
外部块
，而被包含的块被称为
内部块
或
嵌套块
。
使用块有条件地执行多个语句
块最常见的用例之一是与
if 语句
结合使用。默认情况下，如果条件评估为
true
，则
if 语句
执行单个语句。但是，如果我们希望在条件评估为
true
时执行多个语句，我们可以将此单个语句替换为语句块。
例如
#include <iostream>

int main()
{ // start of outer block
    std::cout << "Enter an integer: ";
    int value {};
    std::cin >> value;
    
    if (value >= 0)
    { // start of nested block
        std::cout << value << " is a positive integer (or zero)\n";
        std::cout << "Double this number is " << value * 2 << '\n';
    } // end of nested block
    else
    { // start of another nested block
        std::cout << value << " is a negative integer\n";
        std::cout << "The positive of this number is " << -value << '\n';
    } // end of another nested block

    return 0;
} // end of outer block
如果用户输入数字 3，此程序将打印
Enter an integer: 3
3 is a positive integer (or zero)
Double this number is 6
如果用户输入数字 -4，此程序将打印
Enter an integer: -4
-4 is a negative integer
The positive of this number is 4
块嵌套级别
甚至可以将块放入块中再放入块中。
#include <iostream>

int main()
{ // block 1, nesting level 1
    std::cout << "Enter an integer: ";
    int value {};
    std::cin >> value;
    
    if (value >  0)
    { // block 2, nesting level 2
        if ((value % 2) == 0)
        { // block 3, nesting level 3
            std::cout << value << " is positive and even\n";
        }
        else
        { // block 4, also nesting level 3
            std::cout << value << " is positive and odd\n";
        }
    }

    return 0;
}
函数的
嵌套级别
（也称为
嵌套深度
）是函数中任何一点（包括外部块）可以位于的最大嵌套块数。在上面的函数中，有 4 个块，但嵌套级别是 3，因为在此程序中，你永远不能同时位于超过 3 个块内部。
C++ 标准规定 C++ 编译器应支持 256 个嵌套级别——但并非所有编译器都支持（例如，截至撰写本文时，Visual Studio 支持的级别较少）。
将嵌套级别保持在 3 或更少是个好主意。正如过长的函数是重构（拆分为更小的函数）的好选择一样，过度嵌套的块难以阅读，也是重构（将最内部的块变为单独的函数）的好选择。
最佳实践
将函数的嵌套级别保持在 3 或更少。如果你的函数需要更多的嵌套级别，请考虑将函数重构为子函数。
下一课
7.2
用户定义命名空间和作用域解析运算符
返回目录
上一课
O.4
在二进制和十进制表示之间转换整数