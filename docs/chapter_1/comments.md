# 1.2 — 注释

1.2 — 注释
Alex
2007 年 5 月 30 日，下午 4:17 PDT
2025 年 3 月 19 日
注释
是直接插入到程序源代码中的可供程序员阅读的笔记。注释会被编译器忽略，仅供程序员使用。
在 C++ 中有两种不同风格的注释，它们都具有相同的目的：帮助程序员以某种方式记录代码。
单行注释
//
符号开始一个 C++ 单行注释，它告诉编译器忽略从
//
符号到行尾的所有内容。例如
std::cout << "Hello world!"; // Everything from here to the end of the line is ignored
通常，单行注释用于对单行代码进行快速注释。
std::cout << "Hello world!\n"; // std::cout lives in the iostream library
std::cout << "It is very nice to meet you!\n"; // these comments make the code hard to read
std::cout << "Yeah!\n"; // especially when lines are different lengths
在行右侧添加注释可能会使代码和注释都难以阅读，尤其是在行很长的情况下。如果行相当短，注释可以简单地对齐（通常是对齐到制表位），如下所示
std::cout << "Hello world!\n";                 // std::cout lives in the iostream library
std::cout << "It is very nice to meet you!\n"; // this is much easier to read
std::cout << "Yeah!\n";                        // don't you think so?
但是，如果行很长，将注释放在右侧会使你的行变得非常长。在这种情况下，单行注释通常放在它所注释的行的上方
// std::cout lives in the iostream library
std::cout << "Hello world!\n";

// this is much easier to read
std::cout << "It is very nice to meet you!\n";

// don't you think so?
std::cout << "Yeah!\n";
作者注
在本教程系列中，我们的示例属于以下类别之一
完整的程序（包含
main()
函数的程序）。这些程序已准备好进行编译和运行。
代码片段（小段代码），例如上述语句。我们使用它们以简洁的方式演示特定概念。
我们不打算让你编译代码片段。但是如果你想这样做，你需要将它们变成一个完整的程序。通常，该程序将如下所示
#include <iostream>

int main()
{
    // Replace this line with the snippet(s) of code you'd like to compile

    return 0;
}
多行注释
/*
和
*/
符号对表示 C 风格的多行注释。符号之间的所有内容都将被忽略。
/* This is a multi-line comment.
   This line will be ignored.
   So will this one. */
由于符号之间的所有内容都被忽略，你有时会看到程序员“美化”他们的多行注释
/* This is a multi-line comment.
 * the matching asterisks to the left
 * can make this easier to read
 */
多行风格的注释不能嵌套。因此，以下代码将产生意想不到的结果
/* This is a multi-line /* comment */ this is not inside the comment */
// The above comment ends at the first */, not the second */
当编译器尝试编译这段代码时，它会忽略从第一个
/*
到第一个
*/
的所有内容。由于
this is not inside the comment */
不被视为注释的一部分，编译器会尝试编译它。这必然会导致编译错误。
这是语法高亮器非常有用的一个地方，因为注释的不同颜色应该清楚地表明哪些是注释的一部分，哪些不是。
警告
不要在其他多行注释中使用多行注释。在多行注释中包含单行注释是可以的。
注释的正确使用
通常，注释应用于三件事。首先，对于给定的库、程序或函数，注释最好用于描述该库、程序或函数
做什么
。这些通常放在文件或库的顶部，或紧邻函数之前。例如
// This program calculates the student's final grade based on their test and homework scores.
// This function uses Newton's method to approximate the root of a given equation.
// The following lines generate a random item based on rarity, level, and a weight factor.
所有这些注释让读者很好地了解库、程序或函数试图完成什么，而无需查看实际代码。用户（可能是其他人，或者如果你正在尝试重用以前编写的代码）可以一目了然地判断代码是否与他或她试图完成的任务相关。这在团队合作时尤其重要，因为并非每个人都熟悉所有代码。
其次，在上述库、程序或函数
内部
，注释可用于描述代码将
如何
实现其目标。
/* To calculate the final grade, we sum all the weighted midterm and homework scores
    and then divide by the number of scores to assign a percentage, which is
    used to calculate a letter grade. */
// To generate a random item, we're going to do the following:
// 1) Put all of the items of the desired rarity on a list
// 2) Calculate a probability for each item based on level and weight factor
// 3) Choose a random number
// 4) Figure out which item that random number corresponds to
// 5) Return the appropriate item
这些注释让用户了解代码将如何实现其目标，而无需理解每行代码的作用。
第三，在语句级别，注释应该用于描述代码
为什么
这样做。一个糟糕的语句注释解释了代码在
做什么
。如果你编写的代码如此复杂，以至于需要注释来解释一个语句在
做什么
，你可能需要重写你的语句，而不是注释它。
以下是一些糟糕的行注释和好的语句注释的示例。
糟糕的注释
// Set sight range to 0
sight = 0;
原因：通过查看语句，我们已经可以看到 sight 被设置为 0
好的注释
// The player just drank a potion of blindness and can not see anything
sight = 0;
原因：现在我们知道为什么玩家的视野被设置为 0 了
糟糕的注释
// Calculate the cost of the items
cost = quantity * 2 * storePrice;
原因：我们可以看到这是一个成本计算，但为什么数量要乘以 2 呢？
好的注释
// We need to multiply quantity by 2 here because they are bought in pairs
cost = quantity * 2 * storePrice;
原因：现在我们知道为什么这个公式是合理的了。
程序员经常不得不在以一种方式解决问题和以另一种方式解决问题之间做出艰难的决定。注释是提醒自己（或告诉别人）你做出某个决定而不是另一个决定的原因的好方法。
好的注释
// We decided to use a linked list instead of an array because
// arrays do insertion too slowly.
// We're going to use Newton's method to find the root of a number because
// there is no deterministic way to solve these equations.
最后，注释的编写方式应该让对代码一无所知的人也能理解。程序员经常会说：“这很明显！我绝不会忘记这一点。” 你猜怎么着？这
不
明显，你
会
惊讶于你忘记的速度有多快。:) 你（或其他人）以后会感谢你用人类语言写下了代码的“什么”、“如何”和“为什么”。阅读单独的代码行很容易。理解它们旨在实现的目标则不然。
相关内容
我们在课程
1.7 — 关键字和命名标识符
中讨论变量声明语句的注释。
最佳实践
慷慨地注释你的代码，并像对一个对代码一无所知的人说话一样编写你的注释。不要假设你会记住你做出特定选择的原因。
作者注
在本教程系列的其余部分，我们将在代码块中使用注释来吸引你对特定事物的注意，或帮助说明事物如何工作（同时确保程序仍然可以编译）。敏锐的读者会注意到，按照上述标准，这些注释中的大多数都很糟糕。:) 在阅读其余教程时，请记住这些注释是出于有意的教育目的，而不是试图演示好的注释是什么样子的。
题外话…
Doxygen 等文档生成程序旨在以各种方式帮助生成和利用文档。除其他外，它们可以：
帮助标准化代码的文档方式。
生成图表、可视化和交叉链接，使理解代码结构更容易。
将文档导出为其他格式（例如 HTML），以便轻松与他人共享（例如其他团队成员或正在集成你所写内容的开发人员）。
你在学习语言时不需要这些，但你将来可能会遇到它们或发现它们有用，尤其是在专业环境中。
注释掉代码
将一行或多行代码转换为注释称为
注释掉
你的代码。这提供了一种方便的方法来（临时）排除部分代码，使其不包含在编译后的程序中。
要注释掉单行代码，只需使用 // 风格的注释暂时将一行代码变成注释
未注释掉
std::cout << 1;
已注释掉
//    std::cout << 1;
要注释掉一个代码块，可以在多行代码上使用 //，或者使用 /* */ 风格的注释暂时将代码块变成注释。
未注释掉
std::cout << 1;
    std::cout << 2;
    std::cout << 3;
已注释掉
//    std::cout << 1;
//    std::cout << 2;
//    std::cout << 3;
或
/*
    std::cout << 1;
    std::cout << 2;
    std::cout << 3;
*/
你可能希望这样做有很多原因
你正在编写一段新代码，但它尚未编译，你需要运行程序。如果存在编译错误，编译器将不允许你编译代码。注释掉无法编译的代码将允许程序编译，以便你可以运行它。准备好后，你可以取消注释代码，然后继续对其进行处理。
你编写了新代码，它能编译但无法正常工作，而你暂时没有时间修复它。注释掉损坏的代码将确保在你能修复它之前，损坏的代码不会执行并导致问题。
查找错误来源。如果程序没有产生预期结果（或崩溃），有时禁用部分代码以查看是否可以隔离导致其无法正常工作的原因会很有用。如果你注释掉一行或多行代码，并且你的程序开始按预期工作（或停止崩溃），那么你最后注释掉的代码很可能是问题的一部分。然后你可以调查这些代码行为什么会导致问题。
你想用一段新代码替换一段代码。与其直接删除原始代码，不如将其注释掉并保留在那里作为参考，直到你确定新代码正常工作。一旦你确定新代码正常工作，你就可以删除旧的注释掉的代码。如果你无法让新代码工作，你总能删除新代码并取消注释旧代码，以恢复到以前的状态。
在开发过程中，注释掉代码是很常见的事情，因此许多 IDE 都支持注释掉高亮显示的代码部分。访问此功能的方式因 IDE 而异。
对于 Visual Studio 用户
你可以通过“编辑”菜单 >“高级”>“注释选择”（或“取消注释选择”）来注释或取消注释选定内容。
对于 Code::Blocks 用户
你可以通过“编辑”菜单 >“注释”（或“取消注释”，或“切换注释”，或任何其他注释工具）来注释或取消注释选定内容。
对于 VS Code 用户
你可以通过按 Ctrl-/ 来注释或取消注释选定内容。
提示
如果你总是使用单行注释作为你的普通注释，那么你总是可以使用多行注释来注释掉你的代码而不会发生冲突。如果你使用多行注释来记录你的代码，那么使用注释来注释掉代码可能会变得更具挑战性。
如果你确实需要注释掉包含多行注释的代码块，你还可以考虑使用
#if 0
预处理器指令，我们在课程
2.10 — 预处理器简介
中讨论过。
总结
在库、程序或函数级别，使用注释描述
做什么
。
在库、程序或函数内部，使用注释描述
如何
。
在语句级别，使用注释描述
为什么
。
下一课
1.3
对象和变量简介
返回目录
上一课
1.1
语句和程序结构