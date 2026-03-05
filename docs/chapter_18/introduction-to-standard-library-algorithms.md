# 18.3 — 标准库算法介绍

18.3 — 标准库算法介绍
nascardriver
2020年1月3日，太平洋标准时间上午5:04
2024年9月4日
新手程序员通常会花费大量时间编写自定义循环来执行相对简单的任务，例如对数组进行排序、计数或搜索。这些循环可能会出现问题，无论是出错的容易程度，还是整体可维护性，因为循环可能难以理解。
因为搜索、计数和排序是如此常见的操作，C++ 标准库提供了一系列函数，只需几行代码即可完成这些任务。此外，这些标准库函数经过预先测试、效率高、适用于各种不同的容器类型，并且许多支持并行化（能够将多个 CPU 线程用于同一任务以更快地完成任务）。
算法库中提供的功能通常分为以下三类：
检查器
-- 用于查看（但不修改）容器中的数据。示例包括搜索和计数。
修改器
-- 用于修改容器中的数据。示例包括排序和混洗。
辅助器
-- 用于根据数据成员的值生成结果。示例包括用于乘以值的对象，或用于确定元素对应按什么顺序排序的对象。
这些算法存在于
算法
库中。在本课中，我们将探讨一些更常见的算法 -- 但还有更多，我们鼓励您阅读链接的参考资料以查看所有可用内容！
注意：所有这些都使用了迭代器，因此如果您不熟悉基本迭代器，请回顾第
18.2 课 -- 迭代器介绍
。
使用 std::find 按值查找元素
std::find
搜索容器中值的第一次出现。
std::find
接受 3 个参数：指向序列中起始元素的迭代器、指向序列中结束元素的迭代器以及要搜索的值。如果找到元素，它将返回指向该元素的迭代器；如果未找到元素，则返回容器的末尾迭代器。
例如
#include <algorithm>
#include <array>
#include <iostream>

int main()
{
    std::array arr{ 13, 90, 99, 5, 40, 80 };

    std::cout << "Enter a value to search for and replace with: ";
    int search{};
    int replace{};
    std::cin >> search >> replace;

    // Input validation omitted

    // std::find returns an iterator pointing to the found element (or the end of the container)
    // we'll store it in a variable, using type inference to deduce the type of
    // the iterator (since we don't care)
    auto found{ std::find(arr.begin(), arr.end(), search) };

    // Algorithms that don't find what they were looking for return the end iterator.
    // We can access it by using the end() member function.
    if (found == arr.end())
    {
        std::cout << "Could not find " << search << '\n';
    }
    else
    {
        // Override the found element.
        *found = replace;
    }

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
找到元素时的运行示例
Enter a value to search for and replace with: 5 234
13 90 99 234 40 80
未找到元素时的运行示例
Enter a value to search for and replace with: 0 234
Could not find 0
13 90 99 5 40 80
使用 std::find_if 查找符合某些条件的元素
有时我们想查看容器中是否存在符合某个条件（例如，包含特定子字符串的字符串）而不是精确值的值。在这种情况下，
std::find_if
是完美的。
std::find_if
函数的工作方式类似于
std::find
，但不是传入要搜索的特定值，而是传入一个可调用对象，例如函数指针（或 lambda，我们稍后会介绍）。对于遍历的每个元素，
std::find_if
将调用此函数（将元素作为参数传递给函数），如果找到匹配项，函数可以返回
true
，否则返回
false
。
这是一个使用
std::find_if
检查任何元素是否包含子字符串“nut”的示例
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

// Our function will return true if the element matches
bool containsNut(std::string_view str)
{
    // std::string_view::find returns std::string_view::npos if it doesn't find
    // the substring. Otherwise it returns the index where the substring occurs
    // in str.
    return str.find("nut") != std::string_view::npos;
}

int main()
{
    std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

    // Scan our array to see if any elements contain the "nut" substring
    auto found{ std::find_if(arr.begin(), arr.end(), containsNut) };

    if (found == arr.end())
    {
        std::cout << "No nuts\n";
    }
    else
    {
        std::cout << "Found " << *found << '\n';
    }

    return 0;
}
输出
Found walnut
如果您手动编写上述示例，您至少需要三个循环（一个循环遍历数组，两个用于匹配子字符串）。标准库函数允许我们仅用几行代码完成相同的任务！
使用 std::count 和 std::count_if 计算出现次数
std::count
和
std::count_if
搜索元素的所有出现次数或满足条件的元素。
在以下示例中，我们将计算有多少元素包含子字符串“nut”
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

bool containsNut(std::string_view str)
{
	return str.find("nut") != std::string_view::npos;
}

int main()
{
	std::array<std::string_view, 5> arr{ "apple", "banana", "walnut", "lemon", "peanut" };

	auto nuts{ std::count_if(arr.begin(), arr.end(), containsNut) };

	std::cout << "Counted " << nuts << " nut(s)\n";

	return 0;
}
输出
Counted 2 nut(s)
使用 std::sort 进行自定义排序
我们之前使用
std::sort
按升序排序数组，但 std::sort 的功能远不止于此。
std::sort
有一个版本，它将一个函数作为其第三个参数，允许我们根据需要进行排序。该函数接受两个参数进行比较，如果第一个参数应排在第二个参数之前，则返回 true。默认情况下，
std::sort
以升序排序元素。
让我们使用
std::sort
和名为
greater
的自定义比较函数以逆序排序数组
#include <algorithm>
#include <array>
#include <iostream>

bool greater(int a, int b)
{
    // Order @a before @b if @a is greater than @b.
    return (a > b);
}

int main()
{
    std::array arr{ 13, 90, 99, 5, 40, 80 };

    // Pass greater to std::sort
    std::sort(arr.begin(), arr.end(), greater);

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
输出
99 90 80 40 13 5
再一次，我们不必编写自己的自定义循环函数，只需几行代码即可根据需要对数组进行排序！
我们的
greater
函数需要 2 个参数，但我们没有传递任何参数，那么它们从何而来？当我们使用没有括号 () 的函数时，它只是一个函数指针，而不是一个调用。您可能还记得我们尝试在没有括号的情况下打印函数时
std::cout
打印“1”的情况。
std::sort
使用此指针并使用数组的任意 2 个元素调用实际的
greater
函数。我们不知道
greater
将用哪些元素调用，因为
std::sort
在底层使用的排序算法没有定义。我们将在后面的章节中详细讨论函数指针。
提示
因为降序排序非常常见，C++ 也为此提供了一个自定义类型（名为
std::greater
）（它是
functional
头文件的一部分）。在上面的示例中，我们可以替换
std::sort(arr.begin(), arr.end(), greater); // call our custom greater function
为
std::sort(arr.begin(), arr.end(), std::greater{}); // use the standard library greater comparison
  // Before C++17, we had to specify the element type when we create std::greater
  std::sort(arr.begin(), arr.end(), std::greater<int>{}); // use the standard library greater comparison
请注意，
std::greater{}
需要花括号，因为它不是可调用函数。它是一个类型，为了使用它，我们需要实例化该类型的一个对象。花括号实例化该类型的一个匿名对象（然后将其作为参数传递给 std::sort）。
致进阶读者
为了进一步解释
std::sort
如何使用比较函数，我们必须回到第
18.1 课 -- 使用选择排序对数组进行排序
中选择排序示例的修改版本。
#include <iostream>
#include <iterator>
#include <utility>

void sort(int* begin, int* end)
{
    for (auto startElement{ begin }; startElement != end-1; ++startElement)
    {
        auto smallestElement{ startElement };

        // std::next returns a pointer to the next element, just like (startElement + 1) would.
        for (auto currentElement{ std::next(startElement) }; currentElement != end; ++currentElement)
        {
            if (*currentElement < *smallestElement)
            {
                smallestElement = currentElement;
            }
        }

        std::swap(*startElement, *smallestElement);
    }
}

int main()
{
    int array[]{ 2, 1, 9, 4, 5 };

    sort(std::begin(array), std::end(array));

    for (auto i : array)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
到目前为止，这并没有什么新意，并且
sort
总是从低到高排序元素。要添加比较函数，我们必须使用一个新类型
std::function
来存储一个接受 2 个 int 参数并返回 bool 的函数。现在将此类型视为魔法，我们将在
第 20 章
中解释它。
void sort(int* begin, int* end, std::function<bool(int, int)> compare)
我们现在可以将像
greater
这样的比较函数传递给
sort
，但是
sort
如何使用它呢？我们只需要替换行
if (*currentElement < *smallestElement)
为
if (compare(*currentElement, *smallestElement))
现在
sort
的调用者可以选择如何比较两个元素。
#include <functional> // std::function
#include <iostream>
#include <iterator>
#include <utility>

// sort accepts a comparison function
void sort(int* begin, int* end, std::function<bool(int, int)> compare)
{
    for (auto startElement{ begin }; startElement != end-1; ++startElement)
    {
        auto smallestElement{ startElement };

        for (auto currentElement{ std::next(startElement) }; currentElement != end; ++currentElement)
        {
            // the comparison function is used to check if the current element should be ordered
            // before the currently "smallest" element.
            if (compare(*currentElement, *smallestElement))
            {
                smallestElement = currentElement;
            }
        }

        std::swap(*startElement, *smallestElement);
    }
}

int main()
{
    int array[]{ 2, 1, 9, 4, 5 };

    // use std::greater to sort in descending order
    // (We have to use the global namespace selector to prevent a collision
    // between our sort function and std::sort.)
    ::sort(std::begin(array), std::end(array), std::greater{});

    for (auto i : array)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
使用 std::for_each 对容器的所有元素执行操作
std::for_each
接受一个列表作为输入，并对每个元素应用一个自定义函数。当我们想对列表中的每个元素执行相同的操作时，这很有用。
这是一个使用
std::for_each
将数组中的所有数字加倍的示例
#include <algorithm>
#include <array>
#include <iostream>

void doubleNumber(int& i)
{
    i *= 2;
}

int main()
{
    std::array arr{ 1, 2, 3, 4 };

    std::for_each(arr.begin(), arr.end(), doubleNumber);

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
输出
2 4 6 8
对于新开发人员来说，这通常看起来是最不必要的算法，因为使用基于范围的 for 循环的等效代码更短且更容易。但是
std::for_each
也有好处。让我们比较
std::for_each
与基于范围的 for 循环。
std::ranges::for_each(arr, doubleNumber); // Since C++20, we don't have to use begin() and end().
// std::for_each(arr.begin(), arr.end(), doubleNumber); // Before C++20

for (auto& i : arr)
{
    doubleNumber(i);
}
使用
std::for_each
，我们的意图很明确。对
arr
的每个元素调用
doubleNumber
。在基于范围的 for 循环中，我们必须添加一个新变量
i
。这导致程序员在疲惫或不专心时可能犯几个错误。首先，如果我们不使用
auto
，可能会发生隐式转换。我们可能会忘记引用符 &，
doubleNumber
将不会影响数组。我们可能会不小心将除了
i
之外的变量传递给
doubleNumber
。这些错误不会在使用
std::for_each
时发生。
此外，
std::for_each
可以跳过容器开头或结尾的元素，例如跳过
arr
的第一个元素，可以使用
std::next
将 begin 前进到下一个元素。
std::for_each(std::next(arr.begin()), arr.end(), doubleNumber);
// Now arr is [1, 4, 6, 8]. The first element wasn't doubled.
这对于基于范围的 for 循环是不可能的。
与许多算法一样，
std::for_each
可以并行化以实现更快的处理，使其比基于范围的 for 循环更适合大型项目和大数据。
性能和执行顺序
算法库中的许多算法都会对它们的执行方式做出某种保证。通常，这些是性能保证，或关于它们执行顺序的保证。例如，
std::for_each
保证每个元素只访问一次，并且元素将以向前顺序访问。
虽然大多数算法都提供某种性能保证，但提供执行顺序保证的算法较少。对于此类算法，我们需要注意不要对元素的访问或处理顺序做出假设。
例如，如果我们使用标准库算法将第一个值乘以 1，第二个值乘以 2，第三个值乘以 3，依此类推……我们希望避免使用任何不保证向前顺序执行的算法！
以下算法保证顺序执行：
std::for_each
、
std::copy
、
std::copy_backward
、
std::move
和
std::move_backward
。许多其他算法（特别是那些使用前向迭代器的算法）由于前向迭代器要求而隐式地是顺序的。
最佳实践
在使用特定算法之前，请确保性能和执行顺序保证适用于您的特定用例。
C++20 中的范围
不得不显式地将
arr.begin()
和
arr.end()
传递给每个算法有点烦人。但不用担心 -- C++20 添加了
范围
，它允许我们简单地传递
arr
。这将使我们的代码更短、更易读。
总结
算法库拥有大量有用的功能，可以使您的代码更简单、更健壮。本课只涵盖了很小一部分，但由于大多数这些函数的工作方式非常相似，一旦您了解了少数几个的工作方式，您就可以使用它们中的大多数。
题外话…
这个视频
很好地简洁地解释了库中的各种算法。
最佳实践
优先使用算法库中的函数，而不是编写自己的功能来做同样的事情。
下一课
18.4
测量代码执行时间
返回目录
上一课
18.2
迭代器介绍