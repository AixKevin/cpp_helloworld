# 16.7 — 数组、循环和符号挑战解决方案

16.7 — 数组、循环和符号挑战解决方案
Alex
2023 年 9 月 11 日，下午 2:34 PDT
2024 年 10 月 19 日
在课程
4.5 -- 无符号整数以及为何要避免使用它们
中，我们提到我们通常倾向于使用有符号值来保存数量，因为无符号值可能会以令人惊讶的方式行为。然而，在课程
16.3 -- std::vector 和无符号长度及下标问题
中，我们讨论了
std::vector
（以及其他容器类）如何使用无符号整型
std::size_t
来表示长度和索引。
这可能导致诸如此类的问题
#include <iostream>
#include <vector>

template <typename T>
void printReverse(const std::vector<T>& arr)
{
    for (std::size_t index{ arr.size() - 1 }; index >= 0; --index) // index is unsigned
    {
        std::cout << arr[index] << ' ';
    }

    std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printReverse(arr);

    return 0;
}
此代码首先反向打印数组
9 1 2 8 3 7 6 4
然后表现出未定义行为。它可能会打印垃圾值，或者导致应用程序崩溃。
这里有两个问题。首先，我们的循环执行条件是`index >= 0`（换句话说，只要`index`是正数），当`index`是无符号数时，这总是为真。因此，循环永远不会终止。
其次，当`index`值为`0`时递减它，它将回绕到一个很大的正值，然后我们在下一次迭代中使用该值来索引数组。这是一个越界索引，会导致未定义行为。如果我们的向量为空，我们也会遇到同样的问题。
虽然有很多方法可以解决这些特定问题，但这类问题是滋生 bug 的温床。
为循环变量使用有符号类型更容易避免此类问题，但它也有自己的挑战。以下是使用有符号索引的上述问题的版本
#include <iostream>
#include <vector>

template <typename T>
void printReverse(const std::vector<T>& arr)
{
    for (int index{ static_cast<int>(arr.size()) - 1}; index >= 0; --index) // index is signed
    {
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';
    }

    std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printReverse(arr);

    return 0;
}
虽然此版本按预期工作，但由于添加了两个`static_cast`，代码也变得杂乱无章。`arr[static_cast
(index)]`尤其难以阅读。在这种情况下，我们以牺牲可读性为代价提高了安全性。
这里是使用带符号索引的另一个例子
#include <iostream>
#include <vector>

// Function template to calculate the average value in a std::vector
template <typename T>
T calculateAverage(const std::vector<T>& arr)
{
    int length{ static_cast<int>(arr.size()) };

    T average{ 0 };
    for (int index{ 0 }; index < length; ++index)
        average += arr[static_cast<std::size_t>(index)];
    average /= length;

    return average;
}

int main()
{
    std::vector testScore1 { 84, 92, 76, 81, 56 };
    std::cout << "The class 1 average is: " << calculateAverage(testScore1) << '\n';

    return 0;
}
我们的代码中充满了静态类型转换，这非常糟糕。
那我们该怎么办呢？这是一个没有理想解决方案的领域。
这里有许多可行的选择，我们将按照我们认为从最差到最好的顺序呈现。你可能会在其他人编写的代码中遇到所有这些情况。
作者注
虽然我们将在 `std::vector` 的上下文中讨论这一点，但所有标准库容器（例如 `std::array`）的工作方式都类似，并且面临相同的挑战。接下来的讨论适用于其中任何一个。
关闭有符号/无符号转换警告
如果您想知道为什么有符号/无符号转换警告通常默认禁用，这个问题是主要原因之一。每次我们使用有符号索引对标准库容器进行下标操作时，都会生成一个有符号转换警告。这会很快用虚假警告填满您的编译日志，淹没可能实际上是合法的警告。
因此，避免处理大量有符号/无符号转换警告的一种方法是简单地将这些警告关闭。
这是最简单的解决方案，但我们不推荐，因为它也会抑制可能导致错误的合法符号转换警告的生成，如果不处理这些警告，可能会导致错误。
使用无符号循环变量
许多开发人员认为，既然标准库数组类型被设计为使用无符号索引，那么我们就应该使用无符号索引！这是一个完全合理的立场。我们只需要格外小心，不要在这样做时遇到有符号/无符号不匹配。如果可能，避免将索引循环变量用于索引以外的任何事情。
如果我们决定采用这种方法，我们应该实际使用哪种无符号类型呢？
在课程
16.3 -- std::vector 和无符号长度及下标问题
中，我们提到标准库容器类定义了嵌套类型别名`size_type`，它是一种用于数组长度和索引的无符号整型。`size()`成员函数返回`size_type`，并且`operator[]`使用`size_type`作为索引，因此使用`size_type`作为索引的类型在技术上是最一致和安全的无符号类型（因为它在所有情况下都有效，即使在`size_type`不是`size_t`的极少数情况下也是如此）。例如：
#include <iostream>
#include <vector>

int main()
{
	std::vector arr { 1, 2, 3, 4, 5 };

	for (std::vector<int>::size_type index { 0 }; index < arr.size(); ++index)
		std::cout << arr[index] << ' ';

	return 0;
}
然而，使用`size_type`有一个主要缺点：因为它是一个嵌套类型，要使用它，我们必须显式地用容器的完整模板化名称作为前缀（这意味着我们必须输入`std::vector
::size_type`而不是仅仅`std::size_type`）。这需要大量的输入，难以阅读，并且根据容器和元素类型的不同而变化。
当在函数模板内部使用时，我们可以使用 `T` 作为模板参数。但是我们还需要在类型前加上 `typename` 关键字
#include <iostream>
#include <vector>

template <typename T>
void printArray(const std::vector<T>& arr)
{
	// typename keyword prefix required for dependent type
	for (typename std::vector<T>::size_type index { 0 }; index < arr.size(); ++index)
		std::cout << arr[index] << ' ';
}

int main()
{
	std::vector arr { 9, 7, 5, 3, 1 };

	printArray(arr);

	return 0;
}
如果你忘记了 `typename` 关键字，你的编译器可能会提醒你添加它。
致进阶读者
任何依赖于包含模板参数的类型的名称都称为**依赖名称**。依赖名称必须以关键字`typename`为前缀才能用作类型。
在上面的例子中，`std::vector
`是一个带有模板参数的类型，所以嵌套类型`std::vector
::size_type`是一个依赖名称，必须以`typename`为前缀才能用作类型。
您偶尔会看到数组类型别名，以使循环更易读
using arrayi = std::vector<int>;
    for (arrayi::size_type index { 0 }; index < arr.size(); ++index)
一个更通用的解决方案是让编译器为我们获取数组类型对象的类型，这样我们就不必显式指定容器类型或模板参数。为此，我们可以使用`decltype`关键字，它返回其参数的类型。
// arr is some non-reference type
    for (decltype(arr)::size_type index { 0 }; index < arr.size(); ++index) // decltype(arr) resolves to std::vector<int>
然而，如果`arr`是一个引用类型（例如通过引用传递的数组），上述方法不起作用。我们需要首先从`arr`中删除引用
template <typename T>
void printArray(const std::vector<T>& arr)
{
	// arr can be a reference or non-reference type
	for (typename std::remove_reference_t<decltype(arr)>::size_type index { 0 }; index < arr.size(); ++index)
		std::cout << arr[index] << ' ';
}
不幸的是，这不再简洁或易于记忆。
由于`size_type`几乎总是`size_t`的类型别名，许多程序员完全跳过使用`size_type`，直接使用更易记忆和输入的`std::size_t`
for (std::size_t index { 0 }; index < arr.size(); ++index)
除非你正在使用自定义分配器（你可能没有），我们认为这是一种合理的方法。
使用有符号循环变量
虽然它使得使用标准库容器类型变得有点困难，但使用有符号循环变量与我们代码其余部分采用的最佳实践（倾向于使用有符号值表示数量）保持一致。我们越能始终如一地应用我们的最佳实践，总体上发生的错误就越少。
如果我们要使用有符号循环变量，我们需要解决三个问题
我们应该使用什么有符号类型？
将数组长度作为有符号值获取
将有符号循环变量转换为无符号索引
我们应该使用什么有符号类型？
这里有三个（有时是四个）好的选择。
除非你正在处理一个非常大的数组，否则使用`int`应该没问题（尤其是在int为4字节的架构上）。`int`是我们不关心类型时用于所有事物的默认有符号整数类型，在这里也没有什么理由要改变。
如果你正在处理非常大的数组，或者如果你想更防御性一点，你可以使用奇怪命名的`std::ptrdiff_t`。这个类型别名通常用作`std::size_t`的有符号对应物。
因为`std::ptrdiff_t`的名字很奇怪，另一种好方法是为索引定义自己的类型别名
using Index = std::ptrdiff_t;

// Sample loop using index
for (Index index{ 0 }; index < static_cast<Index>(arr.size()); ++index)
我们将在下一节展示一个完整的例子。
定义自己的类型别名还有一个潜在的未来好处：如果 C++ 标准库发布了旨在用作有符号索引的类型，那么很容易将 `Index` 修改为该类型的别名，或者找到/替换 `Index` 为该类型的名称。
在您可以从初始化器派生循环变量类型的情况下，您可以使用 `auto` 让编译器推断类型
for (auto index{ static_cast<std::ptrdiff_t>(arr.size())-1 }; index >= 0; --index)
在 C++23 中，Z 后缀可用于定义一个类型字面量，该类型是 `std::size_t` 的有符号对应物（可能是 `std::ptrdiff_t`）。
for (auto index{ 0Z }; index < static_cast<std::ptrdiff_t>(arr.size()); ++index)
获取数组的有符号长度
在 C++20 之前，最好的选择是将 `size()` 成员函数或 `std::size()` 的返回值 `static_cast` 为有符号类型。
#include <iostream>
#include <vector>

using Index = std::ptrdiff_t;

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    for (auto index{ static_cast<Index>(arr.size())-1 }; index >= 0; --index)
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';

    return 0;
}
这样，`arr.size()` 返回的无符号值将被转换为有符号类型，因此我们的比较运算符将具有两个有符号操作数。而且由于有符号索引在变为负数时不会溢出，所以我们不会遇到使用无符号索引时遇到的回绕问题。
这种方法的缺点是它会使我们的循环变得杂乱，难以阅读。我们可以通过将长度移出循环来解决这个问题
#include <iostream>
#include <vector>

using Index = std::ptrdiff_t;

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    auto length{ static_cast<Index>(arr.size()) }; 
    for (auto index{ length-1 }; index >= 0; --index)
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';

    return 0;
}
在 C++20 中，使用 `std::ssize()`。
如果您想了解更多 C++ 设计者现在认为有符号索引是正确方向的证据，请考虑 C++20 中引入的 `std::ssize()`。此函数将数组类型的大小作为有符号类型（可能是 `ptrdiff_t`）返回。
#include <iostream>
#include <vector>

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    for (auto index{ std::ssize(arr)-1 }; index >= 0; --index) // std::ssize introduced in C++20
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';

    return 0;
}
将有符号循环变量转换为无符号索引
一旦我们有了有符号循环变量，每当我们尝试将该有符号循环变量用作索引时，我们就会遇到隐式符号转换警告。因此，我们需要某种方法将有符号循环变量转换为无符号值，无论我们打算将其用作索引。
显而易见的选择是将我们的有符号循环变量静态转换为无符号索引。我们在前面的例子中展示了这一点。不幸的是，我们需要在所有数组下标操作中都这样做，这使得我们的数组索引难以阅读。
使用带短名称的转换函数
#include <iostream>
#include <type_traits> // for std::is_integral and std::is_enum
#include <vector>

using Index = std::ptrdiff_t;

// Helper function to convert `value` into an object of type std::size_t
// UZ is the suffix for literals of type std::size_t.
template <typename T>
constexpr std::size_t toUZ(T value)
{
    // make sure T is an integral type
    static_assert(std::is_integral<T>() || std::is_enum<T>());
    
    return static_cast<std::size_t>(value);
}

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    auto length { static_cast<Index>(arr.size()) };  // in C++20, prefer std::ssize()
    for (auto index{ length-1 }; index >= 0; --index)
        std::cout << arr[toUZ(index)] << ' '; // use toUZ() to avoid sign conversion warning

    return 0;
}
在上述示例中，我们创建了一个名为 `toUZ()` 的函数，旨在将整型值转换为 `std::size_t` 类型的值。这使得我们可以将数组索引为 `arr[toUZ(index)]`，这相当易读。
使用自定义视图
在之前的课程中，我们讨论了 `std::string` 如何拥有一个字符串，而 `std::string_view` 如何是其他地方存在的字符串的视图。`std::string_view` 的一个巧妙之处在于它可以查看不同类型的字符串（C 风格字符串字面量、`std::string` 和其他 `std::string_view`），但为我们提供了统一的接口。
虽然我们无法修改标准库容器以接受有符号整数索引，但我们可以创建自己的自定义视图类来“查看”标准库容器类。通过这样做，我们可以定义自己的接口，使其按照我们希望的方式工作。
在下面的例子中，我们定义了一个自定义视图类，它可以查看任何支持索引的标准库容器。我们的接口将做两件事：
允许我们使用带有符号整型类型的`operator[]`访问元素。
获取容器的长度作为有符号整型（因为`std::ssize()`只在 C++20 中可用）。
这使用了运算符重载（我们在课程
13.5 -- I/O 运算符重载简介
中简要介绍过）来实现`operator[]`。您不需要知道`SignedArrayView`是如何实现的才能使用它。
SignedArrayView.h
#ifndef SIGNED_ARRAY_VIEW_H
#define SIGNED_ARRAY_VIEW_H

#include <cstddef> // for std::size_t and std::ptrdiff_t

// SignedArrayView provides a view into a container that supports indexing
// allowing us to work with these types using signed indices
template <typename T>
class SignedArrayView // requires C++17
{
private:
    T& m_array;

public:
    using Index = std::ptrdiff_t;

    SignedArrayView(T& array)
        : m_array{ array } {}

    // Overload operator[] to take a signed index
    constexpr auto& operator[](Index index) { return m_array[static_cast<typename T::size_type>(index)]; }
    constexpr const auto& operator[](Index index) const { return m_array[static_cast<typename T::size_type>(index)]; }
    constexpr auto ssize() const { return static_cast<Index>(m_array.size()); }
};

#endif
main.cpp
#include <iostream>
#include <vector>
#include "SignedArrayView.h"

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };
    SignedArrayView sarr{ arr }; // Create a signed view of our std::vector

    for (auto index{ sarr.ssize() - 1 }; index >= 0; --index)
        std::cout << sarr[index] << ' '; // index using a signed type

    return 0;
}
转而索引底层 C 风格数组
在课程
16.3 -- std::vector 和无符号长度及下标问题
中，我们指出，除了索引标准库容器之外，我们还可以调用`data()`成员函数并转而索引它。由于`data()`将数组数据作为 C 风格数组返回，而 C 风格数组允许使用有符号和无符号值进行索引，这避免了符号转换问题。
int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    auto length { static_cast<Index>(arr.size()) };  // in C++20, prefer std::ssize()
    for (auto index{ length - 1 }; index >= 0; --index)
        std::cout << arr.data()[index] << ' ';       // use data() to avoid sign conversion warning

    return 0;
}
我们认为这种方法是索引选项中最好的。
我们可以使用有符号循环变量和索引。
我们不需要定义任何自定义类型或类型别名。
使用`data()`对可读性的影响不大。
在优化后的代码中，应该没有性能损失。
唯一明智的选择：完全避免索引！
上面提出的所有选项都有其自身的缺点，因此很难推荐一种方法优于另一种。然而，有一种选择比其他选择明智得多：完全避免使用整数值进行索引。
C++ 提供了几种不使用索引遍历数组的方法。如果我们没有索引，那么我们就不会遇到所有这些有符号/无符号转换问题。
两种不使用索引的常见数组遍历方法包括基于范围的 for 循环和迭代器。
相关内容
我们在下一课中讨论基于范围的 for 循环（
16.8 -- 基于范围的 for 循环 (for-each)
）。
我们将在即将到来的课程中介绍迭代器
18.2 -- 迭代器简介
。
如果您只使用索引变量来遍历数组，那么请优先选择不使用索引的方法。
最佳实践
尽可能避免使用整型值进行数组索引。
下一课
16.8
基于范围的 for 循环 (for-each)
返回目录
上一课
16.6
数组和循环