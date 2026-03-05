# 22.6 — std::string 拼接

22.6 — std::string 拼接
Alex
2010 年 7 月 18 日，下午 3:35 PDT
2022 年 8 月 24 日
拼接
使用 operator+=、append() 或 push_back() 可以轻松地将字符串拼接到一个现有字符串的末尾。
string& string::operator+= (const string& str)
string& string::append (const string& str)
这两个函数将 str 中的字符拼接追加到字符串中。
这两个函数都返回 *this，因此它们可以被“链式调用”。
如果结果超出最大字符数，这两个函数都会抛出 length_error 异常。
示例代码
std::string sString{"one"};

sString += std::string{" two"};

std::string sThree{" three"};
sString.append(sThree);

std::cout << sString << '\n';
输出
one two three
还有一种 append() 的变体可以拼接子字符串
string& string::append (const string& str, size_type index, size_type num)
此函数将 str 中从 index 开始的 num 个字符拼接追加到字符串中。
返回 *this，因此可以被“链式调用”。
如果 index 超出范围，则抛出 out_of_range 异常。
如果结果超出最大字符数，则抛出 length_error 异常。
示例代码
std::string sString{"one "};

const std::string sTemp{"twothreefour"};
sString.append(sTemp, 3, 5); // append substring of sTemp starting at index 3 of length 5
std::cout << sString << '\n';
输出
one three
Operator+= 和 append() 也有适用于 C 风格字符串的版本
string& string::operator+= (const char* str)
string& string::append (const char* str)
这两个函数将 str 中的字符拼接追加到字符串中。
这两个函数都返回 *this，因此它们可以被“链式调用”。
如果结果超出最大字符数，这两个函数都会抛出 length_error 异常。
str 不应为 NULL。
示例代码
std::string sString{"one"};

sString += " two";
sString.append(" three");
std::cout << sString << '\n';
输出
one two three
append() 还有一种适用于 C 风格字符串的附加变体
string& string::append (const char* str, size_type len)
将 str 的前 len 个字符拼接追加到字符串中。
返回 *this，因此可以被“链式调用”。
如果结果超出最大字符数，则抛出 length_error 异常。
忽略特殊字符（包括 ""）
示例代码
std::string sString{"one "};

sString.append("threefour", 5);
std::cout << sString << '\n';
输出
one three
此函数很危险，不建议使用。
还有一组用于拼接字符的函数。请注意，拼接字符的非运算符函数名称是 push_back()，而不是 append()！
string& string::operator+= (char c)
void string::push_back (char c)
这两个函数都将字符 c 拼接追加到字符串中。
运算符 += 返回 *this，因此可以被“链式调用”。
如果结果超出最大字符数，这两个函数都会抛出 length_error 异常。
示例代码
std::string sString{"one"};

sString += ' ';
sString.push_back('2');
std::cout << sString << '\n';
输出
one 2
现在你可能想知道为什么这个函数的名字是 push_back() 而不是 append()。这遵循了栈的命名约定，其中 push_back() 是将单个项添加到栈尾的函数。如果你将字符串设想为字符的栈，那么使用 push_back() 在末尾添加单个字符是有意义的。然而，在我看来，缺乏 append() 函数是不一致的！
事实证明，有一个适用于字符的 append() 函数，它看起来像这样
string& string::append (size_type num, char c)
将字符 c 的 num 次出现添加到字符串中
返回 *this，因此可以被“链式调用”。
如果结果超出最大字符数，则抛出 length_error 异常。
示例代码
std::string sString{"aaa"};

sString.append(4, 'b');
std::cout << sString << '\n';
输出
aaabbbb
append() 还有一种最终的变体，它与迭代器一起使用
string& string::append (InputIterator start, InputIterator end)
拼接范围 [start, end) 中的所有字符（包括 start，但不包括 end）
返回 *this，因此可以被“链式调用”。
如果结果超出最大字符数，则抛出 length_error 异常。
下一课
22.7
std::string 插入
返回目录
上一课
22.5
std::string 赋值和交换