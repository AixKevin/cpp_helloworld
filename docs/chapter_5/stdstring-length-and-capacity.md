# 22.3 — std::string 长度和容量

22.3 — std::string 长度和容量
Alex
2009 年 9 月 27 日上午 10:09 (PDT)
2022 年 8 月 15 日
创建字符串后，了解它们的长度通常很有用。这就是长度和容量操作发挥作用的地方。我们还将讨论将 std::string 转换回 C 风格字符串的各种方法，以便您可以将它们与需要 char* 类型字符串的函数一起使用。
字符串的长度
字符串的长度非常简单——它是字符串中的字符数。有两种相同的函数用于确定字符串长度
size_type string::length() const
size_type string::size() const
这两个函数都返回字符串中当前的字符数，不包括空终止符。
示例代码
std::string s { "012345678" };
std::cout << s.length() << '\n';
输出
9
尽管可以使用 length() 来确定字符串是否包含任何字符，但使用 empty() 函数更有效
bool string::empty() const
如果字符串没有字符，则返回 true，否则返回 false。
示例代码
std::string string1 { "Not Empty" };
std::cout << (string1.empty() ? "true" : "false") << '\n';
std::string string2; // empty
std::cout << (string2.empty() ? "true" : "false")  << '\n';
输出
false
true
还有一个与大小相关的函数，您可能永远不会使用，但为了完整起见，我们将其包含在此处
size_type string::max_size() const
返回字符串允许拥有的最大字符数。
此值将根据操作系统和系统架构而异。
示例代码
std::string s { "MyString" };
std::cout << s.max_size() << '\n';
输出
4294967294
字符串的容量
字符串的容量反映了字符串分配了多少内存来保存其内容。此值以字符串字符为单位衡量，不包括 NULL 终止符。例如，容量为 8 的字符串可以容纳 8 个字符。
size_type string::capacity() const
返回字符串在不重新分配的情况下可以容纳的字符数。
示例代码
std::string s { "01234567" };
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';
输出
Length: 8
Capacity: 15
请注意，容量高于字符串的长度！尽管我们的字符串长度为 8，但字符串实际上分配了足够的内存来容纳 15 个字符！为什么会这样？
这里要认识到的重要一点是，如果用户想要在字符串中放入比字符串容量更多的字符，则字符串必须重新分配到更大的容量。例如，如果字符串的长度和容量都为 8，那么向字符串添加任何字符都会强制重新分配。通过使容量大于实际字符串，这为用户提供了一些缓冲区空间，可以在需要重新分配之前扩展字符串。
事实证明，重新分配有很多缺点
首先，重新分配字符串相对昂贵。首先，必须分配新内存。然后，字符串中的每个字符都必须复制到新内存中。如果字符串很大，这可能需要很长时间。最后，必须释放旧内存。如果您进行多次重新分配，此过程会显著降低程序的运行速度。
其次，每当字符串重新分配时，字符串的内容都会更改为新的内存地址。这意味着对字符串的所有引用、指针和迭代器都将失效！
请注意，字符串的分配容量不一定总是大于长度。考虑以下程序
std::string s { "0123456789abcde" };
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';
此程序输出
Length: 15
Capacity: 15
（结果可能因编译器而异）。
让我们向字符串添加一个字符并观察容量变化
std::string s("0123456789abcde");
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';

// Now add a new character
s += "f";
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';
这会产生结果
Length: 15
Capacity: 15
Length: 16
Capacity: 31
void string::reserve()
void string::reserve(size_type unSize)
此函数的第二种形式将字符串的容量设置为至少 unSize（可以更大）。请注意，这可能需要发生重新分配。
如果调用函数的第一种形式，或者第二种形式的 unSize 小于当前容量，则该函数将尝试缩小容量以匹配长度。此缩小容量的请求可能会被忽略，具体取决于实现。
示例代码
std::string s { "01234567" };
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';

s.reserve(200);
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';

s.reserve();
std::cout << "Length: " << s.length() << '\n';
std::cout << "Capacity: " << s.capacity() << '\n';
输出
Length: 8
Capacity: 15
Length: 8
Capacity: 207
Length: 8
Capacity: 207
这个例子展示了两个有趣的事情。首先，尽管我们请求的容量为 200，但我们实际得到的容量为 207。容量总是保证至少与您的请求一样大，但可能更大。然后我们请求容量更改以适应字符串。此请求被忽略，因为容量没有改变。
如果您事先知道您将通过进行大量会增加字符串大小的字符串操作来构造一个大型字符串，则可以通过从一开始就保留足够的容量来避免字符串多次重新分配
#include <iostream>
#include <string>
#include <cstdlib> // for rand() and srand()
#include <ctime> // for time()

int main()
{
    std::srand(std::time(nullptr)); // seed random number generator

    std::string s{}; // length 0
    s.reserve(64); // reserve 64 characters

    // Fill string up with random lower case characters
    for (int count{ 0 }; count < 64; ++count)
        s += 'a' + std::rand() % 26;

    std::cout << s;
}
这个程序的结果每次都会改变，但这是某个执行的输出
wzpzujwuaokbakgijqdawvzjqlgcipiiuuxhyfkdppxpyycvytvyxwqsbtielxpy
我们没有多次重新分配 s，而是只设置一次容量，然后填充字符串。这在通过连接构造大型字符串时可以极大地提高性能。
下一课
22.4
std::string 字符访问和转换为 C 风格数组
返回目录
上一课
22.2
std::string 的构造和析构