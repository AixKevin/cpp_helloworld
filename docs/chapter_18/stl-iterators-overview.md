# 21.3 — STL 迭代器概述

21.3 — STL 迭代器概述
Alex
2011 年 9 月 11 日下午 3:44 PDT
2023 年 1 月 27 日
迭代器
是一个对象，可以遍历（迭代）容器类，而用户无需知道容器是如何实现的。对于许多类（特别是列表和关联类），迭代器是访问这些类元素的主要方式。
迭代器最好被视为指向容器中给定元素的指针，并带有一组重载运算符以提供一组定义明确的功能
运算符*
-- 解引用迭代器返回迭代器当前指向的元素。
运算符++
-- 将迭代器移动到容器中的下一个元素。大多数迭代器还提供
运算符--
以移动到上一个元素。
运算符== 和 运算符!=
-- 基本比较运算符，用于确定两个迭代器是否指向同一个元素。要比较两个迭代器指向的值，请先解引用迭代器，然后使用比较运算符。
运算符=
-- 将迭代器分配到新位置（通常是容器元素的开始或结束）。要分配迭代器指向的元素的值，请先解引用迭代器，然后使用赋值运算符。
每个容器都包含四个基本成员函数，可与运算符= 一起使用
begin()
返回一个迭代器，表示容器中元素的开头。
end()
返回一个迭代器，表示元素末尾之后的一个元素。
cbegin()
返回一个 const（只读）迭代器，表示容器中元素的开头。
cend()
返回一个 const（只读）迭代器，表示元素末尾之后的一个元素。
end() 不指向列表中的最后一个元素可能看起来很奇怪，但这主要是为了方便循环：可以继续迭代元素，直到迭代器到达 end()，然后就知道完成了。
最后，所有容器都提供（至少）两种类型的迭代器
container::iterator
提供读/写迭代器
container::const_iterator
提供只读迭代器
让我们看一些使用迭代器的示例。
遍历 vector
#include <iostream>
#include <vector>

int main()
{
    std::vector<int> vect;
    for (int count=0; count < 6; ++count)
        vect.push_back(count);

    std::vector<int>::const_iterator it; // declare a read-only iterator
    it = vect.cbegin(); // assign it to the start of the vector
    while (it != vect.cend()) // while it hasn't reach the end
    {
        std::cout << *it << ' '; // print the value of the element it points to
        ++it; // and iterate to the next element
    }

    std::cout << '\n';
}
这将打印以下内容
0 1 2 3 4 5
遍历列表
现在让我们用列表做同样的事情
#include <iostream>
#include <list>

int main()
{

    std::list<int> li;
    for (int count=0; count < 6; ++count)
        li.push_back(count);

    std::list<int>::const_iterator it; // declare an iterator
    it = li.cbegin(); // assign it to the start of the list
    while (it != li.cend()) // while it hasn't reach the end
    {
        std::cout << *it << ' '; // print the value of the element it points to
        ++it; // and iterate to the next element
    }

    std::cout << '\n';
}
这会打印
0 1 2 3 4 5
请注意，代码与 vector 情况几乎相同，尽管 vector 和列表的内部实现几乎完全不同！
遍历 set
在下面的示例中，我们将从 6 个数字创建一个 set，并使用迭代器打印 set 中的值
#include <iostream>
#include <set>

int main()
{
    std::set<int> myset;
    myset.insert(7);
    myset.insert(2);
    myset.insert(-6);
    myset.insert(8);
    myset.insert(1);
    myset.insert(-4);

    std::set<int>::const_iterator it; // declare an iterator
    it = myset.cbegin(); // assign it to the start of the set
    while (it != myset.cend()) // while it hasn't reach the end
    {
        std::cout << *it << ' '; // print the value of the element it points to
        ++it; // and iterate to the next element
    }

    std::cout << '\n';
}
此程序产生以下结果：
-6 -4 1 2 7 8
请注意，尽管填充 set 的方式与填充 vector 和列表的方式不同，但用于遍历 set 元素的代码本质上是相同的。
遍历 map
这个有点复杂。map 和 multimap 接受元素对（定义为 std::pair）。我们使用 make_pair() 辅助函数轻松创建对。std::pair 允许通过 first 和 second 成员访问对的元素。在我们的 map 中，我们使用 first 作为键，second 作为值。
#include <iostream>
#include <map>
#include <string>

int main()
{
	std::map<int, std::string> mymap;
	mymap.insert(std::make_pair(4, "apple"));
	mymap.insert(std::make_pair(2, "orange"));
	mymap.insert(std::make_pair(1, "banana"));
	mymap.insert(std::make_pair(3, "grapes"));
	mymap.insert(std::make_pair(6, "mango"));
	mymap.insert(std::make_pair(5, "peach"));

	auto it{ mymap.cbegin() }; // declare a const iterator and assign to start of vector
	while (it != mymap.cend()) // while it hasn't reach the end
	{
		std::cout << it->first << '=' << it->second << ' '; // print the value of the element it points to
		++it; // and iterate to the next element
	}

	std::cout << '\n';
}
这个程序产生的结果是
1=banana 2=orange 3=grapes 4=apple 5=peach 6=mango
请注意这里迭代器使遍历容器的每个元素变得多么容易。你根本不需要关心 map 如何存储其数据！
总结
迭代器提供了一种简单的方法来遍历容器类的元素，而无需了解容器类是如何实现的。当与 STL 的算法和容器类的成员函数结合使用时，迭代器变得更加强大。在下一课中，你将看到一个使用迭代器将元素插入列表的示例（列表不提供重载的运算符[] 以直接访问其元素）。
值得注意的一点是：迭代器必须按类实现，因为迭代器确实需要知道类的实现方式。因此，迭代器总是与特定的容器类绑定。
下一课
21.4
STL 算法概述
返回目录
上一课
21.2
STL 容器概述