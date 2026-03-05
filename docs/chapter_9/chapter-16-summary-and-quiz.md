# 16.x — 第16章总结和测验

16.x — 第16章总结和测验
Alex
2023年9月11日，下午2:56 PDT
2025年2月4日
鼓励的话
这一章不容易。我们涵盖了大量材料，并揭示了C++的一些缺点。恭喜你坚持下来了！
数组是解锁C++程序中巨大力量的关键之一。
章节回顾
容器
是一种数据类型，它为一组无名对象（称为
元素
）提供存储。当我们处理一组相关值时，通常会使用容器。
容器中元素的数量通常称为其
长度
（有时也称为
计数
）。在C++中，术语
大小
也常用于表示容器中元素的数量。在大多数编程语言（包括C++）中，容器是
同质的
，这意味着容器的元素必须具有相同的类型。
容器库
是C++标准库的一部分，其中包含各种实现常见容器类型的类类型。实现容器的类类型有时称为
容器类
。
数组
是一种容器数据类型，它
连续
存储一系列值（这意味着每个元素都放置在相邻的内存位置，没有间隙）。数组允许快速、直接访问任何元素。
C++包含三种主要的数组类型：（C风格）数组，
std::vector
容器类和
std::array
容器类。
std::vector
是C++标准容器库中实现数组的容器类之一。
std::vector
在
头文件中定义为类模板，带有一个模板类型参数，用于定义元素的类型。因此，
std::vector<int>
声明了一个元素类型为
int
的
std::vector
。
容器通常有一个特殊的构造函数，称为
列表构造函数
，它允许我们使用初始化列表构造容器实例。使用带有值初始化列表的列表初始化来构造具有这些元素值的容器。
在C++中，访问数组元素最常见的方式是使用数组名称和下标运算符（
operator[]
）。为了选择特定元素，我们在下标运算符的方括号内提供一个整数值，用于标识我们要选择的元素。这个整数值称为
下标
（或非正式地称为
索引
）。第一个元素使用索引0访问，第二个元素使用索引1访问，依此类推……因为索引从0而不是1开始，所以我们说C++中的数组是
基于0的
。
operator[]
不做任何
边界检查
，这意味着它不检查索引是否在0到N-1（包含）的范围内。向
operator[]
传递无效索引将导致未定义行为。
数组是少数允许
随机访问
的容器类型之一，这意味着容器中的每个元素都可以直接以相同的速度访问，无论容器中元素的数量如何。
构造类类型对象时，匹配的列表构造函数将优先于其他匹配的构造函数被选中。当使用非元素值初始化器构造容器（或任何具有列表构造函数的类型）时，请使用直接初始化。
std::vector v1 { 5 }; // defines a 1 element vector containing value `5`.
std::vector v2 ( 5 ); // defines a 5 element vector where elements are value-initialized.
std::vector
可以设为const，但不能设为constexpr。
每个标准库容器类都定义了一个名为
size_type
的嵌套typedef成员（有时写作
T::size_type
），它是用于容器长度（以及如果支持的话，索引）的类型的别名。
size_type
几乎总是
std::size_t
的别名，但（在极少数情况下）可以被覆盖以使用不同的类型。我们可以合理地假设
size_type
是
std::size_t
的别名。
访问容器类的
size_type
成员时，我们必须使用容器类的完全模板化名称进行范围限定。例如，
std::vector<int>::size_type
。
我们可以使用
size()
成员函数请求容器类对象的长度，它以无符号
size_type
返回长度。在C++17中，我们还可以使用非成员函数
std::size()
。
在C++20中，
std::ssize()
非成员函数返回一个大的
有符号
整数类型（通常是
std::ptrdiff_t
，这是通常用作
std::size_t
的有符号对应类型的类型）的长度。
使用
at()
成员函数访问数组元素会进行运行时边界检查（如果超出范围则抛出
std::out_of_range
类型的异常）。如果未捕获到异常，应用程序将终止。
operator[]
和
at()
成员函数都支持使用非const索引进行索引。然而，两者都期望索引类型为
size_type
，这是一种无符号整数类型。当索引是非constexpr时，这会导致符号转换问题。
std::vector
类型的对象可以像任何其他对象一样传递给函数。这意味着如果我们按值传递
std::vector
，将进行昂贵的复制。因此，我们通常通过（const）引用传递
std::vector
以避免此类复制。
我们可以使用函数模板将具有任何元素类型的
std::vector
传递给函数。您可以使用
assert()
来确保传入的向量具有正确的长度。
术语
复制语义
指的是确定如何复制对象的规则。当我们说调用复制语义时，这意味着我们做了某事将复制一个对象。
当数据的所有权从一个对象转移到另一个对象时，我们说数据已被
移动
。
移动语义
指的是确定如何将一个对象的数据移动到另一个对象的规则。当调用移动语义时，任何可以移动的数据成员都被移动，任何不能移动的数据成员都被复制。移动数据而不是复制数据的能力可以使移动语义比复制语义更高效，特别是当我们可以用廉价的移动替换昂贵的复制时。
通常，当一个对象使用相同类型的对象进行初始化或赋值时，将使用复制语义（假设复制未被消除）。当对象的类型支持移动语义，并且初始化器或被赋值的对象是右值时，将自动使用移动语义。
我们可以按值返回支持移动的类型（如
std::vector
和
std::string
）。这些类型将廉价地移动其值，而不是进行昂贵的复制。
以某种顺序访问容器的每个元素称为
遍历
，或
遍历
容器。遍历有时也称为
迭代
容器。
循环通常用于遍历数组，其中循环变量用作索引。注意差一错误，即循环体执行的次数过多或过少。
范围for循环
（有时也称为
for-each循环
）允许遍历容器而无需进行显式索引。遍历容器时，优先使用范围for循环而不是普通for循环。
在范围for循环中使用类型推导（
auto
）让编译器推断数组元素的类型。元素声明应在通常按（const）引用传递该元素类型时使用（const）引用。除非您需要处理副本，否则请考虑始终使用
const auto&
。这将确保即使以后更改了元素类型，也不会生成副本。
无作用域枚举可以作为索引使用，并有助于提供有关索引含义的任何信息。
添加一个额外的“count”枚举器在我们需要一个代表数组长度的枚举器时非常有用。您可以使用assert或static_assert来确保数组的长度等于count枚举器，以确保数组以预期的初始化器数量初始化。
数组长度必须在实例化时定义且之后不能更改的数组称为
固定大小数组
或
固定长度数组
。
动态数组
（也称为
可调整大小数组
）是实例化后大小可以更改的数组。这种可调整大小的能力使
std::vector
与众不同。
实例化后，可以通过调用
resize()
成员函数并传入新的所需长度来调整
std::vector
的大小。
在
std::vector
的上下文中，
容量
是
std::vector
已分配存储空间的元素数量，而
长度
是当前正在使用的元素数量。我们可以通过
capacity()
成员函数请求
std::vector
的容量。
当
std::vector
改变其管理的存储量时，这个过程称为
重新分配
。因为重新分配通常需要复制数组中的每个元素，所以重新分配是一个昂贵的过程。因此，我们希望尽可能合理地避免重新分配。
下标运算符（
operator[]
）和
at()
成员函数的有效索引基于向量的长度，而不是容量。
std::vector
有一个名为
shrink_to_fit()
的成员函数，它请求向量将其容量缩小以匹配其长度。此请求是非绑定的。
物品被添加到堆栈和从堆栈中移除的顺序可以描述为
后进先出（LIFO）
。最后添加到堆栈中的盘子将是第一个被移除的盘子。在编程中，
堆栈
是一种容器数据类型，其中元素的插入和移除以LIFO方式发生。这通常通过两个名为
push
和
pop
的操作实现。
std::vector
成员函数
push_back()
和
emplace_back()
将增加
std::vector
的长度，如果容量不足以插入值，将导致重新分配。当push触发重新分配时，
std::vector
通常会分配一些额外的容量，以允许在下次添加元素时无需触发另一次重新分配即可添加更多元素。
resize()
成员函数改变向量的长度，并（如果需要）改变容量。
reserve()
成员函数只改变容量（如果需要）
增加
std::vector
中元素的数量
通过索引访问向量时使用
resize()
。这会改变向量的长度，使您的索引有效。
使用堆栈操作访问向量时使用
reserve()
。这会增加容量而不改变向量的长度。
push_back()
和
emplace_back()
都将一个元素推入堆栈。如果待推入的对象已经存在，
push_back()
和
emplace_back()
是等价的。但是，在创建临时对象以将其推入向量的情况下，
emplace_back()
可能更高效。当创建新的临时对象以添加到容器时，或者当您需要访问显式构造函数时，优先使用
emplace_back()
。否则，优先使用
push_back()
。
std::vector<bool>
有一个特殊实现，通过类似地将8个布尔值压缩成一个字节，可能对布尔值更节省空间。
std::vector<bool>
既不是向量（它不需要在内存中是连续的），也不持有
bool
值（它持有一组位），也不符合C++对容器的定义。尽管
std::vector<bool>
在大多数情况下行为类似于向量，但它与标准库的其余部分不完全兼容。与其他元素类型一起使用的代码可能不适用于
std::vector<bool>
。因此，通常应避免使用
std::vector<bool>
。
小测验时间
问题 #1
为以下内容编写定义。尽可能使用CTAD (
13.14 -- 类模板参数推导 (CTAD) 和推导指南
)。
a) 一个用前6个偶数初始化的
std::vector
。
显示答案
std::vector evens { 2, 4, 6, 8, 10, 12 };
b) 一个用值
1.2
、
3.4
、
5.6
和
7.8
初始化的常量
std::vector
。
显示答案
const std::vector d { 1.2, 3.4, 5.6, 7.8 }; // reminder: std::vector can't be constexpr
c) 一个用名称“Alex”、“Brad”、“Charles”和“Dave”初始化的
std::string_view
常量
std::vector
。
显示答案
using namespace std::literals::string_view_literals; // for sv suffix
const std::vector names { "Alex"sv, "Brad"sv, "Charles"sv, "Dave"sv }; // sv suffix needed for CTAD to infer std::string_view
d) 一个只有一个元素值
12
的
std::vector
。
显示答案
std::vector v { 12 };
当用元素值初始化
std::vector
时，我们应该使用列表初始化。
e) 一个包含12个int元素，初始化为默认值的
std::vector
。
显示提示
提示：考虑在这种情况下CTAD是否可用。
显示答案
std::vector<int> v( 12 );
当用初始长度初始化
std::vector
时，我们必须使用直接初始化。我们还必须显式指定类型模板参数，因为没有可用于推断元素类型的初始化器。
问题 #2
假设您正在编写一个游戏，玩家可以持有3种类型的物品：生命药水、火把和箭。
> 步骤 #1
在命名空间中定义一个无作用域枚举以标识不同类型的物品。定义一个
std::vector
来存储玩家携带的每种物品的数量。玩家应该从1个生命药水、5个火把和10支箭开始。断言以确保数组具有正确数量的初始化器。
提示：定义一个count枚举器并在断言中使用它。
程序应输出以下内容
You have 16 total items
显示答案
#include <cassert>
#include <iostream>
#include <vector>

namespace Items
{
    enum Type
    {
        health_potion,
        torch,
        arrow,
        max_items
    };
}

// Inventory items should have integral quantities, so we don't need a function template here
int countTotalItems(const std::vector<int>& inventory)
{
    int sum { 0 };
    for (auto e: inventory)
        sum += e;
    return sum;
}

int main()
{
    std::vector inventory { 1, 5, 10 };
    assert(std::size(inventory) == Items::max_items); // make sure our inventory has the correct number of initializers

    std::cout << "You have " << countTotalItems(inventory) << " total items\n";
    
    return 0;
}
> 步骤 #2
修改您上一步的程序，使其现在输出
You have 1 health potion
You have 5 torches
You have 10 arrows
You have 16 total items
使用循环打印每个库存物品的数量和物品名称。正确处理名称的复数形式。
显示答案
#include <cassert>
#include <iostream>
#include <string_view>
#include <type_traits> // for std::is_integral and std::is_enum
#include <vector>

namespace Items
{
    enum Type: int
    {
        health_potion,
        torch,
        arrow,
        max_items
    };
}

std::string_view getItemNamePlural(Items::Type type)
{
    switch (type)
    {
        case Items::health_potion:  return "health potions";
        case Items::torch:          return "torches";
        case Items::arrow:          return "arrows";

        default:                    return "???";
    }
}

std::string_view getItemNameSingular(Items::Type type)
{
    switch (type)
    {
        case Items::health_potion:  return "health potion";
        case Items::torch:          return "torch";
        case Items::arrow:          return "arrow";

        default:                    return "???";
    }
}

// Helper function to convert `value` into an object of type std::size_t
// UZ is the suffix for literals of type std::size_t.
template <typename T>
constexpr std::size_t toUZ(T value)
{
    // make sure T is an integral type
    static_assert(std::is_integral<T>() || std::is_enum<T>());
    
    return static_cast<std::size_t>(value);
}


void printInventoryItem(const std::vector<int>& inventory, Items::Type type)
{
    bool plural { inventory[toUZ(type)] != 1 };
    std::cout << "You have " << inventory[toUZ(type)] << ' ';
    std::cout << (plural ? getItemNamePlural(type) : getItemNameSingular(type)) << '\n';
}

// Inventory items should have integral quantities, so we don't need a function template here
int countTotalItems(const std::vector<int>& inventory)
{
    int sum { 0 };
    for (auto e: inventory)
        sum += e;
    return sum;
}

int main()
{
    std::vector inventory { 1, 5, 10 };
    assert(std::size(inventory) == Items::max_items); // make sure our inventory has the correct number of initializers

    // Since we can't iterate over an enumerated type using a ranged-for, we'll need to use a traditional for-loop here
    for (int i=0; i < Items::max_items; ++i)
    {
        auto item { static_cast<Items::Type>(i) };
        printInventoryItem(inventory, item);
    }

    std::cout << "You have " << countTotalItems(inventory) << " total items\n";

    return 0;
}
问题 #3
编写一个函数，它接受一个
std::vector
，并返回一个
std::pair
，其中包含数组中具有最小值和最大值的元素的索引。
std::pair
的文档可以在
这里
找到。在以下两个向量上调用该函数
std::vector v1 { 3, 8, 2, 5, 7, 8, 3 };
    std::vector v2 { 5.5, 2.7, 3.3, 7.6, 1.2, 8.8, 6.6 };
程序应输出以下内容
With array ( 3, 8, 2, 5, 7, 8, 3 ):
The min element has index 2 and value 2
The max element has index 1 and value 8

With array ( 5.5, 2.7, 3.3, 7.6, 1.2, 8.8, 6.6 ):
The min element has index 4 and value 1.2
The max element has index 5 and value 8.8
显示答案
#include <iostream>
#include <vector>

template <typename T>
std::pair<std::size_t, std::size_t> findMinMaxIndices(const std::vector<T>& v)
{
    // Assume element 0 is the minimum and the maximum
    std::size_t minIndex { 0 };
    std::size_t maxIndex { 0 };

    // Look through the remaining elements to see if we can find a smaller or larger element
    for (std::size_t index { 1 }; index < v.size(); ++index)
    {
        if (v[index] < v[minIndex])
            minIndex = index;
        if (v[index] > v[maxIndex])
            maxIndex = index;
    }

    return { minIndex, maxIndex };
}

template <typename T>
void printArray(const std::vector<T>& v)
{
    bool comma { false };
    std::cout << "With array ( ";
    for (const auto& e: v)
    {
        if (comma)
            std::cout << ", ";

        std::cout << e;
        comma = true;
    }
    std::cout << " ):\n";
}

int main()
{
    std::vector v1 { 3, 8, 2, 5, 7, 8, 3 };
    printArray(v1);
    
    auto m1 { findMinMaxIndices(v1) };
    std::cout << "The min element has index " << m1.first << " and value " << v1[m1.first] << '\n';
    std::cout << "The max element has index " << m1.second << " and value " << v1[m1.second] << '\n';

    std::cout << '\n';
    
    std::vector v2 { 5.5, 2.7, 3.3, 7.6, 1.2, 8.8, 6.6 };
    printArray(v2);

    auto m2 { findMinMaxIndices(v2) };
    std::cout << "The min element has index " << m2.first << " and value " << v2[m2.first] << '\n';
    std::cout << "The max element has index " << m2.second << " and value " << v2[m2.second] << '\n';

    return 0;
}
问题 #4
修改前面的程序，使之现在允许用户输入任意数量的整数。当用户输入
-1
时停止接受输入。
打印向量并找出最小和最大元素。
当输入为
3 8 5 2 3 7 -1
时运行，程序应产生以下输出
Enter numbers to add (use -1 to stop): 3 8 5 2 3 7 -1
With array ( 3, 8, 5, 2, 3, 7 ):
The min element has index 3 and value 2
The max element has index 1 and value 8
当用户第一次输入
-1
时，做一些合理的处理。
显示答案
#include <iostream>
#include <limits>
#include <vector>

template <typename T>
std::pair<std::size_t, std::size_t> findMinMaxIndices(const std::vector<T>& v)
{
    // Assume element 0 is the minimum and the maximum
    std::size_t minIndex { 0 };
    std::size_t maxIndex { 0 };

    // Look through the remaining elements to see if we can find a smaller or larger element
    for (std::size_t index { 1 }; index < v.size(); ++index)
    {
        if (v[index] < v[minIndex])
            minIndex = index;
        if (v[index] > v[maxIndex])
            maxIndex = index;
    }

    return { minIndex, maxIndex };
}

template <typename T>
void printArray(const std::vector<T>& v)
{
    bool comma { false };
    std::cout << "With array ( ";
    for (const auto& e: v)
    {
        if (comma)
            std::cout << ", ";

        std::cout << e;
        comma = true;
    }
    std::cout << " ):\n";
}

int main()
{
    std::vector<int> v1 { };
    std::cout << "Enter numbers to add (use -1 to stop): ";

    while (true)
    {
        int input{};
        std::cin >> input;
        if (input == -1)
            break;

        if (!std::cin) // if the previous extraction failed
        {
            std::cin.clear(); // put us back in 'normal' operation mode
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // and remove the bad input
            continue;
        }

        v1.push_back(input);
    }

    // If the array is empty
    if (v1.size() == 0)
    {
        std::cout << "The array has no elements\n";
    }
    else
    {
        printArray(v1);

        auto m1 { findMinMaxIndices(v1) };
        std::cout << "The min element has index " << m1.first << " and value " << v1[m1.first] << '\n';
        std::cout << "The max element has index " << m1.second << " and value " << v1[m1.second] << '\n';
    }

    return 0;
}
问题 #5
让我们实现游戏C++man（这将是我们的经典儿童绞刑游戏
Hangman
的版本）。
如果您以前从未玩过，这里是缩写规则
高层次
计算机将随机选择一个单词，并为单词中的每个字母绘制一个下划线。
如果玩家在进行X次错误猜测（X可配置）之前猜出单词中的所有字母，则玩家获胜。
每回合
玩家将猜测一个字母。
如果玩家已经猜过该字母，则不计数，游戏继续。
如果任何下划线代表该字母，则这些下划线将替换为该字母，游戏继续。
如果没有下划线代表该字母，则玩家用掉一次错误猜测。
状态
玩家应知道还剩下多少次错误猜测。
玩家应知道他们错误猜测了哪些字母（按字母顺序排列）。
因为这是C++man，我们将使用
+
符号表示剩余的错误猜测次数。如果您用完了
+
符号，您就输了。
这是完成游戏的示例输出
Welcome to C++man (a variant of Hangman)
To win: guess the word.  To lose: run out of pluses.

The word: ________   Wrong guesses: ++++++
Enter your next letter: a
No, 'a' is not in the word!

The word: ________   Wrong guesses: +++++a
Enter your next letter: b
Yes, 'b' is in the word!

The word: b_______   Wrong guesses: +++++a
Enter your next letter: c
Yes, 'c' is in the word!

The word: b__cc___   Wrong guesses: +++++a
Enter your next letter: d
No, 'd' is not in the word!

The word: b__cc___   Wrong guesses: ++++ad
Enter your next letter: %
That wasn't a valid input.  Try again.

The word: b__cc___   Wrong guesses: ++++ad
Enter your next letter: d
You already guessed that.  Try again.

The word: b__cc___   Wrong guesses: ++++ad
Enter your next letter: e
No, 'e' is not in the word!

The word: b__cc___   Wrong guesses: +++ade
Enter your next letter: f
No, 'f' is not in the word!

The word: b__cc___   Wrong guesses: ++adef
Enter your next letter: g
No, 'g' is not in the word!

The word: b__cc___   Wrong guesses: +adefg
Enter your next letter: h
No, 'h' is not in the word!

The word: b__cc___   Wrong guesses: adefgh
You lost!  The word was: broccoli
> 步骤 #1
目标
我们将从定义单词列表和编写随机单词选择器开始。您可以使用
8.15 -- 全局随机数 (Random.h)
课程中的Random.h来辅助。
任务
首先定义一个名为
WordList
的命名空间。起始单词列表是：“mystery”、“broccoli”、“account”、“almost”、“spaghetti”、“opinion”、“beautiful”、“distance”、“luggage”。您可以根据需要添加其他单词。
编写一个函数来随机选择一个单词并显示选中的单词。多次运行程序以确保单词是随机的。
这是此步骤的示例输出
Welcome to C++man (a variant of Hangman)
To win: guess the word.  To lose: run out of pluses.

The word is: broccoli
显示答案
#include <iostream>
#include <vector>
#include "Random.h"

namespace WordList
{
    // Define your list of words here
    std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };

    std::string_view getRandomWord()
    {
        return words[Random::get<std::size_t>(0, words.size()-1)];
    }
}

int main()
{
    std::cout << "Welcome to C++man (a variant of Hangman)\n";
    std::cout << "To win: guess the word.  To lose: run out of pluses.\n";

    std::cout << "The word is: " << WordList::getRandomWord();
  
    return 0;
}
> 步骤 #2
当我们开发复杂的程序时，我们希望增量地工作，一次添加一两件事，然后确保它们正常工作。接下来添加什么比较合理呢？
目标
能够绘制游戏的基本状态，将单词显示为下划线。
接受用户输入的一个字母，并进行基本错误验证。
在这一步中，我们还不会跟踪用户输入了哪些字母。
这是此步骤的示例输出
Welcome to C++man (a variant of Hangman)
To win: guess the word.  To lose: run out of pluses.

The word: ________
Enter your next letter: %
That wasn't a valid input.  Try again.
Enter your next letter: a
You entered: a
任务
创建一个名为
Session
的类，用于存储游戏会话所需的所有数据。目前，我们只需要知道随机单词是什么。
创建一个函数来显示游戏的基本状态，其中单词显示为下划线。
创建一个函数来接受用户输入的一个字母。进行基本输入验证以过滤掉非字母或多余的输入。
显示答案
#include <iostream>
#include <string_view>
#include <vector>
#include "Random.h"

namespace WordList
{
    // Define your list of words here
    std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };

    std::string_view getRandomWord()
    {
        return words[Random::get<std::size_t>(0, words.size()-1)];
    }
}

class Session
{
private:
    // Game session data
    std::string_view m_word { WordList::getRandomWord() };

public:
    std::string_view getWord() const { return m_word; }
};

void draw(const Session& s)
{
    std::cout << '\n';

    std::cout << "The word: ";
    for ([[maybe_unused]] auto c: s.getWord()) // step through each letter of word
    {
        std::cout << '_';
    }

    std::cout << '\n';
}

char getGuess()
{
    while (true)
    {
        std::cout << "Enter your next letter: ";

        char c{};
        std::cin >> c;

        // If user did something bad, try again
        if (!std::cin)
        {
            // Fix it
            std::cin.clear();
            std::cout << "That wasn't a valid input.  Try again.\n";
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }
        
        // Clear out any extraneous input
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        // If the user entered an invalid char, try again
        if (c < 'a' || c > 'z')
        {
            std::cout << "That wasn't a valid input.  Try again.\n";
            continue;
        }

        return c;
    }
}

int main()
{
    std::cout << "Welcome to C++man (a variant of Hangman)\n";
    std::cout << "To win: guess the word.  To lose: run out of pluses.\n";

    Session s{};

    draw(s);
    char c { getGuess() };
    std::cout << "You guessed: " << c << '\n';
    
    return 0;
}
> 步骤 #3
现在我们可以显示一些游戏状态并从用户那里获取输入，让我们将该用户输入集成到游戏中。
目标
跟踪用户已经猜测了哪些字母。
显示正确猜测的字母。
实现一个基本的游戏循环。
任务
更新Session类以跟踪到目前为止已猜测的字母。
修改游戏状态函数以同时显示下划线和正确猜测的字母。
更新输入例程以拒绝已经猜测的字母。
编写一个循环，执行6次后退出（以便我们可以测试上述内容）。
在这一步中，我们不会告诉用户他们猜测的字母是否在单词中（但我们会将其显示为游戏状态的一部分）。
这一步的难点在于决定如何存储用户已经猜到的字母信息。有几种可行的方法。提示：字母的数量是固定的，而且您会经常进行此操作。
显示提示
提示：为每个字母使用
bool
比维护一个字母列表并必须搜索该列表以确定字母是否存在要更容易、更快。
显示提示
提示：这里可以使用
std::vector<bool>
，因为我们不会使用标准库的任何其他功能。
显示提示
提示：您可以通过
(letter % 32)-1
将字母转换为数组索引。这适用于小写和大写字母。
这是此步骤的示例输出
Welcome to C++man (a variant of Hangman)
To win: guess the word.  To lose: run out of pluses.

The word: ________
Enter your next letter: a

The word: ____a___
Enter your next letter: a
You already guessed that.  Try again.
Enter your next letter: b

The word: ____a___
Enter your next letter: c

The word: ____a___
Enter your next letter: d

The word: d___a___
Enter your next letter: e

The word: d___a__e
Enter your next letter: f

The word: d___a__e
Enter your next letter: g
显示答案
#include <iostream>
#include <string_view>
#include <vector>
#include "Random.h"

namespace WordList
{
    // Define your list of words here
    std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };

    std::string_view getRandomWord()
    {
        return words[Random::get<std::size_t>(0, words.size()-1)];
    }
}

class Session
{
private:
    // Game session data
    std::string_view m_word { WordList::getRandomWord() };
    std::vector<bool> m_letterGuessed { std::vector<bool>(26) };

    std::size_t toIndex(char c) const { return static_cast<std::size_t>((c % 32)-1); }

public:
    std::string_view getWord() const { return m_word; }

    bool isLetterGuessed(char c) const { return m_letterGuessed[toIndex(c)]; }
    void setLetterGuessed(char c) { m_letterGuessed[toIndex(c)] = true; }
};

void draw(const Session& s)
{
    std::cout << '\n';

    std::cout << "The word: ";
    for (auto c: s.getWord()) // step through each letter of word
    {
        if (s.isLetterGuessed(c))
            std::cout << c;
        else
            std::cout << '_';
    }

    std::cout << '\n';
}

char getGuess(const Session& s)
{
    while (true)
    {
        std::cout << "Enter your next letter: ";

        char c{};
        std::cin >> c;

        // If user did something bad, try again
        if (!std::cin)
        {
            // Fix it
            std::cin.clear();
            std::cout << "That wasn't a valid input.  Try again.\n";
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }
        
        // Clear out any extraneous input
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        // If the user entered an invalid char, try again
        if (c < 'a' || c > 'z')
        {
            std::cout << "That wasn't a valid input.  Try again.\n";
            continue;
        }

        // If the letter was already guessed, try again
        if (s.isLetterGuessed(c))
        {
            std::cout << "You already guessed that.  Try again.\n";
            continue;
        }

        // If we got here, this must be a valid guess
        return c;
    }
}

int main()
{
    std::cout << "Welcome to C++man (a variant of Hangman)\n";
    std::cout << "To win: guess the word.  To lose: run out of pluses.\n";

    Session s {};

    int count { 6 };
    while (--count)
    {
        draw(s);
        char c { getGuess(s) };
        s.setLetterGuessed(c);
    }

    // Draw the final state of the game
    draw(s);
    
    return 0;
}
> 第4步
目标：完成游戏。
任务
添加显示剩余的错误猜测总数
添加显示错误猜测的字母
添加胜利/失败条件和胜利/失败文本。
显示答案
#include <iostream>
#include <string_view>
#include <vector>
#include "Random.h"

namespace Settings
{
    constexpr int wrongGuessesAllowed { 6 };
}

namespace WordList
{
    // Define your list of words here
    std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };

    std::string_view getRandomWord()
    {
        return words[Random::get<std::size_t>(0, words.size()-1)];
    }
}

class Session
{
private:
    // Game session data
    std::string_view m_word { WordList::getRandomWord() };
    int m_wrongGuessesLeft { Settings::wrongGuessesAllowed };
    std::vector<bool> m_letterGuessed { std::vector<bool>(26) };

    std::size_t toIndex(char c) const { return static_cast<std::size_t>((c % 32)-1); }

public:
    std::string_view getWord() const { return m_word; }

    int wrongGuessesLeft() const { return m_wrongGuessesLeft; }
    void removeGuess() { --m_wrongGuessesLeft; }

    bool isLetterGuessed(char c) const { return m_letterGuessed[toIndex(c)]; }
    void setLetterGuessed(char c) { m_letterGuessed[toIndex(c)] = true; }

    bool isLetterInWord(char c) const
    {
        for (auto ch: m_word) // step through each letter of word
        {
            if (ch == c)
                return true;
        }

        return false;
    }

    bool won()
    {
        for (auto c: m_word) // step through each letter of word
        {
            if (!isLetterGuessed(c))
                return false;
        }
        
        return true;
    }
};

void draw(const Session& s)
{
    std::cout << '\n';

    std::cout << "The word: ";
    for (auto c: s.getWord()) // step through each letter of word
    {
        if (s.isLetterGuessed(c))
            std::cout << c;
        else
            std::cout << '_';
    }

    std::cout << "   Wrong guesses: ";
    for (int i=0; i < s.wrongGuessesLeft(); ++i)
        std::cout << '+';


    for (char c='a'; c <= 'z'; ++c)
        if (s.isLetterGuessed(c) && !s.isLetterInWord(c))
            std::cout << c;

    std::cout << '\n';
}

char getGuess(const Session& s)
{
    while (true)
    {
        std::cout << "Enter your next letter: ";

        char c{};
        std::cin >> c;

        // If user did something bad, try again
        if (!std::cin)
        {
            // Fix it
            std::cin.clear();
            std::cout << "That wasn't a valid input.  Try again.\n";
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }
        
        // Clear out any extraneous input
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        // If the user entered an invalid char, try again
        if (c < 'a' || c > 'z')
        {
            std::cout << "That wasn't a valid input.  Try again.\n";
            continue;
        }

        // If the letter was already guessed, try again
        if (s.isLetterGuessed(c))
        {
            std::cout << "You already guessed that.  Try again.\n";
            continue;
        }

        // If we got here, this must be a valid guess
        return c;
    }
}

void handleGuess(Session &s, char c)
{
    s.setLetterGuessed(c);
    
    if (s.isLetterInWord(c))
    {
        std::cout << "Yes, '" << c << "' is in the word!\n";
        return;
    }
    
    std::cout << "No, '" << c << "' is not in the word!\n";
    s.removeGuess();
}

int main()
{
    std::cout << "Welcome to C++man (a variant of Hangman)\n";
    std::cout << "To win: guess the word.  To lose: run out of pluses.\n";

    Session s{};

    while (s.wrongGuessesLeft() && !s.won())
    {
        draw(s);
        char c { getGuess(s) };
        handleGuess(s, c);
    }

    // Draw the final state of the game
    draw(s);

    if (!s.wrongGuessesLeft())
        std::cout << "You lost!  The word was: " << s.getWord() << '\n';
    else
        std::cout << "You won!\n";
    
    return 0;
}
下一课
17.1
std::array简介
返回目录
上一课
16.12
std::vector<bool>