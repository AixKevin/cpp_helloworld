# 4.9 — 布尔值

4.9 — 布尔值
Alex
2007 年 6 月 9 日，太平洋夏令时下午 3:34
2025 年 2 月 4 日
在现实生活中，我们经常会问或被问到可以用“是”或“否”来回答的问题。“苹果是水果吗？” 是。“你喜欢芦笋吗？” 否。
现在考虑一个可以用“真”或“假”来回答的类似陈述：“苹果是水果”。这显然是真的。或者“我喜欢芦笋”。绝对是假的（真恶心！）。
这类只有两种可能结果（是/真，或否/假）的句子非常常见，以至于许多编程语言都包含一种特殊的类型来处理它们。这种类型称为**布尔**类型（注意：在英语中，布尔通常大写，因为它以其发明者乔治·布尔的名字命名）。
布尔变量
布尔变量是只能有两种可能值：
true
和
false
的变量。
要声明一个布尔变量，我们使用关键字
bool
。
bool b;
要初始化或将
true
或
false
值赋给布尔变量，我们使用关键字
true
和
false
。
bool b1 { true };
bool b2 { false };
b1 = false;
bool b3 {}; // default initialize to false
就像一元减号运算符 (-) 可以将整数变为负数一样，逻辑非运算符 (!) 可以将布尔值从
true
翻转为
false
，或从
false
翻转为
true
。
bool b1 { !true }; // b1 will be initialized with the value false
bool b2 { !false }; // b2 will be initialized with the value true
布尔值实际上不是以“true”或“false”的词语存储在布尔变量中的。相反，它们以整型值存储：
true
存储为整数
1
，
false
存储为整数
0
。同样，当布尔值被评估时，它们实际上不会评估为“true”或“false”。它们评估为整数
0
(false) 或
1
(true)。因为布尔值存储整型值，所以它们被认为是整型类型。
打印布尔值
当我们打印布尔值时，
std::cout
会打印
0
代表
false
，打印
1
代表
true
。
#include <iostream>

int main()
{
    std::cout << true << '\n'; // true evaluates to 1
    std::cout << !true << '\n'; // !true evaluates to 0

    bool b {false};
    std::cout << b << '\n'; // b is false, which evaluates to 0
    std::cout << !b << '\n'; // !b is true, which evaluates to 1
    return 0;
}
输出
1
0
0
1
使用
std::boolalpha
打印
true
或
false
如果你希望
std::cout
打印
true
或
false
而不是
0
或
1
，你可以输出
std::boolalpha
。这不会输出任何内容，但会操纵
std::cout
输出
bool
值的方式。
这是一个例子
#include <iostream>

int main()
{
    std::cout << true << '\n';
    std::cout << false << '\n';

    std::cout << std::boolalpha; // print bools as true or false

    std::cout << true << '\n';
    std::cout << false << '\n';
    return 0;
}
这会打印
1
0
true
false
你可以使用
std::noboolalpha
将其关闭。
整数到布尔值的转换
使用统一初始化时，您可以使用整数字面量
0
（表示
false
）和
1
（表示
true
）来初始化变量（但您实际上应该使用
false
和
true
）。其他整数字面量会导致编译错误。
#include <iostream>

int main()
{
	bool bFalse { 0 }; // okay: initialized to false
	bool bTrue  { 1 }; // okay: initialized to true
	bool bNo    { 2 }; // error: narrowing conversions disallowed

	std::cout << bFalse << bTrue << bNo << '\n';
	
	return 0;
}
然而，在任何可以将整数转换为布尔值的上下文中，整数
0
将转换为
false
，而任何其他整数将转换为
true
。
#include <iostream>

int main()
{
	std::cout << std::boolalpha; // print bools as true or false

	bool b1 = 4 ; // copy initialization allows implicit conversion from int to bool
	std::cout << b1 << '\n';

	bool b2 = 0 ; // copy initialization allows implicit conversion from int to bool
	std::cout << b2 << '\n';

	return 0;
}
这会打印
true
false
注意：`bool b1 = 4;` 可能会产生警告。如果出现这种情况，您需要禁用将警告视为错误才能编译此示例。
输入布尔值
使用
std::cin
输入布尔值有时会困扰新程序员。
考虑以下程序
#include <iostream>

int main()
{
	bool b{}; // default initialize to false
	std::cout << "Enter a boolean value: ";
	std::cin >> b;
	std::cout << "You entered: " << b << '\n';

	return 0;
}
Enter a Boolean value: true
You entered: 0
等等，什么？
默认情况下，
std::cin
只接受布尔变量的数字输入：
0
是
false
，
1
是
true
。任何其他数字值都将被解释为
true
，并导致
std::cin
进入失败模式。任何非数字值都将被解释为
false
，并导致
std::cin
进入失败模式。
相关内容
我们将在
9.5 -- std::cin 和处理无效输入
课程中讨论失败模式（以及如何摆脱它）。
在这种情况下，因为我们输入了
true
，
std::cin
静默失败并将
b
设置为
false
。因此，当
std::cout
打印
b
的值时，它打印
0
。
要让
std::cin
接受单词
false
和
true
作为输入，您必须首先输入
std::boolalpha
。
#include <iostream>

int main()
{
	bool b{};
	std::cout << "Enter a boolean value: ";

	// Allow the user to input 'true' or 'false' for boolean values
	// This is case-sensitive, so True or TRUE will not work
	std::cin >> std::boolalpha;
	std::cin >> b;

	// Let's also output bool values as `true` or `false`
	std::cout << std::boolalpha;
	std::cout << "You entered: " << b << '\n';

	return 0;
}
但是，当输入启用
std::boolalpha
时，数字值将不再被接受（它们会评估为
false
并导致 std::cin 进入失败模式）。
警告
启用
std::boolalpha
进行输入将只允许接受小写字母的
false
或
true
。带大写字母的变体将不被接受。
0
和
1
也将不再被接受。
请注意，我们使用
std::cin >> std::boolalpha;
将布尔值作为
true
或
false
输入，使用
std::cout << std::boolalpha;
将布尔值作为
true
或
false
输出。这些是独立的控制，可以单独打开（使用
std::boolalpha
）或关闭（使用
std::noboolalpha
）。
布尔返回值
布尔值经常用作检查某事是否为真的函数的返回值。此类函数通常以单词 *is*（例如 isEqual）或 *has*（例如 hasCommonDivisor）开头命名。
考虑以下示例，它与上面非常相似
#include <iostream>

// returns true if x and y are equal, false otherwise
bool isEqual(int x, int y)
{
    return x == y; // operator== returns true if x equals y, and false otherwise
}

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    std::cout << std::boolalpha; // print bools as true or false
    
    std::cout << x << " and " << y << " are equal? ";
    std::cout << isEqual(x, y) << '\n'; // will return true or false

    return 0;
}
这是此程序两次运行的输出
Enter an integer: 5
Enter another integer: 5
5 and 5 are equal? true
Enter an integer: 6
Enter another integer: 4
6 and 4 are equal? false
这如何运作？首先我们读入
x
和
y
的整数值。接下来，表达式
isEqual(x, y)
被求值。在第一次运行时，这导致对
isEqual(5, 5)
的函数调用。在该函数内部，
5 == 5
被求值，产生值
true
。值
true
返回给调用者，由
std::cout
打印。在第二次运行时，对
isEqual(6, 4)
的调用返回值为
false
。
布尔值需要一点时间来适应，但是一旦你理解了它们，它们的简洁性会让人耳目一新！布尔值也是语言的巨大组成部分——你最终会比所有其他基本类型加起来使用它们更多！
我们将在下一课继续探索布尔值。
下一课
4.10
if 语句简介
返回目录
上一课
4.8
浮点数