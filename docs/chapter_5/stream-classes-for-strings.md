# 28.4 — 字符串流类

28.4 — 字符串流类
Alex
2008年3月18日，下午2:58 PDT
2024年2月27日
到目前为止，你所见过的所有I/O示例都是写入 cout 或从 cin 读取。然而，还有另一组类，称为字符串流类，它们允许你使用熟悉的插入运算符 (<<) 和提取运算符 (>>) 来处理字符串。与 istream 和 ostream 一样，字符串流提供了缓冲区来保存数据。但是，与 cin 和 cout 不同，这些流不连接到I/O通道（例如键盘、显示器等）。字符串流的主要用途之一是缓冲输出以供以后显示，或者逐行处理输入。
字符串流有六个类：istringstream（派生自 istream）、ostringstream（派生自 ostream）和 stringstream（派生自 iostream）用于读写普通字符宽度的字符串。wistringstream、wostringstream 和 wstringstream 用于读写宽字符字符串。要使用字符串流，你需要 #include sstream 头文件。
将数据放入字符串流有两种方法
使用插入运算符 (<<)
std::stringstream os {};
os << "en garde!\n"; // insert "en garde!" into the stringstream
使用 str(string) 函数设置缓冲区的值
std::stringstream os {};
os.str("en garde!"); // set the stringstream buffer to "en garde!"
同样，从字符串流中获取数据也有两种方法
使用 str() 函数检索缓冲区的结果
std::stringstream os {};
os << "12345 67.89\n";
std::cout << os.str();
这会打印
12345 67.89
使用提取运算符 (>>)
std::stringstream os {};
os << "12345 67.89"; // insert a string of numbers into the stream

std::string strValue {};
os >> strValue;

std::string strValue2 {};
os >> strValue2;

// print the numbers separated by a dash
std::cout << strValue << " - " << strValue2 << '\n';
这个程序打印
12345 - 67.89
请注意，>> 运算符会遍历字符串——每次连续使用 >> 都会返回流中下一个可提取的值。另一方面，str() 返回流的整个值，即使 >> 已经用于该流。
字符串和数字之间的转换
因为插入和提取运算符知道如何处理所有基本数据类型，所以我们可以使用它们将字符串转换为数字，反之亦然。
首先，让我们看看如何将数字转换为字符串
std::stringstream os {};

constexpr int nValue { 12345 };
constexpr double dValue { 67.89 };
os << nValue << ' ' << dValue;

std::string strValue1, strValue2;
os >> strValue1 >> strValue2;

std::cout << strValue1 << ' ' << strValue2 << '\n';
这段代码打印
12345 67.89
现在让我们将数字字符串转换为数字
std::stringstream os {};
os << "12345 67.89"; // insert a string of numbers into the stream
int nValue {};
double dValue {};

os >> nValue >> dValue;

std::cout << nValue << ' ' << dValue << '\n';
这个程序打印
12345 67.89
清除字符串流以供重用
有几种方法可以清空字符串流的缓冲区。
使用带空C风格字符串的 str() 将其设置为空字符串
std::stringstream os {};
os << "Hello ";

os.str(""); // erase the buffer

os << "World!";
std::cout << os.str();
使用带空 std::string 对象的 str() 将其设置为空字符串
std::stringstream os {};
os << "Hello ";

os.str(std::string{}); // erase the buffer

os << "World!";
std::cout << os.str();
这两个程序都会产生以下结果
World!
清除字符串流时，通常最好也调用 clear() 函数
std::stringstream os {};
os << "Hello ";

os.str(""); // erase the buffer
os.clear(); // reset error flags

os << "World!";
std::cout << os.str();
clear() 会重置可能已设置的任何错误标志，并将流返回到正常状态。我们将在下一课中详细讨论流状态和错误标志。
下一课
28.5
流状态与输入验证
返回目录
上一课
28.3
使用 ostream 和 ios 进行输出