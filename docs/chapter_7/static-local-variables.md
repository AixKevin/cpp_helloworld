# 7.11 — 静态局部变量

7.11 — 静态局部变量
Alex
2007 年 6 月 19 日，太平洋夏令时下午 5:46
2024 年 12 月 26 日
术语
static
是 C++ 语言中最令人困惑的术语之一，很大程度上是因为
static
在不同上下文中有不同的含义。
在之前的课程中，我们提到全局变量具有静态生命周期，这意味着它们在程序启动时创建，在程序结束时销毁。
我们还讨论了
static
关键字如何赋予全局标识符内部链接，这意味着该标识符只能在其定义的文件中使用。
在本课程中，我们将探讨
static
关键字应用于局部变量时的用法。
静态局部变量
在课程
2.5 -- 局部作用域简介
中，你学习到局部变量默认具有自动生命周期，这意味着它们在定义时创建，并在块退出时销毁。
在局部变量上使用
static
关键字会将其生命周期从自动生命周期更改为静态生命周期。这意味着该变量现在在程序启动时创建，并在程序结束时销毁（就像全局变量一样）。因此，静态变量即使在超出作用域后也会保留其值！
展示自动生命周期和静态生命周期局部变量之间差异的最简单方法是通过示例。
自动生命周期（默认）
#include <iostream>

void incrementAndPrint()
{
    int value{ 1 }; // automatic duration by default
    ++value;
    std::cout << value << '\n';
} // value is destroyed here

int main()
{
    incrementAndPrint();
    incrementAndPrint();
    incrementAndPrint();

    return 0;
}
每次调用
incrementAndPrint()
时，都会创建一个名为 value 的变量并将其赋值为
1
。
incrementAndPrint()
将 value 增加到
2
，然后打印值
2
。当
incrementAndPrint()
运行结束时，变量超出作用域并被销毁。因此，此程序输出
2
2
2
现在考虑一个使用静态局部变量的程序版本。这与上述程序唯一的区别在于，我们通过使用
static
关键字将局部变量从自动生命周期更改为静态生命周期。
静态生命周期（使用 static 关键字）
#include <iostream>

void incrementAndPrint()
{
    static int s_value{ 1 }; // static duration via static keyword.  This initializer is only executed once.
    ++s_value;
    std::cout << s_value << '\n';
} // s_value is not destroyed here, but becomes inaccessible because it goes out of scope

int main()
{
    incrementAndPrint();
    incrementAndPrint();
    incrementAndPrint();

    return 0;
}
在这个程序中，因为
s_value
被声明为
static
，它在程序启动时创建。
零初始化或具有 constexpr 初始化器的静态局部变量可以在程序启动时初始化。
没有初始化器或非 constexpr 初始化器的静态局部变量在程序启动时零初始化。具有非 constexpr 初始化器的静态局部变量在首次遇到变量定义时重新初始化。后续调用会跳过定义，因此不会发生进一步的重新初始化。由于它们具有静态生命周期，未显式初始化的静态局部变量将默认进行零初始化。
因为
s_value
具有 constexpr 初始化器
1
，所以
s_value
将在程序启动时初始化。
当
s_value
在函数结束时超出作用域时，它不会被销毁。每次调用
incrementAndPrint()
函数时，
s_value
的值都会保持在我们之前设置的值。因此，此程序输出
2
3
4
关键见解
当您需要局部变量在函数调用之间记住其值时，可以使用静态局部变量。
最佳实践
初始化您的静态局部变量。静态局部变量只在代码首次执行时初始化，而不是在后续调用时初始化。
提示
就像我们使用“g_”作为全局变量的前缀一样，通常使用“s_”作为静态（静态生命周期）局部变量的前缀。
ID 生成
静态生命周期局部变量最常见的用途之一是用于唯一 ID 生成器。想象一个程序，您有许多相似的对象（例如，一个游戏中您被许多僵尸攻击，或者一个模拟中您显示许多三角形）。如果您发现一个缺陷，几乎不可能区分哪个对象有问题。但是，如果每个对象在创建时都赋予一个唯一标识符，那么就可以更容易地区分对象进行进一步调试。
使用静态生命周期局部变量生成唯一 ID 号非常容易
int generateID()
{
    static int s_itemID{ 0 };
    return s_itemID++; // makes copy of s_itemID, increments the real s_itemID, then returns the value in the copy
}
第一次调用此函数时，它返回
0
。第二次调用时，它返回
1
。每次调用时，它都会返回一个比上次调用时高一个的数字。您可以将这些数字分配为对象的唯一 ID。由于
s_itemID
是一个局部变量，它不能被其他函数“篡改”。
静态变量提供了一些全局变量的优点（它们在程序结束之前不会被销毁），同时将其可见性限制在块作用域。这使得它们更容易理解和更安全使用。
关键见解
静态局部变量具有像局部变量一样的块作用域，但其生命周期直到程序结束，像全局变量一样。
静态局部常量
静态局部变量可以设置为 const（或 constexpr）。 const 静态局部变量的一个很好的用途是当您有一个函数需要使用 const 值，但创建或初始化对象很昂贵时（例如，您需要从数据库中读取值）。如果您使用普通的局部变量，则每次执行函数时都会创建和初始化变量。使用 const/constexpr 静态局部变量，您可以创建和初始化昂贵的对象一次，然后在每次调用函数时重复使用它。
关键见解
静态局部变量最好用于避免每次调用函数时昂贵的局部对象初始化。
不要使用静态局部变量来改变程序流程
考虑以下代码：
#include <iostream>

int getInteger()
{
	static bool s_isFirstCall{ true };

	if (s_isFirstCall)
	{
		std::cout << "Enter an integer: ";
		s_isFirstCall = false;
	}
	else
	{
		std::cout << "Enter another integer: ";
	}

	int i{};
	std::cin >> i;
	return i;
}

int main()
{
	int a{ getInteger() };
	int b{ getInteger() };

	std::cout << a << " + " << b << " = " << (a + b) << '\n';

	return 0;
}
样本输出
Enter an integer: 5
Enter another integer: 9
5 + 9 = 14
这段代码确实实现了其预期功能，但由于我们使用了静态局部变量，使得代码更难理解。如果有人在不阅读
getInteger()
实现的情况下阅读
main()
中的代码，他们没有理由认为对
getInteger()
的两次调用会做不同的事情。但这两次调用确实做了不同的事情，如果差异不仅仅是更改提示，这可能会非常令人困惑。
假设您按下微波炉上的 +1 按钮，微波炉会给剩余时间增加 1 分钟。您的饭菜热了，您很高兴。在您将饭菜从微波炉中取出之前，您看到窗外有一只猫，并看了一会儿，因为猫很酷。这段时间比您预期的要长，当您吃第一口饭时，它又冷了。没问题，只需将其放回微波炉并按 +1 键运行一分钟。但这次微波炉只增加了 1 秒而不是 1 分钟。这时您就会说“我什么都没改，现在它坏了”或“上次它还能用”。如果您再次做同样的事情，您会期望与上次相同的行为。函数也是如此。
假设我们想在计算器中添加减法，使得输出如下所示
Addition
Enter an integer: 5
Enter another integer: 9
5 + 9 = 14
Subtraction
Enter an integer: 12
Enter another integer: 3
12 - 3 = 9
我们可能会尝试使用
getInteger()
来读取接下来的两个整数，就像我们做加法一样。
int main()
{
  std::cout << "Addition\n";

  int a{ getInteger() };
  int b{ getInteger() };

  std::cout << a << " + " << b << " = " << (a + b) << '\n';

  std::cout << "Subtraction\n";

  int c{ getInteger() };
  int d{ getInteger() };

  std::cout << c << " - " << d << " = " << (c - d) << '\n';

  return 0;
}
但这并不能如我们所愿，因为输出是
Addition
Enter an integer: 5
Enter another integer: 9
5 + 9 = 14
Subtraction
Enter another integer: 12
Enter another integer: 3
12 - 3 = 9
（倒数第三行是“Enter another integer”而不是“Enter an integer”）
getInteger()
不可重用，因为它具有无法从外部重置的内部状态（静态局部变量
s_isFirstCall
）。
s_isFirstCall
不是一个在整个程序中都应该唯一的变量。尽管我们的程序在首次编写时运行良好，但静态局部变量阻止了我们以后重用该函数。
实现
getInteger
的一个更好的方法是将
s_isFirstCall
作为参数传递。这允许调用者选择要打印的提示符
#include <iostream>

// We'll define a symbolic constant with a nice name
constexpr bool g_firstCall { true };

int getInteger(bool bFirstCall)
{
	if (bFirstCall)
	{
		std::cout << "Enter an integer: ";
	}
	else
	{
		std::cout << "Enter another integer: ";
	}

	int i{};
	std::cin >> i;
	return i;
}

int main()
{
	int a{ getInteger(g_firstCall) };  // so that it's clearer what the argument represents here
	int b{ getInteger(!g_firstCall) };

	std::cout << a << " + " << b << " = " << (a + b) << '\n';

	return 0;
}
非 const 静态局部变量仅在您的整个程序中以及程序可预见的未来中，该变量是唯一的且重置该变量没有意义的情况下才应使用。
最佳实践
const 静态局部变量通常可以安全使用。
非 const 静态局部变量通常应避免使用。如果您确实使用了它们，请确保该变量永远不需要重置，并且不要用于改变程序流程。
提示
一个更可重用的解决方案是将
bool
参数更改为
std::string_view
，并让调用者传入将要使用的文本提示！
致进阶读者
在需要非 const 变量的多个实例以记住其值（例如，拥有多个 ID 生成器）的情况下，函子是一个很好的解决方案（参见课程
21.10 -- 重载括号运算符
）。
小测验时间
问题 #1
关键字
static
对全局变量有什么影响？对局部变量有什么影响？
显示答案
当应用于全局变量时，static 关键字将全局变量定义为具有内部链接，这意味着该变量不能导出到其他文件。
当应用于局部变量时，static 关键字将局部变量定义为具有静态生命周期，这意味着该变量只创建一次，并且直到程序结束才会被销毁。
下一课
7.12
作用域、生命周期和链接总结
返回目录
上一课
7.10
跨多个文件共享全局常量（使用内联变量）