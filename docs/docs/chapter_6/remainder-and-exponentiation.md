# 6.3 — 余数和幂运算

6.3 — 余数和幂运算
Alex
2019 年 8 月 17 日，上午 11:57 PDT
2024 年 12 月 30 日
余数运算符 (
operator%
)
余数运算符
（通常也称为
模运算符
或
模数运算符
）是一种运算符，它在执行整数除法后返回余数。例如，7 / 4 = 1 余 3。因此，7 % 4 = 3。再例如，25 / 7 = 3 余 4，因此 25 % 7 = 4。余数运算符只适用于整数操作数。
这对于测试一个数字是否能被另一个数字整除（意味着除法后没有余数）最有用：如果
x % y
的结果为 0，那么我们知道
x
能被
y
整除。
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";
	int x{};
	std::cin >> x;

	std::cout << "Enter another integer: ";
	int y{};
	std::cin >> y;

	std::cout << "The remainder is: " << x % y << '\n';

	if ((x % y) == 0)
		std::cout << x << " is evenly divisible by " << y << '\n';
	else
		std::cout << x << " is not evenly divisible by " << y << '\n';

	return 0;
}
以下是这个程序的几次运行
Enter an integer: 6
Enter another integer: 3
The remainder is: 0
6 is evenly divisible by 3
Enter an integer: 6
Enter another integer: 4
The remainder is: 2
6 is not evenly divisible by 4
现在我们尝试一个第二个数字大于第一个数字的例子
Enter an integer: 2
Enter another integer: 4
The remainder is: 2
2 is not evenly divisible by 4
余数 2 可能一开始有点不明显，但这很简单：2 / 4 是 0（使用整数除法）余 2。当第二个数字大于第一个数字时，第二个数字将除第一个数字 0 次，因此第一个数字将是余数。
负数的余数
余数运算符也可以与负操作数一起使用。
x % y
总是返回带有
x
符号的结果。
运行上面的程序
Enter an integer: -6
Enter another integer: 4
The remainder is: -2
-6 is not evenly divisible by 4
Enter an integer: 6
Enter another integer: -4
The remainder is: 2
6 is not evenly divisible by -4
在这两种情况下，您都可以看到余数取第一个操作数的符号。
命名法
C++ 标准实际上没有给
operator%
命名。然而，C++20 标准确实说，“二元 % 运算符产生第一个表达式除以第二个表达式的余数”。
尽管
operator%
通常被称为“模数”或“模”运算符，但这可能会令人困惑，因为数学中的模数通常以一种方式定义，当一个（且只有一个）操作数为负数时，它会产生与 C++ 中
operator%
产生的结果不同的结果。
例如，在数学中
-21 模 4 = 3
-21 余 4 = -1
因此，我们认为“余数”是
operator%
比“模数”更准确的名称。
在第一个操作数可能为负数的情况下，必须注意余数也可能为负数。例如，您可能会想编写一个函数来判断一个数字是否为奇数，如下所示
bool isOdd(int x)
{
    return (x % 2) == 1; // fails when x is -5
}
然而，当 x 是负奇数时，例如
-5
，这将失败，因为
-5 % 2
是 -1，而 -1 != 1。
因此，如果要比较余数运算的结果，最好与 0 进行比较，这样就没有正/负数问题
bool isOdd(int x)
{
    return (x % 2) != 0; // could also write return (x % 2)
}
最佳实践
如果可能，最好将余数运算符 (
operator%
) 的结果与 0 进行比较。
幂运算符在哪里？
您会注意到
^
运算符（在数学中通常用于表示幂运算）在 C++ 中是**按位异或**运算（在课程
O.3 -- 使用按位运算符和位掩码进行位操作
中介绍）。C++ 不包含幂运算符。
要在 C++ 中进行幂运算，请 #include <cmath> 头文件，并使用 pow() 函数
#include <cmath>

double x{ std::pow(3.0, 4.0) }; // 3 to the 4th power
请注意，函数 pow() 的参数（和返回值）的类型为 double。由于浮点数中的舍入误差，pow() 的结果可能不精确（即使您传递的是整数或整数）。
如果您想进行整数幂运算，最好使用自己的函数来完成。以下函数实现了整数幂运算（为了效率，使用了不直观的“平方求幂”算法）
#include <cassert> // for assert
#include <cstdint> // for std::int64_t
#include <iostream>

// note: exp must be non-negative
// note: does not perform range/overflow checking, use with caution
constexpr std::int64_t powint(std::int64_t base, int exp)
{
	assert(exp >= 0 && "powint: exp parameter has negative value");

	// Handle 0 case
	if (base == 0)
		return (exp == 0) ? 1 : 0;

	std::int64_t result{ 1 };
	while (exp > 0)
	{
		if (exp & 1)  // if exp is odd
			result *= base;
		exp /= 2;
		base *= base;
	}

	return result;
}

int main()
{
	std::cout << powint(7, 12) << '\n'; // 7 to the 12th power

	return 0;
}
产生
13841287201
如果您不理解此函数的工作原理，请不要担心——您不需要理解它即可调用它。
相关内容
我们在课程
9.6 -- 断言和静态断言
中介绍了断言，并在课程
F.1 -- Constexpr 函数
中介绍了 constexpr 函数。
致进阶读者
constexpr
说明符允许函数在用作常量表达式时在编译时进行求值；否则，它就像一个常规函数，在运行时进行求值。
警告
在绝大多数情况下，整数幂运算会溢出整数类型。这可能就是标准库中最初没有包含此类函数的原因。
这是上面幂运算函数的一个更安全版本，它会检查溢出
#include <cassert> // for assert
#include <cstdint> // for std::int64_t
#include <iostream>
#include <limits> // for std::numeric_limits

// A safer (but slower) version of powint() that checks for overflow
// note: exp must be non-negative
// Returns std::numeric_limits<std::int64_t>::max() if overflow occurs
constexpr std::int64_t powint_safe(std::int64_t base, int exp)
{
    assert(exp >= 0 && "powint_safe: exp parameter has negative value");

    // Handle 0 case
    if (base == 0)
        return (exp == 0) ? 1 : 0;

    std::int64_t result { 1 };

    // To make the range checks easier, we'll ensure base is positive
    // We'll flip the result at the end if needed
    bool negativeResult{ false };

    if (base < 0)
    {
        base = -base;
        negativeResult = (exp & 1);
    }

    while (exp > 0)
    {
        if (exp & 1) // if exp is odd
        {
            // Check if result will overflow when multiplied by base
            if (result > std::numeric_limits<std::int64_t>::max() / base)
            {
                std::cerr << "powint_safe(): result overflowed\n";
                return std::numeric_limits<std::int64_t>::max();
            }

            result *= base;
        }

        exp /= 2;

        // If we're done, get out here
        if (exp <= 0)
            break;

        // The following only needs to execute if we're going to iterate again

        // Check if base will overflow when multiplied by base
        if (base > std::numeric_limits<std::int64_t>::max() / base)
        {
            std::cerr << "powint_safe(): base overflowed\n";
            return std::numeric_limits<std::int64_t>::max();
        }

        base *= base;
    }

    if (negativeResult)
        return -result;

    return result;
}

int main()
{
	std::cout << powint_safe(7, 12) << '\n'; // 7 to the 12th power
	std::cout << powint_safe(70, 12) << '\n'; // 70 to the 12th power (will return the max 64-bit int value)

	return 0;
}
小测验时间
问题 #1
以下表达式求值为多少？
6 + 5 * 4 % 3
显示答案
因为 * 和 % 的优先级高于 +，所以 + 将最后求值。我们可以将表达式改写为 6 + (5 * 4 % 3)。运算符 * 和 % 具有相同的优先级，因此我们必须查看结合性来解析它们。运算符 * 和 % 的结合性是左到右，所以我们首先解析左运算符。我们可以将表达式改写为：6 + ((5 * 4) % 3)。
6 + ((5 * 4) % 3) = 6 + (20 % 3) = 6 + 2 = 8
问题 #2
编写一个程序，要求用户输入一个整数，并告诉用户该数字是偶数还是奇数。编写一个名为
isEven()
的 constexpr 函数，如果传递给它的整数是偶数，则返回 true，否则返回 false。使用余数运算符测试整数参数是否为偶数。确保
isEven()
适用于正数和负数。
显示提示
提示：您可能需要使用 if 语句和比较运算符 (==) 来完成此程序。如果您需要复习如何操作，请参阅课程
4.9 -- 布尔值
。
您的程序应该匹配以下输出
Enter an integer: 5
5 is odd
显示答案
#include <iostream>

constexpr bool isEven(int x)
{
    // if x % 2 == 0, 2 divides evenly into our number, which means it must be an even number
    return (x % 2) == 0;
}

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    if (isEven(x))
        std::cout << x << " is even\n";
    else
        std::cout << x << " is odd\n";

    return 0;
}
注意：您可能曾想将函数 isEven() 写成这样
constexpr bool isEven(int x)
{
    if ((x % 2) == 0)
        return true;
    else
        return false;
}
虽然这可行，但它比需要的更复杂。让我们看看如何简化它。首先，让我们取出 if 语句的条件并将其赋值给一个单独的布尔变量
constexpr bool isEven(int x)
{
    bool isEven = (x % 2) == 0;
    if (isEven) // isEven is true
        return true;
    else // isEven is false
        return false;
}
现在，请注意上面的 if 语句本质上是说“如果 isEven 为真，则返回 true，否则如果 isEven 为假，则返回 false”。如果是这种情况，我们可以直接返回 isEven
constexpr bool isEven(int x)
{
    bool isEven = (x % 2) == 0;
    return isEven;
}
在这种情况下，由于我们只使用变量 isEven 一次，我们不妨消除该变量
constexpr bool isEven(int x)
{
    return (x % 2) == 0;
}
下一课
6.4
递增/递减运算符和副作用
返回目录
上一课
6.2
算术运算符