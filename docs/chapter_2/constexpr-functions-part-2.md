# F.2 — Constexpr 函数（第 2 部分）

F.2 — Constexpr 函数（第 2 部分）
Alex
2024 年 11 月 26 日，太平洋标准时间下午 4:16
2024 年 12 月 10 日
在非必需常量表达式中的 Constexpr 函数调用
你可能认为 constexpr 函数会在可能的情况下在编译时求值，但遗憾的是情况并非如此。
在第
5.5 课 —— 常量表达式
中，我们注意到在不“要求”常量表达式的上下文中，编译器可以选择在编译时或运行时求值一个常量表达式。因此，作为非必需常量表达式一部分的任何 constexpr 函数调用都可以在编译时或运行时求值。
例如
#include <iostream>

constexpr int getValue(int x)
{
    return x;
}

int main()
{
    int x { getValue(5) }; // may evaluate at runtime or compile-time
    
    return 0;
}
在上面的例子中，因为
getValue()
是 constexpr，所以调用
getValue(5)
是一个常量表达式。然而，因为变量
x
不是 constexpr，它不要求常量表达式初始化器。所以即使我们提供了一个常量表达式初始化器，编译器仍然可以自由选择
getValue(5)
是在运行时还是编译时求值。
关键见解
只有在需要常量表达式时，才能保证 constexpr 函数在编译时求值。
在必需常量表达式中对 constexpr 函数的诊断
编译器“不”需要在实际编译时求值之前确定 constexpr 函数是否可以在编译时求值。编写一个在运行时使用时编译成功，但在编译时求值时编译失败的 constexpr 函数是相当容易的。
一个简单的例子如下：
#include <iostream>

int getValue(int x)
{
    return x;
}

// This function can be evaluated at runtime
// When evaluated at compile-time, the function will produce a compilation error
// because the call to getValue(x) cannot be resolved at compile-time
constexpr int foo(int x)
{
    if (x < 0) return 0; // needed prior to adoption of P2448R1 in C++23 (see note below)
    return getValue(x);  // call to non-constexpr function here
}

int main()
{
    int x { foo(5) };           // okay: will evaluate at runtime
    constexpr int y { foo(5) }; // compile error: foo(5) can't evaluate at compile-time

    return 0;
}
在上面的示例中，当
foo(5)
用作非 constexpr 变量
x
的初始化器时，它将在运行时求值。这工作正常，并返回
5
。
然而，当
foo(5)
用作 constexpr 变量
y
的初始化器时，它必须在编译时求值。此时，编译器将确定对
foo(5)
的调用无法在编译时求值，因为
getValue()
不是 constexpr 函数。
因此，在编写 constexpr 函数时，始终明确测试它在编译时求值时是否编译成功（通过在需要常量表达式的上下文中调用它，例如在 constexpr 变量的初始化中）。
最佳实践
所有 constexpr 函数都应该在编译时求值，因为在需要常量表达式的上下文中将要求它们这样做。
始终在需要常量表达式的上下文中测试你的 constexpr 函数，因为 constexpr 函数在运行时求值时可能有效，但在编译时求值时失败。
致进阶读者
在 C++23 之前，如果不存在允许 constexpr 函数在编译时求值的参数值，则程序格式不正确（无需诊断）。如果没有
if (x < 0) return 0
这一行，上面的例子将不包含任何允许函数在编译时求值的参数集，从而使程序格式不正确。考虑到不需要诊断，编译器可能不会强制执行此要求。
此要求已在 C++23 中撤销（
P2448R1
）。
Constexpr/consteval 函数参数不是 constexpr
constexpr 函数的参数不是隐式 constexpr，也不能声明为
constexpr
。
关键见解
constexpr 函数参数将意味着该函数只能使用 constexpr 参数调用。但事实并非如此——当函数在运行时求值时，constexpr 函数可以与非 constexpr 参数一起调用。
由于这些参数不是 constexpr，因此它们不能在函数内的常量表达式中使用。
consteval int goo(int c)    // c is not constexpr, and cannot be used in constant expressions
{
    return c;
}

constexpr int foo(int b)    // b is not constexpr, and cannot be used in constant expressions
{
    constexpr int b2 { b }; // compile error: constexpr variable requires constant expression initializer

    return goo(b);          // compile error: consteval function call requires constant expression argument
}

int main()
{
    constexpr int a { 5 };

    std::cout << foo(a); // okay: constant expression a can be used as argument to constexpr function foo()
    
    return 0;
}
在上面的示例中，函数参数
b
不是 constexpr（即使参数
a
是常量表达式）。这意味着
b
不能在需要常量表达式的任何地方使用，例如 constexpr 变量的初始化器（例如
b2
）或调用 consteval 函数（
goo(b)
）。
constexpr 函数的参数可以声明为
const
，在这种情况下它们被视为运行时常量。
相关内容
如果您需要常量表达式参数，请参阅
11.9 -- 非类型模板参数
。
Constexpr 函数是隐式 inline
当 constexpr 函数在编译时求值时，编译器必须能够在这些函数调用之前看到 constexpr 函数的完整定义（以便它自己执行求值）。在这种情况下，即使实际的函数定义稍后出现在同一个编译单元中，前向声明也不够。
这意味着在多个文件中调用的 constexpr 函数需要将其定义包含到每个翻译单元中——这通常会违反一次定义规则。为了避免此类问题，constexpr 函数是隐式 inline 的，这使它们免受一次定义规则的约束。
因此，constexpr 函数通常在头文件中定义，以便它们可以被 #include 到任何需要完整定义的 .cpp 文件中。
规则
编译器必须能够看到 constexpr（或 consteval）函数的完整定义，而不仅仅是前向声明。
最佳实践
在单个源文件 (.cpp) 中使用的 Constexpr/consteval 函数应在源文件中它们被使用的地方上方定义。
在多个源文件中使用的 Constexpr/consteval 函数应在头文件中定义，以便它们可以包含到每个源文件中。
对于仅在运行时求值的 constexpr 函数调用，前向声明足以满足编译器。这意味着您可以使用前向声明来调用在另一个翻译单元中定义的 constexpr 函数，但前提是您在不需要编译时求值的上下文中调用它。
致进阶读者
根据
CWG2166
，对在编译时求值的 constexpr 函数的前向声明的实际要求是“constexpr 函数必须在最终导致调用的最外层求值之前定义”。因此，这是允许的
#include <iostream>

constexpr int foo(int);

constexpr int goo(int c)
{
	return foo(c);   // note that foo is not defined yet
}

constexpr int foo(int b) // okay because foo is still defined before any calls to goo
{
	return b;
}

int main()
{
	 constexpr int a{ goo(5) }; // this is the outermost invocation

	return 0;
}
这里的目的是允许相互递归的 constexpr 函数（其中两个 constexpr 函数相互调用），否则这将是不可能的。
回顾
将函数标记为
constexpr
意味着它可以在常量表达式中使用。它不意味着“将在编译时求值”。
常量表达式（可能包含 constexpr 函数调用）只有在需要常量表达式的上下文中才需要在编译时求值。
在不需要常量表达式的上下文中，编译器可以选择在编译时或运行时求值常量表达式（可能包含 constexpr 函数调用）。
运行时（非常量）表达式（可能包含 constexpr 函数调用或非 constexpr 函数调用）将在运行时求值。
另一个例子
让我们再举一个例子，进一步探讨 constexpr 函数如何被要求或可能求值。
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int g { greater(5, 6) };              // case 1: always evaluated at compile-time
    std::cout << g << " is greater!\n";

    std::cout << greater(5, 6) << " is greater!\n"; // case 2: may be evaluated at either runtime or compile-time

    int x{ 5 }; // not constexpr but value is known at compile-time
    std::cout << greater(x, 6) << " is greater!\n"; // case 3: likely evaluated at runtime

    std::cin >> x;
    std::cout << greater(x, 6) << " is greater!\n"; // case 4: always evaluated at runtime

    return 0;
}
在情况 1 中，我们在需要常量表达式的上下文中调用
greater()
。因此
greater()
必须在编译时求值。
在情况 2 中，
greater()
函数在不需要常量表达式的上下文中被调用，因为输出语句必须在运行时执行。然而，由于参数是常量表达式，该函数有资格在编译时求值。因此，编译器可以自由选择对
greater()
的此调用是在编译时还是运行时求值。
在情况 3 中，我们调用
greater()
，其中一个参数不是常量表达式。所以这通常会在运行时执行。
然而，这个参数的值在编译时是已知的。根据“如同规则”，编译器可以决定将
x
的求值视为常量表达式，并在编译时求值对
greater()
的此调用。但更可能的是，它将在运行时求值。
相关内容
我们在第
5.5 课 —— 常量表达式
中介绍了“如同规则”。
请注意，即使是非 constexpr 函数也可以根据“如同规则”在编译时求值！
在情况 4 中，参数
x
的值在编译时无法确定，因此对
greater()
的此调用将始终在运行时求值。
关键见解
换句话说，我们可以将函数实际在编译时求值的可能性分类如下：
总是（标准要求）
在需要常量表达式的地方调用 constexpr 函数。
从正在编译时求值的其他函数中调用 constexpr 函数。
可能（没有理由不这样做）
在不需要常量表达式的地方调用 constexpr 函数，所有参数都是常量表达式。
也许（如果在“如同规则”下优化）
在不需要常量表达式的地方调用 constexpr 函数，某些参数不是常量表达式但其值在编译时是已知的。
非 constexpr 函数能够在编译时求值，所有参数都是常量表达式。
从不（不可能）
在不需要常量表达式的地方调用 constexpr 函数，某些参数的值在编译时未知。
请注意，您的编译器优化级别设置可能会影响它决定在编译时还是运行时求值函数。这也意味着您的编译器可能会为调试版本和发布版本做出不同的选择（因为调试版本通常关闭了优化）。
例如，gcc 和 Clang 不会在不需要常量表达式的上下文中对 constexpr 函数进行编译时求值，除非编译器被告知优化代码（例如使用
-O2
编译器选项）。
致进阶读者
编译器还可能选择内联函数调用，甚至完全优化掉函数调用。这两种情况都会影响函数调用内容的求值时间（或是否求值）。
下一课
F.3
Constexpr 函数（第三部分）和 consteval
返回目录
上一课
F.1
Constexpr 函数