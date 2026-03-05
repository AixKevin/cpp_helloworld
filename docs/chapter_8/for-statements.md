# 8.10 — For 语句

8.10 — For 语句
Alex
2007 年 6 月 25 日，太平洋夏令时下午 6:48
2025 年 2 月 19 日
到目前为止，C++ 中使用最广泛的循环语句是 for 语句。当存在一个明显的循环变量时，
for 语句
（也称为
for 循环
）是首选，因为它让我们能够轻松简洁地定义、初始化、测试和更改循环变量的值。
自 C++11 起，有两种不同类型的 for 循环。我们将在本课程中介绍经典的 for 语句，并在未来的课程（
16.8 -- 基于范围的 for 循环 (for-each)
）中介绍较新的基于范围的 for 语句，届时我们已涵盖一些其他先决条件主题。
for 语句在抽象中看起来非常简单
for (init-statement; condition; end-expression)
   statement;
最初理解 for 语句工作原理的最简单方法是将其转换为等效的 while 语句
{ // note the block here
    init-statement; // used to define variables used in the loop
    while (condition)
    {
        statement; 
        end-expression; // used to modify the loop variable prior to reassessment of the condition
    }
} // variables defined inside the loop go out of scope here
for 语句的评估
for 语句分为 3 部分进行评估
首先，执行 init-statement。这只在循环初始化时发生一次。init-statement 通常用于变量定义和初始化。这些变量具有“循环作用域”，这实际上只是一种块作用域的形式，其中这些变量从定义点到循环语句结束都存在。在我们的 while 循环等效中，您可以看到 init-statement 位于包含循环的块内，因此在包含循环的块结束时，在 init-statement 中定义的变量将超出作用域。
其次，在每次循环迭代时，评估条件。如果条件评估为
true
，则执行语句。如果条件评估为
false
，则循环终止，并继续执行循环之外的下一个语句。
最后，在语句执行后，评估 end-expression。通常，此表达式用于递增或递减在 init-statement 中定义的循环变量。在 end-expression 评估后，执行返回到第二步（并再次评估条件）。
关键见解
for 语句不同部分的执行顺序如下
Init-statement
条件（如果为 false，循环在此终止）。
循环体
End-expression（然后跳回条件）
请注意，end-expression 在循环语句
之后
执行，然后重新评估条件。
让我们看一个 for 循环示例并讨论其工作原理
#include <iostream>

int main()
{
    for (int i{ 1 }; i <= 10; ++i)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
首先，我们声明一个名为
i
的循环变量，并将其初始化为值
1
。
其次，评估
i <= 10
，由于
i
是
1
，因此评估为
true
。因此，执行语句，打印
1
和一个空格。
最后，评估
++i
，将
i
递增到
2
。然后循环返回到第二步。
现在，再次评估
i <= 10
。由于
i
的值为
2
，因此评估为
true
，因此循环再次迭代。语句打印
2
和一个空格，并且
i
递增到
3
。循环继续迭代，直到
i
最终递增到
11
，此时
i <= 10
评估为
false
，循环退出。
因此，该程序打印结果
1 2 3 4 5 6 7 8 9 10
为了举例说明，让我们将上面的 for 循环转换为等效的 while 循环
#include <iostream>

int main()
{
    { // the block here ensures block scope for i
        int i{ 1 }; // our init-statement
        while (i <= 10) // our condition
        {
            std::cout << i << ' '; // our statement
            ++i; // our end-expression
        }
    }

    std::cout << '\n';
}
这看起来不那么糟糕，不是吗？请注意，这里需要外部花括号，因为当循环结束时
i
会超出作用域。
For 循环对于新程序员来说可能难以阅读——但是，经验丰富的程序员喜欢它们，因为它们是一种非常紧凑的方式来执行带计数器的循环，所有关于循环变量、循环条件和循环变量修饰符的必要信息都提前呈现。这有助于减少错误。
更多 for 循环示例
这是一个使用 for 循环计算整数指数的函数示例
#include <cstdint> // for fixed-width integers

// returns the value base ^ exponent -- watch out for overflow!
std::int64_t pow(int base, int exponent)
{
    std::int64_t total{ 1 };

    for (int i{ 0 }; i < exponent; ++i)
        total *= base;

    return total;
}
此函数返回 base^exponent（base 的 exponent 次幂）的值。
这是一个直接递增的 for 循环，
i
从
0
循环到（但不包括）
exponent
。
在所有情况下，total 都初始化为
1
。
如果
exponent
为 0，for 循环将执行 0 次。返回
total
（值为
1
），这等效于
base^0
。
如果
exponent
为 1，for 循环将执行 1 次。
total
（值为
1
）乘以
base
，因此现在它的值为
base
，这等效于
base^1
，然后返回。
如果
exponent
为 2，for 循环将执行 2 次。
total
（值为
1
）乘以
base
两次，因此现在它的值为
base * base
，这等效于
base^2
，然后返回。
尽管大多数 for 循环将循环变量递增 1，但我们也可以递减它
#include <iostream>

int main()
{
    for (int i{ 9 }; i >= 0; --i)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
这打印结果
9 8 7 6 5 4 3 2 1 0
或者，我们可以在每次迭代中将循环变量的值更改超过 1
#include <iostream>

int main()
{
    for (int i{ 0 }; i <= 10; i += 2) // increment by 2 each iteration
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
这打印结果
0 2 4 6 8 10
for 循环条件中
operator!=
的危险
在编写涉及值的循环条件时，我们通常可以用许多不同的方式编写条件。以下两个循环执行方式相同
#include <iostream>

int main()
{
    for (int i { 0 }; i < 10; ++i) // uses <
         std::cout << i;

    for (int i { 0 }; i != 10; ++i) // uses !=
         std::cout << i;

     return 0;
}
那么我们应该选择哪一个呢？前者是更好的选择，即使
i
跳过值
10
，它也会终止，而后者不会。以下示例演示了这一点
#include <iostream>

int main()
{
    for (int i { 0 }; i < 10; ++i) // uses <, still terminates
    {
         std::cout << i;
         if (i == 9) ++i; // jump over value 10
    }

    for (int i { 0 }; i != 10; ++i) // uses !=, infinite loop
    {
         std::cout << i;
         if (i == 9) ++i; // jump over value 10
    }

     return 0;
}
最佳实践
在 for 循环条件中进行数值比较时，避免使用
operator!=
。尽可能优先使用
operator<
或
operator<=
。
差一错误
新程序员使用 for 循环（以及其他使用计数器的循环）时遇到的最大问题之一是差一错误。当循环迭代次数过多或过少以产生所需结果时，就会发生
差一错误
。
这是一个例子
#include <iostream>

int main()
{
    // oops, we used operator< instead of operator<=
    for (int i{ 1 }; i < 5; ++i)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
这个程序应该打印
1 2 3 4 5
，但它只打印
1 2 3 4
，因为我们使用了错误的关​​系运算符。
尽管这些错误最常见的原因是使用了错误的关​​系运算符，但有时也可能因为使用了预增量或预减量而不是后增量或后减量，反之亦然。
省略的表达式
可以编写省略任何或所有语句或表达式的
for 循环
。例如，在以下示例中，我们将省略 init-statement 和 end-expression，只留下条件
#include <iostream>

int main()
{
    int i{ 0 };
    for ( ; i < 10; ) // no init-statement or end-expression
    {
        std::cout << i << ' ';
        ++i;
    }

    std::cout << '\n';

    return 0;
}
这个
for 循环
产生结果
0 1 2 3 4 5 6 7 8 9
我们没有让
for 循环
进行初始化和递增，而是手动完成了。在本示例中，我们这样做纯粹是为了学术目的，但在某些情况下，不定义循环变量（因为您已经有一个）或不在 end-expression 中递增它（因为您以其他方式递增它）是理想的。
虽然不常看到，但值得注意的是，以下示例会产生一个无限循环
for (;;)
    statement;
以上示例等同于
while (true)
    statement;
这可能有点出乎意料，因为您可能会期望省略的条件表达式被视为
false
。然而，C++ 标准明确（且不一致地）定义 for 循环中省略的条件表达式应被视为
true
。
我们建议完全避免这种形式的 for 循环，而是使用
while (true)
。
带多个计数器的 for 循环
尽管 for 循环通常只迭代一个变量，但有时 for 循环需要处理多个变量。为了帮助解决这个问题，程序员可以在 init-statement 中定义多个变量，并可以使用逗号运算符在 end-expression 中更改多个变量的值
#include <iostream>

int main()
{
    for (int x{ 0 }, y{ 9 }; x < 10; ++x, --y)
        std::cout << x << ' ' << y << '\n';

    return 0;
}
此循环定义并初始化两个新变量：
x
和
y
。它使
x
在
0
到
9
的范围内迭代，并且在每次迭代后，
x
递增而
y
递减。
这个程序产生的结果是
0 9
1 8
2 7
3 6
4 5
5 4
6 3
7 2
8 1
9 0
这几乎是 C++ 中唯一一个在同一语句中定义多个变量以及使用逗号运算符被认为是可接受实践的地方。
相关内容
我们在课程
6.5 -- 逗号运算符
中介绍了逗号运算符。
最佳实践
在 for 语句中定义多个变量（在 init-statement 中）并使用逗号运算符（在 end-expression 中）是可接受的。
嵌套 for 循环
像其他类型的循环一样，for 循环可以嵌套在其他循环中。在以下示例中，我们将一个 for 循环嵌套在另一个 for 循环中
#include <iostream>

int main()
{
	for (char c{ 'a' }; c <= 'e'; ++c) // outer loop on letters
	{
		std::cout << c; // print our letter first
		
		for (int i{ 0 }; i < 3; ++i) // inner loop on all numbers
			std::cout << i;

		std::cout << '\n';
	}

	return 0;
}
对于外部循环的每次迭代，内部循环完全运行。因此，输出是
a012
b012
c012
d012
e012
以下是有关此处发生情况的更多详细信息。外部循环首先运行，字符
c
初始化为
'a'
。然后评估
c <= 'e'
，结果为
true
，因此循环体执行。由于
c
设置为
'a'
，因此首先打印
a
。接下来内部循环完全执行（打印
0
、
1
和
2
）。然后打印一个换行符。现在外部循环体完成，因此外部循环返回顶部，
c
递增到
'b'
，并重新评估循环条件。由于循环条件仍然为
true
，因此外部循环的下一次迭代开始。这将打印
b012\n
。依此类推。
只在循环内部使用的变量应该在循环内部定义
新程序员常常认为创建变量很昂贵，因此一次性创建变量（然后为其赋值）比多次创建变量（并使用初始化）要好。这导致了看起来像以下变体的循环：
#include <iostream>

int main()
{
    int i {}; // i defined outside loop
    for (i = 0; i < 10; ++i) // i assigned value
    {
        std::cout << i << ' ';        
    }

    // i can still be accessed here

    std::cout << '\n';

    return 0;
}
然而，创建变量没有成本——成本在于初始化，而初始化和赋值之间通常没有成本差异。上面的示例使
i
在循环结束后仍然可用。除非需要在循环之外使用变量，否则在循环之外定义变量可能会带来两个后果
它使我们的程序更复杂，因为我们必须阅读更多代码才能了解变量的使用位置。
它实际上可能会更慢，因为编译器可能无法有效地优化具有更大作用域的变量。
与我们尽可能在最小的合理作用域内定义变量的最佳实践一致，只在循环内部使用的变量应该在循环内部而不是外部定义。
最佳实践
只在循环内部使用的变量应该在循环的作用域内部定义。
总结
For 语句是 C++ 语言中最常用的循环，因为它们将所有关于循环变量、循环条件和循环变量修改的必要信息都放在循环的顶部，这有助于减少错误。尽管其语法对于新程序员来说通常有点令人困惑，但您会经常看到 for 循环，很快就会理解它们！
当您有一个计数器变量时，for 语句表现出色。如果您没有计数器，while 语句可能是更好的选择。
最佳实践
当存在明显的循环变量时，优先选择 for 循环而不是 while 循环。
当没有明显的循环变量时，优先选择 while 循环而不是 for 循环。
小测验时间
问题 #1
编写一个 for 循环，打印从 0 到 20 的所有偶数。
显示答案
for (int i{ 0 }; i <= 20; i += 2)
    std::cout << i << '\n';
问题 #2
编写一个名为
sumTo()
的函数，它接受一个名为 value 的整数参数，并返回从 1 到 value 的所有数字之和。
例如，
sumTo(5)
应该返回 15，即 1 + 2 + 3 + 4 + 5。
提示：使用一个非循环变量来累积和，当您从 1 迭代到输入值时，就像上面的
pow()
示例使用 total 变量在每次迭代中累积返回值一样。
显示答案
int sumTo(int value)
{
    int total{ 0 };
    for (int i{ 1 }; i <= value; ++i)
        total += i;

    return total;
}
问题 #3
以下 for 循环有什么问题？
// Print all numbers from 9 to 0
for (unsigned int i{ 9 }; i >= 0; --i)
    std::cout << i<< ' ';
显示答案
这个 for 循环只要
i >= 0
就执行。换句话说，它运行直到
i
为负数。然而，因为
i
是无符号的，
i
永远不会变为负数。因此，这个循环将永远运行（哈哈）！一般来说，除非必要，最好避免对无符号变量进行循环。
问题 #4
Fizz Buzz
是一款简单的数学游戏，用于教孩子关于可除性。它有时也用作面试问题来评估基本的编程技能。
游戏规则很简单：从 1 开始，向上计数，将任何只能被三整除的数字替换为“fizz”，任何只能被五整除的数字替换为“buzz”，以及任何既能被 3 又能被 5 整除的数字替换为“fizzbuzz”。
在一个名为
fizzbuzz()
的函数中实现这个游戏，该函数接受一个参数来确定计数到哪个数字。使用 for 循环和单个 if-else 链（这意味着您可以使用任意数量的 else-if）。
fizzbuzz(15)
的输出应与以下内容匹配
1
2
fizz
4
buzz
fizz
7
8
fizz
buzz
11
fizz
13
14
fizzbuzz
显示答案
// h/t to reader Waldo for suggesting this quiz
#include <iostream>

void fizzbuzz(int count)
{
	for (int i{ 1 }; i <= count; ++i)
	{
		if (i % 3 == 0 && i % 5 == 0)
		{
			std::cout << "fizzbuzz\n";
		}
		else if (i % 3 == 0)
		{
			std::cout << "fizz\n";
		}
		else if (i % 5 == 0)
		{
			std::cout << "buzz\n";
		}
		else
		{
			std::cout << i << '\n';
		}
	} // end for loop
}

int main()
{
	fizzbuzz(15);

	return 0;
}
问题 #5
修改您在上一测验中编写的 FizzBuzz 程序，添加规则：能被七整除的数字应替换为“pop”。运行程序 150 次迭代。
在此版本中，使用 if/else 链显式涵盖所有可能的单词组合将导致函数过长。优化您的函数，以便只使用 4 个 if 语句：一个用于每个非复合词（“fizz”、“buzz”、“pop”），一个用于打印数字的情况。
显示提示
提示：使用一个布尔变量来跟踪数字是否匹配了其中一个条件。
以下是一些预期输出的片段
4
buzz
fizz
pop
8
19
buzz
fizzpop
22
104
fizzbuzzpop
106
显示答案
// h/t to reader Waldo for suggesting this quiz
#include <iostream>

void fizzbuzz(int count)
{
	for (int i{ 1 }; i <= count; ++i)
	{
		bool printed{ false };
		if (i % 3 == 0)
		{
			std::cout << "fizz";
			printed = true;
		}
		if (i % 5 == 0)
		{
			std::cout << "buzz";
			printed = true;
		}
		if (i % 7 == 0)
		{
			std::cout << "pop";
			printed = true;
		}

		if (!printed)
			std::cout << i;

		std::cout << '\n';
	} // end for loop
}

int main()
{
	fizzbuzz(150);

	return 0;
}
下一课
8.11
break 和 continue
返回目录
上一课
8.9
do while 语句