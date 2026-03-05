# 25.5 — 早期绑定与后期绑定

25.5 — 早期绑定与后期绑定
Alex
2008年2月7日，下午3:46 PST
2024年10月20日
在本节和下一节中，我们将更深入地探讨虚函数的实现方式。虽然这些信息对于有效使用虚函数并非严格必要，但它们很有趣。无论如何，您可以将这两部分内容都视为可选阅读。
当 C++ 程序执行时，它会顺序执行，从
main()
的顶部开始。当遇到函数调用时，执行点会跳转到被调用函数的开头。CPU 是如何知道这样做呢？
当程序编译时，编译器会将 C++ 程序中的每条语句转换为一行或多行机器语言。每行机器语言都被赋予自己独特的顺序地址。函数也不例外——当遇到函数时，它被转换为机器语言并被赋予下一个可用地址。因此，每个函数最终都会有一个唯一的地址。
绑定与调度
我们的程序包含许多名称（标识符、关键字等）。每个名称都有一组关联的属性：例如，如果名称表示一个变量，那么该变量具有类型、值、内存地址等。
例如，当我们说
int x
时，我们是在告诉编译器将名称
x
与类型
int
关联起来。之后，如果我们说
x = 5
，编译器就可以使用这个关联来对赋值进行类型检查，以确保它是有效的。
在通用编程中，**绑定（binding）**是将名称与这些属性关联起来的过程。**函数绑定（function binding）**（或**方法绑定（method binding）**）是确定哪个函数定义与函数调用关联的过程。实际调用已绑定函数的过程称为**调度（dispatching）**。
在 C++ 中，术语“绑定”使用得更随意（而“调度”通常被认为是绑定的一部分）。我们将在下面探讨 C++ 对这些术语的使用。
命名法
绑定是一个重载术语。在其他上下文中，绑定可能指
引用与对象的绑定
std::bind
语言绑定
早期绑定
编译器遇到的大多数函数调用将是直接函数调用。直接函数调用是直接调用函数的语句。例如
#include <iostream>

struct Foo
{
    void printValue(int value)
    {
        std::cout << value;
    }
};

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    printValue(5);   // direct function call to printValue(int)

    Foo f{};
    f.printValue(5); // direct function call to Foo::printValue(int)
    return 0;
}
在 C++ 中，当对非成员函数或非虚成员函数进行直接调用时，编译器可以确定哪个函数定义应该与该调用匹配。这有时被称为**早期绑定（early binding）**（或**静态绑定（static binding）**），因为它可以在编译时执行。然后，编译器（或链接器）可以生成机器语言指令，告诉 CPU 直接跳转到函数的地址。
致进阶读者
如果我们查看为调用
printValue(5)
生成的汇编代码（使用 clang x86-64），我们会看到类似这样：
mov     edi, 5           ; copy argument 5 into edi register in preparation for function call
        call    printValue(int)  ; directly call printValue(int)
您可以清楚地看到，这是一个对 printValue(int) 的直接函数调用。
对重载函数和函数模板的调用也可以在编译时解析。
#include <iostream>

template <typename T>
void printValue(T value)
{
    std::cout << value << '\n';
}

void printValue(double value)
{
    std::cout << value << '\n';
}

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    printValue(5);   // direct function call to printValue(int)
    printValue<>(5); // direct function call to printValue<int>(int)

    return 0;
}
我们来看一个使用早期绑定的简单计算器程序
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int subtract(int x, int y)
{
    return x - y;
}

int multiply(int x, int y)
{
    return x * y;
}

int main()
{
    int x{};
    std::cout << "Enter a number: ";
    std::cin >> x;

    int y{};
    std::cout << "Enter another number: ";
    std::cin >> y;

    int op{};
    std::cout << "Enter an operation (0=add, 1=subtract, 2=multiply): ";
    std::cin >> op;

    int result {};
    switch (op)
    {
        // call the target function directly using early binding
        case 0: result = add(x, y); break;
        case 1: result = subtract(x, y); break;
        case 2: result = multiply(x, y); break;
        default:
            std::cout << "Invalid operator\n";
            return 1;
    }

    std::cout << "The answer is: " << result << '\n';

    return 0;
}
由于
add()
、
subtract()
和
multiply()
都是对非成员函数的直接函数调用，编译器将在编译时将这些函数调用与其各自的函数定义匹配。
请注意，由于 switch 语句的存在，实际调用哪个函数要到运行时才能确定。然而，这是一个执行路径问题，而不是绑定问题。
后期绑定
在某些情况下，函数调用在运行时才能解析。在 C++ 中，这有时被称为**后期绑定（late binding）**（或在虚函数解析的情况下，**动态调度（dynamic dispatch）**）。
作者注
在通用编程术语中，“后期绑定”通常意味着被调用的函数无法仅根据静态类型信息确定，而必须使用动态类型信息来解析。
在 C++ 中，这个术语往往更宽松地使用，指任何在实际进行函数调用时，编译器或链接器无法确定实际被调用函数的函数调用。
在 C++ 中，实现后期绑定的一种方法是使用函数指针。简单回顾一下函数指针，函数指针是一种指向函数而非变量的指针类型。函数指针所指向的函数可以通过对指针使用函数调用运算符
()
来调用。
例如，以下代码通过函数指针调用
printValue()
函数
#include <iostream>

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    auto fcn { printValue }; // create a function pointer and make it point to function printValue
    fcn(5);                  // invoke printValue indirectly through the function pointer

    return 0;
}
通过函数指针调用函数也称为间接函数调用。在实际调用
fcn(5)
时，编译器在编译时不知道正在调用哪个函数。相反，在运行时，会对函数指针所持有的地址处的任何函数进行间接函数调用。
致进阶读者
如果我们查看为调用
fcn(5)
生成的汇编代码（使用 clang x86-64），我们会看到类似这样：
lea     rax, [rip + printValue(int)] ; determine address of printValue and place into rax register
        mov     qword ptr [rbp - 8], rax     ; move value in rax register into memory associated with variable fcn

        mov     edi, 5                       ; copy argument 5 into edi register in preparation for function call
        call    qword ptr [rbp - 8]          ; invoke the function at the address held by variable fcn
您可以清楚地看到，这是一个通过其地址对 printValue(int) 进行的间接函数调用。
下面的计算器程序在功能上与上面的计算器示例相同，只是它使用函数指针而不是直接函数调用
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int subtract(int x, int y)
{
    return x - y;
}

int multiply(int x, int y)
{
    return x * y;
}

int main()
{
    int x{};
    std::cout << "Enter a number: ";
    std::cin >> x;

    int y{};
    std::cout << "Enter another number: ";
    std::cin >> y;

    int op{};
    std::cout << "Enter an operation (0=add, 1=subtract, 2=multiply): ";
    std::cin >> op;

    using FcnPtr = int (*)(int, int); // alias ugly function pointer type
    FcnPtr fcn { nullptr }; // create a function pointer object, set to nullptr initially

    // Set fcn to point to the function the user chose
    switch (op)
    {
        case 0: fcn = add; break;
        case 1: fcn = subtract; break;
        case 2: fcn = multiply; break;
        default:
            std::cout << "Invalid operator\n";
            return 1;
    }

    // Call the function that fcn is pointing to with x and y as parameters
    std::cout << "The answer is: " << fcn(x, y) << '\n';

    return 0;
}
在这个例子中，我们没有直接调用
add()
、
subtract()
或
multiply()
函数，而是将
fcn
设置为指向我们希望调用的函数。然后我们通过指针调用该函数。
编译器无法使用早期绑定来解析函数调用
fcn(x, y)
，因为它在编译时无法判断
fcn
将指向哪个函数！
后期绑定效率略低，因为它涉及额外的间接层。使用早期绑定，CPU 可以直接跳转到函数的地址。使用后期绑定，程序必须读取指针中保存的地址，然后跳转到该地址。这涉及一个额外的步骤，使其速度稍慢。然而，后期绑定的优点是它比早期绑定更灵活，因为关于调用哪个函数的决定不需要在运行时做出。
在下一课中，我们将探讨后期绑定如何用于实现虚函数。
下一课
25.6
虚表
返回目录
上一课
25.4
虚析构函数、虚赋值与重写虚化