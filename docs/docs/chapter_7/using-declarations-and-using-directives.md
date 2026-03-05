# 7.13 — 使用声明与使用指令

7.13 — 使用声明与使用指令
Alex
2016年11月9日，太平洋标准时间下午6:23
2025年3月5日
你可能在许多教科书和教程中见过这个程序
#include <iostream>

using namespace std;

int main()
{
    cout << "Hello world!\n";

    return 0;
}
如果你看到这个，赶紧跑。你的教科书或教程可能已经过时了。在本课中，我们将探讨原因。
提示
一些集成开发环境（IDE）也会自动用类似的程序填充新的C++项目（这样你就可以立即编译一些东西，而不是从空白文件开始）。
一段简短的历史课
在C++支持命名空间之前，现在在`std`命名空间中的所有名称都在全局命名空间中。这导致了程序标识符和标准库标识符之间的命名冲突。在C++的一个版本下工作的程序可能会与C++的更新版本产生命名冲突。
1995年，命名空间被标准化，标准库的所有功能都从全局命名空间移到了`std`命名空间中。这一改变破坏了那些仍然使用不带`std::`的名称的旧代码。
任何处理过大型代码库的人都知道，对代码库的任何更改（无论多么微不足道）都可能导致程序崩溃。将所有已移至`std`命名空间的名称更新为使用`std::`前缀是一项巨大的风险。因此需要一个解决方案。
快进到今天——如果你大量使用标准库，每次使用标准库中的东西都输入`std::`会变得重复，在某些情况下，还会使你的代码更难阅读。
C++通过using语句为这两个问题提供了一些解决方案。
但首先，让我们定义两个术语。
限定名与非限定名
一个名称可以是有限定的，也可以是无限定的。
一个**限定名**是包含关联作用域的名称。通常，名称通过作用域解析运算符（::）用命名空间进行限定。例如
std::cout // identifier cout is qualified by namespace std
::foo // identifier foo is qualified by the global namespace
致进阶读者
名称也可以通过作用域解析运算符（::）由类名限定，或者通过成员选择运算符（. 或 ->）由类对象限定。例如
class C; // some class

C::s_member; // s_member is qualified by class C
obj.x; // x is qualified by class object obj
ptr->y; // y is qualified by pointer to class object ptr
**非限定名**是指不包含作用域限定符的名称。例如，`cout`和`x`都是非限定名，因为它们不包含关联的作用域。
使用声明
减少重复输入`std::`的一种方法是使用`using-declaration`语句。**使用声明**允许我们将非限定名（无作用域）用作限定名的别名。
这是我们基本的“Hello world”程序，在第5行使用了using声明
#include <iostream>

int main()
{
   using std::cout; // this using declaration tells the compiler that cout should resolve to std::cout
   cout << "Hello world!\n"; // so no std:: prefix is needed here!

   return 0;
} // the using declaration expires at the end of the current scope
`using std::cout;`这个使用声明告诉编译器，我们将使用`std`命名空间中的对象`cout`。因此，每当它看到`cout`时，它都会假定我们指的是`std::cout`。如果在`std::cout`和从`main()`内部可见的`cout`的其他用途之间存在命名冲突，则`std::cout`将被优先使用。因此在第6行，我们可以输入`cout`而不是`std::cout`。
在这个简单的例子中，这并没有节省多少精力，但是如果你在一个函数中多次使用`cout`，使用声明可以使你的代码更具可读性。请注意，你需要为每个名称提供一个单独的using声明（例如，一个用于`std::cout`，一个用于`std::cin`等）。
使用声明从声明点到其声明所在作用域的末尾都有效。
尽管使用声明不如使用`std::`前缀那么明确，但它们通常被认为在源（.cpp）文件中是安全和可接受的，只有一个例外，我们将在下面讨论。
使用指令
另一种简化方法是使用`using-directive`。**使用指令**允许在`using-directive`所在的作用域中，引用给定命名空间中的**所有**标识符时无需限定符。
致进阶读者
出于技术原因，使用指令实际上并不会将新的名称含义引入当前作用域——相反，它们会将新的名称含义引入外部作用域（有关选择哪个外部作用域的更多详细信息，请参见
此处
）。
这是我们的Hello World程序，第5行带有`using-directive`
#include <iostream>

int main()
{
   using namespace std; // all names from std namespace now accessible without qualification
   cout << "Hello world!\n"; // so no std:: prefix is needed here

   return 0;
} // the using-directive ends at the end of the current scope
`using namespace std;` 这个 using directive 告诉编译器，`std` 命名空间中的所有名称都应该在当前作用域（在本例中是函数 `main()`）中无需限定符即可访问。当我们使用非限定符的标识符 `cout` 时，它将被解析为 `std::cout`。
使用指令是为那些在命名空间出现之前，使用非限定名来表示标准库功能的旧代码库提供的解决方案。这样，无需手动将每个非限定名更新为限定名（这有风险），只需在每个文件的顶部放置一个单独的使用指令（`using namespace std;`），所有已移至`std`命名空间的名称仍然可以非限定地使用。
使用指令的问题（又名：为什么你应该避免“using namespace std;”）
在现代 C++ 中，与风险相比，使用指令通常只有很少的好处（节省一些打字时间）。这主要有两个原因：
使用指令允许对命名空间中的**所有**名称进行非限定访问（可能包括许多你永远不会使用的名称）。
使用指令不优先使用由使用指令标识的命名空间中的名称，而不是其他名称。
最终结果是，命名冲突的可能性大大增加（特别是如果你导入了`std`命名空间）。
首先，让我们看一个使用指令导致命名冲突的说明性例子
#include <iostream>

namespace A
{
	int x { 10 };
}

namespace B
{
	int x{ 20 };
}

int main()
{
	using namespace A;
	using namespace B;

	std::cout << x << '\n';

	return 0;
}
在上面的例子中，编译器无法确定`main`中的`x`是指`A::x`还是`B::x`。在这种情况下，它将因为“ambiguous symbol”（模糊符号）错误而无法编译。我们可以通过移除其中一个使用指令，改用使用声明，或者限定`x`（如`A::x`或`B::x`）来解决这个问题。
这是另一个更微妙的例子
#include <iostream> // imports the declaration of std::cout

int cout() // declares our own "cout" function
{
    return 5;
}

int main()
{
    using namespace std; // makes std::cout accessible as "cout"
    cout << "Hello, world!\n"; // uh oh!  Which cout do we want here?  The one in the std namespace or the one we defined above?

    return 0;
}
在这个例子中，编译器无法确定我们非限定地使用`cout`是指`std::cout`还是我们定义的`cout`函数，并且会再次因为“ambiguous symbol”（模糊符号）错误而编译失败。尽管这个例子很简单，但如果我们像这样明确地加上`std::cout`的前缀：
std::cout << "Hello, world!\n"; // tell the compiler we mean std::cout
或者使用使用声明代替使用指令
using std::cout; // tell the compiler that cout means std::cout
    cout << "Hello, world!\n"; // so this means std::cout
那么我们的程序一开始就不会有任何问题。虽然你可能不太可能编写一个名为“cout”的函数，但`std`命名空间中还有数百个其他名称，正等着与你的名称发生冲突。
即使使用指令今天不会导致命名冲突，它也会使你的代码更容易受到未来冲突的影响。例如，如果你的代码包含某个库的使用指令，而该库随后被更新，那么更新后的库中引入的所有新名称现在都可能与你现有代码中的名称发生命名冲突。
例如，以下程序编译并运行良好
FooLib.h（某个第三方库的一部分）
#ifndef FOOLIB
#define FOOLIB

namespace Foo
{
    int a { 20 };
}

#endif
main.cpp
#include <iostream>
#include <FooLib.h> // a third-party library we installed outside our project directory, thus angled brackets used

void print()
{
    std::cout << "Hello\n";
}

int main()
{
    using namespace Foo; // Because we're lazy and want to access Foo:: qualified names without typing the Foo:: prefix

    std::cout << a << '\n'; // uses Foo::a
    print(); // calls ::print()

    return 0;
}
现在假设你将 FooLib 更新到新版本，并且 FooLib.h 变为这样：
FooLib.h（更新后）
#ifndef FOOLIB
#define FOOLIB

namespace Foo
{
    int a { 20 };
    void print() { std::cout << "Timmah!"; } // This function added
}
#endif
你的 main.cpp 没有改变，但它将不再编译！这是因为我们的使用指令导致`Foo::print()`可以仅仅作为`print()`访问，现在调用`print()`究竟是指`::print()`还是`Foo::print()`变得模糊不清。
这个问题还会出现一个更隐蔽的版本。更新后的库可能会引入一个函数，该函数不仅名称相同，而且实际上更匹配某个函数调用。在这种情况下，编译器可能会决定优先使用新函数，导致你的程序行为发生意外且悄无声息的改变。
考虑以下程序
Foolib.h（某个第三方库的一部分）
#ifndef FOOLIB_H
#define FOOLIB_H

namespace Foo
{
    int a { 20 };
}
#endif
main.cpp
#include <iostream>
#include <Foolib.h> // a third-party library we installed outside our project directory, thus angled brackets used

int get(long)
{
    return 1;
}

int main()
{
    using namespace Foo; // Because we're lazy and want to access Foo:: qualified names without typing the Foo:: prefix
    std::cout << a << '\n'; // uses Foo::a

    std::cout << get(0) << '\n'; // calls ::get(long)

    return 0;
}
此程序运行并打印 `1`。
现在，假设我们更新了Foolib库，其中包含一个更新后的Foolib.h，它看起来像这样：
Foolib.h（更新后）
#ifndef FOOLIB_H
#define FOOLIB_H

namespace Foo
{
    int a { 20 };

    int get(int) { return 2; } // new function added
}
#endif
我们的`main.cpp`文件再次完全没有改变，但是这个程序现在编译、运行并打印`2`！
当编译器遇到函数调用时，它必须确定应该将该函数调用与哪个函数定义匹配。在从一组潜在匹配函数中选择一个函数时，它会优先选择不需要参数转换的函数，而不是需要参数转换的函数。因为字面值`0`是一个整数，C++会优先将`print(0)`与新引入的`print(int)`匹配（无需转换），而不是`print(long)`（这需要从`int`到`long`的转换）。这导致了我们程序行为的意外改变。
在这种情况下，行为变化相当明显。但在更复杂的程序中，如果返回值不仅仅是打印出来，这个问题可能非常难以发现。
如果我们使用了使用声明或显式作用域限定符，这种情况就不会发生。
最后，缺少显式的范围前缀使得读者更难判断哪些函数是库的一部分，哪些是你的程序的一部分。例如，如果我们使用一个`using-directive`
using namespace NS;

int main()
{
    foo(); // is this foo a user-defined function, or part of the NS library?
}
不清楚对`foo()`的调用是实际调用`NS::foo()`还是用户定义的`foo()`函数。现代IDE应该能够在您将鼠标悬停在名称上时为您消除歧义，但是每次都必须将鼠标悬停在每个名称上才能查看其来源是乏味的。
没有`using-directive`，会清晰得多
int main()
{
    NS::foo(); // clearly part of the NS library
    foo(); // likely a user-defined function
}
在这个版本中，对`NS::foo()`的调用显然是库调用。对普通`foo()`的调用很可能是一个用户定义的函数调用（一些库，包括某些标准库头文件，确实将名称放入全局命名空间，所以这不是一个保证）。
`using`语句的作用域
如果在块内使用using声明或using指令，则这些名称仅适用于该块（它遵循正常的块作用域规则）。这是一件好事，因为它减少了命名冲突仅在该块内发生的可能性。
如果在命名空间（包括全局命名空间）中使用`using-declaration`或`using-directive`，则这些名称适用于文件的其余部分（它们具有文件作用域）。
不要在头文件或`#include`指令之前使用`using`语句
一个好的经验法则是，`using`语句不应该放在任何可能影响其他文件中代码的地方。也不应该放在其他文件的代码可能影响它们的地方。
更具体地说，这意味着不应在头文件或`#include`指令之前使用`using`语句。
例如，如果你在头文件的全局命名空间中放置了一个`using`语句，那么所有`#include`该头文件的其他文件也会获得该`using`语句。这显然不好。出于同样的原因，这也适用于头文件内部的命名空间。
但是，在头文件中定义的函数中使用using语句又如何呢？既然using语句的作用域局限于函数内部，那肯定没问题吧？即使这样也不行。原因与我们不应该在`#include`指令之前使用using语句的原因相同。
事实证明，`using`语句的行为取决于已经引入的标识符。这使得它们具有顺序依赖性，因为如果在使用它们之前引入的标识符发生变化，它们的功能可能会改变。
我们将通过一个例子来说明这一点
FooInt.h
namespace Foo
{
    void print(int)
    {
        std::cout << "print(int)\n" << std::endl;
    }
}
FooDouble.h
namespace Foo
{
    void print(double)
    {
        std::cout << "print(double)\n" << std::endl;
    }
}
main.cpp（正常）
#include <iostream>

#include "FooDouble.h"
#include "FooInt.h"

using Foo::print; // print means Foo::print

int main()
{
    print(5);  // Calls Foo::print(int)
}
运行时，这个程序调用`Foo::print(int)`，它打印`print(int)`。
现在让我们稍微修改一下main.cpp。
main.cpp（错误）
#include <iostream>

#include "FooDouble.h"

using Foo::print; // we moved the using-statement here, before the #include directive
#include "FooInt.h"

int main()
{
    print(5);  // Calls Foo::print(double)
}
我们所做的只是将`using Foo::print;`移到了`#include "FooInt.h"`之前。现在我们的程序打印`print(double)`！不管这是为什么发生的，你大概会同意，这是我们想要避免的行为！
所以，回到前面，我们不应该在头文件中定义的函数中使用`using`语句的原因是相同的——我们无法控制在我们的头文件之前可能`#include`了哪些其他头文件，而且这些头文件可能会做一些事情，从而改变我们的`using`语句的行为！
唯一真正安全地使用`using`语句的地方是在我们的源（.cpp）文件中，在所有`#includes`之后。
致进阶读者
这个例子使用了一个我们尚未介绍的概念，称为“函数重载”（我们将在第
11.1 — 函数重载简介
课中介绍）。对于这个例子，你只需要知道，在同一作用域内的两个函数可以拥有相同的名称，只要它们的参数是不同的。由于`int`和`double`是不同的类型，因此`Foo::print(int)`和`Foo::print(double)`可以并存，没有任何问题。
在正常版本中，当编译器遇到`using Foo::print`时，它已经看到了`Foo::print(int)`和`Foo::print(double)`，因此它使两者都可以作为`print()`被调用。由于`Foo::print(int)`比`Foo::print(double)`更匹配，所以它调用了`Foo::print(int)`。
在错误版本中，当编译器遇到`using Foo::print`时，它只看到了`Foo::print(double)`的声明，因此它只允许`Foo::print(double)`被非限定地调用。所以当我们调用`print(5)`时，只有`Foo::print(double)`有资格被匹配。因此，被调用的是`Foo::print(double)`！
取消或替换`using`语句
一旦声明了一个`using`语句，就没有办法在其声明的作用域内取消或用不同的`using`语句替换它。
int main()
{
    using namespace Foo;

    // there's no way to cancel the "using namespace Foo" here!
    // there's also no way to replace "using namespace Foo" with a different using statement

    return 0;
} // using namespace Foo ends here
最好的办法是，从一开始就使用块作用域规则来有意限制`using`语句的作用域。
int main()
{
    {
        using namespace Foo;
        // calls to Foo:: stuff here
    } // using namespace Foo expires
 
    {
        using namespace Goo;
        // calls to Goo:: stuff here
    } // using namespace Goo expires

    return 0;
}
当然，所有这些麻烦都可以通过一开始就显式使用作用域解析运算符（::）来避免。
`using`语句的最佳实践
最佳实践
优先使用显式命名空间限定符而不是`using`语句。
完全避免使用`using-directives`（除了`using namespace std::literals`来访问`s`和`sv`字面量后缀）。`using-declarations`可以在`.cpp`文件中，在`#include`指令之后使用。不要在头文件中使用`using`语句（尤其不要在头文件的全局命名空间中）。
相关内容
`using`关键字也用于定义类型别名，这与`using`语句无关。我们在
10.7 — Typedefs and type aliases
一课中介绍类型别名。
下一课
7.14
匿名命名空间与内联命名空间
返回目录
上一课
7.12
作用域、生命周期与链接总结