# 1.11 — 开发你的第一个程序

1.11 — 开发你的第一个程序
Alex
2019 年 2 月 1 日，太平洋标准时间上午 10:11
2024 年 3 月 12 日
前面的课程介绍了大量我们将在几乎所有程序中使用的术语和概念。在本课程中，我们将逐步将这些知识整合到我们的第一个简单程序中。
乘以 2
首先，让我们创建一个程序，它要求用户输入一个整数，等待他们输入整数，然后告诉他们该数字的 2 倍是多少。程序应该产生以下输出（假设我输入 4 作为输入）
Enter an integer: 4
Double that number is: 8
我们如何处理这个问题？分步进行。
最佳实践
新程序员经常试图一次性编写整个程序，然后当程序产生大量错误时就会感到不知所措。一个更好的策略是每次添加一小部分，确保它能够编译，并对其进行测试。然后，当你确定它能够正常工作时，再继续下一部分。
我们在这里将利用这个策略。在执行每个步骤时，将每个程序键入（不要复制/粘贴）到你的代码编辑器中，然后编译并运行它。
首先，创建一个新的控制台项目。
现在我们从一些基本框架开始。我们知道我们需要一个 main() 函数（因为所有 C++ 程序都必须有一个），所以如果你的 IDE 在你创建新项目时没有创建一个空的 main() 函数，那么让我们创建一个
int main()
{
	return 0;
}
我们知道我们需要向控制台输出文本，并从用户键盘获取文本，因此我们需要包含 iostream 以访问 std::cout 和 std::cin。
#include <iostream>

int main()
{
	return 0;
}
现在让我们告诉用户我们需要他们输入一个整数
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";

	return 0;
}
此时，你的程序应该产生此结果
Enter an integer:
然后终止。
接下来，我们将获取用户的输入。我们将使用 std::cin 和 `operator>>` 来获取用户的输入。但我们还需要定义一个变量来存储该输入以备后用。
#include <iostream>

int main() // note: this program has an error somewhere
{
	std::cout << "Enter an integer: ";

	int num{ }; // define variable num as an integer variable
	std::cin << num; // get integer value from user's keyboard

	return 0;
}
是时候编译我们的更改了……然后……
噢，不！这是作者在 Visual Studio 2017 上得到的结果
1>------ Build started: Project: Double, Configuration: Release Win32 ------
1>Double.cpp
1>c:\vcprojects\double\double.cpp(8): error C2678: binary '<<': no operator found which takes a left-hand operand of type 'std::istream' (or there is no acceptable conversion)
1>c:\vcprojects\double\double.cpp: note: could be 'built-in C++ operator<<(bool, int)'
1>c:\vcprojects\double\double.cpp: note: while trying to match the argument list '(std::istream, int)'
1>Done building project "Double.vcxproj" -- FAILED.
========== Build: 0 succeeded, 1 failed, 0 up-to-date, 0 skipped ==========
我们遇到了编译错误！
首先，由于程序在我们进行最新更新之前能够编译，而现在不能编译，所以错误**一定**在我们刚刚添加的代码中（第 7 行和第 8 行）。这大大减少了我们扫描以查找错误的代码量。第 7 行非常简单（只是一个变量定义），所以错误可能不在那里。这使得第 8 行成为可能的罪魁祸首。
其次，这个错误信息不是很易读。但是让我们分析一些关键要素：编译器告诉我们它在第 8 行遇到了错误。这意味着实际错误可能在第 8 行，或者可能是前一行，这证实了我们之前的评估。接下来，编译器告诉你它找不到一个左操作数为 `std::istream` 类型（也就是 `std::cin` 的类型）的 `<<` 运算符。换句话说，`operator<<` 不知道如何处理 `std::cin`，所以错误肯定在于我们对 `std::cin` 的使用，或者我们对 `operator<<` 的使用。
现在看到错误了吗？如果你没有，花点时间看看你能不能找到它。
这是包含纠正后代码的程序
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";

	int num{ };
	std::cin >> num; // std::cin uses operator >>, not operator <<!

	return 0;
}
现在程序将编译，我们可以测试它。程序将等待你输入一个数字，所以让我们输入 4。输出应该如下所示
Enter an integer: 4
快完成了！最后一步是将数字加倍。
完成这最后一步后，我们的程序将成功编译并运行，产生所需的输出。
我们有（至少）3 种方法可以做到这一点。让我们从最差到最佳。
不好的解决方案
#include <iostream>

// worst version
int main()
{
	std::cout << "Enter an integer: ";

	int num{ };
	std::cin >> num;

	num = num * 2; // double num's value, then assign that value back to num

	std::cout << "Double that number is: " << num << '\n';

	return 0;
}
在这个解决方案中，我们使用一个表达式将 *num* 乘以 2，然后将该值重新赋值给 *num*。从那时起，*num* 将包含我们加倍后的数字。
为什么这是一个糟糕的解决方案
在赋值语句之前，num 包含用户输入。赋值之后，它包含一个不同的值。这令人困惑。
我们通过将新值赋给输入变量来覆盖了用户的输入，所以如果我们想扩展我们的程序以后对该输入值做其他事情（例如，将用户的输入乘以三），它就已经丢失了。
基本不错的解决方案
#include <iostream>

// less-bad version
int main()
{
	std::cout << "Enter an integer: ";

	int num{ };
	std::cin >> num;

	int doublenum{ num * 2 }; // define a new variable and initialize it with num * 2
	std::cout << "Double that number is: " << doublenum << '\n'; // then print the value of that variable here

	return 0;
}
这个解决方案非常直观易懂，并且解决了最差解决方案中遇到的两个问题。
这里的主要缺点是，我们正在定义一个新变量（这增加了复杂性）来存储一个我们只使用一次的值。我们可以做得更好。
首选解决方案
#include <iostream>

// preferred version
int main()
{
	std::cout << "Enter an integer: ";

	int num{ };
	std::cin >> num;

	std::cout << "Double that number is: " <<  num * 2 << '\n'; // use an expression to multiply num * 2 at the point where we are going to print it

	return 0;
}
这是这一组中首选的解决方案。当 `std::cout` 执行时，表达式 `num * 2` 将被求值，结果将是 `num` 值的两倍。该值将被打印。`num` 本身的值将不会被改变，所以如果需要，我们以后可以再次使用它。
此版本是我们的参考解决方案。
作者注
编程的首要目标是让你的程序能够工作。一个无法工作的程序，无论写得多么好，都是没用的。
然而，我喜欢一句格言：“你必须先写一遍程序，才知道你第一次应该怎么写。”这句话说明了最好的解决方案往往并不明显，而且我们对问题的第一个解决方案通常不如它可能达到的那样好。
当我们专注于如何使程序工作时，投入大量时间在我们甚至不知道是否会保留的代码上是没有多大意义的。所以我们走捷径。我们跳过错误处理和注释等。我们在解决方案中撒入调试代码以帮助我们诊断问题和查找错误。我们边学边做——我们认为可能有效的东西最终不起作用，我们不得不回头尝试另一种方法。
最终结果是，我们的初始解决方案通常结构不佳，不够健壮（防错），可读性差，或不够简洁。因此，一旦你的程序工作了，你的工作实际上并没有完成（除非程序是一次性的/临时性的）。下一步是清理你的代码。这包括：删除（或注释掉）临时/调试代码，添加注释，处理错误情况，格式化你的代码，并确保遵循最佳实践。即使那样，你的程序也可能没有它可能达到的那么简单——也许有可以合并的冗余逻辑，或者可以组合的多个语句，或者不需要的变量，或者其他一千个可以简化的小事情。新程序员太经常专注于性能优化，而他们应该专注于可维护性。
这些教程中呈现的解决方案很少有第一次就非常出色的。相反，它们是持续完善的结果，直到再也找不到可以改进的地方。在许多情况下，读者仍然发现许多其他可以改进的地方！
所有这一切都说明：如果你的解决方案没有从你的大脑中直接生成出最佳优化版本，不要感到沮丧。这是正常的。编程中的完美是一个迭代过程（需要重复的传递）。
作者注
还有一件事：你可能在想，“C++ 有这么多规则和概念。我怎么能记住所有这些东西呢？”。
简短的回答：你不会。C++ 是一部分使用你所知道的，两部分是查找如何做其余的。
当你第一次阅读本网站时，少关注记忆具体细节，多关注理解可能实现什么。然后，当你需要在你正在编写的程序中实现某些功能时，你可以回到这里（或参考网站）并重新学习如何做到这一点。
小测验时间
问题 #1
修改上面“最佳解决方案”程序的解决方案，使其输出如下（假设用户输入 4）
Enter an integer: 4
Double 4 is: 8
Triple 4 is: 12
显示答案
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";

	int num{ };
	std::cin >> num;

	std::cout << "Double " << num << " is: " << num * 2 << '\n';
	std::cout << "Triple " << num << " is: " << num * 3 << '\n';

	return 0;
}
下一课
1.x
第一章总结与测验
返回目录
上一课
1.10
表达式简介