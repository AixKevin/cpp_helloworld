# 5.7 — std::string 介绍

5.7 — std::string 介绍
Alex
2015 年 5 月 8 日，太平洋夏令时上午 7:59
2025 年 1 月 3 日
在课程
5.2 -- 字面量
中，我们介绍了 C 风格字符串字面量
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!"; // "Hello world!" is a C-style string literal.
    return 0;
}
虽然 C 风格字符串字面量可以正常使用，但 C 风格字符串变量行为异常，难以操作（例如，不能使用赋值为 C 风格字符串变量赋新值），并且危险（例如，如果将较长的 C 风格字符串复制到为较短的 C 风格字符串分配的空间中，将导致未定义行为）。在现代 C++ 中，最好避免使用 C 风格字符串变量。
幸运的是，C++ 在语言中引入了两种额外的字符串类型，它们更易于使用且更安全：
std::string
和
std::string_view
(C++17)。与我们之前介绍的类型不同，
std::string
和
std::string_view
不是基本类型（它们是类类型，我们将在未来介绍）。然而，它们的基本用法都很直接且非常有用，因此我们在这里介绍它们。
std::string
介绍
在 C++ 中，处理字符串和字符串对象最简单的方法是通过
std::string
类型，它存在于 <string> 头文件中。
我们可以像其他对象一样创建
std::string
类型的对象
#include <string> // allows use of std::string

int main()
{
    std::string name {}; // empty string

    return 0;
}
就像普通变量一样，您可以按照预期初始化或赋值给 std::string 对象
#include <string>

int main()
{
    std::string name { "Alex" }; // initialize name with string literal "Alex"
    name = "John";               // change name to "John"

    return 0;
}
请注意，字符串也可以由数字字符组成
std::string myID{ "45" }; // "45" is not the same as integer 45!
以字符串形式表示的数字被视为文本，而不是数字，因此不能将其作为数字进行操作（例如，不能将它们相乘）。C++ 不会自动将字符串转换为整数或浮点值，反之亦然（尽管有方法可以做到这一点，我们将在未来的课程中介绍）。
使用
std::cout
进行字符串输出
std::string
对象可以使用
std::cout
按照预期输出
#include <iostream>
#include <string>

int main()
{
    std::string name { "Alex" };
    std::cout << "My name is: " << name << '\n';

    return 0;
}
这会打印
My name is: Alex
空字符串将不打印任何内容
#include <iostream>
#include <string>

int main()
{
    std::string empty{ };
    std::cout << '[' << empty << ']';

    return 0;
}
打印结果为
[]
std::string
可以处理不同长度的字符串
std::string
最棒的功能之一是它能够存储不同长度的字符串
#include <iostream>
#include <string>

int main()
{
    std::string name { "Alex" }; // initialize name with string literal "Alex"
    std::cout << name << '\n';

    name = "Jason";              // change name to a longer string
    std::cout << name << '\n';

    name = "Jay";                // change name to a shorter string
    std::cout << name << '\n';

    return 0;
}
这会打印
Alex
Jason
Jay
在上面的示例中，`name` 被初始化为字符串 `"Alex"`，它包含五个字符（四个显式字符和一个空终止符）。然后我们将 `name` 设置为一个更大的字符串，再设置一个更小的字符串。`std::string` 处理这些都没有问题！你甚至可以在 `std::string` 中存储非常长的字符串。
这是
std::string
如此强大的原因之一。
关键见解
如果
std::string
没有足够的内存来存储字符串，它将使用一种称为动态内存分配的内存分配形式（在运行时）请求额外的内存。这种获取额外内存的能力是
std::string
如此灵活的原因之一，但也是它相对较慢的原因。
我们将在未来的章节中介绍动态内存分配。
使用
std::cin
进行字符串输入
使用
std::string
和
std::cin
可能会带来一些惊喜！考虑以下示例
#include <iostream>
#include <string>

int main()
{
    std::cout << "Enter your full name: ";
    std::string name{};
    std::cin >> name; // this won't work as expected since std::cin breaks on whitespace

    std::cout << "Enter your favorite color: ";
    std::string color{};
    std::cin >> color;

    std::cout << "Your name is " << name << " and your favorite color is " << color << '\n';

    return 0;
}
以下是此程序的示例运行结果
Enter your full name: John Doe
Enter your favorite color: Your name is John and your favorite color is Doe
嗯，这不对劲！发生什么了？原来，当使用
operator>>
从
std::cin
中提取字符串时，
operator>>
只返回到它遇到的第一个空白字符为止的字符。任何其他字符都留在
std::cin
中，等待下一次提取。
因此，当我们使用 `operator>>` 将输入提取到变量 `name` 中时，只提取了 `"John"`，而 `" Doe"` 留在了 `std::cin` 中。当我们随后使用 `operator>>` 将输入提取到变量 `color` 中时，它提取了 `"Doe"`，而不是等待我们输入颜色。然后程序结束。
使用
std::getline()
输入文本
要将整行输入读取到字符串中，最好使用
std::getline()
函数。
std::getline()
需要两个参数：第一个是
std::cin
，第二个是您的字符串变量。
这是上面使用
std::getline()
的相同程序
#include <iostream>
#include <string> // For std::string and std::getline

int main()
{
    std::cout << "Enter your full name: ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // read a full line of text into name

    std::cout << "Enter your favorite color: ";
    std::string color{};
    std::getline(std::cin >> std::ws, color); // read a full line of text into color

    std::cout << "Your name is " << name << " and your favorite color is " << color << '\n';

    return 0;
}
现在我们的程序如期工作
Enter your full name: John Doe
Enter your favorite color: blue
Your name is John Doe and your favorite color is blue
std::ws
到底是什么？
在课程
4.8 -- 浮点数
中，我们讨论了输出操纵符，它允许我们改变输出的显示方式。在该课程中，我们使用了输出操纵符函数
std::setprecision()
来改变
std::cout
显示的精度位数。
C++ 也支持**输入操纵符**，它改变输入被接受的方式。
std::ws
输入操纵符告诉
std::cin
在提取之前忽略任何前导空白。前导空白是字符串开头出现的任何空白字符（空格、制表符、换行符）。
我们来探讨一下为什么这很有用。考虑以下程序
#include <iostream>
#include <string>

int main()
{
    std::cout << "Pick 1 or 2: ";
    int choice{};
    std::cin >> choice;

    std::cout << "Now enter your name: ";
    std::string name{};
    std::getline(std::cin, name); // note: no std::ws here

    std::cout << "Hello, " << name << ", you picked " << choice << '\n';

    return 0;
}
这是此程序的一些输出
Pick 1 or 2: 2
Now enter your name: Hello, , you picked 2
此程序首先要求您输入 1 或 2，并等待您操作。到目前为止一切顺利。然后它会要求您输入您的姓名。然而，它并不会真正等待您输入姓名！相反，它会打印“Hello”字符串，然后退出。
当您使用
operator>>
输入值时，
std::cin
不仅捕获值，还会捕获您按下回车键时产生的换行符 (
'\n'
)。因此，当我们输入
2
并按下回车时，
std::cin
将字符串
"2\n"
作为输入捕获。然后它将值
2
提取到变量
choice
中，将换行符留在后面以备后用。然后，当
std::getline()
提取文本到
name
时，它看到
"\n"
已经在
std::cin
中等待，并认为我们之前肯定输入了一个空字符串！这绝不是我们想要的。
我们可以修改上述程序，使用
std::ws
输入操纵符，告诉
std::getline()
忽略任何前导空白字符。
#include <iostream>
#include <string>

int main()
{
    std::cout << "Pick 1 or 2: ";
    int choice{};
    std::cin >> choice;

    std::cout << "Now enter your name: ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // note: added std::ws here

    std::cout << "Hello, " << name << ", you picked " << choice << '\n';

    return 0;
}
现在这个程序将按预期运行。
Pick 1 or 2: 2
Now enter your name: Alex
Hello, Alex, you picked 2
最佳实践
如果使用
std::getline()
读取字符串，请使用
std::cin >> std::ws
输入操纵符来忽略前导空格。这需要为每个
std::getline()
调用完成，因为
std::ws
不会在调用之间保留。
关键见解
当提取到变量时，提取运算符（
>>
）会忽略前导空格。它在遇到非前导空格时停止提取。
std::getline()
不会忽略前导空格。如果您希望它忽略前导空格，请将
std::cin >> std::ws
作为第一个参数传递。它在遇到换行符时停止提取。
std::string
的长度
如果我们想知道
std::string
中有多少个字符，我们可以向
std::string
对象询问它的长度。这样做的语法与您之前见过的不同，但相当直接
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" };
    std::cout << name << " has " << name.length() << " characters\n";

    return 0;
}
这会打印
Alex has 4 characters
尽管
std::string
必须以 null 终止（自 C++11 起），但
std::string
返回的长度不包括隐式 null 终止符。
请注意，我们不是通过 `length(name)` 来获取字符串长度，而是通过 `name.length()`。`length()` 函数不是一个普通的独立函数——它是 `std::string` 内部嵌套的一种特殊类型的函数，称为*成员函数*。因为 `length()` 成员函数在 `std::string` 内部声明，所以在文档中有时会写成 `std::string::length()`。
我们将在稍后更详细地介绍成员函数，包括如何编写自己的成员函数。
关键见解
对于普通函数，我们调用
function(object)
。对于成员函数，我们调用
object.function()
。
另请注意，`std::string::length()` 返回一个无符号整数值（最可能是 `size_t` 类型）。如果您想将长度赋给 `int` 变量，应该进行 `static_cast`，以避免编译器关于有符号/无符号转换的警告
int length { static_cast<int>(name.length()) };
致进阶读者
在 C++20 中，您还可以使用
std::ssize()
函数获取
std::string
的长度，作为大型有符号整数类型（通常为
std::ptrdiff_t
）
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" };
    std::cout << name << " has " << std::ssize(name) << " characters\n";

    return 0;
}
由于 `ptrdiff_t` 可能比 `int` 大，如果您想将 `std::ssize()` 的结果存储在 `int` 变量中，则应将结果 `static_cast` 为 `int`
int len { static_cast<int>(std::ssize(name)) };
初始化
std::string
代价昂贵
每当初始化 `std::string` 时，都会创建用于初始化它的字符串的副本。复制字符串的开销很大，因此应注意最小化复制次数。
不要按值传递
std::string
当
std::string
按值传递给函数时，
std::string
函数参数必须被实例化并用实参初始化。这会导致昂贵的复制。我们将在课程
5.8 -- std::string_view 介绍
中讨论替代方法（使用
std::string_view
）。
最佳实践
不要按值传递
std::string
，因为它会产生昂贵的复制。
提示
在大多数情况下，请改用
std::string_view
参数（参见课程
5.8 -- std::string_view 介绍
）。
返回
std::string
当一个函数按值返回给调用者时，返回值通常从函数复制回调用者。所以你可能会认为你不应该按值返回
std::string
，因为这样做会返回
std::string
的昂贵副本。
然而，根据经验法则，当返回语句的表达式解析为以下任何一种情况时，按值返回
std::string
是可以的
一个
std::string
类型的局部变量。
从另一个函数调用或操作符中按值返回的
std::string
。
作为返回语句的一部分创建的
std::string
临时对象。
致进阶读者
std::string
支持一种称为移动语义的能力，它允许在函数结束时将被销毁的对象按值返回而无需复制。移动语义的工作原理超出了本入门文章的范围，但我们会在课程
16.5 -- 返回 std::vector，以及移动语义简介
中介绍它。
在大多数其他情况下，应避免按值返回
std::string
，因为这会产生昂贵的复制。
提示
如果返回 C 风格字符串字面量，请改用
std::string_view
返回类型（详见课程
5.9 -- std::string_view (第二部分)
）。
致进阶读者
在某些情况下，
std::string
也可以通过（const）引用返回，这是另一种避免复制的方法。我们将在课程
12.12 -- 通过引用返回和通过地址返回
和
14.6 -- 访问函数
中进一步讨论。
std::string
的字面量
双引号字符串字面量（如“Hello, world!”）默认是 C 风格字符串（因此，类型很奇怪）。
我们可以通过在双引号字符串字面量后使用
s
后缀来创建
std::string
类型的字符串字面量。
s
必须是小写。
#include <iostream>
#include <string> // for std::string

int main()
{
    using namespace std::string_literals; // easy access to the s suffix

    std::cout << "foo\n";   // no suffix is a C-style string literal
    std::cout << "goo\n"s;  // s suffix is a std::string literal

    return 0;
}
提示
“s”后缀存在于命名空间
std::literals::string_literals
中。
访问字面量后缀最简洁的方式是通过 `using` 指令 `using namespace std::literals`。然而，这会将*所有*标准库字面量导入到 `using` 指令的作用域中，从而引入大量您可能不会使用的东西。
我们推荐使用
using namespace std::string_literals
，它只导入
std::string
的字面量。
我们在课程
7.13 -- using 声明和 using 指令
中讨论 using 指令。这是一个例外情况，其中
using
整个命名空间通常是可以接受的，因为其中定义的后缀不太可能与您的任何代码冲突。避免在头文件中的函数外部使用此类 using 指令。
您可能不需要经常使用
std::string
字面量（因为用 C 风格字符串字面量初始化
std::string
对象是可以的），但我们将在未来的课程中看到一些情况（涉及类型推导），其中使用
std::string
字面量而不是 C 风格字符串字面量会使事情变得更容易（请参阅
10.8 -- 使用 auto 关键字进行对象类型推导
的示例）。
致进阶读者
"Hello"s
解析为
std::string { "Hello", 5 }
，它创建一个用 C 风格字符串字面量“Hello”初始化的临时
std::string
（其长度为 5，不包括隐式空终止符）。
Constexpr 字符串
如果您尝试定义 `constexpr std::string`，您的编译器可能会报错
#include <iostream>
#include <string>

int main()
{
    using namespace std::string_literals;

    constexpr std::string name{ "Alex"s }; // compile error

    std::cout << "My name is: " << name;

    return 0;
}
发生这种情况是因为 `constexpr std::string` 在 C++17 或更早版本中根本不受支持，并且仅在 C++20/23 的非常有限的情况下才有效。如果需要 constexpr 字符串，请改用 `std::string_view`（在课程
5.8 -- std::string_view 介绍
中讨论）。
总结
std::string
很复杂，它利用了许多我们尚未介绍的语言特性。幸运的是，您不需要理解这些复杂性就可以使用
std::string
完成简单的任务，例如基本的字符串输入和输出。我们鼓励您现在就开始尝试字符串，我们稍后将介绍其他字符串功能。
小测验时间
问题 #1
编写一个程序，要求用户输入他们的全名和年龄。输出时，告诉用户他们的年龄和姓名中字符数的总和（使用
std::string::length()
成员函数获取字符串长度）。为简单起见，姓名中的任何空格都算作一个字符。
样本输出
Enter your full name: John Doe
Enter your age: 32
Your age + length of name is: 40
提醒：我们需要注意不要混合有符号和无符号值。
std::string::length()
返回一个无符号值。如果您支持 C++20，请使用
std::ssize()
获取有符号长度。否则，将
std::string::length()
的返回值
static_cast
为
int
。
显示答案
#include <iostream>
#include <string>

int main()
{
    std::cout << "Enter your full name: ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // read a full line of text into name

    std::cout << "Enter your age: ";
    int age{}; // age needs to be an integer, not a string, so we can do math with it
    std::cin >> age;

    // age is signed, and name.length() is unsigned -- we shouldn't mix these
    // We'll convert name.length() to a signed value
    int nameLen { static_cast<int>(name.length()) }; // get number of chars in name (including spaces)
    std::cout << "Your age + length of name is: " << age + nameLen << '\n';

    return 0;
}
下一课
5.8
std::string_view 介绍
返回目录
上一课
5.6
Constexpr 变量