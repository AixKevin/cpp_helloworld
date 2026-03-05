# 2.8 — 包含多个代码文件的程序

2.8 — 包含多个代码文件的程序
Alex
2007 年 6 月 2 日，下午 8:26 PDT
2025 年 2 月 11 日
向项目中添加文件
随着程序变得越来越大，通常会为了组织或重用目的将其拆分为多个文件。使用 IDE 的一个优点是它们使处理多个文件变得更加容易。您已经知道如何创建和编译单文件项目。向现有项目添加新文件非常容易。
最佳实践
当您向项目中添加新的代码文件时，请给它们 `.cpp` 扩展名。
对于 Visual Studio 用户
在 Visual Studio 中，右键单击解决方案资源管理器窗口中的“源文件”文件夹（或项目名称），然后选择“添加 > 新建项…”。
确保选择了“C++ 文件 (.cpp)”。给新文件命名，它将被添加到您的项目中。
注意：您的 Visual Studio 可能会选择显示紧凑视图而不是上面显示完整视图。您可以使用紧凑视图，或者单击“显示所有模板”以获取完整视图。
注意：如果您从“文件”菜单而不是从解决方案资源管理器中的项目创建新文件，则新文件将不会自动添加到您的项目中。您必须手动将其添加到项目中。为此，右键单击“解决方案资源管理器”中的“源文件”，选择“添加 > 现有项”，然后选择您的文件。
现在当您编译程序时，您应该会看到编译器在编译时列出文件的名称。
对于 Code::Blocks 用户
在 Code::Blocks 中，转到“文件”菜单并选择“新建 > 文件…”。
在“从模板新建”对话框中，选择“C/C++ source”并单击“Go”。
此时您可能会或可能不会看到一个“欢迎使用 C/C++ 源文件向导”对话框。如果看到了，请单击“下一步”。
在向导的下一页，选择“C++”并单击“下一步”。
现在为新文件命名（不要忘记 .cpp 扩展名），然后单击“全部”按钮以确保选择了所有构建目标。最后，选择“完成”。
现在当您编译程序时，您应该会看到编译器在编译时列出文件的名称。
对于 gcc 用户
从命令行，您可以使用您喜欢的编辑器自行创建附加文件，并为其命名。当您编译程序时，您需要将所有相关的代码文件包含在编译行中。例如：`g++ main.cpp add.cpp -o main`，其中 `main.cpp` 和 `add.cpp` 是您的代码文件的名称，`main` 是输出文件的名称。
对于 VS Code 用户
要创建新文件，请从顶部导航中选择“视图 > 资源管理器”以打开资源管理器窗格，然后单击项目名称右侧的“新建文件”图标。或者，从顶部导航中选择“文件 > 新建文件”。然后给您的新文件命名（不要忘记 .cpp 扩展名）。如果文件出现在 `.vscode` 文件夹中，将其向上拖动一级到项目文件夹。
接下来打开 `tasks.json` 文件，找到行 `"${file}",`。
您这里有两个选项
如果您希望明确要编译哪些文件，请将 `"${file}",` 替换为您希望编译的每个文件的名称，每行一个，如下所示
"main.cpp",
"add.cpp",
读者“geo”报告说，您可以通过将 `"${file}",` 替换为 `"${fileDirname}\\**.cpp"`（在 Windows 上）来让 VS Code 自动编译目录中的所有 .cpp 文件。
读者“Orb”报告说 `"${fileDirname}/**.cpp"` 在 Unix 上有效。
多文件示例
在
2.7 -- 前向声明与定义
课程中，我们看了一个无法编译的单文件程序
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}

int add(int x, int y)
{
    return x + y;
}
当编译器在 `main` 的第 5 行到达对 `add` 的函数调用时，它不知道 `add` 是什么，因为我们直到第 9 行才定义 `add`！我们的解决方案是重新排序函数（将 `add` 放在前面）或为 `add` 使用前向声明。
现在让我们看一个类似的多文件程序
add.cpp
int add(int x, int y)
{
    return x + y;
}
main.cpp
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n'; // compile error
    return 0;
}
您的编译器可能会首先编译 `add.cpp` 或 `main.cpp`。无论哪种方式，`main.cpp` 都将无法编译，并给出与上一个示例相同的编译器错误
main.cpp(5) : error C3861: 'add': identifier not found
原因也完全相同：当编译器到达 `main.cpp` 的第 5 行时，它不知道标识符 `add` 是什么。
请记住，编译器会单独编译每个文件。它不知道其他代码文件的内容，也不会记住它从先前编译的代码文件中看到的任何内容。因此，即使编译器可能以前见过函数 `add` 的定义（如果它首先编译了 `add.cpp`），它也不会记住。
这种有限的可见性和短期记忆是故意的，原因有几个
它允许项目的源文件以任何顺序编译。
当我们更改源文件时，只需要重新编译该源文件。
它减少了不同文件中标识符之间命名冲突的可能性。
我们将在下一课中探讨名称冲突时会发生什么（
2.9 -- 命名冲突与命名空间简介
）。
我们这里的解决方案选项与之前相同：将函数 `add` 的定义放在函数 `main` 之前，或者使用前向声明来满足编译器。在这种情况下，因为函数 `add` 在另一个文件中，所以重新排序选项是不可能的。
这里的解决方案是使用前向声明
main.cpp（带前向声明）
#include <iostream>

int add(int x, int y); // needed so main.cpp knows that add() is a function defined elsewhere

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}
add.cpp（保持不变）
int add(int x, int y)
{
    return x + y;
}
现在，当编译器编译 `main.cpp` 时，它会知道标识符 `add` 是什么并感到满意。链接器会将 `main.cpp` 中对 `add` 的函数调用连接到 `add.cpp` 中函数 `add` 的定义。
使用这种方法，我们可以让文件访问存在于另一个文件中的函数。
尝试自己编译 `add.cpp` 和带有前向声明的 `main.cpp`。如果出现链接器错误，请确保您已正确将 `add.cpp` 添加到您的项目或编译行中。
提示
因为编译器单独编译每个代码文件（然后忘记它所看到的内容），所以每个使用 `std::cout` 或 `std::cin` 的代码文件都需要 `#include
`。
在上面的例子中，如果 `add.cpp` 使用了 `std::cout` 或 `std::cin`，它就需要 `#include
`。
关键见解
当标识符在表达式中使用时，该标识符必须连接到其定义。
如果编译器在正在编译的文件中既没有看到标识符的前向声明也没有看到定义，它将在使用标识符的地方报错。
否则，如果同一文件中存在定义，编译器会将标识符的使用连接到其定义。
否则，如果定义存在于不同的文件中（并且对链接器可见），链接器会将标识符的使用连接到其定义。
否则，链接器将发出一个错误，指示它找不到标识符的定义。
出错了！
第一次尝试使用多个文件时，可能会出现很多问题。如果您尝试了上面的示例并遇到错误，请检查以下内容
如果您收到关于 `main` 中未定义 `add` 的编译器错误，您可能忘记了在 `main.cpp` 中为函数 `add` 进行前向声明。
如果您收到关于 `add` 未定义的链接器错误，例如
unresolved external symbol "int __cdecl add(int,int)" (?add@@YAHHH@Z) referenced in function _main
2a. ……最可能的原因是 `add.cpp` 未正确添加到您的项目中。当您编译时，您应该看到编译器列出 `main.cpp` 和 `add.cpp`。如果您只看到 `main.cpp`，那么 `add.cpp` 肯定没有被编译。如果您使用的是 Visual Studio 或 Code::Blocks，您应该在 IDE 左侧或右侧的解决方案资源管理器/项目窗格中看到 `add.cpp`。如果没有，右键单击您的项目，添加文件，然后再次尝试编译。如果您在命令行上编译，不要忘记在编译命令中同时包含 `main.cpp` 和 `add.cpp`。
2b. ……您可能将 `add.cpp` 添加到了错误的项目中。
2c. ……文件可能设置为不编译或不链接。检查文件属性，确保文件配置为编译/链接。在 Code::Blocks 中，编译和链接是应该勾选的单独复选框。在 Visual Studio 中，有一个“从构建中排除”选项，应设置为“否”或留空。确保单独检查每个构建配置（例如调试和发布）。
不要从 `main.cpp` 中 `#include "add.cpp"`。虽然在这种情况下这样做可以编译，但 `#include` .cpp 文件会增加命名冲突和其他意外后果的风险（特别是当程序变得更大更复杂时）。我们将在
2.10 -- 预处理器简介
课程中进一步讨论 `#include`。
总结
C++ 的设计使得每个源文件都可以独立编译，而无需了解其他文件中的内容。因此，文件实际编译的顺序无关紧要。
一旦我们进入面向对象编程，我们将大量使用多个文件，所以现在是确保您了解如何添加和编译多个文件项目的好时机。
提醒：每当您创建新的代码 (.cpp) 文件时，您都需要将其添加到您的项目中，以便它被编译。
小测验时间
问题 #1
将以下程序拆分为两个文件（main.cpp 和 input.cpp）。main.cpp 应该包含 main 函数，input.cpp 应该包含 getInteger 函数。
显示提示
提示：不要忘记您需要在 main.cpp 中为函数 getInteger() 进行前向声明。
#include <iostream>

int getInteger()
{
	std::cout << "Enter an integer: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getInteger() };
	int y{ getInteger() };

	std::cout << x << " + " << y << " is " << x + y << '\n';
	return 0;
}
显示答案
input.cpp
#include <iostream> // we need iostream since we use it in this file

int getInteger()
{
	std::cout << "Enter an integer: ";
	int x{};
	std::cin >> x;
	return x;
}
main.cpp
#include <iostream> // we need iostream here too since we use it in this file as well

int getInteger(); // forward declaration for function getInteger

int main()
{
	int x{ getInteger() };
	int y{ getInteger() };

	std::cout << x << " + " << y << " is " << x + y << '\n';
	return 0;
}
如果您收到链接器关于 `getInteger()` 未定义引用的错误，那么您可能忘记编译 `input.cpp`。
下一课
2.9
命名冲突与命名空间简介
返回目录
上一课
2.7
前向声明与定义