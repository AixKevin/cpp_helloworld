# 9.3 — C++ 中常见的语义错误

9.3 — C++ 中常见的语义错误
Alex
2020年12月21日，太平洋标准时间上午11:29
2024年11月10日
在课程
3.1 -- 语法和语义错误
中，我们讨论了当您编写不符合 C++ 语言语法的代码时发生的
语法错误
。编译器会通知您此类错误，因此它们很容易被捕获，并且通常很容易修复。
我们还讨论了
语义错误
，当您编写的代码没有达到预期效果时，就会发生语义错误。编译器通常不会捕获语义错误（尽管在某些情况下，智能编译器可能会生成警告）。
语义错误可能导致与
未定义行为
相同的大多数症状，例如导致程序产生错误的结果、导致不稳定的行为、损坏程序数据、导致程序崩溃——或者它们可能根本没有任何影响。
在编写程序时，几乎不可避免地会犯语义错误。您可能会在使用程序时注意到其中一些错误：例如，如果您正在编写一个迷宫游戏，而您的角色能够穿墙。测试您的程序（
9.1 -- 您的代码测试简介
）也可以帮助发现语义错误。
但是还有一件事可以帮助您——那就是知道哪种类型的语义错误最常见，这样您就可以花更多时间确保这些情况下的正确性。
在本课程中，我们将介绍 C++ 中最常见的语义错误类型（其中大多数与某种形式的流控制有关）。
条件逻辑错误
最常见的语义错误类型之一是条件逻辑错误。当程序员错误地编写条件语句或循环条件的逻辑时，就会发生**条件逻辑错误**。这是一个简单的例子
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    if (x >= 5) // oops, we used operator>= instead of operator>
        std::cout << x << " is greater than 5\n";

    return 0;
}
以下是展示条件逻辑错误的程序运行
Enter an integer: 5
5 is greater than 5
当用户输入
5
时，条件表达式
x >= 5
计算结果为
true
，因此执行相关语句。
这是另一个使用 for 循环的例子
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    // oops, we used operator> instead of operator<
    for (int count{ 1 }; count > x; ++count)
    {
        std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
这个程序应该打印 1 到用户输入的数字之间的所有数字。但它实际做了什么
Enter an integer: 5
它什么也没打印。这是因为进入 for 循环时，
count > x
为
false
，因此循环根本不会迭代。
无限循环
在课程
8.8 -- 循环和 while 语句简介
中，我们介绍了无限循环，并展示了这个例子
#include <iostream>
 
int main()
{
    int count{ 1 };
    while (count <= 10) // this condition will never be false
    {
        std::cout << count << ' '; // so this line will repeatedly execute
    }
 
    std::cout << '\n'; // this line will never execute

    return 0; // this line will never execute
}
在这种情况下，我们忘记了递增
count
，因此循环条件永远不会为假，循环将继续打印
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
……直到用户关闭程序。
这是另一个老师们喜欢作为测验问题提出的例子。下面的代码有什么问题？
#include <iostream>

int main()
{
    for (unsigned int count{ 5 }; count >= 0; --count)
    {
        if (count == 0)
            std::cout << "blastoff! ";
        else
          std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
这个程序应该打印
5 4 3 2 1 blastoff!
，它确实打印了，但它并没有停止在那里。实际上，它打印了
5 4 3 2 1 blastoff! 4294967295 4294967294 4294967293 4294967292 4294967291
然后不断递减。程序永远不会终止，因为当
count
是无符号整数时，
count >= 0
永远不会是
false
。
差一错误
**差一错误**是指循环执行次数过多或过少时发生的错误。这是我们在课程
8.10 -- For 语句
中介绍过的一个例子
#include <iostream>

int main()
{
    for (int count{ 1 }; count < 5; ++count)
    {
        std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
程序员打算让这段代码打印
1 2 3 4 5
。但是，使用了错误的比较运算符（
<
而不是
<=
），因此循环执行次数比预期少一次，打印
1 2 3 4
。
运算符优先级不正确
在课程
6.8 -- 逻辑运算符
中，以下程序犯了一个运算符优先级错误
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 7 };

    if (!x > y) // oops: operator precedence issue
        std::cout << x << " is not greater than " << y << '\n';
    else
        std::cout << x << " is greater than " << y << '\n';

    return 0;
}
因为
逻辑非
的优先级高于
运算符 >
，所以条件表达式的评估方式就好像它是
(!x) > y
，这与程序员的意图不符。
结果，这个程序打印
5 is greater than 7
这在同一个表达式中混合使用逻辑或和逻辑与时也可能发生（逻辑与的优先级高于逻辑或）。使用显式括号来避免此类错误。
浮点类型的精度问题
以下浮点变量没有足够的精度来存储整个数字
#include <iostream>

int main()
{
    float f{ 0.123456789f };
    std::cout << f << '\n';

    return 0;
}
由于缺乏精度，数字会略微四舍五入
0.123457
在课程
6.7 -- 关系运算符和浮点数比较
中，我们讨论了由于微小的舍入误差（以及如何处理）而导致使用
operator==
和
operator!=
对浮点数进行比较可能出现问题。这是一个例子
#include <iostream>

int main()
{
    double d{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 }; // should sum to 1.0

    if (d == 1.0)
        std::cout << "equal\n";
    else
        std::cout << "not equal\n";

    return 0;
}
这个程序打印
not equal
对浮点数进行的算术运算越多，它积累的微小舍入误差就越多。
整数除法
在下面的例子中，我们本意是进行浮点除法，但由于两个操作数都是整数，我们最终进行了整数除法
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 3 };

    std::cout << x << " divided by " << y << " is: " << x / y << '\n'; // integer division

    return 0;
}
这会打印
5 divided by 3 is: 1
在课程
6.2 -- 算术运算符
中，我们展示了可以使用 static_cast 将其中一个整数操作数转换为浮点值以进行浮点除法。
意外的空语句
在课程
8.3 -- 常见的 if 语句问题
中，我们讨论了
空语句
，即什么也不做的语句。
在下面的程序中，我们只希望在获得用户许可的情况下摧毁世界
#include <iostream>

void blowUpWorld()
{
    std::cout << "Kaboom!\n";
} 

int main()
{
    std::cout << "Should we blow up the world again? (y/n): ";
    char c{};
    std::cin >> c;

    if (c == 'y');     // accidental null statement here
        blowUpWorld(); // so this will always execute since it's not part of the if-statement
 
    return 0;
}
然而，由于一个意外的
空语句
，函数调用
blowUpWorld()
总是被执行，所以无论如何我们都会摧毁它
Should we blow up the world again? (y/n): n
Kaboom!
当需要复合语句时未使用复合语句
上述程序的另一个变体，它总是摧毁世界
#include <iostream>

void blowUpWorld()
{
    std::cout << "Kaboom!\n";
} 

int main()
{
    std::cout << "Should we blow up the world again? (y/n): ";
    char c{};
    std::cin >> c;

    if (c == 'y')
        std::cout << "Okay, here we go...\n";
        blowUpWorld(); // Will always execute.  Should be inside compound statement.
 
    return 0;
}
这个程序打印
Should we blow up the world again? (y/n): n
Kaboom!
一个
悬空else
（在课程
8.3 -- 常见的 if 语句问题
中讨论）也属于这一类别。
在条件语句中使用赋值而不是相等性
因为赋值运算符（
=
）和相等运算符（
==
）相似，我们可能本打算使用相等运算符，但却意外地使用了赋值运算符
#include <iostream>

void blowUpWorld()
{
    std::cout << "Kaboom!\n";
} 

int main()
{
    std::cout << "Should we blow up the world again? (y/n): ";
    char c{};
    std::cin >> c;

    if (c = 'y') // uses assignment operator instead of equality operator
        blowUpWorld();
 
    return 0;
}
这个程序打印
Should we blow up the world again? (y/n): n
Kaboom!
赋值运算符返回其左操作数。
c = 'y'
首先执行，它将
y
赋值给
c
并返回
c
。然后评估
if (c)
。由于
c
现在是非零的，它被隐式转换为
bool
值
true
，并且与 if 语句关联的语句被执行。
因为条件语句中的赋值几乎从不被有意使用，所以现代编译器在遇到这种情况时通常会发出警告。但是，如果您没有解决所有警告的习惯，此类警告很容易被忽略。
调用函数时忘记使用函数调用运算符
#include <iostream>

int getValue()
{
    return 5;
}

int main()
{
    std::cout << getValue << '\n';

    return 0;
}
虽然您可能期望此程序打印
5
，但它很可能会打印
1
（在某些编译器上，它会以十六进制打印内存地址）。
我们没有使用
getValue()
（它会调用函数并产生一个
int
返回值），而是使用了没有函数调用运算符的
getValue
。在许多情况下，这会导致一个值被转换为
bool
值
true
）。
在上面的例子中，输出的是这个
bool
值
true
，它打印
1
。
致进阶读者
不调用函数而使用其名称通常会产生一个函数指针，其中包含函数的地址。这样的函数指针将隐式转换为
bool
值。而且由于该指针的地址永远不应为
0
，因此该
bool
值将始终为
true
。
我们在课程
20.1 -- 函数指针
中介绍了函数指针。
还有什么？
以上很好地代表了 C++ 新手程序员最常见的语义错误类型，但还有很多。读者们，如果您有任何其他您认为常见的陷阱，请在评论中留言。
下一课
9.4
检测和处理错误
返回目录
上一课
9.2
代码覆盖率