# 22.5 — std::string 赋值和交换

22.5 — std::string 赋值和交换
Alex
2010 年 7 月 18 日，下午 2:21 PDT
2022 年 9 月 16 日
字符串赋值
给字符串赋值最简单的方法是使用重载的 operator= 函数。还有一个 assign() 成员函数，它也具有部分相同的功能。
string& string::operator= (const string& str)
string& string::assign (const string& str)
string& string::operator= (const char* str)
string& string::assign (const char* str)
string& string::operator= (char c)
这些函数将各种类型的值赋给字符串。
这些函数返回 *this，因此可以“链式调用”。
请注意，没有接受单个 char 的 assign() 函数。
示例代码
std::string sString;

// Assign a string value
sString = std::string("One");
std::cout << sString << '\n';

const std::string sTwo("Two");
sString.assign(sTwo);
std::cout << sString << '\n';

// Assign a C-style string
sString = "Three";
std::cout << sString << '\n';

sString.assign("Four");
std::cout << sString << '\n';

// Assign a char
sString = '5';
std::cout << sString << '\n';

// Chain assignment
std::string sOther;
sString = sOther = "Six";
std::cout << sString << ' ' << sOther << '\n';
输出
One
Two
Three
Four
5
Six Six
assign() 成员函数还有其他几种形式
string& string::assign (const string& str, size_type index, size_type len)
赋值 str 的子字符串，从 index 开始，长度为 len
如果 index 超出范围，则抛出 out_of_range 异常
返回 *this，因此可以被“链式调用”。
示例代码
const std::string sSource("abcdefg");
std::string sDest;

sDest.assign(sSource, 2, 4); // assign a substring of source from index 2 of length 4
std::cout << sDest << '\n';
输出
cdef
string& string::assign (const char* chars, size_type len)
从 C 风格数组 chars 中赋值 len 个字符
如果结果超过最大字符数，则抛出 length_error 异常
返回 *this，因此可以被“链式调用”。
示例代码
std::string sDest;

sDest.assign("abcdefg", 4);
std::cout << sDest << '\n';
输出
abcd
此函数具有潜在危险性，不建议使用。
string& string::assign (size_type len, char c)
赋值 len 个字符 c
如果结果超过最大字符数，则抛出 length_error 异常
返回 *this，因此可以被“链式调用”。
示例代码
std::string sDest;

sDest.assign(4, 'g');
std::cout << sDest << '\n';
输出
gggg
交换
如果您有两个字符串并希望交换它们的值，可以使用两个名为 swap() 的函数。
void string::swap (string& str)
void swap (string& str1, string& str2)
这两个函数都交换两个字符串的值。成员函数交换 *this 和 str，全局函数交换 str1 和 str2。
这些函数效率很高，应该用于执行字符串交换，而不是赋值。
示例代码
std::string sStr1("red");
std::string sStr2("blue");

std::cout << sStr1 << ' ' << sStr2 << '\n';
swap(sStr1, sStr2);
std::cout << sStr1 << ' ' << sStr2 << '\n';
sStr1.swap(sStr2);
std::cout << sStr1 << ' ' << sStr2 << '\n';
输出
red blue
blue red
red blue
下一课
22.6
std::string 字符串追加
返回目录
上一课
22.4
std::string 字符访问和转换为 C 风格数组