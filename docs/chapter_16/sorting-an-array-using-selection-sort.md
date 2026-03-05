# 18.1 — 使用选择排序对数组进行排序

18.1 — 使用选择排序对数组进行排序
Alex
2007年7月3日，太平洋时间下午1:47
2023年9月11日
排序的用途
对数组进行排序是将数组中的所有元素按特定顺序排列的过程。在许多不同情况下，对数组进行排序都可能很有用。例如，您的电子邮件程序通常按接收时间显示电子邮件，因为最近的电子邮件通常被认为更相关。当您查看联系人列表时，姓名通常按字母顺序排列，因为这样更容易找到您要查找的姓名。这两种呈现方式都涉及在呈现之前对数据进行排序。
对数组进行排序可以使数组搜索更高效，不仅对人类，对计算机也是如此。例如，考虑我们想知道一个姓名是否出现在姓名列表中的情况。为了查看一个姓名是否在列表中，我们必须检查数组中的每个元素以查看该姓名是否出现。对于包含许多元素的数组，搜索所有元素可能代价高昂。
但是，现在假设我们的姓名数组已按字母顺序排序。在这种情况下，我们只需搜索到遇到一个按字母顺序大于我们要查找的姓名为止。此时，如果我们还没有找到该姓名，我们就知道它不存在于数组的其余部分，因为我们尚未查看的所有姓名都保证按字母顺序更大！
事实证明，甚至有更好的算法来搜索已排序的数组。使用一种简单的算法，我们可以使用仅仅20次比较来搜索包含1,000,000个元素的已排序数组！当然，缺点是，对数组进行排序相对而言代价高昂，而且通常不值得对数组进行排序以加快搜索速度，除非您要多次搜索它。
在某些情况下，对数组进行排序可以使搜索变得不必要。考虑另一个例子，我们想找到最好的考试成绩。如果数组未排序，我们必须遍历数组中的每个元素才能找到最大的考试成绩。如果列表已排序，最好的考试成绩将位于第一个或最后一个位置（取决于我们是按升序还是降序排序），因此我们根本不需要搜索！
排序原理
排序通常通过重复比较成对的数组元素，并在它们满足某些预定义条件时交换它们来执行。这些元素比较的顺序因所使用的排序算法而异。条件取决于列表将如何排序（例如，按升序或降序）。
要交换两个元素，我们可以使用 C++ 标准库中的 `std::swap()` 函数，该函数定义在 `utility` 头文件中。
#include <iostream>
#include <utility>

int main()
{
    int x{ 2 };
    int y{ 4 };
    std::cout << "Before swap: x = " << x << ", y = " << y << '\n';
    std::swap(x, y); // swap the values of x and y
    std::cout << "After swap:  x = " << x << ", y = " << y << '\n';

    return 0;
}
这个程序打印
Before swap: x = 2, y = 4
After swap:  x = 4, y = 2
请注意，交换后，x 和 y 的值已经互换！
选择排序
有许多方法可以对数组进行排序。选择排序可能是最容易理解的排序，这使得它成为教学的好选择，尽管它是较慢的排序之一。
选择排序执行以下步骤，将数组从小到大排序：
从数组索引 0 开始，搜索整个数组以找到最小值。
将数组中找到的最小值与索引 0 处的值交换。
从下一个索引开始重复步骤 1 和 2。
换句话说，我们将找到数组中最小的元素，并将其交换到第一个位置。然后我们将找到下一个最小的元素，并将其交换到第二个位置。这个过程将重复，直到我们用完元素。
这是一个算法作用于 5 个元素的示例。让我们从一个示例数组开始：
{ 30, 50, 20, 10, 40 }
首先，我们从索引 0 开始，找到最小的元素
{ 30, 50, 20,
10
, 40 }
然后我们将其与索引 0 处的元素交换
{
10
, 50, 20,
30
, 40 }
现在第一个元素已排序，我们可以忽略它。现在，我们从索引 1 开始，找到最小的元素
{
10
, 50,
20
, 30, 40 }
并将其与索引 1 中的元素交换
{
10
,
20
,
50
, 30, 40 }
现在我们可以忽略前两个元素。从索引 2 开始找到最小的元素
{
10
,
20
, 50,
30
, 40 }
并将其与索引 2 中的元素交换
{
10
,
20
,
30
,
50
, 40 }
从索引 3 开始找到最小的元素
{
10
,
20
,
30
, 50,
40
}
并将其与索引 3 中的元素交换
{
10
,
20
,
30
,
40
,
50
}
最后，从索引 4 开始找到最小的元素
{
10
,
20
,
30
,
40
,
50
}
并将其与索引 4 中的元素交换（这没有任何作用）
{
10
,
20
,
30
,
40
,
50
}
完成！
{ 10, 20, 30, 40, 50 }
请注意，最后一次比较总是与自身进行（这是冗余的），所以我们实际上可以在数组结束前提前一个元素停止。
C++ 中的选择排序
以下是该算法在 C++ 中的实现方式
#include <iostream>
#include <iterator>
#include <utility>

int main()
{
	int array[]{ 30, 50, 20, 10, 40 };
	constexpr int length{ static_cast<int>(std::size(array)) };

	// Step through each element of the array
	// (except the last one, which will already be sorted by the time we get there)
	for (int startIndex{ 0 }; startIndex < length - 1; ++startIndex)
	{
		// smallestIndex is the index of the smallest element we’ve encountered this iteration
		// Start by assuming the smallest element is the first element of this iteration
		int smallestIndex{ startIndex };

		// Then look for a smaller element in the rest of the array
		for (int currentIndex{ startIndex + 1 }; currentIndex < length; ++currentIndex)
		{
			// If we've found an element that is smaller than our previously found smallest
			if (array[currentIndex] < array[smallestIndex])
				// then keep track of it
				smallestIndex = currentIndex;
		}

		// smallestIndex is now the index of the smallest element in the remaining array
                // swap our start element with our smallest element (this sorts it into the correct place)
		std::swap(array[startIndex], array[smallestIndex]);
	}

	// Now that the whole array is sorted, print our sorted array as proof it works
	for (int index{ 0 }; index < length; ++index)
		std::cout << array[index] << ' ';

	std::cout << '\n';

	return 0;
}
这个算法最令人困惑的部分是循环内部的另一个循环（称为**嵌套循环**）。外层循环（startIndex）逐个遍历每个元素。对于外层循环的每次迭代，内层循环（currentIndex）用于在剩余数组中（从startIndex+1开始）找到最小的元素。smallestIndex 记录内层循环找到的最小元素的索引。然后 smallestIndex 与 startIndex 交换。最后，外层循环（startIndex）前进一个元素，并重复该过程。
提示：如果您在理解上述程序的工作原理时遇到困难，可以通过在纸上模拟示例情况来帮助理解。将起始（未排序）数组元素水平写在纸的顶部。画箭头指示 startIndex、currentIndex 和 smallestIndex 索引的元素。手动跟踪程序，并在索引改变时重新绘制箭头。对于外层循环的每次迭代，另起一行显示数组的当前状态。
排序名称使用相同的算法。只需将数组类型从 int 更改为 std::string，并用适当的值进行初始化。
std::sort
由于数组排序非常常见，C++ 标准库包含一个名为 `std::sort` 的排序函数。`std::sort` 位于 `
` 头文件中，可以像这样在数组上调用：
#include <algorithm> // for std::sort
#include <iostream>
#include <iterator> // for std::size

int main()
{
	int array[]{ 30, 50, 20, 10, 40 };

	std::sort(std::begin(array), std::end(array));

	for (int i{ 0 }; i < static_cast<int>(std::size(array)); ++i)
		std::cout << array[i] << ' ';

	std::cout << '\n';

	return 0;
}
默认情况下，std::sort 使用 `operator<` 比较成对的元素并根据需要交换它们（与我们上面选择排序的例子非常相似），按升序排序。
我们将在未来的章节中详细讨论 `std::sort`。
小测验时间
问题 #1
手动演示选择排序如何作用于以下数组：{ 30, 60, 20, 50, 40, 10 }。每次交换后显示数组。
显示答案
30 60 20 50 40 10
10
60 20 50 40
30
10
20
60
50 40 30
10 20
30
50 40
60
10 20 30
40
50
60
10 20 30 40
50
60 (自交换)
10 20 30 40 50
60
(自交换)
问题 #2
重写上面的选择排序代码，使其按降序排序（最大的数字优先）。虽然这看起来很复杂，但实际上却出奇地简单。
显示答案
只需将
if (array[currentIndex] < array[smallestIndex])
改为
if (array[currentIndex] > array[smallestIndex])
smallestIndex 可能也应该改名为 largestIndex。
#include <iostream>
#include <iterator> // for std::size
#include <utility>

int main()
{
    int array[]{ 30, 50, 20, 10, 40 };
    constexpr int length{ static_cast<int>(std::size(array)) }; // C++17
//  constexpr int length{ sizeof(array) / sizeof(array[0]) }; // use instead if not C++17 capable

    // Step through each element of the array except the last
    for (int startIndex{ 0 }; startIndex < length - 1; ++startIndex)
    {
        // largestIndex is the index of the largest element we've encountered so far.
        int largestIndex{ startIndex };

        // Search through every element starting at startIndex + 1
        for (int currentIndex{ startIndex + 1 }; currentIndex < length; ++currentIndex)
        {
            // If the current element is larger than our previously found largest
            if (array[currentIndex] > array[largestIndex])
                // This is the new largest number for this iteration
                largestIndex = currentIndex;
        }

        // Swap our start element with our largest element
        std::swap(array[startIndex], array[largestIndex]);
    }

    // Now print our sorted array as proof it works
    for (int index{ 0 }; index < length; ++index)
        std::cout << array[index] << ' ';

    std::cout << '\n';

    return 0;
}
问题 #3
这个会很难，所以请做好准备。
另一种简单的排序算法称为“冒泡排序”。冒泡排序通过比较相邻的元素对，并在满足条件时交换它们，从而使元素“冒泡”到数组的末尾。尽管有相当多的方法可以优化冒泡排序，但在本次测验中，我们将坚持使用未优化的版本，因为它最简单。
未优化的冒泡排序执行以下步骤，将数组从小到大排序：
A) 比较数组元素 0 和数组元素 1。如果元素 0 较大，则将其与元素 1 交换。
B) 现在对元素 1 和 2，以及其后每对元素执行相同的操作，直到到达数组末尾。此时，数组中的最后一个元素将已排序。
C) 重复前两个步骤，直到数组排序完成。
编写代码，根据上述规则对以下数组进行冒泡排序
int array[]{ 6, 3, 2, 9, 7, 1, 5, 4, 8 };
在程序结束时打印排序后的数组元素。
提示：如果我们每次迭代能够排序一个元素，这意味着我们需要迭代的次数大约是数组中数字的个数，才能保证整个数组都已排序。
提示：比较元素对时，请注意数组的范围。
显示答案
#include <iostream>
#include <iterator> // for std::size
#include <utility>

int main()
{
    int array[]{ 6, 3, 2, 9, 7, 1, 5, 4, 8 };
    constexpr int length{ static_cast<int>(std::size(array)) }; // C++17
//  constexpr int length{ sizeof(array) / sizeof(array[0]) }; // use instead if not C++17 capable

    // Step through each element of the array (except the last, which will already be sorted by the time we get to it)
    for (int iteration{ 0 }; iteration < length-1; ++iteration)
    {
        // Search through all elements up to the end of the array - 1
        // The last element has no pair to compare against
        for (int currentIndex{ 0 }; currentIndex < length - 1; ++currentIndex)
        {
            // If the current element is larger than the element after it, swap them
            if (array[currentIndex] > array[currentIndex+1])
                std::swap(array[currentIndex], array[currentIndex + 1]);
        }
    }

    // Now print our sorted array as proof it works
    for (int index{ 0 }; index < length; ++index)
        std::cout << array[index] << ' ';

    std::cout << '\n';

    return 0;
}
问题 #4
为您在上一道测验题中编写的冒泡排序算法添加两项优化
注意，在冒泡排序的每次迭代中，剩余的最大数字都会冒泡到数组的末尾。第一次迭代后，最后一个数组元素已排序。第二次迭代后，倒数第二个数组元素也已排序。依此类推……每次迭代，我们都不需要重新检查已知已排序的元素。修改您的循环，使其不重新检查已排序的元素。
如果我们完成整个迭代而没有进行任何交换，那么我们就知道数组一定已经排序。实现一个检查来确定本次迭代是否进行了任何交换，如果没有，则提前终止循环。如果循环提前终止，请打印排序在哪个迭代中提前结束。
您的输出应与此匹配
Early termination on iteration 6
1 2 3 4 5 6 7 8 9
显示答案
#include <iostream>
#include <iterator> // for std::size
#include <utility>

int main()
{
    int array[]{ 6, 3, 2, 9, 7, 1, 5, 4, 8 };
    constexpr int length{ static_cast<int>(std::size(array)) }; // C++17
//  constexpr int length{ sizeof(array) / sizeof(array[0]) }; // use instead if not C++17 capable

    // Step through each element of the array except the last
    for (int iteration{ 0 }; iteration < length-1; ++iteration)
    {
        // Account for the fact that the last element is already sorted with each subsequent iteration
        // so our array "ends" one element sooner
        int endOfArrayIndex{ length - iteration };

        bool swapped{ false }; // Keep track of whether any elements were swapped this iteration

        // Search through all elements up to the end of the array - 1
        // The last element has no pair to compare against
        for (int currentIndex{ 0 }; currentIndex < endOfArrayIndex - 1; ++currentIndex)
        {
            // If the current element is larger than the element after it
            if (array[currentIndex] > array[currentIndex + 1])
            {
                // Swap them
                std::swap(array[currentIndex], array[currentIndex + 1]);
                swapped = true;
            }
        }

        // If we haven't swapped any elements this iteration, we're done early
        if (!swapped)
        {
            // iteration is 0 based, but counting iterations is 1-based.  So add 1 here to adjust.
            std::cout << "Early termination on iteration: " << iteration+1 << '\n';
            break;
        }
    }

    // Now print our sorted array as proof it works
    for (int index{ 0 }; index < length; ++index)
        std::cout << array[index] << ' ';

    std::cout << '\n';

    return 0;
}
下一课
18.2
迭代器简介
返回目录
上一课
17.x
第17章 总结与测验