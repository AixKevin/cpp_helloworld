# 22.7 — std::string 插入

22.7 — std::string 插入
Alex
2010 年 7 月 18 日，太平洋夏令时晚上 9:50
2021 年 8 月 26 日
插入
可以通过 insert() 函数将字符插入到现有字符串中。
string& string::insert (size_type index, const string& str)
string& string::insert (size_type index, const char* str)
这两个函数都将 str 中的字符插入到字符串的 index 位置。
这两个函数都返回 *this，因此可以“链式调用”。
如果 index 无效，这两个函数都会抛出 out_of_range 异常。
如果结果超过最大字符数，这两个函数都会抛出 length_error 异常。
在 C 风格字符串版本中，str 不能为 NULL。
示例代码
string sString("aaaa");
cout << sString << endl;

sString.insert(2, string("bbbb"));
cout << sString << endl;

sString.insert(4, "cccc");
cout << sString << endl;
输出
aaaa
aabbbbaa
aabbccccbbaa
这是一个疯狂的 insert() 版本，它允许您将子字符串插入到字符串的任意索引处。
string& string::insert (size_type index, const string& str, size_type startindex, size_type num)
此函数将从 startindex 开始的 str 中的 num 个字符插入到字符串的 index 位置。
返回 *this，因此可以被“链式调用”。
如果 index 或 startindex 超出范围，则抛出 out_of_range 异常。
如果结果超过最大字符数，则抛出 length_error 异常。
示例代码
string sString("aaaa");

const string sInsert("01234567");
sString.insert(2, sInsert, 3, 4); // insert substring of sInsert from index [3,7) into sString at index 2
cout << sString << endl;
输出
aa3456aa
insert() 有一种变体可以插入 C 风格字符串的第一部分。
string& string::insert(size_type index, const char* str, size_type len)
将 str 的 len 个字符插入到字符串的 index 位置。
返回 *this，因此可以被“链式调用”。
如果 index 无效，则抛出 out_of_range 异常。
如果结果超过最大字符数，则抛出 length_error 异常。
忽略特殊字符（例如 ”）
示例代码
string sString("aaaa");

sString.insert(2, "bcdef", 3);
cout << sString << endl;
输出
aabcdaa
还有一种 insert() 变体可以多次插入相同的字符。
string& string::insert(size_type index, size_type num, char c)
在字符串的 index 位置插入 num 个字符 c 的实例。
返回 *this，因此可以被“链式调用”。
如果 index 无效，则抛出 out_of_range 异常。
如果结果超过最大字符数，则抛出 length_error 异常。
示例代码
string sString("aaaa");

sString.insert(2, 4, 'c');
cout << sString << endl;
输出
aaccccaa
最后，insert() 函数还有三个使用迭代器不同版本。
void insert(iterator it, size_type num, char c)
iterator string::insert(iterator it, char c)
void string::insert(iterator it, InputIterator begin, InputIterator end)
第一个函数在迭代器 it 之前插入 num 个字符 c 的实例。
第二个函数在迭代器 it 之前插入单个字符 c，并返回指向插入字符位置的迭代器。
第三个函数在迭代器 it 之前插入 [begin,end) 之间的所有字符。
如果结果超过最大字符数，所有函数都会抛出 length_error 异常。
下一课
没有下一课
返回目录
上一课
22.6
std::string 附加