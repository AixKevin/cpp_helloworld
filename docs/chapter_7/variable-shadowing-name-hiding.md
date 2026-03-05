# 7.5 — 变量遮蔽（名称隐藏）

7.5 — 变量遮蔽（名称隐藏）
Alex
2020 年 1 月 3 日，上午 11:01 （太平洋标准时间）
2024 年 7 月 18 日
每个块都定义了自己的作用域区域。那么，当我们在一个嵌套块中有一个变量，而这个变量与外部块中的变量同名时会发生什么呢？当这种情况发生时，嵌套变量会在它们都在作用域中的区域“隐藏”外部变量。这被称为
名称隐藏
或
遮蔽
。
局部变量的遮蔽
#include <iostream>

int main()
{ // outer block
    int apples { 5 }; // here's the outer block apples

    { // nested block
        // apples refers to outer block apples here
        std::cout << apples << '\n'; // print value of outer block apples

        int apples{ 0 }; // define apples in the scope of the nested block

        // apples now refers to the nested block apples
        // the outer block apples is temporarily hidden

        apples = 10; // this assigns value 10 to nested block apples, not outer block apples

        std::cout << apples << '\n'; // print value of nested block apples
    } // nested block apples destroyed


    std::cout << apples << '\n'; // prints value of outer block apples

    return 0;
} // outer block apples destroyed
如果你运行这个程序，它会打印
5
10
5
在上面的程序中，我们首先在外部块中声明了一个名为
apples
的变量。这个变量在内部块中是可见的，我们可以通过打印它的值（
5
）来看到这一点。然后我们在嵌套块中声明了一个不同的变量（也名为
apples
）。从这一点到块的末尾，名称
apples
指的是嵌套块的
apples
，而不是外部块的
apples
。
因此，当我们给
apples
赋值
10
时，我们是赋值给嵌套块的
apples
。打印这个值（
10
）后，嵌套块结束，嵌套块的
apples
被销毁。外部块的
apples
的存在和值不受影响，我们通过打印外部块的
apples
的值（
5
）来证明这一点。
请注意，如果嵌套块的
apples
没有被定义，嵌套块中的名称
apples
仍将指代外部块的
apples
，因此将值
10
赋值给
apples
将作用于外部块的
apples
。
#include <iostream>

int main()
{ // outer block
    int apples{5}; // here's the outer block apples

    { // nested block
        // apples refers to outer block apples here
        std::cout << apples << '\n'; // print value of outer block apples

        // no inner block apples defined in this example

        apples = 10; // this applies to outer block apples

        std::cout << apples << '\n'; // print value of outer block apples
    } // outer block apples retains its value even after we leave the nested block

    std::cout << apples << '\n'; // prints value of outer block apples

    return 0;
} // outer block apples destroyed
上面的程序打印
5
10
10
在嵌套块内部时，无法直接访问外部块中被遮蔽的变量。
全局变量的遮蔽
与嵌套块中的变量可以遮蔽外部块中的变量类似，与全局变量同名的局部变量会在局部变量作用域内的任何地方遮蔽全局变量。
#include <iostream>
int value { 5 }; // global variable

void foo()
{
    std::cout << "global variable value: " << value << '\n'; // value is not shadowed here, so this refers to the global value
}

int main()
{
    int value { 7 }; // hides the global variable value (wherever local variable value is in scope)

    ++value; // increments local value, not global value

    std::cout << "local variable value: " << value << '\n';

    foo();

    return 0;
} // local value is destroyed
此代码打印
local variable value: 8
global variable value: 5
然而，由于全局变量是全局命名空间的一部分，我们可以使用没有前缀的作用域运算符 (::) 来告诉编译器我们指的是全局变量而不是局部变量。
#include <iostream>
int value { 5 }; // global variable

int main()
{
    int value { 7 }; // hides the global variable value
    ++value; // increments local value, not global value

    --(::value); // decrements global value, not local value (parenthesis added for readability)

    std::cout << "local variable value: " << value << '\n';
    std::cout << "global variable value: " << ::value << '\n';

    return 0;
} // local value is destroyed
此代码打印
local variable value: 8
global variable value: 4
避免变量遮蔽
通常应避免局部变量的遮蔽，因为它可能导致意外错误，即使用了错误的变量或修改了错误的变量。有些编译器在变量被遮蔽时会发出警告。
出于我们建议避免遮蔽局部变量的相同原因，我们也建议避免遮蔽全局变量。如果所有全局名称都使用“g_”前缀，则这很容易避免。
最佳实践
避免变量遮蔽。
对于 gcc 用户
GCC 和 Clang 支持
-Wshadow
标志，如果变量被遮蔽，它将生成警告。此标志有几个子变体（
-Wshadow=global
、
-Wshadow=local
和
-Wshadow=compatible-local
。请查阅
GCC 文档
以了解其差异。
Visual Studio 默认启用此类警告。
下一课
7.6
内部链接
返回目录
上一课
7.4
全局变量简介