# 28.2 — 使用 istream 进行输入

28.2 — 使用 istream 进行输入
Alex
2008 年 3 月 4 日，下午 4:09 PST
2024 年 12 月 23 日
iostream 库相当复杂——因此我们无法在本教程中完全涵盖它。但是，我们将向您展示最常用的功能。在本节中，我们将介绍输入类 (istream) 的各个方面。
提取运算符
如许多课程所示，我们可以使用提取运算符 (>>) 从输入流中读取信息。C++ 为所有内置数据类型预定义了提取操作，您已经了解了如何为自己的类
重载提取运算符
。
当读取字符串时，提取运算符的一个常见问题是如何防止输入溢出缓冲区。考虑到以下示例
char buf[10]{};
std::cin >> buf;
如果用户输入 18 个字符会发生什么？缓冲区溢出，然后就会发生不好的事情。一般来说，对用户将输入多少个字符做任何假设都是一个坏主意。
处理这个问题的一种方法是使用操纵符。
操纵符
是一个对象，当与提取 (>>) 或插入 (<<) 运算符一起使用时，用于修改流。您已经使用过的一个操纵符是“std::endl”，它既打印换行符又刷新任何缓冲输出。C++ 提供了一个名为
setw
（在 iomanip 头文件中）的操纵符，可用于限制从流中读取的字符数。要使用 setw()，只需提供要读取的最大字符数作为参数，并将其插入到您的输入语句中，如下所示
#include <iomanip>
char buf[10]{};
std::cin >> std::setw(10) >> buf;
此程序现在将只从流中读取前 9 个字符（为终止符留出空间）。任何剩余的字符将保留在流中，直到下一次提取。
提取和空白符
提醒一下，提取运算符会跳过空白符（空格、制表符和换行符）。
请看以下程序
int main()
{
    char ch{};
    while (std::cin >> ch)
        std::cout << ch;

    return 0;
}
当用户输入以下内容时
Hello my name is Alex
提取运算符会跳过空格和换行符。因此，输出是
HellomynameisAlex
通常，您会希望获取用户输入但不丢弃空白符。为此，istream 类提供了许多可用于此目的的函数。
最有用的是
get()
函数，它只是从输入流中获取一个字符。这是上面使用 get() 的相同程序
int main()
{
    char ch{};
    while (std::cin.get(ch))
        std::cout << ch;

    return 0;
}
现在当我们使用输入时
Hello my name is Alex
输出是
Hello my name is Alex
get() 还有一个字符串版本，它接受要读取的最大字符数
int main()
{
    char strBuf[11]{};
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';

    return 0;
}
如果我们输入
Hello my name is Alex
输出是
Hello my n
请注意，我们只读取了前 10 个字符（我们必须为终止符留一个字符）。剩余的字符保留在输入流中。
关于 get() 需要注意的一件重要事情是它不读取换行符！这可能会导致一些意想不到的结果
int main()
{
    char strBuf[11]{};
    // Read up to 10 characters
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';

    // Read up to 10 more characters
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';
    return 0;
}
如果用户输入
Hello!
程序将打印
Hello!
然后终止！为什么它不再要求 10 个字符了呢？答案是因为第一个 get() 读取到换行符然后停止了。第二个 get() 发现 cin 流中仍然有输入并尝试读取它。但第一个字符是换行符，所以它立即停止了。
因此，还有一个名为
getline()
的函数，其工作方式类似于 get()，但会提取（并丢弃）分隔符。
int main()
{
    char strBuf[11]{};
    // Read up to 10 characters
    std::cin.getline(strBuf, 11);
    std::cout << strBuf << '\n';

    // Read up to 10 more characters
    std::cin.getline(strBuf, 11);
    std::cout << strBuf << '\n';
    return 0;
}
即使用户输入包含换行符的字符串，此代码也会按预期执行。
如果您需要知道上次调用 getline() 提取了多少个字符，请使用
gcount()
int main()
{
    char strBuf[100]{};
    std::cin.getline(strBuf, 100);
    std::cout << strBuf << '\n';
    std::cout << std::cin.gcount() << " characters were read" << '\n';

    return 0;
}
gcount() 包括任何已提取和已丢弃的分隔符。
std::string 的特殊版本 getline()
有一个特殊版本的 getline() 存在于 istream 类之外，用于读取 std::string 类型的变量。这个特殊版本不是 ostream 或 istream 的成员，并包含在 string 头文件中。以下是其使用示例
#include <string>
#include <iostream>

int main()
{
    std::string strBuf{};
    std::getline(std::cin, strBuf);
    std::cout << strBuf << '\n';

    return 0;
}
更多有用的 istream 函数
您可能还需要使用一些其他有用的输入函数
ignore()
丢弃流中的第一个字符。
ignore(int nCount)
丢弃前 nCount 个字符。
peek()
允许您从流中读取一个字符，而无需将其从流中删除。
unget()
将最后读取的字符返回到流中，以便下一次调用可以再次读取它。
putback(char ch)
允许您将自己选择的字符放回流中，以便下一次调用读取。
istream 包含许多其他函数以及上述函数的变体，这些函数可能很有用，具体取决于您需要做什么。您可以在参考网站（例如
https://cppreference.cn/w/cpp/io/basic_istream
）上找到这些函数。
下一课
28.3
使用 ostream 和 ios 进行输出
返回目录
上一课
28.1
输入和输出 (I/O) 流