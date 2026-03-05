# 8.6 — Switch 穿透和作用域

8.6 — Switch 穿透和作用域
Alex
2020年12月21日，太平洋标准时间上午11:20
2024年9月1日
本课程将继续我们从上节课
8.5 -- Switch 语句基础
开始的 switch 语句探索。在上一课中，我们提到标签下的每组语句都应以一个
break 语句
或一个
return 语句
结束。
在本课程中，我们将探讨原因，并讨论一些有时会让新程序员感到困惑的 switch 作用域问题。
穿透（Fallthrough）
当 switch 表达式匹配一个 case 标签或可选的 default 标签时，执行从匹配标签后的第一个语句开始。执行将顺序继续，直到以下终止条件之一发生：
到达 switch 块的末尾。
另一个控制流语句（通常是
break
或
return
）导致 switch 块或函数退出。
其他情况中断了程序的正常流程（例如，操作系统关闭程序，宇宙内爆等…）
请注意，存在另一个 case 标签
不是
这些终止条件之一——因此，如果没有
break
或
return
，执行将溢出到后续的 case 中。
这是一个展示这种行为的程序：
#include <iostream>

int main()
{
    switch (2)
    {
    case 1: // Does not match
        std::cout << 1 << '\n'; // Skipped
    case 2: // Match!
        std::cout << 2 << '\n'; // Execution begins here
    case 3:
        std::cout << 3 << '\n'; // This is also executed
    case 4:
        std::cout << 4 << '\n'; // This is also executed
    default:
        std::cout << 5 << '\n'; // This is also executed
    }

    return 0;
}
该程序输出以下内容：
2
3
4
5
这可能不是我们想要的！当执行从一个标签下的语句流向后续标签下的语句时，这被称为
穿透
。
警告
一旦 case 或 default 标签下的语句开始执行，它们将溢出（穿透）到后续的 case 中。
break
或
return
语句通常用于防止这种情况。
由于穿透很少是期望或有意的，许多编译器和代码分析工具会将穿透标记为警告。
[[fallthrough]] 属性
注释有意的穿透是告诉其他开发人员穿透是有意为之的常见约定。虽然这对其他开发人员有用，但编译器和代码分析工具不知道如何解释注释，因此它不会消除警告。
为了解决这个问题，C++17 添加了一个名为
[[fallthrough]]
的新属性。
属性
是现代 C++ 的一个特性，允许程序员向编译器提供一些关于代码的额外数据。要指定一个属性，属性名称放在双括号之间。属性不是语句——相反，它们几乎可以在任何上下文相关的地方使用。
[[fallthrough]]
属性修改一个
null 语句
，以表明穿透是有意的（并且不应触发任何警告）。
#include <iostream>

int main()
{
    switch (2)
    {
    case 1:
        std::cout << 1 << '\n';
        break;
    case 2:
        std::cout << 2 << '\n'; // Execution begins here
        [[fallthrough]]; // intentional fallthrough -- note the semicolon to indicate the null statement
    case 3:
        std::cout << 3 << '\n'; // This is also executed
        break;
    }

    return 0;
}
这个程序打印
2
3
并且它不应该产生任何关于穿透的警告。
最佳实践
使用
[[fallthrough]]
属性（连同空语句）来表示有意的穿透。
连续的 case 标签
您可以使用逻辑或运算符将多个测试组合成一个语句：
bool isVowel(char c)
{
    return (c=='a' || c=='e' || c=='i' || c=='o' || c=='u' ||
        c=='A' || c=='E' || c=='I' || c=='O' || c=='U');
}
这与我们在 switch 语句介绍中提出的挑战相同：
c
被评估多次，读者必须确保每次评估的都是
c
。
您可以通过放置多个连续的 case 标签来使用 switch 语句执行类似的操作：
bool isVowel(char c)
{
    switch (c)
    {
    case 'a': // if c is 'a'
    case 'e': // or if c is 'e'
    case 'i': // or if c is 'i'
    case 'o': // or if c is 'o'
    case 'u': // or if c is 'u'
    case 'A': // or if c is 'A'
    case 'E': // or if c is 'E'
    case 'I': // or if c is 'I'
    case 'O': // or if c is 'O'
    case 'U': // or if c is 'U'
        return true;
    default:
        return false;
    }
}
请记住，执行从匹配的 case 标签后的第一个语句开始。case 标签不是语句（它们是标签），所以它们不计算在内。
上面程序中
所有
case 语句后的第一个语句是
return true
，所以如果任何 case 标签匹配，函数将返回
true
。
因此，我们可以“堆叠” case 标签，使所有这些 case 标签共享相同的后续语句集。这不被视为穿透行为，因此此处不需要使用注释或
[[fallthrough]]
。
标签不定义新的作用域
对于
if 语句
，在 if-条件之后只能有一个语句，并且该语句被隐式地视为在一个块内：
if (x > 10)
    std::cout << x << " is greater than 10\n"; // this line implicitly considered to be inside a block
然而，对于 switch 语句，标签后的语句都作用于 switch 块。没有创建隐式块。
switch (1)
{
case 1: // does not create an implicit block
    foo(); // this is part of the switch scope, not an implicit block to case 1
    break; // this is part of the switch scope, not an implicit block to case 1
default:
    std::cout << "default case\n";
    break;
}
在上面的示例中，
case 1
和 default 标签之间的 2 条语句被作用于 switch 块的一部分，而不是
case 1
的隐式块。
case 语句内的变量声明和初始化
您可以在 switch 内部声明或定义（但不能初始化）变量，无论是在 case 标签之前还是之后：
switch (1)
{
    int a; // okay: definition is allowed before the case labels
    int b{ 5 }; // illegal: initialization is not allowed before the case labels

case 1:
    int y; // okay but bad practice: definition is allowed within a case
    y = 4; // okay: assignment is allowed
    break;

case 2:
    int z{ 4 }; // illegal: initialization is not allowed if subsequent cases exist
    y = 5; // okay: y was declared above, so we can use it here too
    break;

case 3:
    break;
}
尽管变量
y
在
case 1
中定义，但它也在
case 2
中使用。switch 内部的所有语句都被视为同一作用域的一部分。因此，在一个 case 中声明或定义的变量可以在后面的 case 中使用，即使定义变量的 case 从未执行（因为 switch 跳过了它）！
然而，变量的初始化
确实
需要定义来执行。在任何不是最后一个 case 的 case 中，都不允许初始化变量（因为如果存在后续定义的 case，switch 可能会跳过初始化程序，在这种情况下变量将是未定义的，访问它将导致未定义行为）。在第一个 case 之前也不允许初始化，因为这些语句永远不会执行，因为 switch 无法到达它们。
如果一个 case 需要定义和/或初始化新变量，最佳实践是在 case 语句下的显式块中进行：
switch (1)
{
case 1:
{ // note addition of explicit block here
    int x{ 4 }; // okay, variables can be initialized inside a block inside a case
    std::cout << x;
    break;
}

default:
    std::cout << "default case\n";
    break;
}
最佳实践
如果在 case 语句中定义变量，请在 case 内的块中进行。
小测验时间
问题 #1
编写一个名为
calculate()
的函数，它接受两个整数和一个字符，代表以下数学运算之一：+、-、*、/ 或 %（求余）。使用 switch 语句对整数执行适当的数学运算，并返回结果。如果将无效运算符传递给函数，函数应打印错误消息。对于除法运算符，执行整数除法，不必担心除以零。
提示：“operator”是一个关键字，变量不能命名为“operator”。
显示答案
#include <iostream>

int calculate(int x, int y, char op)
{
    switch (op)
    {
    case '+':
        return x + y;
    case '-':
        return x - y;
    case '*':
        return x * y;
    case '/':
        return x / y;
    case '%':
        return x % y;
    default:
        std::cout << "calculate(): Unhandled case\n";
        return 0;
    }
}

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    std::cout << "Enter a mathematical operator (+, -, *, /, or %): ";
    char op{};
    std::cin >> op;

    // We'll call calculate first so an invalid operator prints an error message on its own line
    int result{ calculate(x, y, op) };
    std::cout << x << ' ' << op << ' ' << y << " is " << result << '\n';

    return 0;
}
下一课
8.7
Goto 语句
返回目录
上一课
8.5
Switch 语句基础