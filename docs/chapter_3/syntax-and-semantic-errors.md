# 3.1 — 语法错误和语义错误

3.1 — 语法错误和语义错误
Alex
2019年2月1日, 11:53 am PST
2024年9月4日
软件错误无处不在。犯错容易，找错难。在本章中，我们将探讨与查找和移除 C++ 程序中的 bug 相关的主题，包括学习如何使用 IDE 中集成的调试器。
尽管调试工具和技术并非 C++ 标准的一部分，但学会查找和修复自己所写程序中的 bug，是成为一名成功程序员极为重要的一环。因此，我们将花一些时间来介绍这些主题，这样随着你编写的程序越来越复杂，你诊断和解决问题的能力也能同步提升。
如果你有调试其他编程语言程序的经验，那么这些内容对你来说会很熟悉。
语法错误
编程可能具有挑战性，而 C++ 又是一门有些古怪的语言。这两者结合在一起，就有很多犯错的方式。错误通常分为两类：语法错误和语义错误（逻辑错误）。
当你编写的语句不符合 C++ 语言的语法规则时，就会发生
语法错误 (syntax error)
。这包括缺少分号、括号或花括号不匹配等错误。例如，下面的程序包含相当多的语法错误：
#include <iostream>

int main( // missing closing brace
{
    int 1x; // variable name can't start with number
    std::cout << "Hi there"; << x +++ << '\n'; // extraneous semicolon, operator+++ does not exist
    return 0 // missing semicolon at end of statement
}
幸运的是，编译器会检测到语法错误并发出编译警告或错误，因此你可以轻松地识别和修复问题。然后，你只需不断地重新编译，直到消除所有错误为止。
语义错误
语义错误 (semantic error)
是指意义上的错误。当一条语句在语法上有效，但违反了语言的其他规则，或者没有实现程序员的意图时，就会发生这种错误。
某些语义错误可以被编译器捕捉到。常见的例子包括使用未声明的变量、类型不匹配（在某个地方使用了错误类型的对象）等等。
例如，下面的程序包含几个编译时语义错误：
int main()
{
    5 = x; // x not declared, cannot assign a value to 5
    return "hello"; // "hello" cannot be converted to an int
}
其他语义错误只在运行时才会显现。有时这些错误会导致你的程序崩溃，例如除以零的情况：
#include <iostream>

int main()
{
    int a { 10 };
    int b { 0 };
    std::cout << a << " / " << b << " = " << a / b << '\n'; // division by 0 is undefined in mathematics
    return 0;
}
更常见的情况是，它们只会产生错误的值或行为：
#include <iostream>

int main()
{
    int x; // no initializer provided
    std::cout << x << '\n'; // Use of uninitialized variable leads to undefined result

    return 0;
}
或
#include <iostream>

int add(int x, int y) // this function is supposed to perform addition
{
    return x - y; // but it doesn't due to the wrong operator being used
}

int main()
{
    std::cout << "5 + 3 = " << add(5, 3) << '\n'; // should produce 8, but produces 2

    return 0;
}
或
#include <iostream>

int main()
{
    return 0; // function returns here

    std::cout << "Hello, world!\n"; // so this never executes
}
在上面的例子中，错误相当容易发现。但在大多数不那么简单的程序中，运行时语义错误很难通过肉眼检查代码找到。这时，调试技巧就能派上用场了。
下一课
3.2
调试过程
返回目录
上一课
2.x
第 2 章总结与测验