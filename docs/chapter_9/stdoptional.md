# 12.15 — std::optional

12.15 — std::optional
Alex
2024 年 3 月 19 日，太平洋夏令时上午 11:44
2025 年 2 月 8 日
在课程
9.4 -- 检测和处理错误
中，我们讨论了函数遇到自身无法合理处理的错误的情况。例如，考虑一个计算并返回值函数
int doIntDivision(int x, int y)
{
    return x / y;
}
如果调用者传入一个语义无效的值（例如
y
=
0
），此函数无法计算返回值（因为除以 0 在数学上是未定义的）。在这种情况下我们该怎么办？由于计算结果的函数不应有副作用，此函数无法合理地自行解决错误。在这种情况下，通常的做法是让函数检测错误，然后将错误传回给调用者，以便以某种适合程序的方式处理。
在之前链接的课程中，我们介绍了两种让函数将错误返回给调用者的方式
让返回 void 的函数返回 bool（表示成功或失败）。
让返回值函数返回一个哨兵值（一个特殊值，不属于函数可能返回的值集合）以指示错误。
作为后者的一个例子，如果用户为
x
传入语义无效的参数，下面的
reciprocal()
函数返回
0.0
（这个值在其他情况下绝不会出现）
#include <iostream>

// The reciprocal of x is 1/x, returns 0.0 if x=0
double reciprocal(double x)
{
    if (x == 0.0) // if x is semantically invalid
       return 0.0; // return 0.0 as a sentinel to indicate an error occurred

    return 1.0 / x;
}

void testReciprocal(double d)
{
     double result { reciprocal(d) };
     std::cout << "The reciprocal of " << d << " is ";
     if (result != 0.0)
         std::cout << result << '\n';
     else
         std::cout << "undefined\n";
}

int main()
{
    testReciprocal(5.0);
    testReciprocal(-4.0);
    testReciprocal(0.0);

    return 0;
}
虽然这是一个相当有吸引力的解决方案，但它有许多潜在的缺点
程序员必须知道函数使用哪个哨兵值来指示错误（并且此值对于使用此方法返回错误的每个函数可能不同）。
同一函数的不同版本可能使用不同的哨兵值。
此方法不适用于所有可能的哨兵值都是有效返回值的函数。
考虑我们上面的
doIntDivision()
函数。如果用户为
y
传入
0
，它能返回什么值？我们不能使用
0
，因为
0
除以任何数都得到
0
作为有效结果。实际上，我们无法返回任何不能自然出现的值。
那我们该怎么办呢？
首先，我们可以选择一些（希望是）不常见的返回值作为我们的哨兵，并用它来指示错误
#include <limits> // for std::numeric_limits

// returns std::numeric_limits<int>::lowest() on failure
int doIntDivision(int x, int y)
{
    if (y == 0)
        return std::numeric_limits<int>::lowest();
    return x / y;
}
std::numeric_limits<T>::lowest()
是一个函数，它返回类型
T
的最小值。它与我们在课程
9.5 -- std::cin 和处理无效输入
中介绍的
std::numeric_limits<T>::max()
函数（返回类型
T
的最大正值）相对应。
在上面的示例中，如果
doIntDivision()
无法继续，我们返回
std::numeric_limits<int>::lowest()
，它将最小值返回给调用者，以指示函数失败。
虽然这大部分情况下都有效，但它有两个缺点
每次调用此函数时，我们都需要测试返回值是否等于
std::numeric_limits<int>::lowest()
以查看它是否失败。这既冗长又丑陋。
它是一个
半谓词问题
的例子：如果用户调用
doIntDivision(std::numeric_limits<int>::lowest(), 1)
，返回结果
std::numeric_limits<int>::lowest()
将模糊不清，无法判断函数是成功还是失败。这可能是也可能不是问题，具体取决于函数的实际使用方式，但这是我们必须担心的另一件事，也是错误可能潜入我们程序的另一种潜在方式。
其次，我们可以放弃使用返回值来返回错误，并使用其他机制（例如异常）。但是，异常有其自身的复杂性和性能成本，并且可能不适用或不受欢迎。对于这样的事情来说，这可能有点大材小用。
第三，我们可以放弃返回单个值，而是返回两个值：一个（类型为
bool
）指示函数是否成功，另一个（所需返回类型）包含实际返回值（如果函数成功）或不确定值（如果函数失败）。这可能是这堆选项中最好的。
在 C++17 之前，选择后者需要您自行实现。虽然 C++ 提供了多种方法来实现这一点，但任何自行实现的方法都不可避免地会导致不一致和错误。
返回
std::optional
C++17 引入了
std::optional
，它是一个类模板类型，实现了一个可选值。也就是说，一个
std::optional<T>
可以包含一个类型为
T
的值，也可以不包含。我们可以使用它来实现上面的第三个选项
#include <iostream>
#include <optional> // for std::optional (C++17)

// Our function now optionally returns an int value
std::optional<int> doIntDivision(int x, int y)
{
    if (y == 0)
        return {}; // or return std::nullopt
    return x / y;
}

int main()
{
    std::optional<int> result1 { doIntDivision(20, 5) };
    if (result1) // if the function returned a value
        std::cout << "Result 1: " << *result1 << '\n'; // get the value
    else
        std::cout << "Result 1: failed\n";

    std::optional<int> result2 { doIntDivision(5, 0) };

    if (result2)
        std::cout << "Result 2: " << *result2 << '\n';
    else
        std::cout << "Result 2: failed\n";

    return 0;
}
这会打印
Result 1: 4
Result 2: failed
使用
std::optional
非常简单。我们可以使用有值或无值的方式构造一个
std::optional<T>
std::optional<int> o1 { 5 };            // initialize with a value
std::optional<int> o2 {};               // initialize with no value
std::optional<int> o3 { std::nullopt }; // initialize with no value
要查看
std::optional
是否有值，我们可以选择以下之一
if (o1.has_value()) // call has_value() to check if o1 has a value
if (o2)             // use implicit conversion to bool to check if o2 has a value
要从
std::optional
获取值，我们可以选择以下之一
std::cout << *o1;             // dereference to get value stored in o1 (undefined behavior if o1 does not have a value)
std::cout << o2.value();      // call value() to get value stored in o2 (throws std::bad_optional_access exception if o2 does not have a value)
std::cout << o3.value_or(42); // call value_or() to get value stored in o3 (or value `42` if o3 doesn't have a value)
请注意，
std::optional
的使用语法与指针基本相同
行为
指针
std::optional
不持有值
初始化/赋值
{}
或
std::nullptr
初始化/赋值
{}
或
std::nullopt
持有值
初始化/赋值一个地址
初始化/赋值一个值
检查是否有值
隐式转换为 bool
隐式转换为 bool 或
has_value()
获取值
解引用
解引用或
value()
然而，从语义上讲，指针和
std::optional
截然不同。
指针具有引用语义，这意味着它引用其他对象，并且赋值会复制指针，而不是对象。如果我们按地址返回指针，则指针会被复制回调用者，而不是指向的对象。这意味着我们不能按地址返回局部对象，因为我们会将该对象的地址复制回调用者，然后对象将被销毁，导致返回的指针悬空。
std::optional
具有值语义，这意味着它实际上包含其值，并且赋值会复制值。如果我们按值返回
std::optional
，则
std::optional
（包括包含的值）会被复制回调用者。这意味着我们可以使用
std::optional
将值从函数返回给调用者。
考虑到这一点，让我们看看我们的示例是如何工作的。我们的
doIntDivision()
现在返回
std::optional<int>
而不是
int
。在函数体内部，如果检测到错误，我们返回
{}
，它隐式返回一个不包含值的
std::optional
。如果有一个值，我们返回该值，它隐式返回一个包含该值的
std::optional
。
在
main()
中，我们使用隐式转换为 bool 来检查返回的
std::optional
是否有值。如果有，我们解引用
std::optional
对象以获取值。如果没有，则执行错误条件。就是这样！
返回
std::optional
的优缺点
返回
std::optional
有许多优点
使用
std::optional
有效地表明函数可能返回值，也可能不返回值。
我们不必记住哪个值作为哨兵返回。
使用
std::optional
的语法方便直观。
返回
std::optional
也有一些缺点
在获取值之前，我们必须确保
std::optional
包含一个值。如果解引用一个不包含值的
std::optional
，会得到未定义行为。
std::optional
不提供传回函数失败原因的信息的方式。
除非您的函数需要返回有关其失败原因的附加信息（以便更好地理解失败，或区分不同类型的失败），否则
std::optional
是可能返回值或失败的函数的绝佳选择。
最佳实践
对于可能失败的函数，返回
std::optional
（而不是哨兵值），除非您的函数需要返回有关其失败原因的附加信息。
相关内容
std::expected
（在 C++23 中引入）旨在处理函数可以返回预期值或意外错误代码的情况。有关更多信息，请参阅
std::expected 参考
。
将
std::optional
用作可选函数参数
在课程
12.11 -- 按地址传递（第二部分）
中，我们讨论了如何使用按地址传递来允许函数接受“可选”参数（即，调用者可以传入
nullptr
表示“无参数”或一个对象）。然而，这种方法的一个缺点是，非空指针参数必须是左值（以便将其地址传递给函数）。
或许不足为奇（考虑到这个名字），
std::optional
是函数接受可选参数的另一种方式（仅用作输入参数）。而不是这样
#include <iostream>

void printIDNumber(const int *id=nullptr)
{
    if (id)
        std::cout << "Your ID number is " << *id << ".\n";
    else
        std::cout << "Your ID number is not known.\n";
}

int main()
{
    printIDNumber(); // we don't know the user's ID yet

    int userid { 34 };
    printIDNumber(&userid); // we know the user's ID now

    return 0;
}
你可以这样做
#include <iostream>
#include <optional>

void printIDNumber(std::optional<const int> id = std::nullopt)
{
    if (id)
        std::cout << "Your ID number is " << *id << ".\n";
    else
        std::cout << "Your ID number is not known.\n";
}

int main()
{
    printIDNumber(); // we don't know the user's ID yet

    int userid { 34 };
    printIDNumber(userid); // we know the user's ID now

    printIDNumber(62); // we can also pass an rvalue
    
    return 0;
}
这种方法有两个优点
它有效地表明该参数是可选的。
我们可以传入右值（因为
std::optional
会进行复制）。
但是，由于
std::optional
会复制其参数，当
T
是复制成本高的类型（如
std::string
）时，这会成为问题。对于普通函数参数，我们通过将参数设置为
const lvalue reference
来解决此问题，这样就不会进行复制。不幸的是，截至 C++23，
std::optional
不支持引用。
因此，我们建议仅当
T
通常按值传递时，才将
std::optional<T>
用作可选参数。否则，请使用
const T*
。
致进阶读者
虽然
std::optional
不直接支持引用，但您可以使用
std::reference_wrapper
（我们在课程
17.5 -- 通过 std::reference_wrapper 实现引用数组
中介绍）来模拟引用。让我们看看使用
std::string
id 和
std::reference_wrapper
时上面的程序是什么样子
#include <functional>  // for std::reference_wrapper
#include <iostream>
#include <optional>
#include <string>

struct Employee
{
    std::string name{}; // expensive to copy
    int id;
};

void printEmployeeID(std::optional<std::reference_wrapper<Employee>> e=std::nullopt)
{
    if (e)
        std::cout << "Your ID number is " << e->get().id << ".\n";
    else
        std::cout << "Your ID number is not known.\n";
}

int main()
{
    printEmployeeID(); // we don't know the Employee yet

    Employee e { "James", 34 };
    printEmployeeID(e); // we know the Employee's ID now

    return 0;
}
为了比较，指针版本
#include <iostream>
#include <string>

struct Employee
{
    std::string name{}; // expensive to copy
    int id;
};

void printEmployeeID(const Employee* e=nullptr)
{
    if (e)
        std::cout << "Your ID number is " << e->id << ".\n";
    else
        std::cout << "Your ID number is not known.\n";
}

int main()
{
    printEmployeeID(); // we don't know the Employee yet

    Employee e { "James", 34 };
    printEmployeeID(&e); // we know the Employee's ID now

    return 0;
}
这两个程序几乎相同。我们认为前者并不比后者更具可读性或可维护性，不值得在程序中引入两个额外的类型。
在许多情况下，函数重载提供了一个更优越的解决方案
#include <iostream>
#include <string>

struct Employee
{
    std::string name{}; // expensive to copy
    int id;
};

void printEmployeeID()
{
    std::cout << "Your ID number is not known.\n";
}

void printEmployeeID(const Employee& e)
{
    std::cout << "Your ID number is " << e.id << ".\n";
}

int main()
{
    printEmployeeID(); // we don't know the Employee yet

    Employee e { "James", 34 };
    printEmployeeID(e); // we know the Employee's ID now

    printEmployeeID( { "Dave", 62 } ); // we can even pass rvalues

    return 0;
}
最佳实践
对于可选返回类型，首选
std::optional
。
对于可选函数参数（如果可能），首选函数重载。否则，当
T
通常按值传递时，对可选参数使用
std::optional<T>
。当
T
复制成本高时，优先使用
const T*
。
下一课
12.x
第 12 章总结和测验
返回目录
上一课
12.14
指针、引用和 const 的类型推断