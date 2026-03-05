# 10.x — 第10章总结与测验

10.x — 第10章总结与测验
Alex
2021年6月17日，太平洋夏令时下午5:48
2024年9月3日
能走到这一步，干得漂亮。标准转换规则相当复杂——如果你不理解每一个细微之处，也不必担心。
章节回顾
将一个值从一种数据类型转换为另一种数据类型的过程称为
类型转换
。
当期望一种数据类型，但提供了不同数据类型时，就会执行
隐式类型转换
（也称为
自动类型转换
或
强制类型转换
）。如果编译器能够找出两种类型之间如何进行转换，它就会执行。如果它不知道如何转换，则会因编译错误而失败。
C++语言定义了其基本类型之间的一些内置转换（以及一些更高级类型的转换），这些转换称为
标准转换
。这包括数值提升、数值转换和算术转换。
数值提升
是将某些较小的数值类型转换为某些较大的数值类型（通常是
int
或
double
），以便CPU可以在与处理器自然数据大小匹配的数据上进行操作。数值提升包括整型提升和浮点型提升。数值提升是
值保留的
，这意味着没有值或精度的损失。并非所有拓宽转换都是提升。
数值转换
是基本类型之间的类型转换，而不是数值提升。
窄化转换
是一种数值转换，可能会导致值或精度的损失。
在C++中，某些二元运算符要求其操作数类型相同。如果提供了不同类型的操作数，一个或两个操作数将使用一组称为
常用算术转换
的规则隐式转换为匹配类型。
显式类型转换
是在程序员通过强制转换显式请求转换时执行的。
强制转换
代表程序员要求进行显式类型转换。C++支持5种类型的强制转换：
C风格强制转换
、
静态强制转换
、
const强制转换
、
动态强制转换
和
重新解释强制转换
。通常应避免使用
C风格强制转换
、
const强制转换
和
重新解释强制转换
。
static_cast
用于将一个值从一种类型转换为另一种类型的值，并且是C++中使用最广泛的强制转换。
Typedefs
和
类型别名
允许程序员为数据类型创建别名。这些别名不是新类型，并且与被别名的类型行为完全相同。Typedefs和类型别名不提供任何类型安全，需要注意不要假设别名与其所别名的类型不同。
auto
关键字有多种用途。首先，auto可以用于执行
类型推导
（也称为
类型推断
），它将从变量的初始化器中推导出变量的类型。类型推导会去除const和引用，因此如果需要它们，请务必将其添加回来。
Auto也可以用作函数返回类型，让编译器根据函数的返回语句推断函数的返回类型，尽管对于普通函数应避免这样做。Auto用作
尾随返回语法
的一部分。
小测验时间
问题 #1
在以下每种情况下会发生哪种类型的转换？有效答案是：无需转换、数值提升、数值转换、因窄化转换而无法编译。假设
int
和
long
都是4字节。
int main()
{
    int a { 5 }; // 1a
    int b { 'a' }; // 1b
    int c { 5.4 }; // 1c
    int d { true }; // 1d
    int e { static_cast<int>(5.4) }; // 1e

    double f { 5.0f }; // 1f
    double g { 5 }; // 1g

    // Extra credit section
    long h { 5 }; // 1h

    float i { f }; // 1i (uses previously defined variable f)
    float j { 5.0 }; // 1j

}
1a)
显示答案
无需转换
1b)
显示答案
字符'a'到int的数值提升
1c)
显示答案
因窄化转换而无法编译
1d)
显示答案
布尔值true到int的数值提升
1e)
显示答案
双精度浮点数5.4到int的数值转换
1f)
显示答案
浮点数到双精度浮点数的数值提升
1g)
显示答案
int到double的数值转换
1h)
显示答案
int到long的数值转换（此转换微不足道，但仍是转换）
1i)
显示答案
因双精度浮点数到浮点数的窄化转换而无法编译
1j)
显示答案
双精度浮点数到浮点数的数值转换（这允许，因为5.0是constexpr且在浮点数范围内）
问题 #2
2a) 更新以下程序以对角度和弧度值使用类型别名
#include <iostream>

namespace constants
{
    constexpr double pi { 3.14159 };
}

double convertToRadians(double degrees)
{
    return degrees * constants::pi / 180;
}

int main()
{
    std::cout << "Enter a number of degrees: ";
    double degrees{};
    std::cin >> degrees;

    double radians { convertToRadians(degrees) };
    std::cout << degrees << " degrees is " << radians << " radians.\n";

    return 0;
}
显示答案
#include <iostream>

namespace constants
{
    constexpr double pi{ 3.14159 };
}

using Degrees = double;
using Radians = double;

Radians convertToRadians(Degrees degrees)
{
    return degrees * constants::pi / 180;
}

int main()
{
    std::cout << "Enter a number of degrees: ";
    Degrees degrees{};
    std::cin >> degrees;

    Radians radians{ convertToRadians(degrees) };
    std::cout << degrees << " degrees is " << radians << " radians.\n";

    return 0;
}
2b) 给定上一个测验答案中
degrees
和
radians
的定义，解释以下语句为何会编译或不会编译
radians = degrees;
显示答案
它将编译。
radians
的类型是
Radians
，它是
double
的类型别名。
degrees
的类型是
Degrees
，它也是
double
的类型别名。所以这只是将一个
double
值赋给一个
double
类型的变量。
下一课
11.1
函数重载简介
返回目录
上一课
10.9
函数的类型推导