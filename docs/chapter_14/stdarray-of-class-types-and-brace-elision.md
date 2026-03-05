# 17.4 — std::array 的类类型，以及花括号省略

17.4 — std::array 的类类型，以及花括号省略
Alex
2023年9月11日，下午3:48 PDT
2024年9月29日
一个
std::array
不仅限于基本类型的元素。相反，
std::array
的元素可以是任何对象类型，包括复合类型。这意味着您可以创建指针的
std::array
，或者结构体（或类）的
std::array
然而，初始化结构体或类的
std::array
往往会让新程序员感到困惑，所以我们将在本课中明确涵盖这个主题。
作者注
我们将在本课中使用结构体来说明我们的观点。这些材料同样适用于类。
定义和赋值给结构体数组的
std::array
我们从一个简单的结构体开始
struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};
定义一个
House
的
std::array
并赋值元素，就像你预期的那样
#include <array>
#include <iostream>

struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};

int main()
{
    std::array<House, 3> houses{};

    houses[0] = { 13, 1, 7 };
    houses[1] = { 14, 2, 5 };
    houses[2] = { 15, 2, 4 };

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
                  << " has " << (house.stories * house.roomsPerStory)
                  << " rooms.\n";
    }

    return 0;
}
上面输出如下：
House number 13 has 7 rooms.
House number 14 has 10 rooms.
House number 15 has 8 rooms.
初始化结构体数组的
std::array
初始化结构体数组也像你预期的那样，只要你明确元素类型
#include <array>
#include <iostream>

struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};

int main()
{
    constexpr std::array houses { // use CTAD to deduce template arguments <House, 3>
            House{ 13, 1, 7 },
            House{ 14, 2, 5 },
            House{ 15, 2, 4 }
        };

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
            << " has " << (house.stories * house.roomsPerStory)
            << " rooms.\n";
    }

    return 0;
}
在上面的例子中，我们使用 CTAD 来推导
std::array
的类型为
std::array<House, 3>
。然后我们提供 3 个
House
对象作为初始化器，这工作得很好。
初始化时未显式指定每个初始化器的元素类型
在上面的例子中，你会注意到每个初始化器都要求我们列出元素类型
constexpr std::array houses {
            House{ 13, 1, 7 }, // we mention House here
            House{ 14, 2, 5 }, // and here
            House{ 15, 2, 4 }  // and here
        };
但是我们在赋值的情况下不需要这样做
// The compiler knows that each element of houses is a House
    // so it will implicitly convert the right hand side of each assignment to a House
    houses[0] = { 13, 1, 7 };
    houses[1] = { 14, 2, 5 };
    houses[2] = { 15, 2, 4 };
所以你可能会尝试这样的操作
// doesn't work
    constexpr std::array<House, 3> houses { // we're telling the compiler that each element is a House
            { 13, 1, 7 }, // but not mentioning it here
            { 14, 2, 5 },
            { 15, 2, 4 } 
        };
也许令人惊讶的是，这行不通。让我们来探究一下原因。
一个
std::array
被定义为一个包含一个 C 风格数组成员（其名称由实现定义）的结构体，如下所示：
template<typename T, std::size_t N>
struct array
{
    T implementation_defined_name[N]; // a C-style array with N elements of type T
}
作者注
我们还没有介绍 C 风格数组，但为了本课的目的，你只需要知道
T implementation_defined_name[N];
是一个包含 N 个 T 类型元素的固定大小数组（就像
std::array<T, N> implementation_defined_name;
）。
我们将在即将到来的课程
17.7 -- C 风格数组简介
中介绍 C 风格数组。
因此，当我们尝试按上述方式初始化
houses
时，编译器会这样解释初始化：
// Doesn't work
constexpr std::array<House, 3> houses { // initializer for houses
    { 13, 1, 7 }, // initializer for C-style array member with implementation_defined_name
    { 14, 2, 5 }, // ?
    { 15, 2, 4 }  // ?
};
编译器会将
{ 13, 1, 7 }
解释为
houses
的第一个成员的初始化器，它是一个具有实现定义名称的 C 风格数组。这将用
{ 13, 1, 7 }
初始化 C 风格数组的元素 0，其余成员将被零初始化。然后编译器会发现我们又提供了两个初始化值（
{ 14, 2, 7 }
和
{ 15, 2, 5 }
），并产生一个编译错误，告诉我们提供了过多的初始化值。
正确的初始化方式是添加额外的一对大括号，如下所示：
// This works as expected
constexpr std::array<House, 3> houses { // initializer for houses
    { // extra set of braces to initialize the C-style array member with implementation_defined_name
        { 13, 4, 30 }, // initializer for array element 0
        { 14, 3, 10 }, // initializer for array element 1
        { 15, 3, 40 }, // initializer for array element 2
     }
};
注意所需的额外大括号（用于开始初始化
std::array
结构体内部的 C 风格数组成员）。在这些大括号内，我们可以单独初始化每个元素，每个元素都在其自己的大括号内。
这就是为什么当元素类型需要值列表而我们未显式提供元素类型作为初始化器的一部分时，您会看到
std::array
初始化器带有额外的一对大括号。
关键见解
当使用结构体、类或数组初始化
std::array
并且不为每个初始化器提供元素类型时，您需要额外的一对花括号，以便编译器正确解释要初始化什么。
这是聚合初始化的一种特性，其他标准库容器类型（使用列表构造函数）在这种情况下不需要双花括号。
这是一个完整的例子
#include <array>
#include <iostream>

struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};

int main()
{
    constexpr std::array<House, 3> houses {{ // note double braces
        { 13, 1, 7 },
        { 14, 2, 5 },
        { 15, 2, 4 }
    }};

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
                  << " has " << (house.stories * house.roomsPerStory)
                  << " rooms.\n";
    }

    return 0;
}
聚合的花括号省略
根据上面的解释，你可能想知道为什么上面的情况需要双大括号，而我们看到的所有其他情况都只需要单大括号
#include <array>
#include <iostream>

int main()
{
    constexpr std::array<int, 5> arr { 1, 2, 3, 4, 5 }; // single braces

    for (const auto n : arr)
        std::cout << n << '\n';

    return 0;
}
结果是，你可以为这类数组提供双大括号
#include <array>
#include <iostream>

int main()
{
    constexpr std::array<int, 5> arr {{ 1, 2, 3, 4, 5 }}; // double braces

    for (const auto n : arr)
        std::cout << n << '\n';

    return 0;
}
然而，C++ 中的聚合支持一种称为**花括号省略**的概念，它规定了何时可以省略多个花括号。通常，当用标量（单个）值初始化
std::array
，或者当用类类型或数组初始化时，并且每个元素都显式命名其类型时，可以省略花括号。
始终使用双花括号初始化
std::array
没有坏处，因为这样可以避免考虑在特定情况下是否适用花括号省略。或者，您可以尝试单花括号初始化，如果编译器无法识别，它通常会报错。在这种情况下，您可以快速添加额外的花括号。
另一个例子
这里有一个我们用
Student
结构体初始化
std::array
的例子。
#include <array>
#include <iostream>
#include <string_view>

// Each student has an id and a name
struct Student
{
	int id{};
	std::string_view name{};
};

// Our array of 3 students (single braced since we mention Student with each initializer)
constexpr std::array students{ Student{0, "Alex"}, Student{ 1, "Joe" }, Student{ 2, "Bob" } };

const Student* findStudentById(int id)
{
	// Look through all the students
	for (auto& s : students)
	{
		// Return student with matching id
		if (s.id == id) return &s;
	}

	// No matching id found
	return nullptr;
}

int main()
{
	constexpr std::string_view nobody { "nobody" };

	const Student* s1 { findStudentById(1) };
	std::cout << "You found: " << (s1 ? s1->name : nobody) << '\n';

	const Student* s2 { findStudentById(3) };
	std::cout << "You found: " << (s2 ? s2->name : nobody) << '\n';

	return 0;
}
这会打印
You found: Joe
You found: nobody
请注意，由于
std::array students
是 constexpr，我们的
findStudentById()
函数必须返回一个 const 指针，这意味着我们
main()
中的
Student
指针也必须是 const。
小测验时间
问题 #1
定义一个名为
Item
的结构体，它包含两个成员：
std::string_view name
和
int gold
。定义一个
std::array
并用 4 个
Item
对象初始化它。使用 CTAD 推导元素类型和数组大小。
显示提示
提示：您需要为每个初始化器显式指定元素类型。
程序应输出以下内容
A sword costs 5 gold.
A dagger costs 3 gold.
A club costs 2 gold.
A spear costs 7 gold.
显示答案
#include <array>
#include <iostream>
#include <string_view>

struct Item
{
    std::string_view name {};
    int gold {};
};

template <std::size_t N>
void printStore(const std::array<Item, N>& arr)
{
    for (const auto& item: arr)
    {
        std::cout << "A " << item.name << " costs " << item.gold << " gold.\n";
    }
}

int main()
{
    constexpr std::array store { // CTAD, single braces due to brace elision
        Item { "sword",    5 },
        Item { "dagger",   3 },
        Item { "club",     2 },
        Item { "spear",    7 } };
    printStore(store);
    
    return 0;
}
由于我们明确指定了每个初始化器的元素类型，因此这里可以使用 CTAD 和单花括号（由于花括号省略）。
问题 #2
更新您的测验 1 解决方案，使其不再显式指定每个初始化器的元素类型。
显示答案
#include <array>
#include <iostream>
#include <string_view>

struct Item
{
    std::string_view name {};
    int gold {};
};

template <std::size_t N>
void printStore(const std::array<Item, N>& arr)
{
    for (const auto& item: arr)
    {
        std::cout << "A " << item.name << " costs " << item.gold << " gold.\n";
    }
}

int main()
{
    constexpr std::array<Item, 4> store {{ // No CTAD, must use double braces
        { "sword",    5 },
        { "dagger",   3 },
        { "club",     2 },
        { "spear",    7 }
    }};
    printStore(store);
    
    return 0;
}
由于我们没有显式指定每个初始化器的元素类型，我们不能使用 CTAD 也不能使用花括号省略。这意味着我们必须使用双花括号。
下一课
17.5
通过 std::reference_wrapper 实现引用数组
返回目录
上一课
17.3
传递和返回 std::array