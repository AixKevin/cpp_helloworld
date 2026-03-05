# 16.2 — std::vector 和列表构造函数介绍

16.2 — std::vector 和列表构造函数介绍
Alex
2015年9月28日，下午4:34 PDT
2024年12月26日
在上一课
16.1 -- 容器和数组简介
中，我们介绍了容器和数组。在本课中，我们将介绍本章其余部分将重点关注的数组类型：
std::vector
。我们还将解决上一课中引入的可伸缩性挑战的一部分。
std::vector
简介
std::vector
是 C++ 标准容器库中实现数组的容器类之一。
std::vector
在 <vector> 头文件中定义为一个类模板，带有定义元素类型的模板类型参数。因此，
std::vector<int>
声明了一个元素类型为
int
的
std::vector
。
实例化
std::vector
对象非常简单
#include <vector>

int main()
{
	// Value initialization (uses default constructor)
	std::vector<int> empty{}; // vector containing 0 int elements

	return 0;
}
变量
empty
被定义为一个元素类型为
int
的
std::vector
。由于我们在这里使用了值初始化，我们的向量将从空开始（即没有元素）。
现在一个没有元素的向量可能看起来没什么用，但我们将在未来的课程中再次遇到它（尤其是
16.11 -- std::vector 和栈行为
）。
用值列表初始化
std::vector
由于容器的目标是管理一组相关值，因此我们通常希望用这些值来初始化我们的容器。我们可以通过使用列表初始化来指定我们想要的初始化值。例如
#include <vector>

int main()
{
	// List construction (uses list constructor)
	std::vector<int> primes{ 2, 3, 5, 7 };          // vector containing 4 int elements with values 2, 3, 5, and 7
	std::vector vowels { 'a', 'e', 'i', 'o', 'u' }; // vector containing 5 char elements with values 'a', 'e', 'i', 'o', and 'u'.  Uses CTAD (C++17) to deduce element type char (preferred).

	return 0;
}
对于
primes
，我们明确指定我们想要一个元素类型为
int
的
std::vector
。由于我们提供了 4 个初始化值，
primes
将包含 4 个元素，其值分别为
2
、
3
、
5
和
7
。
对于
vowels
，我们没有明确指定元素类型。相反，我们使用 C++17 的 CTAD（类模板参数推导）让编译器从初始化器推导出元素类型。由于我们提供了 5 个初始化值，
vowels
将包含 5 个元素，其值分别为
'a'
、
'e'
、
'i'
、
'o'
和
'u'
。
列表构造函数和初始化列表
让我们更详细地讨论一下上面是如何工作的。
在课程
13.8 -- 结构体聚合初始化
中，我们将初始化列表定义为用逗号分隔的值的括号列表（例如
{ 1, 2, 3 }
）。
容器通常有一个特殊的构造函数，称为**列表构造函数**，它允许我们使用初始化列表构造容器实例。列表构造函数执行三件事
确保容器有足够的存储空间来容纳所有初始化值（如果需要）。
将容器的长度设置为初始化列表中元素的数量（如果需要）。
按顺序将元素初始化为初始化列表中的值。
因此，当我们为容器提供一个值初始化列表时，列表构造函数被调用，并且容器使用该值列表构造！
最佳实践
使用带有值初始化列表的列表初始化来构造一个具有这些元素值的容器。
相关内容
我们将在课程
23.7 -- std::initializer_list
中讨论如何为程序定义的类添加列表构造函数。
使用下标运算符 (operator[]) 访问数组元素
既然我们已经创建了一个元素数组……我们如何访问它们呢？
让我们暂时使用一个类比。考虑一组并排的相同邮箱。为了更容易识别邮箱，每个邮箱前面都画有一个数字。第一个邮箱编号为 0，第二个编号为 1，依此类推……所以如果你被告知把东西放进编号为 0 的邮箱，你就会知道那指的是第一个邮箱。
在 C++ 中，访问数组元素最常用的方法是使用数组名称和下标运算符（
operator[]
）。要选择特定元素，我们在下标运算符的方括号内提供一个整数值，该整数值标识我们要选择的元素。这个整数值称为**下标**（或非正式地称为**索引**）。就像我们的邮箱一样，第一个元素使用索引 0 访问，第二个使用索引 1 访问，依此类推……
例如，
primes[0]
将返回
prime
数组中索引为
0
的元素（第一个元素）。下标运算符返回实际元素的引用，而不是副本。一旦我们访问了数组元素，我们就可以像使用普通对象一样使用它（例如，给它赋值，输出它，等等……）。
因为索引从 0 而不是 1 开始，所以我们说 C++ 中的数组是**零基**的。这可能会令人困惑，因为我们习惯于从 1 开始计数对象。
关键见解
索引实际上是与数组第一个元素的距离（偏移量）。
如果你从数组的第一个元素开始移动 0 个元素，你仍然在第一个元素上。因此索引 0 是第一个元素。
如果你从数组的第一个元素开始移动 1 个元素，你现在在第二个元素上。因此索引 1 是第二个元素。
我们将在课程
17.9 -- 指针算术和下标
中讨论索引是相对距离（而不是绝对位置）。
这也可能导致一些语言上的歧义，因为当我们谈论数组元素 1 时，可能不清楚我们指的是第一个数组元素（索引为 0）还是第二个数组元素（索引为 1）。通常，我们将根据位置而不是索引来谈论数组元素（因此“第一个元素”是索引为 0 的元素）。
这是一个例子
#include <iostream>
#include <vector>

int main()
{
    std::vector primes { 2, 3, 5, 7, 11 }; // hold the first 5 prime numbers (as int)

    std::cout << "The first prime number is: " << primes[0] << '\n';
    std::cout << "The second prime number is: " << primes[1] << '\n';
    std::cout << "The sum of the first 5 primes is: " << primes[0] + primes[1] + primes[2] + primes[3] + primes[4] << '\n';

    return 0;
}
这会打印
The first prime number is: 2
The second prime number is: 3
The sum of the first 5 primes is: 28
通过使用数组，我们不再需要定义 5 个不同名称的变量来保存我们的 5 个质数值。相反，我们可以定义一个包含 5 个元素的单个数组（
primes
），只需更改索引值即可访问不同的元素！
我们将在下一课
16.3 -- std::vector 和无符号长度及下标问题
中详细讨论
operator[]
和其他一些访问数组元素的方法。
下标越界
在索引数组时，提供的索引必须选择数组的有效元素。也就是说，对于长度为 N 的数组，下标必须是 0 到 N-1（包括）之间的值。
operator[]
不执行任何**边界检查**，这意味着它不检查索引是否在 0 到 N-1（包括）的范围内。向
operator[]
传递无效索引将导致未定义行为。
记住不要使用负下标相当容易。记住没有索引为 N 的元素则不那么容易！数组的最后一个元素索引为 N-1，因此使用索引 N 将导致编译器尝试访问数组末尾之后的一个元素。
提示
在一个包含 N 个元素的数组中，第一个元素的索引为 0，第二个元素的索引为 1，最后一个元素的索引为 N-1。没有索引为 N 的元素！
使用 N 作为下标将导致未定义行为（因为这实际上是在尝试访问第 N+1 个元素，它不是数组的一部分）。
提示
一些编译器（如 Visual Studio）提供运行时断言来检查索引是否有效。在这种情况下，如果在调试模式下提供了无效索引，程序将断言退出。在发布模式下，断言被编译掉，因此没有性能损失。
数组在内存中是连续的
数组的一个决定性特征是元素总是连续分配在内存中，这意味着元素在内存中都是相邻的（它们之间没有间隙）。
举例说明这一点
#include <iostream>
#include <vector>

int main()
{
    std::vector primes { 2, 3, 5, 7, 11 }; // hold the first 5 prime numbers (as int)

    std::cout << "An int is " << sizeof(int) << " bytes\n";
    std::cout << &(primes[0]) << '\n';
    std::cout << &(primes[1]) << '\n';
    std::cout << &(primes[2]) << '\n';

    return 0;
}
在作者的机器上，上面程序的一次运行产生了以下结果
An int is 4 bytes
00DBF720
00DBF724
00DBF728
您会注意到这些 int 元素的内存地址相隔 4 字节，与作者机器上
int
的大小相同。
这意味着数组没有每元素开销。它还允许编译器快速计算数组中任何元素的地址。
相关内容
我们将在课程
17.9 -- 指针算术和下标
中讨论下标背后的数学原理。
数组是少数允许**随机访问**的容器类型之一，这意味着容器中的任何元素都可以直接访问（与顺序访问相对，后者必须按特定顺序访问元素）。对数组元素的随机访问通常是高效的，并且使数组非常易于使用。这是数组通常优于其他容器的主要原因。
构造指定长度的
std::vector
考虑我们希望用户输入 10 个值并将其存储在
std::vector
中的情况。在这种情况下，我们需要一个长度为 10 的
std::vector
，而我们还没有任何值可以放入
std::vector
。我们如何解决这个问题？
我们可以创建一个
std::vector
并使用一个包含 10 个占位符值的初始化列表来初始化它
std::vector<int> data { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; // vector containing 10 int values
但这有很多缺点。它需要大量的输入。不容易看出有多少个初始化器。而且如果以后我们决定需要不同数量的值，它也不容易更新。
幸运的是，
std::vector
有一个显式构造函数（
explicit std::vector<T>(std::size_t)
），它接受一个单一的
std::size_t
值，定义要构造的
std::vector
的长度
std::vector<int> data( 10 ); // vector containing 10 int elements, value-initialized to 0
每个创建的元素都经过值初始化，对于
int
来说是零初始化（对于类类型则调用默认构造函数）。
然而，使用这个构造函数有一个不明显的地方：它必须使用直接初始化来调用。
非空初始化列表优先选择列表构造函数
要理解为什么前一个构造函数必须使用直接初始化来调用，请考虑以下定义
std::vector<int> data{ 10 }; // what does this do?
有两个不同的构造函数与此初始化匹配
{ 10 }
可以解释为一个初始化列表，并与列表构造函数匹配，以构造一个长度为 1、值为 10 的向量。
{ 10 }
可以解释为单个括号初始化值，并与
std::vector<T>(std::size_t)
构造函数匹配，以构造一个长度为 10、元素值为 0 的向量。
通常，当一个类类型定义匹配多个构造函数时，匹配被认为是模糊的，并导致编译错误。然而，C++ 对这种情况有一个特殊规则：当初始化列表非空时，匹配的列表构造函数将优先于其他匹配的构造函数被选择。如果没有这个规则，列表构造函数将与接受单一类型参数的任何构造函数产生模糊匹配。
由于
{ 10 }
可以解释为一个初始化列表，并且
std::vector
有一个列表构造函数，因此在这种情况下列表构造函数优先。
关键见解
使用初始化列表构造类类型对象时
如果初始化列表为空，则默认构造函数优先于列表构造函数。
如果初始化列表非空，则匹配的列表构造函数优先于其他匹配的构造函数。
为了进一步阐明各种初始化情况下的行为，让我们看看使用复制初始化、直接初始化和列表初始化的类似情况
// Copy init
	std::vector<int> v1 = 10;     // 10 not an initializer list, copy init won't match explicit constructor: compilation error

	// Direct init
	std::vector<int> v2(10);      // 10 not an initializer list, matches explicit single-argument constructor

	// List init
	std::vector<int> v3{ 10 };    // { 10 } interpreted as initializer list, matches list constructor

	// Copy list init
	std::vector<int> v4 = { 10 }; // { 10 } interpreted as initializer list, matches list constructor
	std::vector<int> v5({ 10 });  // { 10 } interpreted as initializer list, matches list constructor

        // Default init
        std::vector<int> v6 {};       // {} is empty initializer list, matches default constructor
        std::vector<int> v7 = {};     // {} is empty initializer list, matches default constructor
在情况
v1
中，初始化值
10
不是初始化列表，因此列表构造函数不匹配。单参数构造函数
explicit std::vector<T>(std::size_t)
也不匹配，因为复制初始化不匹配显式构造函数。由于没有构造函数匹配，这是一个编译错误。
在情况
v2
中，初始化值
10
不是初始化列表，因此列表构造函数不匹配。单参数构造函数
explicit std::vector<T>(std::size_t)
匹配，因此选择单参数构造函数。
在情况
v3
（列表初始化）中，
{ 10 }
可以与列表构造函数或
explicit std::vector<T>(std::size_t)
匹配。列表构造函数优先于其他匹配构造函数并被选中。
在情况
v4
（复制列表初始化）中，
{ 10 }
可以与列表构造函数匹配（它是一个非显式构造函数，因此可以与复制初始化一起使用）。列表构造函数被选中。
情况
v5
令人惊讶地是复制列表初始化的替代语法（而不是直接初始化），与
v4
相同。
这是 C++ 初始化的一些缺点之一：如果存在列表构造函数，
{ 10 }
将匹配列表构造函数；如果不存在列表构造函数，则匹配单参数构造函数。这意味着您得到的行为取决于是否存在列表构造函数！通常您可以假设容器具有列表构造函数。
警告
如果一个类没有列表构造函数，但后来添加了一个，这将改变所有使用非空初始化列表初始化的对象的构造函数调用方式。
v6
和
v7
都使用空初始化列表进行初始化。在这种情况下，默认构造函数优先。
总而言之，列表初始化器通常旨在允许我们使用元素值列表初始化容器，并应用于此目的。这正是我们大多数时候想要的。因此，如果
10
旨在成为元素值，则
{ 10 }
是合适的。如果
10
旨在成为容器的非列表构造函数的参数，请使用直接初始化。
最佳实践
当使用非元素值的初始化器构造容器（或任何具有列表构造函数的类型）时，请使用直接初始化。
提示
当
std::vector
是类类型的成员时，如何提供一个将
std::vector
的长度设置为某个初始值的默认初始化器并不明显
#include <vector>

struct Foo
{
    std::vector<int> v1(8); // compile error: direct initialization not allowed for member default initializers
};
这不起作用，因为成员默认初始化器不允许直接（括号）初始化。
为类类型的成员提供默认初始化器时
我们必须使用复制初始化或列表初始化（直接或复制）。
不允许 CTAD（因此我们必须明确指定元素类型）。
答案如下
struct Foo
{
    std::vector<int> v{ std::vector<int>(8) }; // ok 
};
这会创建一个容量为 8 的
std::vector
，然后将其用作
v
的初始化器。
const 和 constexpr
std::vector
std::vector
类型的对象可以设置为
const
#include <vector>

int main()
{
    const std::vector<int> prime { 2, 3, 5, 7, 11 }; // prime and its elements cannot be modified

    return 0;
}
一个
const std::vector
必须被初始化，然后不能被修改。这个向量的元素被视为 const。
std::vector
的元素类型不能定义为 const（例如
std::vector<const int>
是不允许的）。
关键见解
根据
Howard Hinnant 在此处的评论
，标准库容器并非设计为具有 const 元素。
容器的 const-ness 来自于将容器本身设置为 const，而不是元素。
std::vector
最大的缺点之一是它不能是
constexpr
。如果您需要
constexpr
数组，请使用
std::array
。
相关内容
我们将在课程
17.1 -- std::array 简介
中介绍
std::array
。
为什么它叫“vector”？
当人们在对话中使用“vector”这个词时，他们通常指的是几何向量，这是一个具有大小和方向的对象。那么
std::vector
又是如何得名的呢，因为它不是一个几何向量？
在《从数学到泛型编程》一书中，Alexander Stepanov 写道：“STL 中的 vector 名称取自早期的编程语言 Scheme 和 Common Lisp。不幸的是，这与数学中这个术语的更古老含义不一致……这个数据结构应该被称为 array。遗憾的是，如果你犯了错误并违反了这些原则，结果可能会持续很长时间。”
所以，基本上，
std::vector
是一个错误的命名，但现在改变它为时已晚。
小测验时间
问题 #1
使用 CTAD 定义一个
std::vector
，并用前 5 个正平方数（1, 4, 9, 16 和 25）初始化它。
显示答案
std::vector squares{ 1, 4, 9, 16, 25 };
问题 #2
这两个定义之间有什么行为差异？
std::vector<int> v1 { 5 };
std::vector<int> v2 ( 5 );
显示答案
v1
调用列表构造函数来定义一个包含值
5
的 1 元素向量。
v2
调用非列表构造函数来定义一个包含 5 个元素且已值初始化的向量。
问题 #3
定义一个
std::vector
（使用显式模板类型参数）来保存一年中每天的最高温度（精确到小数点后一位，假设一年有 365 天）。
显示答案
std::vector<double> temperature (365); // create a vector to hold 365 double values
问题 #4
使用
std::vector
，编写一个程序，要求用户输入 3 个整数值。打印这些值的和与积。
输出应与以下内容匹配
Enter 3 integers: 3 4 5
The sum is: 12
The product is: 60
显示答案
#include <iostream>
#include <vector>

int main()
{
	std::vector<int> arr(3); // create a vector of length 3
	
	std::cout << "Enter 3 integers: ";
	std::cin >> arr[0] >> arr[1] >> arr[2];

	std::cout << "The sum is: " << arr[0] + arr[1] + arr[2] << '\n';
	std::cout << "The product is: " << arr[0] * arr[1] * arr[2] << '\n';

	return 0;
}
下一课
16.3
std::vector 和无符号长度及下标问题
返回目录
上一课
16.1
容器和数组简介