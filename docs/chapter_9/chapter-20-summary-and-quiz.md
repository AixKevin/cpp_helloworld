# 20.x — 第 20 章总结和测验

20.x — 第 20 章总结和测验
Alex
2015 年 12 月 4 日，太平洋标准时间晚上 7:31
2025 年 2 月 8 日
章节回顾
又一个章节完成了！现在只剩下这个烦人的测验了…
函数参数可以通过值、引用或地址传递。对于基本数据类型和枚举器，请使用按值传递。对于结构体、类，或者当您需要函数修改参数时，请使用按引用传递。对于传递指针或内置数组，请使用按地址传递。尽可能将您的按引用和按地址参数设置为 const。
值可以通过值、引用或地址返回。大多数情况下，按值返回是可以的，但是当处理动态分配的数据、结构体或类时，按引用或按地址返回会很有用。如果按引用或按地址返回，请记住确保您没有返回将超出作用域的东西。
函数指针允许我们将一个函数传递给另一个函数。这对于允许调用者自定义函数的行为很有用，例如列表的排序方式。
动态内存分配在堆上。
调用栈记录了从程序开始到当前执行点所有活动的函数（那些已被调用但尚未终止的函数）。局部变量分配在栈上。栈的大小有限。std::vector 可以用来实现类似栈的行为。
递归函数是调用自身的函数。所有递归函数都需要一个终止条件。
命令行参数允许用户或其他程序在启动时将数据传递到我们的程序中。命令行参数总是 C 风格的字符串，如果需要数值，则必须将其转换为数字。
省略号允许您向函数传递可变数量的参数。然而，省略号参数会暂停类型检查，并且不知道传递了多少个参数。程序需要跟踪这些细节。
Lambda 函数是可以嵌套在其他函数中的函数。它们不需要名称，与算法库结合使用非常有用。
小测验时间
问题 #1
为以下情况编写函数原型。必要时使用 const。
a) 一个名为 max() 的函数，接受两个 double 并返回其中较大的一个。
显示答案
double max(double x, double y);
b) 一个名为 swap() 的函数，用于交换两个整数。
显示答案
void swap(int& x, int& y);
c) 一个名为 getLargestElement() 的函数，接受一个动态分配的整数数组，并以调用者可以更改返回元素值的方式返回其中最大的数字（不要忘记长度参数）。
显示答案
// Note: array can't be const in this case, because returning a non-const reference to a const element would be a const violation.
int& getLargestElement(int* array, int length);
问题 #2
这些程序有什么问题？
a)
int& doSomething()
{
    int array[]{ 1, 2, 3, 4, 5 };
    return array[3];
}
显示答案
doSomething() 返回对局部变量的引用，该变量将在 doSomething 终止时被销毁。
b)
int sumTo(int value)
{
    return value + sumTo(value - 1);
}
显示答案
函数 sumTo() 没有终止条件。变量 value 最终会变为负数，函数将无限循环直到栈溢出。
c)
float divide(float x, float y)
{
    return x / y;
}

double divide(float x, float y)
{
    return x / y;
}
显示答案
这两个 divide 函数不明确，因为它们具有相同的名称和相同的参数。还存在潜在的除以 0 问题。
d)
#include <iostream>

int main()
{
    int array[100000000]{};

    for (auto x: array)
        std::cout << x << ' ';

    std::cout << '\n';

    return 0;
}
显示答案
该数组太大，无法在栈上分配。它应该动态分配。
e)
#include <iostream>

int main(int argc, char* argv[])
{
    int age{ argv[1] };
    std::cout << "The user's age is " << age << '\n';

    return 0;
}
显示答案
argv[1] 可能不存在。如果存在，argv[1] 是一个字符串参数，不能通过赋值转换为整数。
问题 #3
确定值是否存在于排序数组中的最佳算法称为二分查找。
二分查找的工作原理如下：
查看数组的中心元素（如果数组元素数量为偶数，则向下取整）。
如果中心元素大于目标元素，则丢弃数组的上半部分（或在下半部分递归）。
如果中心元素小于目标元素，则丢弃数组的下半部分（或在上半部分递归）。
如果中心元素等于目标元素，则返回中心元素的索引。
如果您在没有找到目标元素的情况下丢弃了整个数组，则返回一个表示“未找到”的哨兵值（在此例中，我们将使用 -1，因为它是无效的数组索引）。
因为我们每次迭代都可以丢弃一半的数组，所以这种算法非常快。即使是包含一百万个元素的数组，最多也只需 20 次迭代即可确定值是否存在于数组中！但是，它只适用于排序数组。
修改数组（例如丢弃数组中一半的元素）开销很大，因此我们通常不修改数组。相反，我们使用两个整数（min 和 max）来保存我们感兴趣检查的数组的最小和最大元素的索引。
让我们看一个此算法如何工作的示例，给定数组 { 3, 6, 7, 9, 12, 15, 18, 21, 24 }，目标值为 7。最初，min = 0，max = 8，因为我们正在搜索整个数组（数组长度为 9，因此最后一个元素的索引为 8）。
第一次传递）我们计算 min (0) 和 max (8) 的中点，即 4。元素 #4 的值为 12，大于我们的目标值。由于数组已排序，我们知道所有索引等于或大于中点 (4) 的元素都必须太大。所以我们保持 min 不变，并将 max 设置为 3。
第二次传递）我们计算 min (0) 和 max (3) 的中点，即 1。元素 #1 的值为 6，小于我们的目标值。由于数组已排序，我们知道所有索引等于或小于中点 (1) 的元素都必须太小。所以我们将 min 设置为 2，并保持 max 不变。
第三次传递）我们计算 min (2) 和 max (3) 的中点，即 2。元素 #2 的值为 7，这是我们的目标值。所以我们返回 2。
在 C++20 中，可以通过调用
std::midpoint
来计算中点。在 C++20 之前，您需要自己计算中点——在这种情况下，您可以使用
min + ((max - min) / 2)
来避免溢出（当 min 和 max 都为正时）。
给定以下代码
#include <iostream>
#include <iterator>

// array is the array to search over.
// target is the value we're trying to determine exists or not.
// min is the index of the lower bounds of the array we're searching.
// max is the index of the upper bounds of the array we're searching.
// binarySearch() should return the index of the target element if the target is found, -1 otherwise
int binarySearch(const int* array, int target, int min, int max)
{

}

int main()
{
    constexpr int array[]{ 3, 6, 8, 12, 14, 17, 20, 21, 26, 32, 36, 37, 42, 44, 48 };

    // We're going to test a bunch of values to see if the algorithm returns the result we expect

    // Here are the test values
    constexpr int testValues[]{ 0, 3, 12, 13, 22, 26, 43, 44, 48, 49 };

    // And here are the results that we expect for those test values
    int expectedResult[]{ -1, 0, 3, -1, -1, 8, -1, 13, 14, -1 };

    // Make sure we have the same number of test values and expected results
    static_assert(std::size(testValues) == std::size(expectedResult));

    int numTestValues { std::size(testValues) };
    // Loop through all of the test values
    for (int count{ 0 }; count < numTestValues; ++count)
    {
        // See if our test value is in the array
        int index{ binarySearch(array, testValues[count], 0, static_cast<int>(std::size(array)) - 1) };
        // If it matches our expected value, then great!
        if (index == expectedResult[count])
             std::cout << "test value " << testValues[count] << " passed!\n";
        else // otherwise, our binarySearch() function must be broken
             std::cout << "test value " << testValues[count] << " failed.  There's something wrong with your code!\n";
    }

    return 0;
}
a) 编写 binarySearch 函数的迭代版本。
提示：当 min 索引大于 max 索引时，您可以安全地说目标元素不存在。
显示答案
#include <cassert>
#include <iostream>
#include <numeric> // for std::midpoint

// array is the array to search over.
// target is the value we're trying to determine exists or not.
// min is the index of the lower bounds of the array we're searching.
// max is the index of the upper bounds of the array we're searching.
// binarySearch() should return the index of the target element if the target is found, -1 otherwise
int binarySearch(const int* array, int target, int min, int max)
{
    assert(array); // make sure array exists

    while (min <= max)
    {
        // implement this iteratively
        int midpoint{ std::midpoint(min, max) };
        // Before C++20
        // int midpoint{ min + ((max-min) / 2) }; // this way of calculating midpoint avoids overflow

        if (array[midpoint] > target)
        {
            // if array[midpoint] > target, then we know the number must be in the lower half of the array
            // we can use midpoint - 1 as the upper index, since we don't need to retest the midpoint next iteration
            max = midpoint - 1;
        }
        else if (array[midpoint] < target)
        {
            // if array[midpoint] < target, then we know the number must be in the upper half of the array
            // we can use midpoint + 1 as the lower index, since we don't need to retest the midpoint next iteration
            min = midpoint + 1;
        }
        else
        {
            return midpoint;
        }
    }
    
    return -1;
}
b) 编写 binarySearch 函数的递归版本。
显示答案
#include <cassert>
#include <numeric> // for std::midpoint

// array is the array to search over.
// target is the value we're trying to determine exists or not.
// min is the index of the lower bounds of the array we're searching.
// max is the index of the upper bounds of the array we're searching.
// binarySearch() should return the index of the target element if the target is found, -1 otherwise
int binarySearch(const int* array, int target, int min, int max)
{
    assert(array); // make sure array exists

    // implement this recursively

    if (min > max)
        return -1;

    int midpoint{ std::midpoint(min, max) };
    // Before C++20
    // int midpoint{ min + ((max-min) / 2) }; // this way of calculating midpoint avoids overflow

    if (array[midpoint] > target)
    {
        return binarySearch(array, target, min, midpoint - 1);
    }
    else if (array[midpoint] < target)
    {
        return binarySearch(array, target, midpoint + 1, max);
    }

    return midpoint;
}
提示
std::binary_search
如果值存在于排序列表中，则返回 true。
std::equal_range
返回具有给定值的第一个和最后一个元素的迭代器。
不要使用这些函数来解决测验，但如果您将来需要二分查找，请使用它们。
下一课
21.1
运算符重载简介
返回目录
上一课
20.7
Lambda 捕获