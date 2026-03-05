# 4.10 — if 语句简介

4.10 — if 语句简介
Alex
2019年4月23日，太平洋夏令时下午12:57
2025年2月11日
假设你要去市场，你的室友告诉你：“如果草莓打折，就买一些”。这是一个条件语句，意味着你只有在条件（“草莓打折”）为真时才执行某个动作（“买一些”）。
这种条件在编程中很常见，因为它们允许我们在程序中实现条件行为。C++ 中最简单的条件语句叫做
if 语句
。
if 语句
允许我们仅在某个条件为真时执行一行（或多行）代码。
最简单的
if 语句
形式如下：
if (condition) true_statement;
为了可读性，这通常写成如下形式：
if (condition)
    true_statement;
条件
（也称为
条件表达式
）是一个求值为布尔值的表达式。
如果
if 语句
的
条件
求值为布尔值
true
，则执行
true_statement
。如果
条件
求值为布尔值
false
，则跳过
true_statement
。
使用 if 语句的示例程序
给定以下程序：
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x == 0)
        std::cout << "The value is zero\n";

    return 0;
}
这是该程序的一次运行输出：
Enter an integer: 0
The value is zero
让我们更详细地研究一下这是如何工作的。
首先，用户输入一个整数。然后评估条件
x == 0
。
相等运算符
(==) 用于测试两个值是否相等。运算符 == 返回
true
如果操作数相等，返回
false
如果它们不相等。由于
x
的值为 0，并且
0 == 0
为真，因此此表达式求值为
true
。
因为条件求值为
true
，所以后续语句执行，打印
The value is zero
。
这是该程序的另一次运行：
Enter an integer: 5
在这种情况下，
x == 0
求值为
false
。后续语句被跳过，程序结束，没有打印其他内容。
警告
If 语句
仅有条件地执行单个语句。我们将在课程
8.2 -- if 语句和块
中讨论如何有条件地执行多个语句。
If-else
根据上面的示例，如果我们想告诉用户他们输入的数字是非零的怎么办？
我们可以这样写：
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x == 0)
        std::cout << "The value is zero\n";
    if (x != 0)
        std::cout << "The value is non-zero\n";

    return 0;
}
或者这样：
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    bool zero { (x == 0) };
    if (zero)
        std::cout << "The value is zero\n";
    if (!zero)
        std::cout << "The value is non-zero\n";

    return 0;
}
这两个程序都比它们实际需要的更复杂。相反，我们可以使用
if 语句
的另一种形式，称为
if-else
。
If-else
形式如下：
if (condition)
    true_statement;
else
    false_statement;
如果
条件
求值为布尔值 true，则执行
true_statement
。否则执行
false_statement
。
让我们修改之前的程序以使用
if-else
。
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x == 0)
        std::cout << "The value is zero\n";
    else
        std::cout << "The value is non-zero\n";

    return 0;
}
现在我们的程序将产生以下输出：
Enter an integer: 0
The value is zero
Enter an integer: 5
The value is non-zero
链式 if 语句
有时我们想按顺序检查几个条件的真假。我们可以通过将一个
if-statement
（或
if-else
）链接到之前的
if-else
来实现，如下所示：
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x > 0)
        std::cout << "The value is positive\n";
    else if (x < 0)
        std::cout << "The value is negative\n";
    else 
        std::cout << "The value is zero\n";

    return 0;
}
小于运算符
(<) 用于测试一个值是否小于另一个值。类似地，
大于运算符
(>) 用于测试一个值是否大于另一个值。这两个运算符都返回布尔值。
这是该程序的几次运行输出：
Enter an integer: 4
The value is positive
Enter an integer: -3
The value is negative
Enter an integer: 0
The value is zero
请注意，您可以根据要评估的条件，多次链接
if 语句
。我们将在测验中看到一个有用的示例。
布尔返回值和 if 语句
在上一课（
4.9 -- 布尔值
）中，我们编写了这个使用返回布尔值的函数的程序：
#include <iostream>
 
// returns true if x and y are equal, false otherwise
bool isEqual(int x, int y)
{
    return x == y; // operator== returns true if x equals y, and false otherwise
}
 
int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;
 
    std::cout << "Enter another integer: ";
    int y {};
    std::cin >> y;
 
    std::cout << std::boolalpha; // print bools as true or false
    
    std::cout << x << " and " << y << " are equal? ";
    std::cout << isEqual(x, y); // will return true or false

    std::cout << '\n';
 
    return 0;
}
让我们使用
if 语句
改进这个程序：
#include <iostream>
 
// returns true if x and y are equal, false otherwise
bool isEqual(int x, int y)
{
    return x == y; // operator== returns true if x equals y, and false otherwise
}
 
int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;
 
    std::cout << "Enter another integer: ";
    int y {};
    std::cin >> y;
    
    if (isEqual(x, y))
        std::cout << x << " and " << y << " are equal\n";
    else
        std::cout << x << " and " << y << " are not equal\n";

    return 0;
}
该程序的两次运行：
Enter an integer: 5
Enter another integer: 5
5 and 5 are equal
Enter an integer: 6
Enter another integer: 4
6 and 4 are not equal
在这种情况下，我们的条件表达式只是一个对函数
isEqual
的函数调用，它返回一个布尔值。
非布尔条件
在以上所有示例中，我们的条件要么是布尔值（
true
或
false
）、布尔变量，要么是返回布尔值的函数。如果您的条件是一个不求值为布尔值的表达式会发生什么？
在这种情况下，条件表达式的结果会转换为布尔值：非零值转换为布尔
true
，零值转换为布尔
false
。
因此，如果我们这样做：
#include <iostream>

int main()
{
    int x { 4 };
    if (x) // nonsensical, but for the sake of example...
        std::cout << "hi\n";
    else
        std::cout << "bye\n";

    return 0;
}
这将打印
hi
，因为
x
的值为
4
，而
4
是一个非零值，它会转换为布尔
true
，从而导致条件后的语句执行。
关键见解
if (x)
意味着“如果 x 非零/非空”。
If-语句和提前返回
函数中不是最后一条语句的 return 语句称为
提前返回
。这样的语句将导致函数在 return 语句执行时返回给调用者（在函数本来会返回给调用者之前，因此称为“提前”）。
无条件的提前返回没有用处
void print()
{
    std::cout << "A" << '\n';

    return; // the function will always return to the caller here

    std::cout << "B" << '\n'; // this will never be printed
}
由于
std::cout << "B" << '\n';
永远不会执行，我们不妨将其删除，这样我们的
return
语句就不再是提前返回了。
然而，当与 if 语句结合使用时，提前返回提供了一种条件化函数返回值的方法。
#include <iostream>

// returns the absolute value of x
int abs(int x) 
{
    if (x < 0)
        return -x; // early return (only when x < 0)

    return x;
}

int main()
{
    std::cout << abs(4) << '\n'; // prints 4
    std::cout << abs(-3) << '\n'; // prints 3

    return 0;
}
当调用
abs(4)
时，
x
的值为
4
。
if (x < 0)
为 false，因此提前返回不执行。函数在函数末尾将
x
（值
4
）返回给调用者。
当调用
abs(-3)
时，
x
的值为
-3
。
if (x < 0)
为 true，因此提前返回执行。函数此时将
-x
（值
3
）返回给调用者。
历史上，提前返回是不受欢迎的。然而，在现代编程中，它们更被接受，特别是当它们可以使函数更简单，或者用于由于某些错误条件而提前中止函数时。
相关内容
我们将在课程
8.11 -- break 和 continue
中进一步讨论关于提前返回的争论
我们将在未来的课程
8.2 -- If 语句和块
中继续探索 if-语句。
小测验时间
问题 #1
什么是提前返回，它的行为是什么？
显示答案
提前返回是函数中在最后一行之前出现的 return 语句。它导致函数立即返回给调用者。
问题 #2
质数是大于 1 且只能被 1 和自身整除的整数。编写一个程序，要求用户输入一个 0 到 9（包括 0 和 9）之间的数字。如果用户输入的是该范围内的质数（2、3、5 或 7），则打印“The digit is prime”。否则，打印“The digit is not prime”。
显示提示
提示：使用一系列
if-else 语句
将用户输入的数字与质数进行比较，看是否匹配。
显示答案
#include <iostream>

bool isPrime(int x)
{
    if (x == 2) // if user entered 2, the digit is prime
        return true;
    else if (x == 3) // if user entered 3, the digit is prime
        return true;
    else if (x == 5) // if user entered 5, the digit is prime
        return true;
    else if (x == 7) // if user entered 7, the digit is prime
        return true;

    return false; // if the user did not enter 2, 3, 5, 7, the digit must not be prime
}

int main()
{
    std::cout << "Enter a number 0 through 9: ";
    int x {};
    std::cin >> x;

    if ( isPrime(x) )
        std::cout << "The digit is prime\n";
    else
        std::cout << "The digit is not prime\n";

    return 0;
}
致进阶读者
如果上面的
isPrime()
函数看起来有点冗长/重复——确实如此。我们可以使用一些我们将在未来课程中解释的概念，更紧凑和高效地编写
isPrime()
。
使用逻辑或 (||) 运算符 (
6.8 -- 逻辑运算符
)
bool isPrime(int x)
{
    return x == 2 || x == 3 || x == 5 || x == 7; // if user entered 2 or 3 or 5 or 7 the digit is prime
}
使用 switch 语句 (
8.5 -- switch 语句基础
)
bool isPrime(int x)
{
    switch (x)
    {
        case 2: // if the user entered 2
        case 3: // or if the user entered 3
        case 5: // or if the user entered 5
        case 7: // or if the user entered 7
            return true; // then the digit is prime
    }

    return false; // otherwise the digit must not be prime
}
问题 #3
如何在不改变格式的情况下减少以下代码的长度？
#include <iostream>

bool isAllowedToTakeFunRide()
{
  std::cout << "How tall are you? (cm)\n";

  double height{};
  std::cin >> height;

  if (height >= 140.0)
    return true;
  else
    return false;
}

int main()
{
  if (isAllowedToTakeFunRide())
    std::cout << "Have fun!\n";
  else
    std::cout << "Sorry, you're too short.\n";

  return 0;
}
显示答案
我们不需要
isAllowedToTakeFunRide()
中的 if 语句。表达式
height >= 140.0
求值为一个
bool
值，可以直接返回。
bool isAllowedToTakeFunRide()
{
  std::cout << "How tall are you? (cm)\n";

  double height{};
  std::cin >> height;

  return height >= 140.0;
}
你永远不需要以下形式的 if 语句：
if (condition)
  return true;
else
  return false;
这可以被单个语句
return condition
替换。
下一课
4.11
字符
返回目录
上一课
4.9
布尔值