# 21.4 — STL 算法概述

21.4 — STL 算法概述
Alex
2011 年 9 月 11 日下午 3:45 PDT
2021 年 10 月 21 日
除了容器类和迭代器之外，STL 还提供了许多通用算法，用于处理容器类的元素。这些算法可以让你实现诸如搜索、排序、插入、重新排序、删除和复制容器类元素等功能。
请注意，算法是作为使用迭代器操作的函数实现的。这意味着每个算法只需要实现一次，并且通常会自动适用于所有提供一组迭代器（包括你自定义的容器类）的容器。虽然这非常强大，可以快速编写复杂的代码，但它也有一个阴暗面：某些算法和容器类型的组合可能无法工作，可能导致无限循环，或者可能工作但性能极差。因此，使用这些算法需自行承担风险。
STL 提供了相当多的算法——我们在这里只介绍一些更常见和易于使用的算法。其余的（以及完整的详细信息）将保留在关于 STL 算法的章节中。
要使用任何 STL 算法，只需包含 algorithm 头文件。
min_element 和 max_element
std::min_element
和
std::max_element
算法用于查找容器类中的最小和最大元素。
std::iota
生成一系列连续的值。
#include <algorithm> // std::min_element and std::max_element
#include <iostream>
#include <list>
#include <numeric> // std::iota

int main()
{
    std::list<int> li(6);
    // Fill li with numbers starting at 0.
    std::iota(li.begin(), li.end(), 0);

    std::cout << *std::min_element(li.begin(), li.end()) << ' '
              << *std::max_element(li.begin(), li.end()) << '\n';
	
    return 0;
}
打印
0 5
find (和 list::insert)
在这个例子中，我们将使用
std::find()
算法在 list 类中查找一个值，然后使用 list::insert() 函数在该位置向 list 中添加一个新值。
#include <algorithm>
#include <iostream>
#include <list>
#include <numeric>

int main()
{
    std::list<int> li(6);
    std::iota(li.begin(), li.end(), 0);

    // Find the value 3 in the list
    auto it{ std::find(li.begin(), li.end(), 3) };
    
    // Insert 8 right before 3.
    li.insert(it, 8);

    for (int i : li) // for loop with iterators
        std::cout << i << ' ';
    	
    std::cout << '\n';

    return 0;
}
这将打印值
0 1 2 8 3 4 5
当搜索算法没有找到它要查找的内容时，它会返回结束迭代器。
如果我们不确定 3 是
li
的一个元素，那么在使用返回的迭代器进行其他操作之前，我们必须检查
std::find
是否找到了它。
if (it == li.end())
{
  std::cout << "3 was not found\n";
}
else
{
  // ...
}
sort 和 reverse
在这个例子中，我们将对一个 vector 进行排序，然后将其反转。
#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    std::vector<int> vect{ 7, -3, 6, 2, -5, 0, 4 };

    // sort the vector
    std::sort(vect.begin(), vect.end());

    for (int i : vect)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    // reverse the vector
    std::reverse(vect.begin(), vect.end());

    for (int i : vect)
    {
        std::cout << i << ' ';
    }
 	
    std::cout << '\n';

    return 0;
}
这会产生结果
-5 -3 0 2 4 6 7
7 6 4 2 0 -3 -5
或者，我们可以将自定义比较函数作为第三个参数传递给 `std::sort`。在
头文件中，有几个我们可以使用的比较函数，这样我们就不必自己编写。我们可以将 `std::greater` 传递给 `std::sort` 并删除对 `std::reverse` 的调用。Vector 将立即从高到低排序。
请注意，
std::sort()
不适用于 list 容器类——list 类提供了自己的
sort()
成员函数，它比通用版本效率更高。
总结
尽管这只是 STL 提供的算法的一小部分，但它应该足以说明这些算法与迭代器和基本容器类结合使用是多么容易。还有足够的其他算法可以填满一整章！
下一课
22.1
std::string 和 std::wstring
返回目录
上一课
21.3
STL 迭代器概述