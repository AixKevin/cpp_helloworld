# 7.3 — 局部变量

7.3 — 局部变量
Alex
2015年3月23日，太平洋时间上午11:32
2024年6月9日
在第
2.5 — 局部作用域简介
课中，我们介绍了
局部变量
，它们是函数内部定义的变量（包括函数参数）。
事实证明，C++ 实际上没有一个单一的属性来定义一个变量是局部变量。相反，局部变量有几个不同的属性，这些属性将它们的行为与其它类型的（非局部）变量区分开来。我们将在本课和接下来的课程中探讨这些属性。
在第
2.5 — 局部作用域简介
课中，我们还介绍了作用域的概念。标识符的
作用域
决定了标识符在源代码中可以在何处被访问。当标识符可以被访问时，我们说它处于
作用域内
。当标识符不能被访问时，我们说它处于
作用域外
。作用域是一个编译时属性，尝试在标识符超出作用域时使用它将导致编译错误。
局部变量具有块作用域
局部变量具有
块作用域
，这意味着它们从定义点到定义它们所在块的末尾都处于
作用域内
。
相关内容
如果您需要复习块，请查看第
7.1 — 复合语句（块）
课。
int main()
{
    int i { 5 }; // i enters scope here
    double d { 4.0 }; // d enters scope here

    return 0;
} // d and i go out of scope here
尽管函数参数不是在函数体内部定义的，但对于典型的函数，它们可以被认为是函数体块作用域的一部分。
int max(int x, int y) // x and y enter scope here
{
    // assign the greater of x or y to max
    int max{ (x > y) ? x : y }; // max enters scope here

    return max;
} // max, y, and x leave scope here
一个作用域内的所有变量名必须是唯一的
变量名在一个给定的作用域内必须是唯一的，否则对该名称的任何引用都将是模糊的。考虑以下程序
void someFunction(int x)
{
    int x{}; // compilation failure due to name collision with function parameter
}

int main()
{
    return 0;
}
上述程序无法编译，因为在函数体内部定义的变量
x
和函数参数
x
具有相同的名称，并且都处于相同的块作用域中。
局部变量具有自动存储期
变量的
存储期
（通常简称为
期
）决定了何时以及如何创建（实例化）和销毁变量的规则。在大多数情况下，变量的存储期直接决定了它的
生命周期
。
相关内容
我们在第
2.5 — 局部作用域简介
课中讨论了什么是生命周期。
例如，局部变量具有
自动存储期
，这意味着它们在定义点创建，并在定义它们所在块的末尾销毁。例如
int main()
{
    int i { 5 }; // i created and initialized here
    double d { 4.0 }; // d created and initialized here

    return 0;
} // d and i are destroyed here
因此，局部变量有时被称为
自动变量
。
嵌套块中的局部变量
局部变量可以在嵌套块内定义。这与函数体块中的局部变量工作方式相同
int main() // outer block
{
    int x { 5 }; // x enters scope and is created here

    { // nested block
        int y { 7 }; // y enters scope and is created here
    } // y goes out of scope and is destroyed here

    // y can not be used here because it is out of scope in this block

    return 0;
} // x goes out of scope and is destroyed here
在上面的示例中，变量
y
定义在一个嵌套块内。它的作用域从定义点到嵌套块的末尾，其生命周期也相同。由于变量
y
的作用域仅限于它所在的内部块，因此在外部块中的任何地方都无法访问它。
请注意，嵌套块被认为是定义它们所在外部块作用域的一部分。因此，在外部块中定义的变量
可以
在嵌套块中看到
#include <iostream>

int main()
{ // outer block

    int x { 5 }; // x enters scope and is created here

    { // nested block
        int y { 7 }; // y enters scope and is created here

        // x and y are both in scope here
        std::cout << x << " + " << y << " = " << x + y << '\n';
    } // y goes out of scope and is destroyed here

    // y can not be used here because it is out of scope in this block

    return 0;
} // x goes out of scope and is destroyed here
局部变量没有链接
标识符还有一个名为
链接
的属性。标识符的
链接
决定了同一标识符在不同作用域中的声明是否指向同一个对象（或函数）。
局部变量没有链接。没有链接的标识符的每个声明都指向一个唯一的对象或函数。
例如
int main()
{
    int x { 2 }; // local variable, no linkage

    {
        int x { 3 }; // this declaration of x refers to a different object than the previous x
    }

    return 0;
}
作用域和链接可能看起来有些相似。但是，作用域决定了单个标识符的声明在代码中何处可见和使用。链接决定了同一标识符的多个声明是否指向同一个对象。
相关内容
我们在第
7.5 — 变量遮蔽（名称隐藏）
课中讨论了当嵌套块中出现同名变量时会发生什么。
链接在局部变量的上下文中不是很重要，但我们将在接下来的几课中更多地讨论它。
变量应在最受限的作用域内定义
如果一个变量只在嵌套块内使用，它应该在该嵌套块内定义
#include <iostream>

int main()
{
    // do not define y here

    {
        // y is only used inside this block, so define it here
        int y { 5 };
        std::cout << y << '\n';
    }

    // otherwise y could still be used here, where it's not needed

    return 0;
}
通过限制变量的作用域，您可以减少程序的复杂性，因为活动变量的数量减少了。此外，它使您更容易看到变量的使用位置（或未使用位置）。在块内定义的变量只能在该块（或嵌套块）内使用。这可以使程序更容易理解。
如果外部块需要一个变量，它需要在外部块中声明
#include <iostream>

int main()
{
    int y { 5 }; // we're declaring y here because we need it in this outer block later

    {
        int x{};
        std::cin >> x;

        // if we declared y here, immediately before its actual first use...
        if (x == 4)
            y = 4;
    } // ... it would be destroyed here

    std::cout << y; // and we need y to exist here

    return 0;
}
上面的例子展示了您可能需要在首次使用变量之前很早声明变量的罕见情况之一。
新开发人员有时会想，是否值得创建一个嵌套块只是为了有意限制变量的作用域（并强制它超出作用域/提前销毁）。这样做会使该变量更简单，但整体函数因此变得更长、更复杂。这种权衡通常不值得。如果创建嵌套块似乎有助于有意限制一段代码的作用域，那么最好将该代码放在一个单独的函数中。
最佳实践
在最受限的现有作用域中定义变量。避免创建唯一目的是限制变量作用域的新块。
小测验时间
问题 #1
编写一个程序，要求用户输入两个整数，一个名为
smaller
，另一个名为
larger
。如果用户为第二个整数输入了较小的值，则使用块和临时变量交换
smaller
和
larger
的值。然后打印
smaller
和
larger
变量的值。在您的代码中添加注释，指示每个变量的生命周期结束位置。注意：当您打印值时，无论它们以何种顺序输入，
smaller
都应包含较小的输入，
larger
都应包含较大的输入。
程序输出应与以下内容匹配
Enter an integer: 4
Enter a larger integer: 2
Swapping the values
The smaller value is 2
The larger value is 4
显示答案
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int smaller{};
    std::cin >> smaller;

    std::cout << "Enter a larger integer: ";
    int larger{};
    std::cin >> larger;

    // if user did it wrong
    if (smaller > larger)
    {
        // swap values of smaller and larger
        std::cout << "Swapping the values\n";

        int temp{ larger };
        larger = smaller;
        smaller = temp;
    } // temp dies here

    std::cout << "The smaller value is: " << smaller << '\n';
    std::cout << "The larger value is: " << larger << '\n';

    return 0;
} // smaller and larger die here
将来，您可以使用
头文件中的
std::swap()
来交换两个变量的值。例如
int temp{ larger };
larger = smaller;
smaller = temp;

// is the same as
std::swap(larger, smaller);
问题 #2
变量的作用域、期和生命周期有什么区别？默认情况下，局部变量有什么样的作用域和期（以及它们意味着什么）？
显示答案
变量的作用域决定了变量在源代码中的可访问位置。期定义了何时创建和销毁变量的规则。变量的生命周期是其创建和销毁之间的实际时间。
局部变量具有块作用域，这意味着它们可以从定义点到定义它们所在块的末尾进行访问。
局部变量具有自动期，这意味着它们在定义点创建，并在定义它们所在块的末尾销毁。
下一课
7.4
全局变量简介
返回目录
上一课
7.2
用户自定义命名空间和作用域解析运算符