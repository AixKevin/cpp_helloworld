# 12.2 — 值类别（左值和右值）

12.2 — 值类别（左值和右值）
Alex
2022 年 1 月 18 日，上午 10:04 PST
2025 年 1 月 3 日
在我们讨论第一个复合类型（左值引用）之前，我们先绕道谈谈什么是
lvalue
（左值）。
在课程
1.10 -- 表达式简介
中，我们将表达式定义为“文字、变量、运算符和函数调用的组合，可以执行以产生一个单一的值”。
例如
#include <iostream>

int main()
{
    std::cout << 2 + 3 << '\n'; // The expression 2 + 3 produces the value 5

    return 0;
}
在上面的程序中，表达式
2 + 3
被求值为值 5，然后将其打印到控制台。
在课程
6.4 -- 增量/减量运算符和副作用
中，我们还注意到表达式可以产生超出表达式生命周期的副作用。
#include <iostream>

int main()
{
    int x { 5 };
    ++x; // This expression statement has the side-effect of incrementing x
    std::cout << x << '\n'; // prints 6

    return 0;
}
在上面的程序中，表达式
++x
增加了
x
的值，即使在表达式完成求值后，该值仍保持改变。
除了产生值和副作用之外，表达式还可以做一件事：它们可以求值为对象或函数。我们稍后将进一步探讨这一点。
表达式的属性
为了帮助确定表达式应如何求值以及它们可以在何处使用，C++ 中的所有表达式都有两个属性：类型和值类别。
表达式的类型
表达式的类型等同于求值后的表达式所产生的值、对象或函数的类型。例如
int main()
{
    auto v1 { 12 / 4 }; // int / int => int
    auto v2 { 12.0 / 4 }; // double / int => double

    return 0;
}
对于
v1
，编译器将在编译时确定两个
int
操作数的除法将产生一个
int
结果，因此
int
是该表达式的类型。通过类型推断，
int
将被用作
v1
的类型。
对于
v2
，编译器将在编译时确定
double
操作数和
int
操作数的除法将产生一个
double
结果。请记住，算术运算符的操作数类型必须匹配，因此在这种情况下，
int
操作数会转换为
double
，并执行浮点除法。因此
double
是该表达式的类型。
编译器可以使用表达式的类型来确定表达式在给定上下文中是否有效。例如
#include <iostream>

void print(int x)
{
    std::cout << x << '\n';
}

int main()
{
    print("foo"); // error: print() was expecting an int argument, we tried to pass in a string literal

    return 0;
}
在上面的程序中，
print(int)
函数期望一个
int
参数。但是，我们传入的表达式类型（字符串字面量
"foo"
）不匹配，并且找不到转换。因此导致编译错误。
请注意，表达式的类型必须在编译时可确定（否则类型检查和类型推导将不起作用）——但是，表达式的值可以在编译时（如果表达式是 constexpr）或运行时（如果表达式不是 constexpr）确定。
表达式的值类别
现在考虑以下程序
int main()
{
    int x{};

    x = 5; // valid: we can assign 5 to x
    5 = x; // error: can not assign value of x to literal value 5

    return 0;
}
其中一个赋值语句是有效的（将值
5
赋给变量
x
），另一个是无效的（将
x
的值赋给字面值
5
意味着什么？）。那么编译器如何知道哪些表达式可以合法地出现在赋值语句的任意一侧呢？
答案在于表达式的第二个属性：
值类别
。表达式（或子表达式）的
值类别
指示表达式是否解析为值、函数或某种类型的对象。
在 C++11 之前，只有两种可能的值类别：
lvalue
（左值）和
rvalue
（右值）。
在 C++11 中，添加了三个额外的值类别（
glvalue
、
prvalue
和
xvalue
）以支持一项新特性，称为
move semantics
（移动语义）。
作者注
在本课程中，我们将坚持 C++11 之前的值类别视图，因为这使得值类别的介绍更加温和（并且是目前我们所需要的）。我们将在未来的章节中介绍移动语义（以及额外的三个值类别）。
左值和右值表达式
左值
（发音为“ell-value”，是“left value”或“locator value”的缩写，有时写成“l-value”）是一个求值为可识别对象或函数（或位域）的表达式。
C++ 标准使用了“identity”（标识）一词，但没有明确定义。具有标识的实体（例如对象或函数）可以与其他类似实体区分开来（通常通过比较实体的地址）。
具有标识的实体可以通过标识符、引用或指针访问，并且通常具有比单个表达式或语句更长的生命周期。
int main()
{
    int x { 5 };
    int y { x }; // x is an lvalue expression

    return 0;
}
在上面的程序中，表达式
x
是一个左值表达式，因为它求值为变量
x
（它有一个标识符）。
自从语言引入常量以来，左值有两种子类型：
可修改左值
是其值可以修改的左值。
不可修改左值
是其值不能修改的左值（因为左值是 const 或 constexpr）。
int main()
{
    int x{};
    const double d{};

    int y { x }; // x is a modifiable lvalue expression
    const double e { d }; // d is a non-modifiable lvalue expression

    return 0;
}
右值
（发音为“arr-value”，是“right value”的缩写，有时写成
r-value
）是不是左值的表达式。右值表达式求值为一个值。常见的右值包括字面量（C 风格字符串字面量除外，它们是左值）以及按值返回的函数和运算符的返回值。右值不可识别（这意味着它们必须立即使用），并且只存在于它们被使用的表达式的作用域内。
int return5()
{
    return 5;
}

int main()
{
    int x{ 5 }; // 5 is an rvalue expression
    const double d{ 1.2 }; // 1.2 is an rvalue expression

    int y { x }; // x is a modifiable lvalue expression
    const double e { d }; // d is a non-modifiable lvalue expression
    int z { return5() }; // return5() is an rvalue expression (since the result is returned by value)

    int w { x + 1 }; // x + 1 is an rvalue expression
    int q { static_cast<int>(d) }; // the result of static casting d to an int is an rvalue expression

    return 0;
}
您可能想知道为什么
return5()
、
x + 1
和
static_cast
(d)
是右值：答案是因为这些表达式产生的是不可识别的临时值。
关键见解
左值表达式求值为一个可识别的对象。
右值表达式求值为一个值。
值类别和运算符
除非另有说明，否则运算符期望其操作数为右值。例如，二元
operator+
期望其操作数为右值
#include <iostream>

int main()
{
    std::cout << 1 + 2; // 1 and 2 are rvalues, operator+ returns an rvalue

    return 0;
}
字面量
1
和
2
都是右值表达式。
operator+
将乐于使用它们返回右值表达式
3
。
现在我们可以回答为什么
x = 5
有效而
5 = x
无效的问题：赋值操作要求其左操作数是可修改的左值表达式。后一个赋值（
5 = x
）失败是因为左操作数表达式
5
是一个右值，而不是一个可修改的左值。
int main()
{
    int x{};

    // Assignment requires the left operand to be a modifiable lvalue expression and the right operand to be an rvalue expression
    x = 5; // valid: x is a modifiable lvalue expression and 5 is an rvalue expression
    5 = x; // error: 5 is an rvalue expression and x is a modifiable lvalue expression

    return 0;
}
左值到右值转换
由于赋值操作期望右操作数是右值表达式，您可能想知道为什么以下代码有效
int main()
{
    int x{ 1 };
    int y{ 2 };

    x = y; // y is not an rvalue, but this is legal

    return 0;
}
在期望右值但提供了左值的情况下，左值将进行左值到右值的转换，以便可以在此类上下文中使用。这基本上意味着左值被求值以产生其值，该值是一个右值。
在上面的例子中，左值表达式
y
经过左值到右值的转换，将
y
求值为一个右值（
2
），然后将其赋值给
x
。
关键见解
左值会隐式转换为右值。这意味着左值可以在任何期望右值的地方使用。
另一方面，右值不会隐式转换为左值。
现在考虑这个例子
int main()
{
    int x { 2 };

    x = x + 1;

    return 0;
}
在这个语句中，变量
x
在两个不同的上下文中使用。在赋值运算符的左侧（需要左值表达式的地方），
x
是一个求值为变量
x
的左值表达式。在赋值运算符的右侧，
x
经过左值到右值的转换，然后被求值，以便其值（
2
）可以用作
operator+
的左操作数。
operator+
返回右值表达式
3
，然后将其用作赋值的右操作数。
如何区分左值和右值
您可能仍然对哪些表达式是左值，哪些是右值感到困惑。例如，
operator++
的结果是左值还是右值？我们将在这里介绍几种可以用来确定它们的哪个是哪个的方法。
提示
识别左值和右值表达式的经验法则
左值表达式是那些求值为函数或可识别对象（包括变量），并且在表达式结束之后仍然存在的表达式。
右值表达式是那些求值为值，包括字面量和在表达式结束之后不再存在的临时对象的表达式。
有关左值和右值表达式的更完整列表，您可以查阅技术文档。
提示
左值和右值表达式的完整列表可以在
这里
找到。在 C++11 中，右值分为两种子类型：prvalues 和 xvalues，因此我们这里讨论的右值是这两个类别的总和。
最后，我们可以编写一个程序，让编译器告诉我们某个表达式是什么类型的表达式。以下代码演示了一种确定表达式是左值还是右值的方法
#include <iostream>
#include <string>

// T& is an lvalue reference, so this overload will be preferred for lvalues
template <typename T>
constexpr bool is_lvalue(T&)
{
    return true;
}

// T&& is an rvalue reference, so this overload will be preferred for rvalues
template <typename T>
constexpr bool is_lvalue(T&&)
{
    return false;
}

// A helper macro (#expr prints whatever is passed in for expr as text)
#define PRINTVCAT(expr) { std::cout << #expr << " is an " << (is_lvalue(expr) ? "lvalue\n" : "rvalue\n"); }

int getint() { return 5; }

int main()
{
    PRINTVCAT(5);        // rvalue
    PRINTVCAT(getint()); // rvalue
    int x { 5 };
    PRINTVCAT(x);        // lvalue
    PRINTVCAT(std::string {"Hello"}); // rvalue
    PRINTVCAT("Hello");  // lvalue
    PRINTVCAT(++x);      // lvalue
    PRINTVCAT(x++);      // rvalue
}
这会打印
5 is an rvalue
getint() is an rvalue
x is an lvalue
std::string {"Hello"} is an rvalue
"Hello" is an lvalue
++x is an lvalue
x++ is an rvalue
此方法依赖于两个重载函数：一个带有左值引用参数，另一个带有右值引用参数。左值引用版本将优先用于左值参数，右值引用版本将优先用于右值参数。因此，我们可以根据选择了哪个函数来确定参数是左值还是右值。
因此，正如您所看到的，
operator++
的结果是左值还是右值取决于它是作为前缀运算符（返回左值）还是后缀运算符（返回右值）使用！
致进阶读者
与其他字面量（都是右值）不同，C 风格字符串字面量是左值，因为 C 风格字符串（C 风格数组）会衰变为指针。衰变过程只有当数组是左值时才有效（因此它有一个可以存储在指针中的地址）。C++ 为了向后兼容继承了这一点。
我们在课程
17.8 -- C 风格数组衰变
中介绍了数组衰变。
现在我们已经介绍了左值，我们可以开始学习我们的第一个复合类型：
左值引用
。
下一课
12.3
左值引用
返回目录
上一课
12.1
复合数据类型简介