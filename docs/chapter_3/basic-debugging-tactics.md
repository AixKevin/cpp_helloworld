# 3.4 — 基本调试策略

3.4 — 基本调试策略
Alex
2019 年 2 月 1 日，太平洋标准时间上午 11:56
2024 年 12 月 30 日
在上一课中，我们探讨了一种通过运行程序并使用猜测来找出问题所在区域的策略。在本课中，我们将探讨一些基本的策略，用于实际进行这些猜测并收集信息以帮助查找问题。
调试策略 #1：注释掉你的代码
让我们从一个简单的开始。如果你的程序出现了错误行为，一种减少需要搜索的代码量的方法是注释掉一些代码，看看问题是否仍然存在。如果问题保持不变，那么被注释掉的代码可能不是导致问题的原因。
考虑以下代码：
int main()
{
    getNames(); // ask user to enter a bunch of names
    doMaintenance(); // do some random stuff
    sortNames(); // sort them in alphabetical order
    printNames(); // print the sorted list of names

    return 0;
}
假设这个程序应该按字母顺序打印用户输入的姓名，但它却按逆字母顺序打印。问题出在哪里？是
getNames
输入姓名不正确吗？是
sortNames
倒序排序吗？是
printNames
倒序打印吗？这些都可能是。但我们可能怀疑 doMaintenance() 与问题无关，所以我们先注释掉它。
int main()
{
    getNames(); // ask user to enter a bunch of names
//    doMaintenance(); // do some random stuff
    sortNames(); // sort them in alphabetical order
    printNames(); // print the sorted list of names

    return 0;
}
有三种可能的结果：
如果问题消失了，那么
doMaintenance
肯定是导致问题的原因，我们应该将注意力集中在那里。
如果问题没有改变（这更有可能），那么我们可以合理地假设
doMaintenance
没有问题，我们可以暂时将整个函数排除在搜索范围之外。这并不能帮助我们理解实际问题是在调用
doMaintenance
之前还是之后，但它减少了我们后续需要查看的代码量。
如果注释掉
doMaintenance
导致问题演变成其他相关问题（例如程序停止打印姓名），那么
doMaintenance
很可能正在做一些其他代码依赖的有用事情。在这种情况下，我们可能无法判断问题是在
doMaintenance
中还是在其他地方，因此我们可以取消注释
doMaintenance
并尝试其他方法。
警告
不要忘记你注释掉了哪些函数，以便以后可以取消注释它们！
在进行许多与调试相关的更改后，很容易忘记撤销一两个。如果发生这种情况，你最终会修复一个错误，但却引入其他错误！
拥有一个好的版本控制系统在这里非常有用，因为你可以将你的代码与主分支进行比较，以查看你所做的所有与调试相关的更改（并确保在提交更改之前将其恢复）。
提示
一种替代反复添加/删除或取消注释/注释调试语句的方法是使用第三方库，该库允许你将调试语句留在代码中，但在发布模式下通过预处理器宏将其编译掉。
dbg
就是这样一种仅包含头文件的库，旨在帮助实现这一点（通过
DBG_MACRO_DISABLE
预处理器宏）。
我们在第
7.9 课 -- 内联函数和变量
中讨论了仅包含头文件的库。
调试策略 #2：验证你的代码流程
在更复杂的程序中，另一个常见问题是程序调用函数次数过多或过少（包括根本不调用）。
在这种情况下，在函数顶部放置语句以打印函数名称可能会有所帮助。这样，当程序运行时，你就可以看到哪些函数被调用了。
提示
在打印调试信息时，使用
std::cerr
而不是
std::cout
。原因之一是
std::cout
可能会被缓冲，这意味着从你要求
std::cout
输出文本到它实际输出之间可能会经过一段时间。如果你使用
std::cout
输出，然后程序立即崩溃，那么
std::cout
可能已经输出，也可能还没有。这可能会误导你问题出在哪里。另一方面，
std::cerr
是非缓冲的，这意味着你发送给它的任何内容都会立即输出。这有助于确保所有调试输出尽快出现（以牺牲一些性能为代价，这在调试时通常不重要）。
使用
std::cerr
也有助于明确输出的信息是针对错误情况而不是正常情况。
我们在第
9.4 课 -- 检测和处理错误
中进一步讨论何时使用
std::cout
与
std::cerr
。
考虑以下不能正常工作的简单程序：
#include <iostream>

int getValue()
{
	return 4;
}

int main()
{
    std::cout << getValue << '\n';

    return 0;
}
您可能需要禁用“将警告视为错误”才能编译上述代码。
尽管我们期望这个程序打印值
4
，但它应该打印值
1
在 Visual Studio（以及可能一些其他编译器）上，它可能会打印以下内容：
00101424
相关内容
我们在
20.1 课 -- 函数指针
中讨论了为什么有些编译器打印
1
而不是地址（以及如果你的编译器打印
1
但你希望它打印地址该怎么办）。
让我们为这些函数添加一些调试语句
#include <iostream>

int getValue()
{
std::cerr << "getValue() called\n";
	return 4;
}

int main()
{
std::cerr << "main() called\n";
    std::cout << getValue << '\n';

    return 0;
}
提示
添加临时调试语句时，不缩进它们可能会有所帮助。这使得它们以后更容易被找到并删除。
如果你正在使用 clang-format 来格式化你的代码，它会尝试自动缩进这些行。你可以像这样抑制自动格式化：
// clang-format off
std::cerr << "main() called\n";
// clang-format on
现在当这些函数执行时，它们将输出它们的名称，表明它们被调用了
main() called
1
现在我们可以看到函数
getValue
从未被调用。调用该函数的代码一定有问题。让我们仔细看看那一行：
std::cout << getValue << '\n';
哦，看，我们忘了函数调用的括号。它应该是
#include <iostream>

int getValue()
{
std::cerr << "getValue() called\n";
	return 4;
}

int main()
{
std::cerr << "main() called\n";
    std::cout << getValue() << '\n'; // added parenthesis here

    return 0;
}
现在这将产生正确的输出
main() called
getValue() called
4
然后我们可以删除临时调试语句。
调试策略 #3：打印值
对于某些类型的错误，程序可能会计算或传递错误的值。
我们还可以输出变量（包括参数）或表达式的值，以确保它们是正确的。
考虑以下应该将两个数字相加但不能正常工作的程序：
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getUserInput() };
	int y{ getUserInput() };

	int z{ add(x, 5) };
	printResult(z);

	return 0;
}
这是这个程序的一些输出
Enter a number: 4
Enter a number: 3
The answer is: 9
那不对。你看到错误了吗？即使在这个简短的程序中，也很难发现。让我们添加一些代码来调试我们的值
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, 5) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
这是上面的输出
Enter a number: 4
main::x = 4
Enter a number: 3
main::y = 3
main::z = 9
The answer is: 9
变量
x
和
y
获得了正确的值，但是变量
z
没有。问题一定在这两点之间，这使得函数
add
成为一个关键的嫌疑对象。
让我们修改函数 add
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x <<", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, 5) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
现在我们将得到输出
Enter a number: 4
main::x = 4
Enter a number: 3
main::y = 3
add() called (x=4, y=5)
main::z = 9
The answer is: 9
变量
y
的值为 3，但不知何故，我们的函数
add
为参数
y
获得了值 5。我们一定是传递了错误的参数。果然
int z{ add(x, 5) };
就在那里。我们传递了字面量
5
而不是变量
y
的值作为参数。这是一个简单的修复，然后我们可以删除调试语句。
再举一个例子
这个程序与前一个非常相似，但也无法正常工作。
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return --x;
}

int main()
{
	int x{ getUserInput() };
	int y{ getUserInput() };

	int z { add(x, y) };
	printResult(z);

	return 0;
}
如果我们运行这段代码并看到以下内容
Enter a number: 4
Enter a number: 3
The answer is: 5
嗯，有点不对劲。但是哪里出了问题？
让我们用一些调试工具来检测这段代码
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x << ", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
std::cerr << "printResult() called (z=" << z << ")\n";
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return --x;
}

int main()
{
std::cerr << "main() called\n";
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, y) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
现在，让我们再次使用相同的输入运行程序。
main() called
getUserInput() called
Enter a number: 4
main::x = 3
getUserInput() called
Enter a number: 3
main::y = 2
add() called (x=3, y=2)
main::z = 5
printResult() called (z=5)
The answer is: 5
现在我们可以立即看到出了问题：用户输入的值是
4
，但 main 中的
x
却得到了值
3
。从用户输入到该值分配给 main 的变量
x
之间一定出了问题。让我们通过在函数
getUserInput
中添加一些调试代码来确保程序从用户那里获得了正确的值：
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x << ", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
std::cerr << "printResult() called (z=" << z << ")\n";
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
std::cerr << "getUserInput::x = " << x << '\n'; // added this additional line of debugging
	return --x;
}

int main()
{
std::cerr << "main() called\n";
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, y) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
和输出
main() called
getUserInput() called
Enter a number: 4
getUserInput::x = 4
main::x = 3
getUserInput() called
Enter a number: 3
getUserInput::x = 3
main::y = 2
add() called (x=3, y=2)
main::z = 5
printResult() called (z=5)
The answer is: 5
通过这额外的调试行，我们可以看到用户输入正确地接收到了 getUserInput 的变量
x
中。然而，main 的变量
x
却得到了错误的值。问题一定是在这两点之间。唯一的罪魁祸首就是函数
getUserInput
的返回值。让我们更仔细地看看那一行。
return --x;
嗯，这很奇怪。x 前面那个
--
符号是什么？我们还没有在本教程中涉及它，所以如果你不知道它是什么意思，请不要担心。但是即使不知道它是什么意思，通过你的调试努力，你也可以合理地确定这一特定行有问题——因此，很可能这个
--
符号导致了问题。
由于我们真的希望
getUserInput
只返回
x
的值，所以让我们移除
--
看看会发生什么
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x << ", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
std::cerr << "printResult() called (z=" << z << ")\n";
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
std::cerr << "getUserInput::x = " << x << '\n';
	return x; // removed -- before x
}

int main()
{
std::cerr << "main() called\n";
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, y) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
现在输出
main() called
getUserInput() called
Enter a number: 4
getUserInput::x = 4
main::x = 4
getUserInput() called
Enter a number: 3
getUserInput::x = 3
main::y = 3
add() called (x=4, y=3)
main::z = 7
printResult() called (z=7)
The answer is: 7
程序现在正常运行。即使不了解
--
的作用，我们也能够识别导致问题的特定代码行，然后修复问题。
为什么使用打印语句进行调试效果不佳
虽然在程序中添加调试语句用于诊断目的是一种常见的基本技术，并且是一种有效的方法（尤其是在某种原因无法使用调试器时），但由于多种原因，它并不是那么好
调试语句会使你的代码变得混乱。
调试语句会使程序的输出变得混乱。
调试语句需要修改你的代码才能添加和删除，这可能会引入新的错误。
调试语句在你用完后必须删除，这使得它们不可重用。
我们可以做得更好。我们将在未来的课程中探讨如何做到这一点。
下一课
3.5
更多调试策略
返回目录
上一课
3.3
调试策略