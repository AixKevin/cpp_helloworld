# 8.7 — Goto 语句

8.7 — Goto 语句
Alex
2007 年 6 月 21 日，太平洋夏令时下午 6:55
2024 年 10 月 14 日
我们将要介绍的下一类控制流语句是无条件跳转。无条件跳转会使执行跳到代码中的另一个位置。“无条件”一词意味着跳转总是发生（不像 if 语句或 switch 语句，跳转只根据表达式的结果有条件地发生）。
在 C++ 中，无条件跳转通过
goto 语句
实现，要跳转到的位置通过使用
语句标签
标识。与 switch case 标签一样，语句标签通常不缩进。
以下是 goto 语句和语句标签的示例
#include <iostream>
#include <cmath> // for sqrt() function

int main()
{
    double x{};
tryAgain: // this is a statement label
    std::cout << "Enter a non-negative number: "; 
    std::cin >> x;

    if (x < 0.0)
        goto tryAgain; // this is the goto statement

    std::cout << "The square root of " << x << " is " << std::sqrt(x) << '\n';
    return 0;
}
在这个程序中，要求用户输入一个非负数。但是，如果输入了负数，程序会利用 goto 语句跳回
tryAgain
标签。然后再次要求用户输入一个新数字。通过这种方式，我们可以不断要求用户输入，直到他或她输入有效内容。
以下是该程序的示例运行
Enter a non-negative number: -4
Enter a non-negative number: 4
The square root of 4 is 2
语句标签具有函数作用域
在关于对象作用域的章节（
第 7 章
）中，我们介绍了两种作用域：局部（块）作用域和文件（全局）作用域。语句标签使用第三种作用域：
函数作用域
，这意味着标签在函数中即使在其声明点之前也可见。goto 语句及其相应的
statement label
必须出现在同一个函数中。
虽然上面的例子展示了一个向后跳转（跳到函数中前面的点）的 goto 语句，但 goto 语句也可以向前跳转
#include <iostream>

void printCats(bool skip)
{
    if (skip)
        goto end; // jump forward; statement label 'end' is visible here due to it having function scope
    
    std::cout << "cats\n";
end:
    ; // statement labels must be associated with a statement
}

int main()
{
    printCats(true);  // jumps over the print statement and doesn't print anything
    printCats(false); // prints "cats"

    return 0;
}
这会打印
cats
除了向前跳转之外，上面的程序还有一些值得一提的有趣之处。
首先，请注意语句标签必须与语句关联（因此得名：它们标记一个语句）。因为函数末尾没有语句，我们不得不使用空语句，以便有一个语句可以标记。其次，由于语句标签具有函数作用域，我们能够跳转到由 `end` 标记的语句，即使我们尚未声明 `end`。语句标签不需要前向声明。第三，值得明确提及的是，上面的程序形式不佳——使用 if 语句跳过打印语句会比使用 goto 语句跳过它更好。
跳转有两个主要限制：你只能在一个函数的范围内跳转（你不能跳出一个函数进入另一个函数），如果你向前跳转，你不能跳过在跳转到的位置仍处于作用域的任何变量的初始化。例如
int main()
{
    goto skip;   // error: this jump is illegal because...
    int x { 5 }; // this initialized variable is still in scope at statement label 'skip'
skip:
    x += 3;      // what would this even evaluate to if x wasn't initialized?
    return 0;
}
请注意，你可以向后跳过变量初始化，并且当执行初始化时，变量将被重新初始化。
避免使用 goto
在 C++（以及其他现代高级语言）中，使用
goto
是被排斥的。
Edsger W. Dijkstra
，一位著名的计算机科学家，在一篇著名但难以阅读的论文《
Go To Statement Considered Harmful
》中阐述了避免 goto 的理由。goto 的主要问题在于它允许程序员任意地在代码中跳转。这会产生不那么讨人喜欢的“意大利面条式代码”。
意大利面条式代码
是执行路径类似于一碗意大利面（缠绕扭曲）的代码，使得此类代码的逻辑极难理解。
正如 Dijkstra 有点幽默地说，“程序员的质量是他们生成的程序中 go to 语句密度的递减函数”。
几乎所有使用 goto 语句编写的代码都可以使用 C++ 中的其他构造更清晰地编写，例如 if 语句和循环。一个显著的例外是当你需要退出嵌套循环但不需要退出整个函数时——在这种情况下，goto 到循环之外可能是最干净的解决方案。
致进阶读者
以下是使用 goto 退出嵌套循环而不退出函数的一个人为例子
#include <iostream>

int main()
{
    for (int i = 1; i < 5; ++i)
    {        
        for (int j = 1; j < 5; ++j)
        {
            std::cout << i << " * " << j << " is " << i*j << '\n';
            
            // If the product is divisible by 9, jump to the "end" label
            if (i*j % 9 == 0)
            {
                std::cout << "Found product divisible by 9.  Ending early.\n";
                goto end;
            }
        }

        std::cout << "Incrementing the first factor.\n";
    }

end:
    std::cout << "And we're done." << '\n';

    return 0;
}
作者注
来自我们的朋友
xkcd
最佳实践
避免使用 goto 语句（除非替代方案对代码可读性的影响显著更差）。
下一课
8.8
循环和 while 语句简介
返回目录
上一课
8.6
Switch 穿透和作用域