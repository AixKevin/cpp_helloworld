# 11.2 — 函数重载区分

11.2 — 函数重载区分
Alex
2021年6月17日，太平洋夏令时下午5:43
2024年12月11日
在上一课（
11.1 -- 函数重载简介
）中，我们介绍了函数重载的概念，它允许我们创建多个同名函数，只要每个同名函数具有不同的参数类型（或者函数可以通过其他方式区分）。
在本课中，我们将仔细研究如何区分重载函数。未正确区分的重载函数将导致编译器发出编译错误。
如何区分重载函数
函数属性
用于区分
备注
参数数量
是
参数类型
是
排除 typedef、类型别名和值参数上的 const 限定符。包括省略号。
返回类型
否
请注意，函数的返回类型不用于区分重载函数。我们稍后会详细讨论。
致进阶读者
对于成员函数，还会考虑额外的函数级限定符
函数级限定符
用于重载
const 或 volatile
是
引用限定符
是
例如，const 成员函数可以与否则相同的非 const 成员函数区分开来（即使它们共享相同的参数集）。
相关内容
我们在第
20.5 -- 省略号（以及为什么要避免它们）
课中介绍了省略号。
基于参数数量的重载
只要每个重载函数具有不同数量的参数，就可以区分重载函数。例如
int add(int x, int y)
{
    return x + y;
}

int add(int x, int y, int z)
{
    return x + y + z;
}
编译器可以很容易地判断具有两个整数参数的函数调用应该转到
add(int, int)
，而具有三个整数参数的函数调用应该转到
add(int, int, int)
。
基于参数类型的重载
只要每个重载函数的参数类型列表不同，也可以区分函数。例如，以下所有重载都是可区分的
int add(int x, int y); // integer version
double add(double x, double y); // floating point version
double add(int x, double y); // mixed version
double add(double x, int y); // mixed version
由于类型别名（或 typedef）不是不同的类型，因此使用类型别名的重载函数与使用别名类型的重载函数没有区别。例如，以下所有重载都不可区分（并将导致编译错误）
typedef int Height; // typedef
using Age = int; // type alias

void print(int value);
void print(Age value); // not differentiated from print(int)
void print(Height value); // not differentiated from print(int)
对于按值传递的参数，const 限定符也不被考虑。因此，以下函数不被视为可区分的
void print(int);
void print(const int); // not differentiated from print(int)
致进阶读者
我们还没有介绍省略号，但省略号参数被认为是一种独特的参数类型
void foo(int x, int y);
void foo(int x, ...); // differentiated from foo(int, int)
因此，对
foo(4, 5)
的调用将匹配
foo(int, int)
，而不是
foo(int, ...)
。
函数的返回类型不考虑区分
在区分重载函数时，不考虑函数的返回类型。
考虑这样一种情况：您想编写一个返回随机数的函数，但您需要一个返回 int 的版本，以及另一个返回 double 的版本。您可能会倾向于这样做
int getRandomValue();
double getRandomValue();
在 Visual Studio 2019 上，这会导致以下编译错误
error C2556: 'double getRandomValue(void)': overloaded function differs only by return type from 'int getRandomValue(void)'
这很有道理。如果您是编译器，并且看到这个语句
getRandomValue();
您会调用两个重载函数中的哪一个？这不清楚。
题外话…
这是一个有意的选择，因为它确保函数调用的行为可以独立于表达式的其余部分确定，从而使理解复杂表达式变得更简单。换句话说，我们总是可以仅根据函数调用中的参数来确定将调用哪个版本的函数。如果返回值为区分所用，那么我们将没有一个简单的语法方式来判断调用了函数的哪个重载——我们还必须了解返回值的用途，这需要更多的分析。
解决此问题的最佳方法是为函数提供不同的名称
int getRandomInt();
double getRandomDouble();
类型签名
函数的
类型签名
（通常称为
签名
）定义为函数头中用于函数区分的部分。在 C++ 中，这包括函数名、参数数量、参数类型和函数级限定符。值得注意的是，它
不
包括返回类型。
名称修饰
题外话…
当编译器编译函数时，它会执行
名称修饰
，这意味着函数的编译名称会根据各种标准（例如参数的数量和类型）进行更改（“修饰”），以便链接器可以使用唯一的名称。
例如，具有原型
int fcn()
的函数可能会编译为修饰名
__fcn_v
，而
int fcn(int)
可能会编译为修饰名
__fcn_i
。因此，虽然在源代码中，两个重载函数共享名称
fcn()
，但在编译代码中，修饰名称是唯一的（
__fcn_v
与
__fcn_i
）。
名称修饰的方式没有标准化，因此不同的编译器会生成不同的修饰名称。
下一课
11.3
函数重载解析和模糊匹配
返回目录
上一课
11.1
函数重载简介