# 8.8 — 循环和 while 语句简介

8.8 — 循环和 while 语句简介
Alex
2007 年 6 月 22 日下午 1:32 PDT
2025 年 2 月 5 日
循环简介
现在真正的乐趣开始了——在接下来的几节课中，我们将学习循环。循环是控制流结构，允许一段代码重复执行，直到满足某个条件。循环为您的编程工具包增添了极大的灵活性，让您可以完成许多原本难以完成的事情。
例如，假设您想打印从 1 到 10 的所有数字。如果没有循环，您可以尝试这样做：
#include <iostream>

int main()
{
    std::cout << "1 2 3 4 5 6 7 8 9 10";
    std::cout << " done!\n";
    return 0;
}
虽然这可行，但当您想打印更多数字时，它会变得越来越不可行：如果您想打印从 1 到 1000 的所有数字怎么办？那将需要大量的输入！但是这样的程序可以通过这种方式编写，因为我们知道在编译时要打印多少个数字。
现在，让我们稍微改变一下参数。如果我们要让用户输入一个数字，然后打印从 1 到用户输入的数字之间的所有数字怎么办？用户将输入的数字在编译时是未知的。那么我们该如何解决这个问题呢？
While 语句
while 语句
（也称为
while 循环
）是 C++ 提供的三种循环类型中最简单的一种，它的定义与 if 语句非常相似
while (condition)
    statement;
while 语句
使用
while
关键字声明。当 while 语句执行时，表达式
条件
被求值。如果条件求值为
true
，则相关的
语句
执行。
然而，与 if 语句不同，一旦语句执行完毕，控制权将返回到 while 语句的顶部，并重复该过程。这意味着只要条件持续求值为
true
，while 语句就会一直循环。
让我们看一个简单的 while 循环，它打印从 1 到 10 的所有数字
#include <iostream>

int main()
{
    int count{ 1 };
    while (count <= 10)
    {
        std::cout << count << ' ';
        ++count;
    }

    std::cout << "done!\n";

    return 0;
}
这输出
1 2 3 4 5 6 7 8 9 10 done!
让我们仔细看看这个程序在做什么。
首先，我们定义一个名为
count
的变量并将其设置为
1
。条件
count <= 10
为
true
，因此语句执行。在这种情况下，我们的语句是一个块，因此块中的所有语句都将执行。块中的第一条语句打印
1
和一个空格，第二条语句将
count
递增到 2。现在控制权返回到 while 语句的顶部，并且条件再次求值。
2 <= 10
求值为
true
，因此代码块再次执行。循环将重复执行，直到
count
为
11
，此时
11 <= 10
将求值为
false
，并且与循环关联的语句将被跳过。此时，循环完成。
虽然这个程序比直接输入 1 到 10 之间的所有数字的代码量多一点，但请考虑修改程序以打印 1 到 1000 之间的所有数字是多么容易：您只需要将
count <= 10
更改为
count <= 1000
。
While 语句最初求值为 false
请注意，如果条件最初求值为
false
，则关联的语句根本不会执行。考虑以下程序
#include <iostream>

int main()
{
    int count{ 15 };
    while (count <= 10)
    {
        std::cout << count << ' ';
        ++count;
    }

    std::cout << "done!\n";

    return 0;
}
条件
15 <= 10
求值为
false
，因此关联的语句被跳过。程序继续执行，唯一打印的是
done!
。
无限循环
另一方面，如果表达式总是求值为
true
，while 循环将永远执行。这称为
无限循环
。以下是一个无限循环的示例
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
因为在这个程序中
count
从未递增，所以
count <= 10
将永远为真。因此，循环永远不会终止，程序将永远打印
1 1 1 1 1
...。
有意无限循环
我们可以这样声明一个有意无限循环
while (true)
{
  // this loop will execute forever
}
退出无限循环的唯一方法是通过 return 语句、break 语句、exit 语句、goto 语句、抛出异常或用户终止程序。
这里有一个演示此功能的简单示例
#include <iostream>

int main()
{

    while (true) // infinite loop
    {
        std::cout << "Loop again (y/n)? ";
        char c{};
        std::cin >> c;

        if (c == 'n')
            return 0;
    }

    return 0;
}
此程序将持续循环，直到用户输入
n
作为输入，此时 if 语句将求值为
true
，并且关联的
return 0;
将导致函数
main()
退出，从而终止程序。
在持续运行并服务网络请求的 Web 服务器应用程序中，这种类型的循环很常见。
最佳实践
对于有意无限循环，请优先使用
while(true)
。
无意无限循环
在 while 循环条件后无意地放置分号是导致程序挂起的好方法。
这是一个先前的示例，展示了如果犯了这种简单错误会发生什么
#include <iostream>

int main()
{
    int count{ 1 };
    while (count <= 10); // note the semicolon here
    {
        std::cout << count << ' ';
        ++count;
    }

    std::cout << "done!\n";

    return 0;
}
程序执行起来就像我们写了这样
#include <iostream>

int main()
{
    int count{ 1 };
    while (count <= 10) // this is an infinite loop
        ;               // whose body is a null statement

    { // this is no longer associated with the while loop
        std::cout << count << ' ';
        ++count;
    }

    std::cout << "done!\n";

    return 0;
}
因为循环条件求值为
true
，所以循环体执行。但是循环体是一个空语句，它什么也不做。然后循环条件再次求值。由于
count
从未递增，因此条件永远不能求值为
false
，因此循环将永远运行而什么也不做。我们的程序将看起来像被挂起一样。
与 if 语句不同，在 if 语句中条件后的分号始终是错误，而 while 语句偶尔会故意这样做。例如，如果我们想持续调用一个函数直到它返回
false
，我们可以简洁地写成如下：
while (keepRunning()); // will keep calling this function until it returns false
当然，如果函数从不返回
false
，您将得到一个无限循环。
警告
请注意不要在 while 语句的条件后放置分号，因为它会导致无限循环，除非条件以某种方式求值为
false
。
循环变量和命名
循环变量
是用于控制循环执行次数的变量。例如，给定
while (count <= 10)
，
count
是一个循环变量。虽然大多数循环变量的类型为
int
，但您偶尔也会看到其他类型（例如
char
）。
循环变量通常使用简单的名称，最常见的是
i
、
j
和
k
。
题外话…
使用
i
、
j
和
k
作为循环变量名称的出现是因为它们是 Fortran 编程语言中整数变量的前三个最短名称。这个约定一直沿用至今。
然而，如果您想知道程序中某个循环变量的使用位置，并且您使用搜索功能搜索
i
、
j
或
k
，搜索功能将返回程序中一半的行！因此，一些开发人员更喜欢使用
iii
、
jjj
或
kkk
等循环变量名称。由于这些名称更具唯一性，这使得搜索循环变量变得更容易，并有助于它们作为循环变量脱颖而出。更好的方法是使用“真实”的变量名，例如
count
、
index
，或者一个更能详细说明您正在计数的名称（例如
userCount
）。
最常见的循环变量类型称为
计数器
，它是一个循环变量，用于计算循环执行的次数。在上面的示例中，变量
count
是一个计数器。
整数循环变量应为有符号类型
整数循环变量几乎总是应该是有符号的，因为无符号整数可能会导致意想不到的问题。考虑以下代码
#include <iostream>

int main()
{
    unsigned int count{ 10 }; // note: unsigned

    // count from 10 down to 0
    while (count >= 0)
    {
        if (count == 0)
        {
            std::cout << "blastoff!";
        }
        else
        {
            std::cout << count << ' ';
        }
        --count;
    }

    std::cout << '\n';

    return 0;
}
看上面的例子，看看你能否找出错误。如果你以前没见过，这不是很明显。
事实证明，这个程序是一个无限循环。它首先按预期打印
10 9 8 7 6 5 4 3 2 1 blastoff!
，然后循环变量
count
溢出，并开始从
4294967295
倒数（假设 32 位整数）。为什么？因为循环条件
count >= 0
永远不会为假！当
count
为
0
时，
0 >= 0
为真。然后执行
--count
，并且
count
循环回到
4294967295
。由于
4294967295 >= 0
为
true
，程序继续。由于
count
是无符号的，它永远不能为负数，并且因为它永远不能为负数，循环将不会终止。
最佳实践
整数循环变量通常应为有符号整数类型。
每 N 次迭代执行一次操作
循环每次执行都称为一次
迭代
。
通常，我们希望每第 2 次、第 3 次或第 4 次迭代执行一些操作，例如打印换行符。这可以通过在计数器上使用取余运算符轻松完成
#include <iostream>

// Iterate through every number between 1 and 50
int main()
{
    int count{ 1 };
    while (count <= 50)
    {
        // print the number (pad numbers under 10 with a leading 0 for formatting purposes)
        if (count < 10)
        {
            std::cout << '0';
        }

        std::cout << count << ' ';

        // if the loop variable is divisible by 10, print a newline
        if (count % 10 == 0)
        {
            std::cout << '\n';
        }
            
        // increment the loop counter
        ++count;
    }

    return 0;
}
这个程序产生的结果是
01 02 03 04 05 06 07 08 09 10
11 12 13 14 15 16 17 18 19 20
21 22 23 24 25 26 27 28 29 30
31 32 33 34 35 36 37 38 39 40
41 42 43 44 45 46 47 48 49 50
嵌套循环
也可以将循环嵌套在其他循环中。嵌套循环对新程序员来说往往有点令人困惑，所以让我们从一个稍微简单的例子开始
#include <iostream>

void printUpto(int outer)
{
    // loop between 1 and outer
    // note: inner will be created and destroyed at the end of the block
    int inner{ 1 };
    while (inner <= outer)
    {
        std::cout << inner << ' ';
        ++inner;
    }
} // inner destroyed here

int main()
{
    // outer loops between 1 and 5
    int outer{ 1 };
    while (outer <= 5)
    {
        // For each iteration of the outer loop, the code in the body of the loop executes once

        // This function prints numbers between 1 and outer
        printUpto(outer);

        // print a newline at the end of each row
        std::cout << '\n';
        ++outer;
    }

    return 0;
}
在此示例中，我们有一个外部循环，其计数器名为
outer
，从 1 数到 5。对于循环的每次迭代，循环体使用外部循环变量作为参数调用
printUpto()
，打印换行符，并递增
outer
。
printUpto()
函数也有一个循环，它打印从 1 到传入值之间的所有数字。
因此，当
outer
为 1 时，循环体调用
printUpto(1)
，它打印数字
1
。然后循环体打印一个换行符并递增
outer
。现在
outer
是 2。循环体再次执行，调用
printUpto(2)
，它打印
1 2
。循环体再次打印一个换行符并递增
outer
。随后的迭代调用
printUpto(3)
、
printUpto(4)
和
printUpto(5)
。
因此，此程序打印
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
请注意，这是一种嵌套循环形式——在外部循环的主体中，我们正在调用一个自身包含循环的函数。换句话说，对于外部循环的每次迭代，函数中的循环都会执行。
现在让我们来看一个更令人困惑的例子
#include <iostream>

int main()
{
    // outer loops between 1 and 5
    int outer{ 1 };
    while (outer <= 5)
    {
        // For each iteration of the outer loop, the code in the body of the loop executes once

        // inner loops between 1 and outer
        // note: inner will be created and destroyed at the end of the block
        int inner{ 1 };
        while (inner <= outer)
        {
            std::cout << inner << ' ';
            ++inner;
        }

        // print a newline at the end of each row
        std::cout << '\n';
        ++outer;
    } // inner destroyed here

    return 0;
}
这个程序有完全相同的输出
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
由于我们有一个 while 循环直接嵌套在另一个 while 循环中，这看起来有点令人困惑。然而，我们所做的只是将原来在
printUpto()
函数内部的代码直接放在外部循环体内部。
让我们更详细地研究一下这是如何工作的。
首先，我们有一个外部循环（带有循环变量
outer
），它将循环 5 次（
outer
依次取值
1
、
2
、
3
、
4
和
5
）。
在外部循环的第一次迭代中，
outer
的值为
1
，然后外部循环体执行。在外部循环体内部，我们有另一个带有循环变量
inner
的循环。内部循环从
1
迭代到
outer
（其值为
1
），因此这个内部循环将执行一次，打印值
1
。然后我们打印一个换行符，并将
outer
递增到
2
。
在外部循环的第二次迭代中，
outer
的值为
2
，然后外部循环体执行。在外部循环体内部，
inner
再次从
1
迭代到
outer
（现在值为
2
），因此这个内部循环将执行两次，打印值
1
和
2
。然后我们打印一个换行符，并将
outer
递增到
3
。
此过程继续进行，内部循环在后续通过中打印
1 2 3
、
1 2 3 4
和
1 2 3 4 5
。最终，
outer
递增到
6
，并且由于外部循环条件（
outer <= 5
）为假，外部循环结束。然后程序结束。
如果您仍然觉得这令人困惑，那么使用调试器逐行调试此程序并观察
inner
和
outer
的值是更好地理解正在发生的事情的好方法。
小测验时间
问题 #1
在上面的程序中，变量
inner
为什么声明在 while 块内部，而不是紧随
outer
声明之后？
显示答案
变量 inner 被声明在 while 块内部，这样它每次外部循环执行时都会被重新创建（并重新初始化为 1）。如果变量 inner 在外部 while 循环之前声明，它的值将永远不会重置为 1，或者我们必须通过赋值语句来完成。此外，因为变量 inner 只在外部 while 循环块内部使用，所以将其声明在那里是合理的。记住，在尽可能小的作用域内声明变量！
问题 #2
编写一个程序，打印出从 a 到 z 的字母及其 ASCII 码。使用
char
类型的循环变量。
显示提示
提示：要将字符打印为整数，您必须使用
static_cast
。
显示答案
#include <iostream>

int main()
{
    char myChar{ 'a' };
    while (myChar <= 'z')
    {
        std::cout << myChar << ' ' << static_cast<int>(myChar) << '\n';
        ++myChar;
    }

    return 0;
}
问题 #3
反转嵌套循环示例，使其打印以下内容：
5 4 3 2 1
4 3 2 1
3 2 1
2 1
1
显示答案
#include <iostream>

// Loop between 5 and 1
int main()
{
	int outer{ 5 };
	while (outer >= 1)
	{
		// loop between outer and 1
		int inner{ outer };
		while (inner >= 1)
        {
			std::cout << inner-- << ' ';
        }

		// print a newline at the end of each row
		std::cout << '\n';
		--outer;
	}

	return 0;
}
问题 #4
现在让数字这样打印：
1
      2 1
    3 2 1
  4 3 2 1
5 4 3 2 1
提示：先弄清楚如何使其像这样打印
X X X X 1
X X X 2 1
X X 3 2 1
X 4 3 2 1
5 4 3 2 1
显示答案
// Thanks to Shiva for this solution
#include <iostream>

int main()
{
	// There are 5 rows, we can loop from 1 to 5
	int outer{ 1 };

	while (outer <= 5)
	{
		// Row elements appear in descending order, so start from 5 and loop through to 1
		int inner{ 5 };

		while (inner >= 1)
		{
			// The first number in any row is the same as the row number
			// So number should be printed only if it is <= the row number, space otherwise
			if (inner <= outer)
				std::cout << inner << ' '; // print the number and a single space
			else
				std::cout << "  "; // don't print a number, but print two spaces

			--inner;
		}

		// A row has been printed, move to the next row
		std::cout << '\n';

		++outer;
	}

	return 0;
}
下一课
8.9
Do while 语句
返回目录
上一课
8.7
Goto 语句