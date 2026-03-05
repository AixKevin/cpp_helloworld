# 11.10 — 在多个文件中使用函数模板

11.10 — 在多个文件中使用函数模板
Alex
2024年6月11日，太平洋夏令时上午11:06
2024年10月20日
考虑以下程序，它无法正常工作
main.cpp
#include <iostream>

template <typename T>
T addOne(T x); // function template forward declaration

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';

    return 0;
}
add.cpp
template <typename T>
T addOne(T x) // function template definition
{
    return x + 1;
}
如果
addOne
是一个非模板函数，这个程序会正常工作：在
main.cpp
中，编译器会接受
addOne
的前向声明，并且链接器会将
main.cpp
中对
addOne()
的调用连接到
add.cpp
中的函数定义。
但由于
addOne
是一个模板，这个程序无法工作，我们得到一个链接器错误
1>Project6.obj : error LNK2019: unresolved external symbol "int __cdecl addOne<int>(int)" (??$addOne@H@@YAHH@Z) referenced in function _main
1>Project6.obj : error LNK2019: unresolved external symbol "double __cdecl addOne<double>(double)" (??$addOne@N@@YANN@Z) referenced in function _main
在
main.cpp
中，我们调用
addOne<int>
和
addOne<double>
。然而，由于编译器看不到函数模板
addOne
的定义，它无法在
main.cpp
内部实例化这些函数。它确实看到了
addOne
的前向声明，并会假设这些函数存在于其他地方，并且稍后会被链接。
当编译器编译
add.cpp
时，它会看到函数模板
addOne
的定义。然而，在
add.cpp
中没有使用这个模板，所以编译器不会实例化任何东西。最终结果是链接器无法将
main.cpp
中对
addOne<int>
和
addOne<double>
的调用连接到实际函数，因为这些函数从未被实例化。
题外话…
如果
add.cpp
实例化了这些函数，程序就能正常编译和链接。但这种解决方案是脆弱的，应该避免：如果
add.cpp
中的代码后来改变，使得这些函数不再被实例化，程序将再次无法链接。或者如果
main.cpp
调用了
addOne
的不同版本（例如
addOne<float>
）而该版本没有在
add.cpp
中实例化，我们也会遇到同样的问题。
解决此问题的最常规方法是将所有模板代码放在头文件 (.h) 中，而不是源文件 (.cpp) 中
add.h
#ifndef ADD_H
#define ADD_H

template <typename T>
T addOne(T x) // function template definition
{
    return x + 1;
}

#endif
main.cpp
#include "add.h" // import the function template definition
#include <iostream>

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';

    return 0;
}
这样，任何需要访问模板的文件都可以 #include 相关的头文件，模板定义将由预处理器复制到源文件中。然后编译器就能实例化任何需要的函数。
你可能想知道这为什么不会导致违反单一定义规则 (ODR)。ODR 规定类型、模板、内联函数和内联变量允许在不同的文件中具有相同的定义。因此，如果模板定义被复制到多个文件中（只要每个定义都相同），就没有问题。
相关内容
我们在
2.7 -- 前向声明和定义
课程中介绍了 ODR。
但那些被实例化的函数本身呢？如果一个函数在多个文件中被实例化，这怎么不会导致违反 ODR 呢？答案是，从模板隐式实例化的函数是隐式内联的。正如你所知，内联函数可以在多个文件中定义，只要每个定义都相同。
关键见解
模板定义不受单一定义规则中“每个程序只能有一个定义”部分的要求，因此将相同的模板定义 #include 到多个源文件中没有问题。而且从函数模板隐式实例化的函数是隐式内联的，所以它们可以在多个文件中定义，只要每个定义都相同。
模板本身不是内联的，因为内联的概念只适用于变量和函数。
这是另一个将函数模板放在头文件中，以便可以将其包含到多个源文件中的示例
max.h
#ifndef MAX_H
#define MAX_H

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

#endif
foo.cpp
#include "max.h" // import template definition for max<T>(T, T)
#include <iostream>

void foo()
{
	std::cout << max(3, 2) << '\n';
}
main.cpp
#include "max.h" // import template definition for max<T>(T, T)
#include <iostream>

void foo(); // forward declaration for function foo

int main()
{
    std::cout << max(3, 5) << '\n';
    foo();

    return 0;
}
在上面的示例中，main.cpp 和 foo.cpp 都
#include "max.h"
，因此两个文件中的代码都可以使用
max<T>(T, T)
函数模板。
最佳实践
需要在多个文件中使用的模板应该在头文件中定义，然后在使用它们的地方 #include。这允许编译器看到完整的模板定义并在需要时实例化模板。
下一课
11.x
第11章总结与测验
返回目录
上一课
11.9
非类型模板参数