# 6.1 — 运算符优先级和结合性

6.1 — 运算符优先级和结合性
Alex
2007年6月13日，太平洋夏令时下午3:55
2025年2月19日
章节介绍
本章建立在第
1.9 课 -- 字面量和运算符简介
的概念之上。下面快速回顾一下。
运算
是一个数学过程，涉及零个或多个输入值（称为
操作数
），产生一个新值（称为输出值）。要执行的具体运算由一个结构（通常是一个符号或一对符号）表示，该结构称为
运算符
。
例如，我们从小就知道
2 + 3
等于
5
。在这种情况下，字面量
2
和
3
是操作数，符号
+
是运算符，它告诉我们对操作数应用数学加法以产生新值
5
。由于这里只使用了一个运算符，所以这很简单。
在本章中，我们将讨论与运算符相关的主题，并探索 C++ 支持的许多常见运算符。
复合表达式的求值
现在，让我们考虑一个复合表达式，例如
4 + 2 * 3
。它应该被分组为
(4 + 2) * 3
，结果为
18
，还是
4 + (2 * 3)
，结果为
10
？根据正常的数学优先级规则（乘法在加法之前解析），我们知道上述表达式应分组为
4 + (2 * 3)
以产生值
10
。但编译器是如何知道的呢？
为了求值表达式，编译器必须做两件事：
在编译时，编译器必须解析表达式并确定操作数如何与运算符分组。这通过优先级和结合性规则完成，我们稍后将讨论。
在编译时或运行时，操作数被求值并执行操作以产生结果。
运算符优先级
为了帮助解析复合表达式，所有运算符都被分配了一个优先级级别。
优先级
级别较高的运算符首先与操作数分组。
您可以在下表中看到，乘法和除法（优先级级别 5）比加法和减法（优先级级别 6）具有更高的优先级级别。因此，乘法和除法将在加法和减法之前与操作数分组。换句话说，
4 + 2 * 3
将被分组为
4 + (2 * 3)
。
运算符结合性
考虑一个复合表达式，例如
7 - 4 - 1
。它应该被分组为
(7 - 4) - 1
，结果为
2
，还是
7 - (4 - 1)
，结果为
4
？由于两个减法运算符具有相同的优先级级别，编译器无法仅凭优先级来确定它应该如何分组。
如果表达式中两个具有相同优先级级别的运算符相邻，则运算符的
结合性
告诉编译器是自左向右求值运算符（而不是操作数！）还是自右向左求值运算符。减法的优先级级别为 6，并且优先级级别为 6 的运算符的结合性是自左向右。因此，此表达式从左到右分组：
(7 - 4) - 1
。
运算符优先级和结合性表
下表主要是一个参考图表，您可以在将来查阅它来解决您可能有的任何优先级或结合性问题。
备注
优先级级别 1 是最高优先级级别，级别 17 是最低优先级级别。优先级级别较高的运算符其操作数首先分组。
L->R 表示从左到右结合性。
R->L 表示从右到左结合性。
优先级/结合性
运算符
描述
模式
1 L->R
::
::
全局作用域（一元）
命名空间作用域（二元）
::name
class_name::member_name
2 L->R
()
()
type()
type{}
[]
.
->
++
––
typeid
const_cast
dynamic_cast
reinterpret_cast
static_cast
sizeof…
noexcept
alignof
括号
函数调用
函数式转换
列表初始化临时对象（C++11）
数组下标
对象成员访问
对象指针成员访问
后置递增
后置递减
运行时类型信息
去除const限定
运行时类型检查转换
类型转换
编译时类型检查转换
获取参数包大小
编译时异常检查
获取类型对齐方式
(expression)
function_name(arguments)
type(expression)
type{expression}
pointer[expression]
object.member_name
object_pointer->member_name
lvalue++
lvalue––
typeid(type) or typeid(expression)
const_cast<type>(expression)
dynamic_cast<type>(expression)
reinterpret_cast<type>(expression)
static_cast<type>(expression)
sizeof…(expression)
noexcept(expression)
alignof(type)
3 R->L
+
-
++
––
!
not
~
(type)
sizeof
co_await
&
*
new
new[]
delete
delete[]
一元加
一元减
前置递增
前置递减
逻辑非
逻辑非
按位非
C风格转换
字节大小
等待异步调用
取地址
解引用
动态内存分配
动态数组分配
动态内存删除
动态数组删除
+expression
-expression
++lvalue
––lvalue
!expression
not expression
~expression
(new_type)expression
sizeof(type) or sizeof(expression)
co_await expression (C++20)
&lvalue
*expression
new type
new type[expression]
delete pointer
delete[] pointer
4 L->R
->*
.*
成员指针选择器
成员对象选择器
object_pointer->*pointer_to_member
object.*pointer_to_member
5 L->R
*
/
%
乘法
除法
取余
expression * expression
expression / expression
expression % expression
6 L->R
+
-
加法
减法
expression + expression
expression - expression
7 L->R
<<
>>
位左移 / 插入
位右移 / 提取
expression << expression
expression >> expression
8 L->R
<=>
三路比较 (C++20)
expression <=> expression
9 L->R
<
<=
>
>=
小于比较
小于等于比较
大于比较
大于等于比较
expression < expression
expression <= expression
expression > expression
expression >= expression
10 L->R
==
!=
相等
不等
expression == expression
expression != expression
11 L->R
&
按位与
expression & expression
12 L->R
^
按位异或
expression ^ expression
13 L->R
|
按位或
expression | expression
14 L->R
&&
and
逻辑与
逻辑与
expression && expression
expression and expression
15 L->R
||
或
逻辑或
逻辑或
expression || expression
expression or expression
16 R->L
throw
co_yield
?:
=
*=
/=
%=
+=
-=
<<=
>>=
&=
|=
^=
抛出表达式
yield 表达式 (C++20)
条件
赋值
乘法赋值
除法赋值
取余赋值
加法赋值
减法赋值
位左移赋值
位右移赋值
按位与赋值
按位或赋值
按位异或赋值
throw expression
co_yield expression
expression ? expression : expression
lvalue = expression
lvalue *= expression
lvalue /= expression
lvalue %= expression
lvalue += expression
lvalue -= expression
lvalue <<= expression
lvalue >>= expression
lvalue &= expression
lvalue |= expression
lvalue ^= expression
17 L->R
,
逗号运算符
expression, expression
您应该已经认识其中一些运算符，例如
+
、
-
、
*
、
/
、
()
和
sizeof
。然而，除非您有其他编程语言的经验，否则此表中的大多数运算符现在对您来说可能是不可理解的。这一点是预料之中的。我们将在本章中介绍其中许多，其余的将在需要时介绍。
问：指数运算符在哪里？
C++ 不包含用于幂运算的运算符（
operator^
在 C++ 中有不同的功能）。我们在
6.3 -- 取余和幂运算
这一课中更详细地讨论幂运算。
请注意，
operator<<
处理位左移和插入，而
operator>>
处理位右移和提取。编译器可以根据操作数的类型来确定执行哪个操作。
加括号
由于优先级规则，
4 + 2 * 3
将被分组为
4 + (2 * 3)
。但是，如果我们实际想表达的是
(4 + 2) * 3
怎么办？就像在普通数学中一样，在 C++ 中，我们可以显式使用括号来根据我们的需要设置操作数的分组。这是因为括号具有最高的优先级级别之一，因此括号通常在它们内部的内容之前求值。
使用括号使复合表达式更容易理解
现在考虑一个像
x && y || z
这样的表达式。它会被求值为
(x && y) || z
还是
x && (y || z)
？你可以查表发现
&&
的优先级高于
||
。但是运算符和优先级级别太多了，很难全部记住。而且你不想每次都查运算符来理解复合表达式是如何求值的。
为了减少错误并使您的代码更容易理解，而无需查阅优先级表，最好将任何非平凡的复合表达式用括号括起来，以便清楚您的意图。
最佳实践
使用括号明确非平凡复合表达式的求值方式（即使在技术上并非必要）。
一个好的经验法则是：除了加法、减法、乘法和除法之外，所有表达式都加括号。
上述最佳实践还有一个额外的例外：只有一个赋值运算符（且没有逗号运算符）的表达式不需要将赋值的右操作数用括号括起来。
例如
x = (y + z + w);   // instead of this
x = y + z + w;     // it's okay to do this

x = ((y || z) && w); // instead of this
x = (y || z) && w;   // it's okay to do this

x = (y *= z); // expressions with multiple assignments still benefit from parenthesis
赋值运算符的优先级次低（仅逗号运算符更低，且它很少使用）。因此，只要只有一个赋值（且没有逗号），我们就知道右操作数将在赋值之前完全求值。
最佳实践
只有一个赋值运算符的表达式不需要将赋值的右操作数用括号括起来。
运算的值计算
C++ 标准使用术语
值计算
来表示表达式中运算符的执行以产生一个值。优先级和结合性规则决定了值计算发生的顺序。
例如，给定表达式
4 + 2 * 3
，由于优先级规则，它被分组为
4 + (2 * 3)
。
(2 * 3)
的值计算必须首先发生，以便
4 + 6
的值计算可以完成。
操作数的求值
C++ 标准（主要）使用术语
求值
来指代操作数的求值（而不是运算符或表达式的求值！）。例如，给定表达式
a + b
，
a
将被求值以产生某个值，
b
将被求值以产生某个值。然后这些值可以用作
operator+
的操作数进行值计算。
命名法
非正式地，我们通常使用“求值”一词来指代整个表达式的求值（值计算），而不仅仅是表达式的操作数。
操作数（包括函数参数）的求值顺序大多未指定
在大多数情况下，操作数和函数参数的求值顺序未指定，这意味着它们可以按任何顺序求值。
考虑以下表达式：
a * b + c * d
我们从上面的优先级和结合性规则中得知，这个表达式将被分组，就像我们输入了
(a * b) + (c * d)
如果
a
是
1
，
b
是
2
，
c
是
3
，
d
是
4
，这个表达式将始终计算出值
14
。
然而，优先级和结合性规则只告诉我们运算符和操作数是如何分组的以及值计算发生的顺序。它们没有告诉我们操作数或子表达式的求值顺序。编译器可以自由地按任何顺序求值操作数
a
、
b
、
c
或
d
。编译器也可以自由地先计算
a * b
或
c * d
。
对于大多数表达式，这无关紧要。在我们上面的示例表达式中，变量
a
、
b
、
c
或
d
的值以何种顺序求值并不重要：计算出的值将始终是
14
。这里没有歧义。
但是，可以编写求值顺序确实很重要的表达式。考虑这个程序，它包含一个 C++ 新手程序员经常犯的错误。
#include <iostream>

int getValue()
{
    std::cout << "Enter an integer: ";

    int x{};
    std::cin >> x;
    return x;
}

void printCalculation(int x, int y, int z)
{
    std::cout << x + (y * z);
}

int main()
{
    printCalculation(getValue(), getValue(), getValue()); // this line is ambiguous

    return 0;
}
如果您运行此程序并输入
1
、
2
和
3
，您可能会认为该程序会计算
1 + (2 * 3)
并打印
7
。但这假设
printCalculation()
的参数将按从左到右的顺序求值（因此参数
x
得到值
1
，
y
得到值
2
，
z
得到值
3
）。如果相反，参数按从右到左的顺序求值（因此参数
z
得到值
1
，
y
得到值
2
，
x
得到值
3
），那么程序将打印
5
。
提示
Clang 编译器按从左到右的顺序求值参数。GCC 编译器按从右到左的顺序求值参数。
如果您想亲自查看此行为，可以在
Wandbox
上进行。将上面的程序粘贴进去，在“Stdin”选项卡中输入
1 2 3
，选择 GCC 或 Clang，然后编译程序。输出将出现在页面底部（您可能需要向下滚动才能看到）。您会注意到 GCC 和 Clang 的输出不同！
通过将每个对
getValue()
的函数调用作为一个单独的语句，可以使上述程序消除歧义。
#include <iostream>

int getValue()
{
    std::cout << "Enter an integer: ";

    int x{};
    std::cin >> x;
    return x;
}

void printCalculation(int x, int y, int z)
{
    std::cout << x + (y * z);
}

int main()
{
    int a{ getValue() }; // will execute first
    int b{ getValue() }; // will execute second
    int c{ getValue() }; // will execute third

    printCalculation(a, b, c); // this line is now unambiguous

    return 0;
}
在此版本中，
a
将始终为
1
，
b
将为
2
，
c
将为
3
。当
printCalculation()
的参数被求值时，参数求值的顺序无关紧要——参数
x
始终会得到值
1
，
y
会得到值
2
，
z
会得到值
3
。此版本将确定性地打印
7
。
关键见解
操作数、函数参数和子表达式可以按任何顺序求值。
一个常见的错误是认为运算符优先级和结合性会影响求值顺序。优先级和结合性仅用于确定操作数如何与运算符分组，以及值计算的顺序。
警告
确保您编写的表达式（或函数调用）不依赖于操作数（或参数）的求值顺序。
相关内容
具有副作用的运算符也可能导致意外的求值结果。我们将在
6.4 -- 递增/递减运算符和副作用
这一课中介绍。
小测验时间
问题 #1
你从日常数学中知道，括号内的表达式会首先求值。例如，在表达式
(2 + 3) * 4
中，
(2 + 3)
部分首先求值。
对于此练习，您将获得一组没有括号的表达式。使用上表中的运算符优先级和结合性规则，为每个表达式添加括号，以明确编译器将如何求值该表达式。
显示提示
提示：使用上表中的模式列来确定运算符是一元的（有一个操作数）还是二元的（有两个操作数）。如果您需要复习一元和二元运算符是什么，请查阅
1.9 -- 字面量和运算符简介
课程。
示例问题：x = 2 + 3 % 4
二元运算符
%
的优先级高于运算符
+
或运算符
=
，因此它首先被求值
x = 2 + (3 % 4)
二元运算符
+
的优先级高于运算符
=
，因此它接下来被求值
最终答案：x = (2 + (3 % 4))
我们现在不再需要上表来理解这个表达式将如何求值。
a) x = 3 + 4 + 5;
显示答案
二元运算符
+
具有高于
=
的优先级
x = (3 + 4 + 5);
二元运算符
+
具有从左到右的结合性
最终答案：x = ((3 + 4) + 5);
b) x = y = z;
显示答案
二元运算符
=
具有从右到左的结合性
最终答案：x = (y = z);
c) z *= ++y + 5;
显示答案
一元运算符
++
具有最高优先级
z *= (++y) + 5;
二元运算符
+
具有次高优先级
最终答案：z *= ((++y) + 5);
d) a || b && c || d;
显示答案
二元运算符
&&
具有高于
||
的优先级
a || (b && c) || d;
二元运算符
||
具有从左到右的结合性
最终答案：(a || (b && c)) || d;
下一课
6.2
算术运算符
返回目录
上一课
5.x
第5章 总结与测验