# 8.5 — Switch 语句基础

8.5 — Switch 语句基础
Alex
2007 年 6 月 21 日，太平洋夏令时下午 6:41
2024 年 12 月 28 日
尽管可以将许多 if-else 语句串联起来，但这既难以阅读又效率低下。考虑以下程序：
#include <iostream>

void printDigitName(int x)
{
    if (x == 1)
        std::cout << "One";
    else if (x == 2)
        std::cout << "Two";
    else if (x == 3)
        std::cout << "Three";
    else
        std::cout << "Unknown";
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
printDigitName()
中的变量
x
根据传入的值可能会被评估多达三次（效率低下），而且读者必须确保每次评估的都是
x
（而不是其他变量）。
因为针对一组不同值测试变量或表达式的相等性很常见，所以 C++ 提供了一种替代的条件语句，称为 switch 语句，专门用于此目的。下面是使用 switch 的相同程序：
#include <iostream>

void printDigitName(int x)
{
    switch (x)
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    default:
        std::cout << "Unknown";
        return;
    }
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
switch 语句
背后的思想很简单：一个表达式（有时称为条件）被评估以产生一个值。
然后发生以下情况之一：
如果表达式的值等于任何 case 标签后的值，则执行匹配 case 标签后的语句。
如果没有找到匹配的值并且存在 default 标签，则执行 default 标签后的语句。
如果没有找到匹配的值并且没有 default 标签，则跳过 switch。
让我们更详细地研究这些概念。
开始一个 switch
我们通过使用
switch
关键字开始一个 switch 语句，后跟括号，其中包含我们想要评估的条件表达式。通常表达式只是一个单个变量，但它可以是任何有效的表达式。
switch 中的条件必须评估为整数类型（如果您需要提醒哪些基本类型被视为整数类型，请参阅课程
4.1 -- 基本数据类型介绍
）或枚举类型（在未来的课程
13.2 -- 未限定作用域枚举
和
13.6 -- 限定作用域枚举 (enum classes)
中介绍），或者可以转换为其中之一。评估为浮点类型、字符串和大多数其他非整数类型的表达式不能在此处使用。
致进阶读者
为什么 switch 类型只允许整数（或枚举）类型？答案是 switch 语句旨在高度优化。历史上，编译器实现 switch 语句最常见的方式是通过
跳转表
——而跳转表只适用于整数值。
对于那些已经熟悉数组的人来说，跳转表的工作方式很像数组，一个整数值被用作数组索引来“直接跳转”到结果。这比进行一堆顺序比较要高效得多。
当然，编译器不一定非要使用跳转表来实现 switch，有时它们也不会。从技术上讲，C++ 并没有理由不能放宽限制，以便其他类型也可以使用，它们只是还没有这样做（截至 C++23）。
在条件表达式之后，我们声明一个块。在块内部，我们使用标签来定义所有我们想要测试相等性的值。switch 语句有两种标签，我们将在后面讨论。
Case 标签
第一种标签是
case 标签
，它使用
case
关键字声明，后跟一个常量表达式。常量表达式必须与条件的类型匹配或必须可转换为该类型。
如果条件表达式的值等于
case 标签
后的表达式，则执行在该
case 标签
后的第一条语句处开始，然后顺序继续。
以下是条件匹配
case 标签
的示例：
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x is evaluated to produce value 2
    {
    case 1:
        std::cout << "One";
        return;
    case 2: // which matches the case statement here
        std::cout << "Two"; // so execution starts here
        return; // and then we return to the caller
    case 3:
        std::cout << "Three";
        return;
    default:
        std::cout << "Unknown";
        return;
    }
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
此代码打印
Two
在上面的程序中，
x
被评估以产生值
2
。因为存在一个值为
2
的 case 标签，所以执行跳到该匹配 case 标签下方的语句。程序打印
Two
，然后执行
return 语句
，返回到调用者。
您可以拥有的 case 标签数量没有实际限制，但 switch 中所有的 case 标签都必须是唯一的。也就是说，您不能这样做：
switch (x)
{
case 54:
case 54:  // error: already used value 54!
case '6': // error: '6' converts to integer value 54, which is already used
}
如果条件表达式不匹配任何 case 标签，则不执行任何 case。我们将在稍后展示一个示例。
默认标签
第二种标签是
default 标签
（通常称为
default case
），它使用
default
关键字声明。如果条件表达式不匹配任何 case 标签并且存在 default 标签，则执行在 default 标签后的第一条语句处开始。
以下是条件匹配 default 标签的示例：
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x is evaluated to produce value 5
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    default: // which does not match to any case labels
        std::cout << "Unknown"; // so execution starts here
        return; // and then we return to the caller
    }
}

int main()
{
    printDigitName(5);
    std::cout << '\n';

    return 0;
}
此代码打印
Unknown
default 标签是可选的，每个 switch 语句只能有一个 default 标签。按照惯例，default case 放置在 switch 块的最后。
最佳实践
将 default case 放在 switch 块的最后。
没有匹配的 case 标签且没有 default case
如果条件表达式的值不匹配任何 case 标签，并且没有提供 default case，则 switch 内部不执行任何 case。执行在 switch 块结束之后继续。
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x is evaluated to produce value 5
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    // no matching case exists and there is no default case
    }

    // so execution continues here
    std::cout << "Hello";
}

int main()
{
    printDigitName(5);
    std::cout << '\n';

    return 0;
}
在上面的示例中，
x
评估为
5
，但没有匹配
5
的 case 标签，也没有 default case。结果，没有 case 执行。执行在 switch 块之后继续，打印
Hello
。
休息一下
在上面的例子中，我们使用 return 语句来停止标签后面语句的执行。然而，这也会退出整个函数。
break 语句
（使用
break
关键字声明）告诉编译器我们已经完成了 switch 内语句的执行，并且执行应该在 switch 块结束后的语句处继续。这允许我们退出 switch 语句而无需退出整个函数。
这是一个稍微修改过的示例，使用
break
而不是
return
重写：
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x evaluates to 3
    {
    case 1:
        std::cout << "One";
        break;
    case 2:
        std::cout << "Two";
        break;
    case 3:
        std::cout << "Three"; // execution starts here
        break; // jump to the end of the switch block
    default:
        std::cout << "Unknown";
        break;
    }

    // execution continues here
    std::cout << " Ah-Ah-Ah!";
}

int main()
{
    printDigitName(3);
    std::cout << '\n';

    return 0;
}
上面的例子打印：
Three Ah-Ah-Ah!
最佳实践
标签下的每组语句都应该以 break 语句或 return 语句结束。这包括 switch 中最后一个标签下的语句。
那么，如果您不以
break
或
return
结束标签下的一组语句会发生什么？我们将在下一课中探讨该主题和其他主题。
标签通常不缩进
在课程
2.9 -- 命名冲突和命名空间介绍
中，我们注意到代码通常缩进一级，以帮助识别它是嵌套作用域区域的一部分。由于 switch 的花括号定义了一个新的作用域区域，我们通常会将其花括号内的所有内容缩进一级。
另一方面，标签不定义嵌套作用域。因此，标签后面的代码通常不缩进。
然而，如果我们将标签和随后的语句都缩进到相同的级别，我们最终会得到如下所示：
// Unreadable version
void printDigitName(int x)
{
    switch (x)
    {
        case 1:
        std::cout << "One";
        return;
        case 2:
        std::cout << "Two";
        return;
        case 3:
        std::cout << "Three";
        return;
        default:
        std::cout << "Unknown";
        return;
    }
}
这使得很难确定每个 case 的开始和结束位置。
我们这里有两种选择。首先，我们可以无论如何都缩进标签后面的语句：
// Acceptable but not preferred version
void printDigitName(int x)
{
    switch (x)
    {
        case 1: // indented from switch block
            std::cout << "One"; // indented from label (misleading)
            return;
        case 2:
            std::cout << "Two";
            return;
        case 3:
            std::cout << "Three";
            return;
        default:
            std::cout << "Unknown";
            return;
    }
}
虽然这肯定比之前的版本更具可读性，但它暗示每个标签下的语句都在嵌套作用域中，而事实并非如此（我们将在下一课中看到这方面的例子，其中我们在一个 case 中定义的变量可以在另一个 case 中使用）。这种格式被认为是可接受的（因为它可读），但不是首选。
按照惯例，标签根本不缩进：
// Preferred version
void printDigitName(int x)
{
    switch (x)
    {
    case 1: // not indented from switch statement
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    default:
        std::cout << "Unknown";
        return;
    }
}
这使得识别每个标签变得容易。而且由于语句只从 switch 块缩进一级，它正确地暗示了这些语句都是 switch 块作用域的一部分。
在未来的课程中，我们将遇到其他类型的标签——出于同样的原因，这些标签通常也不缩进。
最佳实践
尽量不要缩进标签。这使得它们能够从周围的代码中脱颖而出，而不会暗示它们正在定义嵌套作用域区域。
Switch 与 if-else
当有一个单一表达式（具有非布尔整数类型或枚举类型）我们想要针对少量值进行相等性评估时，switch 语句是最佳选择。如果 case 标签的数量太大，switch 可能会难以阅读。
与等效的 if-else 语句相比，switch 语句更具可读性，更清楚地表明在每种情况下测试的是相同的表达式的相等性，并且具有只评估一次表达式的优点（使其更高效）。
然而，if-else 灵活性显著更高。if 或 if-else 通常更好的情况：
测试除了相等性之外的比较表达式（例如
x > 5
）
测试多个条件（例如
x == 5 && y == 6
）
确定值是否在范围内（例如
x >= 5 && x <= 10
）
表达式的类型是 switch 不支持的（例如
d == 4.0
）。
表达式评估为
bool
。
最佳实践
当针对少量值测试单个表达式（具有非布尔整数类型或枚举类型）的相等性时，优先使用 switch 语句而不是 if-else 语句。
下一课
8.6
Switch 穿透与作用域
返回目录
上一课
8.4
Constexpr if 语句