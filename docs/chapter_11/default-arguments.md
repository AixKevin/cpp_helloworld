# 11.5 — 默认参数

11.5 — 默认参数
Alex
2007 年 8 月 6 日，下午 4:38 PDT
2024 年 11 月 10 日
默认参数
是为函数参数提供的一个默认值。例如
void print(int x, int y=10) // 10 is the default argument
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
进行函数调用时，调用者可以选择性地为任何具有默认参数的函数参数提供一个实参。如果调用者提供了实参，则使用函数调用中实参的值。如果调用者未提供实参，则使用默认参数的值。
考虑以下程序
#include <iostream>

void print(int x, int y=4) // 4 is the default argument
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}

int main()
{
    print(1, 2); // y will use user-supplied argument 2
    print(3); // y will use default argument 4, as if we had called print(3, 4)

    return 0;
}
此程序生成以下输出：
x: 1
y: 2
x: 3
y: 4
在第一次函数调用中，调用者为两个参数都提供了显式实参，因此使用了这些实参值。在第二次函数调用中，调用者省略了第二个实参，因此使用了默认值
4
。
请注意，您必须使用等号来指定默认参数。使用括号或花括号初始化将不起作用
void foo(int x = 5);   // ok
void goo(int x ( 5 )); // compile error
void boo(int x { 5 }); // compile error
也许令人惊讶的是，默认参数是由编译器在调用点处理的。在上面的例子中，当编译器看到
print(3)
时，它会重写这个函数调用为
print(3, 4)
，以便参数的数量与参数的数量匹配。然后，重写的函数调用正常工作。
关键见解
默认参数由编译器在函数调用点插入。
默认参数在 C++ 中经常使用，您会在遇到的代码（以及未来的课程）中大量看到它们。
何时使用默认参数
当函数需要一个具有合理默认值的值，但您希望调用者能够根据需要覆盖它时，默认参数是一个绝佳的选择。
例如，这里有几个函数原型，默认参数可能常用于其中
int rollDie(int sides=6);
void openLogFile(std::string filename="default.log");
作者注
由于用户可以选择提供特定的实参值或使用默认值，因此提供默认值的参数有时被称为
可选参数
。然而，
可选参数
这个术语也用于指代其他几种类型的参数（包括通过地址传递的参数和使用
std::optional
的参数），因此我们建议避免使用此术语。
默认参数在我们需要向现有函数添加新参数的情况下也很有用。如果我们添加一个没有默认参数的新参数，它将破坏所有现有的函数调用（这些调用没有为该参数提供实参）。这可能会导致大量更新现有函数调用（如果您不拥有调用代码，甚至可能无法实现）。但是，如果我们添加一个带有默认参数的新参数，所有现有函数调用仍将起作用（因为它们将使用该参数的默认参数），同时仍然允许新函数调用在需要时指定显式实参。
多个默认参数
一个函数可以有多个带有默认参数的参数
#include <iostream>

void print(int x=10, int y=20, int z=30)
{
    std::cout << "Values: " << x << " " << y << " " << z << '\n';
}

int main()
{
    print(1, 2, 3); // all explicit arguments
    print(1, 2); // rightmost argument defaulted
    print(1); // two rightmost arguments defaulted
    print(); // all arguments defaulted

    return 0;
}
产生以下输出
Values: 1 2 3
Values: 1 2 30
Values: 1 20 30
Values: 10 20 30
C++（截至 C++23）不支持
print(,,3)
这样的函数调用语法（作为提供
z
的显式值而使用
x
和
y
的默认参数的方式）。这有三个主要后果
在函数调用中，任何显式提供的实参都必须是最左边的实参（带有默认值的实参不能跳过）。
例如
void print(std::string_view sv="Hello", double d=10.0);

int main()
{
    print();           // okay: both arguments defaulted
    print("Macaroni"); // okay: d defaults to 10.0
    print(20.0);       // error: does not match above function (cannot skip argument for sv)

    return 0;
}
如果一个参数被赋予了默认参数，则所有后续参数（右侧）也必须被赋予默认参数。
以下是不允许的
void print(int x=10, int y); // not allowed
规则
如果一个参数被赋予了默认参数，则所有后续参数（右侧）也必须被赋予默认参数。
如果多个参数具有默认参数，则最左边的参数应该最有可能由用户显式设置。
默认参数不能重新声明，并且必须在使用前声明
一旦声明，默认参数不能在同一翻译单元中重新声明。这意味着对于具有前向声明和函数定义的函数，默认参数可以在前向声明或函数定义中声明，但不能同时在两者中声明。
#include <iostream>

void print(int x, int y=4); // forward declaration

void print(int x, int y=4) // compile error: redefinition of default argument
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
默认参数也必须在使用前在翻译单元中声明
#include <iostream>

void print(int x, int y); // forward declaration, no default argument

int main()
{
    print(3); // compile error: default argument for y hasn't been defined yet

    return 0;    
}

void print(int x, int y=4)
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
最佳实践是在前向声明中而不是在函数定义中声明默认参数，因为前向声明更有可能被其他文件看到并在使用前包含（尤其是在头文件中）。
在 foo.h 中
#ifndef FOO_H
#define FOO_H
void print(int x, int y=4);
#endif
在 main.cpp 中
#include "foo.h"
#include <iostream>

void print(int x, int y)
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}

int main()
{
    print(5);

    return 0;
}
请注意，在上面的示例中，我们能够使用函数
print()
的默认参数，因为
main.cpp
#includes
foo.h
，其中包含定义默认参数的前向声明。
最佳实践
如果函数有前向声明（尤其是头文件中的前向声明），请将默认参数放在那里。否则，将默认参数放在函数定义中。
默认参数和函数重载
带有默认参数的函数可以被重载。例如，以下是允许的
#include <iostream>
#include <string_view>

void print(std::string_view s)
{
    std::cout << s << '\n';
}

void print(char c = ' ')
{
    std::cout << c << '\n';
}

int main()
{
    print("Hello, world"); // resolves to print(std::string_view)
    print('a');            // resolves to print(char)
    print();               // resolves to print(char)

    return 0;
}
对
print()
的函数调用实际上调用了
print(char)
，其行为就好像用户已显式调用
print(' ')
一样。
现在考虑这种情况
void print(int x);                  // signature print(int)
void print(int x, int y = 10);      // signature print(int, int)
void print(int x, double y = 20.5); // signature print(int, double)
默认值不是函数签名的一部分，因此这些函数声明是不同的重载。
相关内容
我们在课程
11.2 -- 函数重载区分
中讨论函数重载区分。
默认参数可能导致模糊匹配
默认参数很容易导致模糊的函数调用
void foo(int x = 0)
{
}

void foo(double d = 0.0)
{
}

int main()
{
    foo(); // ambiguous function call

    return 0;
}
在此示例中，编译器无法判断
foo()
应该解析为
foo(0)
还是
foo(0.0)
。
这是一个稍微复杂的示例
void print(int x);                  // signature print(int)
void print(int x, int y = 10);      // signature print(int, int)
void print(int x, double y = 20.5); // signature print(int, double) 

int main()
{
    print(1, 2);   // will resolve to print(int, int)
    print(1, 2.5); // will resolve to print(int, double) 
    print(1);      // ambiguous function call

    return 0;
}
对于调用
print(1)
，编译器无法判断它应该解析为
print(int)
、
print(int, int)
还是
print(int, double)
。
如果我们打算调用
print(int, int)
或
print(int, double)
，我们总是可以显式指定第二个参数。但是如果我们想调用
print(int)
呢？如何做到这一点并不明显。
通过函数指针调用的函数不支持默认参数
高级
我们在课程
20.1 -- 函数指针
中讨论此主题。由于使用此方法不考虑默认参数，这也提供了一种解决方法，可以调用原本会因默认参数而模糊的函数。
下一课
11.6
函数模板
返回目录
上一课
11.4
删除函数