# 28.3 — 使用 ostream 和 ios 进行输出

28.3 — 使用 ostream 和 ios 进行输出
Alex
2008 年 3 月 12 日，下午 3:10 PDT
2024 年 3 月 16 日
在本节中，我们将介绍 iostream 输出类 (ostream) 的各个方面。
插入运算符
插入运算符 (<<) 用于将信息放入输出流。C++ 为所有内置数据类型预定义了插入操作，你已经看到了如何为自己的类
重载插入运算符
。
在关于
流
的课程中，你看到 istream 和 ostream 都派生自一个名为 ios 的类。ios (和 ios_base) 的工作之一是控制输出的格式化选项。
格式化
有两种方法可以更改格式化选项：标志和操纵符。你可以将
标志
视为可以打开和关闭的布尔变量。
操纵符
是放置在流中并影响输入和输出方式的对象。
要打开标志，请使用
setf()
函数，并将相应的标志作为参数。例如，默认情况下，C++ 不会在正数前面打印 + 号。但是，通过使用 std::ios::showpos 标志，我们可以更改此行为
std::cout.setf(std::ios::showpos); // turn on the std::ios::showpos flag
std::cout << 27 << '\n';
这会产生以下输出
+27
可以使用按位或 (|) 运算符同时打开多个 ios 标志
std::cout.setf(std::ios::showpos | std::ios::uppercase); // turn on the std::ios::showpos and std::ios::uppercase flag
std::cout << 1234567.89f << '\n';
这输出
+1.23457E+06
要关闭标志，请使用
unsetf()
函数
std::cout.setf(std::ios::showpos); // turn on the std::ios::showpos flag
std::cout << 27 << '\n';
std::cout.unsetf(std::ios::showpos); // turn off the std::ios::showpos flag
std::cout << 28 << '\n';
这会产生以下输出
+27
28
使用 setf() 时还需要提及另一个小技巧。许多标志属于组，称为格式组。
格式组
是一组执行类似（有时互斥）格式化选项的标志。例如，名为“basefield”的格式组包含标志“oct”、“dec”和“hex”，它们控制整数值的基数。默认情况下，“dec”标志已设置。因此，如果我们这样做
std::cout.setf(std::ios::hex); // try to turn on hex output
std::cout << 27 << '\n';
我们得到以下输出
27
它不起作用！原因是 setf() 只会打开标志——它不够聪明，无法关闭互斥的标志。因此，当我们打开 std::hex 时，std::ios::dec 仍然打开，并且 std::ios::dec 显然具有优先权。有两种方法可以解决这个问题。
首先，我们可以关闭 std::ios::dec，以便只设置 std::hex
std::cout.unsetf(std::ios::dec); // turn off decimal output
std::cout.setf(std::ios::hex); // turn on hexadecimal output
std::cout << 27 << '\n';
现在我们得到了预期的输出
1b
第二种方法是使用不同形式的 setf()，它接受两个参数：第一个参数是要设置的标志，第二个是它所属的格式组。使用这种形式的 setf() 时，属于该组的所有标志都将关闭，并且只打开传入的标志。例如
// Turn on std::ios::hex as the only std::ios::basefield flag
std::cout.setf(std::ios::hex, std::ios::basefield);
std::cout << 27 << '\n';
这也产生了预期的输出
1b
使用 setf() 和 unsetf() 往往很笨拙，因此 C++ 提供了第二种方法来更改格式化选项：操纵符。操纵符的好处在于它们足够智能，可以打开和关闭适当的标志。以下是使用一些操纵符更改基数的示例
std::cout << std::hex << 27 << '\n'; // print 27 in hex
std::cout << 28 << '\n'; // we're still in hex
std::cout << std::dec << 29 << '\n'; // back to decimal
此程序产生输出
1b
1c
29
通常，使用操纵符比设置和取消设置标志容易得多。许多选项可以通过标志和操纵符（例如更改基数）获得，但是，其他选项只能通过标志或操纵符获得，因此了解如何使用两者非常重要。
有用的格式化器
以下是一些更有用的标志、操纵符和成员函数的列表。标志位于 std::ios 类中，操纵符位于 std 命名空间中，成员函数位于 std::ostream 类中。
组
标志
含义
std::ios::boolalpha
如果设置，布尔值打印“true”或“false”。如果未设置，布尔值打印 0 或 1
操纵符
含义
std::boolalpha
布尔值打印“true”或“false”
std::noboolalpha
布尔值打印 0 或 1（默认）
示例
std::cout << true << ' ' << false << '\n';

std::cout.setf(std::ios::boolalpha);
std::cout << true << ' ' << false << '\n';

std::cout << std::noboolalpha << true << ' ' << false << '\n';

std::cout << std::boolalpha << true << ' ' << false << '\n';
结果
1 0
true false
1 0
true false
组
标志
含义
std::ios::showpos
如果设置，正数前缀为 +
操纵符
含义
std::showpos
正数前缀为 +
std::noshowpos
正数前不加 +
示例
std::cout << 5 << '\n';

std::cout.setf(std::ios::showpos);
std::cout << 5 << '\n';

std::cout << std::noshowpos << 5 << '\n';

std::cout << std::showpos << 5 << '\n';
结果
5
+5
5
+5
组
标志
含义
std::ios::uppercase
如果设置，使用大写字母
操纵符
含义
std::uppercase
使用大写字母
std::nouppercase
使用小写字母
示例
std::cout << 12345678.9 << '\n';

std::cout.setf(std::ios::uppercase);
std::cout << 12345678.9 << '\n';

std::cout << std::nouppercase << 12345678.9 << '\n';

std::cout << std::uppercase << 12345678.9 << '\n';
结果
1.23457e+007
1.23457E+007
1.23457e+007
1.23457E+007
组
标志
含义
std::ios::basefield
std::ios::dec
以十进制打印值（默认）
std::ios::basefield
std::ios::hex
以十六进制打印值
std::ios::basefield
std::ios::oct
以八进制打印值
std::ios::basefield
（无）
根据值的引导字符打印值
操纵符
含义
std::dec
以十进制打印值
std::hex
以十六进制打印值
std::oct
以八进制打印值
示例
std::cout << 27 << '\n';

std::cout.setf(std::ios::dec, std::ios::basefield);
std::cout << 27 << '\n';

std::cout.setf(std::ios::oct, std::ios::basefield);
std::cout << 27 << '\n';

std::cout.setf(std::ios::hex, std::ios::basefield);
std::cout << 27 << '\n';

std::cout << std::dec << 27 << '\n';
std::cout << std::oct << 27 << '\n';
std::cout << std::hex << 27 << '\n';
结果
27
27
33
1b
27
33
1b
现在，你应该能够看出通过标志和操纵符设置格式之间的关系。在未来的示例中，除非操纵符不可用，否则我们将使用操纵符。
精度、表示法和小数点
使用操纵符（或标志），可以更改浮点数显示时的精度和格式。有几种格式化选项以某种复杂的方式组合，因此我们将更仔细地研究这一点。
组
标志
含义
std::ios::floatfield
std::ios::fixed
浮点数使用十进制表示法
std::ios::floatfield
std::ios::scientific
浮点数使用科学记数法
std::ios::floatfield
（无）
对于位数少的数字使用 fixed，否则使用 scientific
std::ios::floatfield
std::ios::showpoint
始终显示小数点和浮点值的尾随 0
操纵符
含义
std::fixed
值使用十进制表示法
std::scientific
值使用科学记数法
std::showpoint
显示小数点和浮点值的尾随 0
std::noshowpoint
不显示小数点和浮点值的尾随 0
std::setprecision(int)
设置浮点数的精度（定义在 iomanip 头文件中）
成员函数
含义
std::ios_base::precision()
返回浮点数的当前精度
std::ios_base::precision(int)
设置浮点数的精度并返回旧精度
如果使用 fixed 或 scientific 表示法，精度决定了小数部分显示多少位小数。请注意，如果精度小于有效数字的数量，则数字将被四舍五入。
std::cout << std::fixed << '\n';
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';

std::cout << std::scientific << '\n';
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';
产生结果
123.456
123.4560
123.45600
123.456000
123.4560000

1.235e+002
1.2346e+002
1.23456e+002
1.234560e+002
1.2345600e+002
如果既不使用 fixed 也不使用 scientific，则精度决定应显示多少有效数字。同样，如果精度小于有效数字的数量，则数字将被四舍五入。
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';
产生以下结果
123
123.5
123.46
123.456
123.456
使用 showpoint 操纵符或标志，可以使流写入小数点和尾随零。
std::cout << std::showpoint << '\n';
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';
产生以下结果
123.
123.5
123.46
123.456
123.4560
以下是一些更多示例的汇总表
选项
精度
12345.0
0.12345
正常
3
1.23e+004
0.123
4
1.235e+004
0.1235
5
12345
0.12345
6
12345
0.12345
Showpoint
3
1.23e+004
0.123
4
1.235e+004
0.1235
5
12345.
0.12345
6
12345.0
0.123450
Fixed
3
12345.000
0.123
4
12345.0000
0.1235
5
12345.00000
0.12345
6
12345.000000
0.123450
Scientific
3
1.235e+004
1.235e-001
4
1.2345e+004
1.2345e-001
5
1.23450e+004
1.23450e-001
6
1.234500e+004
1.234500e-001
宽度、填充字符和对齐方式
通常，当您打印数字时，数字的打印不考虑其周围的空间。但是，可以将数字的打印左对齐或右对齐。为此，我们必须首先定义一个字段宽度，它定义一个值将具有的输出空间数量。如果实际打印的数字小于字段宽度，它将左对齐或右对齐（如指定）。如果实际数字大于字段宽度，它将不会被截断——它将溢出字段。
组
标志
含义
std::ios::adjustfield
std::ios::internal
数字的符号左对齐，值右对齐
std::ios::adjustfield
std::ios::left
符号和值左对齐
std::ios::adjustfield
std::ios::right
符号和值右对齐（默认）
操纵符
含义
std::internal
数字的符号左对齐，值右对齐
std::left
符号和值左对齐
std::right
符号和值右对齐
std::setfill(char)
设置参数作为填充字符（定义在 iomanip 头文件中）
std::setw(int)
将输入和输出的字段宽度设置为参数（定义在 iomanip 头文件中）
成员函数
含义
std::basic_ostream::fill()
返回当前填充字符
std::basic_ostream::fill(char)
设置填充字符并返回旧填充字符
std::ios_base::width()
返回当前字段宽度
std::ios_base::width(int)
设置当前字段宽度并返回旧字段宽度
为了使用这些格式化器中的任何一个，我们必须首先设置字段宽度。这可以通过 width(int) 成员函数或 setw() 操纵符完成。请注意，右对齐是默认设置。
std::cout << -12345 << '\n'; // print default value with no field width
std::cout << std::setw(10) << -12345 << '\n'; // print default with field width
std::cout << std::setw(10) << std::left << -12345 << '\n'; // print left justified
std::cout << std::setw(10) << std::right << -12345 << '\n'; // print right justified
std::cout << std::setw(10) << std::internal << -12345 << '\n'; // print internally justified
这会产生结果
-12345
    -12345
-12345
    -12345
-    12345
需要注意的是，setw() 和 width() 只影响下一个输出语句。它们不像其他一些标志/操纵符那样是持久的。
现在，让我们设置一个填充字符并执行相同的示例
std::cout.fill('*');
std::cout << -12345 << '\n'; // print default value with no field width
std::cout << std::setw(10) << -12345 << '\n'; // print default with field width
std::cout << std::setw(10) << std::left << -12345 << '\n'; // print left justified
std::cout << std::setw(10) << std::right << -12345 << '\n'; // print right justified
std::cout << std::setw(10) << std::internal << -12345 << '\n'; // print internally justified
这会产生输出
-12345
****-12345
-12345****
****-12345
-****12345
请注意，字段中的所有空白区域都已填充了填充字符。
ostream 类和 iostream 库包含其他输出函数、标志和操纵符，它们可能很有用，具体取决于您需要做什么。与 istream 类一样，这些主题更适合专注于标准库的教程或书籍。
下一课
28.4
字符串流类
返回目录
上一课
28.2
使用 istream 进行输入