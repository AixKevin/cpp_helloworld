# 20.5 — 省略号（以及为何要避免它们）

20.5 — 省略号（以及为何要避免它们）
Alex
2008 年 2 月 22 日下午 4:08 (太平洋标准时间)
2023 年 9 月 11 日
到目前为止，我们看到的所有函数都必须提前知道函数将接受的参数数量（即使它们有默认值）。然而，在某些情况下，能够向函数传递可变数量的参数会很有用。C++ 提供了一种特殊的说明符，称为省略号（又名“…”），它允许我们精确地做到这一点。
由于省略号很少使用，可能很危险，并且我们建议避免使用它们，因此本节可以被视为可选阅读。
使用省略号的函数采用以下形式
return_type function_name(argument_list, ...)
argument_list
是一个或多个正常的函数参数。请注意，使用省略号的函数必须至少有一个非省略号参数。传递给函数的任何参数都必须首先与 argument_list 参数匹配。
省略号（用连续的三个点表示）必须始终是函数中的最后一个参数。省略号捕获任何额外的参数（如果存在）。虽然不太准确，但将省略号概念性地视为一个数组，用于保存 argument_list 中之外的任何额外参数是很有用的。
一个省略号示例
了解省略号的最佳方法是举例说明。因此，让我们编写一个使用省略号的简单程序。假设我们要编写一个计算一堆整数平均值的函数。我们会这样做：
#include <iostream>
#include <cstdarg> // needed to use ellipsis

// The ellipsis must be the last parameter
// count is how many additional arguments we're passing
double findAverage(int count, ...)
{
    int sum{ 0 };

    // We access the ellipsis through a va_list, so let's declare one
    std::va_list list;

    // We initialize the va_list using va_start.  The first argument is
    // the list to initialize.  The second argument is the last non-ellipsis
    // parameter.
    va_start(list, count);

    // Loop through all the ellipsis values
    for (int arg{ 0 }; arg < count; ++arg)
    {
         // We use va_arg to get values out of our ellipsis
         // The first argument is the va_list we're using
         // The second argument is the type of the value
         sum += va_arg(list, int);
    }

    // Cleanup the va_list when we're done.
    va_end(list);

    return static_cast<double>(sum) / count;
}

int main()
{
    std::cout << findAverage(5, 1, 2, 3, 4, 5) << '\n';
    std::cout << findAverage(6, 1, 2, 3, 4, 5, 6) << '\n';

    return 0;
}
此代码打印
3
3.5
如您所见，此函数接受可变数量的参数！现在，让我们看看构成此示例的组件。
首先，我们必须包含 cstdarg 头文件。此头文件定义了 va_list、va_arg、va_start 和 va_end，它们是我们需要用来访问作为省略号一部分的参数的宏。
然后我们声明使用省略号的函数。请记住，参数列表必须是一个或多个固定参数。在这种情况下，我们传递一个整数，它告诉我们要平均多少个数字。省略号总是放在最后。
请注意，省略号参数没有名称！相反，我们通过一种特殊类型（称为 va_list）访问省略号中的值。将 va_list 概念性地视为指向省略号数组的指针是很有用的。首先，我们声明一个 va_list，为了简单起见，我们将其命名为“list”。
我们需要做的下一件事是让 list 指向我们的省略号参数。我们通过调用 va_start() 来完成此操作。va_start() 接受两个参数：va_list 本身，以及函数中
最后
一个非省略号参数的名称。调用 va_start() 后，va_list 指向省略号中的第一个参数。
要获取 va_list 当前指向的参数的值，我们使用 va_arg()。va_arg() 也接受两个参数：va_list 本身，以及我们要访问的参数的类型。请注意，va_arg() 还会将 va_list 移动到省略号中的下一个参数！
最后，当我们完成时，我们调用 va_end()，并将 va_list 作为参数。
请注意，va_start() 可以随时再次调用，以便将 va_list 重置为再次指向省略号中的第一个参数。
为什么省略号很危险：类型检查被暂停
省略号为程序员提供了很大的灵活性，可以实现接受可变数量参数的函数。然而，这种灵活性也伴随着一些缺点。
对于常规函数参数，编译器使用类型检查来确保函数参数的类型与函数参数的类型匹配（或可以隐式转换以使其匹配）。这有助于确保您不会在函数期望字符串时传递整数，反之亦然。但是，请注意省略号参数没有类型声明。使用省略号时，编译器会完全暂停对省略号参数的类型检查。这意味着可以将任何类型的参数发送到省略号！然而，缺点是如果调用函数时省略号参数没有意义，编译器将无法再警告您。使用省略号时，完全由调用者确保调用函数时省略号参数是函数可以处理的。显然，这留下了很大的错误空间（特别是如果调用者不是编写函数的人）。
让我们看一个非常微妙的错误示例
std::cout << findAverage(6, 1.0, 2, 3, 4, 5, 6) << '\n';
虽然乍一看这可能看起来无害，但请注意第二个参数（第一个省略号参数）是 double 而不是整数。这编译得很顺利，并产生了一个有点令人惊讶的结果
1.78782e+008
这是一个非常大的数字。这是怎么发生的？
正如您在前面的课程中了解到的那样，计算机将所有数据存储为位序列。变量的类型告诉计算机如何将该位序列转换为有意义的值。然而，您刚刚了解到省略号会丢弃变量的类型！因此，从省略号中获取有意义的值的唯一方法是手动告诉 va_arg() 下一个参数的预期类型。这就是 va_arg() 的第二个参数所做的事情。如果实际参数类型与预期参数类型不匹配，通常会发生不好的事情。
在上面的 findAverage 程序中，我们告诉 va_arg() 我们的变量都预期具有 int 类型。因此，每次调用 va_arg() 都会将下一个位序列解释为整数返回。
在这种情况下，问题在于我们作为第一个省略号参数传入的 double 是 8 字节，而 va_arg(list, int) 每次调用只会返回 4 字节的数据。因此，对 va_arg 的第一次调用将只读取 double 的前 4 字节（产生垃圾结果），对 va_arg 的第二次调用将读取 double 的后 4 字节（产生另一个垃圾结果）。因此，我们的整体结果是垃圾。
由于类型检查被暂停，如果我们做一些完全荒谬的事情，编译器甚至不会抱怨，比如这样
int value{ 7 };
    std::cout << findAverage(6, 1.0, 2, "Hello, world!", 'G', &value, &findAverage) << '\n';
信不信由你，这实际上编译得很顺利，并在作者的机器上产生了以下结果
1.79766e+008
这个结果概括了“垃圾进，垃圾出”这句话，这是一个流行的计算机科学短语，“主要用于提醒人们，计算机不像人类，会毫无疑问地处理最荒谬的输入数据并产生荒谬的输出”（
维基百科
）。
所以，总而言之，参数的类型检查被暂停，我们必须相信调用者会传入正确类型的参数。如果他们不这样做，编译器不会抱怨——我们的程序只会产生垃圾（或者可能崩溃）。
为什么省略号很危险：省略号不知道传递了多少参数
省略号不仅会丢弃参数的
类型
，还会丢弃省略号中参数的
数量
。这意味着我们必须设计自己的解决方案来跟踪传递给省略号的参数数量。通常，这可以通过以下三种方式之一完成。
方法 1：传递一个长度参数
方法 #1 是让其中一个固定参数表示传递的可选参数的数量。这是我们在上面的 findAverage() 示例中使用的解决方案。
然而，即使在这里，我们也会遇到麻烦。例如，考虑以下调用：
std::cout << findAverage(6, 1, 2, 3, 4, 5) << '\n';
在作者编写本文时，在作者的机器上，这产生了结果
699773
发生了什么？我们告诉 findAverage() 我们将提供 6 个额外的值，但我们只给了它 5 个。因此，va_arg() 返回的前五个值是我们传入的值。它返回的第 6 个值是堆栈中某个地方的垃圾值。因此，我们得到了一个垃圾答案。
一个更阴险的案例
std::cout << findAverage(6, 1, 2, 3, 4, 5, 6, 7) << '\n';
这产生答案 3.5，乍一看可能看起来是正确的，但它省略了平均值中的最后一个数字，因为我们只告诉它我们将提供 6 个额外的值（然后实际提供了 7 个）。这种错误很难被发现。
方法 2：使用哨兵值
方法 #2 是使用一个哨兵值。
哨兵
是一个特殊值，用于在遇到时终止循环。例如，对于字符串，空终止符用作哨兵值以表示字符串的结尾。对于省略号，哨兵通常作为最后一个参数传入。以下是 findAverage() 重写为使用哨兵值 -1 的示例：
#include <iostream>
#include <cstdarg> // needed to use ellipsis

// The ellipsis must be the last parameter
double findAverage(int first, ...)
{
	// We have to deal with the first number specially
	int sum{ first };

	// We access the ellipsis through a va_list, so let's declare one
	std::va_list list;

	// We initialize the va_list using va_start.  The first argument is
	// the list to initialize.  The second argument is the last non-ellipsis
	// parameter.
	va_start(list, first);

	int count{ 1 };
	// Loop indefinitely
	while (true)
	{
		// We use va_arg to get values out of our ellipsis
		// The first argument is the va_list we're using
		// The second argument is the type of the value
		int arg{ va_arg(list, int) };

		// If this parameter is our sentinel value, stop looping
		if (arg == -1)
			break;

		sum += arg;
		++count;
	}

	// Cleanup the va_list when we're done.
	va_end(list);

	return static_cast<double>(sum) / count;
}

int main()
{
	std::cout << findAverage(1, 2, 3, 4, 5, -1) << '\n';
	std::cout << findAverage(1, 2, 3, 4, 5, 6, -1) << '\n';

	return 0;
}
请注意，我们不再需要将显式长度作为第一个参数传递。相反，我们将哨兵值作为最后一个参数传递。
然而，这里有几个挑战。首先，C++ 要求我们至少传递一个固定参数。在前面的示例中，这是我们的 count 变量。在此示例中，第一个值实际上是要平均的数字的一部分。因此，我们没有将要平均的第一个值视为省略号参数的一部分，而是将其显式声明为普通参数。然后，我们需要在函数内部对其进行特殊处理（在这种情况下，我们将 sum 设置为 first 而不是 0 开始）。
其次，这要求用户将哨兵作为最后一个值传入。如果用户忘记传入哨兵值（或传入错误的值），函数将无限循环，直到遇到与哨兵匹配的垃圾（或崩溃）。
最后，请注意我们选择了 -1 作为我们的哨兵。如果我们只想找到正数的平均值，那没关系，但是如果我们想包含负数呢？哨兵值只有在存在一个超出您尝试解决的问题的有效值集的值时才有效。
方法 3：使用解码字符串
方法 #3 涉及传递一个“解码字符串”，它告诉程序如何解释参数。
#include <iostream>
#include <string_view>
#include <cstdarg> // needed to use ellipsis

// The ellipsis must be the last parameter
double findAverage(std::string_view decoder, ...)
{
	double sum{ 0 };

	// We access the ellipsis through a va_list, so let's declare one
	std::va_list list;

	// We initialize the va_list using va_start.  The first argument is
	// the list to initialize.  The second argument is the last non-ellipsis
	// parameter.
	va_start(list, decoder);

	for (auto codetype: decoder)
	{
		switch (codetype)
		{
		case 'i':
			sum += va_arg(list, int);
			break;

		case 'd':
			sum += va_arg(list, double);
			break;
		}
	}

	// Cleanup the va_list when we're done.
	va_end(list);

	return sum / std::size(decoder);
}

int main()
{
	std::cout << findAverage("iiiii", 1, 2, 3, 4, 5) << '\n';
	std::cout << findAverage("iiiiii", 1, 2, 3, 4, 5, 6) << '\n';
	std::cout << findAverage("iiddi", 1, 2, 3.5, 4.5, 5) << '\n';

	return 0;
}
在此示例中，我们传递一个字符串，它编码了可选变量的数量及其类型。酷的是，这使我们能够处理不同类型的参数。然而，这种方法也有缺点：解码字符串可能有点神秘，如果可选参数的数量或类型与解码字符串不精确匹配，可能会发生不好的事情。
对于那些来自 C 语言的人来说，这就是 printf 所做的！
更安全地使用省略号的建议
首先，如果可能，完全不要使用省略号！通常，即使需要稍微多做一些工作，也存在其他合理的解决方案。例如，在我们的 findAverage() 程序中，我们可以传入一个动态大小的整数数组。这将提供强大的类型检查（以确保调用者不会尝试做一些无意义的事情），同时保留传递可变数量整数以进行平均的能力。
其次，如果您确实使用省略号，最好传递给省略号参数的所有值都是相同类型（例如，全部为
int
，或全部为
double
，而不是混合）。混合不同类型会大大增加调用者无意中传入错误类型数据和 va_arg() 产生垃圾结果的可能性。
第三，使用计数参数或解码字符串参数通常比使用哨兵值更安全。这会强制用户为计数/解码参数选择一个适当的值，这确保了即使它产生垃圾值，省略号循环也会在合理的迭代次数后终止。
致进阶读者
为了改进类似省略号的功能，C++11 引入了
参数包
和
可变参数模板
，它们提供了与省略号类似的功能，但具有强类型检查。然而，显着的使用性挑战阻碍了此功能的采用。
在 C++17 中，添加了
折叠表达式
，这显著提高了参数包的可用性，以至于它们现在是一个可行的选择。
我们希望在未来的网站更新中介绍这些主题的课程。
下一课
20.6
Lambda 表达式（匿名函数）简介
返回目录
上一课
20.4
命令行参数