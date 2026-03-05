# 22.2 — std::string 的构造与析构

22.2 — std::string 的构造与析构
Alex
2009年9月20日，太平洋时间上午10:10
2023年6月15日
在本课程中，我们将学习如何构造 std::string 对象，以及如何将数字转换为字符串，反之亦然。
字符串构造
字符串类有许多构造函数可用于创建字符串。我们将在本节中逐一介绍它们。
注意：string::size_type 解析为 size_t，它是与 sizeof 运算符返回的相同无符号整数类型。size_t 的实际大小取决于环境。就本教程而言，将其视为无符号整型。
string::string()
这是默认构造函数。它创建一个空字符串。
示例代码
std::string sSource;
std::cout << sSource;
输出
string::string(const string& strString)
这是复制构造函数。此构造函数创建一个新字符串，作为 strString 的副本。
示例代码
std::string sSource{ "my string" };
std::string sOutput{ sSource };
std::cout << sOutput;
输出
my string
string::string(const string& strString, size_type unIndex)
string::string(const string& strString, size_type unIndex, size_type unLength)
此构造函数创建一个新字符串，该字符串包含 strString 中最多 unLength 个字符，从索引 unIndex 开始。如果遇到 NULL，字符串复制将结束，即使未达到 unLength 也会如此。
如果未提供 unLength，将使用从 unIndex 开始的所有字符。
如果 unIndex 大于字符串的大小，将抛出 out_of_range 异常。
示例代码
std::string sSource{ "my string" };
std::string sOutput{ sSource, 3 };
std::cout << sOutput<< '\n';
std::string sOutput2(sSource, 3, 4);
std::cout << sOutput2 << '\n';
输出
string
stri
string::string(const char* szCString)
此构造函数从 C 风格字符串 szCString 创建一个新字符串，直到但不包括 NULL 终止符。
如果结果大小超过最大字符串长度，将抛出 length_error 异常。
警告：
szCString 不得为 NULL。
示例代码
const char* szSource{ "my string" };
std::string sOutput{ szSource };
std::cout << sOutput << '\n';
输出
my string
string::string(const char* szCString, size_type unLength)
此构造函数从 C 风格字符串 szCString 的前 unLength 个字符创建一个新字符串。
如果结果大小超过最大字符串长度，将抛出 length_error 异常。
警告：
仅对于此函数，szCString 中的 NULL 不被视为字符串结束符！这意味着如果 unLength 过大，可能会读取字符串的末尾。请注意不要溢出字符串缓冲区！
示例代码
const char* szSource{ "my string" };
std::string sOutput(szSource, 4);
std::cout << sOutput << '\n';
输出
my s
string::string(size_type nNum, char chChar)
此构造函数创建一个新字符串，由字符 chChar 重复 nNum 次初始化。
如果结果大小超过最大字符串长度，将抛出 length_error 异常。
示例代码
std::string sOutput(4, 'Q');
std::cout << sOutput << '\n';
输出
QQQQ
模板
string::string(InputIterator itBeg, InputIterator itEnd)
此构造函数创建一个新字符串，由范围 [itBeg, itEnd) 中的字符初始化。
如果结果大小超过最大字符串长度，将抛出 length_error 异常。
没有此项的示例代码。它足够晦涩，你可能永远不会用到它。
string::~string()
字符串析构
这是析构函数。它销毁字符串并释放内存。
此处也没有示例代码，因为析构函数不会被显式调用。
从数字构造字符串
std::string 类的一个显著遗漏是无法从数字创建字符串。例如
std::string sFour{ 4 };
产生以下错误
c:vcprojectstest2test2test.cpp(10) : error C2664: 'std::basic_string<_Elem,_Traits,_Ax>::basic_string(std::basic_string<_Elem,_Traits,_Ax>::_Has_debug_it)' : cannot convert parameter 1 from 'int' to 'std::basic_string<_Elem,_Traits,_Ax>::_Has_debug_it'
还记得我说过字符串类会产生可怕的错误吗？这里相关的信息是
cannot convert parameter 1 from 'int' to 'std::basic_string
换句话说，它试图将你的 int 转换为字符串，但失败了。
将数字转换为字符串最简单的方法是使用 std::ostringstream 类。std::ostringstream 已经设置为接受来自各种来源的输入，包括字符、数字、字符串等……它也能够输出字符串（通过提取运算符 >> 或通过 str() 函数）。有关 std::ostringstream 的更多信息，请参阅
28.4 -- 字符串的流类
。
这是一个从各种输入类型创建 std::string 的简单解决方案
#include <iostream>
#include <sstream>
#include <string>
 
template <typename T>
inline std::string ToString(T tX)
{
    std::ostringstream oStream;
    oStream << tX;
    return oStream.str();
}
以下是一些用于测试的示例代码
int main()
{
    std::string sFour{ ToString(4) };
    std::string sSixPointSeven{ ToString(6.7) };
    std::string sA{ ToString('A') };
    std::cout << sFour << '\n';
    std::cout << sSixPointSeven << '\n';
    std::cout << sA << '\n';
}
以及输出
4
6.7
A
请注意，此解决方案省略了任何错误检查。将 tX 插入 oStream 可能会失败。适当的响应是如果转换失败则抛出异常。
相关内容
标准库还包含一个名为
std::to_string()
的函数，可用于将数字转换为 std::string。虽然这对于基本情况来说是一个更简单的解决方案，但 std::to_string 的输出可能与 std::cout 或我们上面 ToString() 函数的输出不同。其中一些差异目前记录在
此处
。
将字符串转换为数字
类似于上述解决方案
#include <iostream>
#include <sstream>
#include <string>
 
template <typename T>
inline bool FromString(const std::string& sString, T& tX)
{
    std::istringstream iStream(sString);
    return !(iStream >> tX).fail(); // extract value into tX, return success or not
}
以下是一些用于测试的示例代码
int main()
{
    double dX;
    if (FromString("3.4", dX))
        std::cout << dX << '\n'; 
    if (FromString("ABC", dX))
        std::cout << dX << '\n'; 
}
以及输出
3.4
请注意，第二次转换失败并返回 false。
下一课
22.3
std::string 的长度和容量
返回目录
上一课
22.1
std::string 和 std::wstring