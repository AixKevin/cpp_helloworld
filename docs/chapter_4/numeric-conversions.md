# 10.3 — 数值转换

10.3 — 数值转换
Alex
2021年6月17日，太平洋夏令时下午5:39
2024年8月20日
在上一课 (
10.2 -- 浮点和整型提升
) 中，我们讨论了数值提升，即将特定的较窄数值类型转换为可以高效处理的较宽数值类型（通常是
int
或
double
）。
C++ 支持另一种数值类型转换，称为
数值转换
。这些数值转换涵盖了基本类型之间额外的类型转换。
关键见解
数值提升规则 (
10.2 -- 浮点和整型提升
) 所涵盖的任何类型转换都称为数值提升，而不是数值转换。
数值转换有五种基本类型。
将整型转换为任何其他整型（不包括整型提升）
short s = 3; // convert int to short
long l = 3; // convert int to long
char ch = s; // convert short to char
unsigned int u = 3; // convert int to unsigned int
将浮点类型转换为任何其他浮点类型（不包括浮点提升）
float f = 3.0; // convert double to float
long double ld = 3.0; // convert double to long double
将浮点类型转换为任何整型
int i = 3.5; // convert double to int
将整型转换为任何浮点类型
double d = 3; // convert int to double
将整型或浮点类型转换为布尔型
bool b1 = 3; // convert int to bool
bool b2 = 3.0; // convert double to bool
题外话…
由于花括号初始化严格禁止某些类型的数值转换（下一课将详细介绍），为了保持示例的简单性，本课中我们使用复制初始化（它没有任何此类限制）。
安全和不安全转换
与数值提升（总是保留值因此是“安全”的）不同，许多数值转换是不安全的。
不安全转换
是指源类型中至少有一个值无法转换为目标类型的等效值。
数值转换分为三个通用安全类别
值保留转换
是安全的数值转换，其中目标类型可以精确地表示源类型中的所有可能值。
例如，
int
到
long
和
short
到
double
是安全转换，因为源值总是可以转换为目标类型的等效值。
int main()
{
    int n { 5 };
    long l = n; // okay, produces long value 5

    short s { 5 };
    double d = s; // okay, produces double value 5.0

    return 0;
}
编译器通常不会对隐式值保留转换发出警告。
使用值保留转换转换的值总是可以转换回源类型，从而得到一个与原始值等效的值
#include <iostream>

int main()
{
    int n = static_cast<int>(static_cast<long>(3)); // convert int 3 to long and back
    std::cout << n << '\n';                         // prints 3

    char c = static_cast<char>(static_cast<double>('c')); // convert 'c' to double and back
    std::cout << c << '\n';                               // prints 'c'

    return 0;
}
重解释转换
是不安全的数值转换，其中转换后的值可能与源值不同，但没有数据丢失。有符号/无符号转换属于此类别。
例如，当将
signed int
转换为
unsigned int
时
int main()
{
    int n1 { 5 };
    unsigned int u1 { n1 }; // okay: will be converted to unsigned int 5 (value preserved)

    int n2 { -5 };
    unsigned int u2 { n2 }; // bad: will result in large integer outside range of signed int

    return 0;
}
在
u1
的情况下，有符号整型值
5
转换为无符号整型值
5
。因此，在这种情况下值被保留。
在
u2
的情况下，有符号整型值
-5
转换为无符号整型。由于无符号整型不能表示负数，结果将是模数包装到一个超出有符号整型范围的大整数值。在这种情况下值未被保留。
这种值的改变通常是不希望的，并且经常会导致程序表现出意外或实现定义行为。
相关内容
我们在
4.12 -- 类型转换和 static_cast 介绍
一课中讨论了超出范围的值如何在有符号和无符号类型之间进行转换。
警告
尽管重解释转换不安全，但大多数编译器默认禁用隐式有符号/无符号转换警告。
这是因为在现代 C++ 的某些领域（例如在使用标准库数组时），有符号/无符号转换很难避免。实际上，大多数此类转换并不会实际导致值改变。因此，启用此类警告可能会导致许多关于有符号/无符号转换的虚假警告，而这些转换实际上是正常的（从而淹没合法的警告）。
如果您选择禁用此类警告，请格外小心这些类型之间意外的转换（尤其是在将参数传递给接受相反符号参数的函数时）。
使用重解释转换转换的值可以转换回源类型，从而得到一个与原始值等效的值（即使初始转换产生的值超出了源类型的范围）。因此，重解释转换在转换过程中不会丢失数据。
#include <iostream>

int main()
{
    int u = static_cast<int>(static_cast<unsigned int>(-5)); // convert '-5' to unsigned and back
    std::cout << u << '\n'; // prints -5
    
    return 0;
}
致进阶读者
在 C++20 之前，将超出有符号值范围的无符号值进行转换在技术上是实现定义行为（因为允许有符号整数使用与无符号整数不同的二进制表示）。实际上，这在现代系统上不是问题。
C++20 现在要求有符号整数使用二进制补码。因此，转换规则发生了变化，上述情况现在被定义为重解释转换（超出范围的转换将产生模数包装）。
请注意，尽管此类转换是良好定义的，但有符号算术溢出（当算术运算产生的值超出可存储范围时发生）仍然是未定义行为。
有损转换
是不安全的数值转换，其中在转换过程中可能会丢失数据。
例如，
double
到
int
是一种可能导致数据丢失的转换
int i = 3.0; // okay: will be converted to int value 3 (value preserved)
int j = 3.5; // data lost: will be converted to int value 3 (fractional value 0.5 lost)
从
double
到
float
的转换也可能导致数据丢失
float f = 1.2;        // okay: will be converted to float value 1.2 (value preserved)
float g = 1.23456789; // data lost: will be converted to float 1.23457 (precision lost)
将已丢失数据的值转换回源类型将导致与原始值不同的值
#include <iostream>

int main()
{
    double d { static_cast<double>(static_cast<int>(3.5)) }; // convert double 3.5 to int and back
    std::cout << d << '\n'; // prints 3

    double d2 { static_cast<double>(static_cast<float>(1.23456789)) }; // convert double 1.23456789 to float and back
    std::cout << d2 << '\n'; // prints 1.23457

    return 0;
}
例如，如果
double
值
3.5
转换为
int
值
3
，则小数部分
0.5
会丢失。当
3
转换回
double
时，结果是
3.0
，而不是
3.5
。
当运行时将执行隐式有损转换时，编译器通常会发出警告（或在某些情况下是错误）。
警告
某些转换可能根据平台属于不同的类别。
例如，
int
到
double
通常是安全转换，因为
int
通常是 4 字节，而
double
通常是 8 字节，并且在此类系统上，所有可能的
int
值都可以表示为
double
。然而，有些架构中
int
和
double
都是 8 字节。在此类架构上，
int
到
double
是有损转换！
我们可以通过将一个 long long 值（必须至少是 64 位）转换为 double 再转换回来进行演示
#include <iostream>

int main()
{
    std::cout << static_cast<long long>(static_cast<double>(10000000000000001LL));

    return 0;
}
这会打印
10000000000000000
请注意，我们最后一位数字丢失了！
应尽可能避免不安全转换。但是，这并非总是可能的。当使用不安全转换时，通常是在以下情况：
我们可以将要转换的值限制为只能转换为等效值。例如，当我们可以保证
int
是非负数时，可以安全地将
int
转换为
unsigned int
。
我们不介意丢失一些不相关的数据。例如，将
int
转换为
bool
会导致数据丢失，但我们通常对此没问题，因为我们只是检查
int
的值是否为
0
。
更多关于数值转换
数值转换的具体规则复杂而众多，所以这里只列出最重要的事情。
在
所有
情况下，将一个值转换为其范围不支持该值的类型将导致可能意想不到的结果。例如
int main()
{
    int i{ 30000 };
    char c = i; // chars have range -128 to 127

    std::cout << static_cast<int>(c) << '\n';

    return 0;
}
在此示例中，我们已将一个大整数分配给
char
类型的变量（其范围为 -128 到 127）。这会导致 char 溢出，并产生意想不到的结果
48
请记住，对于无符号值，溢出是明确定义的，而对于有符号值，则会产生未定义行为。
从较大的整型或浮点类型转换为同家族的较小类型通常可行，只要该值适合较小类型的范围。例如
int i{ 2 };
    short s = i; // convert from int to short
    std::cout << s << '\n';

    double d{ 0.1234 };
    float f = d;
    std::cout << f << '\n';
这产生了预期的结果
2
0.1234
对于浮点值，由于较小类型精度损失，可能会发生一些舍入。例如
float f = 0.123456789; // double value 0.123456789 has 9 significant digits, but float can only support about 7
    std::cout << std::setprecision(9) << f << '\n'; // std::setprecision defined in iomanip header
在这种情况下，我们看到精度损失，因为
float
不能像
double
那样保持那么高的精度
0.123456791
从整数转换为浮点数通常可行，只要该值适合浮点类型的范围。例如
int i{ 10 };
    float f = i;
    std::cout << f << '\n';
这产生了预期的结果
10
从浮点数转换为整数可行，只要该值适合整数的范围，但任何小数部分都会丢失。例如
int i = 3.5;
    std::cout << i << '\n';
在此示例中，小数部分 (.5) 丢失，留下以下结果
3
虽然数值转换规则看起来很吓人，但实际上，如果您尝试做一些危险的事情（排除一些有符号/无符号转换），编译器通常会警告您。
下一课
10.4
窄化转换、列表初始化和 constexpr 初始化器
返回目录
上一课
10.2
浮点和整型提升