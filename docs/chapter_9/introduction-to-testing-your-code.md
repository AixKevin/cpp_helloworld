# 9.1 — 代码测试入门

9.1 — 代码测试入门
Alex
2016 年 9 月 8 日，太平洋时间下午 2:06
2024 年 4 月 30 日
你已经编写了一个程序，它能编译，甚至看起来也能正常工作！接下来呢？
嗯，这取决于情况。如果你编写的程序只运行一次就被丢弃，那么你就完成了。在这种情况下，你的程序并非适用于所有情况可能不重要——如果它适用于你需要的那个情况，而且你只运行一次，那么你就完成了。
如果你的程序完全是线性的（没有条件语句，例如
if 语句
或
switch 语句
），不接受任何输入，并且产生正确的结果，那么你可能就完成了。在这种情况下，你已经通过运行程序并验证输出来测试了整个程序。你可能希望在几个不同的系统上编译并运行程序，以确保其行为一致（如果行为不一致，你可能做了某些会产生未定义行为的事情，但这些行为恰好在你的初始系统上也能工作）。
但你很可能编写了一个打算多次运行的程序，它使用循环和条件逻辑，并接受某种用户输入。你可能还编写了一些将来可以在其他程序中重用的函数。你可能经历了一些
范围蔓延
，即你添加了一些最初未计划的新功能。也许你甚至打算将此程序分发给其他人（他们可能会尝试一些你没想到的事情）。在这种情况下，你确实应该验证你的程序在各种条件下是否像你预期的那样工作——这需要一些主动的测试。
仅仅因为你的程序在一组输入下工作正常，并不意味着它在所有情况下都能正常工作。
软件测试
（也称为
软件验证
）是确定软件是否按预期工作的过程。
测试挑战
在讨论一些测试代码的实用方法之前，让我们先谈谈为什么全面测试程序很困难。
考虑这个简单的程序
#include <iostream>

void compare(int x, int y)
{
    if (x > y)
        std::cout << x << " is greater than " << y << '\n'; // case 1
    else if (x < y)
        std::cout << x << " is less than " << y << '\n'; // case 2
    else
        std::cout << x << " is equal to " << y << '\n'; // case 3
}

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another number: ";
    int y{};
    std::cin >> y;

    compare(x, y);

    return 0;
}
假设一个 4 字节整数，明确地用每种可能的输入组合测试这个程序将需要你运行程序 18,446,744,073,709,551,616 次（约 18 亿亿）。显然这不是一个可行的任务！
每次我们要求用户输入，或者代码中有一个条件，我们程序的可能执行方式的数量就会乘以某个乘数因子。除了最简单的程序之外，明确测试所有输入组合几乎立即变得不可能。
现在，你的直觉应该告诉你，你实际上不需要运行上述程序 18 亿亿次来确保它能工作。你可以合理地得出结论，如果情况 1 对于一对
x
和
y
值（其中
x > y
）有效，那么它对于任何一对
x
和
y
（其中
x > y
）都应该有效。鉴于此，很明显我们实际上只需要运行这个程序大约三次（一次运行
compare()
函数中的三种情况中的每一种），就可以高度确信它能按预期工作。我们还可以使用其他类似的技巧来大大减少测试次数，从而使测试变得可管理。
关于测试方法论有很多可以写——事实上，我们可以专门写一整章。但由于这不是 C++ 特有的主题，我们将仅作一个简短而非正式的介绍，从你（作为开发人员）测试自己代码的角度出发。在接下来的几个小节中，我们将讨论你在测试代码时应该考虑的一些
实际
问题。
小块测试你的程序
考虑一家汽车制造商正在建造一辆定制概念车。你认为他们会做以下哪一项？
a) 在安装每个汽车部件之前，单独制造（或购买）并测试它。一旦部件被证明可以工作，就将其集成到汽车中并重新测试，以确保集成成功。最后，测试整车，作为一切看起来都正常的最终验证。
b) 一次性用所有部件组装一辆汽车，然后直到最后才第一次测试整车。
显然，选项 a) 似乎是更好的选择。然而，许多新程序员却像选项 b) 那样编写代码！
在情况 b) 中，如果任何汽车零件未能按预期工作，机械师将不得不诊断整辆汽车以确定问题所在——问题可能在任何地方。一个症状可能有许多原因——例如，汽车无法启动是由于火花塞故障、电池、燃油泵还是其他原因？这导致大量时间浪费在试图精确查明问题所在以及如何解决这些问题上。如果发现问题，后果可能是灾难性的——一个领域的改变可能会在其他多个地方引起“连锁反应”（改变）。例如，燃油泵过小可能导致发动机重新设计，进而导致车架重新设计。在最坏的情况下，你可能最终会重新设计汽车的很大一部分，仅仅是为了适应最初的一个小问题！
在情况 a) 中，公司边做边测试。如果任何组件刚出厂就有问题，他们会立即知道并能修复/更换。在部件本身被证明可以工作之前，不会将其集成到汽车中，然后一旦集成到汽车中，该部件会立即重新测试。这样，任何意外问题都会尽早被发现，因为它们仍然是易于解决的小问题。
当他们组装完整个汽车时，他们应该对汽车能够正常工作抱有合理的信心——毕竟，所有部件都经过了单独测试和初始集成测试。此时仍有可能发现意外问题，但这种风险通过所有先前的测试降至最低。
上面的类比对程序同样适用，尽管由于某种原因，新程序员通常没有意识到这一点。你最好编写小型函数（或类），然后立即编译和测试它们。这样，如果你犯了错误，你就会知道它一定是你自上次编译/测试以来更改的一小部分代码。这意味着要查找的地方更少，调试时间也大大减少。
单独测试你代码的一小部分以确保该“单元”代码是正确的，这称为
单元测试
。每个
单元测试
都旨在确保该单元的特定行为是正确的。
最佳实践
将你的程序编写成小的、定义良好的单元（函数或类），经常编译，并随时测试你的代码。
如果程序很短并且接受用户输入，尝试各种用户输入可能就足够了。但是随着程序越来越长，这种方法变得不那么充分，并且在将单个函数或类集成到程序的其余部分之前测试它们具有更大的价值。
那么我们如何以单元为单位测试我们的代码呢？
非正式测试
测试代码的一种方法是在编写程序时进行非正式测试。在编写完一个代码单元（一个函数、一个类或一些其他离散的“代码包”）后，你可以编写一些代码来测试刚刚添加的单元，然后在测试通过后删除该测试。例如，对于下面的
isLowerVowel()
函数，你可能会编写以下代码：
#include <iostream>

// We want to test the following function
// For simplicity, we'll ignore that 'y' is sometimes counted as a vowel
bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}

int main()
{
    // So here's our temporary tests to validate it works
    std::cout << isLowerVowel('a') << '\n'; // temporary test code, should produce 1
    std::cout << isLowerVowel('q') << '\n'; // temporary test code, should produce 0

    return 0;
}
如果结果返回
1
和
0
，那么就没问题了。你知道你的函数在一些基本情况下可以工作，并且通过查看代码，你可以合理地推断它将适用于你没有测试的情况（'e'、'i'、'o' 和 'u'）。所以你可以删除临时的测试代码，然后继续编程。
保留你的测试
尽管编写临时测试是一种快速简便的代码测试方法，但它没有考虑到你将来可能需要再次测试同一段代码的事实。也许你修改了一个函数以添加新功能，并且想要确保你没有破坏任何已经正常工作的功能。因此，保留你的测试以便将来可以再次运行可能更有意义。例如，你可以将测试移到
testVowel()
函数中，而不是删除你的临时测试代码：
#include <iostream>

bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}

// Not called from anywhere right now
// But here if you want to retest things later
void testVowel()
{
    std::cout << isLowerVowel('a') << '\n'; // temporary test code, should produce 1
    std::cout << isLowerVowel('q') << '\n'; // temporary test code, should produce 0
}

int main()
{
    return 0;
}
随着你创建更多的测试，你可以简单地将它们添加到
testVowel()
函数中。
自动化你的测试函数
上述测试函数的一个问题是，它依赖于你在运行它时手动验证结果。这要求你至少记住预期的答案（假设你没有记录），并手动将实际结果与预期结果进行比较。
我们可以通过编写一个包含测试和预期答案并进行比较的测试函数来做得更好，这样我们就不必手动操作了。
#include <iostream>

bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}

// returns the number of the test that failed, or 0 if all tests passed
int testVowel()
{
    if (!isLowerVowel('a')) return 1;
    if (isLowerVowel('q')) return 2;

    return 0;
}

int main()
{
    int result { testVowel() };
    if (result != 0)
        std::cout << "testVowel() test " << result << " failed.\n";
    else
        std::cout << "testVowel() tests passed.\n";

    return 0;
}
现在，您可以随时调用
testVowel()
来重新验证您没有破坏任何东西，测试例程会为您完成所有工作，返回“一切正常”信号（返回值
0
），或者返回未通过的测试编号，以便您可以调查它为什么失败。这在修改旧代码时特别有用，可以确保您没有意外地破坏任何东西！
致进阶读者
一个更好的方法是使用
assert
，如果任何测试失败，它将导致程序以错误消息中止。这样我们就不必创建和处理测试用例编号了。
#include <cassert> // for assert
#include <cstdlib> // for std::abort
#include <iostream>

bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}

// Program will halt on any failed test case
int testVowel()
{
#ifdef NDEBUG
    // If NDEBUG is defined, asserts are compiled out.
    // Since this function requires asserts to not be compiled out, we'll terminate the program if this function is called when NDEBUG is defined.
    std::cerr << "Tests run with NDEBUG defined (asserts compiled out)";
    std::abort();
#endif

    assert(isLowerVowel('a'));
    assert(isLowerVowel('e'));
    assert(isLowerVowel('i'));
    assert(isLowerVowel('o'));
    assert(isLowerVowel('u'));
    assert(!isLowerVowel('b'));
    assert(!isLowerVowel('q'));
    assert(!isLowerVowel('y'));
    assert(!isLowerVowel('z'));

    return 0;
}

int main()
{
    testVowel();

    // If we reached here, all tests must have passed
    std::cout << "All tests succeeded\n";

    return 0;
}
我们将在课程
9.6 -- assert 和 static_assert
中介绍
assert
。
单元测试框架
由于编写函数来测试其他函数非常常见且有用，因此有专门的框架（称为
单元测试框架
）旨在简化编写、维护和执行单元测试的过程。由于这些框架涉及第三方软件，我们在此不作介绍，但你应该知道它们的存在。
集成测试
一旦你的每个单元都经过了单独测试，它们就可以被集成到你的程序中并重新测试，以确保它们集成正确。这被称为
集成测试
。集成测试往往更复杂——目前，运行你的程序几次并抽查集成单元的行为就足够了。
小测验时间
问题 #1
你什么时候应该开始测试你的代码？
显示答案
一旦你写了一个非平凡的函数。
下一课
9.2
代码覆盖率
返回目录
上一课
8.x
第 8 章总结与测验