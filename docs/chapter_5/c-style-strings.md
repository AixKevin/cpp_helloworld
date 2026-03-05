# 17.10 — C 风格字符串

17.10 — C 风格字符串
Alex
2007 年 7 月 9 日，下午 4:35 PDT
2024 年 5 月 25 日
在
17.7 课 —— C 风格数组简介
中，我们介绍了 C 风格数组，它允许我们定义元素的顺序集合
int testScore[30] {}; // an array of 30 ints, indices 0 through 29
在
5.2 课 —— 字面量
中，我们将字符串定义为字符的顺序集合（例如 “Hello, world!”），并介绍了 C 风格字符串字面量。我们还指出，C 风格字符串字面量 “Hello, world!” 的类型是
const char[14]
（13 个显式字符加上 1 个隐藏的空终止符）。
如果你之前没有把这些点联系起来，那么现在应该很明显了：C 风格字符串就是元素类型为
char
或
const char
的 C 风格数组！
尽管 C 风格字符串字面量在我们的代码中可以正常使用，但 C 风格字符串对象在现代 C++ 中已经不再受青睐，因为它们难以使用且危险（
std::string
和
std::string_view
是现代替代品）。尽管如此，你可能仍然会在旧代码中遇到 C 风格字符串对象的使用，我们如果不完全涵盖它们将是失职的。
因此，在本课中，我们将探讨现代 C++ 中 C 风格字符串对象最重要的几点。
定义 C 风格字符串
要定义 C 风格字符串变量，只需声明一个
char
（或
const char
/
constexpr char
）类型的 C 风格数组变量
char str1[8]{};                    // an array of 8 char, indices 0 through 7

const char str2[]{ "string" };     // an array of 7 char, indices 0 through 6
constexpr char str3[] { "hello" }; // an array of 6 const char, indices 0 through 5
请记住，我们需要一个额外的字符用于隐式空终止符。
当使用初始化器定义 C 风格字符串时，我们强烈建议省略数组长度，让编译器计算长度。这样，如果将来初始化器发生变化，您就不必记住更新长度，并且没有忘记包含一个额外元素来存放空终止符的风险。
C 风格字符串会“衰变”
在
17.8 课 —— C 风格数组衰变
中，我们讨论了 C 风格数组在大多数情况下如何衰变为指针。因为 C 风格字符串是 C 风格数组，所以它们也会衰变——C 风格字符串字面量衰变为
const char*
，C 风格字符串数组根据数组是否为 const 衰变为
const char*
或
char*
。当 C 风格字符串衰变为指针时，字符串的长度（编码在类型信息中）会丢失。
这种长度信息的丢失是 C 风格字符串具有空终止符的原因。字符串的长度可以通过计算字符串开头和空终止符之间的元素数量来（低效地）重新生成。
输出 C 风格字符串
当输出 C 风格字符串时，
std::cout
会一直输出字符，直到遇到空终止符。这个空终止符标记了字符串的结尾，这样衰变（已丢失长度信息）的字符串仍然可以被打印。
#include <iostream>

void print(char ptr[])
{
    std::cout << ptr << '\n'; // output string
}

int main()
{
    char str[]{ "string" };
    std::cout << str << '\n'; // outputs string

    print(str);

    return 0;
}
如果您尝试打印一个没有空终止符的字符串（例如，因为空终止符被某种方式覆盖了），结果将是未定义行为。在这种情况下，最可能的结果是字符串中的所有字符都被打印出来，然后它会继续打印相邻内存槽中的所有内容（被解释为字符），直到它碰巧遇到一个包含 0 的内存字节（这将解释为空终止符）！
输入 C 风格字符串
考虑这样一个情况：我们要求用户掷骰子任意多次，并输入掷出的数字，不带空格（例如
524412616
）。用户会输入多少个字符？我们不知道。
因为 C 风格字符串是固定大小的数组，所以解决方案是声明一个比我们可能需要的更大的数组
#include <iostream>

int main()
{
    char rolls[255] {}; // declare array large enough to hold 254 characters + null terminator
    std::cout << "Enter your rolls: ";
    std::cin >> rolls;
    std::cout << "You entered: " << rolls << '\n';

    return 0;
}
在 C++20 之前，
std::cin >> rolls
会尽可能多地提取字符到
rolls
（在第一个非前导空格处停止）。没有任何东西能阻止用户输入超过 254 个字符（无论是无意的还是恶意的）。如果发生这种情况，用户的输入将溢出
rolls
数组，并导致未定义行为。
关键见解
数组溢出
或
缓冲区溢出
是一种计算机安全问题，当将更多数据复制到存储区时，存储区无法容纳这些数据。在这种情况下，存储区之外的内存将被覆盖，导致未定义行为。恶意攻击者可能会利用此类漏洞来覆盖内存内容，希望以某种有利的方式改变程序的行为。
在 C++20 中，
operator>>
被修改为仅适用于输入未衰变的 C 风格字符串。这允许
operator>>
仅提取 C 风格字符串长度允许的字符数量，从而防止溢出。但这也意味着您不能再使用
operator>>
来输入衰变的 C 风格字符串。
使用
std::cin
读取 C 风格字符串的推荐方式如下
#include <iostream>
#include <iterator> // for std::size

int main()
{
    char rolls[255] {}; // declare array large enough to hold 254 characters + null terminator
    std::cout << "Enter your rolls: ";
    std::cin.getline(rolls, std::size(rolls));
    std::cout << "You entered: " << rolls << '\n';

    return 0;
}
对
cin.getline()
的此调用会将最多 254 个字符（包括空格）读入
rolls
。任何多余的字符都将被丢弃。因为
getline()
接受一个长度参数，我们可以提供要接受的最大字符数。对于未衰变的数组，这很容易——我们可以使用
std::size()
获取数组长度。对于衰变的数组，我们必须以其他方式确定长度。如果我们提供了错误的长度，我们的程序可能会出现故障或存在安全问题。
在现代 C++ 中，当存储用户输入的文本时，使用
std::string
更安全，因为
std::string
会自动调整以容纳所需的字符数。
修改 C 风格字符串
需要注意的一个重要点是，C 风格字符串遵循与 C 风格数组相同的规则。这意味着您可以在创建时初始化字符串，但此后不能使用赋值运算符为其赋值！
char str[]{ "string" }; // ok
str = "rope";           // not ok!
这使得使用 C 风格字符串有点笨拙。
由于 C 风格字符串是数组，您可以使用 [] 运算符更改字符串中的单个字符
#include <iostream>

int main()
{
    char str[]{ "string" };
    std::cout << str << '\n';
    str[1] = 'p';
    std::cout << str << '\n';

    return 0;
}
这个程序打印
string
spring
获取 C 风格字符串的长度
由于 C 风格字符串是 C 风格数组，您可以使用
std::size()
（或 C++20 中的
std::ssize()
）来获取字符串作为数组的长度。这里有两个注意事项：
这不适用于衰变（decayed）的字符串。
返回 C 风格数组的实际长度，而不是字符串的长度。
#include <iostream>

int main()
{
    char str[255]{ "string" }; // 6 characters + null terminator
    std::cout << "length = " << std::size(str) << '\n'; // prints length = 255

    char *ptr { str };
    std::cout << "length = " << std::size(ptr) << '\n'; // compile error

    return 0;
}
另一种解决方案是使用
strlen()
函数，它位于
头文件中。
strlen()
适用于衰变的数组，并返回所持字符串的长度，不包括空终止符
#include <cstring> // for std::strlen
#include <iostream>

int main()
{
    char str[255]{ "string" }; // 6 characters + null terminator
    std::cout << "length = " << std::strlen(str) << '\n'; // prints length = 6

    char *ptr { str };
    std::cout << "length = " << std::strlen(ptr) << '\n';   // prints length = 6

    return 0;
}
然而，
std::strlen()
速度很慢，因为它必须遍历整个数组，计算字符直到遇到空终止符。
其他 C 风格字符串操作函数
由于 C 风格字符串是 C 语言中的主要字符串类型，C 语言提供了许多用于操作 C 风格字符串的函数。这些函数已作为
头文件的一部分被 C++ 继承。
以下是您可能在旧代码中看到的一些最有用的函数
strlen() -- 返回 C 风格字符串的长度
strcpy(), strncpy(), strcpy_s() -- 用一个 C 风格字符串覆盖另一个 C 风格字符串
strcat(), strncat() -- 将一个 C 风格字符串附加到另一个 C 风格字符串的末尾
strcmp(), strncmp() -- 比较两个 C 风格字符串（如果相等则返回
0
）
除了
strlen()
，我们通常建议避免使用这些函数。
避免非 const C 风格字符串对象
除非您有特定且充分的理由使用非 const C 风格字符串，否则最好避免使用它们，因为它们操作起来很笨拙，而且容易发生越界，这将导致未定义行为（并可能导致安全问题）。
在您确实需要处理 C 风格字符串或固定缓冲区大小的极少数情况下（例如，对于内存受限的设备），我们建议使用经过良好测试的第三方固定长度字符串库，该库专为此目的而设计。
最佳实践
避免非 const C 风格字符串对象，而偏爱
std::string
。
小测验时间
问题 #1
编写一个函数，逐字符打印 C 风格字符串。使用指针和指针算术遍历字符串中的每个字符并打印该字符。编写一个
main
函数，用字符串字面量 “Hello, world!” 测试该函数。
显示答案
#include <iostream>

// str will point to the first letter of the C-style string.
// Note that str points to a const char, so we can not change the values it points to.
// However, we can point str at something else.  This does not change the value of the argument.
void printCString(const char str[])
{
    // While we haven't encountered a null terminator
    while (*str != '\0')
    {
        // print the current character
        std::cout << *str;

        // and use pointer arithmetic to move str to the next character
        ++str;
    }
}

int main()
{
    printCString("Hello world!");

    std::cout << '\n';

    return 0;
}
问题 #2
重复测验 #1，但这次函数应该倒序打印字符串。
显示答案
#include <iostream>

void printCStringBackwards(const char str[])
{
    // We can't modify str this time (we need it later)
    // So we'll define a new pointer with the same address as str
    const char *ptr{ str };

    // Find the null terminator
    while (*ptr != '\0')
        ++ptr;

    // Now walk backwards and print characters until ptr reaches str again
    while (ptr-- != str)
    {
        std::cout << *ptr;
    } 
}

int main()
{
    printCStringBackwards("Hello world!");

    std::cout << '\n';

    return 0;
}
下一课
17.11
C 风格字符串符号常量
返回目录
上一课
17.9
指针算术和下标