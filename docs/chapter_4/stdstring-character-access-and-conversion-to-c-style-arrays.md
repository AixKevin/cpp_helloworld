# 22.4 — std::string 字符访问和转换为 C 风格数组

22.4 — std::string 字符访问和转换为 C 风格数组
Alex
2009 年 10 月 4 日，上午 9:54 PDT
2022 年 9 月 16 日
字符访问
有两种几乎相同的方法来访问字符串中的字符。更易于使用且更快的版本是重载的运算符[]
char& string::operator[] (size_type nIndex)
const char& string::operator[] (size_type nIndex) const
这两个函数都返回索引为 nIndex 的字符
传递无效索引会导致未定义行为
因为 char& 是返回类型，所以您可以使用它来编辑数组中的字符
示例代码
std::string sSource{ "abcdefg" };
std::cout << sSource[5] << '\n';
sSource[5] = 'X';
std::cout << sSource << '\n';
输出
f
abcdeXg
还有一个非运算符版本。此版本速度较慢，因为它使用异常来检查 nIndex 是否有效。如果您不确定 nIndex 是否有效，则应使用此版本访问数组
char& string::at (size_type nIndex)
const char& string::at (size_type nIndex) const
这两个函数都返回索引为 nIndex 的字符
传递无效索引会导致 out_of_range 异常
因为 char& 是返回类型，所以您可以使用它来编辑数组中的字符
示例代码
std::string sSource{ "abcdefg" };
std::cout << sSource.at(5) << '\n';
sSource.at(5) = 'X';
std::cout << sSource << '\n';
输出
f
abcdeXg
转换为 C 风格数组
许多函数（包括所有 C 函数）都期望字符串格式为 C 风格字符串而不是 std::string。因此，std::string 提供了 3 种不同的方法将 std::string 转换为 C 风格字符串。
const char* string::c_str () const
将字符串内容作为 const C 风格字符串返回
会附加一个空终止符
C 风格字符串由 std::string 拥有，不应删除
示例代码
#include <cstring>

std::string sSource{ "abcdefg" };
std::cout << std::strlen(sSource.c_str());
输出
7
const char* string::data () const
将字符串内容作为 const C 风格字符串返回
会附加一个空终止符。此函数与
c_str()
执行相同的操作
C 风格字符串由 std::string 拥有，不应删除
示例代码
#include <cstring>

std::string sSource{ "abcdefg" };
const char* szString{ "abcdefg" };
// memcmp compares the first n characters of two C-style strings and returns 0 if they are equal
if (std::memcmp(sSource.data(), szString, sSource.length()) == 0)
    std::cout << "The strings are equal";
else
    std::cout << "The strings are not equal";
输出
The strings are equal
size_type string::copy(char* szBuf, size_type nLength, size_type nIndex = 0) const
这两个版本最多将字符串的 nLength 个字符复制到 szBuf，从字符 nIndex 开始
返回复制的字符数
不附加空字符。调用者负责确保 szBuf 初始化为 NULL 或使用返回的长度终止字符串
调用者负责不使 szBuf 溢出
示例代码
std::string sSource{ "sphinx of black quartz, judge my vow" };

char szBuf[20];
int nLength{ static_cast<int>(sSource.copy(szBuf, 5, 10)) };
szBuf[nLength] = '\0';  // Make sure we terminate the string in the buffer

std::cout << szBuf << '\n';
输出
black
应尽可能避免使用此函数，因为它相对危险（因为调用者负责提供空终止符并避免缓冲区溢出）。
下一课
22.5
std::string 赋值和交换
返回目录
上一课
22.3
std::string 长度和容量