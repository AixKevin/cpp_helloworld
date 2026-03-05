# 8.9 — do-while 语句

8.9 — do-while 语句
Alex
2007 年 6 月 25 日，下午 4:54 PDT
2025 年 2 月 5 日
考虑这样一种情况：我们想向用户显示一个菜单，并要求他们做出选择——如果用户选择无效，则再次询问他们。显然，菜单和选择应该放在某种循环中（这样我们就可以一直询问用户，直到他们输入有效输入），但我们应该选择哪种循环呢？
由于 while 循环预先评估条件，因此它是一个尴尬的选择。我们可以这样解决这个问题
#include <iostream>

int main()
{
    // selection must be declared outside while-loop, so we can use it later
    int selection {}; // value initialized to 0

    while (selection < 1 || selection > 4)
    {
        std::cout << "Please make a selection: \n";
        std::cout << "1) Addition\n";
        std::cout << "2) Subtraction\n";
        std::cout << "3) Multiplication\n";
        std::cout << "4) Division\n";
        std::cin >> selection;
    }

    // do something with selection here
    // such as a switch statement

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
但这只起作用，因为我们
selection
的初始值
0
不在有效值集（
1, 2, 3 或 4
）中。如果
0
是一个有效选择怎么办？我们就必须选择不同的初始化器来表示“无效”——现在我们的代码中引入了魔法数字（
5.2 -- 字面量
）。
我们可以改为添加一个新变量来跟踪有效性，如下所示
#include <iostream>

int main()
{
    int selection {};
    bool invalid { true }; // new variable just to gate the loop

    while (invalid)
    {
        std::cout << "Please make a selection: \n";
        std::cout << "1) Addition\n";
        std::cout << "2) Subtraction\n";
        std::cout << "3) Multiplication\n";
        std::cout << "4) Division\n";

        std::cin >> selection;
        invalid = (selection < 1 || selection > 4);
    }

    // do something with selection here
    // such as a switch statement

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
虽然这避免了魔法数字，但它引入了一个新变量只是为了确保循环运行一次，这增加了复杂性以及额外错误的可能性。
do-while 语句
为了帮助解决上述问题，C++ 提供了 do-while 语句
do
    statement; // can be a single statement or a compound statement
while (condition);
do-while 语句
是一种循环结构，其工作方式与 while 循环完全相同，只是语句总是至少执行一次。语句执行后，do-while 循环检查条件。如果条件评估为
true
，则执行路径跳回到 do-while 循环的顶部并再次执行。
这是我们上面使用 do-while 循环而不是 while 循环的示例
#include <iostream>

int main()
{
    // selection must be declared outside of the do-while-loop, so we can use it later
    int selection {};

    do
    {
        std::cout << "Please make a selection: \n";
        std::cout << "1) Addition\n";
        std::cout << "2) Subtraction\n";
        std::cout << "3) Multiplication\n";
        std::cout << "4) Division\n";
        std::cin >> selection;
    }
    while (selection < 1 || selection > 4);

    // do something with selection here
    // such as a switch statement

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
通过这种方式，我们避免了魔法数字和额外的变量。
在上面的示例中值得讨论的一点是
selection
变量必须在 do 块之外声明。如果
selection
变量在 do 块内声明，则当 do 块终止时（在条件评估之前发生），它将被销毁。但我们在 while 条件中需要该变量——因此，
selection
变量必须在 do 块之外声明（即使它后来没有在函数体中使用）。
实际上，do-while 循环并不常用。将条件放在循环的底部会模糊循环条件，这可能导致错误。因此，许多开发人员建议完全避免使用 do-while 循环。我们将采取更温和的立场，主张在选择相等时优先选择 while 循环而不是 do-while 循环。
最佳实践
在选择相等时，优先选择 while 循环而不是 do-while 循环。
下一课
8.10
for 语句
返回目录
上一课
8.8
循环和 while 语句简介