# 10.6 — 显式类型转换（casting）和 static_cast

10.6 — 显式类型转换（casting）和 static_cast
Alex
2015 年 4 月 16 日，太平洋时间下午 3:54
2025 年 3 月 4 日
在
10.1 -- 隐式类型转换
课程中，我们讨论了编译器可以使用隐式类型转换将值从一种数据类型转换为另一种数据类型。当你想将一个值从一种数据类型进行数值提升到更宽的数据类型时，使用隐式类型转换是没问题的。
许多 C++ 新手程序员会尝试这样的代码：
double d = 10 / 4; // does integer division, initializes d with value 2.0
因为
10
和
4
都是
int
类型，所以会执行整数除法，表达式计算结果为
int
值
2
。这个值在用于初始化变量
d
之前，会经历数值转换成为
double
值
2.0
。这很可能不是预期的结果。
在使用字面量操作数的情况下，将一个或两个整数字面量替换为双精度字面量将导致浮点除法而不是整数除法。
double d = 10.0 / 4.0; // does floating point division, initializes d with value 2.5
但是如果使用的是变量而不是字面量呢？考虑这种情况：
int x { 10 };
int y { 4 };
double d = x / y; // does integer division, initializes d with value 2.0
由于这里使用了整数除法，变量
d
的最终值将为
2.0
。在这种情况下，我们如何告诉编译器我们希望使用浮点除法而不是整数除法？字面量后缀不能用于变量。我们需要某种方法将一个（或两个）变量操作数转换为浮点类型，以便使用浮点除法。
幸运的是，C++ 提供了许多不同的**类型转换运算符**（更常称为**强制类型转换**），程序员可以使用它们让编译器执行类型转换。由于强制类型转换是程序员的显式请求，这种形式的类型转换通常称为**显式类型转换**（与隐式类型转换相对，隐式类型转换是编译器自动执行类型转换）。
类型转换
C++ 支持 5 种不同类型的强制类型转换：
static_cast
、
dynamic_cast
、
const_cast
、
reinterpret_cast
和 C 风格强制类型转换。前四种有时被称为**命名强制类型转换**。
致进阶读者
强制类型转换
描述
安全？
static_cast
在编译时对相关类型进行类型转换。
是
dynamic_cast
在多态（继承）层次结构中对指针或引用执行运行时类型转换。
是
const_cast
添加或移除 const。
仅用于添加 const
reinterpret_cast
将一种类型的位级表示重新解释为另一种类型。
否
C 风格强制类型转换
执行
static_cast
、
const_cast
或
reinterpret_cast
的某种组合。
否
每个强制类型转换的工作方式都相同。作为输入，强制类型转换接受一个表达式（求值为一个值或一个对象）和一个目标类型。作为输出，强制类型转换返回转换结果。
因为它们是最常用的强制类型转换，所以我们将在本课中介绍 C 风格强制类型转换和
static_cast
。
相关内容
我们将在
25.10 -- 动态类型转换
课中讨论
dynamic_cast
，此前我们会先介绍其他前提主题。
const_cast
和
reinterpret_cast
通常应避免使用，因为它们只在极少数情况下有用，并且如果使用不当可能会造成损害。
警告
除非你有充分的理由使用
const_cast
和
reinterpret_cast
，否则请避免使用它们。
C 风格强制类型转换
在标准 C 编程中，类型转换是通过
operator()
完成的，要转换到的类型名称放在括号内，要转换的值紧跟在右括号之后。在 C++ 中，这种类型转换被称为**C 风格强制类型转换**。你可能仍然会在从 C 转换的代码中看到它们。
例如
#include <iostream>

int main()
{
    int x { 10 };
    int y { 4 };

    std::cout << (double)x / y << '\n'; // C-style cast of x to double

    return 0;
}
在上面的程序中，我们使用 C 风格强制类型转换来告诉编译器将
x
转换为
double
。因为
operator/
的左操作数现在求值为浮点值，所以右操作数也将转换为浮点值，并且除法将使用浮点除法而不是整数除法完成。
C++ 还提供了一种替代的 C 风格强制类型转换形式，称为**函数式强制类型转换**，它类似于函数调用
std::cout << double(x) / y << '\n'; //  // function-style cast of x to double
函数式类型转换使得更容易分辨出被转换的是什么（因为它看起来像一个标准的函数参数）。
在现代 C++ 中，通常会避免使用 C 风格类型转换，主要有几个原因。
首先，尽管 C 风格类型转换看起来是一个单一的类型转换，但它实际上可以根据其使用方式执行各种不同的转换。这可以包括静态转换、const 转换或 reinterpret 转换（后两者我们上面提到你应该避免）。C 风格类型转换并不能清楚地表明实际将执行哪些转换，这不仅使你的代码更难理解，而且还为无意中的误用打开了大门（你以为你正在实现一个简单的转换，结果却做了危险的事情）。通常这最终会产生一个直到运行时才被发现的错误。
此外，由于 C 风格强制类型转换只是一个类型名称、括号和变量或值，因此它们既难以识别（使你的代码更难阅读），也更难以搜索。
相比之下，具名转换易于发现和搜索，清晰地表明其作用，能力有限，并且在你尝试误用时会产生编译错误。
最佳实践
避免使用 C 风格强制类型转换。
致进阶读者
C 风格的强制类型转换会按顺序尝试执行以下 C++ 强制类型转换：
const_cast
static_cast
static_cast
，后跟
const_cast
reinterpret_cast
reinterpret_cast
，后跟
const_cast
C 风格强制类型转换有一点是 C++ 强制类型转换无法做到的：C 风格强制类型转换可以将派生对象转换为不可访问的基类（例如，因为它是私有继承的）。
static_cast
应该用于转换大多数值
C++ 中使用最广泛的强制类型转换运算符是**静态强制类型转换**运算符，通过
static_cast
关键字访问。当我们希望将一个类型的值显式转换为另一个类型的值时，使用
static_cast
。
你之前已经见过
static_cast
用于将
char
转换为
int
，以便
std::cout
将其打印为整数而不是字符
#include <iostream>

int main()
{
    char c { 'a' };
    std::cout << static_cast<int>(c) << '\n'; // prints 97 rather than a

    return 0;
}
要执行静态转换，我们首先使用
static_cast
关键字，然后将要转换的类型放在尖括号内。然后，在括号内，我们放置将要转换的表达式。请注意，该语法与名为
static_cast
()
的函数调用多么相似，其中将要转换的表达式作为参数提供！将值静态转换为另一种类型的值会返回一个用转换后的值直接初始化的临时对象。
下面是如何使用
static_cast
解决我们在本课开头提出的问题：
#include <iostream>

int main()
{
    int x { 10 };
    int y { 4 };

    // static cast x to a double so we get floating point division
    std::cout << static_cast<double>(x) / y << '\n'; // prints 2.5

    return 0;
}
static_cast
(x)
返回一个包含转换值
10.0
的临时
double
对象。这个临时对象随后用作浮点除法的左操作数。
static_cast
有两个重要的特性。
首先，
static_cast
提供编译时类型检查。如果我们尝试将值转换为某种类型而编译器不知道如何执行该转换，我们将收到编译错误。
// a C-style string literal can't be converted to an int, so the following is an invalid conversion
    int x { static_cast<int>("Hello") }; // invalid: will produce compilation error
其次，
static_cast
(有意地) 比 C 风格强制类型转换功能弱，因为它会阻止某些危险的转换 (例如那些需要重新解释或丢弃 const 的转换)。
最佳实践
当你需要将值从一种类型转换为另一种类型时，优先使用
static_cast
。
致进阶读者
由于 static_cast 使用直接初始化，因此在初始化要返回的临时对象时，会考虑目标类类型的任何显式构造函数。我们在
14.16 -- 转换构造函数和 explicit 关键字
课程中讨论显式构造函数。
使用
static_cast
显式进行窄化转换
当执行可能不安全（窄化）的隐式类型转换时，编译器通常会发出警告。例如，考虑以下代码片段：
int i { 48 };
char ch = i; // implicit narrowing conversion
将一个
int
(2 或 4 字节) 转换为
char
(1 字节) 可能不安全 (因为编译器无法判断整数值是否会溢出
char
的范围)，因此编译器通常会打印警告。如果我们使用列表初始化，编译器会产生错误。
为了解决这个问题，我们可以使用静态转换来显式地将我们的整数转换为
char
int i { 48 };

// explicit conversion from int to char, so that a char is assigned to variable ch
char ch { static_cast<char>(i) };
当我们这样做时，我们明确地告诉编译器这个转换是有意的，并且我们接受其后果（例如，如果发生溢出，
char
的范围会溢出）。由于此静态转换的输出类型是
char
，因此变量
ch
的初始化不会产生任何类型不匹配，因此不会有警告或错误。
这是另一个例子，编译器通常会抱怨将
double
转换为
int
可能会导致数据丢失
int i { 100 };
i = i / 2.5;
为了告诉编译器我们明确地要这样做
int i { 100 };
i = static_cast<int>(i / 2.5);
相关内容
我们将在
14.13 -- 临时类对象
课程中讨论更多与类类型相关的
static_cast
用法。
强制类型转换与初始化临时对象
假设我们有一个变量
x
需要转换为
int
。有两种常用的方法可以做到这一点：
static_cast
(x)
，返回一个由
x
直接初始化
的临时
int
对象。
int { x }
，创建一个由
x
直接列表初始化
的临时
int
对象。
我们应该避免使用
int ( x )
，它是一个 C 风格的强制类型转换。这将返回一个用
x
的值直接初始化的临时
int
（就像我们从语法中期望的那样），但它也有 C 风格强制类型转换部分提到的其他缺点（例如允许执行危险转换的可能性）。
static_cast
和直接列表初始化的临时对象之间至少存在三个显著差异
int { x }
使用列表初始化，这会禁止窄化转换。这在初始化变量时非常有用，因为在这种情况下我们很少打算丢失数据。但是在使用强制类型转换时，我们假设我们知道自己在做什么，如果我们要进行可能丢失一些数据的强制类型转换，我们应该能够这样做。在这种情况下，窄化转换限制可能会成为障碍。
我们来看一个例子，包括它如何导致平台特定的问题
#include <iostream>

int main()
{
    int x { 10 };
    int y { 4 };

    // We want to do floating point division, so one of the operands needs to be a floating point type
    std::cout << double{x} / y << '\n'; // okay if int is 32-bit, narrowing if x is 64-bit
}
在此示例中，我们已决定将
x
转换为
double
，以便执行浮点除法而不是整数除法。在 32 位架构上，这将正常工作（因为
double
可以表示 32 位
int
中可以存储的所有值，因此它不是窄化转换）。但在 64 位架构上，情况并非如此，因此将 64 位
int
转换为
double
是一种窄化转换。由于列表初始化禁止窄化转换，因此在
int
为 64 位的架构上将无法编译。
static_cast
更清楚地表明我们打算执行转换。尽管
static_cast
比直接列表初始化的替代方案更冗长，但在这种情况下，这是一件好事，因为它使转换更容易发现和搜索。这最终使你的代码更安全、更容易理解。
临时对象的直接列表初始化只允许单字类型名称。由于一个奇怪的语法怪癖，C++ 中有几个地方只允许单字类型名称（C++ 标准称这些名称为“简单类型说明符”）。因此，虽然
int { x }
是有效的转换语法，但
unsigned int { x }
不是。
您可以在以下示例中亲自看到这一点，它会产生编译错误：
#include <iostream>

int main()
{
    unsigned char c { 'a' };
    std::cout << unsigned int { c } << '\n';

    return 0;
}
有一些简单的方法可以解决这个问题，最简单的方法是使用单字类型别名：
#include <iostream>

int main()
{
    unsigned char c { 'a' };
    using uint = unsigned int;
    std::cout << uint { c } << '\n';

    return 0;
}
但是，既然可以直接
static_cast
，为什么要费这个劲呢？
由于所有这些原因，我们通常更喜欢
static_cast
而不是临时对象的直接列表初始化。
最佳实践
当需要进行类型转换时，优先使用
static_cast
而不是初始化临时对象。
小测验时间
问题 #1
隐式类型转换和显式类型转换有什么区别？
显示答案
当期望一种数据类型，但提供了另一种数据类型时，会自动执行隐式类型转换。
当程序员使用类型转换来显式地将一个值从一种类型转换为另一种类型时，就会发生显式类型转换。
下一课
10.7
类型定义和类型别名
返回目录
上一课
10.5
算术转换