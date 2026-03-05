# 1.10 — 表达式简介

1.10 — 表达式简介
Alex
2007 年 6 月 6 日，上午 8:15 PDT
2025 年 2 月 15 日
表达式
考虑以下一系列语句，每个语句都定义并初始化一个变量
// five() is a function that returns the value 5
int five()
{
    return 5;
}

int main()
{
    int a{ 2 };             // initialize variable a with literal value 2
    int b{ 2 + 3 };         // initialize variable b with computed value 5
    int c{ (2 * 3) + 4 };   // initialize variable c with computed value 10
    int d{ b };             // initialize variable d with variable value 5
    int e{ five() };        // initialize variable e with function return value 5

    return 0;
}
请注意，上面的初始化器使用了各种不同的实体：字面量、变量、运算符和函数调用。不知何故，C++ 将所有这些不同的东西转换成一个单一的值，然后可以用作变量的初始值。
所有这些初始化器有什么共同点？它们都使用了表达式。
在一般编程中，
表达式
是字面量、变量、运算符和函数调用的非空序列，用于计算一个值。执行表达式的过程称为
求值
，生成的结果值称为表达式的
结果
（有时也称为
返回值
）。
致进阶读者
在 C++ 中，表达式的结果是以下之一
一个值（最常见）
一个对象或一个函数。我们将在课程
12.2 -- 值类别（左值和右值）
中讨论返回对象的表达式。
无。这些是非值返回函数调用（在课程
2.3 -- 空函数（非值返回函数）
中介绍）的结果，这些函数调用仅用于其副作用
目前，为了简单起见，我们假设表达式求值以产生值。
当表达式求值时，表达式中的每个项都会被求值，直到只剩下一个值。以下是一些不同类型表达式的示例，并附有注释说明它们如何求值
2               // 2 is a literal that evaluates to value 2
"Hello world!"  // "Hello world!" is a literal that evaluates to text "Hello world!"
x               // x is a variable that evaluates to the value held by variable x
2 + 3           // operator+ uses operands 2 and 3 to evaluate to value 5
five()          // evaluates to the return value of function five()
如您所见，字面量求值得到它们自己的值。变量求值得到变量的值。运算符（例如
operator+
）使用其操作数求值得到其他值。我们尚未介绍函数调用，但在表达式的上下文中，函数调用求值得到函数返回的任何值。
致进阶读者
涉及带副作用的运算符的表达式有点复杂
x = 5           // x = 5 has side effect of assigning 5 to x, evaluates to x
x = 2 + 3       // has side effect of assigning 5 to x, evaluates to x
std::cout << x  // has side effect of printing value of x to console, evaluates to std::cout
关键见解
在 C++ 中，任何期望单个值的地方，您都可以使用产生值的表达式代替，并且表达式将被求值以产生单个值。
表达式不以分号结尾，也不能单独编译。例如，如果您尝试编译表达式
x = 5
，您的编译器会抱怨（可能是缺少分号）。相反，表达式总是作为语句的一部分进行求值。
例如，看这个语句
int x{ 2 + 3 }; // 2 + 3 is an expression that has no semicolon -- the semicolon is at the end of the statement containing the expression
如果您将此语句分解为其语法，它将如下所示
类型 标识符 { 表达式 };
type
可以是任何有效类型（我们选择
int
）。
identifier
可以是任何有效名称（我们选择
x
）。而
expression
可以是任何有效表达式（我们选择
2 + 3
，它使用两个字面量和一个运算符）。
表达式语句
某些表达式（例如
x = 5
）主要用于其副作用（在这种情况下，将值
5
赋值给变量
x
），而不是它们产生的值。
相关内容
我们在课程
1.9 -- 字面量和运算符简介
中介绍了副作用。
然而，我们上面提到表达式不能单独执行——它们必须作为语句的一部分存在。幸运的是，将任何表达式转换为等效语句是微不足道的。
表达式语句
是由一个表达式后跟一个分号组成的语句。当表达式语句执行时，表达式将被求值。
因此，我们可以获取任何表达式（例如
x = 5
），并将其转换为可编译的表达式语句（
x = 5;
）。
当表达式在表达式语句中使用时，表达式生成的任何结果都将被丢弃（因为它未使用）。例如，当表达式
x = 5
求值时，
operator=
的返回值将被丢弃。这很好，因为我们反正只是想将
5
赋值给
x
。
无用的表达式语句
我们还可以创建可编译但无效的表达式语句。例如，表达式语句（
2 * 3;
）是一个表达式语句，其表达式求值得到结果值
6
，然后该值被丢弃。虽然语法有效，但此类表达式语句是无用的。一些编译器（例如 gcc 和 Clang）如果能检测到表达式语句无用，则会产生警告。
子表达式、完整表达式和复合表达式
我们偶尔需要讨论特定类型的表达式。为此，我们将定义一些相关术语。
考虑以下表达式
2               // 2 is a literal that evaluates to value 2
2 + 3           // 2 + 3 uses operator+ to evaluate to value 5
x = 4 + 5       // 4 + 5 evaluates to value 9, which is then assigned to variable x
简化一下，
子表达式
是作为操作数使用的表达式。例如，
x = 4 + 5
的子表达式是
x
和
4 + 5
。
4 + 5
的子表达式是
4
和
5
。
完整表达式
是不是子表达式的表达式。上面所有三个表达式（
2
、
2 + 3
和
x = 4 + 5
）都是完整表达式。
在口语中，
复合表达式
是包含两个或更多运算符使用的表达式。
x = 4 + 5
是一个复合表达式，因为它包含两个运算符使用（
operator=
和
operator+
）。
2
和
2 + 3
不是复合表达式。
小测验时间
问题 #1
语句和表达式有什么区别？
显示答案
当我们希望程序执行动作时使用语句。当我们希望程序计算值时使用表达式。
问题 #2
指明以下每一行是
不包含表达式的语句
、
包含表达式的语句
，还是
表达式语句
。
a)
int x;
显示答案
语句不包含表达式。这是一个变量定义语句。在这种上下文中，
x
不是表达式，因为它正在被定义，而不是求值。
b)
int x = 5;
显示答案
语句包含表达式。
int x
是一个变量定义。
=
是复制初始化语法的一部分。等号右侧的初始化器是一个表达式。
c)
x = 5;
显示答案
表达式语句。
x = 5
是对
operator=
的调用，带有两个操作数：
x
和
5
。分号使其成为表达式语句。
d) 附加题
foo(); // foo is a function
显示答案
函数调用是表达式的一部分，所以这是一个表达式语句。
e) 附加题
std::cout << x; // Hint: operator<< is a binary operator.
显示答案
operator<<
是一个二元运算符，所以
std::cout
必须是左操作数，而
x
必须是右操作数。由于这是整个语句，这必须是一个表达式语句。
问题 #3
确定以下程序输出的值。不要编译此程序。只需在脑海中逐行思考即可。
#include <iostream>

int main()
{
	std::cout << 2 + 3 << '\n';
	
	int x{ 6 };
	int y{ x - 2 };
	std::cout << y << '\n';

	int z{};
	z = x;
	std::cout << z * x << '\n';

	return 0;
}
显示答案
5
4
36
下一课
1.11
开发你的第一个程序
返回目录
上一课
1.9
字面量和运算符简介