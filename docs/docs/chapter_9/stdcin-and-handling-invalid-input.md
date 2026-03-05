# 9.5 — std::cin 和处理无效输入

9.5 — std::cin 和处理无效输入
Alex
2016 年 4 月 21 日，太平洋夏令时下午 1:01
2025 年 1 月 29 日
大多数具有某种用户界面的程序都需要处理用户输入。在您一直在编写的程序中，您一直使用 `std::cin` 来要求用户输入文本。由于文本输入非常自由（用户可以输入任何内容），用户很容易输入意外的输入。
在编写程序时，您应该始终考虑用户将如何（无意或有心）滥用您的程序。一个编写良好的程序将预测用户将如何滥用它，并优雅地处理这些情况或（如果可能）从一开始就阻止它们发生。一个能够很好地处理错误情况的程序被称为**健壮**的。
在本课程中，我们将专门探讨用户通过 `std::cin` 输入无效文本输入的方式，并向您展示处理这些情况的不同方法。
在我们讨论 `std::cin` 和 `operator>>` 如何失败之前，让我们回顾一下它们的工作原理。我们在第
1.5 课 -- iostream 简介：cout、cin 和 endl
中讨论了这些内容。
以下是 `operator>>` 用于输入的简化视图
首先，前导空格（缓冲区开头的空格、制表符和换行符）将从输入缓冲区中丢弃。这将丢弃先前输入行中剩余的任何未提取的换行符。
如果输入缓冲区现在为空，`operator>>` 将等待用户输入更多数据。前导空格再次被丢弃。
`operator>>` 然后提取尽可能多的连续字符，直到遇到换行符（表示输入行的末尾）或对要提取到的变量无效的字符。
提取结果如下
如果在上面的第 3 步中提取了任何字符，则提取成功。提取的字符将被转换为一个值，然后分配给变量。
如果在上面的第 3 步中没有提取任何字符，则提取失败。要提取到的对象被赋值为 `0`（从 C++11 开始），并且任何未来的提取将立即失败（直到 `std::cin` 被清除）。
验证输入
检查用户输入是否符合程序预期要求的过程称为**输入验证**。
输入验证有三种基本方法
内联（用户输入时）
从一开始就阻止用户输入无效输入。
输入后（用户输入后）
让用户将他们想要的任何内容输入到字符串中，然后验证字符串是否正确，如果是，则将字符串转换为最终的变量格式。
让用户输入他们想要的任何内容，让 `std::cin` 和 `operator>>` 尝试提取，并处理错误情况。
一些图形用户界面和高级文本界面将允许您在用户输入时（逐个字符）验证输入。一般来说，程序员提供一个验证函数，该函数接受用户目前已输入的输入，如果输入有效则返回 `true`，否则返回 `false`。每次用户按下按键时都会调用此函数。如果验证函数返回 `true`，则接受用户刚刚按下的按键。如果验证函数返回 `false`，则丢弃用户刚刚输入的字符（并且不在屏幕上显示）。使用此方法，您可以确保用户输入的任何输入都保证有效，因为任何无效的击键都会立即被发现并丢弃。不幸的是，`std::cin` 不支持这种验证方式。
由于字符串对可以输入的字符没有任何限制，因此提取保证成功（但请记住 `std::cin` 在第一个非前导空格字符处停止提取）。一旦输入字符串，程序就可以解析字符串以查看其是否有效。然而，解析字符串并将字符串输入转换为其他类型（例如数字）可能具有挑战性，因此这只在极少数情况下进行。
最常见的情况是，我们让 `std::cin` 和提取运算符完成繁重的工作。在这种方法下，我们让用户输入他们想要的任何内容，让 `std::cin` 和 `operator>>` 尝试提取它，并在失败时处理后果。这是最简单的方法，也是我们将在下面更多讨论的方法。
示例程序
考虑以下没有错误处理的计算器程序
#include <iostream>
 
double getDouble()
{
    std::cout << "Enter a decimal number: ";
    double x{};
    std::cin >> x;
    return x;
}
 
char getOperator()
{
    std::cout << "Enter one of the following: +, -, *, or /: ";
    char op{};
    std::cin >> op;
    return op;
}
 
void printResult(double x, char operation, double y)
{
    std::cout << x << ' ' << operation << ' ' << y << " is ";

    switch (operation)
    {
    case '+':
        std::cout << x + y << '\n';
        return;
    case '-':
        std::cout << x - y << '\n';
        return;
    case '*':
        std::cout << x * y << '\n';
        return;
    case '/':
        std::cout << x / y << '\n';
        return;
    }
}
 
int main()
{
    double x{ getDouble() };
    char operation{ getOperator() };
    double y{ getDouble() };

    printResult(x, operation, y);
 
    return 0;
}
这个简单的程序要求用户输入两个数字和一个数学运算符。
Enter a decimal number: 5
Enter one of the following: +, -, *, or /: *
Enter a decimal number: 7
5 * 7 is 35
现在，考虑无效的用户输入可能会破坏此程序的哪些地方。
首先，我们要求用户输入一些数字。如果他们输入数字以外的内容（例如 'q'）怎么办？在这种情况下，提取将失败。
其次，我们要求用户输入四个可能符号中的一个。如果他们输入我们预期的符号之外的字符怎么办？我们将能够提取输入，但我们目前不处理之后发生的情况。
第三，如果我们要求用户输入一个符号，而他们输入一个字符串，如 `"*q hello"`，怎么办？尽管我们可以提取我们需要的 `*` 字符，但缓冲区中还有额外的输入，可能会在以后引起问题。
无效文本输入的类型
我们通常可以将输入文本错误分为四种类型
输入提取成功，但输入对程序没有意义（例如，输入 'k' 作为您的数学运算符）。
输入提取成功，但用户输入了额外内容（例如，输入 `*q hello` 作为您的数学运算符）。
输入提取失败（例如，尝试将 'q' 输入到数字输入中）。
输入提取成功，但用户使数字值溢出。
因此，为了使我们的程序健壮，每当我们要求用户输入时，理想情况下我们应该确定上述每种情况是否可能发生，如果可能，则编写代码来处理这些情况。
让我们深入探讨这些情况，以及如何使用 `std::cin` 处理它们。
错误情况 1：提取成功但输入无意义
这是最简单的情况。考虑上述程序的以下执行
Enter a decimal number: 5
Enter one of the following: +, -, *, or /: k
Enter a decimal number: 7
在这种情况下，我们要求用户输入四个符号中的一个，但他们输入了 'k'。'k' 是一个有效字符，因此 `std::cin` 愉快地将其提取到变量 `op` 中，并将其返回到 `main`。但我们的程序没有预料到这种情况会发生，因此它没有正确处理这种情况。结果，它输出
5 k 7 is
这里的解决方案很简单：进行输入验证。这通常包括 3 个步骤
检查用户的输入是否符合您的预期。
如果是，将值返回给调用者。
如果不是，告诉用户出了问题，让他们再试一次。
以下是更新后的 `getOperator()` 函数，它进行了输入验证。
char getOperator()
{
    while (true) // Loop until user enters a valid input
    {
        std::cout << "Enter one of the following: +, -, *, or /: ";
        char operation{};
        std::cin >> operation;

        // Check whether the user entered meaningful input
        switch (operation)
        {
        case '+':
        case '-':
        case '*':
        case '/':
            return operation; // return it to the caller
        default: // otherwise tell the user what went wrong
            std::cout << "Oops, that input is invalid.  Please try again.\n";
        }
    } // and try again
}
如您所见，我们正在使用 `while` 循环不断循环，直到用户提供有效输入。如果他们不这样做，我们要求他们再试一次，直到他们给我们有效输入，关闭程序，或者破坏他们的计算机。
错误情况 2：提取成功但存在多余输入
考虑上述程序的以下执行
Enter a decimal number: 5*7
你认为接下来会发生什么？
Enter a decimal number: 5*7
Enter one of the following: +, -, *, or /: Enter a decimal number: 5 * 7 is 35
程序打印了正确的答案，但格式完全混乱了。让我们仔细看看原因。
当用户输入 `5*7` 时，该输入进入缓冲区。然后 `operator>>` 将 5 提取到变量 x，在缓冲区中留下 `*7\n`。接下来，程序打印“请输入以下之一：+、-、* 或 /:”。然而，当调用提取运算符时，它看到 `*7\n` 在缓冲区中等待提取，因此它使用该内容而不是要求用户输入更多内容。因此，它提取了 '*' 字符，在缓冲区中留下 `7\n`。
在要求用户输入另一个十进制数字后，缓冲区中的 `7` 在未询问用户的情况下被提取。由于用户从未有机会输入额外数据并按下 Enter 键（导致换行符），因此所有输出提示都在同一行上运行。
尽管上述程序有效，但执行过程很混乱。如果简单地忽略任何输入的多余字符会更好。幸运的是，忽略字符很简单
std::cin.ignore(100, '\n');  // clear up to 100 characters out of the buffer, or until a '\n' character is removed
此调用最多可删除 100 个字符，但如果用户输入超过 100 个字符，我们将再次得到混乱的输出。要忽略所有字符直到下一个“\n”，我们可以将 `std::numeric_limits
::max()` 传递给 `std::cin.ignore()`。`std::numeric_limits
::max()` 返回可以存储在 `std::streamsize` 类型变量中的最大值。将此值传递给 `std::cin.ignore()` 会使其禁用计数检查。
要忽略所有内容，直到并包括下一个“\n”字符，我们调用
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
因为这行代码很长，所以把它封装在一个函数中会很方便，可以代替 `std::cin.ignore()` 调用。
#include <limits> // for std::numeric_limits

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}
由于用户输入的最后一个字符通常是“\n”，我们可以告诉 `std::cin` 忽略缓冲字符，直到它找到一个换行符（该换行符也会被删除）。
让我们更新我们的 `getDouble()` 函数，以忽略任何多余的输入
double getDouble()
{
    std::cout << "Enter a decimal number: ";
    double x{};
    std::cin >> x;

    ignoreLine();
    return x;
}
现在我们的程序将按预期工作，即使我们为第一个输入输入 `5*7` —— 5 将被提取，其余字符将从输入缓冲区中删除。由于输入缓冲区现在为空，因此下次执行提取操作时，将正确要求用户输入！
提示
在某些情况下，最好将多余的输入视为失败情况（而不是简单地忽略它）。然后我们可以要求用户重新输入他们的输入。
以下是 `getDouble()` 的变体，如果存在任何多余的输入，它会要求用户重新输入他们的输入
// returns true if std::cin has unextracted input on the current line, false otherwise
bool hasUnextractedInput()
{
    return !std::cin.eof() && std::cin.peek() != '\n';
}

double getDouble()
{
    while (true) // Loop until user enters a valid input
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        // NOTE: YOU SHOULD CHECK FOR A FAILED EXTRACTION HERE (see section below)

        // If there is extraneous input, treat as failure case
        if (hasUnextractedInput())
        {
            ignoreLine(); // remove extraneous input
            continue;
        }
    
        return x;
    }
}
上面的代码片段使用了我们以前没有见过的两个函数
`std::cin.eof()` 函数如果上次输入操作（在本例中是提取到 `x`）到达输入流的末尾，则返回 `true`。
`std::cin.peek()` 函数允许我们查看输入流中的下一个字符，而无需提取它。
此函数的工作原理如下。将用户输入提取到 `x` 后，`std::cin` 中可能存在或不存在额外的（未提取的）字符。
首先，我们调用 `std::cin.eof()` 查看提取到 `x` 是否到达了输入流的末尾。如果是，那么我们知道所有字符都已提取，这是一个成功的情况。
否则，`std::cin` 中肯定还有其他字符等待提取。在这种情况下，我们调用 `std::cin.peek()` 来查看下一个等待提取的字符，而无需实际提取它。如果下一个字符是 `'\n'`，这意味着我们已经将此输入行中的所有字符都提取到了 `x` 中。这同样也是一个成功的情况。
然而，如果下一个字符不是 `'\n'`，那么用户一定输入了多余的输入，而这些输入没有被提取到 `x` 中。这就是我们的失败情况。我们清除所有这些多余的输入，然后 `continue` 回到循环的顶部，再试一次。
如果您在理解 `hasUnextractedInput()` 中的布尔表达式如何求值时遇到困难，这并不奇怪——带有否定的布尔表达式可能难以理解。在这种情况下，使用德摩根定律可以有所帮助。一个等价的语句是 `return !(std::cin.eof() || std::cin.peek() == '\n');`。这更清楚地表明我们正在测试 EOF 或换行符。如果其中任何一个为真，那么我们已经提取了所有输入。然后我们应用 `operator!` 来告诉我们是否没有提取所有输入，这意味着仍然存在未提取的输入。
错误情况 3：提取失败
当无法将任何输入提取到指定变量时，提取失败。
现在考虑我们更新后的计算器程序的以下执行
Enter a decimal number: a
程序没有按预期执行，这不应该让您感到惊讶，但它的失败方式很有趣
Enter a decimal number: a
Enter one of the following: +, -, *, or /: Oops, that input is invalid.  Please try again.
Enter one of the following: +, -, *, or /: Oops, that input is invalid.  Please try again.
Enter one of the following: +, -, *, or /: Oops, that input is invalid.  Please try again.
最后一行一直打印，直到程序关闭。
这看起来与多余输入的情况非常相似，但又有点不同。让我们仔细看看。
当用户输入“a”时，该字符被放置在缓冲区中。然后 `operator>>` 尝试将“a”提取到 `double` 类型的变量 x 中。由于“a”无法转换为 `double`，`operator>>` 无法进行提取。此时发生两件事：“a”留在缓冲区中，并且 `std::cin` 进入“故障模式”。
一旦进入“故障模式”，未来的输入提取请求将静默失败。因此在我们的计算器程序中，输出提示仍然打印，但任何进一步的提取请求都将被忽略。这意味着我们不会等待输入操作，而是跳过输入提示，我们陷入一个无限循环，因为无法到达有效情况之一。
为了让 `std::cin` 再次正常工作，我们通常需要做三件事
检测到先前的提取失败。
将 `std::cin` 恢复到正常操作模式。
删除导致失败的输入（这样下一个提取请求就不会以相同的方式失败）。
以下是它看起来的样子
if (std::cin.fail()) // If the previous extraction failed
{
    // Let's handle the failure
    std::cin.clear(); // Put us back in 'normal' operation mode
    ignoreLine();     // And remove the bad input
}
由于 `std::cin` 具有一个布尔转换，指示上次输入是否成功，因此将上述代码写成以下形式更符合习惯
if (!std::cin) // If the previous extraction failed
{
    // Let's handle the failure
    std::cin.clear(); // Put us back in 'normal' operation mode
    ignoreLine();     // And remove the bad input
}
关键见解
一旦提取失败，未来的输入提取请求（包括对 `ignore()` 的调用）将静默失败，直到调用 `clear()` 函数。因此，在检测到提取失败后，调用 `clear()` 通常是您应该做的第一件事。
让我们把它整合到我们的 `getDouble()` 函数中
double getDouble()
{
    while (true) // Loop until user enters a valid input
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        if (!std::cin) // If the previous extraction failed
        {
            // Let's handle the failure
            std::cin.clear(); // Put us back in 'normal' operation mode
            ignoreLine();     // And remove the bad input
            continue;
        }

        // Our extraction succeeded
        ignoreLine(); // Ignore any additional input on this line
        return x;     // Return the value we extracted
    }
}
对于基本类型，由于无效输入导致的提取失败将导致变量被赋值为 `0`（或 `0` 在变量类型中转换成的任何值）。
即使提取没有失败，也可以调用 `clear()` —— 它不会做任何事情。在无论成功还是失败我们都将调用 `ignoreLine()` 的情况下，我们基本上可以将两种情况结合起来
double getDouble()
{
    while (true) // Loop until user enters a valid input
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        bool success { std::cin }; // Remember whether we had a successful extraction
        std::cin.clear();          // Put us back in 'normal' operation mode (in case we failed)
        ignoreLine();              // Ignore any additional input on this line (regardless)

        if (success)               // If we actually extracted a value
            return x;              // Return it (otherwise, we go back to top of loop)
    }
}
检查 EOF
我们还需要解决另一种情况。
文件结束（EOF）是一种特殊的错误状态，表示“没有更多数据可用”。这通常在输入操作因没有数据可用而失败**之后**生成。例如，如果您正在读取磁盘文件的内容，然后尝试在您已经到达文件末尾后读取更多数据，则会生成 EOF 以告知您没有更多数据可用。在文件输入的情况下，这不是问题——我们可以直接关闭文件并继续。
现在考虑 `std::cin`。如果我们在 `std::cin` 中尝试提取输入而没有输入，它设计上不会生成 EOF —— 它只会等待用户输入更多内容。但是，`std::cin` 在某些情况下会生成 EOF —— 最常见的是当用户为其操作系统输入特殊按键组合时。Unix（通过 ctrl-D）和 Windows（通过 ctrl-Z + ENTER）都支持从键盘输入“EOF 字符”。
关键见解
在 C++ 中，EOF 是一种错误状态，而不是一个字符。不同的操作系统有特殊的字符组合被视为“用户输入的 EOF 请求”。这些有时被称为“EOF 字符”。
当将数据提取到 `std::cin` 并且用户输入 EOF 字符时，行为是操作系统特定的。通常会发生以下情况
如果 EOF 不是输入的第一个字符：EOF 之前的所有输入都将被刷新，并且 EOF 字符被忽略。在 Windows 上，EOF 之后输入的任何字符（除了换行符）都将被忽略。
如果 EOF 是输入的第一个字符：EOF 错误将被设置。输入流可能会（或可能不会）断开连接。
虽然 `std::cin.clear()` 会清除 EOF 错误，但如果输入流已断开连接，则下一个输入请求将生成另一个 EOF 错误。当我们的输入在一个 `while(true)` 循环中时，这会产生问题，因为我们将陷入 EOF 错误的无限循环。
由于键盘输入的 `EOF` 字符的目的是终止输入流，因此最好的做法是检测 EOF（通过 `std::cin.eof()`），然后终止程序。
因为清除失败的输入流是我们可能经常检查的事情，所以这是一个可重用函数的好候选者
#include <limits> // for std::numeric_limits

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// returns true if extraction failed, false otherwise
bool clearFailedExtraction()
{
    // Check for failed extraction
    if (!std::cin) // If the previous extraction failed
    {
        if (std::cin.eof()) // If the user entered an EOF
        {
            std::exit(0); // Shut down the program now
        }

        // Let's handle the failure
        std::cin.clear(); // Put us back in 'normal' operation mode
        ignoreLine();     // And remove the bad input

        return true;
    }
    
    return false;
}
错误情况 4：提取成功但用户溢出数字值
考虑以下简单示例
#include <cstdint>
#include <iostream>

int main()
{
    std::int16_t x{}; // x is 16 bits, holds from -32768 to 32767
    std::cout << "Enter a number between -32768 and 32767: ";
    std::cin >> x;

    std::int16_t y{}; // y is 16 bits, holds from -32768 to 32767
    std::cout << "Enter another number between -32768 and 32767: ";
    std::cin >> y;

    std::cout << "The sum is: " << x + y << '\n';
    return 0;
}
如果用户输入的数字过大（例如 40000）会发生什么？
Enter a number between -32768 and 32767: 40000
Enter another number between -32768 and 32767: The sum is: 32767
在上述情况下，`std::cin` 立即进入“故障模式”，但也会将最接近范围内的值赋给变量。当输入的值大于该类型的最大可能值时，最接近范围内的值就是该类型的最大可能值。因此，`x` 的赋值值为 `32767`。额外的输入被跳过，导致 `y` 的初始值为 `0`。我们可以像处理失败的提取一样处理这种错误。
融会贯通
这是我们的示例计算器，更新了一些额外的错误检查
#include <cstdlib> // for std::exit
#include <iostream>
#include <limits> // for std::numeric_limits

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// returns true if extraction failed, false otherwise
bool clearFailedExtraction()
{
    // Check for failed extraction
    if (!std::cin) // If the previous extraction failed
    {
        if (std::cin.eof()) // If the stream was closed
        {
            std::exit(0); // Shut down the program now
        }

        // Let's handle the failure
        std::cin.clear(); // Put us back in 'normal' operation mode
        ignoreLine();     // And remove the bad input

        return true;
    }
    
    return false;
}

double getDouble()
{
    while (true) // Loop until user enters a valid input
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        if (clearFailedExtraction())
        {
            std::cout << "Oops, that input is invalid.  Please try again.\n";
            continue;
        }

        ignoreLine(); // Remove any extraneous input
        return x;     // Return the value we extracted
    }
}

char getOperator()
{
    while (true) // Loop until user enters a valid input
    {
        std::cout << "Enter one of the following: +, -, *, or /: ";
        char operation{};
        std::cin >> operation;

        if (!clearFailedExtraction()) // we'll handle error messaging if extraction failed below
             ignoreLine(); // remove any extraneous input (only if extraction succeded)

        // Check whether the user entered meaningful input
        switch (operation)
        {
        case '+':
        case '-':
        case '*':
        case '/':
            return operation; // Return the entered char to the caller
        default: // Otherwise tell the user what went wrong
            std::cout << "Oops, that input is invalid.  Please try again.\n";
        }
    }
}
 
void printResult(double x, char operation, double y)
{
    std::cout << x << ' ' << operation << ' ' << y << " is ";

    switch (operation)
    {
    case '+':
        std::cout << x + y << '\n';
        return;
    case '-':
        std::cout << x - y << '\n';
        return;
    case '*':
        std::cout << x * y << '\n';
        return;
    case '/':
        if (y == 0.0)
            break;

        std::cout << x / y << '\n';
        return;
    }

    std::cout << "???";  // Being robust means handling unexpected parameters as well, even though getOperator() guarantees operation is valid in this particular program
}
 
int main()
{
    double x{ getDouble() };
    char operation{ getOperator() };
    double y{ getDouble() };

    // Handle division by 0
    while (operation == '/' && y == 0.0) 
    {
        std::cout << "The denominator cannot be zero.  Try again.\n";
        y = getDouble();
    }
 
    printResult(x, operation, y);
 
    return 0;
}
总结
在编写程序时，请考虑用户将如何滥用您的程序，尤其是在文本输入方面。对于每个文本输入点，请考虑
提取会失败吗？
用户会输入比预期更多的输入吗？
用户会输入无意义的输入吗？
用户会使输入溢出吗？
您可以使用 `if` 语句和布尔逻辑来测试输入是否符合预期且有意义。
以下代码将清除任何多余的输入
#include <limits> // for std::numeric_limits

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}
以下代码将测试并修复失败的提取或溢出（并删除多余的输入）
// returns true if extraction failed, false otherwise
bool clearFailedExtraction()
{
    // Check for failed extraction
    if (!std::cin) // If the previous extraction failed
    {
        if (std::cin.eof()) // If the stream was closed
        {
            std::exit(0); // Shut down the program now
        }

        // Let's handle the failure
        std::cin.clear(); // Put us back in 'normal' operation mode
        ignoreLine();     // And remove the bad input

        return true;
    }
    
    return false;
}
我们可以通过以下方式检测是否存在未提取的输入（除了换行符）
// returns true if std::cin has unextracted input on the current line, false otherwise
bool hasUnextractedInput()
{
    return !std::cin.eof() && std::cin.peek() != '\n';
}
最后，如果原始输入无效，请使用循环要求用户重新输入。
作者注
输入验证很重要且有用，但它也往往使示例更复杂，更难理解。因此，在未来的课程中，我们通常不会进行任何类型的输入验证，除非它与我们试图教授的内容相关。
下一课
9.6
Assert 和 static_assert
返回目录
上一课
9.4
检测和处理错误