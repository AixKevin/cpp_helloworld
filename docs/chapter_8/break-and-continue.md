# 8.11 — Break 和 continue

8.11 — Break 和 continue
Alex
2007 年 6 月 26 日，下午 4:22 PDT
2023 年 9 月 11 日
Break
尽管你已经在
switch
语句的上下文中看到过
break
语句（
8.5 -- Switch 语句基础
），但它值得更全面的介绍，因为它也可以用于其他类型的控制流语句。
break 语句
会导致 while 循环、do-while 循环、for 循环或 switch 语句结束，执行将继续进行到循环或 switch 语句后的下一条语句。
中断 switch
在
switch
语句的上下文中，
break
通常用于每个 case 的末尾，以表示 case 已完成（这可以防止执行落入后续 case）
#include <iostream>

void printMath(int x, int y, char ch)
{
    switch (ch)
    {
    case '+':
        std::cout << x << " + " << y << " = " << x + y << '\n';
        break; // don't fall-through to next case
    case '-':
        std::cout << x << " - " << y << " = " << x - y << '\n';
        break; // don't fall-through to next case
    case '*':
        std::cout << x << " * " << y << " = " << x * y << '\n';
        break; // don't fall-through to next case
    case '/':
        std::cout << x << " / " << y << " = " << x / y << '\n';
        break;
    }
}

int main()
{
    printMath(2, 3, '+');

    return 0;
}
有关执行落入以及其他示例的更多信息，请参阅课程
8.6 -- Switch 执行落入和作用域
。
中断循环
在循环的上下文中，
break
语句可以用于提前结束循环。执行将继续进行到循环结束后的下一条语句。
例如
#include <iostream>

int main()
{
    int sum{ 0 };

    // Allow the user to enter up to 10 numbers
    for (int count{ 0 }; count < 10; ++count)
    {
        std::cout << "Enter a number to add, or 0 to exit: ";
        int num{};
        std::cin >> num;

        // exit loop if user enters 0
        if (num == 0)
            break; // exit the loop now

        // otherwise add number to our sum
        sum += num;
    }

    // execution will continue here after the break
    std::cout << "The sum of all the numbers you entered is: " << sum << '\n';

    return 0;
}
此程序允许用户输入最多 10 个数字，并在最后显示所有输入数字的总和。如果用户输入 0，则 break 会导致循环提前终止（在输入 10 个数字之前）。
以下是上述程序的示例执行
Enter a number to add, or 0 to exit: 5
Enter a number to add, or 0 to exit: 2
Enter a number to add, or 0 to exit: 1
Enter a number to add, or 0 to exit: 0
The sum of all the numbers you entered is: 8
break
也是退出有意无限循环的常见方式
#include <iostream>

int main()
{
    while (true) // infinite loop
    {
        std::cout << "Enter 0 to exit or any other integer to continue: ";
        int num{};
        std::cin >> num;

        // exit loop if user enters 0
        if (num == 0)
            break;
    }

    std::cout << "We're out!\n";

    return 0;
}
上述程序的示例运行
Enter 0 to exit or any other integer to continue: 5
Enter 0 to exit or any other integer to continue: 3
Enter 0 to exit or any other integer to continue: 0
We're out!
Break 与 return
新程序员有时难以理解
break
和
return
之间的区别。
break
语句终止 switch 或循环，执行在 switch 或循环之外的第一条语句处继续。
return
语句终止循环所在的整个函数，执行在函数被调用的点处继续。
#include <iostream>

int breakOrReturn()
{
    while (true) // infinite loop
    {
        std::cout << "Enter 'b' to break or 'r' to return: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'b')
            break; // execution will continue at the first statement beyond the loop

        if (ch == 'r')
            return 1; // return will cause the function to immediately return to the caller (in this case, main())
    }

    // breaking the loop causes execution to resume here

    std::cout << "We broke out of the loop\n";

    return 0;
}

int main()
{
    int returnValue{ breakOrReturn() };
    std::cout << "Function breakOrReturn returned " << returnValue << '\n';

    return 0;
}
以下是此程序的两次运行
Enter 'b' to break or 'r' to return: r
Function breakOrReturn returned 1
Enter 'b' to break or 'r' to return: b
We broke out of the loop
Function breakOrReturn returned 0
Continue
continue 语句
提供了一种方便的方式来结束循环的当前迭代，而无需终止整个循环。
以下是使用 continue 的示例
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // if the number is divisible by 4, skip this iteration
        if ((count % 4) == 0)
            continue; // go to next iteration

        // If the number is not divisible by 4, keep going
        std::cout << count << '\n';

        // The continue statement jumps to here
    }

    return 0;
}
此程序打印 0 到 9 之间所有不能被 4 整除的数字
1
2
3
5
6
7
9
continue
语句通过使当前执行点跳转到当前循环的底部来工作。
对于 for 循环，for 循环的结束语句（在上面的示例中为
++count
）在 continue 之后仍然会执行（因为它发生在循环体结束之后）。
在使用
continue
语句与 while 或 do-while 循环时要小心。这些循环通常在循环体内部更改条件中使用的变量的值。如果使用
continue
语句导致这些行被跳过，则循环可能会变成无限循环！
考虑以下程序
#include <iostream>

int main()
{
    int count{ 0 };
    while (count < 10)
    {
        if (count == 5)
            continue; // jump to end of loop body

        std::cout << count << '\n';

        ++count; // this statement is never executed after count reaches 5

        // The continue statement jumps to here
    }

    return 0;
}
此程序旨在打印 0 到 9 之间的所有数字，除了 5。但它实际上打印
0
1
2
3
4
然后进入无限循环。当
count
为
5
时，
if
语句评估为
true
，
continue
导致执行跳转到循环底部。
count
变量从不递增。因此，在下一次传递中，
count
仍然是
5
，
if
语句仍然是
true
，程序继续永远循环。
当然，你已经知道，如果你有一个明显的计数器变量，你应该使用
for
循环，而不是
while
或
do while
循环。
关于 break 和 continue 使用的争论
许多教科书告诫读者不要在循环中使用
break
和
continue
，既因为它会导致执行流跳转，也因为它会使逻辑流更难跟踪。例如，复杂逻辑中间的
break
可能会被遗漏，或者在什么条件下应该触发它可能不明显。
然而， judiciously 使用
break
和
continue
可以通过减少嵌套块的数量和减少复杂循环逻辑的需要来帮助使循环更具可读性。
例如，考虑以下程序
#include <iostream>

int main()
{
    int count{ 0 }; // count how many times the loop iterates
    bool keepLooping { true }; // controls whether the loop ends or not
    while (keepLooping)
    {
        std::cout << "Enter 'e' to exit this loop or any other character to continue: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'e')
            keepLooping = false;
        else
        {
            ++count;
            std::cout << "We've iterated " << count << " times\n";
        }
    }

    return 0;
}
此程序使用布尔变量控制循环是否继续，以及仅在用户不退出时运行的嵌套块。
以下是更易于理解的版本，使用
break
语句
#include <iostream>

int main()
{
    int count{ 0 }; // count how many times the loop iterates
    while (true) // loop until user terminates
    {
        std::cout << "Enter 'e' to exit this loop or any other character to continue: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'e')
            break;

        ++count;
        std::cout << "We've iterated " << count << " times\n";
    }

    return 0;
}
在此版本中，通过使用单个
break
语句，我们避免了使用布尔变量（以及不得不理解其预期用途以及其值在哪里更改）、
else
语句和嵌套块。
continue
语句最有效地用于 for 循环的顶部，以便在满足某些条件时跳过循环迭代。这可以让我们避免嵌套块。
例如，而不是这样：
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // if the number is not divisible by 4...
        if ((count % 4) != 0) // nested block
        {
                // Print the number
                std::cout << count << '\n';
        }
    }

    return 0;
}
我们可以这样写
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // if the number is divisible by 4, skip this iteration
        if ((count % 4) == 0)
            continue;

        // no nested block needed

        std::cout << count << '\n';
    }

    return 0;
}
最小化使用的变量数量并减少嵌套块的数量都比
break
或
continue
损害代码可理解性更有益。因此，我们认为 judiciously 使用
break
或
continue
是可以接受的。
最佳实践
当
break
和
continue
简化你的循环逻辑时使用它们。
关于提前返回的争论
对于 return 语句也有类似的论点。不是函数中最后一条语句的 return 语句称为
提前返回
。许多程序员认为应该避免提前返回。只在函数底部有一个 return 语句的函数具有简单性——你可以假设函数将接收其参数，执行其已实现的任何逻辑，并返回结果而不会出现偏差。拥有额外的返回会使逻辑复杂化。
反驳的论点是，使用提前返回允许你的函数在完成后立即退出，这减少了阅读不必要的逻辑的需要，并最大限度地减少了条件嵌套块的需要，这使得你的代码更具可读性。
一些开发人员采取中间立场，只在函数顶部使用提前返回来执行参数验证（捕获传入的错误参数），然后只有一个 return。
我们的立场是，提前返回利大于弊，但我们认识到这种做法有点艺术性。
最佳实践
当它们简化你的函数逻辑时使用提前返回。
下一课
8.12
停止（提前退出程序）
返回目录
上一课
8.10
For 语句