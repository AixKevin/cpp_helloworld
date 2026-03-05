# 13.13 — 类模板

13.13 — 类模板
Alex
2022 年 4 月 21 日，下午 1:48 PDT
2024 年 12 月 30 日
在第
11.6 课 -- 函数模板
中，我们介绍了必须为每组不同的类型创建单独的（重载）函数的挑战。
#include <iostream>

// function to calculate the greater of two int values
int max(int x, int y)
{
    return (x < y) ? y : x;
}

// almost identical function to calculate the greater of two double values
// the only difference is the type information
double max(double x, double y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(5, 6);     // calls max(int, int)
    std::cout << '\n';
    std::cout << max(1.2, 3.4); // calls max(double, double)

    return 0;
}
这个问题的解决方案是创建一个函数模板，编译器可以使用它为我们需要的任何一组类型实例化普通函数。
#include <iostream>

// a single function template for max
template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(5, 6);     // instantiates and calls max<int>(int, int)
    std::cout << '\n';
    std::cout << max(1.2, 3.4); // instantiates and calls max<double>(double, double)

    return 0;
}
相关内容
我们在第
11.7 课 -- 函数模板实例化
中介绍了函数模板实例化是如何工作的。
聚合类型也面临类似的挑战。
我们遇到了聚合类型（结构体/类/联合和数组）的类似挑战。
例如，假设我们正在编写一个程序，我们需要处理成对的
int
值，并且需要确定这两个数字中哪个更大。我们可能会编写一个像这样的程序：
#include <iostream>

struct Pair
{
    int first{};
    int second{};
};

constexpr int max(Pair p) // pass by value because Pair is small
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair p1{ 5, 6 };
    std::cout << max(p1) << " is larger\n";

    return 0;
}
后来，我们发现我们还需要成对的
double
值。所以我们更新了我们的程序如下：
#include <iostream>

struct Pair
{
    int first{};
    int second{};
};

struct Pair // compile error: erroneous redefinition of Pair
{
    double first{};
    double second{};
};

constexpr int max(Pair p)
{
    return (p.first < p.second ? p.second : p.first);
}

constexpr double max(Pair p) // compile error: overloaded function differs only by return type
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair p1{ 5, 6 };
    std::cout << max(p1) << " is larger\n";

    Pair p2{ 1.2, 3.4 };
    std::cout << max(p2) << " is larger\n";

    return 0;
}
不幸的是，这个程序无法编译，并且有许多问题需要解决。
首先，与函数不同，类型定义不能被重载。编译器会将
Pair
的第二个定义视为
Pair
第一个定义的错误重新声明。其次，尽管函数可以重载，但我们的
max(Pair)
函数仅在返回类型上有所不同，而重载函数不能仅通过返回类型来区分。第三，这里有很多冗余。每个
Pair
结构体都是相同的（除了数据类型），我们的
max(Pair)
函数也是如此（除了返回类型）。
我们可以通过给我们的
Pair
结构体不同的名称（例如
PairInt
和
PairDouble
）来解决前两个问题。但是那样我们既要记住我们的命名方案，又要为我们想要的每种额外的对类型复制一大堆代码，这并不能解决冗余问题。
幸运的是，我们可以做得更好。
作者注
在继续之前，如果您对函数模板、模板类型或函数模板实例化如何工作感到模糊，请回顾第
11.6 课 -- 函数模板
和
11.7 课 -- 函数模板实例化
。
类模板
就像函数模板是用于实例化函数的模板定义一样，
类模板
是用于实例化类类型的模板定义。
提醒
“类类型”是指结构体、类或联合类型。尽管为了简单起见，我们将在结构体上演示“类模板”，但这里的一切同样适用于类。
作为提醒，这是我们的
int
对结构体定义：
struct Pair
{
    int first{};
    int second{};
};
让我们将我们的对类重写为类模板：
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

int main()
{
    Pair<int> p1{ 5, 6 };        // instantiates Pair<int> and creates object p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // instantiates Pair<double> and creates object p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // creates object p3 using prior definition for Pair<double>
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
就像函数模板一样，我们以模板参数声明开始类模板定义。我们以
template
关键字开头。接下来，我们在尖括号（<>）内指定我们的类模板将使用的所有模板类型。对于我们需要的每个模板类型，我们使用关键字
typename
（首选）或
class
（不首选），后跟模板类型的名称（例如
T
）。在这种情况下，由于我们的两个成员将是相同的类型，我们只需要一个模板类型。
接下来，我们像往常一样定义我们的结构体，只是我们可以在任何需要模板类型的地方使用我们的模板类型（
T
），它将在以后被真实的类型替换。就这样！我们完成了类模板定义。
在 main 函数内部，我们可以使用我们想要的任何类型实例化
Pair
对象。首先，我们实例化一个
Pair
类型的对象。因为
Pair
的类型定义尚不存在，所以编译器使用类模板来实例化一个名为
Pair
的结构体类型定义，其中所有模板类型
T
的出现都替换为
int
类型。
接下来，我们实例化一个
Pair
类型的对象，它实例化了一个名为
Pair
的结构体类型定义，其中
T
被替换为
double
。对于
p3
，
Pair
已经实例化，因此编译器将使用之前的类型定义。
这是上面的相同示例，显示了所有模板实例化完成后编译器实际编译的内容：
#include <iostream>

// A declaration for our Pair class template
// (we don't need the definition any more since it's not used)
template <typename T>
struct Pair;

// Explicitly define what Pair<int> looks like
template <> // tells the compiler this is a template type with no template parameters
struct Pair<int>
{
    int first{};
    int second{};
};

// Explicitly define what Pair<double> looks like
template <> // tells the compiler this is a template type with no template parameters
struct Pair<double>
{
    double first{};
    double second{};
};

int main()
{
    Pair<int> p1{ 5, 6 };        // instantiates Pair<int> and creates object p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // instantiates Pair<double> and creates object p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // creates object p3 using prior definition for Pair<double>
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
您可以直接编译此示例，看看它是否按预期工作！
致进阶读者
上面的例子利用了一个名为类模板特化（在未来的课程
26.4 -- 类模板特化
中介绍）的特性。目前不需要了解此特性如何工作。
在函数中使用我们的类模板
现在让我们回到让我们的
max()
函数处理不同类型的挑战。因为编译器将
Pair
和
Pair
视为不同的类型，我们可以使用通过参数类型区分的重载函数：
constexpr int max(Pair<int> p)
{
    return (p.first < p.second ? p.second : p.first);
}

constexpr double max(Pair<double> p) // okay: overloaded function differentiated by parameter type
{
    return (p.first < p.second ? p.second : p.first);
}
虽然这可以编译，但它并没有解决冗余问题。我们真正想要的是一个可以接受任何类型的对的函数。换句话说，我们想要一个接受
Pair
类型的参数的函数，其中 T 是一个模板类型参数。这意味着我们需要一个函数模板来完成这项工作！
这是一个完整的示例，其中
max()
被实现为一个函数模板：
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
constexpr T max(Pair<T> p)
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair<int> p1{ 5, 6 };
    std::cout << max<int>(p1) << " is larger\n"; // explicit call to max<int>

    Pair<double> p2{ 1.2, 3.4 };
    std::cout << max(p2) << " is larger\n"; // call to max<double> using template argument deduction (prefer this)

    return 0;
}
max()
函数模板非常简单。因为我们想传入一个
Pair
，所以我们需要编译器理解
T
是什么。因此，我们需要以定义模板类型 T 的模板参数声明开始我们的函数。然后我们可以将
T
用作返回类型，以及
Pair
的模板类型。
当
max()
函数被调用时，传入一个
Pair
参数，编译器将从函数模板实例化函数
int max
(Pair
)
，其中模板类型
T
被替换为
int
。以下代码片段显示了在这种情况下编译器实际实例化的内容：
template <>
constexpr int max(Pair<int> p)
{
    return (p.first < p.second ? p.second : p.first);
}
与所有对函数模板的调用一样，我们可以显式指定模板类型参数（例如
max
(p1)
）或者隐式指定（例如
max(p2)
），并让编译器使用模板参数推导来确定模板类型参数应该是什么。
包含模板类型和非模板类型成员的类模板
类模板可以有一些成员使用模板类型，而其他成员使用普通（非模板）类型。例如：
template <typename T>
struct Foo
{
    T first{};    // first will have whatever type T is replaced with
    int second{}; // second will always have type int, regardless of what type T is
};
这完全符合您的预期：
first
将是模板类型
T
的任何类型，而
second
始终是
int
。
具有多个模板类型的类模板
类模板也可以有多个模板类型。例如，如果我们要让我们的
Pair
类的两个成员可以有不同的类型，我们可以用两个模板类型来定义我们的
Pair
类模板：
#include <iostream>

template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
void print(Pair<T, U> p)
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}

int main()
{
    Pair<int, double> p1{ 1, 2.3 }; // a pair holding an int and a double
    Pair<double, int> p2{ 4.5, 6 }; // a pair holding a double and an int
    Pair<int, int> p3{ 7, 8 };      // a pair holding two ints

    print(p2);

    return 0;
}
要定义多个模板类型，在我们的模板参数声明中，我们用逗号分隔我们想要的每个模板类型。在上面的例子中，我们定义了两个不同的模板类型，一个命名为
T
，另一个命名为
U
。
T
和
U
的实际模板类型参数可以不同（如上面
p1
和
p2
的情况），也可以相同（如
p3
的情况）。
使函数模板适用于多种类类型
考虑上面示例中的
print()
函数模板：
template <typename T, typename U>
void print(Pair<T, U> p)
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}
因为我们已经显式地将函数参数定义为
Pair
，所以只有
Pair
类型的参数（或可以转换为
Pair
的参数）才会匹配。如果我们只想用
Pair
参数调用我们的函数，这是理想的选择。
在某些情况下，我们可能编写希望用于任何成功编译的类型的函数模板。为此，我们只需使用类型模板参数作为函数参数即可。
例如
#include <iostream>

template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

struct Point
{
    int first{};
    int second{};
};

template <typename T>
void print(T p) // type template parameter will match anything
{
    std::cout << '[' << p.first << ", " << p.second << ']'; // will only compile if type has first and second members
}

int main()
{
    Pair<double, int> p1{ 4.5, 6 };
    print(p1); // matches print(Pair<double, int>)

    std::cout << '\n';

    Point p2 { 7, 8 };
    print(p2); // matches print(Point)

    std::cout << '\n';
    
    return 0;
}
在上面的示例中，我们重写了
print()
，使其只有一个类型模板参数 (
T
)，它将匹配任何类型。函数体将成功编译任何具有
first
和
second
成员的类类型。我们通过调用
print()
，先传入一个
Pair
类型的对象，然后再次传入一个
Point
类型的对象来演示这一点。
有一种情况可能具有误导性。考虑以下版本的
print()
：
template <typename T, typename U>
struct Pair // defines a class type named Pair
{
    T first{};
    U second{};
};

template <typename Pair> // defines a type template parameter named Pair (shadows Pair class type)
void print(Pair p)       // this refers to template parameter Pair, not class type Pair
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}
您可能期望此函数仅在调用时传入
Pair
类类型参数时匹配。但是此版本的
print()
在功能上与先前版本相同，其中模板参数名为
T
，并且将匹配
任何
类型。这里的问题是，当我们定义
Pair
作为类型模板参数时，它会遮蔽全局范围内
Pair
名称的其他用法。因此，在函数模板内部，
Pair
指的是模板参数
Pair
，而不是类类型
Pair
。而且由于类型模板参数将匹配任何类型，因此此
Pair
匹配任何参数类型，而不仅仅是类类型
Pair
的参数！
这是一个很好的理由，应该坚持使用简单的模板参数名称，例如
T
、
U
、
N
，因为它们不太可能遮蔽类类型名称。
std::pair
因为处理数据对很常见，C++ 标准库包含一个名为
std::pair
的类模板（在
头文件中），其定义与前一节中具有多个模板类型的
Pair
类模板完全相同。事实上，我们可以将我们开发的
pair
结构体替换为
std::pair
：
#include <iostream>
#include <utility>

template <typename T, typename U>
void print(std::pair<T, U> p)
{
    // the members of std::pair have predefined names `first` and `second`
    std::cout << '[' << p.first << ", " << p.second << ']';
}

int main()
{
    std::pair<int, double> p1{ 1, 2.3 }; // a pair holding an int and a double
    std::pair<double, int> p2{ 4.5, 6 }; // a pair holding a double and an int
    std::pair<int, int> p3{ 7, 8 };      // a pair holding two ints

    print(p2);

    return 0;
}
我们在本课中开发了自己的
Pair
类来展示其工作原理，但在实际代码中，您应该优先使用
std::pair
，而不是自己编写。
在多个文件中使用类模板
就像函数模板一样，类模板通常定义在头文件中，这样它们就可以被需要它们的任何代码文件包含。模板定义和类型定义都免于单定义规则，因此这不会引起问题。
pair.h
#ifndef PAIR_H
#define PAIR_H

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
constexpr T max(Pair<T> p)
{
    return (p.first < p.second ? p.second : p.first);
}

#endif
foo.cpp
#include "pair.h"
#include <iostream>

void foo()
{
    Pair<int> p1{ 1, 2 };
    std::cout << max(p1) << " is larger\n";
}
main.cpp
#include "pair.h"
#include <iostream>

void foo(); // forward declaration for function foo()

int main()
{
    Pair<double> p2 { 3.4, 5.6 };
    std::cout << max(p2) << " is larger\n";

    foo();

    return 0;
}
下一课
13.14
类模板参数推导 (CTAD) 和推导指南
返回目录
上一课
13.12
使用指针和引用进行成员选择