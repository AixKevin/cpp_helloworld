# 18.2 — 迭代器简介

18.2 — 迭代器简介
Alex
2019 年 12 月 17 日，太平洋标准时间上午 10:38
2025 年 2 月 11 日
在编程中，遍历数组（或其他数据结构）是一件非常常见的事情。到目前为止，我们已经介绍了许多不同的方法来实现这一点：使用循环和索引（
for-loops
和
while loops
），使用指针和指针算术，以及使用
range-based for-loops
。
#include <array>
#include <cstddef>
#include <iostream>

int main()
{
    // In C++17, the type of variable arr is deduced to std::array<int, 7>
    // If you get an error compiling this example, see the warning below
    std::array arr{ 0, 1, 2, 3, 4, 5, 6 };
    std::size_t length{ std::size(arr) };

    // while-loop with explicit index
    std::size_t index{ 0 };
    while (index < length)
    {
        std::cout << arr[index] << ' ';
        ++index;
    }
    std::cout << '\n';

    // for-loop with explicit index
    for (index = 0; index < length; ++index)
    {
        std::cout << arr[index] << ' ';
    }
    std::cout << '\n';

    // for-loop with pointer (Note: ptr can't be const, because we increment it)
    for (auto ptr{ &arr[0] }; ptr != (&arr[0] + length); ++ptr)
    {
        std::cout << *ptr << ' ';
    }
    std::cout << '\n';

    // range-based for loop
    for (int i : arr)
    {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    return 0;
}
警告
本课程中的示例使用 C++17 的一个特性，称为
class template argument deduction
，它根据模板变量的初始化器推导模板参数。在上面的示例中，当编译器看到
std::array arr{ 0, 1, 2, 3, 4, 5, 6 };
时，它将推导出我们想要
std::array
arr { 0, 1, 2, 3, 4, 5, 6 };
。
如果您的编译器未启用 C++17，您将收到类似“缺少模板参数在‘arr’之前”的错误。在这种情况下，最好的办法是启用 C++17，按照课程
0.12 -- 配置编译器：选择语言标准
。如果您无法启用，您可以将使用类模板参数推导的行替换为具有显式模板参数的行（例如，将
std::array arr{ 0, 1, 2, 3, 4, 5, 6 };
替换为
std::array
arr { 0, 1, 2, 3, 4, 5, 6 };
）。
如果只使用索引来访问元素，那么使用索引循环会比需要的多写很多代码。它也只适用于容器（例如数组）提供对元素的直接访问（数组可以，但其他一些类型的容器，例如列表，则不能）。
使用指针和指针算术进行循环很冗长，并且对于不了解指针算术规则的读者来说可能会造成混淆。指针算术也只在元素在内存中是连续的情况下才有效（数组是这样，但其他类型的容器，如列表、树和映射则不是）。
致进阶读者
指针（不带指针算术）也可以用来遍历一些非顺序结构。在链表中，每个元素通过指针连接到前一个元素。我们可以通过跟随指针链来遍历列表。
基于范围的 for 循环更有趣一些，因为遍历容器的机制是隐藏的——但它们仍然适用于各种不同的结构（数组、列表、树、映射等……）。它们是如何工作的呢？它们使用迭代器。
迭代器
迭代器
是一个旨在遍历容器（例如数组中的值或字符串中的字符）的对象，并在此过程中提供对每个元素的访问。
容器可以提供不同类型的迭代器。例如，数组容器可以提供一个正向迭代器，以正向顺序遍历数组，以及一个反向迭代器，以反向顺序遍历数组。
一旦创建了适当类型的迭代器，程序员就可以使用迭代器提供的接口来遍历和访问元素，而无需担心正在进行的遍历类型或数据在容器中的存储方式。而且，由于 C++ 迭代器通常使用相同的接口进行遍历（operator++ 移动到下一个元素）和访问（operator* 访问当前元素），因此我们可以使用一致的方法遍历各种不同的容器类型。
指针作为迭代器
最简单的迭代器是指针，它（使用指针算术）适用于按顺序存储在内存中的数据。让我们回顾一个使用指针和指针算术的简单数组遍历。
#include <array>
#include <iostream>

int main()
{
    std::array arr{ 0, 1, 2, 3, 4, 5, 6 };

    auto begin{ &arr[0] };
    // note that this points to one spot beyond the last element
    auto end{ begin + std::size(arr) };

    // for-loop with pointer
    for (auto ptr{ begin }; ptr != end; ++ptr) // ++ to move to next element
    {
        std::cout << *ptr << ' '; // Indirection to get value of current element
    }
    std::cout << '\n';

    return 0;
}
输出
0 1 2 3 4 5 6
在上面，我们定义了两个变量：
begin
（指向容器的开头）和
end
（标记一个结束点）。对于数组，结束标记通常是如果容器再包含一个元素，最后一个元素将位于内存中的位置。
然后指针在
begin
和
end
之间迭代，当前元素可以通过解引用指针来访问。
警告
您可能会尝试使用地址运算符和数组语法来计算结束标记，如下所示：
int* end{ &arr[std::size(arr)] };
但这会导致未定义行为，因为
arr[std::size(arr)]
隐式地解引用了一个超出数组末尾的元素。
相反，使用
int* end{ arr.data() + std::size(arr) }; // data() returns a pointer to the first element
标准库迭代器
迭代是一个如此常见的操作，以至于所有标准库容器都直接支持迭代。我们不再需要自己计算起点和终点，只需通过名为
begin()
和
end()
的成员函数向容器请求起点和终点即可。
#include <array>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // Ask our array for the begin and end points (via the begin and end member functions).
    auto begin{ array.begin() };
    auto end{ array.end() };

    for (auto p{ begin }; p != end; ++p) // ++ to move to next element.
    {
        std::cout << *p << ' '; // Indirection to get value of current element.
    }
    std::cout << '\n';

    return 0;
}
这会打印
1 2 3
iterator
头文件还包含两个可以使用的通用函数（
std::begin
和
std::end
）。
提示
C 风格数组的
std::begin
和
std::end
在 `
` 头文件中定义。
支持迭代器的容器的
std::begin
和
std::end
在这些容器的头文件中定义（例如 `
`、`
`）。
#include <array>    // includes <iterator>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // Use std::begin and std::end to get the begin and end points.
    auto begin{ std::begin(array) };
    auto end{ std::end(array) };

    for (auto p{ begin }; p != end; ++p) // ++ to move to next element
    {
        std::cout << *p << ' '; // Indirection to get value of current element
    }
    std::cout << '\n';

    return 0;
}
这也打印
1 2 3
暂时不用担心迭代器的类型，我们会在后面的章节中重新讨论迭代器。重要的是迭代器会处理遍历容器的细节。我们只需要四样东西：起始点、结束点、`operator++` 来将迭代器移动到下一个元素（或结束），以及 `operator*` 来获取当前元素的值。
迭代器的
operator<
与
operator!=
在第
8.10 -- For 语句
课中，我们提到在循环条件中进行数字比较时，优先使用
operator<
而不是
operator!=
。
for (index = 0; index < length; ++index)
对于迭代器，通常使用
operator!=
来测试迭代器是否已达到结束元素。
for (auto p{ begin }; p != end; ++p)
这是因为某些迭代器类型无法进行关系比较。
operator!=
适用于所有迭代器类型。
返回基于范围的 for 循环
所有具有
begin()
和
end()
成员函数，或者可以与
std::begin()
和
std::end()
一起使用的类型，都可以在基于范围的 for 循环中使用。
#include <array>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // This does exactly the same as the loop we used before.
    for (int i : array)
    {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    return 0;
}
在幕后，基于范围的 for 循环会调用要遍历的类型的
begin()
和
end()
。
std::array
具有
begin
和
end
成员函数，因此我们可以在基于范围的循环中使用它。C 风格的固定大小数组可以使用
std::begin
和
std::end
函数，因此我们也可以用基于范围的循环遍历它们。但是动态 C 风格数组（或退化 C 风格数组）则不行，因为它们没有
std::end
函数（因为类型信息不包含数组的长度）。
您将在以后学习如何向您的类型添加这些函数，以便它们也可以用于基于范围的 for 循环。
基于范围的 for 循环并不是唯一使用迭代器的东西。它们也用于
std::sort
和其他算法中。现在您知道它们是什么了，您会注意到它们在标准库中被大量使用。
迭代器失效（悬空迭代器）
与指针和引用非常相似，如果被迭代的元素改变地址或被销毁，迭代器可能会“悬空”。当这种情况发生时，我们称迭代器已**失效**。访问失效的迭代器会产生未定义行为。
某些修改容器的操作（例如向
std::vector
添加元素）可能会导致容器中的元素更改地址。发生这种情况时，指向这些元素的现有迭代器将失效。良好的 C++ 参考文档应该注明哪些容器操作可能会或将使迭代器失效。例如，请参阅 cppreference 上
std::vector
的
“迭代器失效”部分
。
由于基于范围的 for 循环在幕后使用迭代器，我们必须小心，不要执行任何会使我们正在遍历的容器的迭代器失效的操作。
#include <vector>

int main()
{
    std::vector v { 0, 1, 2, 3 };

    for (auto num : v) // implicitly iterates over v
    {
        if (num % 2 == 0)
            v.push_back(num + 1); // when this invalidates the iterators of v, undefined behavior will result
    }

    return 0;
}
这是迭代器失效的另一个示例
#include <iostream>
#include <vector>

int main()
{
	std::vector v{ 1, 2, 3, 4, 5, 6, 7 };

	auto it{ v.begin() };

	++it; // move to second element
	std::cout << *it << '\n'; // ok: prints 2

	v.erase(it); // erase the element currently being iterated over

	// erase() invalidates iterators to the erased element (and subsequent elements)
	// so iterator "it" is now invalidated

	++it; // undefined behavior
	std::cout << *it << '\n'; // undefined behavior

	return 0;
}
失效的迭代器可以通过为其分配一个有效的迭代器（例如
begin()
、
end()
或返回迭代器的其他函数的返回值）来重新验证。
erase()
函数返回一个指向被擦除元素之后一个元素的迭代器（如果删除了最后一个元素，则返回
end()
）。因此，我们可以这样修复上面的代码：
#include <iostream>
#include <vector>

int main()
{
	std::vector v{ 1, 2, 3, 4, 5, 6, 7 };

	auto it{ v.begin() };

	++it; // move to second element
	std::cout << *it << '\n';

	it = v.erase(it); // erase the element currently being iterated over, set `it` to next element

	std::cout << *it << '\n'; // now ok, prints 3

	return 0;
}
下一课
18.3
标准库算法简介
返回目录
上一课
18.1
使用选择排序对数组进行排序
（鸣谢 nascardriver 对本课程的重大贡献）