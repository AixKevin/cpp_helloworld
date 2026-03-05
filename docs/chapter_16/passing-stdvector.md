# 16.4 — 传递 std::vector

16.4 — 传递 std::vector
Alex
2023 年 9 月 11 日下午 2:28 PDT
2024 年 3 月 21 日
类型为
std::vector
的对象可以像其他任何对象一样传递给函数。这意味着如果我们通过值传递
std::vector
，会进行昂贵的复制。因此，我们通常通过（const）引用传递
std::vector
以避免此类复制。
对于
std::vector
，元素类型是对象类型信息的一部分。因此，当我们使用
std::vector
作为函数参数时，我们必须显式指定元素类型
#include <iostream>
#include <vector>

void passByRef(const std::vector<int>& arr) // we must explicitly specify <int> here
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes);

    return 0;
}
传递不同元素类型的
std::vector
因为我们的
passByRef()
函数期望一个
std::vector<int>
，所以我们无法传递具有不同元素类型的向量
#include <iostream>
#include <vector>

void passByRef(const std::vector<int>& arr)
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes);  // ok: this is a std::vector<int>

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl); // compile error: std::vector<double> is not convertible to std::vector<int>

    return 0;
}
在 C++17 或更高版本中，您可能会尝试使用 CTAD 来解决此问题
#include <iostream>
#include <vector>

void passByRef(const std::vector& arr) // compile error: CTAD can't be used to infer function parameters
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 }; // okay: use CTAD to infer std::vector<int>
    passByRef(primes);

    return 0;
}
尽管 CTAD 在定义向量时可以通过初始化器推断其元素类型，但 CTAD（目前）不适用于函数参数。
我们之前遇到过这类问题，即重载的函数仅在参数类型上有所不同。这是一个使用函数模板的绝佳场景！我们可以创建一个函数模板，将元素类型参数化，然后 C++ 将使用该函数模板来实例化具有实际类型的函数。
相关内容
我们在第
11.6 课 -- 函数模板
中介绍了函数模板。
我们可以创建一个使用相同模板参数声明的函数模板
#include <iostream>
#include <vector>

template <typename T>
void passByRef(const std::vector<T>& arr)
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // ok: compiler will instantiate passByRef(const std::vector<int>&)

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl);    // ok: compiler will instantiate passByRef(const std::vector<double>&)

    return 0;
}
在上面的示例中，我们创建了一个名为
passByRef()
的函数模板，其参数类型为
const std::vector<T>&
。
T
在上一行的模板参数声明中定义：
template <typename T
。
T
是一个标准类型模板参数，允许调用者指定元素类型。
因此，当我们从
main()
调用
passByRef(primes)
（其中
primes
定义为
std::vector<int>
）时，编译器将实例化并调用
void passByRef(const std::vector<int>& arr)
。
当我们从
main()
调用
passByRef(dbl)
（其中
dbl
定义为
std::vector<double>
）时，编译器将实例化并调用
void passByRef(const std::vector<double>& arr)
。
因此，我们创建了一个函数模板，它可以实例化函数来处理任何元素类型和长度的
std::vector
参数！
使用通用模板或简写函数模板传递
std::vector
我们还可以创建一个可以接受任何类型对象的函数模板
#include <iostream>
#include <vector>

template <typename T>
void passByRef(const T& arr) // will accept any type of object that has an overloaded operator[]
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // ok: compiler will instantiate passByRef(const std::vector<int>&)

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl);    // ok: compiler will instantiate passByRef(const std::vector<double>&)

    return 0;
}
在 C++20 中，我们可以使用简写函数模板（通过
auto
参数）来做同样的事情
#include <iostream>
#include <vector>

void passByRef(const auto& arr) // abbreviated function template
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // ok: compiler will instantiate passByRef(const std::vector<int>&)

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl);    // ok: compiler will instantiate passByRef(const std::vector<double>&)

    return 0;
}
这两者都将接受任何可以编译的类型的参数。这在编写我们可能希望对不仅仅是
std::vector
进行操作的函数时是可取的。例如，上述函数也适用于
std::array
、
std::string
或我们甚至可能没有考虑过的其他类型。
这种方法的潜在缺点是，如果函数传递了一个可以编译但语义上没有意义的对象，它可能会导致错误。
断言数组长度
考虑以下模板函数，它类似于上面介绍的那个
#include <iostream>
#include <vector>

template <typename T>
void printElement3(const std::vector<T>& arr)
{
    std::cout << arr[3] << '\n';
}

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };
    printElement3(arr);

    return 0;
}
虽然
printElement3(arr)
在这种情况下工作正常，但这个程序中潜伏着一个潜在的错误，等待粗心的程序员。看到了吗？
上述程序打印索引为 3 的数组元素的值。只要数组有索引为 3 的有效元素，这都没问题。但是，编译器会愉快地让您传入索引 3 超出范围的数组。例如
#include <iostream>
#include <vector>

template <typename T>
void printElement3(const std::vector<T>& arr)
{
    std::cout << arr[3] << '\n';
}

int main()
{
    std::vector arr{ 9, 7 }; // a 2-element array (valid indexes 0 and 1)
    printElement3(arr);

    return 0;
}
这会导致未定义行为。
这里的一个选项是断言
arr.size()
，这将在调试构建配置中运行时捕获此类错误。因为
std::vector::size()
是一个非 constexpr 函数，所以我们只能在这里进行运行时断言。
提示
更好的选择是在需要断言数组长度的情况下避免使用
std::vector
。使用支持
constexpr
数组的类型（例如
std::array
）可能是一个更好的选择，因为您可以对 constexpr 数组的长度进行
static_assert
。我们将在未来的课程
17.3 -- 传递和返回 std::array
中介绍这一点。
最好的选择是避免编写依赖用户传入具有最小长度的向量的函数。
小测验时间
问题 #1
编写一个函数，它接受两个参数：一个
std::vector
和一个索引。如果索引超出范围，则打印错误。如果索引在范围内，则打印元素的值。
以下示例程序应该可以编译
#include <iostream>
#include <vector>

// Write your printElement function here

int main()
{
    std::vector v1 { 0, 1, 2, 3, 4 };
    printElement(v1, 2);
    printElement(v1, 5);

    std::vector v2 { 1.1, 2.2, 3.3 };
    printElement(v2, 0);
    printElement(v2, -1);

    return 0;
}
并产生以下结果
The element has value 2
Invalid index
The element has value 1.1
Invalid index
显示答案
#include <iostream>
#include <vector>

// index needs to be an int, not a std::size_t, otherwise we won't be able to detect if the user passes in a negative index
template <typename T>
void printElement(const std::vector<T>& arr, int index)
{
    if (index < 0 || index >= static_cast<int>(arr.size())) // In C++20, could use std::ssize(arr) to avoid the cast
        std::cout << "Invalid index\n";
    else
        std::cout << "The element has value " << arr[static_cast<std::size_t>(index)] << '\n';  
}

int main()
{
    std::vector v1 { 0, 1, 2, 3, 4 };
    printElement(v1, 2);
    printElement(v1, 5);

    std::vector v2 { 1.1, 2.2, 3.3 };
    printElement(v2, 0);
    printElement(v2, -1);

    return 0;
}
下一课
16.5
返回 std::vector，以及移动语义的介绍
返回目录
上一课
16.3
std::vector 和无符号长度及下标问题