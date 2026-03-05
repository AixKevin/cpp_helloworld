# 20.4 — 命令行参数

20.4 — 命令行参数
Alex
2008 年 2 月 15 日，下午 4:06 PST
2024 年 6 月 25 日
对命令行参数的需求
正如你在第
0.5 课——编译器、链接器和库简介
中所学，当你编译和链接程序时，输出是一个可执行文件。程序运行时，执行从名为 main() 的函数顶部开始。到目前为止，我们像这样声明 main：
int main()
注意，这个版本的 main() 没有参数。然而，许多程序需要某种输入才能工作。例如，假设你正在编写一个名为 Thumbnail 的程序，它读取图像文件，然后生成一个缩略图（图像的缩小版本）。Thumbnail 如何知道要读取和处理哪个图像？用户必须有某种方法告诉程序要打开哪个文件。为此，你可以采用这种方法：
// Program: Thumbnail
#include <iostream>
#include <string>

int main()
{
    std::cout << "Please enter an image filename to create a thumbnail for: ";
    std::string filename{};
    std::cin >> filename;

    // open image file
    // create thumbnail
    // output thumbnail
}
然而，这种方法存在一个潜在问题。每次程序运行时，程序都会等待用户输入。如果你从命令行手动运行此程序一次，这可能不是问题。但在其他情况下，例如当你想在许多文件上运行此程序，或者让另一个程序运行此程序时，这就会有问题。
让我们进一步探讨这些情况。
考虑你想为给定目录中的所有图像文件创建缩略图的情况。你将如何做到这一点？你可以根据目录中的图像数量多次运行此程序，手动输入每个文件名。然而，如果图片有数百张，这可能需要一整天！一个好的解决方案是编写一个程序，循环遍历目录中的每个文件名，为每个文件调用一次 Thumbnail。
现在考虑你正在运行一个网站的情况，并且你希望你的网站在用户每次上传图像到你的网站时创建一个缩略图。这个程序没有设置为接受来自网络的输入，那么在这种情况下，上传者如何输入文件名呢？一个好的解决方案是让你的网络服务器在上传后自动调用 Thumbnail。
在这两种情况下，我们确实需要一种方法，让外部**程序**在启动 Thumbnail 时将文件名作为输入传递给我们的 Thumbnail 程序，而不是让 Thumbnail 在启动后等待**用户**输入文件名。
**命令行参数**是操作系统在程序启动时传递给程序的可选字符串参数。程序可以将其用作输入（或忽略它们）。就像函数参数提供了一种函数向另一个函数提供输入的方式一样，命令行参数提供了一种人或程序向**程序**提供输入的方式。
传递命令行参数
可执行程序可以通过名称调用在命令行上运行。例如，要在 Windows 机器的当前目录中运行可执行文件“WordCount”，你可以键入：
WordCount
在基于 Unix 的操作系统上，等效的命令行是：
./WordCount
为了将命令行参数传递给 WordCount，我们只需在可执行文件名后列出命令行参数：
WordCount Myfile.txt
现在，当 WordCount 执行时，Myfile.txt 将作为命令行参数提供。一个程序可以有多个命令行参数，用空格分隔：
WordCount Myfile.txt Myotherfile.txt
如果你从 IDE 运行程序，IDE 应该提供一种输入命令行参数的方法。
在 Microsoft Visual Studio 中，右键单击解决方案资源管理器中的项目，然后选择属性。打开“配置属性”树元素，然后选择“调试”。在右侧窗格中，有一行名为“命令行参数”。你可以在那里输入你的命令行参数进行测试，当程序运行时，它们将自动传递给你的程序。
在 Code::Blocks 中，选择“项目 -> 设置程序参数”。
使用命令行参数
现在你知道如何向程序提供命令行参数，下一步是从我们的 C++ 程序中访问它们。为此，我们使用一种与以前见过的不同的 main() 形式。这种新形式的 main() 接受两个参数（按照惯例命名为 argc 和 argv），如下所示：
int main(int argc, char* argv[])
你有时也会看到它写成：
int main(int argc, char** argv)
尽管这些被视为相同，但我们更喜欢第一种表示形式，因为它直观上更容易理解。
**argc** 是一个整数参数，包含传递给程序的参数数量（可以理解为：argc = **arg**ument **c**ount）。argc 总是至少为 1，因为第一个参数总是程序本身的名称。用户提供的每个命令行参数都会使 argc 增加 1。
**argv** 是实际参数值存储的地方（可以理解为：argv = **arg**ument **v**alues，尽管其正确名称是“argument vectors”）。尽管 argv 的声明看起来令人望而生畏，但 argv 实际上只是一个 C 风格的 char 指针数组（每个指针都指向一个 C 风格字符串）。此数组的长度是 argc。
让我们编写一个名为“MyArgs”的短程序来打印所有命令行参数的值：
// Program: MyArgs
#include <iostream>

int main(int argc, char* argv[])
{
    std::cout << "There are " << argc << " arguments:\n";

    // Loop through each argument and print its number and value
    for (int count{ 0 }; count < argc; ++count)
    {
        std::cout << count << ' ' << argv[count] << '\n';
    }

    return 0;
}
现在，当我们用命令行参数“Myfile.txt”和“100”调用此程序 (MyArgs) 时，输出将如下所示：
There are 3 arguments:
0 C:\MyArgs
1 Myfile.txt
2 100
参数 0 是当前正在运行的程序的路径和名称。本例中的参数 1 和 2 是我们传入的两个命令行参数。
请注意，我们不能使用基于范围的 for 循环迭代 `argv`，因为基于范围的 for 循环不适用于退化的 C 风格数组。
处理数字参数
命令行参数总是以字符串形式传递，即使提供的值本质上是数字。要将命令行参数用作数字，你必须将其从字符串转换为数字。不幸的是，C++ 使这比应有的难度更大。
C++ 的做法如下：
#include <iostream>
#include <sstream> // for std::stringstream
#include <string>

int main(int argc, char* argv[])
{
	if (argc <= 1)
	{
		// On some operating systems, argv[0] can end up as an empty string instead of the program's name.
		// We'll conditionalize our response on whether argv[0] is empty or not.
		if (argv[0])
			std::cout << "Usage: " << argv[0] << " <number>" << '\n';
		else
			std::cout << "Usage: <program name> <number>" << '\n';
            
		return 1;
	}

	std::stringstream convert{ argv[1] }; // set up a stringstream variable named convert, initialized with the input from argv[1]

	int myint{};
	if (!(convert >> myint)) // do the conversion
		myint = 0; // if conversion fails, set myint to a default value

	std::cout << "Got integer: " << myint << '\n';

	return 0;
}
当输入为“567”时，此程序打印：
Got integer: 567
std::stringstream 的工作方式与 std::cin 非常相似。在这种情况下，我们用 argv[1] 的值对其进行初始化，以便我们可以使用运算符>>将值提取到整数变量（与 std::cin 相同）。
我们将在未来的章节中更详细地讨论 std::stringstream。
操作系统首先解析命令行参数
当你在命令行输入内容（或从 IDE 运行程序）时，操作系统负责翻译和路由该请求。这不仅包括运行可执行文件，还包括解析任何参数以确定如何处理并将它们传递给应用程序。
通常，操作系统对于双引号和反斜杠等特殊字符有特殊的处理规则。
例如
MyArgs Hello world!
打印：
There are 3 arguments:
0 C:\MyArgs
1 Hello
2 world!
通常，用双引号括起来的字符串被认为是同一字符串的一部分：
MyArgs "Hello world!"
打印：
There are 2 arguments:
0 C:\MyArgs
1 Hello world!
大多数操作系统都允许你通过反斜杠引用双引号来包含文字双引号：
MyArgs \"Hello world!\"
打印：
There are 3 arguments:
0 C:\MyArgs
1 "Hello
2 world!"
其他字符也可能需要反斜杠或转义，具体取决于你的操作系统如何解释它们。
总结
命令行参数为用户或其他程序在启动时将输入数据传递到程序中提供了一种很好的方式。考虑将程序在启动时运行所需的任何输入数据作为命令行参数。如果未传入命令行，你总是可以检测到并要求用户输入。这样，你的程序就可以以两种方式运行。
下一课
20.5
省略号（以及为何要避免使用它们）
返回目录
上一课
20.3
递归