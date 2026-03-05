# 12.13 — 输入和输出参数

12.13 — 输入和输出参数
Alex
2023 年 7 月 31 日，上午 11:22 PDT
2024 年 12 月 9 日
函数及其调用者通过两种机制相互通信：参数和返回值。当函数被调用时，调用者提供实参，函数通过其形参接收这些实参。这些实参可以通过值、引用或地址传递。
通常，我们将通过值或 const 引用传递实参。但有时我们可能需要采取其他方式。
输入参数
在大多数情况下，函数形参仅用于接收调用者的输入。仅用于接收调用者输入的形参有时称为
输入参数
。
#include <iostream>

void print(int x) // x is an in parameter
{
    std::cout << x << '\n';
}

void print(const std::string& s) // s is an in parameter
{
    std::cout << s << '\n';
}

int main()
{
    print(5);
    std::string s { "Hello, world!" };
    print(s);

    return 0;
}
输入参数通常通过值或 const 引用传递。
输出参数
通过非 const 引用（或指向非 const 的指针）传递的函数实参允许函数修改作为实参传递的对象的值。这提供了一种函数将数据返回给调用者的方法，以防在某些情况下使用返回值不足。
仅用于将信息返回给调用者的函数形参称为
输出参数
。
例如
#include <cmath>    // for std::sin() and std::cos()
#include <iostream>

// sinOut and cosOut are out parameters
void getSinCos(double degrees, double& sinOut, double& cosOut)
{
    // sin() and cos() take radians, not degrees, so we need to convert
    constexpr double pi { 3.14159265358979323846 }; // the value of pi
    double radians = degrees * pi / 180.0;
    sinOut = std::sin(radians);
    cosOut = std::cos(radians);
}
 
int main()
{
    double sin { 0.0 };
    double cos { 0.0 };
 
    double degrees{};
    std::cout << "Enter the number of degrees: ";
    std::cin >> degrees;

    // getSinCos will return the sin and cos in variables sin and cos
    getSinCos(degrees, sin, cos);
 
    std::cout << "The sin is " << sin << '\n';
    std::cout << "The cos is " << cos << '\n';

    return 0;
}
此函数有一个参数
degrees
（其实参按值传递）作为输入，并“返回”两个参数（按引用）作为输出。
我们给这些输出参数命名时加上了“out”后缀，以表示它们是输出参数。这有助于提醒调用者，传递给这些参数的初始值无关紧要，并且我们应该期望它们被覆盖。按照惯例，输出参数通常是参数列表中最右侧的参数。
让我们更详细地探讨一下这是如何工作的。首先，main 函数创建局部变量
sin
和
cos
。这些变量通过引用（而不是按值）传递给函数
getSinCos()
。这意味着函数
getSinCos()
可以访问
main()
中实际的
sin
和
cos
变量，而不仅仅是副本。
getSinCos()
相应地将新值赋给
sin
和
cos
（分别通过引用
sinOut
和
cosOut
），这会覆盖
sin
和
cos
中的旧值。然后，函数
main()
打印这些更新后的值。
如果
sin
和
cos
是按值而不是按引用传递的，那么
getSinCos()
将会更改
sin
和
cos
的副本，导致任何更改在函数结束时被丢弃。但是由于
sin
和
cos
是按引用传递的，因此对
sin
或
cos
所做的任何更改（通过引用）都会在函数之外持续存在。因此，我们可以使用这种机制将值返回给调用者。
题外话…
StackOverflow 上的这个答案
是一篇有趣的读物，它解释了为什么非 const 左值引用不允许绑定到右值/临时对象（因为隐式类型转换与输出参数结合会产生意外行为）。
输出参数具有不自然的用法语法
输出参数虽然功能强大，但也有一些缺点。
首先，调用者必须实例化（并初始化）对象并将它们作为实参传递，即使它不打算使用它们。这些对象必须能够被赋值，这意味着它们不能是 const。
其次，由于调用者必须传入对象，这些值不能用作临时变量，也不能轻易地在单个表达式中使用。
以下示例显示了这两个缺点
#include <iostream>

int getByValue()
{
    return 5;
}

void getByReference(int& x)
{
    x = 5;
}

int main()
{
    // return by value
    [[maybe_unused]] int x{ getByValue() }; // can use to initialize object
    std::cout << getByValue() << '\n';      // can use temporary return value in expression

    // return by out parameter
    int y{};                // must first allocate an assignable object
    getByReference(y);      // then pass to function to assign the desired value
    std::cout << y << '\n'; // and only then can we use that value

    return 0;
}
如您所见，使用输出参数的语法有点不自然。
按引用传递的输出参数不会使其修改实参变得明显
当我们给一个对象的函数返回值赋值时，很明显这个对象的值正在被修改
x = getByValue(); // obvious that x is being modified
这很好，因为它清楚地表明我们应该期望
x
的值发生变化。
然而，让我们再次看一下上面示例中对
getSinCos()
的函数调用
getSinCos(degrees, sin, cos);
从这个函数调用中，不清楚
degrees
是输入参数，而
sin
和
cos
是输出参数。如果调用者没有意识到
sin
和
cos
将被修改，很可能会导致语义错误。
在某些情况下，使用按地址传递而不是按引用传递可以使输出参数更明显，因为这要求调用者将对象的地址作为实参传递。
考虑以下示例
void foo1(int x);  // pass by value
void foo2(int& x); // pass by reference
void foo3(int* x); // pass by address

int main()
{
    int i{};
 
    foo1(i);  // can't modify i
    foo2(i);  // can modify i (not obvious)
    foo3(&i); // can modify i

    int *ptr { &i };
    foo3(ptr); // can modify i (not obvious)

    return 0;
}
请注意，在调用
foo3(&i)
时，我们必须传入
&i
而不是
i
，这有助于更清楚地表明我们应该期望
i
被修改。
然而，这并非万无一失，因为
foo3(ptr)
允许
foo3()
修改
i
并且不要求调用者获取
ptr
的地址。
调用者也可能认为他们可以将
nullptr
或空指针作为有效参数传入，而这是不允许的。现在函数需要进行空指针检查和处理，这增加了复杂性。这种对额外空指针处理的需求通常比坚持按引用传递导致更多问题。
由于所有这些原因，除非没有其他好的选择，否则应避免使用输出参数。
最佳实践
避免使用输出参数（除非在极少数情况下没有更好的选择）。
对于非可选的输出参数，首选按引用传递。
输入/输出参数
在极少数情况下，函数实际上会在覆盖其值之前使用输出参数的值。这样的参数称为
输入/输出参数
。输入/输出参数与输出参数的功能相同，并且具有所有相同的挑战。
何时通过非 const 引用传递
如果您要通过引用传递以避免创建参数的副本，那么您几乎总是应该通过 const 引用传递。
作者注
在以下示例中，我们将使用
Foo
来表示我们关心的一些类型。现在，您可以将
Foo
想象为您选择的类型的类型别名（例如
std::string
）。
然而，有两种主要情况下，通过非 const 引用传递可能是更好的选择。
首先，当参数是输入/输出参数时，使用非 const 引用传递。由于我们已经传入了我们需要输出的对象，通常直接修改该对象更直接和高效。
void someFcn(Foo& inout)
{
    // modify inout
}

int main()
{
    Foo foo{};
    someFcn(foo); // foo modified after this call, may not be obvious

    return 0;
}
给函数一个好名字会有帮助
void modifyFoo(Foo& inout)
{
    // modify inout
}

int main()
{
    Foo foo{};
    modifyFoo(foo); // foo modified after this call, slightly more obvious

    return 0;
}
另一种方法是像往常一样通过值或 const 引用传递对象，并通过值返回一个新对象，然后调用者可以将其赋回原始对象
Foo someFcn(const Foo& in)
{
    Foo foo { in }; // copy here
    // modify foo
    return foo;
}

int main()
{
    Foo foo{};
    foo = someFcn(foo); // makes it obvious foo is modified, but another copy made here

    return 0;
}
这具有使用更传统的返回语法的优点，但需要额外创建 2 个副本（有时编译器可以优化掉其中一个副本）。
其次，当函数否则会通过值向调用者返回一个对象，但复制该对象
极其
昂贵时，请使用非 const 引用传递。特别是当函数在性能关键的代码段中多次调用时。
void generateExpensiveFoo(Foo& out)
{
    // modify out
}

int main()
{
    Foo foo{};
    generateExpensiveFoo(foo); // foo modified after this call

    return 0;
}
致进阶读者
上述最常见的例子是当函数需要用数据填充一个大型 C 风格数组或
std::array
，并且数组具有昂贵的复制元素类型时。我们将在未来的章节中讨论数组。
话虽如此，对象的复制很少会昂贵到需要诉诸非常规方法来返回这些对象。
下一课
12.14
指针、引用和 const 的类型推断
返回目录
上一课
12.12
按引用返回和按地址返回