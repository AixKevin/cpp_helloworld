# 11.8 — 具有多个模板类型的函数模板

11.8 — 具有多个模板类型的函数模板
Alex
2021 年 6 月 17 日，下午 5:46 （太平洋夏令时）
2024 年 12 月 18 日
在
11.6 — 函数模板
这一课中，我们编写了一个函数模板来计算两个值的最大值。
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(1, 2) << '\n';   // will instantiate max(int, int)
    std::cout << max(1.5, 2.5) << '\n'; // will instantiate max(double, double)

    return 0;
}
现在考虑以下类似的程序：
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n';  // compile error

    return 0;
}
你可能会惊讶地发现这个程序无法编译。相反，编译器会发出许多（可能看起来很奇怪的）错误消息。在 Visual Studio 上，作者得到了以下错误：
Project3.cpp(11,18): error C2672: 'max': no matching overloaded function found
Project3.cpp(11,28): error C2782: 'T max(T,T)': template parameter 'T' is ambiguous
Project3.cpp(4): message : see declaration of 'max'
Project3.cpp(11,28): message : could be 'double'
Project3.cpp(11,28): message : or       'int'
Project3.cpp(11,28): error C2784: 'T max(T,T)': could not deduce template argument for 'T' from 'double'
Project3.cpp(4): message : see declaration of 'max'
在我们的函数调用
max(2, 3.5)
中，我们传递了两种不同类型的参数：一个
int
和一个
double
。因为我们在不使用尖括号指定实际类型的情况下进行函数调用，编译器会首先查找是否存在
max(int, double)
的非模板匹配项。它将找不到。
接下来，编译器会查看是否能找到函数模板匹配项（使用模板参数推导，我们在
11.7 — 函数模板实例化
这一课中讨论过）。然而，这也会失败，原因很简单：
T
只能表示一个类型。没有类型
T
能让编译器将函数模板
max<T>(T, T)
实例化为具有两种不同参数类型的函数。换句话说，因为函数模板中的两个参数都是
T
类型，它们必须解析为相同的实际类型。
由于既找不到非模板匹配项，也找不到模板匹配项，函数调用无法解析，我们得到了一个编译错误。
你可能想知道为什么编译器没有生成函数
max<double>(double, double)
，然后使用数值转换将
int
参数类型转换为
double
。答案很简单：类型转换只在解析函数重载时进行，而不是在执行模板参数推导时进行。
这种缺乏类型转换是有意为之的，至少有两个原因。首先，它有助于保持简单：我们要么在函数调用参数和模板类型参数之间找到精确匹配，要么找不到。其次，它允许我们为希望确保两个或更多参数具有相同类型的情况创建函数模板（如上例所示）。
我们必须找到另一种解决方案。幸运的是，我们可以通过（至少）三种方式解决这个问题。
使用 static_cast 将参数转换为匹配类型
第一个解决方案是将转换参数为匹配类型的负担放在调用者身上。例如：
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(static_cast<double>(2), 3.5) << '\n'; // convert our int to a double so we can call max(double, double)

    return 0;
}
现在两个参数都是
double
类型，编译器将能够实例化
max(double, double)
来满足此函数调用。
然而，这种解决方案显得笨拙且难以阅读。
提供显式类型模板参数
如果我们编写了一个非模板
max(double, double)
函数，那么我们就能够调用
max(int, double)
并让隐式类型转换规则将我们的
int
参数转换为
double
，这样函数调用就可以被解析：
#include <iostream>

double max(double x, double y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n'; // the int argument will be converted to a double

    return 0;
}
然而，当编译器进行模板参数推导时，它不会进行任何类型转换。幸运的是，如果我们指定一个显式类型模板参数来代替，我们就不必使用模板参数推导：
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    // we've explicitly specified type double, so the compiler won't use template argument deduction
    std::cout << max<double>(2, 3.5) << '\n';

    return 0;
}
在上面的示例中，我们调用
max<double>(2, 3.5)
。因为我们已明确指定
T
应该替换为
double
，所以编译器将不会使用模板参数推导。相反，它将直接实例化函数
max<double>(double, double)
，然后对任何不匹配的参数进行类型转换。我们的
int
参数将隐式转换为
double
。
虽然这比使用
static_cast
更具可读性，但如果我们在调用
max
函数时根本不必考虑类型，那会更好。
具有多个模板类型参数的函数模板
我们问题的根源在于，我们只为函数模板定义了单一的模板类型（
T
），然后指定了两个参数都必须是这种相同的类型。
解决这个问题的最佳方法是重写函数模板，使参数可以解析为不同的类型。我们现在将使用两个（
T
和
U
）而不是一个模板类型参数
T
：
#include <iostream>

template <typename T, typename U> // We're using two template type parameters named T and U
T max(T x, U y) // x can resolve to type T, and y can resolve to type U
{
    return (x < y) ? y : x; // uh oh, we have a narrowing conversion problem here
}

int main()
{
    std::cout << max(2, 3.5) << '\n'; // resolves to max<int, double>

    return 0;
}
因为我们将
x
定义为模板类型
T
，将
y
定义为模板类型
U
，所以
x
和
y
现在可以独立解析它们的类型。当我们调用
max(2, 3.5)
时，
T
可以是
int
，
U
可以是
double
。编译器将很乐意为我们实例化
max<int, double>(int, double)
。
关键见解
因为
T
和
U
是独立的模板参数，它们相互独立地解析其类型。这意味着
T
和
U
可以解析为不同的类型，或者它们可以解析为相同的类型。
然而，这个例子并不完全正确。如果你编译并运行程序（关闭“将警告视为错误”选项），它将产生以下结果：
3
这是怎么回事？2 和 3.5 的最大值怎么会是 3 呢？
条件运算符（?:）要求其（非条件）操作数具有相同的通用类型。通常的算术规则（
10.5 — 算术转换
）用于确定通用类型，条件运算符的结果也将使用此通用类型。例如，
int
和
double
的通用类型是
double
，因此当我们的条件运算符的（非条件）操作数是
int
和
double
时，条件运算符产生的值将是
double
类型。在这种情况下，结果是
3.5
，这是正确的。
然而，我们函数的声明返回类型是
T
。当
T
是
int
而
U
是
double
时，函数的返回类型是
int
。我们的值
3.5
正在经历窄化转换到
int
值
3
，导致数据丢失（并且可能产生编译器警告）。
那我们怎么解决这个问题呢？将返回类型改为
U
也无法解决问题，因为
max(3.5, 2)
中的
U
是
int
，也会出现同样的问题。
在这种情况下，返回类型推导（通过
auto
）可能会很有用——我们将让编译器从返回语句中推导出返回类型：
#include <iostream>

template <typename T, typename U>
auto max(T x, U y) // ask compiler can figure out what the relevant return type is
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n';

    return 0;
}
这个版本的
max
现在可以很好地处理不同类型的操作数。请注意，具有
auto
返回类型的函数需要在其被使用之前完全定义（前向声明不足），因为编译器必须检查函数实现以确定返回类型。
致进阶读者
如果我们需要一个可以前向声明的函数，我们必须明确返回类型。由于我们的返回类型需要是
T
和
U
的通用类型，我们可以使用
std::common_type_t
（在
10.5 — 算术转换
这一课中讨论过）来获取
T
和
U
的通用类型作为我们的显式返回类型：
#include <iostream>
#include <type_traits> // for std::common_type_t

template <typename T, typename U>
auto max(T x, U y) -> std::common_type_t<T, U>; // returns the common type of T and U

int main()
{
    std::cout << max(2, 3.5) << '\n';

    return 0;
}

template <typename T, typename U>
auto max(T x, U y) -> std::common_type_t<T, U>
{
    return (x < y) ? y : x;
}
简写函数模板
C++20
C++20 引入了
auto
关键字的新用法：当
auto
关键字在普通函数中用作参数类型时，编译器会自动将该函数转换为函数模板，其中每个
auto
参数都成为一个独立的模板类型参数。这种创建函数模板的方法称为**简写函数模板**。
例如
auto max(auto x, auto y)
{
    return (x < y) ? y : x;
}
在 C++20 中是以下内容的简写：
template <typename T, typename U>
auto max(T x, U y)
{
    return (x < y) ? y : x;
}
这与我们上面编写的
max
函数模板相同。
在您希望每个模板类型参数都是独立类型的情况下，此形式是首选，因为删除了模板参数声明行，使您的代码更简洁易读。
当您希望多个
auto
参数是同一类型时，没有简洁的方法来使用简写函数模板。也就是说，对于以下情况，没有简单的简写函数模板：
template <typename T>
T max(T x, T y) // two parameters of the same type
{
    return (x < y) ? y : x;
}
最佳实践
随意使用只有一个 auto 参数的简写函数模板，或者每个 auto 参数都应该是一个独立类型（并且您的语言标准设置为 C++20 或更高版本）的情况。
函数模板可以被重载
就像函数可以重载一样，函数模板也可以重载。这样的重载可以有不同数量的模板类型和/或不同数量或类型的函数参数：
#include <iostream>

// Add two values with matching types
template <typename T>
auto add(T x, T y)
{
    return x + y;
}

// Add two values with non-matching types
// As of C++20 we could also use auto add(auto x, auto y)
template <typename T, typename U>
auto add(T x, U y)
{
    return x + y;
}

// Add three values with any type
// As of C++20 we could also use auto add(auto x, auto y, auto z)
template <typename T, typename U, typename V>
auto add(T x, U y, V z)
{
    return x + y + z;
}

int main()
{
    std::cout << add(1.2, 3.4) << '\n'; // instantiates and calls add<double>()
    std::cout << add(5.6, 7) << '\n';   // instantiates and calls add<double, int>()
    std::cout << add(8, 9, 10) << '\n'; // instantiates and calls add<int, int, int>()

    return 0;
}
这里一个有趣的注意事项是，对于对
add(1.2, 3.4)
的调用，编译器将优先选择
add<T>(T, T)
而非
add<T, U>(T, U)
，即使两者都可能匹配。
确定多个匹配函数模板中应优先选择哪个的规则称为“函数模板的偏序”。简而言之，哪个函数模板更具限制性/更特化，哪个就会被优先选择。在这种情况下，
add<T>(T, T)
是更具限制性的函数模板（因为它只有一个模板参数），所以它被优先选择。
如果多个函数模板可以匹配一个调用，并且编译器无法确定哪个更具限制性，编译器将因模糊匹配而报错。
下一课
11.9
非类型模板参数
返回目录
上一课
11.7
函数模板实例化