# 17.3 — 传递和返回 std::array

17.3 — 传递和返回 std::array
Alex
2023 年 9 月 11 日下午 3:46 PDT
2024 年 12 月 2 日
类型为
std::array
的对象可以像其他任何对象一样传递给函数。这意味着如果我们按值传递
std::array
，将会进行昂贵的复制。因此，我们通常通过（const）引用传递
std::array
以避免此类复制。
对于
std::array
，元素类型和数组长度都是对象类型信息的一部分。因此，当我们使用
std::array
作为函数参数时，我们必须显式指定元素类型和数组长度。
#include <array>
#include <iostream>

void passByRef(const std::array<int, 5>& arr) // we must explicitly specify <int, 5> here
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // CTAD deduces type std::array<int, 5>
    passByRef(arr);

    return 0;
}
CTAD（当前）不适用于函数参数，因此我们不能只在这里指定
std::array
并让编译器推断模板参数。
使用函数模板传递不同元素类型或长度的
std::array
为了编写一个可以接受任何元素类型或任何长度的
std::array
的函数，我们可以创建一个函数模板，该模板将
std::array
的元素类型和长度都参数化，然后 C++ 将使用该函数模板实例化具有实际类型和长度的真实函数。
相关内容
我们在第
11.6 课 -- 函数模板
中介绍了函数模板。
由于
std::array
定义如下
template<typename T, std::size_t N> // N is a non-type template parameter
struct array;
我们可以创建一个使用相同模板参数声明的函数模板
#include <array>
#include <iostream>

template <typename T, std::size_t N> // note that this template parameter declaration matches the one for std::array
void passByRef(const std::array<T, N>& arr)
{
    static_assert(N != 0); // fail if this is a zero-length std::array

    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // use CTAD to infer std::array<int, 5>
    passByRef(arr);  // ok: compiler will instantiate passByRef(const std::array<int, 5>& arr)

    std::array arr2{ 1, 2, 3, 4, 5, 6 }; // use CTAD to infer std::array<int, 6>
    passByRef(arr2); // ok: compiler will instantiate passByRef(const std::array<int, 6>& arr)

    std::array arr3{ 1.2, 3.4, 5.6, 7.8, 9.9 }; // use CTAD to infer std::array<double, 5>
    passByRef(arr3); // ok: compiler will instantiate passByRef(const std::array<double, 5>& arr)

    return 0;
}
在上面的示例中，我们创建了一个名为
passByRef()
的函数模板，它有一个类型为
std::array<T, N>
的参数。
T
和
N
在上一行的模板参数声明中定义：
template <typename T, std::size_t N>
。
T
是一个标准类型模板参数，允许调用者指定元素类型。
N
是一个类型为
std::size_t
的非类型模板参数，允许调用者指定数组长度。
警告
请注意，
std::array
的非类型模板参数的类型应该是
std::size_t
，而不是
int
！这是因为
std::array
被定义为
template<class T, std::size_t N> struct array;
。如果您使用
int
作为非类型模板参数的类型，编译器将无法将类型为
std::array<T, std::size_t>
的参数与类型为
std::array<T, int>
的参数匹配（并且模板不会进行转换）。
因此，当我们从
main()
调用
passByRef(arr)
（其中
arr
定义为
std::array<int, 5>
）时，编译器将实例化并调用
void passByRef(const std::array<int, 5>& arr)
。
arr2
和
arr3
也发生类似的过程。
因此，我们创建了一个函数模板，可以实例化函数来处理任何元素类型和长度的
std::array
参数！
如果需要，也可以只模板化两个模板参数中的一个。在以下示例中，我们只参数化
std::array
的长度，但元素类型显式定义为
int
#include <array>
#include <iostream>

template <std::size_t N> // note: only the length has been templated here
void passByRef(const std::array<int, N>& arr) // we've defined the element type as int
{
    static_assert(N != 0); // fail if this is a zero-length std::array

    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // use CTAD to infer std::array<int, 5>
    passByRef(arr);  // ok: compiler will instantiate passByRef(const std::array<int, 5>& arr)

    std::array arr2{ 1, 2, 3, 4, 5, 6 }; // use CTAD to infer std::array<int, 6>
    passByRef(arr2); // ok: compiler will instantiate passByRef(const std::array<int, 6>& arr)

    std::array arr3{ 1.2, 3.4, 5.6, 7.8, 9.9 }; // use CTAD to infer std::array<double, 5>
    passByRef(arr3); // error: compiler can't find matching function

    return 0;
}
自动非类型模板参数
C++20
为了在您自己的函数模板的模板参数声明中使用非类型模板参数的类型，不得不记住（或查找）它，这很麻烦。
在 C++20 中，我们可以在模板参数声明中使用
auto
，让非类型模板参数从参数中推断其类型
#include <array>
#include <iostream>

template <typename T, auto N> // now using auto to deduce type of N
void passByRef(const std::array<T, N>& arr)
{
    static_assert(N != 0); // fail if this is a zero-length std::array

    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // use CTAD to infer std::array<int, 5>
    passByRef(arr);  // ok: compiler will instantiate passByRef(const std::array<int, 5>& arr)

    std::array arr2{ 1, 2, 3, 4, 5, 6 }; // use CTAD to infer std::array<int, 6>
    passByRef(arr2); // ok: compiler will instantiate passByRef(const std::array<int, 6>& arr)

    std::array arr3{ 1.2, 3.4, 5.6, 7.8, 9.9 }; // use CTAD to infer std::array<double, 5>
    passByRef(arr3); // ok: compiler will instantiate passByRef(const std::array<double, 5>& arr)

    return 0;
}
如果您的编译器支持 C++20，则可以使用此功能。
静态断言数组长度
考虑以下模板函数，它与上面介绍的函数类似
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    std::cout << arr[3] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 };
    printElement3(arr);

    return 0;
}
虽然
printElement3()
在这种情况下工作正常，但此程序中有一个潜在的错误正等待粗心的程序员。看到了吗？
上述程序打印索引为 3 的数组元素的值。只要数组有一个索引为 3 的有效元素，这就可以了。但是，编译器会很高兴地让您传入索引 3 超出范围的数组。例如
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    std::cout << arr[3] << '\n'; // invalid index
}

int main()
{
    std::array arr{ 9, 7 }; // a 2-element array (valid indexes 0 and 1)
    printElement3(arr);

    return 0;
}
这会导致未定义的行为。理想情况下，我们希望编译器在尝试这样做时警告我们！
模板参数相对于函数参数的一个优点是模板参数是编译时常量。这意味着我们可以利用需要常量表达式的功能。
因此，一个解决方案是使用
std::get()
（它执行编译时边界检查）而不是
operator[]
（它不执行边界检查）
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    std::cout << std::get<3>(arr) << '\n'; // checks that index 3 is valid at compile-time
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 };
    printElement3(arr); // okay

    std::array arr2{ 9, 7 };
    printElement3(arr2); // compile error

    return 0;
}
当编译器到达对
printElement3(arr2)
的调用时，它将实例化函数
printElement3(const std::array<int, 2>&)
。此函数体中有一行
std::get<3>(arr)
。由于数组参数的长度为 2，这是无效访问，编译器将发出错误。
另一种解决方案是使用
static_assert
来验证数组长度的先决条件
相关内容
我们在第
9.6 课 -- Assert 和 static_assert
中介绍了先决条件。
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    // precondition: array length must be greater than 3 so element 3 exists
    static_assert (N > 3);

    // we can assume the array length is greater than 3 beyond this point

    std::cout << arr[3] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 };
    printElement3(arr); // okay

    std::array arr2{ 9, 7 };
    printElement3(arr2); // compile error

    return 0;
}
当编译器到达对
printElement3(arr2)
的调用时，它将实例化函数
printElement3(const std::array<int, 2>&)
。此函数体中有一行
static_assert (N > 3)
。由于
N
模板非类型参数的值为
2
，而
2 > 3
为假，编译器将发出错误。
关键见解
在上面的示例中，您可能想知道为什么我们使用
static_assert (N > 3);
而不是
static_assert (std::size(arr) > 3)
。由于上一课中提到的语言缺陷（
17.2 -- std::array 长度和索引
），后者在 C++23 之前无法编译。
返回
std::array
除了语法之外，将
std::array
传递给函数在概念上很简单——通过（const）引用传递。但是，如果我们需要一个函数返回
std::array
怎么办？事情有点复杂。与
std::vector
不同，
std::array
不支持移动，因此按值返回
std::array
将会复制数组。如果数组中的元素支持移动，则会移动它们，否则会复制它们。
这里有两种传统的选择，您应该选择哪一种取决于具体情况。
按值返回
std::array
当以下所有条件都为真时，按值返回
std::array
是可以的
数组不大。
元素类型复制（或移动）开销小。
代码没有在对性能敏感的上下文中使用。
在这种情况下，会复制
std::array
，但如果上述所有条件都为真，性能损失将很小，并且坚持使用最传统的方式将数据返回给调用者可能是最佳选择。
#include <array>
#include <iostream>
#include <limits>

// return by value
template <typename T, std::size_t N>
std::array<T, N> inputArray() // return by value
{
	std::array<T, N> arr{};
	std::size_t index { 0 };
	while (index < N)
	{
		std::cout << "Enter value #" << index << ": ";
		std::cin >> arr[index];

		if (!std::cin) // handle bad input
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			continue;
		}
		++index;
	}

	return arr;
}

int main()
{
	std::array<int, 5> arr { inputArray<int, 5>() };

	std::cout << "The value of element 2 is " << arr[2] << '\n';

	return 0;
}
这种方法有一些优点
它使用最传统的方式将数据返回给调用者。
函数返回一个值是显而易见的。
我们可以定义一个数组并使用该函数在单个语句中初始化它。
也有一些缺点
函数返回数组及其所有元素的副本，这并不便宜。
当我们调用函数时，我们必须显式提供模板参数，因为没有参数可以从中推断它们。
通过输出参数返回
std::array
在按值返回太昂贵的情况下，我们可以使用输出参数。在这种情况下，调用者负责通过非 const 引用（或通过地址）传入
std::array
，然后函数可以修改此数组。
#include <array>
#include <limits>
#include <iostream>

template <typename T, std::size_t N>
void inputArray(std::array<T, N>& arr) // pass by non-const reference
{
	std::size_t index { 0 };
	while (index < N)
	{
		std::cout << "Enter value #" << index << ": ";
		std::cin >> arr[index];

		if (!std::cin) // handle bad input
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			continue;
		}
		++index;
	}

}

int main()
{
	std::array<int, 5> arr {};
	inputArray(arr);

	std::cout << "The value of element 2 is " << arr[2] << '\n';

	return 0;
}
此方法的主要优点是不会复制数组，因此效率很高。
也有一些缺点
这种返回数据的方法不符合常规，并且不容易看出函数正在修改参数。
我们只能使用此方法为数组赋值，而不能初始化它。
这样的函数不能用于生成临时对象。
改为返回
std::vector
std::vector
支持移动，可以按值返回而不会进行昂贵的复制。如果您按值返回
std::array
，您的
std::array
可能不是 constexpr，您应该考虑使用（并返回）
std::vector
。
小测验时间
问题 #1
完成以下程序
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr1 { 1, 4, 9, 16 };
    printArray(arr1);

    constexpr std::array arr2 { 'h', 'e', 'l', 'l', 'o' };
    printArray(arr2);
    
    return 0;
}
运行时，它应该打印
The array (1, 4, 9, 16) has length 4
The array (h, e, l, l, o) has length 5
显示答案
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printArray(const std::array<T, N>& arr)
{
    std::cout << "The array (";

    auto separator {""};
    for (const auto& e: arr)
    {
        std::cout << separator << e;
        separator = ", ";
    }
    
    std::cout << ") has length " << N << '\n';
}

int main()
{
    constexpr std::array arr1 { 1, 4, 9, 16 };
    printArray(arr1);

    constexpr std::array arr2 { 'h', 'e', 'l', 'l', 'o' };
    printArray(arr2);
    
    return 0;
}
下一课
17.4
类类型和花括号省略的 std::array
返回目录
上一课
17.2
std::array 长度和索引