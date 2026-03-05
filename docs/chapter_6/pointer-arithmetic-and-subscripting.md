# 17.9 — 指针算术和下标

17.9 — 指针算术和下标
Alex
2015 年 8 月 15 日，下午 4:31 PDT
2024 年 8 月 10 日
在课程
16.1 -- 容器和数组简介
中，我们提到数组在内存中是顺序存储的。在本课中，我们将深入探讨数组索引的数学原理。
尽管我们不会在未来的课程中使用索引数学，但本课中涵盖的主题将让您深入了解基于范围的 for 循环是如何实际工作的，并且在我们稍后介绍迭代器时会再次派上用场。
什么是指针算术？
指针算术
是一种特性，它允许我们对指针应用某些整数算术运算符（加法、减法、增量或减量）以生成新的内存地址。
给定某个指针
ptr
，
ptr + 1
返回内存中
下一个对象
的地址（基于所指向的类型）。因此，如果
ptr
是
int*
，并且一个
int
是 4 字节，那么
ptr + 1
将返回
ptr
之后 4 字节的内存地址，而
ptr + 2
将返回
ptr
之后 8 字节的内存地址。
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // assume 4 byte ints

    std::cout << ptr << ' ' << (ptr + 1) << ' ' << (ptr + 2) << '\n';

    return 0;
}
在作者的机器上，这打印出来
00AFFD80 00AFFD84 00AFFD88
请注意，每个内存地址都比前一个大 4 字节。
尽管不太常见，但指针算术也适用于减法。给定某个指针
ptr
，
ptr - 1
返回内存中
上一个对象
的地址（基于所指向的类型）。
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // assume 4 byte ints

    std::cout << ptr << ' ' << (ptr - 1) << ' ' << (ptr - 2) << '\n';

    return 0;
}
在作者的机器上，这打印出来
00AFFD80 00AFFD7C 00AFFD78
在这种情况下，每个内存地址都比前一个少 4 字节。
关键见解
指针算术返回下一个/上一个对象的地址（基于所指向的类型），而不是下一个/上一个地址。
对指针应用增量（
++
）和减量（
--
）运算符分别与指针加法和指针减法做相同的事情，但实际上修改了指针持有的地址。
给定某个 int 值
x
，
++x
是
x = x + 1
的简写。类似地，给定某个指针
ptr
，
++ptr
是
ptr = ptr + 1
的简写，它执行指针算术并将结果赋值回
ptr
。
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // assume 4 byte ints

    std::cout << ptr << '\n';

    ++ptr; // ptr = ptr + 1
    std::cout << ptr << '\n';

    --ptr; // ptr = ptr - 1
    std::cout << ptr << '\n';

    return 0;
}
在作者的机器上，这打印出来
00AFFD80 00AFFD84 00AFFD80
警告
从技术上讲，上述行为是未定义的。根据 C++ 标准，
指针算术仅在指针和结果在同一数组（或超过数组末尾一个位置）内时才定义
。然而，现代 C++ 实现通常不强制执行此规定，并且通常不会阻止您在数组之外使用指针算术。
下标是通过指针算术实现的
在前面的课程 (
17.8 -- C 风格数组退化
) 中，我们注意到
operator[]
可以应用于指针。
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    
    const int* ptr{ arr }; // a normal pointer holding the address of element 0
    std::cout << ptr[2];   // subscript ptr to get element 2, prints 5

    return 0;
}
让我们深入了解这里发生了什么。
事实证明，下标操作 `ptr[n]` 是一种简洁的语法，等同于更冗长的表达式 `*((ptr) + (n))`。您会注意到这只是指针算术，加上一些额外的括号以确保求值顺序正确，以及一个隐式解引用以获取该地址处的对象。
首先，我们用
arr
初始化
ptr
。当
arr
用作初始化器时，它会退化为一个指针，该指针保存索引为 0 的元素的地址。因此，
ptr
现在保存元素 0 的地址。
接下来，我们打印
ptr[2]
。
ptr[2]
等效于
*((ptr) + (2))
，它等效于
*(ptr + 2)
。
ptr + 2
返回比
ptr
晚两个对象的对象的地址，即索引为 2 的元素。然后将该地址处的对象返回给调用者。
让我们看另一个例子
#include <iostream>

int main()
{
    const int arr[] { 3, 2, 1 };

    // First, let's use subscripting to get the address and values of our array elements
    std::cout << &arr[0] << ' ' << &arr[1] << ' ' << &arr[2] << '\n';
    std::cout << arr[0] << ' ' << arr[1] << ' ' << arr[2] << '\n';

    // Now let's do the equivalent using pointer arithmetic
    std::cout << arr<< ' ' << (arr+ 1) << ' ' << (arr+ 2) << '\n';
    std::cout << *arr<< ' ' << *(arr+ 1) << ' ' << *(arr+ 2) << '\n';

    return 0;
}
在作者的机器上，这打印出来
00AFFD80 00AFFD84 00AFFD88
3 2 1
00AFFD80 00AFFD84 00AFFD88
3 2 1
你会注意到 `arr` 存储地址 `00AFFD80`，`(arr + 1)` 返回一个 4 字节后的地址，而 `(arr + 2)` 返回一个 8 字节后的地址。我们可以解引用这些地址来获取这些地址处的元素。
因为数组元素在内存中总是连续的，如果
arr
是指向数组元素 0 的指针，那么
*(arr + n)
将返回数组中的第 n 个元素。
这是数组以 0 为基数而不是 1 为基数的主要原因。它使数学运算更有效率（因为编译器在下标时不必减去 1）！
题外话…
作为一段有趣的趣闻，因为编译器在对指针进行下标操作时会将 `ptr[n]` 转换为 `*((ptr) + (n))`，这意味着我们也可以将指针下标为 `n[ptr]`！编译器会将其转换为 `*((n) + (ptr))`，其行为与 `*((ptr) + (n))` 完全相同。不过，不要这样做，因为它会让人困惑。
指针算术和下标是相对地址
初学数组下标时，很自然地会认为索引代表数组中固定的元素：索引 0 始终是第一个元素，索引 1 始终是第二个元素，等等……
这是一种错觉。数组索引实际上是相对位置。索引之所以看起来固定，是因为我们几乎总是从数组的起始（元素 0）开始索引！
记住，给定某个指针
ptr
，
*(ptr + 1)
和
ptr[1]
都返回内存中的
下一个对象
（基于所指向的类型）。“下一个”是一个相对术语，而不是绝对术语。因此，如果
ptr
指向元素 0，那么
*(ptr + 1)
和
ptr[1]
都将返回元素 1。但如果
ptr
指向元素 3，那么
*(ptr + 1)
和
ptr[1]
都将返回元素 4！
下面的例子演示了这一点
#include <array>
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };
    const int *ptr { arr }; // arr decays into a pointer to element 0

    // Prove that we're pointing at element 0
    std::cout << *ptr << ptr[0] << '\n'; // prints 99
    // Prove that ptr[1] is element 1
    std::cout << *(ptr+1) << ptr[1] << '\n'; // prints 88

    // Now set ptr to point at element 3
    ptr = &arr[3];

    // Prove that we're pointing at element 3
    std::cout << *ptr << ptr[0] << '\n'; // prints 66
    // Prove that ptr[1] is element 4!
    std::cout << *(ptr+1) << ptr[1] << '\n'; // prints 55
 
    return 0;
}
然而，您也会注意到，如果我们不能假设 `ptr[1]` 总是索引为 1 的元素，那么我们的程序会变得更加混乱。因此，我们建议仅在从数组开头（元素 0）索引时使用下标。只有在进行相对定位时才使用指针算术。
最佳实践
当从数组开头（元素 0）开始索引时，倾向于使用下标，这样数组索引与元素对齐。
当从给定元素进行相对定位时，倾向于使用指针算术。
负数索引
在上一课中，我们提到（与标准库容器类不同）C 风格数组的索引可以是无符号整数或有符号整数。这不仅仅是为了方便——实际上可以用负数下标索引 C 风格数组。听起来很奇怪，但它是有道理的。
我们刚刚讲过
*(ptr+1)
返回内存中的
下一个对象
。而
ptr[1]
只是做同样事情的方便语法。
在本课的开头，我们提到 `*(ptr-1)` 返回内存中的*上一个对象*。想猜猜它的下标等效是什么吗？是的，`ptr[-1]`。
#include <array>
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };

    // Set ptr to point at element 3
    const int* ptr { &arr[3] };

    // Prove that we're pointing at element 3
    std::cout << *ptr << ptr[0] << '\n'; // prints 66
    // Prove that ptr[-1] is element 2!
    std::cout << *(ptr-1) << ptr[-1] << '\n'; // prints 77
 
    return 0;
}
指针算术可用于遍历数组
指针算术最常见的用途之一是在没有显式索引的情况下遍历 C 风格数组。下面的示例说明了如何做到这一点
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	const int* begin{ arr };                // begin points to start element
	const int* end{ arr + std::size(arr) }; // end points to one-past-the-end element

	for (; begin != end; ++begin)           // iterate from begin up to (but excluding) end
	{
		std::cout << *begin << ' ';     // dereference our loop variable to get the current element
	}

	return 0;
}
在上面的示例中，我们从 `begin` 指向的元素（在本例中是数组的元素 0）开始遍历。由于 `begin != end`，循环体执行。在循环内部，我们通过 `*begin` 访问当前元素，这只是一个指针解引用。在循环体之后，我们执行 `++begin`，它使用指针算术将 `begin` 递增以指向下一个元素。由于 `begin != end`，循环体再次执行。这会一直持续到 `begin != end` 为 `false`，即 `begin == end` 时。
因此，以上内容打印
9 7 5 3 1
请注意，`end` 设置为数组的末尾后一个位置。让 `end` 保存这个地址是没问题的（只要我们不解引用 `end`，因为该地址处没有有效元素）。我们这样做是因为它使我们的数学和比较尽可能简单（无需在任何地方加或减 1）。
提示
对于指向 C 风格数组元素的指针，指针算术有效，只要结果地址是有效数组元素的地址，或最后一个元素的后一个地址。如果指针算术导致超出这些边界的地址，则它是未定义行为（即使结果未被解引用）。
在之前的课程
17.8 -- C 风格数组退化
中，我们提到数组退化使得重构函数变得困难，因为某些东西适用于未退化的数组，而不适用于退化的数组（例如 `std::size`）。以这种方式遍历数组的一个优点是，我们可以将上面示例的循环部分完全按照原样重构为一个单独的函数，并且它仍然可以工作
#include <iostream>

void printArray(const int* begin, const int* end)
{
	for (; begin != end; ++begin)   // iterate from begin up to (but excluding) end
	{
		std::cout << *begin << ' '; // dereference our loop variable to get the current element
	}
    
	std::cout << '\n';
}

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	const int* begin{ arr };                // begin points to start element
	const int* end{ arr + std::size(arr) }; // end points to one-past-the-end element

	printArray(begin, end);

	return 0;
}
请注意，即使我们从未显式地将数组传递给函数，此程序也能编译并产生正确的结果！而且因为我们没有传递 `arr`，所以我们不必在 `printArray()` 中处理退化的 `arr`。相反，`begin` 和 `end` 包含了遍历数组所需的所有信息。
在未来的课程中（当我们涵盖迭代器和算法时），我们将看到标准库中充满了使用 `begin` 和 `end` 对来定义函数应操作的容器元素的函数。
C 风格数组的基于范围的 for 循环是使用指针算术实现的
考虑以下基于范围的 for 循环
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	for (auto e : arr)         // iterate from `begin` up to (but excluding) `end`
	{
		std::cout << e << ' '; // dereference our loop variable to get the current element
	}

	return 0;
}
如果你查看基于范围的 for 循环的
文档
，你会发现它们通常是这样实现的
{
    auto __begin = begin-expr;
    auto __end = end-expr;

    for ( ; __begin != __end; ++__begin)
    {
        range-declaration = *__begin;
        loop-statement;
    }
}
让我们将前面示例中的基于范围的 for 循环替换为这个实现
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	auto __begin = arr;                // arr is our begin-expr
	auto __end = arr + std::size(arr); // arr + std::size(arr) is our end-expr

	for ( ; __begin != __end; ++__begin)
	{
		auto e = *__begin;         // e is our range-declaration
		std::cout << e << ' ';     // here is our loop-statement
	}

	return 0;
}
请注意这与我们在前一节中编写的示例有多么相似！唯一的区别是我们正在将 `*__begin` 赋值给 `e` 并使用 `e`，而不是直接使用 `*__begin`！
小测验时间
问题 #1
a) 为什么
arr[0]
等同于
*arr
？
显示答案
arr[0]
是
*((arr) + (0))
的简写，它等于
*(arr + 0)
，即
*arr
。
相关内容
在下一课（
17.10 -- C 风格字符串
）中，我们有更多关于指针算术的测验问题。
下一课
17.10
C 风格字符串
返回目录
上一课
17.8
C 风格数组退化