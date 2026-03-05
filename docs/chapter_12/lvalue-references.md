# 12.3 — 左值引用

12.3 — 左值引用
Alex
2007 年 7 月 16 日，太平洋夏令时下午 6:19
2024 年 11 月 11 日
在 C++ 中，**引用 (reference)** 是现有对象的别名。一旦定义了引用，对引用的任何操作都会应用于被引用的对象。这意味着我们可以使用引用来读取或修改被引用的对象。
尽管引用乍一看可能显得愚蠢、无用或冗余，但它们在 C++ 中无处不在（我们会在接下来的几节课中看到示例）。
关键见解
引用本质上与被引用的对象相同。
你也可以创建函数引用，尽管这种情况较少见。
现代 C++ 包含两种类型的引用：左值引用和右值引用。在本章中，我们将讨论左值引用。
相关内容
因为本课中我们将讨论左值和右值，如果你需要复习这些术语，请在继续之前查看
12.2 -- 值类别（左值和右值）
。右值引用将在移动语义一章中介绍（
第 22 章
）。
左值引用类型
**左值引用**（通常简称为“引用”，因为在 C++11 之前只有一种类型的引用）充当现有左值（例如变量）的别名。
就像对象的类型决定了它能容纳什么类型的值一样，引用的类型决定了它能引用什么类型的对象。左值引用类型可以通过在类型说明符中使用单个与号（&）来识别。
// regular types
int        // a normal int type (not an reference)
int&       // an lvalue reference to an int object
double&    // an lvalue reference to a double object
const int& // an lvalue reference to a const int object
例如，
int&
是对
int
对象的左值引用类型，而
const int&
是对
const int
对象的左值引用类型。
指定引用的类型（例如
int&
）被称为**引用类型 (reference type)**。可以被引用的类型（例如
int
）被称为**被引用类型 (referenced type)**。
命名法
左值引用有两种
对非 const 的左值引用通常简称为“左值引用”，但也可以称为**对非 const 的左值引用 (lvalue reference to non-const)** 或**非 const 左值引用 (non-const lvalue reference)**（因为它没有使用
const
关键字定义）。
对 const 的左值引用通常称为**对 const 的左值引用 (lvalue reference to const)** 或**const 左值引用 (const lvalue reference)**。
我们将在本课中重点讨论非 const 左值引用，在下一课中（
12.4 -- 对 const 的左值引用
）讨论 const 左值引用。
左值引用变量
我们可以用左值引用类型做的一件事是创建左值引用变量。**左值引用变量 (lvalue reference variable)** 是一个作为左值（通常是另一个变量）引用的变量。
要创建左值引用变量，我们只需定义一个具有左值引用类型的变量。
#include <iostream>

int main()
{
    int x { 5 };    // x is a normal integer variable
    int& ref { x }; // ref is an lvalue reference variable that can now be used as an alias for variable x

    std::cout << x << '\n';  // print the value of x (5)
    std::cout << ref << '\n'; // print the value of x via ref (5)

    return 0;
}
在上面的示例中，类型
int&
将
ref
定义为对 int 的左值引用，然后我们用左值表达式
x
初始化它。此后，
ref
和
x
可以同义使用。因此，该程序打印：
5
5
从编译器的角度来看，与号是“附加”到类型名称 (
int& ref
) 还是变量名称 (
int &ref
) 并不重要，你选择哪种方式是风格问题。现代 C++ 程序员倾向于将与号附加到类型，因为这更清楚地表明引用是类型信息的一部分，而不是标识符的一部分。
最佳实践
定义引用时，将与号放在类型旁边（而不是引用变量的名称旁边）。
致进阶读者
对于已经熟悉指针的人来说，此上下文中的与号不表示“地址”，它表示“左值引用”。
通过非 const 左值引用修改值
在上面的示例中，我们展示了可以使用引用来读取被引用对象的值。我们还可以使用非 const 引用来修改被引用对象的值。
#include <iostream>

int main()
{
    int x { 5 }; // normal integer variable
    int& ref { x }; // ref is now an alias for variable x

    std::cout << x << ref << '\n'; // print 55

    x = 6; // x now has value 6

    std::cout << x << ref << '\n'; // prints 66

    ref = 7; // the object being referenced (x) now has value 7

    std::cout << x << ref << '\n'; // prints 77

    return 0;
}
此代码打印
55
66
77
在上面的示例中，
ref
是
x
的别名，因此我们可以通过
x
或
ref
更改
x
的值。
引用初始化
与常量非常相似，所有引用都必须初始化。引用使用一种称为**引用初始化 (reference initialization)** 的初始化形式进行初始化。
int main()
{
    int& invalidRef;   // error: references must be initialized

    int x { 5 };
    int& ref { x }; // okay: reference to int is bound to int variable

    return 0;
}
当引用用对象（或函数）初始化时，我们说它**绑定 (bound)** 到该对象（或函数）。这种引用绑定的过程称为**引用绑定 (reference binding)**。被引用的对象（或函数）有时被称为**指代物 (referent)**。
非 const 左值引用只能绑定到**可修改的**左值。
int main()
{
    int x { 5 };
    int& ref { x };         // okay: non-const lvalue reference bound to a modifiable lvalue

    const int y { 5 };
    int& invalidRef { y };  // invalid: non-const lvalue reference can't bind to a non-modifiable lvalue 
    int& invalidRef2 { 0 }; // invalid: non-const lvalue reference can't bind to an rvalue

    return 0;
}
关键见解
如果非 const 左值引用可以绑定到不可修改的（const）左值或右值，那么你将能够通过引用更改这些值，这将违反它们的 const 属性。
不允许对
void
的左值引用（有什么意义呢？）。
尽管引用的类型（例如
int&
）与被绑定对象的类型（例如
int
）不完全匹配，但这里不应用任何转换（甚至不是微不足道的转换）——类型差异作为引用初始化过程的一部分处理。
引用（通常）只绑定到与其被引用类型匹配的对象
在大多数情况下，引用只绑定到类型与其被引用类型匹配的对象（此规则有一些例外，我们将在讨论继承时讨论）。
如果你尝试将引用绑定到类型与其被引用类型不匹配的对象，编译器将尝试隐式地将对象转换为被引用类型，然后将引用绑定到该类型。
关键见解
由于转换的结果是右值，并且非 const 左值引用不能绑定到右值，因此尝试将非 const 左值引用绑定到类型与其被引用类型不匹配的对象将导致编译错误。
int main()
{
    int x { 5 };
    int& ref { x };            // okay: referenced type (int) matches type of initializer

    double d { 6.0 };
    int& invalidRef { d };     // invalid: conversion of double to int is narrowing conversion, disallowed by list initialization
    double& invalidRef2 { x }; // invalid: non-const lvalue reference can't bind to rvalue (result of converting x to double)

    return 0;
}
引用不能重新绑定（更改为引用另一个对象）
一旦初始化，C++ 中的引用就不能**重新绑定 (reseated)**，这意味着它不能更改为引用另一个对象。
新的 C++ 程序员经常尝试通过使用赋值来为引用提供另一个变量来重新绑定引用。这会编译和运行——但功能不符合预期。考虑以下程序：
#include <iostream>

int main()
{
    int x { 5 };
    int y { 6 };

    int& ref { x }; // ref is now an alias for x
    
    ref = y; // assigns 6 (the value of y) to x (the object being referenced by ref)
    // The above line does NOT change ref into a reference to variable y!

    std::cout << x << '\n'; // user is expecting this to print 5

    return 0;
}
也许令人惊讶的是，这会打印：
6
当引用在表达式中求值时，它解析为它所引用的对象。所以
ref = y
不会改变
ref
来引用
y
。相反，因为
ref
是
x
的别名，所以表达式的求值就像写成
x = y
一样——由于
y
求值为值
6
，
x
被赋值为
6
。
引用作用域和持续时间
引用变量遵循与普通变量相同的范围和持续时间规则。
#include <iostream>

int main()
{
    int x { 5 }; // normal integer
    int& ref { x }; // reference to variable value

     return 0;
} // x and ref die here
引用和指代物具有独立的生命周期
除一个例外（我们将在下一课中介绍），引用及其指代物的生命周期是独立的。换句话说，以下两点都成立：
引用可以在其所引用的对象之前被销毁。
被引用的对象可以在引用之前被销毁。
当引用在其指代物之前被销毁时，指代物不受影响。以下程序演示了这一点：
#include <iostream>

int main()
{
    int x { 5 };

    {
        int& ref { x };   // ref is a reference to x
        std::cout << ref << '\n'; // prints value of ref (5)
    } // ref is destroyed here -- x is unaware of this

    std::cout << x << '\n'; // prints value of x (5)

    return 0;
} // x destroyed here
上面打印：
5
5
当
ref
死亡时，变量
x
正常运行，完全不知道对它的引用已被销毁。
悬空引用
当被引用的对象在对它的引用之前被销毁时，该引用会引用一个不再存在的对象。这种引用被称为**悬空引用 (dangling reference)**。访问悬空引用会导致未定义行为。
悬空引用很容易避免，但我们将在
12.12 -- 通过引用返回和通过地址返回
这一课中展示一个实际可能发生这种情况的例子。
引用不是对象
也许令人惊讶的是，引用在 C++ 中不是对象。引用不需要存在或占用存储。如果可能，编译器将通过用指代物替换所有引用的出现来优化引用。然而，这并非总是可能的，在这种情况下，引用可能需要存储。
这也意味着“引用变量”这个术语有点用词不当，因为变量是具有名称的对象，而引用不是对象。
因为引用不是对象，所以它们不能用在任何需要对象的地方（例如，你不能有一个指向引用的引用，因为左值引用必须引用一个可识别的对象）。在需要作为对象的引用或可以重新绑定的引用时，
std::reference_wrapper
（我们将在
23.3 -- 聚合
这一课中介绍）提供了一个解决方案。
题外话…
考虑以下变量：
int var{};
int& ref1{ var };  // an lvalue reference bound to var
int& ref2{ ref1 }; // an lvalue reference bound to var
因为
ref2
（一个引用）是用
ref1
（一个引用）初始化的，你可能会倾向于得出结论，
ref2
是对引用的引用。它不是。因为
ref1
是对
var
的引用，当在表达式中（例如初始化器）使用时，
ref1
求值为
var
。所以
ref2
只是一个普通的左值引用（如其类型
int&
所示），绑定到
var
。
对引用（对
int
的引用）的语法将是
int&&
——但由于 C++ 不支持对引用的引用，此语法在 C++11 中被重新用于表示右值引用（我们将在
22.2 -- 右值引用
这一课中介绍）。
作者注
如果引用在这一点上看起来有点无用，请不要担心。引用被大量使用，我们很快就会在
12.5 -- 通过左值引用传递
和
12.6 -- 通过 const 左值引用传递
这一课中介绍主要原因之一。
小测验时间
问题 #1
自己确定以下程序打印的值（不要编译程序）。
#include <iostream>

int main()
{
    int x{ 1 };
    int& ref{ x };

    std::cout << x << ref << '\n';

    int y{ 2 };
    ref = y;
    y = 3;

    std::cout << x << ref << '\n';

    x = 4;

    std::cout << x << ref << '\n';

    return 0;
}
显示答案
11
22
44
因为
ref
绑定到
x
，所以
x
和
ref
是同义的，它们将始终打印相同的值。行
ref = y
将
y
的值 (2) 赋值给
ref
——它不会改变
ref
来引用
y
。随后的行
y = 3
只改变
y
。
下一课
12.4
对 const 的左值引用
返回目录
上一课
12.2
值类别（左值和右值）