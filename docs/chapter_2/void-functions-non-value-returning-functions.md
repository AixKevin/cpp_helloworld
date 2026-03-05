# 2.3 — Void 函数（无返回值函数）

2.3 — Void 函数（无返回值函数）
Alex
2022 年 4 月 15 日，太平洋夏令时下午 5:19
2023 年 10 月 23 日
在之前的课程（
2.1 -- 函数简介
）中，我们指出函数定义的语法如下
returnType identifier() // identifier replaced with the name of your function
{
// Your code here
}
虽然我们展示了返回类型为
void
的函数的例子，但我们没有讨论这意味着什么。在本课中，我们将探讨返回类型为
void
的函数。
Void 返回值
函数不需要向调用者返回值。要告诉编译器一个函数不返回值，可以使用返回类型
void
。例如
#include <iostream>

// void means the function does not return a value to the caller
void printHi()
{
    std::cout << "Hi" << '\n';

    // This function does not return a value so no return statement is needed
}

int main()
{
    printHi(); // okay: function printHi() is called, no value is returned

    return 0;
}
在上面的例子中，
printHi
函数有一个有用的行为（它打印“Hi”），但它不需要向调用者返回任何东西。因此，
printHi
被赋予了
void
返回类型。
当
main
调用
printHi
时，
printHi
中的代码执行，并打印“Hi”。在
printHi
结束时，控制权返回到
main
，程序继续执行。
不返回值的函数称为
无返回值函数
（或
void 函数
）。
Void 函数不需要 return 语句
void 函数会在函数结束时自动返回给调用者。不需要 return 语句。
return 语句（没有返回值）可以在 void 函数中使用——这样的语句会导致函数在 return 语句执行的点返回给调用者。这与函数结束时发生的情况相同。因此，在 void 函数的末尾放置一个空的 return 语句是多余的
#include <iostream>

// void means the function does not return a value to the caller
void printHi()
{
    std::cout << "Hi" << '\n';

    return; // tell compiler to return to the caller -- this is redundant since the return will happen at the end of the function anyway!
} // function will return to caller here

int main()
{
    printHi();

    return 0;
}
最佳实践
不要在无返回值函数的末尾放置 return 语句。
Void 函数不能用于需要值的表达式
某些类型的表达式需要值。例如
#include <iostream>

int main()
{
    std::cout << 5; // ok: 5 is a literal value that we're sending to the console to be printed
    std::cout << ;  // compile error: no value provided

    return 0;
}
在上面的程序中，要打印的值需要在
std::cout <<
的右侧提供。如果没有提供值，编译器将产生语法错误。由于对
std::cout
的第二次调用没有提供要打印的值，这会导致错误。
现在考虑以下程序
#include <iostream>

// void means the function does not return a value to the caller
void printHi()
{
    std::cout << "Hi" << '\n';
}

int main()
{
    printHi(); // okay: function printHi() is called, no value is returned

    std::cout << printHi(); // compile error

    return 0;
}
对
printHi()
的第一次调用是在不需要值的上下文中进行的。由于函数不返回值，这没问题。
对函数
printHi()
的第二次函数调用甚至不会编译。函数
printHi
的返回类型是
void
，这意味着它不返回值。但是，此语句试图将
printHi
的返回值发送到
std::cout
进行打印。
std::cout
不知道如何处理此情况（它会输出什么值？）。因此，编译器会将其标记为错误。您需要注释掉这行代码才能使您的代码编译。
提示
有些语句需要提供值，有些则不需要。
当我们的语句只包含函数调用时（例如上面示例中的第一个
printHi()
），我们是为了其行为而不是返回值而调用函数。在这种情况下，我们可以调用无返回值函数，或者我们可以调用有返回值函数并忽略返回值。
当我们在需要值的上下文中调用函数时（例如
std::cout
），必须提供一个值。在这种上下文中，我们只能调用有返回值函数。
#include <iostream>

// Function that does not return a value
void returnNothing()
{
}

// Function that returns a value
int returnFive()
{
    return 5;
}

int main()
{
    // When calling a function by itself, no value is required
    returnNothing(); // ok: we can call a function that does not return a value
    returnFive();    // ok: we can call a function that returns a value, and ignore that return value

    // When calling a function in a context that requires a value (like std::cout)
    std::cout << returnFive();    // ok: we can call a function that returns a value, and the value will be used
    std::cout << returnNothing(); // compile error: we can't call a function that returns void in this context

    return 0;
}
从 void 函数返回值是编译错误
尝试从无返回值函数返回值将导致编译错误
void printHi() // This function is non-value returning
{
    std::cout << "In printHi()" << '\n';

    return 5; // compile error: we're trying to return a value
}
小测验时间
问题 #1
检查以下程序并说明它们输出什么，或者它们是否不会编译。
1a)
#include <iostream>

void printA()
{
    std::cout << "A\n";
}

void printB()
{
    std::cout << "B\n";
}

int main()
{
    printA();
    printB();

    return 0;
}
显示答案
此程序在单独的行上打印字母 A 和 B。
1b)
#include <iostream>

void printA()
{
    std::cout << "A\n";
}

int main()
{
    std::cout << printA() << '\n';

    return 0;
}
显示答案
此程序无法编译。函数
printA()
返回
void
，不能发送到
std::cout
进行打印。这将产生编译错误。
下一课
2.4
函数参数和实参简介
返回目录
上一课
2.2
函数返回值（有返回值函数）