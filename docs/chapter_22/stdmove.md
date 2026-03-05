# 22.4 — std::move

22.4 — std::move
Alex
2017年3月4日，太平洋标准时间晚上8:21
2024年5月8日
一旦你开始更频繁地使用移动语义，你就会发现一些情况，你想要调用移动语义，但是你必须处理的对象是左值，而不是右值。以下面的交换函数为例：
#include <iostream>
#include <string>

template <typename T>
void mySwapCopy(T& a, T& b) 
{ 
	T tmp { a }; // invokes copy constructor
	a = b; // invokes copy assignment
	b = tmp; // invokes copy assignment
}

int main()
{
	std::string x{ "abc" };
	std::string y{ "de" };

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	mySwapCopy(x, y);

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	return 0;
}
传入两个T类型（本例中为std::string）的对象，该函数通过进行三次复制来交换它们的值。因此，该程序会打印：
x: abc
y: de
x: de
y: abc
正如我们在上一课中展示的，进行复制效率低下。而此版本的交换操作进行了3次复制。这导致了大量的字符串创建和销毁，非常缓慢。
然而，这里不需要进行复制。我们真正想要做的只是交换a和b的值，这同样可以通过3次移动来完成！因此，如果我们将复制语义切换到移动语义，我们可以让我们的代码性能更好。
但是如何做到呢？这里的问题是参数a和b是左值引用，而不是右值引用，所以我们无法调用移动构造函数和移动赋值运算符来代替复制构造函数和复制赋值。默认情况下，我们得到的是复制构造函数和复制赋值的行为。我们该怎么办？
std::move
在C++11中，std::move是一个标准库函数，它将（使用static_cast）其参数转换为右值引用，以便可以调用移动语义。因此，我们可以使用std::move将左值转换为优先被移动而不是被复制的类型。std::move在utility头文件中定义。
这是与上面相同的程序，但有一个mySwapMove()函数，它使用std::move将我们的左值转换为右值，以便我们可以调用移动语义：
#include <iostream>
#include <string>
#include <utility> // for std::move

template <typename T>
void mySwapMove(T& a, T& b) 
{ 
	T tmp { std::move(a) }; // invokes move constructor
	a = std::move(b); // invokes move assignment
	b = std::move(tmp); // invokes move assignment
}

int main()
{
	std::string x{ "abc" };
	std::string y{ "de" };

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	mySwapMove(x, y);

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	return 0;
}
这会打印出与上面相同的结果：
x: abc
y: de
x: de
y: abc
但效率要高得多。当tmp被初始化时，我们没有复制x，而是使用std::move将左值变量x转换为右值。由于参数是右值，因此调用了移动语义，x被移动到tmp中。
再经过几次交换，变量x的值已移至y，变量y的值已移至x。
另一个例子
我们还可以使用std::move来填充容器（例如std::vector）的元素，其中包含左值。
在以下程序中，我们首先使用复制语义向向量添加一个元素。然后，我们使用移动语义向向量添加一个元素。
#include <iostream>
#include <string>
#include <utility> // for std::move
#include <vector>

int main()
{
	std::vector<std::string> v;

	// We use std::string because it is movable (std::string_view is not)
	std::string str { "Knock" };

	std::cout << "Copying str\n";
	v.push_back(str); // calls l-value version of push_back, which copies str into the array element
	
	std::cout << "str: " << str << '\n';
	std::cout << "vector: " << v[0] << '\n';

	std::cout << "\nMoving str\n";

	v.push_back(std::move(str)); // calls r-value version of push_back, which moves str into the array element
	
	std::cout << "str: " << str << '\n'; // The result of this is indeterminate
	std::cout << "vector:" << v[0] << ' ' << v[1] << '\n';

	return 0;
}
在作者的机器上，此程序打印：
Copying str
str: Knock
vector: Knock

Moving str
str:
vector: Knock Knock
在第一种情况下，我们向push_back()传递了一个左值，因此它使用复制语义向向量添加了一个元素。因此，str中的值保持不变。
在第二种情况下，我们向push_back()传递了一个右值（实际上是通过std::move转换的左值），因此它使用移动语义向向量添加了一个元素。这更高效，因为向量元素可以窃取字符串的值，而无需复制它。
被移动的对象的有效状态可能是不确定的
当我们从临时对象移动值时，被移动对象的剩余值无关紧要，因为临时对象无论如何都会立即被销毁。但是，我们对左值对象使用了std::move()会怎样呢？因为我们可以在它们的值被移动后继续访问这些对象（例如，在上面的示例中，我们在str被移动后打印它的值），所以了解它们剩余的值是很有用的。
这里有两种思想流派。一个流派认为，被移动的对象应该重置回某个默认/零状态，即对象不再拥有资源。我们在上面看到了一个例子，其中 `str` 已被清除为空字符串。
另一个学派认为我们应该做最方便的事情，并且如果清除被移动的对象不方便，则不强求。
那么在这种情况下，标准库是如何做的呢？关于这一点，C++标准规定：“除非另有说明，否则[C++标准库中定义的类型]的被移动对象应处于有效但未指定的状态。”
在上面的示例中，当作者在对 `str` 调用 `std::move` 后打印 `str` 的值时，它打印了一个空字符串。然而，这不是必需的，它可能打印任何有效的字符串，包括空字符串、原始字符串或任何其他有效字符串。因此，我们应该避免使用被移动对象的值，因为结果将是实现定义的。
在某些情况下，我们希望重用其值已被移动的对象（而不是分配新对象）。例如，在mySwapMove()的实现中，我们首先将资源从`a`中移出，然后将另一个资源移入`a`。这没有问题，因为在我们将`a`的资源移出和将一个确定的新值赋给`a`之间，我们从未使用过`a`的值。
对于一个被移动的对象，调用任何不依赖于对象当前值的函数都是安全的。这意味着我们可以设置或重置被移动对象的值（使用 `operator=`，或任何 `clear()` 或 `reset()` 成员函数）。我们还可以测试被移动对象的状态（例如，使用 `empty()` 查看对象是否有值）。然而，我们应该避免使用像 `operator[]` 或 `front()` 这样的函数（它返回容器中的第一个元素），因为这些函数依赖于容器有元素，而一个被移动的容器可能有没有元素。
关键见解
`std::move()`向编译器提示程序员不再需要对象的值。仅对要移动其值的持久对象使用`std::move()`，并且不要对此对象在该点之后的值做任何假设。在当前值被移动后，给一个被移动的对象一个新值（例如，使用`operator=`）是可以的。
std::move 在其他地方有什么用？
std::move 在对元素数组进行排序时也很有用。许多排序算法（例如选择排序和冒泡排序）通过交换元素对来工作。在之前的课程中，我们不得不求助于复制语义来完成交换。现在我们可以使用移动语义，它更高效。
如果我们要将一个智能指针管理的内容移动到另一个智能指针，它也可能很有用。
相关内容
`std::move()`有一个有用的变体，叫做`std::move_if_noexcept()`，如果对象有一个`noexcept`移动构造函数，它会返回一个可移动的右值，否则它会返回一个可复制的左值。我们在
第27.10课——std::move_if_noexcept
中介绍了这一点。
总结
每当我们需要将左值视为右值以调用移动语义而不是复制语义时，都可以使用std::move。
下一课
22.5
std::unique_ptr
返回目录
上一课
22.3
移动构造函数和移动赋值