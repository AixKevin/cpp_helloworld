# 16.11 — std::vector 和栈行为

16.11 — std::vector 和栈行为
Alex
2023 年 9 月 11 日下午 2:51 PDT
2024 年 10 月 6 日
考虑这样一种情况：你正在编写一个程序，用户将输入一个值列表（例如一堆考试分数）。在这种情况下，他们将输入的值的数量在编译时是未知的，并且每次运行程序时都可能不同。你将这些值存储在
std::vector
中以供显示和/或处理。
根据我们到目前为止的讨论，有几种方法可以解决这个问题
首先，你可以询问用户有多少条目，创建一个该长度的向量，然后要求用户输入该数量的值。
这并不是一个糟糕的方法，但它要求用户提前知道他们有多少条目，并且在计数时没有犯错。手动计数十多个或二十多个项目可能很乏味——而且，当我们可以替用户完成计数时，为什么要要求用户计数呢？
或者，我们可以假设用户不想输入超过某个数量的值（例如 30），并创建一个（或调整大小）具有那么多元素的向量。然后我们可以要求用户输入数据，直到他们完成（或直到他们达到 30 个输入值）。因为向量的长度旨在表示已使用的元素数量，所以我们可以将向量的大小调整为用户实际输入的值的数量。
这种方法的缺点是用户只能输入 30 个值，我们不知道这是否太多或太少。如果用户想输入更多值，那很遗憾。
我们可以通过添加一些逻辑来解决这个问题，即当用户达到最大值数量时，将向量的大小调整得更大。但这表示我们现在必须将数组大小管理与程序逻辑混合在一起，这将显著增加程序的复杂性（这不可避免地会导致错误）。
这里真正的问题是，我们试图猜测用户可能输入多少元素，以便我们可以适当地管理向量的大小。对于事先真正不知道要输入多少元素的情况，有更好的方法。
但在此之前，我们需要简要地旁白一下。
什么是栈？
类比时间！考虑自助餐厅里的一叠盘子。由于某种未知的原因，这些盘子特别重，每次只能拿起一个。由于盘子堆叠且很重，你只能通过以下两种方式修改盘子叠：
在叠的顶部放一个新盘子（如果存在的话，会遮住下面的盘子）
从叠的顶部移除最上面的盘子（如果存在的话，会露出下面的盘子）
不允许从叠的中间或底部添加或移除盘子，因为这需要一次拿起多个盘子。
将项目添加到栈中和从栈中移除项目的顺序可以描述为
后进先出（LIFO）
。最后添加到栈中的盘子将是第一个被移除的盘子。
编程中的栈
在编程中，
栈
是一种容器数据类型，其中元素的插入和删除以 LIFO 方式进行。这通常通过两个名为
push
和
pop
的操作来实现
操作名称
行为
必需？
备注
Push
将新元素放在栈顶
是
Pop
从栈中移除顶部元素
是
可能返回移除的元素或 void
许多栈实现还可选地支持其他有用的操作
操作名称
行为
必需？
备注
Top 或 Peek
获取栈顶元素
可选
不移除项目
Empty
确定栈是否没有元素
可选
Size
栈中有多少元素的计数
可选
栈在编程中很常见。在课程
3.9 -- 使用集成调试器：调用栈
中，我们讨论了调用栈，它跟踪已调用的函数。调用栈是……一个栈！（我知道，这个揭示有点令人失望）。当一个函数被调用时，一个包含该函数信息的条目被添加到调用栈的顶部。当函数返回时，包含该函数信息的条目从调用栈的顶部移除。通过这种方式，调用栈的顶部始终表示当前正在执行的函数，并且每个后续条目表示之前正在执行的函数。
例如，这是一个显示压入和弹出栈如何工作的简短序列
(Stack: empty)
Push 1 (Stack: 1)
Push 2 (Stack: 1 2)
Push 3 (Stack: 1 2 3)
Pop    (Stack: 1 2)
Push 4 (Stack: 1 2 4)
Pop    (Stack: 1 2)
Pop    (Stack: 1)
Pop    (Stack: empty)
C++ 中的栈
在某些语言中，栈被实现为自己的独立容器类型（与其他容器分开）。然而，这可能相当受限。考虑一下我们希望在不修改栈的情况下打印栈中的所有值的情况。纯栈接口不提供直接的方法来做到这一点。
在 C++ 中，栈式操作（作为成员函数）被添加到现有的标准库容器类中，这些类支持在一个端点高效地插入和移除元素（
std::vector
、
std::deque
和
std::list
）。这使得这些容器除了其固有的能力之外，还可以用作栈。
题外话…
盘子堆的类比很好，但我们可以做一个更好的类比来帮助我们理解如何使用数组实现栈。与其考虑一个当前盘子数量可变的盘子堆，不如考虑一列信箱，它们都堆叠在一起。每个信箱只能放一个物品，并且所有信箱一开始都是空的。每个信箱都钉在它下面的信箱上，并且列的顶部被有毒的尖刺覆盖，因此不能在任何地方插入新的信箱。
如果我们不能改变邮箱的数量，我们如何获得类似栈的行为？
首先，我们使用一个标记（比如一张便利贴）来记录栈顶在哪里——这总是最低的空邮箱。一开始，栈是空的，所以标记放在最下面的邮箱上。
当我们向邮箱栈中推入一个项目时，我们将其放入标记的邮箱中（即最低的空邮箱），并将标记向上移动一个邮箱。当我们从栈中弹出一个项目时，我们将标记向下移动一个邮箱（使其指向顶部非空邮箱），并从该邮箱中移除该项目，使其现在为空。
标记下方的项目被认为是“在栈上”。标记处或标记上方的项目不在栈上。
现在，我们将标记称为
length
，将邮箱数量称为
capacity
……
在本课的其余部分，我们将研究
std::vector
的栈接口如何工作，然后我们将通过展示它如何帮助我们解决本课开头提出的挑战来结束。
使用
std::vector
的栈行为
std::vector
中的栈行为通过以下成员函数实现
函数名称
栈操作
行为
备注
push_back()
Push
将新元素放在栈顶
将元素添加到向量末尾
pop_back()
Pop
从栈中移除顶部元素
返回 void，移除向量末尾的元素
back()
Top 或 Peek
获取栈顶元素
不移除项目
emplace_back()
Push
push_back() 的另一种形式，可能更高效（见下文）
将元素添加到向量末尾
让我们看一个使用其中一些函数的示例
#include <iostream>
#include <vector>

void printStack(const std::vector<int>& stack)
{
	if (stack.empty()) // if stack.size == 0
		std::cout << "Empty";

	for (auto element : stack)
		std::cout << element << ' ';

	// \t is a tab character, to help align the text
	std::cout << "\tCapacity: " << stack.capacity() << "  Length " << stack.size() << "\n";
}

int main()
{
	std::vector<int> stack{}; // empty stack

	printStack(stack);

	stack.push_back(1); // push_back() pushes an element on the stack
	printStack(stack);

	stack.push_back(2);
	printStack(stack);

	stack.push_back(3);
	printStack(stack);

	std::cout << "Top: " << stack.back() << '\n'; // back() returns the last element

	stack.pop_back(); // pop_back() pops an element off the stack
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	return 0;
}
在 GCC 或 Clang 上，这会打印
Empty   Capacity: 0  Length: 0
1       Capacity: 1  Length: 1
1 2     Capacity: 2  Length: 2
1 2 3   Capacity: 4  Length: 3
Top:3
1 2     Capacity: 4  Length: 2
1       Capacity: 4  Length: 1
Empty   Capacity: 4  Length: 0
请记住，长度是向量中元素的数量，在本例中，它是我们栈中元素的数量。
与下标运算符
operator[]
或
at()
成员函数不同，
push_back()
（和
emplace_back()
）会增加向量的长度，并且如果容量不足以插入值，则会导致重新分配。
在上面的示例中，向量被重新分配了 3 次（从容量 0 到 1，1 到 2，2 到 4）。
关键见解
push_back()
和
emplace_back()
将增加
std::vector
的长度，并且如果容量不足以插入值，则会导致重新分配。
因 push 而产生的额外容量
在上面的输出中，请注意当第三次重新分配发生时，容量从 2 跳到 4（即使我们只压入了一个元素）。当压入触发重新分配时，
std::vector
通常会分配一些额外容量，以便在下次添加元素时无需再次触发重新分配。
分配多少额外容量取决于编译器对
std::vector
的实现，不同的编译器通常会做不同的事情
GCC 和 Clang 会将当前容量加倍。当最后一次调整大小被触发时，容量从 2 倍增到 4。
Visual Studio 2022 将当前容量乘以 1.5。当最后一次调整大小被触发时，容量从 2 变为 3。
因此，上述程序的输出可能会因您使用的编译器而略有不同。
调整向量大小不适用于栈行为
重新分配向量在计算上是昂贵的（与向量的长度成比例），因此我们希望在合理的情况下避免重新分配。在上面的示例中，如果我们在程序开始时手动将向量大小调整为容量 3，我们可以避免向量被重新分配 3 次。
让我们看看如果我们将上面示例中的第 18 行更改为以下内容会发生什么
std::vector<int> stack(3); // parenthesis init to set vector's capacity to 3
现在，当我们再次运行程序时，我们得到以下输出
0 0 0 	Capacity: 3  Length 3
0 0 0 1 	Capacity: 6  Length 4
0 0 0 1 2 	Capacity: 6  Length 5
0 0 0 1 2 3 	Capacity: 6  Length 6
Top: 3
0 0 0 1 2 	Capacity: 6  Length 5
0 0 0 1 	Capacity: 6  Length 4
0 0 0 	Capacity: 6  Length 3
那不对——我们的栈开头不知何故有一堆
0
值！这里的问题是，括号初始化（用于设置向量的初始大小）和
resize()
函数同时设置了容量和长度。我们的向量以容量 3 开始（这是我们想要的），但长度也被设置为 3。所以我们的向量以 3 个值为 0 的元素开始。我们稍后推入的元素会推到这些初始元素之上。
当我们要使用下标访问元素时（因为我们的索引需要小于长度才能有效），
resize()
成员函数更改向量长度是没问题的，但当我们把向量用作栈时，它会导致问题。
我们真正想要的是一种在不改变长度（这会附带地向栈中添加新元素）的情况下改变容量（以避免将来的重新分配）的方法。
reserve()
成员函数改变容量（但不改变长度）
reserve()
成员函数可用于重新分配
std::vector
而不改变当前长度。
这是之前的相同示例，但增加了对
reserve()
的调用来设置容量
#include <iostream>
#include <vector>

void printStack(const std::vector<int>& stack)
{
	if (stack.empty()) // if stack.size == 0
		std::cout << "Empty";

	for (auto element : stack)
		std::cout << element << ' ';

	// \t is a tab character, to help align the text
	std::cout << "\tCapacity: " << stack.capacity() << "  Length " << stack.size() << "\n";
}

int main()
{
	std::vector<int> stack{};

	printStack(stack);

	stack.reserve(6); // reserve space for 6 elements (but do not change length)
	printStack(stack);

	stack.push_back(1);
	printStack(stack);

	stack.push_back(2);
	printStack(stack);

	stack.push_back(3);
	printStack(stack);

	std::cout << "Top: " << stack.back() << '\n';

	stack.pop_back();
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	return 0;
}
在作者的机器上，这会打印出
Empty   Capacity: 0  Length: 0
Empty   Capacity: 6  Length: 0
1       Capacity: 6  Length: 1
1 2     Capacity: 6  Length: 2
1 2 3   Capacity: 6  Length: 3
Top: 3
1 2     Capacity: 6  Length: 2
1       Capacity: 6  Length: 1
Empty   Capacity: 6  Length: 0
你可以看到，调用
reserve(6)
将容量更改为 6，但没有影响长度。不再发生重新分配，因为
std::vector
足够大，可以容纳我们压入的所有元素。
关键见解
resize()
成员函数改变向量的长度和容量（如果需要）。
reserve()
成员函数只改变容量（如果需要）
提示
要增加
std::vector
中的元素数量
当通过索引访问向量时，使用
resize()
。这会改变向量的长度，以便您的索引有效。
当使用栈操作访问向量时，使用
reserve()
。这会增加容量而不改变向量的长度。
push_back()
vs
emplace_back()
push_back()
和
emplace_back()
都将一个元素压入栈中。如果被压入的对象已经存在，
push_back()
和
emplace_back()
是等效的，并且应首选
push_back()
。
然而，在我们需要创建临时对象（与向量元素类型相同）以将其推入向量的情况下，
emplace_back()
可以更高效
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Foo
{
private:
    std::string m_a{};
    int m_b{};

public:
    Foo(std::string_view a, int b)
        : m_a { a }, m_b { b }
        {}

    explicit Foo(int b)
        : m_a {}, m_b { b }
        {};
};

int main()
{
	std::vector<Foo> stack{};

	// When we already have an object, push_back and emplace_back are similar in efficiency
	Foo f{ "a", 2 };
	stack.push_back(f);    // prefer this one
	stack.emplace_back(f);

	// When we need to create a temporary object to push, emplace_back is more efficient
	stack.push_back({ "a", 2 }); // creates a temporary object, and then copies it into the vector
	stack.emplace_back("a", 2);  // forwards the arguments so the object can be created directly in the vector (no copy made)

	// push_back won't use explicit constructors, emplace_back will
	stack.push_back({ 2 }); // compile error: Foo(int) is explicit
	stack.emplace_back(2);  // ok
    
	return 0;
}
在上面的例子中，我们有一个
Foo
对象向量。使用
push_back({ "a", 2 })
，我们正在创建并初始化一个临时的
Foo
对象，然后将其复制到向量中。对于复制开销大的类型（如
std::string
），这种复制可能导致性能下降。
使用
emplace_back()
，我们不需要创建要传递的临时对象。相反，我们传递用于创建临时对象的参数，然后
emplace_back()
将它们（使用一种称为完美转发的特性）转发到向量中，在那里它们用于在向量内部创建和初始化对象。这避免了本来会发生的复制。
值得注意的是，
push_back()
不会使用显式构造函数，而
emplace_back()
会。这使得
emplace_back
更危险，因为它更容易意外地调用显式构造函数来执行一些没有意义的转换。
在 C++20 之前，
emplace_back()
不适用于聚合初始化。
最佳实践
当创建新的临时对象添加到容器中，或者需要访问显式构造函数时，首选
emplace_back()
。
否则，首选
push_back()
。
本文
对此最佳实践有更多解释。
使用栈操作解决我们的挑战
现在应该很清楚我们应该如何解决本课开头提出的挑战了。如果事先不知道要向
std::vector
中添加多少元素，使用栈函数插入这些元素是最好的方法。
这是一个例子
#include <iostream>
#include <limits>
#include <vector>

int main()
{
	std::vector<int> scoreList{};

	while (true)
	{
		std::cout << "Enter a score (or -1 to finish): ";
		int x{};
		std::cin >> x;

		if (!std::cin) // handle bad input
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			continue;
		}

		// If we're done, break out of loop
		if (x == -1)
			break;

		// The user entered a valid element, so let's push it on the vector
		scoreList.push_back(x);
	}

	std::cout << "Your list of scores: \n";

	for (const auto& score : scoreList)
		std::cout << score << ' ';

	return 0;
}
这个程序让用户输入考试分数，并将每个分数添加到向量中。用户完成添加分数后，向量中的所有值都会被打印出来。
请注意，在这个程序中，我们完全不需要进行任何计数、索引或处理数组长度！我们可以只关注我们希望程序执行的逻辑，让向量处理所有存储问题！
小测验时间
问题 #1
编写一个程序，执行压入和弹出值，并输出以下序列
(Stack: empty)
Push 1 (Stack: 1)
Push 2 (Stack: 1 2)
Push 3 (Stack: 1 2 3)
Pop    (Stack: 1 2)
Push 4 (Stack: 1 2 4)
Pop    (Stack: 1 2)
Pop    (Stack: 1)
Pop    (Stack: empty)
显示答案
#include <iostream>
#include <vector>

void printStackValues(const std::vector<int>& v)
{
    std::cout << "\t(Stack:";
    
    for (auto e : v)
        std::cout << ' ' << e;

    if (v.empty()) // if v.size == 0
        std::cout << " empty";

    std::cout << ")\n";
}

void pushAndPrint(std::vector<int>& v, int val)
{
    v.push_back(val);
    std::cout << "Push " << val;
    printStackValues(v);
}

void popAndPrint(std::vector<int>& v)
{
    v.pop_back();
    std::cout << "Pop ";
    printStackValues(v);
}

int main()
{
    std::vector<int> v {};

    printStackValues(v);

    pushAndPrint(v, 1);
    pushAndPrint(v, 2);
    pushAndPrint(v, 3);
    popAndPrint(v);
    pushAndPrint(v, 4);
    popAndPrint(v);
    popAndPrint(v);
    popAndPrint(v);

    return 0;
}
下一课
16.12
std::vector<bool>
返回目录
上一课
16.10
std::vector 的大小调整和容量