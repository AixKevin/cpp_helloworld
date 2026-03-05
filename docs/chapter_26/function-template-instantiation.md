# 11.7 — 函数模板实例化

11.7 — 函数模板实例化
Alex
2021 年 6 月 17 日，下午 5:50 PDT
2024 年 8 月 21 日
在上一课（
11.6 -- 函数模板
）中，我们介绍了函数模板，并将一个普通的
max()
函数转换成了
max<T>
函数模板
template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}
在本课中，我们将重点介绍函数模板的使用方式。
使用函数模板
函数模板实际上不是函数——它们的代码不会被直接编译或执行。相反，函数模板只有一项工作：生成函数（它们会被编译和执行）。
要使用我们的
max<T>
函数模板，我们可以使用以下语法进行函数调用
max<actual_type>(arg1, arg2); // actual_type is some actual type, like int or double
这看起来很像一个普通的函数调用——主要区别在于增加了尖括号中的类型（称为
模板实参
），它指定了将用于替换模板类型
T
的实际类型。
让我们在一个简单的例子中看看这个
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // instantiates and calls function max<int>(int, int)

    return 0;
}
当编译器遇到函数调用
max<int>(1, 2)
时，它将确定
max<int>(int, int)
的函数定义尚不存在。因此，编译器将隐式使用我们的
max<T>
函数模板来创建一个。
从函数模板（带有模板类型）创建函数（带有特定类型）的过程称为
函数模板实例化
（或简称
实例化
）。当函数因函数调用而实例化时，它被称为
隐式实例化
。从模板实例化的函数在技术上称为
特化
，但在常用语言中通常称为
函数实例
。产生特化的模板称为
主模板
。函数实例在所有方面都是普通函数。
命名法
“特化”这个术语更常用于指代显式特化，它允许我们显式定义一个特化（而不是让它从主模板隐式实例化）。我们在第
26.3 -- 函数模板特化
课中介绍了显式特化。
实例化函数的过程很简单：编译器实质上克隆主模板，并将模板类型（
T
）替换为我们指定的实际类型（
int
）。
因此，当我们调用
max<int>(1, 2)
时，被实例化的函数特化看起来像这样
template<> // ignore this for now
int max<int>(int x, int y) // the generated function max<int>(int, int)
{
    return (x < y) ? y : x;
}
这是上面相同的例子，显示了在所有实例化完成后编译器实际编译的内容
#include <iostream>

// a declaration for our function template (we don't need the definition any more)
template <typename T> 
T max(T x, T y);

template<>
int max<int>(int x, int y) // the generated function max<int>(int, int)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // instantiates and calls function max<int>(int, int)

    return 0;
}
您可以自己编译它并查看它是否有效。函数模板只在每个翻译单元中首次进行函数调用时实例化。对该函数的进一步调用将路由到已经实例化的函数。
相反，如果对函数模板没有进行函数调用，则该函数模板在该翻译单元中将不会被实例化。
让我们再举一个例子
#include <iostream>

template <typename T>
T max(T x, T y) // function template for max(T, T)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n';    // instantiates and calls function max<int>(int, int)
    std::cout << max<int>(4, 3) << '\n';    // calls already instantiated function max<int>(int, int)
    std::cout << max<double>(1, 2) << '\n'; // instantiates and calls function max<double>(double, double)

    return 0;
}
这与上一个例子类似，但我们的函数模板这次将用于生成两个函数：一次将
T
替换为
int
，另一次将
T
替换为
double
。所有实例化完成后，程序将看起来像这样
#include <iostream>

// a declaration for our function template (we don't need the definition any more)
template <typename T>
T max(T x, T y); 

template<>
int max<int>(int x, int y) // the generated function max<int>(int, int)
{
    return (x < y) ? y : x;
}

template<>
double max<double>(double x, double y) // the generated function max<double>(double, double)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n';    // instantiates and calls function max<int>(int, int)
    std::cout << max<int>(4, 3) << '\n';    // calls already instantiated function max<int>(int, int)
    std::cout << max<double>(1, 2) << '\n'; // instantiates and calls function max<double>(double, double)

    return 0;
}
这里需要注意的另一件事：当我们实例化
max<double>
时，实例化的函数具有
double
类型的参数。由于我们提供了
int
实参，这些实参将隐式转换为
double
。
模板实参推导
在大多数情况下，我们希望用于实例化的实际类型将与我们的函数参数的类型匹配。例如
std::cout << max<int>(1, 2) << '\n'; // specifying we want to call max<int>
在此函数调用中，我们指定要将
T
替换为
int
，但我们还使用
int
实参调用函数。
在实参类型与我们想要的实际类型匹配的情况下，我们不需要指定实际类型——相反，我们可以使用
模板实参推导
让编译器从函数调用中的实参类型推导出应该使用的实际类型。
例如，而不是像这样进行函数调用
std::cout << max<int>(1, 2) << '\n'; // specifying we want to call max<int>
我们可以这样做
std::cout << max<>(1, 2) << '\n';
std::cout << max(1, 2) << '\n';
在任一情况下，编译器都将看到我们没有提供实际类型，因此它将尝试从函数实参推导出实际类型，以便生成一个
max()
函数，其中所有模板参数都与所提供实参的类型匹配。在此示例中，编译器将推导出使用实际类型为
int
的函数模板
max<T>
可以实例化函数
max<int>(int, int)
，这样两个函数参数的类型（
int
）都与所提供实参的类型（
int
）匹配。
这两种情况之间的区别在于编译器如何从一组重载函数中解析函数调用。在上面的情况（带有空尖括号）中，编译器在确定要调用哪个重载函数时，只会考虑
max<int>
模板函数重载。在下面的情况（不带尖括号）中，编译器会同时考虑
max<int>
模板函数重载和
max
非模板函数重载。当下面的情况导致模板函数和非模板函数都同样可行时，非模板函数将优先。
关键见解
普通函数调用语法将优先选择非模板函数，而不是从模板实例化的同样可行的函数。
例如
#include <iostream>

template <typename T>
T max(T x, T y)
{
    std::cout << "called max<int>(int, int)\n";
    return (x < y) ? y : x;
}

int max(int x, int y)
{
    std::cout << "called max(int, int)\n";
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // calls max<int>(int, int)
    std::cout << max<>(1, 2) << '\n';    // deduces max<int>(int, int) (non-template functions not considered)
    std::cout << max(1, 2) << '\n';      // calls max(int, int)

    return 0;
}
请注意，下面情况的语法与普通函数调用完全相同！在大多数情况下，这种普通函数调用语法将是我们用来调用从函数模板实例化的函数的方式。
这有几个原因
语法更简洁。
我们很少会同时拥有匹配的非模板函数和函数模板。
如果我们确实有一个匹配的非模板函数和一个匹配的函数模板，我们通常会更倾向于调用非模板函数。
最后一点可能不明显。函数模板的实现适用于多种类型——但因此，它必须是通用的。非模板函数只处理特定类型的组合。它可能拥有比函数模板版本更优化或更专门针对这些特定类型的实现。例如
#include <iostream>

// This function template can handle many types, so its implementation is generic
template <typename T>
void print(T x)
{
    std::cout << x; // print T however it normally prints
}

// This function only needs to consider how to print a bool, so it can specialize how it handles
// printing of a bool
void print(bool x)
{
    std::cout << std::boolalpha << x; // print bool as true or false, not 1 or 0
}

int main()
{
    print<bool>(true); // calls print<bool>(bool) -- prints 1
    std::cout << '\n';

    print<>(true);     // deduces print<bool>(bool) (non-template functions not considered) -- prints 1
    std::cout << '\n';

    print(true);       // calls print(bool) -- prints true
    std::cout << '\n';

    return 0;
}
最佳实践
当调用从函数模板实例化的函数时，请优先使用普通函数调用语法（除非您需要函数模板版本优先于匹配的非模板函数）。
带有非模板参数的函数模板
可以创建同时具有模板参数和非模板参数的函数模板。类型模板参数可以匹配任何类型，而非模板参数则像普通函数的参数一样工作。
例如
// T is a type template parameter
// double is a non-template parameter
// We don't need to provide names for these parameters since they aren't used
template <typename T>
int someFcn(T, double)
{
    return 5;
}

int main()
{
    someFcn(1, 3.4); // matches someFcn(int, double)
    someFcn(1, 3.4f); // matches someFcn(int, double) -- the float is promoted to a double
    someFcn(1.2, 3.4); // matches someFcn(double, double)
    someFcn(1.2f, 3.4); // matches someFcn(float, double)
    someFcn(1.2f, 3.4f); // matches someFcn(float, double) -- the float is promoted to a double

    return 0;
}
此函数模板的第一个参数是模板化的，但第二个参数固定为
double
类型。请注意，返回类型也可以是任何类型。在此示例中，我们的函数将始终返回一个
int
值。
实例化的函数可能无法总是编译成功
考虑以下程序
#include <iostream>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';

    return 0;
}
编译器将有效地编译并执行此代码
#include <iostream>

template <typename T>
T addOne(T x);

template<>
int addOne<int>(int x)
{
    return x + 1;
}

template<>
double addOne<double>(double x)
{
    return x + 1;
}

int main()
{
    std::cout << addOne(1) << '\n';   // calls addOne<int>(int)
    std::cout << addOne(2.3) << '\n'; // calls addOne<double>(double)

    return 0;
}
这将产生结果
2
3.3
但如果我们尝试这样的操作会怎样？
#include <iostream>
#include <string>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

int main()
{
    std::string hello { "Hello, world!" };
    std::cout << addOne(hello) << '\n';

    return 0;
}
当编译器尝试解析
addOne(hello)
时，它不会找到
addOne(std::string)
的非模板函数匹配，但它会找到我们的
addOne(T)
函数模板，并确定可以从中生成一个
addOne(std::string)
函数。因此，编译器将生成并编译此代码
#include <iostream>
#include <string>

template <typename T>
T addOne(T x);

template<>
std::string addOne<std::string>(std::string x)
{
    return x + 1;
}

int main()
{
    std::string hello{ "Hello, world!" };
    std::cout << addOne(hello) << '\n';

    return 0;
}
然而，这将产生一个编译错误，因为当
x
是
std::string
时，
x + 1
没有意义。这里显而易见的解决方案是根本不要使用
std::string
类型的参数调用
addOne()
。
实例化的函数可能并非总是在语义上有意义
只要语法上合理，编译器就会成功编译实例化函数模板。但是，编译器无法检查这样的函数是否在语义上真正有意义。
例如
#include <iostream>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

int main()
{
    std::cout << addOne("Hello, world!") << '\n';

    return 0;
}
在这个例子中，我们正在对 C 风格的字符串字面值调用
addOne()
。这在语义上到底意味着什么？谁知道！
或许令人惊讶的是，由于 C++ 在语法上允许将整数值添加到字符串字面值（我们将在未来的课程
17.9 -- 指针算术和下标
中介绍），上面的示例可以编译，并产生以下结果
ello, world!
警告
只要语法有效，编译器就会实例化并编译在语义上没有意义的函数模板。您有责任确保使用有意义的参数调用此类函数模板。
致进阶读者
我们可以告诉编译器，某些参数的函数模板实例化应该被禁止。这通过使用函数模板特化来完成，它允许我们针对特定的模板参数集重载函数模板，并结合
= delete
，这会告诉编译器，任何使用该函数的行为都应发出编译错误。
#include <iostream>
#include <string>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

// Use function template specialization to tell the compiler that addOne(const char*) should emit a compilation error
// const char* will match a string literal
template <>
const char* addOne(const char* x) = delete;

int main()
{
    std::cout << addOne("Hello, world!") << '\n'; // compile error

    return 0;
}
我们在第
26.3 -- 函数模板特化
课中介绍了函数模板特化。
函数模板与非模板参数的默认实参
就像普通函数一样，函数模板可以为非模板参数设置默认实参。从模板实例化的每个函数都将使用相同的默认实参。
例如
#include <iostream>

template <typename T>
void print(T val, int times=1)
{
    while (times--)
    {
        std::cout << val;        
    }
}

int main()
{
    print(5);      // print 5 1 time
    print('a', 3); // print 'a' 3 times

    return 0;
}
这会打印
5aaa
小心带有可修改的静态局部变量的函数模板
在第
7.11 -- 静态局部变量
课中，我们讨论了静态局部变量，它们是具有静态持续时间（在程序生命周期内持续存在）的局部变量。
当静态局部变量在函数模板中使用时，从该模板实例化的每个函数都将拥有一个独立的静态局部变量版本。如果静态局部变量是常量，这很少会成为问题。但如果静态局部变量是可修改的，结果可能不会像预期那样。
例如
#include <iostream>

// Here's a function template with a static local variable that is modified
template <typename T>
void printIDAndValue(T value)
{
    static int id{ 0 };
    std::cout << ++id << ") " << value << '\n';
}

int main()
{
    printIDAndValue(12);
    printIDAndValue(13);

    printIDAndValue(14.5);

    return 0;
}
这会产生结果
1) 12
2) 13
1) 14.5
您可能预期最后一行会打印
3) 14.5
。然而，这就是编译器实际编译和执行的内容
#include <iostream>

template <typename T>
void printIDAndValue(T value);

template <>
void printIDAndValue<int>(int value)
{
    static int id{ 0 };
    std::cout << ++id << ") " << value << '\n';
}

template <>
void printIDAndValue<double>(double value)
{
    static int id{ 0 };
    std::cout << ++id << ") " << value << '\n';
}

int main()
{
    printIDAndValue(12);   // calls printIDAndValue<int>()
    printIDAndValue(13);   // calls printIDAndValue<int>()

    printIDAndValue(14.5); // calls printIDAndValue<double>()

    return 0;
}
请注意，
printIDAndValue<int>
和
printIDAndValue<double>
各自拥有自己独立的名为
id
的静态局部变量，而不是它们之间共享的。
泛型编程
因为模板类型可以被任何实际类型替换，所以模板类型有时被称为
泛型类型
。又因为模板可以不考虑特定类型地编写，所以用模板编程有时被称为
泛型编程
。C++ 通常非常注重类型和类型检查，相比之下，泛型编程让我们能够专注于算法的逻辑和数据结构的设计，而不必过多担心类型信息。
总结
一旦您习惯了编写函数模板，您会发现它们实际上并不比编写具有实际类型的函数花费更长时间。函数模板可以通过最小化需要编写和维护的代码量来显著减少代码维护和错误。
函数模板确实有一些缺点，我们不能不提。首先，编译器会为每个具有独特实参类型的函数调用创建（并编译）一个函数。因此，虽然函数模板编写起来很简洁，但它们可以扩展成大量的代码，这可能导致代码膨胀和编译时间变慢。函数模板更大的缺点是它们倾向于产生看起来很疯狂、几乎无法阅读的错误消息，这些错误消息比普通函数的错误消息更难解密。这些错误消息可能相当吓人，但一旦您理解它们试图告诉您什么，它们所指出的问题通常相当容易解决。
与模板为您的编程工具包带来的强大功能和安全性相比，这些缺点微不足道，因此在任何需要类型灵活性的地方都请随意使用模板！一个好的经验法则是首先创建普通函数，然后如果您发现需要为不同的参数类型进行重载，则将其转换为函数模板。
最佳实践
在需要时，使用函数模板编写可处理各种类型的泛型代码。
下一课
11.8
具有多个模板类型的函数模板
返回目录
上一课
11.6
函数模板