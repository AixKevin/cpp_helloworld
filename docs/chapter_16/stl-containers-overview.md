# 21.2 — STL 容器概览

21.2 — STL 容器概览
Alex
2011年9月11日，下午3:41 (太平洋夏令时)
2021年9月19日
到目前为止，STL 库最常用的功能是 STL 容器类。如果你需要快速回顾容器类，请查阅课程
23.6 -- 容器类
。
STL 包含许多不同的容器类，可用于不同的情况。一般来说，容器类分为三大基本类别：序列容器、关联容器和容器适配器。我们在这里只对容器进行快速概览。
序列容器
序列容器是维护容器中元素顺序的容器类。序列容器的一个显著特征是，你可以选择按位置插入元素。序列容器最常见的例子是数组：如果你向数组中插入四个元素，这些元素将按照你插入它们的精确顺序排列。
截至 C++11，STL 包含 6 种序列容器：std::vector、std::deque、std::array、std::list、std::forward_list 和 std::basic_string。
如果你学过物理，你可能会将向量（vector）视为一个既有大小又有方向的实体。STL 中不幸命名为
vector
的类是一个动态数组，能够根据需要增长以容纳其元素。vector 类允许通过 operator[] 随机访问其元素，并且从 vector 末尾插入和删除元素通常很快。
以下程序将 6 个数字插入一个 vector，并使用重载的 [] 运算符按顺序访问它们以打印它们。
#include <vector>
#include <iostream>

int main()
{

    std::vector<int> vect;
    for (int count=0; count < 6; ++count)
        vect.push_back(10 - count); // insert at end of array

    for (int index=0; index < vect.size(); ++index)
        std::cout << vect[index] << ' ';

    std::cout << '\n';
}
这个程序产生的结果是
10 9 8 7 6 5
deque
类（发音为“deck”）是一个双端队列类，实现为可从两端增长的动态数组。
#include <iostream>
#include <deque>

int main()
{
    std::deque<int> deq;
    for (int count=0; count < 3; ++count)
    {
        deq.push_back(count); // insert at end of array
        deq.push_front(10 - count); // insert at front of array
    }

    for (int index=0; index < deq.size(); ++index)
        std::cout << deq[index] << ' ';

    std::cout << '\n';
}
这个程序产生的结果是
8 9 10 0 1 2
list
是一种特殊类型的序列容器，称为双向链表，其中容器中的每个元素都包含指向列表中下一个和上一个元素的指针。列表只提供对列表开头和结尾的访问——不提供随机访问。如果你想查找中间的值，你必须从一端开始“遍历列表”，直到找到你想要查找的元素。列表的优点是，如果你已经知道要插入元素的位置，插入元素的速度非常快。通常使用迭代器遍历列表。
我们将在未来的课程中详细讨论链表和迭代器。
尽管 STL
string
（和 wstring）类通常不作为序列容器的一种类型包含在内，但它们本质上是，因为它们可以被认为是数据元素类型为 char（或 wchar）的 vector。
关联容器
关联容器是当输入插入到容器中时自动对其进行排序的容器。默认情况下，关联容器使用 operator< 比较元素。
set
是一个存储唯一元素的容器，不允许重复元素。元素根据其值进行排序。
multiset
是允许重复元素的 set。
map
（也称为关联数组）是一个 set，其中每个元素都是一个对，称为键/值对。键用于排序和索引数据，并且必须是唯一的。值是实际数据。
multimap
（也称为字典）是允许重复键的 map。现实生活中的字典是 multimap：键是单词，值是单词的含义。所有键都按升序排序，你可以通过键查找值。有些单词可以有多个含义，这就是为什么字典是 multimap 而不是 map。
容器适配器
容器适配器是为特定用途而设计的特殊预定义容器。容器适配器有趣的部分在于你可以选择它们要使用的序列容器。
stack
是一种容器，其中元素以 LIFO（后进先出）上下文操作，元素从容器的末尾插入（压入）和移除（弹出）。栈默认使用 deque 作为其默认序列容器（这看起来很奇怪，因为 vector 似乎更自然），但也可以使用 vector 或 list。
queue
是一种容器，其中元素以 FIFO（先进先出）上下文操作，元素从容器的后端插入（压入）并从前端移除（弹出）。队列默认使用 deque，但也可以使用 list。
priority queue
是一种队列类型，其中元素保持排序（通过 operator<）。当元素被压入时，元素在队列中排序。从前端移除元素将返回优先队列中优先级最高的项。
下一课
21.3
STL 迭代器概览
返回目录
上一课
21.1
标准库