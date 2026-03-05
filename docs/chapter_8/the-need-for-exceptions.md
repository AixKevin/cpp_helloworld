# 27.1 — 异常的必要性

27.1 — 异常的必要性
Alex
2008 年 10 月 4 日，下午 1:26 PDT
2024 年 5 月 23 日
在上一节关于
错误处理
的课程中，我们讨论了如何使用 assert()、std::cerr 和 exit() 来处理错误。但是，我们推迟了一个更深层的话题，现在将涵盖它：异常。
当返回码失效时
在编写可重用代码时，错误处理是必需的。处理潜在错误最常见的方法之一是通过返回码。例如：
#include <string_view>

int findFirstChar(std::string_view string, char ch)
{
    // Step through each character in string
    for (std::size_t index{ 0 }; index < string.length(); ++index)
        // If the character matches ch, return its index
        if (string[index] == ch)
            return index;

    // If no match was found, return -1
    return -1;
}
此函数返回字符串中与 ch 匹配的第一个字符的索引。如果找不到该字符，函数将返回 -1 作为未找到该字符的指示。
这种方法的主要优点是它极其简单。然而，当在非平凡的情况下使用时，使用返回码会很快暴露出一些缺点：
首先，返回值可能难以理解——如果一个函数返回 -1，它是想表示一个错误，还是它实际上是一个有效的返回值？通常很难判断，除非深入研究函数内部或查阅文档。
其次，函数只能返回一个值，那么当你需要同时返回函数结果和可能的错误码时会发生什么？考虑以下函数：
double divide(int x, int y)
{
    return static_cast<double>(x)/y;
}
这个函数急需一些错误处理，因为如果用户为参数 y 传入 0，它将崩溃。但是，它还需要返回 x/y 的结果。它如何同时做到这两点？最常见的答案是，结果或错误处理必须作为引用参数传回，这会导致代码变得丑陋且不方便使用。例如：
#include <iostream>

double divide(int x, int y, bool& outSuccess)
{
    if (y == 0)
    {
        outSuccess = false;
        return 0.0;
    }

    outSuccess = true;
    return static_cast<double>(x)/y;
}

int main()
{
    bool success {}; // we must now pass in a bool value to see if the call was successful
    double result { divide(5, 3, success) };

    if (!success) // and check it before we use the result
        std::cerr << "An error occurred" << std::endl;
    else
        std::cout << "The answer is " << result << '\n';
}
第三，在许多事情都可能出错的代码序列中，必须不断检查错误码。考虑以下代码片段，它涉及解析文本文件以获取应该存在的值：
std::ifstream setupIni { "setup.ini" }; // open setup.ini for reading
    // If the file couldn't be opened (e.g. because it was missing) return some error enum
    if (!setupIni)
        return ERROR_OPENING_FILE;

    // Now read a bunch of values from a file
    if (!readIntegerFromFile(setupIni, m_firstParameter)) // try to read an integer from the file
        return ERROR_READING_VALUE; // Return enum value indicating value couldn't be read

    if (!readDoubleFromFile(setupIni, m_secondParameter)) // try to read a double from the file
        return ERROR_READING_VALUE;

    if (!readFloatFromFile(setupIni, m_thirdParameter)) // try to read a float from the file
        return ERROR_READING_VALUE;
我们还没有介绍文件访问，所以如果你不理解上述内容是如何工作的，请不要担心——只需注意每次调用都需要进行错误检查并返回给调用者这一事实。现在想象一下，如果有二十个不同类型的参数——你基本上要检查错误并返回 ERROR_READING_VALUE 二十次！所有这些错误检查和返回值使得确定函数正在尝试做什么变得更加困难。
第四，返回码与构造函数结合得不太好。如果你正在创建一个对象，并且构造函数内部出现了灾难性的错误，会发生什么？构造函数没有返回类型来传回状态指示，并且通过引用参数传回会很混乱，并且必须显式检查。此外，即使你这样做，对象仍然会被创建，然后必须处理或销毁。
最后，当错误码返回给调用者时，调用者可能并不总是能够处理该错误。如果调用者不想处理该错误，它要么忽略它（在这种情况下它将永远丢失），要么将错误返回到调用它的函数。这会很混乱，并导致许多上述相同的问题。
总而言之，返回码的主要问题是错误处理代码最终与代码的正常控制流紧密相连。这反过来又限制了代码的布局方式以及错误可以合理处理的方式。
异常
异常处理提供了一种机制，可以将错误或其他异常情况的处理与代码的典型控制流分离。这允许在给定情况下以最有效的方式和时间自由处理错误，从而减轻了返回码造成的大部分（如果不是全部）混乱。
在下一课中，我们将探讨异常在 C++ 中是如何工作的。
下一课
27.2
基本异常处理
返回目录
上一课
26.x
第 26 章总结与测验