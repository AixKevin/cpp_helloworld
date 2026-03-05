# 20.3 — 递归

20.3 — 递归
Alex
2007年8月13日，太平洋时间晚上9:30
2024年2月5日
C++ 中的
递归函数
是调用自身的函数。下面是一个写得不好的递归函数的例子：
#include <iostream>

void countDown(int count)
{
    std::cout << "push " << count << '\n';
    countDown(count-1); // countDown() calls itself recursively
}

int main()
{
    countDown(5);

    return 0;
}
当调用 countDown(5) 时，“push 5”被打印，然后 countDown(4) 被调用。countDown(4) 打印“push 4”并调用 countDown(3)。countDown(3) 打印“push 3”并调用 countDown(2)。countDown(n) 调用 countDown(n-1) 的序列无限重复，有效地形成了无限循环的递归等价形式。
在
20.2 — 栈和堆
课程中，您了解到每个函数调用都会导致数据被放置在调用栈上。因为 countDown() 函数从不返回（它只是再次调用 countDown()），所以这些信息从未从栈中弹出！因此，在某个时候，计算机将耗尽栈内存，导致栈溢出，程序将崩溃或终止。在作者的机器上，这个程序在终止前倒数到 -11732！
作者注
尾调用
是发生在函数尾部（末尾）的函数调用。带有递归尾调用的函数很容易被编译器优化为迭代（非递归）函数。这样的函数在上述示例中不会导致系统耗尽栈空间。如果您运行上述程序并它一直运行，很可能就是这种情况。
递归终止条件
递归函数调用通常与普通函数调用一样工作。然而，上面的程序说明了递归函数最重要的区别：您必须包含一个递归终止条件，否则它们将“永远”运行（实际上，直到调用栈内存耗尽）。
递归终止
是一个条件，当满足时，将导致递归函数停止调用自身。
递归终止通常涉及使用 if 语句。这是我们使用终止条件（和一些额外的输出）重新设计的函数：
#include <iostream>

void countDown(int count)
{
    std::cout << "push " << count << '\n';

    if (count > 1) // termination condition
        countDown(count-1);

    std::cout << "pop " << count << '\n';
}

int main()
{
    countDown(5);
    return 0;
}
现在当我们运行程序时，countDown() 将首先输出以下内容：
push 5
push 4
push 3
push 2
push 1
如果此时查看调用栈，您将看到以下内容：
countDown(1)
countDown(2)
countDown(3)
countDown(4)
countDown(5)
main()
由于终止条件，countDown(1) 不会调用 countDown(0)——相反，“if 语句”不会执行，因此它打印“pop 1”然后终止。此时，countDown(1) 从栈中弹出，控制权返回到 countDown(2)。countDown(2) 在调用 countDown(1) 后的点恢复执行，因此它打印“pop 2”然后终止。递归函数调用随后从栈中弹出，直到 countDown 的所有实例都被移除。
因此，这个程序总共输出：
push 5
push 4
push 3
push 2
push 1
pop 1
pop 2
pop 3
pop 4
pop 5
值得注意的是，“push”输出以正向顺序发生，因为它们发生在递归函数调用之前。“pop”输出以反向顺序发生，因为它们发生在递归函数调用之后，因为函数正在从栈中弹出（这与它们被压入的顺序相反）。
一个更有用的例子
现在我们已经讨论了递归函数调用的基本机制，让我们来看另一个稍微更典型的递归函数：
// return the sum of all the integers between 1 (inclusive) and sumto (inclusive)
// returns 0 for negative numbers
int sumTo(int sumto)
{
    if (sumto <= 0)
        return 0; // base case (termination condition) when user passed in an unexpected argument (0 or negative)
    if (sumto == 1)
        return 1; // normal base case (termination condition)

    return sumTo(sumto - 1) + sumto; // recursive function call
}
递归程序通常很难通过查看来理解。通常，查看当我们使用特定值调用递归函数时会发生什么是有益的。所以让我们看看当我们使用参数 sumto = 5 调用此函数时会发生什么。
sumTo(5) called, 5 <= 1 is false, so we return sumTo(4) + 5.
sumTo(4) called, 4 <= 1 is false, so we return sumTo(3) + 4.
sumTo(3) called, 3 <= 1 is false, so we return sumTo(2) + 3.
sumTo(2) called, 2 <= 1 is false, so we return sumTo(1) + 2.
sumTo(1) called, 1 <= 1 is true, so we return 1.  This is the termination condition.
现在我们展开调用栈（当每个函数返回时将其从调用栈中弹出）：
sumTo(1) returns 1.
sumTo(2) returns sumTo(1) + 2, which is 1 + 2 = 3.
sumTo(3) returns sumTo(2) + 3, which is 3 + 3 = 6.
sumTo(4) returns sumTo(3) + 4, which is 6 + 4 = 10.
sumTo(5) returns sumTo(4) + 5, which is 10 + 5 = 15.
此时，更容易看出我们正在将 1 到传入值之间的数字相加（包括两者）。
因为递归函数很难通过查看来理解，所以良好的注释尤其重要。
请注意，在上面的代码中，我们使用值
sumto - 1
而不是
--sumto
进行递归。我们这样做是因为
operator--
有副作用，并且在给定表达式中多次使用具有副作用的变量将导致未定义行为。使用
sumto - 1
避免了副作用，使得 sumto 可以安全地在表达式中多次使用。
递归算法
递归函数通常通过首先（递归地）找到问题子集的解决方案，然后修改该子解决方案以获得解决方案来解决问题。在上述算法中，sumTo(value) 首先解决 sumTo(value-1)，然后添加变量 value 的值以找到 sumTo(value) 的解决方案。
在许多递归算法中，某些输入会产生琐碎的输出。例如，sumTo(1) 有琐碎的输出 1（您可以在脑海中计算），并且不会受益于进一步的递归。算法对这些输入直接产生输出的情况称为
基本情况
。基本情况作为算法的终止条件。基本情况通常可以通过考虑输入为 0、1、“”、'' 或 null 时的输出来识别。
斐波那契数
最著名的数学递归算法之一是斐波那契数列。斐波那契数列出现在自然界的许多地方，例如树木的分枝、贝壳的螺旋、菠萝的果肉、展开的蕨类植物叶片以及松果的排列。
这是一张斐波那契螺旋图：
每个斐波那契数是该数字所在正方形的边长。
斐波那契数在数学上定义为：
F(n) =
0 如果 n = 0
1 如果 n = 1
f(n-1) + f(n-2) 如果 n > 1
因此，编写一个（效率不高）的递归函数来计算第 n 个斐波那契数相当简单：
#include <iostream>

int fibonacci(int count)
{
    if (count == 0)
        return 0; // base case (termination condition)
    if (count == 1)
        return 1; // base case (termination condition)
    return fibonacci(count-1) + fibonacci(count-2);
}

// And a main program to display the first 13 Fibonacci numbers
int main()
{
    for (int count { 0 }; count < 13; ++count)
        std::cout << fibonacci(count) << ' ';

    return 0;
}
运行程序会产生以下结果：
0 1 1 2 3 5 8 13 21 34 55 89 144
您会注意到这些数字与斐波那契螺旋图中出现的数字完全相同。
记忆化算法
上述递归斐波那契算法效率不高，部分原因是非基本情况的每次斐波那契调用都会导致两次额外的斐波那契调用。这会产生指数级的函数调用次数（实际上，上述示例调用 fibonacci() 1205 次！）。有一些技术可以用来减少必要的调用次数。一种称为
记忆化
的技术会缓存昂贵函数调用的结果，以便在再次出现相同输入时可以直接返回结果。
这是递归斐波那契算法的记忆化版本：
#include <iostream>
#include <vector>

// h/t to potterman28wxcv for a variant of this code
// count is now a std::size_t to make indexing the std::vector easier
int fibonacci(std::size_t count)
{
	// We'll use a static std::vector to cache calculated results
	static std::vector results{ 0, 1 };

	// If we've already seen this count, then use the cache'd result
	if (count < std::size(results))
		return results[count];

	// Otherwise calculate the new result and add it
	results.push_back(fibonacci(count - 1) + fibonacci(count - 2));
	return results[count];   
}

// And a main program to display the first 13 Fibonacci numbers
int main()
{
	for (int count { 0 }; count < 13; ++count)
		std::cout << fibonacci(static_cast<std::size_t>(count)) << ' ';

	return 0;
}
这个记忆化版本进行了 35 次函数调用，比原始算法的 1205 次好得多。
递归与迭代
关于递归函数经常被问的一个问题是：“如果可以使用迭代（使用
for 循环
或
while 循环
）完成许多相同的任务，为什么要使用递归函数？”事实证明，您总是可以迭代地解决递归问题——然而，对于非平凡的问题，递归版本通常更容易编写（和阅读）。例如，虽然可以迭代地编写斐波那契函数，但它要困难一些！（试试看！）
迭代函数（使用 for 循环或 while 循环的函数）几乎总是比其递归对应项更高效。这是因为每次调用函数时，在压入和弹出栈帧时都会产生一定的开销。迭代函数避免了这种开销。
这并不是说迭代函数总是更好的选择。有时，函数的递归实现非常清晰且易于理解，以至于为了可维护性的好处，承担一点额外的开销是值得的，特别是如果算法不需要递归太多次才能找到解决方案。
通常，当以下大部分情况属实时，递归是一个不错的选择：
递归代码实现起来简单得多。
递归深度可以限制（例如，无法提供导致它递归下降 100,000 级的输入）。
算法的迭代版本需要管理数据栈。
这不是代码的性能关键部分。
但是，如果递归算法实现起来更简单，那么开始时使用递归，然后稍后优化为迭代算法可能是有意义的。
最佳实践
通常优先选择迭代而不是递归，除非递归确实有意义。
小测验时间
整数 N 的阶乘（写作 N!）定义为 1 到 N 之间所有数字的乘积（0! = 1）。编写一个名为 factorial 的递归函数，返回输入的阶乘。用前 7 个阶乘测试它。
提示：记住 (x * y) = (y * x)，所以 1 到 N 之间所有数字的乘积与 N 到 1 之间所有数字的乘积相同。
显示答案
#include <iostream>

int factorial(int n)
{
	if (n <= 0)
		return 1;

	return factorial(n - 1) * n;
}

int main()
{
	for (int count { 0 }; count < 7; ++count)
		std::cout << factorial(count) << '\n';
}
编写一个递归函数，接受一个整数作为输入，并返回该整数中每个单独数字的总和（例如，357 = 3 + 5 + 7 = 15）。打印输入 93427 的答案（即 25）。假设输入值为正数。
显示答案
#include <iostream>

int sumDigits(int x)
{
	if (x < 10)
		return x;

	return sumDigits(x / 10) + x % 10;
}

int main()
{
	std::cout << sumDigits(93427);
}
3a) 这个稍微有点复杂。编写一个程序，要求用户输入一个正整数，然后使用递归函数打印出该数字的二进制表示。使用
O.4 — 在二进制和十进制表示之间转换整数
课程中的方法 1。
提示：使用方法 1，我们希望以相反的顺序打印位。这意味着您的打印语句应该在递归调用
之后
。
显示答案
#include <iostream>

// h/t to reader Gapo for this solution
void printBinary(int x)
{
        // Termination case
	if (x == 0)
		return;
	
	// Recurse to the next bit
	printBinary(x / 2);

	// Print out the remainders (in reverse order)
	std::cout << x % 2;
}

int main()
{
	int x;
	std::cout << "Enter a positive integer: ";
	std::cin >> x;

	printBinary(x);
}
3b) 额外加分：更新 3a 中的代码，以处理用户可能输入 0 或负数的情况。
这是一个示例输出（假设 32 位整数）：
Enter an integer: -15
11111111111111111111111111110001
提示：您的 printBinary() 函数实际上不需要处理负数。如果您传递给它一个与负数具有相同二进制表示的正值，它将产生正确的输出。
显示提示
提示：有符号和无符号之间的转换不会改变二进制表示，只改变值的解释方式。例如，有符号整数
-15
的二进制表示为
11111111111111111111111111110001
，与无符号整数
4294967281
相同。
显示提示
提示：有符号值可以是正数或负数，但无符号值总是正数……
显示答案
// h/t to reader Donlod for this solution
#include <iostream>

void printBinary(unsigned int n)
{
	if (n > 1) // we only recurse if n > 1, so this is our termination case for n == 0
	{
		printBinary(n / 2);
	}

	std::cout << n % 2;
}

int main()
{
	int x{};
	std::cout << "Enter an integer: ";
	std::cin >> x;

	printBinary(static_cast<unsigned int>(x));
}
如提示所示，有符号和无符号之间的转换不会改变二进制表示，只改变值的解释方式。因此，如果我们将用户的输入捕获为有符号 int，然后将其转换为无符号 int，我们将得到一个始终为正但具有与用户输入的有符号值相同二进制表示的值。这样，我们的函数只需处理正数。
下一课
20.4
命令行参数
返回目录
上一课
20.2
栈和堆