# 3.5 — 更多调试策略

3.5 — 更多调试策略
Alex
2019 年 2 月 1 日，太平洋标准时间上午 11:57
2024 年 8 月 26 日
在上一节（
3.4 -- 基本调试策略
）中，我们开始探索如何手动调试问题。在那一节中，我们对使用语句打印调试文本提出了一些批评
调试语句会使您的代码变得混乱。
调试语句会使您的程序输出变得混乱。
调试语句需要修改您的代码才能添加和删除，这可能会引入新的错误。
调试语句在您使用完毕后必须删除，这使得它们不可重用。
我们可以缓解其中一些问题。在本节中，我们将探讨一些实现此目的的基本技术。
条件化您的调试代码
考虑以下包含一些调试语句的程序
#include <iostream>
 
int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}
 
int main()
{
std::cerr << "main() called\n";
    int x{ getUserInput() };
    std::cout << "You entered: " << x << '\n';
 
    return 0;
}
当您使用完调试语句时，您需要将其删除或注释掉。然后，如果您以后再次需要它们，您必须将其添加回来或取消注释。
一种使在程序中禁用和启用调试变得更容易的方法是使用预处理器指令使您的调试语句具有条件性
#include <iostream>
 
#define ENABLE_DEBUG // comment out to disable debugging

int getUserInput()
{
#ifdef ENABLE_DEBUG
std::cerr << "getUserInput() called\n";
#endif
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}
 
int main()
{
#ifdef ENABLE_DEBUG
std::cerr << "main() called\n";
#endif
    int x{ getUserInput() };
    std::cout << "You entered: " << x << '\n';
 
    return 0;
}
现在，我们只需注释/取消注释
#define ENABLE_DEBUG
即可启用调试。这使我们能够重用以前添加的调试语句，然后在我们使用完毕后禁用它们，而不是实际从代码中删除它们。如果这是一个多文件程序，#define ENABLE_DEBUG 将放在一个头文件中，该头文件包含在所有代码文件中，这样我们就可以在单个位置注释/取消注释 #define，并使其传播到所有代码文件。
这解决了必须删除调试语句及其风险的问题，但代价是代码更加混乱。这种方法的另一个缺点是，如果您打字错误（例如拼错“DEBUG”）或忘记将头文件包含到代码文件中，该文件的部分或全部调试可能无法启用。因此，尽管这比无条件版本更好，但仍有改进空间。
使用日志记录器
通过预处理器进行条件调试的替代方法是将您的调试信息发送到日志。
日志
是对已发生的事件的顺序记录，通常带有时间戳。生成日志的过程称为
日志记录
。通常，日志写入磁盘上的文件（称为
日志文件
），以便以后可以查看。大多数应用程序和操作系统都会写入日志文件，可用于帮助诊断发生的问题。
日志文件有一些优点。由于写入日志文件的信息与程序的输出分开，因此您可以避免将正常输出和调试输出混合在一起造成的混乱。日志文件也可以轻松地发送给其他人进行诊断——因此，如果使用您的软件的人遇到问题，您可以要求他们将日志文件发送给您，这可能会帮助您找到问题所在。
C++ 包含一个名为
std::clog
的输出流，旨在用于写入日志信息。但是，默认情况下，
std::clog
写入标准错误流（与
std::cerr
相同）。虽然您可以将其重定向到文件，但这是一个您通常最好使用许多现有第三方日志记录工具的领域。使用哪个由您决定。
为了说明目的，我们将展示使用
plog
日志记录器输出到日志记录器的样子。Plog 实现为一组头文件，因此您可以轻松地将其包含在任何需要的地方，并且它轻巧且易于使用。
#include <plog/Log.h> // Step 1: include the logger headers
#include <plog/Initializers/RollingFileInitializer.h>
#include <iostream>

int getUserInput()
{
	PLOGD << "getUserInput() called"; // PLOGD is defined by the plog library

	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	plog::init(plog::debug, "Logfile.txt"); // Step 2: initialize the logger

	PLOGD << "main() called"; // Step 3: Output to the log as if you were writing to the console

	int x{ getUserInput() };
	std::cout << "You entered: " << x << '\n';

	return 0;
}
这是来自上述日志记录器的输出（在
Logfile.txt
文件中）
2018-12-26 20:03:33.295 DEBUG [4752] [main@19] main() called
2018-12-26 20:03:33.296 DEBUG [4752] [getUserInput@7] getUserInput() called
您包含、初始化和使用日志记录器的方式将根据您选择的特定日志记录器而异。
请注意，使用此方法也不需要条件编译指令，因为大多数日志记录器都有减少/消除向日志写入输出的方法。这使得代码更易于阅读，因为条件编译行会增加大量混乱。使用 plog，可以通过将 init 语句更改为以下内容来暂时禁用日志记录
plog::init(plog::none , "Logfile.txt"); // plog::none eliminates writing of most messages, essentially turning logging off
我们将来不会在任何课程中使用 plog，所以您不必担心学习它。
题外话…
如果您想自己编译上述示例，或在您自己的项目中使用 plog，您可以按照以下说明安装它
首先，获取最新的 plog 版本
访问
plog
存储库。
单击右上角的绿色代码按钮，然后选择“下载 zip”
接下来，将整个存档解压缩到硬盘上的
某个位置
。
最后，对于每个项目，将
某个位置\plog-master\include\
目录设置为 IDE 中的
include directory
。有关如何在 Visual Studio 中执行此操作的说明在此处：
A.2 -- 在 Visual Studio 中使用库
，Code::Blocks 在此处：
A.3 -- 在 Code::Blocks 中使用库
。由于 plog 没有预编译库文件，您可以跳过与预编译库文件相关的部分。
日志文件通常会在您的可执行文件所在的目录中创建。
提示
在大型或对性能敏感的项目中，可能更喜欢更快、功能更丰富的日志记录器，例如
spdlog
。
下一课
3.6
使用集成调试器：步进
返回目录
上一课
3.4
基本调试策略