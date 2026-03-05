# 16.10 — std::vector 大小调整和容量

16.10 — std::vector 大小调整和容量
Alex
2015 年 11 月 24 日，下午 4:15 PST
2024 年 1 月 10 日
在本章之前的课程中，我们介绍了容器、数组和
std::vector
。我们还讨论了诸如如何访问数组元素、获取数组长度以及如何遍历数组等主题。虽然我们在示例中使用了
std::vector
，但我们讨论的概念通常适用于所有数组类型。
在本章的剩余课程中，我们将重点关注使
std::vector
与大多数其他数组类型显着不同的一件事：在实例化后调整自身大小的能力。
固定大小数组与动态数组
大多数数组类型都有一个显著的限制：数组的长度必须在实例化时确定，然后不能更改。这种数组称为
固定大小数组
或
固定长度数组
。
std::array
和
C 风格数组
都是固定大小的数组类型。我们将在下一章进一步讨论这些。
另一方面，
std::vector
是一个动态数组。
动态数组
（也称为
可调整大小的数组
）是一种在实例化后可以更改大小的数组。这种可调整大小的能力使得
std::vector
变得特别。
在运行时调整
std::vector
的大小
std::vector
可以在实例化后通过调用
resize()
成员函数并指定新的所需长度来调整大小
#include <iostream>
#include <vector>

int main()
{
    std::vector v{ 0, 1, 2 }; // create vector with 3 elements
    std::cout << "The length is: " << v.size() << '\n';

    v.resize(5);              // resize to 5 elements
    std::cout << "The length is: " << v.size() << '\n';

    for (auto i : v)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
这会打印
The length is: 3
The length is: 5
0 1 2 0 0
这里有两点需要注意。首先，当我们调整向量大小时，现有元素的值被保留了！其次，新元素是值初始化的（对于类类型执行默认初始化，对于其他类型执行零初始化）。因此，两个新的
int
类型元素被零初始化为值
0
。
向量也可以缩小大小
#include <iostream>
#include <vector>

void printLength(const std::vector<int>& v)
{
	std::cout << "The length is: "	<< v.size() << '\n';
}

int main()
{
    std::vector v{ 0, 1, 2, 3, 4 }; // length is initially 5
    printLength(v);

    v.resize(3);                    // resize to 3 elements
    printLength(v);

    for (int i : v)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
这会打印
The length is: 5
The length is: 3
0 1 2
std::vector
的长度与容量
想象一排 12 栋房子。我们会说房子数量（或房子排的长度）是 12。如果我们想知道哪些房子目前有人居住……我们必须通过其他方式确定（例如，按门铃看是否有人应答）。当我们只有长度时，我们只知道有多少东西存在。
现在想象一盒目前有 5 个鸡蛋的鸡蛋。我们会说鸡蛋的数量是 5。但在这种情况下，我们关心另一个维度：如果装满了，这盒鸡蛋能装多少个。我们会说这盒鸡蛋的容量是 12。这盒鸡蛋有容纳 12 个鸡蛋的空间，而只有 5 个正在使用——因此，我们可以再添加 7 个鸡蛋而不会使盒子溢出。当我们同时拥有长度和容量时，我们可以区分当前有多少东西存在和有多少东西有空间。
到目前为止，我们只讨论了
std::vector
的长度。但是
std::vector
也有一个容量。在
std::vector
的上下文中，
容量
是
std::vector
已分配存储空间的元素数量，而
长度
是当前正在使用的元素数量。
容量为 5 的
std::vector
已为 5 个元素分配了空间。如果向量中包含 2 个正在使用的元素，则向量的长度（大小）为 2。剩余的 3 个元素已为其分配了内存，但它们不被视为正在使用中。它们以后可以使用而不会使向量溢出。
关键见解
向量的长度是“正在使用”的元素数量。
向量的容量是已在内存中分配的元素数量。
获取
std::vector
的容量
我们可以通过
capacity()
成员函数获取
std::vector
的容量。
例如
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "Capacity: " << v.capacity() << " Length:"	<< v.size() << '\n';
}

int main()
{
    std::vector v{ 0, 1, 2 }; // length is initially 3

    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    v.resize(5); // resize to 5 elements

    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
在作者的机器上，这会打印以下内容
Capacity: 3  Length: 3
0 1 2
Capacity: 5  Length: 5
0 1 2 0 0
首先，我们用 3 个元素初始化了向量。这使得向量分配了 3 个元素的存储空间（容量为 3），并且所有 3 个元素都被视为正在使用中（长度 = 3）。
然后我们调用
resize(5)
，这意味着我们现在需要一个长度为 5 的向量。由于向量只为 3 个元素分配了存储空间，但它需要 5 个，因此向量需要获取更多的存储空间来容纳额外的元素。
调用
resize()
完成后，我们可以看到向量现在有 5 个元素的空间（容量为 5），并且所有 5 个元素现在都被视为正在使用中（长度为 5）。
大多数情况下，您不需要使用
capacity()
函数，但在以下示例中我们会大量使用它，以便我们可以看到向量存储发生了什么。
存储的重新分配，以及为什么它很昂贵
当
std::vector
更改它管理的存储量时，这个过程称为
重新分配
。通俗地说，重新分配过程大致如下
std::vector
获取具有所需元素数量的新内存。这些元素被值初始化。
旧内存中的元素被复制（如果可能，则移动）到新内存中。然后旧内存被返回给系统。
std::vector
的容量和长度被设置为新值。
从外部看，
std::vector
似乎已调整了大小。但在内部，内存（以及所有元素）实际上已被替换！
相关内容
在运行时获取新内存的过程称为动态内存分配。我们在
19.1 课 -- 使用 new 和 delete 进行动态内存分配
中介绍了这一点。
由于重新分配通常需要复制数组中的每个元素，因此重新分配是一个昂贵的过程。因此，我们希望尽可能避免重新分配。
关键见解
重新分配通常很昂贵。避免不必要的重新分配。
为什么要区分长度和容量？
如果需要，
std::vector
会重新分配其存储空间，但就像梅尔维尔的巴特尔比一样，它宁愿不这样做，因为重新分配存储空间在计算上很昂贵。
如果
std::vector
只跟踪其长度，那么每个
resize()
请求都会导致对新长度的昂贵重新分配。将长度和容量分开使
std::vector
能够更智能地判断何时需要重新分配。
以下示例说明了这一点
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "Capacity: " << v.capacity() << " Length:"	<< v.size() << '\n';
}

int main()
{
    // Create a vector with length 5
    std::vector v{ 0, 1, 2, 3, 4 };
    v = { 0, 1, 2, 3, 4 }; // okay, array length = 5
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // Resize vector to 3 elements
    v.resize(3); // we could also assign a list of 3 elements here
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // Resize vector back to 5 elements
    v.resize(5);
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
这会产生以下结果
Capacity: 5  Length: 5
0 1 2 3 4 
Capacity: 5  Length: 3
0 1 2 
Capacity: 5  Length: 5
0 1 2 0 0
当我们用 5 个元素初始化向量时，容量设置为 5，表明我们的向量最初分配了 5 个元素的空间。长度也设置为 5，表明所有这些元素都在使用中。
在我们调用
v.resize(3)
后，长度更改为 3 以满足我们对更小数组的请求。但是，请注意容量仍然是 5，这意味着向量没有进行重新分配！
最后，我们调用了
v.resize(5)
。由于向量已经有容量 5，它不需要重新分配。它只是将长度改回 5，并对最后两个元素进行值初始化。
通过将长度和容量分开，在此示例中我们避免了原本会发生的 2 次重新分配。在下一课中，我们将看到一个逐个向向量添加元素的示例。在这种情况下，不每次长度更改都重新分配的能力更为重要。
关键见解
将容量与长度分开跟踪允许
std::vector
在长度更改时避免一些重新分配。
向量索引基于长度，而不是容量
您可能会惊讶地发现，下标运算符 (
operator[]
) 和
at()
成员函数的有效索引是基于向量的长度，而不是容量。
在上面的示例中，当
v
的容量为 5 且长度为 3 时，只有索引 0 到 2 有效。即使长度 3（包含）和容量 5（不包含）之间的索引的元素存在，它们的索引也被视为超出边界。
警告
下标仅在 0 和向量长度（而不是其容量）之间有效！
收缩
std::vector
将向量调整得更大将增加向量的长度，如果需要，还会增加其容量。但是，将向量调整得更小只会减小其长度，而不会减小其容量。
仅仅为了回收少量不再需要的元素的内存而重新分配向量是一个糟糕的选择。但是，如果我们有一个包含大量不再需要的元素的向量，内存浪费可能会很严重。
为了解决这种情况，
std::vector
有一个名为
shrink_to_fit()
的成员函数，它请求向量将其容量缩小以匹配其长度。此请求是非绑定的，这意味着实现可以自由地忽略它。根据实现认为最好的方式，实现可能会决定满足请求，可能会部分满足（例如，减小容量但不是完全减小），或者可能会完全忽略请求。
这是一个例子
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "Capacity: " << v.capacity() << " Length:"	<< v.size() << '\n';
}

int main()
{

	std::vector<int> v(1000); // allocate room for 1000 elements
	printCapLen(v);

	v.resize(0); // resize to 0 elements
	printCapLen(v);

	v.shrink_to_fit();
	printCapLen(v);

	return 0;
}
在作者的机器上，这会产生以下结果
Capacity: 1000  Length: 1000
Capacity: 1000  Length: 0
Capacity: 0  Length: 0
如您所见，当调用
v.shrink_to_fit()
时，向量将其容量重新分配为 0，从而释放了 1000 个元素的内存。
小测验时间
问题 #1
std::vector 的长度和容量代表什么？
显示答案
长度是当前正在使用的元素数量。
容量是已分配存储空间的元素数量。
为什么长度和容量是独立的值？
显示答案
单独跟踪容量是为了当长度改变时，向量可以避免一些重新分配。
std::vector
的有效索引是基于长度还是容量？
显示答案
长度。
下一课
16.11
std::vector 和栈行为
返回目录
上一课
16.9
使用枚举器进行数组索引和长度