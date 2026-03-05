# 8.2 — If 语句和代码块

8.2 — If 语句和代码块
Alex
2007 年 6 月 21 日，太平洋夏令时上午 10:01
2025 年 3 月 5 日
我们将讨论的第一类控制流语句是条件语句。
条件语句
是指定是否应执行某些相关语句的语句。
C++ 支持两种基本类型的条件语句：
if 语句
（我们在课程
4.10 -- if 语句简介
中介绍过，并将在本文中进一步讨论）和
switch 语句
（我们将在接下来的几节课中介绍）。
if 语句快速回顾
C++ 中最基本的条件语句是
if 语句
。
if 语句
的形式为
if (condition)
    true_statement;
或者带有可选的
else 语句
if (condition)
    true_statement;
else
    false_statement;
如果
condition
的求值结果为
true
，则执行
true_statement
。如果
condition
的求值结果为
false
并且存在可选的
else 语句
，则执行
false_statement
。
这是一个使用带有可选
else 语句
的
if 语句
的简单程序
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x > 10)
        std::cout << x << " is greater than 10\n";
    else
        std::cout << x << " is not greater than 10\n";

    return 0;
}
这个程序就像您期望的那样工作
Enter a number: 15
15 is greater than 10
Enter a number: 4
4 is not greater than 10
if 或 else 带有多个条件语句
新程序员经常尝试这样做
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "Enter your height (in cm): ";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "You are tall enough to ride.\n";
    else
        std::cout << "You are not tall enough to ride.\n";
        std::cout << "Too bad!\n"; // focus on this line

    return 0;
}
但是，请考虑程序的以下运行
Enter your height (in cm): 180
You are tall enough to ride.
Too bad!
这个程序没有按预期工作，因为
true_statement
和
false_statement
只能是单个语句。这里的缩进具有欺骗性——上面的程序执行时就好像它是这样写的
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "Enter your height (in cm): ";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "You are tall enough to ride.\n";
    else
        std::cout << "You are not tall enough to ride.\n";

    std::cout << "Too bad!\n"; // focus on this line

    return 0;
}
这使得“太糟糕了！”将始终执行更加清晰。
但是，通常需要根据某些条件执行多个语句。为此，我们可以使用复合语句（代码块）
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "Enter your height (in cm): ";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "You are tall enough to ride.\n";
    else
    { // note addition of block here
        std::cout << "You are not tall enough to ride.\n";
        std::cout << "Too bad!\n";
    }

    return 0;
}
请记住，代码块被视为单个语句，因此现在它可以按预期工作
Enter your height (in cm): 180
You are tall enough to ride.
Enter your height (in cm): 130
You are not tall enough to ride.
Too bad!
隐式代码块
如果程序员在
if 语句
或
else 语句
的语句部分中没有声明代码块，编译器将隐式声明一个。因此
if (condition)
    true_statement;
else
    false_statement;
实际上等同于
if (condition)
{
    true_statement;
}
else
{
    false_statement;
}
大多数情况下，这无关紧要。但是，新程序员有时会尝试在隐式代码块中定义变量，如下所示
#include <iostream>

int main()
{
    if (true)
        int x{ 5 };
    else
        int x{ 6 };

    std::cout << x << '\n';

    return 0;
}
这将无法编译，编译器会生成标识符
x
未定义的错误。这是因为上面的示例等同于
#include <iostream>

int main()
{
    if (true)
    {
        int x{ 5 };
    } // x destroyed here
    else
    {
        int x{ 6 };
    } // x destroyed here

    std::cout << x << '\n'; // x isn't in scope here

    return 0;
}
在这种情况下，更清楚的是变量
x
具有块作用域并在块结束时销毁。当我们到达
std::cout
行时，
x
不存在。
是否对单个语句使用代码块
在程序员社区中，关于在
if
或
else
之后的单个语句是否应明确地包含在代码块中存在争议。
使用代码块的理由有很多。
不使用代码块更容易不小心添加看起来是条件语句但实际上不是的语句。考虑
if (age >= minDrinkingAge)
    purchaseBeer();
现在假设我们很着急，修改这个程序以添加另一个功能
if (age >= minDrinkingAge)
    purchaseBeer();
    gamble(); // will always execute
哎呀，我们刚允许未成年人赌博。祝您在监狱里玩得开心！
不使用代码块可能会使程序更难以调试。假设我们有以下代码片段
if (age >= minDrinkingAge)
    addBeerToCart(); // conditionally executes

checkout(); // always executes
假设我们怀疑
addBeerToCart()
函数有问题，所以我们将其注释掉
if (age >= minDrinkingAge)
//    addBeerToCart();

checkout(); // conditionally executes now
现在我们已经使
checkout()
变为条件语句，这当然不是我们想要的。
如果您总是在
if
或
else
之后使用代码块，则上述情况都不会发生。
if constexpr
（C++23 中添加的 if 语句的变体）要求使用代码块。因此，使用代码块可确保
if
和
if constexpr
之间的一致性。
不围绕单个语句使用代码块的最佳论点是，添加代码块会通过垂直间隔使您一次看到的的代码更少，这会降低代码的可读性，并可能导致其他更严重的错误。
社区似乎更倾向于始终使用代码块而不是不使用代码块，尽管这个建议肯定不是普遍的。
最佳实践
考虑将与
if
或
else
相关的单个语句放入代码块中（尤其是在学习时）。更有经验的 C++ 开发人员有时会为了更紧凑的垂直间距而忽视这种做法。
一个合理的折衷方案是将单行放在与
if
或
else
同一行
if (age >= minDrinkingAge) purchaseBeer();
else std::cout << "No drinky for you\n".
这避免了上述两个缺点，但以可读性为代价。
单行方法的一个公平批评是它会产生更难以调试的代码
因为条件和相关语句将作为同一步骤的一部分执行，所以更难判断语句是实际执行还是被跳过。
因为条件和相关语句在同一行，所以您无法只对相关语句设置断点（以便仅在语句实际执行时停止执行）。
但是，如果上述任何一点在调试时造成阻碍，您可以在条件和语句之间插入一个换行符（使它们在单独的行上），进行调试，然后删除换行符。
if-else 与 if-if
新程序员有时会想知道何时应该使用 if-else（if 后跟一个或多个 else 语句）或 if-if（if 后跟一个或多个额外的 if 语句）。
当您只想在第一个
true
条件之后执行代码时，使用 if-else。
当您想在所有
true
条件之后执行代码时，使用 if-if。
这是一个演示此功能的程序
#include <iostream>

void ifelse(bool a, bool b, bool c)
{
    if (a)      // always evaluates
        std::cout << "a";
    else if (b) // only evaluates when prior if-statement condition is false
        std::cout << "b";
    else if (c) // only evaluates when prior if-statement condition is false
        std::cout << "c";
    std::cout << '\n';
}

void ifif(bool a, bool b, bool c)
{
    if (a) // always evaluates
        std::cout << "a";
    if (b) // always evaluates
        std::cout << "b";
    if (c) // always evaluates
        std::cout << "c";
    std::cout << '\n';
}

int main()
{
    ifelse(false, true, true);
    ifif(false, true, true);

    return 0;
}
在调用
ifelse(false, true, true)
时，
a
为
false
，因此我们不执行相关语句，而是执行相关的
else
。
b
为 true，因此我们打印
b
。由于此
if
条件为 true，因此相关的
else
将不会执行（其后紧跟的任何其他
else
语句也不会执行）。请注意，我们只执行了第一个
true
条件 (
b
) 之后的代码。
在调用
ifif(false, true, true)
时，
a
为 false，因此我们不执行相关语句，并移动到下一个
if
。
b
为 true，因此我们打印
b
并移动到下一个
if
。
c
为 true，因此我们打印
c
。请注意，我们执行了所有
true
条件 (
b
和
c
) 之后的代码。
现在看看这个有些相似的函数
char getFirstMatchingChar(bool a, bool b, bool c)
{
    if (a) // always evaluates
        return 'a';
    else if (b) // only evaluates when prior if-statement condition is false
        return 'b';
    else if (c) // only evaluates when prior if-statement condition is false
        return 'c';

    return 0;
}
由于我们使用的是 if-else，因此很明显我们只想在第一个
true
条件之后执行代码。但是当每个相关语句都返回一个值时，我们可以这样写
char getFirstMatchingChar(bool a, bool b, bool c)
{
    if (a) // always evaluates
        return 'a'; // returns when if-statement is true
    if (b) // only evaluates when prior if-statement condition is false
        return 'b'; // returns when if-statement is true
    if (c) // only evaluates when prior if-statement condition is false
        return 'c'; // returns when if-statement is true

    return 0;
}
虽然这在表面上看起来我们想在每个
true
条件之后执行代码，但一旦我们找到第一个
true
条件，相关语句将导致函数返回。其余的 if 语句没有机会进行评估。因此，这与之前的版本行为相同。当所有相关语句都返回一个值时，许多程序员更喜欢省略
else
关键字，因为这样做可以避免不必要的混乱，并且条件排列得更好。
关键见解
当所有相关语句都返回一个值时，您总是可以使用 if-if，因为
else
不提供任何价值。
我们将在下一课中继续探索 if 语句。
下一课
8.3
常见的 if 语句问题
返回目录
上一课
8.1
控制流简介