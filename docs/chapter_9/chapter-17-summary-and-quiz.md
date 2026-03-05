# 17.x — 第 17 章总结和测验

17.x — 第 17 章总结和测验
Alex
2015 年 10 月 5 日，太平洋夏令时下午 4:20
2025 年 1 月 6 日
章节回顾
固定大小数组
（或
定长数组
）要求数组的长度在实例化时已知，并且该长度之后不能更改。C 风格数组和
std::array
都是固定大小数组。动态数组可以在运行时调整大小。
std::vector
是一个动态数组。
std::array
的长度必须是一个常量表达式。通常，为长度提供的值将是整数文字、constexpr 变量或无作用域枚举器。
std::array
是一个聚合体。这意味着它没有构造函数，而是使用聚合初始化进行初始化。
尽可能将
std::array
定义为 constexpr。如果您的
std::array
不是 constexpr，请考虑改用
std::vector
。
使用类模板参数推导 (CTAD) 让编译器从其初始化器推导
std::array
的类型和长度。
std::array
被实现为一个模板结构体，其声明如下：
template<typename T, std::size_t N> // N is a non-type template parameter
struct array;
表示数组长度的非类型模板参数 (
N
) 的类型为
std::size_t
。
获取
std::array
的长度
我们可以使用
size()
成员函数（返回长度为无符号
size_type
）询问
std::array
对象的长度。
在 C++17 中，我们可以使用
std::size()
非成员函数（对于
std::array
，它只是调用
size()
成员函数，因此返回长度为无符号
size_type
）。
在 C++20 中，我们可以使用
std::ssize()
非成员函数，它返回长度作为一个大的
有符号
整型（通常是
std::ptrdiff_t
）。
所有这三个函数都将返回长度作为一个 constexpr 值，除非在通过引用传递的
std::array
上调用。此缺陷已在 C++23 中通过
P2280
解决。
索引
std::array
使用下标运算符（
operator[]
）。在这种情况下不进行边界检查，传入无效索引将导致未定义行为。
使用
at()
成员函数，它在运行时进行下标操作并进行边界检查。我们建议避免使用此函数，因为我们通常希望在索引之前进行边界检查，或者我们希望进行编译时边界检查。
使用
std::get()
函数模板，它将索引作为非类型模板参数，并进行编译时边界检查。
您可以使用模板参数声明
template <typename T, std::size_t N>
将具有不同元素类型和长度的
std::array
传递给函数。或者在 C++20 中，使用
template <typename T, auto N>
。
按值返回
std::array
将复制数组和所有元素，但如果数组很小且元素复制成本不高，这可能是可以接受的。在某些情况下，使用输出参数可能是一个更好的选择。
当使用结构体、类或数组初始化
std::array
并且不为每个初始化器提供元素类型时，您需要额外的一对大括号，以便编译器能够正确解释要初始化什么。这是聚合初始化的一个产物，其他标准库容器类型（使用列表构造函数）在这种情况下不需要双大括号。
C++ 中的聚合体支持一种称为
大括号省略
的概念，它规定了一些何时可以省略多个大括号的规则。通常，当用标量（单个）值初始化
std::array
，或当用类类型或数组初始化时，并且每个元素都明确指定了类型时，可以省略大括号。
不能有引用数组，但可以有
std::reference_wrapper
数组，其行为类似于可修改的左值引用。
关于
std::reference_wrapper
，有几点值得注意：
Operator=
将重新设置
std::reference_wrapper
（更改引用的对象）。
std::reference_wrapper<T>
将隐式转换为
T&
。
get()
成员函数可用于获取
T&
。当我们想要更新所引用对象的值时，这很有用。
提供了
std::ref()
和
std::cref()
函数作为创建
std::reference_wrapper
和
const std::reference_wrapper
包装对象的快捷方式。
尽可能使用
static_assert
来确保使用 CTAD 的
constexpr std::array
具有正确数量的初始化器。
C 风格数组继承自 C 语言，并且是 C++ 核心语言的内置部分。因为它们是核心语言的一部分，C 风格数组有自己特殊的声明语法。在 C 风格数组声明中，我们使用方括号 ([]) 告诉编译器声明的对象是一个 C 风格数组。在方括号内，我们可以选择提供数组的长度，它是一个
std::size_t
类型的整数值，告诉编译器数组中有多少个元素。C 风格数组的长度必须是一个常量表达式。
C 风格数组是聚合体，这意味着它们可以使用聚合初始化进行初始化。当使用初始化列表初始化 C 风格数组的所有元素时，最好省略长度，让编译器计算数组的长度。
C 风格数组可以通过
operator[]
进行索引。C 风格数组的索引可以是带符号或无符号整数，也可以是无作用域枚举。这意味着 C 风格数组不受标准库容器类所有符号转换索引问题的影响！
C 风格数组可以是 const 或 constexpr。
获取 C 风格数组的长度
在 C++17 中，我们可以使用
std::size()
非成员函数，它返回无符号的
std::size_t
类型长度。
在 C++20 中，我们可以使用
std::ssize()
非成员函数，它返回长度作为一个大的
有符号
整型（通常是
std::ptrdiff_t
）。
在大多数情况下，当 C 风格数组在表达式中使用时，数组将被隐式转换为指向元素类型的指针，并用第一个元素（索引为 0）的地址初始化。通俗地说，这被称为
数组衰减
（或简称衰减）。
指针算术
是一种特性，允许我们对指针应用某些整数算术运算符（加、减、增、减）以产生新的内存地址。给定一些指针
ptr
，
ptr + 1
返回内存中下一个
对象
的地址（基于指向的类型）。
当从数组开头（元素 0）索引时使用下标，这样数组索引与元素对齐。
当从给定元素进行相对定位时，使用指针算术。
C 风格字符串只是元素类型为
char
或
const char
的 C 风格数组。因此，C 风格字符串会衰减。
数组的
维数
是选择一个元素所需的索引数量。
只包含一个维度的数组称为
单维数组
（有时缩写为
1d 数组
）。数组的数组称为
二维数组
（有时缩写为
2d 数组
），因为它有两个下标。具有多个维度的数组称为
多维数组
。
扁平化
数组是减少数组维度的过程（通常减少到单个维度）。
在 C++23 中，
std::mdspan
是一个视图，为连续的元素序列提供多维数组接口。
小测验时间
问题 #1
这些片段有什么问题，你将如何修复它们？
a)
#include <array>
#include <iostream>

int main()
{
    std::array arr { 0, 1, 2, 3 };

    for (std::size_t count{ 0 }; count <= std::size(arr); ++count)
    {
        std::cout << arr[count] << ' ';
    }

    std::cout << '\n';

    return 0;
}
显示答案
for 循环有一个差一错误，并尝试访问索引为 4 的数组元素，该元素不存在。
解决方案：for 循环中的条件应使用 < 而不是 <=。
b)
#include <iostream>

void printArray(int array[])
{
    for (int element : array)
    {
        std::cout << element << ' ';
    }
}

int main()
{
    int array[] { 9, 7, 5, 3, 1 };

    printArray(array);

    std::cout << '\n';

    return 0;
}
显示答案
当
array
传递给
printArray()
时，它会衰减为指针。基于范围的 for 循环无法与指向数组的指针一起使用，因为数组的大小未知。
解决方案：改用
std::array
，它不会衰减。
c)
#include <array>
#include <iostream>

int main()
{
    std::cout << "Enter the number of test scores: ";
    std::size_t length{};
    std::cin >> length;

    std::array<int, length> scores;

    for (std::size_t i { 0 } ; i < length; ++i)
    {
        std::cout << "Enter score " << i << ": ";
        std::cin >> scores[i];
    }
    return 0;
}
显示答案
length
不是一个常量表达式，不能用于定义
std::array
的长度。
解决方案：改用
std::vector
。
问题 #2
本次测验，我们将实现罗斯科的药水店，这片土地上最好的药水店！这将是一个更大的挑战。
实现一个输出以下内容的程序
Welcome to Roscoe's potion emporium!
Enter your name: Alex
Hello, Alex, you have 85 gold.

Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50
Enter the number of the potion you'd like to buy, or 'q' to quit: a
That is an invalid input.  Try again: 3
You purchased a potion of invisibility.  You have 35 gold left.

Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50
Enter the number of the potion you'd like to buy, or 'q' to quit: 4
That is an invalid input.  Try again: 2
You purchased a potion of speed.  You have 23 gold left.

Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50
Enter the number of the potion you'd like to buy, or 'q' to quit: 2
You purchased a potion of speed.  You have 11 gold left.

Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50
Enter the number of the potion you'd like to buy, or 'q' to quit: 4
You can not afford that.

Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50
Enter the number of the potion you'd like to buy, or 'q' to quit: q

Your inventory contains: 
2x potion of speed
1x potion of invisibility
You escaped with 11 gold remaining.

Thanks for shopping at Roscoe's potion emporium!
玩家起始金币数量随机，介于 80 到 120 之间。
听起来有趣吗？那就动手吧！因为一次性实现所有功能会很困难，所以我们将分步开发。
> 步骤 #1
创建一个名为
Potion
的命名空间，其中包含一个名为
Type
的枚举，用于存储药水类型。创建两个
std::array
：一个
int
数组用于存储药水成本，一个
std::string_view
数组用于存储药水名称。
还要编写一个名为
shop()
的函数，它遍历药水列表并打印它们的编号、名称和成本。
程序应输出以下内容
Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50
显示提示
提示：在
17.6 -- std::array 和枚举
课程中，我们展示了一种使用基于范围的 for 循环遍历枚举的方法。
显示答案
#include <array>
#include <iostream>
#include <string_view>

namespace Potion
{
    enum Type
    {
    healing,
    mana,
    speed,
    invisibility,
    max_potions
    };

    constexpr std::array types { healing, mana, speed, invisibility }; // An array of our enumerators

    // We could put these in a struct, but since we only have two attributes we'll keep them separate for now
    // We will explicitly define the element type so we don't have to use the sv suffix
    constexpr std::array<std::string_view, max_potions> name { "healing", "mana", "speed", "invisibility" };
    constexpr std::array cost { 20, 30, 12, 50 };

    static_assert(std::size(types) == max_potions);  // ensure 'all' contains the correct number of enumerators
    static_assert(std::size(cost) == max_potions);
    static_assert(std::size(name) == max_potions);
}

void shop()
{
    std::cout << "Here is our selection for today:\n";

    for (auto p: Potion::types)
        std::cout << p << ") " << Potion::name[p] << " costs " << Potion::cost[p] << '\n';
}

int main()
{
    shop();

    return 0;
}
> 步骤 #2
创建一个
Player
类来存储玩家的姓名、药水库存和金币。添加 Roscoe 商店的介绍和告别文本。获取玩家姓名并随机化他们的金币。
使用课程
8.15 -- 全局随机数 (Random.h)
中的“Random.h”文件，使随机化变得容易。
程序应输出以下内容
Welcome to Roscoe's potion emporium!
Enter your name: Alex
Hello, Alex, you have 84 gold.

Here is our selection for today:
0) healing costs 20
1) mana costs 30
2) speed costs 12
3) invisibility costs 50

Thanks for shopping at Roscoe's potion emporium!
显示答案
#include <array>
#include <iostream>
#include <string_view>
#include "Random.h"

namespace Potion
{
    enum Type
    {
        healing,
        mana,
        speed,
        invisibility,
        max_potions
    };

    constexpr std::array types { healing, mana, speed, invisibility }; // An array of our enumerators

    // We could put these in a struct, but since we only have two attributes we'll keep them separate for now
    // We will explicitly define the element type so we don't have to use the sv suffix
    constexpr std::array<std::string_view, max_potions> name { "healing", "mana", "speed", "invisibility" };
    constexpr std::array cost { 20, 30, 12, 50 };

    static_assert(std::size(types) == max_potions);  // ensure 'all' contains the correct number of enumerators
    static_assert(std::size(cost) == max_potions);
    static_assert(std::size(name) == max_potions);
}

class Player
{
private:
    static constexpr int s_minStartingGold { 80 };
    static constexpr int s_maxStartingGold { 120 };

    std::string m_name {};
    int m_gold {};
    std::array<int, Potion::max_potions> m_inventory { };

public:
    explicit Player(std::string_view name) :
        m_name { name },
        m_gold { Random::get(s_minStartingGold, s_maxStartingGold) }
    { 
    }

    int gold() const { return m_gold; }
    int inventory(Potion::Type p) const { return m_inventory[p]; }
};

void shop()
{
    std::cout << "Here is our selection for today:\n";

    for (auto p: Potion::types)
        std::cout << p << ") " << Potion::name[p] << " costs " << Potion::cost[p] << '\n';
}

int main()
{
    std::cout << "Welcome to Roscoe's potion emporium!\n";
    std::cout << "Enter your name: ";

    std::string name{};
    std::getline(std::cin >> std::ws, name); // read a full line of text into name

    Player player { name };

    std::cout << "Hello, " << name << ", you have " << player.gold() << " gold.\n\n";

    shop();

    std::cout << "\nThanks for shopping at Roscoe's potion emporium!\n";

    return 0;
}
> 步骤 #3
添加购买药水的功能，处理无效输入（将任何冗余输入视为失败）。玩家离开后打印玩家的库存。此步骤完成后，程序应完整。
确保测试以下情况
用户输入无效药水编号（例如 'd'）
用户输入有效的药水编号但带有冗余输入（例如
2d
,
25
）
我们在课程
9.5 -- std::cin 和处理无效输入
中介绍了无效输入处理。
显示提示
提示：用户可以输入数字或“q”，因此将用户输入提取到
char
类型。
要将 ASCII 数字字符转换为 int（例如
'5'
转换为
5
），您可以使用以下方法：
int charNumToInt(char c)
{
    return c - '0';
}
显示提示
提示：编写一个函数来处理用户输入。它应该返回用户选择的
Potion::Type
。如果用户选择退出，该函数可以返回
Potion::max_potions
。您需要将用户输入
static_cast
为
Potion::Type
。
显示答案
#include <array>
#include <iostream>
#include <limits> // for std::numeric_limits
#include <string_view>
#include "Random.h"

namespace Potion
{
    enum Type
    {
        healing,
        mana,
        speed,
        invisibility,
        max_potions
    };

    constexpr std::array types { healing, mana, speed, invisibility }; // An array of our enumerators

    // We could put these in a struct, but since we only have two attributes we'll keep them separate for now
    // We will explicitly define the element type so we don't have to use the sv suffix
    constexpr std::array<std::string_view, max_potions> name { "healing", "mana", "speed", "invisibility" };
    constexpr std::array cost { 20, 30, 12, 50 };

    static_assert(std::size(types) == max_potions);  // ensure 'all' contains the correct number of enumerators
    static_assert(std::size(cost) == max_potions);
    static_assert(std::size(name) == max_potions);
}

class Player
{
private:
    static constexpr int s_minStartingGold { 80 };
    static constexpr int s_maxStartingGold { 120 };

    std::string m_name {};
    int m_gold {};
    std::array<int, Potion::max_potions> m_inventory { };

public:
    explicit Player(std::string_view name) :
        m_name { name },
        m_gold { Random::get(s_minStartingGold, s_maxStartingGold) }
    { 
    }

    // returns false if can't afford, true if purchased
    bool buy(Potion::Type type)
    {
        if (m_gold < Potion::cost[type])
            return false;

        m_gold -= Potion::cost[type];
        ++m_inventory[type];
        return true;
    }

    int gold() const { return m_gold; }
    int inventory(Potion::Type p) const { return m_inventory[p]; }
};

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

int charNumToInt(char c)
{
    return c - '0';
}

Potion::Type whichPotion()
{
    std::cout << "Enter the number of the potion you'd like to buy, or 'q' to quit: ";
    char input{};
    while (true)
    {
        std::cin >> input;
        if (!std::cin)
        {
            std::cin.clear(); // put us back in 'normal' operation mode
            ignoreLine(); // and remove the bad input
            continue;
        }

        // If there is extraneous input, treat as failure case
        if (!std::cin.eof() && std::cin.peek() != '\n')
        {
            std::cout << "I didn't understand what you said.  Try again: ";
            ignoreLine(); // ignore any extraneous input
            continue;
        }

        if (input == 'q')
            return Potion::max_potions;

        // Convert the char to a number and see if it's a valid potion selection
        int val { charNumToInt(input) };
        if (val >= 0 && val < Potion::max_potions)
            return static_cast<Potion::Type>(val);

        // It wasn't a valid potion selection
        std::cout << "I didn't understand what you said.  Try again: ";
        ignoreLine();
    }
}

void shop(Player &player)
{
    while (true)
    {
        std::cout << "Here is our selection for today:\n";

        for (auto p: Potion::types)
            std::cout << p << ") " << Potion::name[p] << " costs " << Potion::cost[p] << '\n';
        
        Potion::Type which { whichPotion() };
        if (which == Potion::max_potions)
            return;

        bool success { player.buy(which) };
        if (!success)
            std::cout << "You can not afford that.\n\n";
        else
            std::cout << "You purchased a potion of " << Potion::name[which] << ".  You have " << player.gold() << " gold left.\n\n";
    }
}

void printInventory(Player& player)
{
    std::cout << "Your inventory contains: \n";
    
    for (auto p: Potion::types)
    {
        if (player.inventory(p) > 0)
            std::cout << player.inventory(p) << "x potion of " << Potion::name[p] << '\n';
    }

    std::cout << "You escaped with " << player.gold() << " gold remaining.\n";
}

int main()
{
    std::cout << "Welcome to Roscoe's potion emporium!\n";
    std::cout << "Enter your name: ";

    std::string name{};
    std::cin >> name;

    Player player { name };

    std::cout << "Hello, " << name << ", you have " << player.gold() << " gold.\n\n";

    shop(player);

    std::cout << '\n';

    printInventory(player);

    std::cout << "\nThanks for shopping at Roscoe's potion emporium!\n";

    return 0;
}
问题 #3
假设我们要编写一个使用标准扑克牌组的纸牌游戏。为此，我们需要一种方法来表示这些牌和牌组。让我们构建这个功能。
我们将在下一个测验问题中实际实现一个游戏。
> 步骤 #1
一副牌有 52 张独特的牌（4 种花色，每种花色 13 种牌）。为牌的等级（A、2、3、4、5、6、7、8、9、10、J、Q、K）和花色（梅花、方块、红心、黑桃）创建枚举。
显示答案
// Because identifiers can't start with a number, we'll use a "rank_" prefix for these
enum Rank
{
    rank_ace,
    rank_2,
    rank_3,
    rank_4,
    rank_5,
    rank_6,
    rank_7,
    rank_8,
    rank_9,
    rank_10,
    rank_jack,
    rank_queen,
    rank_king,

    max_ranks
};

// We'll also prefix these for consistency
enum Suit
{
    suit_club,
    suit_diamond,
    suit_heart,
    suit_spade,

    max_suits
};
> 步骤 #2
每张牌都将由一个名为
Card
的结构体表示，该结构体包含一个等级和一个花色成员。创建该结构体并将枚举移入其中。
显示答案
struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    Rank rank{};
    Suit suit{};
};
> 步骤 #3
接下来，让我们为我们的 Card 结构体添加一些有用的函数。首先，重载
operator<<
以将牌的等级和花色打印为 2 字母代码（例如，黑桃 J 将打印为 JS）。您可以通过完成以下函数来做到这一点：
struct Card
{
    // Your other stuff here

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        out << // print your card rank and suit here
        return out;
    }
};
其次，添加一个返回 Card 值的函数。将 Ace 视为值 11。最后，添加一个 Rank 和 Suit 的
std::array
（分别命名为
allRanks
和
allSuits
），以便它们可以被迭代。因为这些是结构体的一部分（而不是命名空间），所以将它们设置为静态，以便它们只实例化一次（而不是每个对象实例化一次）。
以下代码应能编译：
int main()
{
    // Print one card
    Card card { Card::rank_5, Card::suit_heart };
    std::cout << card << '\n';

    // Print all cards
    for (auto suit : Card::allSuits)
        for (auto rank : Card::allRanks)
            std::cout << Card { rank, suit } << ' ';
    std::cout << '\n';

    return 0;
}
并产生以下输出：
5H
AC 2C 3C 4C 5C 6C 7C 8C 9C TC JC QC KC AD 2D 3D 4D 5D 6D 7D 8D 9D TD JD QD KD AH 2H 3H 4H 5H 6H 7H 8H 9H TH JH QH KH AS 2S 3S 4S 5S 6S 7S 8S 9S TS JS QS KS
显示答案
#include <array>
#include <iostream>

struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    // These need to be static so they are only created once per program, not once per Card
    static constexpr std::array allRanks { rank_ace, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10, rank_jack, rank_queen, rank_king };
    static constexpr std::array allSuits { suit_club, suit_diamond, suit_heart, suit_spade };

    Rank rank{};
    Suit suit{};

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        static constexpr std::array ranks { 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' };
        static constexpr std::array suits { 'C', 'D', 'H', 'S' };

        out << ranks[card.rank] << suits[card.suit];
        return out;
    }

    int value() const
    {
        static constexpr std::array rankValues { 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
        return rankValues[rank];
    }
};

int main()
{
    // Print one card
    Card card { Card::rank_5, Card::suit_heart };
    std::cout << card << '\n';

    // Print all cards
    for (auto suit : Card::allSuits)
        for (auto rank : Card::allRanks)
            std::cout << Card { rank, suit } << ' ';
    std::cout << '\n';

    return 0;
}
> 第4步
接下来，我们来创建一副牌。创建一个名为
Deck
的类，其中包含一个
std::array
类型的 Card。您可以假定一副牌有 52 张。
甲板应该有三个功能
首先，默认构造函数应该初始化牌组数组。您可以使用类似于前面示例的 main() 函数中的范围 for 循环来遍历所有花色和牌面。
其次，添加一个
dealCard()
函数，该函数按值返回牌组中的下一张牌。由于
std::array
是一个固定大小的数组，请思考如何跟踪下一张牌的位置。当牌组中的所有牌都已发完时，调用此函数应断言失败。
第三，编写一个
shuffle()
成员函数来洗牌。为了简化，我们将借助
std::shuffle
。
#include <algorithm> // for std::shuffle
#include "Random.h"  // for Random::mt

    // Put this line in your shuffle function to shuffle m_cards using the Random::mt Mersenne Twister
    // This will rearrange all the Cards in the deck randomly
    std::shuffle(m_cards.begin(), m_cards.end(), Random::mt);
shuffle()
函数也应该将你跟踪下一张牌位置的方式重置回牌组的开头。
以下程序应该运行
int main()
{
    Deck deck{};
    std::cout << deck.dealCard() << ' ' << deck.dealCard() << ' ' << deck.dealCard() << '\n';

    deck.shuffle();
    std::cout << deck.dealCard() << ' ' << deck.dealCard() << ' ' << deck.dealCard() << '\n';

    return 0;
}
并产生以下输出（最后 3 张牌应随机化）
AC 2C 3C
2H 7H 9C
显示答案
#include <algorithm> // for std::shuffle
#include <array>
#include <cassert>
#include <iostream>
#include "Random.h"

struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    static constexpr std::array allRanks { rank_ace, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10, rank_jack, rank_queen, rank_king };
    static constexpr std::array allSuits { suit_club, suit_diamond, suit_heart, suit_spade };

    Rank rank{};
    Suit suit{};

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        static constexpr std::array ranks { 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' };
        static constexpr std::array suits { 'C', 'D', 'H', 'S' };

        out << ranks[card.rank] << suits[card.suit];
        return out;
    }

    int value() const
    {
        static constexpr std::array rankValues { 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
        return rankValues[rank];
    }
};

class Deck
{
private:
    std::array<Card, 52> m_cards {};
    std::size_t m_nextCardIndex { 0 };

public:
    Deck()
    {
        std::size_t count { 0 };
        for (auto suit: Card::allSuits)
            for (auto rank: Card::allRanks)
                m_cards[count++] = Card{rank, suit};
    }

    void shuffle()
    {
        std::shuffle(m_cards.begin(), m_cards.end(), Random::mt);
        m_nextCardIndex = 0;
    }

    Card dealCard()
    {
        assert(m_nextCardIndex != 52 && "Deck::dealCard ran out of cards");
        return m_cards[m_nextCardIndex++];
    }
};

int main()
{
    Deck deck{};
    std::cout << deck.dealCard() << ' ' << deck.dealCard() << ' ' << deck.dealCard() << '\n';

    deck.shuffle();
    std::cout << deck.dealCard() << ' ' << deck.dealCard() << ' ' << deck.dealCard() << '\n';

    return 0;
}
问题 #4
好的，现在让我们用我们的 Card 和 Deck 来实现一个简化版的二十一点！如果您还不熟悉二十一点，可以查看
二十一点
的维基百科文章。
这是我们版本的二十一点规则
庄家先发一张牌（现实中庄家发两张，但其中一张是面朝下，所以目前无关紧要）。
玩家先发两张牌。
玩家先行。
玩家可以反复“要牌”或“停牌”。
如果玩家“停牌”，则其回合结束，并根据所发牌计算其分数。
如果玩家“要牌”，他们会得到另一张牌，该牌的价值会加到他们的总分中。
一张 A 通常计为 1 或 11（以对总分更有利者为准）。为简单起见，这里我们将其计为 11。
如果玩家分数超过 21，则爆牌并立即输掉。
玩家完成后，轮到庄家。
庄家重复抽牌，直到分数达到 17 或以上，此时他们必须停止抽牌。
如果庄家分数超过 21，则爆牌，玩家立即获胜。
否则，如果玩家分数高于庄家，则玩家获胜。否则，玩家输（为简化起见，我们将平局视为庄家获胜）。
在我们简化版的二十一点中，我们不会跟踪玩家和庄家具体发到了哪些牌。我们只跟踪玩家和庄家发到的牌面总和。这样可以保持简单。
从您在之前的测验中编写的代码开始（或使用我们的参考解决方案）。
> 步骤 #1
创建一个名为
Player
的结构体，它将代表我们游戏中的参与者（庄家或玩家）。由于在这个游戏中我们只关心玩家的分数，所以这个结构体只需要一个成员。
编写一个函数，它将（最终）进行一轮二十一点游戏。目前，这个函数应该为庄家随机抽一张牌，为玩家随机抽两张牌。它应该返回一个布尔值，表示谁的分数更高。
代码应输出以下内容
The dealer is showing: 10
You have score: 13
You win!
The dealer is showing: 10
You have score: 8
You lose!
显示答案
#include <algorithm> // for std::shuffle
#include <array>
#include <cassert>
#include <iostream>
#include "Random.h"

struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    static constexpr std::array allRanks { rank_ace, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10, rank_jack, rank_queen, rank_king };
    static constexpr std::array allSuits { suit_club, suit_diamond, suit_heart, suit_spade };

    Rank rank{};
    Suit suit{};

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        static constexpr std::array ranks { 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' };
        static constexpr std::array suits { 'C', 'D', 'H', 'S' };

        out << ranks[card.rank] << suits[card.suit];
        return out;
    }

    int value() const
    {
        static constexpr std::array rankValues { 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
        return rankValues[rank];
    }
};

class Deck
{
private:
    std::array<Card, 52> m_cards {};
    std::size_t m_nextCardIndex { 0 };

public:
    Deck()
    {
        std::size_t count { 0 };
        for (auto suit: Card::allSuits)
            for (auto rank: Card::allRanks)
                m_cards[count++] = Card{rank, suit};
    }

    void shuffle()
    {
        std::shuffle(m_cards.begin(), m_cards.end(), Random::mt);
        m_nextCardIndex = 0;
    }

    Card dealCard()
    {
        assert(m_nextCardIndex != 52 && "Deck::dealCard ran out of cards");
        return m_cards[m_nextCardIndex++];
    }
};

struct Player
{
    int score{};
};

bool playBlackjack()
{
    Deck deck{};
    deck.shuffle();

    Player dealer{ deck.dealCard().value() };

    std::cout << "The dealer is showing: " << dealer.score << '\n';

    Player player { deck.dealCard().value() + deck.dealCard().value() };

    std::cout << "You have score: " << player.score << '\n';

    return (player.score > dealer.score);
}

int main()
{
    if (playBlackjack())
    {
        std::cout << "You win!\n";
    }
    else
    {
        std::cout << "You lose!\n";
    }

    return 0;
}
> 步骤 #2
添加一个
Settings
命名空间，其中包含两个常量：玩家爆牌的分数，以及庄家必须停止抽牌的分数。
添加处理庄家回合的逻辑。庄家将抽牌直到达到 17 点，然后他们必须停止。如果他们爆牌，玩家获胜。
以下是一些示例输出
The dealer is showing: 8
You have score: 9
The dealer flips a 4D.  They now have: 12
The dealer flips a JS.  They now have: 22
The dealer went bust!
You win!
The dealer is showing: 6
You have score: 13
The dealer flips a 3D.  They now have: 9
The dealer flips a 3H.  They now have: 12
The dealer flips a 9S.  They now have: 21
You lose!
The dealer is showing: 7
You have score: 21
The dealer flips a JC.  They now have: 17
You win!
显示答案
#include <algorithm> // for std::shuffle
#include <array>
#include <cassert>
#include <iostream>
#include "Random.h"

struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    static constexpr std::array allRanks { rank_ace, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10, rank_jack, rank_queen, rank_king };
    static constexpr std::array allSuits { suit_club, suit_diamond, suit_heart, suit_spade };

    Rank rank{};
    Suit suit{};

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        static constexpr std::array ranks { 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' };
        static constexpr std::array suits { 'C', 'D', 'H', 'S' };

        out << ranks[card.rank] << suits[card.suit];
        return out;
    }

    int value() const
    {
        static constexpr std::array rankValues { 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
        return rankValues[rank];
    }
};

class Deck
{
private:
    std::array<Card, 52> m_cards {};
    std::size_t m_nextCardIndex { 0 };

public:
    Deck()
    {
        std::size_t count { 0 };
        for (auto suit: Card::allSuits)
            for (auto rank: Card::allRanks)
                m_cards[count++] = Card{rank, suit};
    }

    void shuffle()
    {
        std::shuffle(m_cards.begin(), m_cards.end(), Random::mt);
        m_nextCardIndex = 0;
    }

    Card dealCard()
    {
        assert(m_nextCardIndex != 52 && "Deck::dealCard ran out of cards");
        return m_cards[m_nextCardIndex++];
    }

};

struct Player
{
    int score{};
};

namespace Settings
{
    // Maximum score before losing.
    constexpr int bust{ 21 };

    // Minium score that the dealer has to have.
    constexpr int dealerStopsAt{ 17 };
}

// Returns true if the dealer went bust. False otherwise.
bool dealerTurn(Deck& deck, Player& dealer)
{
    while (dealer.score < Settings::dealerStopsAt)
    {
        Card card { deck.dealCard() };
        dealer.score += card.value();
        std::cout << "The dealer flips a " << card << ".  They now have: " << dealer.score << '\n';
    }

    if (dealer.score > Settings::bust)
    {
        std::cout << "The dealer went bust!\n";
        return true;
    }
    
    return false;
}

bool playBlackjack()
{
    Deck deck{};
    deck.shuffle();

    Player dealer{ deck.dealCard().value() };

    std::cout << "The dealer is showing: " << dealer.score << '\n';

    Player player { deck.dealCard().value() + deck.dealCard().value() };

    std::cout << "You have score: " << player.score << '\n';

    if (dealerTurn(deck, dealer))
        return true;

    return (player.score > dealer.score);
}

int main()
{
    if (playBlackjack())
    {
        std::cout << "You win!\n";
    }
    else
    {
        std::cout << "You lose!\n";
    }

    return 0;
}
> 步骤 #3
最后，添加玩家回合的逻辑。这将完成游戏。
以下是一些示例输出
The dealer is showing: 2
You have score: 14
(h) to hit, or (s) to stand: h
You were dealt KH.  You now have: 24
You went bust!
You lose!
The dealer is showing: 10
You have score: 9
(h) to hit, or (s) to stand: h
You were dealt TH.  You now have: 19
(h) to hit, or (s) to stand: s
The dealer flips a 3D.  They now have: 13
The dealer flips a 7H.  They now have: 20
You lose!
The dealer is showing: 7
You have score: 12
(h) to hit, or (s) to stand: h
You were dealt 7S.  You now have: 19
(h) to hit, or (s) to stand: h
You were dealt 2D.  You now have: 21
(h) to hit, or (s) to stand: s
The dealer flips a 6H.  They now have: 13
The dealer flips a QC.  They now have: 23
The dealer went bust!
You win!
显示答案
#include <algorithm> // for std::shuffle
#include <array>
#include <cassert>
#include <iostream>
#include "Random.h"

struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    static constexpr std::array allRanks { rank_ace, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10, rank_jack, rank_queen, rank_king };
    static constexpr std::array allSuits { suit_club, suit_diamond, suit_heart, suit_spade };

    Rank rank{};
    Suit suit{};

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        static constexpr std::array ranks { 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' };
        static constexpr std::array suits { 'C', 'D', 'H', 'S' };

        out << ranks[card.rank] << suits[card.suit];
        return out;
    }

    int value() const
    {
        static constexpr std::array rankValues { 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
        return rankValues[rank];
    }
};

class Deck
{
private:
    std::array<Card, 52> m_cards {};
    std::size_t m_nextCardIndex { 0 };

public:
    Deck()
    {
        std::size_t count { 0 };
        for (auto suit: Card::allSuits)
            for (auto rank: Card::allRanks)
                m_cards[count++] = Card{rank, suit};
    }

    void shuffle()
    {
        std::shuffle(m_cards.begin(), m_cards.end(), Random::mt);
        m_nextCardIndex = 0;
    }

    Card dealCard()
    {
        assert(m_nextCardIndex != 52 && "Deck::dealCard ran out of cards");
        return m_cards[m_nextCardIndex++];
    }

};

struct Player
{
    int score{};
};

namespace Settings
{
    // Maximum score before losing.
    constexpr int bust{ 21 };

    // Minium score that the dealer has to have.
    constexpr int dealerStopsAt{ 17 };
}

bool playerWantsHit()
{
    while (true)
    {
        std::cout << "(h) to hit, or (s) to stand: ";

        char ch{};
        std::cin >> ch;

        switch (ch)
        {
            case 'h':
                return true;
            case 's':
                return false;
        }
    }
}

// Returns true if the player went bust. False otherwise.
bool playerTurn(Deck& deck, Player& player)
{
    while (player.score < Settings::bust && playerWantsHit())
    {
        Card card { deck.dealCard() };
        player.score += card.value();

        std::cout << "You were dealt " << card  << ". You now have: " << player.score << '\n';
    }

    if (player.score > Settings::bust)
    {
        std::cout << "You went bust!\n";
        return true;
    }

    return false;
}

// Returns true if the dealer went bust. False otherwise.
bool dealerTurn(Deck& deck, Player& dealer)
{
    while (dealer.score < Settings::dealerStopsAt)
    {
        Card card { deck.dealCard() };
        dealer.score += card.value();
        std::cout << "The dealer flips a " << card << ".  They now have: " << dealer.score << '\n';
    }

    if (dealer.score > Settings::bust)
    {
        std::cout << "The dealer went bust!\n";
        return true;
    }

    return false;
}

bool playBlackjack()
{
    Deck deck{};
    deck.shuffle();

    Player dealer{ deck.dealCard().value() };

    std::cout << "The dealer is showing: " << dealer.score << '\n';

    Player player { deck.dealCard().value() + deck.dealCard().value() };

    std::cout << "You have score: " << player.score << '\n';

    if (playerTurn(deck, player))
        return false;

    if (dealerTurn(deck, dealer))
        return true;

    return (player.score > dealer.score);
}

int main()
{
    if (playBlackjack())
    {
        std::cout << "You win!\n";
    }
    else
    {
        std::cout << "You lose!\n";
    }

    return 0;
}
问题 #5
a) 描述如何修改上述程序以处理 A 可以等于 1 或 11 的情况。
重要的是要注意，我们只跟踪牌的总和，而不是用户具体有哪些牌。
显示答案
一种方法是跟踪玩家和庄家发到的 A 的数量（在
Player
结构体中，作为整数）。如果玩家或庄家超过 21 点且其 A 计数器大于零，则可以将他们的分数减少 10（将 A 从 11 点转换为 1 点）并递减 A 计数器。这可以根据需要重复多次，直到 A 计数器达到零。
b) 在实际的二十一点游戏中，如果玩家和庄家得分相同（且玩家未爆牌），结果是平局，双方均不赢。描述你将如何修改上述程序来处理这种情况。
显示答案
我们的
playBlackjack()
版本目前返回一个布尔值，指示玩家是否获胜。我们需要更新此函数以返回三种可能性：庄家赢、玩家赢、平局。最好的方法是为这三个选项定义一个枚举，并让函数返回相应的枚举器。
c) 额外奖励：将上述两个想法实现到你的二十一点游戏中。请注意，你需要显示庄家的初始牌和玩家的初始两张牌，以便他们知道自己是否有 A。
以下是示例输出：
The dealer is showing JH (10)
You are showing AH 7D (18)
(h) to hit, or (s) to stand: h
You were dealt JD.  You now have: 18
(h) to hit, or (s) to stand: s
The dealer flips a 6C.  They now have: 16
The dealer flips a AD.  They now have: 17
You win!
显示答案
#include <algorithm> // for std::shuffle
#include <array>
#include <cassert>
#include <iostream>
#include "Random.h"

namespace Settings
{
    // Maximum score before losing.
    constexpr int bust{ 21 };

    // Minium score that the dealer has to have.
    constexpr int dealerStopsAt{ 17 };
}

struct Card
{
    enum Rank
    {
        rank_ace,
        rank_2,
        rank_3,
        rank_4,
        rank_5,
        rank_6,
        rank_7,
        rank_8,
        rank_9,
        rank_10,
        rank_jack,
        rank_queen,
        rank_king,

        max_ranks
    };

    enum Suit
    {
        suit_club,
        suit_diamond,
        suit_heart,
        suit_spade,

        max_suits
    };

    static constexpr std::array allRanks { rank_ace, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10, rank_jack, rank_queen, rank_king };
    static constexpr std::array allSuits { suit_club, suit_diamond, suit_heart, suit_spade };

    Rank rank{};
    Suit suit{};

    friend std::ostream& operator<<(std::ostream& out, const Card &card)
    {
        static constexpr std::array ranks { 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' };
        static constexpr std::array suits { 'C', 'D', 'H', 'S' };

        out << ranks[card.rank] << suits[card.suit];
        return out;
    }

    int value() const
    {
        static constexpr std::array rankValues { 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
        return rankValues[rank];
    }
};

class Deck
{
private:
    std::array<Card, 52> m_cards {};
    std::size_t m_nextCardIndex { 0 };

public:
    Deck()
    {
        std::size_t count { 0 };
        for (auto suit: Card::allSuits)
            for (auto rank: Card::allRanks)
                m_cards[count++] = Card{rank, suit};
    }

    void shuffle()
    {
        std::shuffle(m_cards.begin(), m_cards.end(), Random::mt);
        m_nextCardIndex = 0;
    }

    Card dealCard()
    {
        assert(m_nextCardIndex != 52 && "Deck::dealCard ran out of cards");
        return m_cards[m_nextCardIndex++];
    }

};

class Player
{
private:
    int m_score{ };
    int m_ace11Count { 0 }; // how many aces worth 11 points the player has

public:
    // We'll use a function to add the card to the player's score
    // Since we now need to count aces
    void addToScore(Card card)
    {
        m_score += card.value();
        if (card.rank == Card::rank_ace)
            ++m_ace11Count; // aces start at 11 points
        consumeAces();
    }

    // Decrease aceCount by 1 and 
    void consumeAces()
    {
        // If the player would bust, see if we can switch aces from 11 points to 1
        while (m_score > Settings::bust && m_ace11Count > 0)
        {
            m_score -= 10;
            --m_ace11Count;
        }
    }

    int score() { return m_score; }
};

bool playerWantsHit()
{
    while (true)
    {
        std::cout << "(h) to hit, or (s) to stand: ";

        char ch{};
        std::cin >> ch;

        switch (ch)
        {
            case 'h':
                return true;
            case 's':
                return false;
        }
    }
}

// Returns true if the player went bust. False otherwise.
bool playerTurn(Deck& deck, Player& player)
{
    while (player.score() < Settings::bust && playerWantsHit())
    {
        Card card { deck.dealCard() };
        player.addToScore(card);

        std::cout << "You were dealt " << card  << ". You now have: " << player.score() << '\n';
    }

    if (player.score() > Settings::bust)
    {
        std::cout << "You went bust!\n";
        return true;
    }

    return false;
}


// Returns true if the dealer went bust. False otherwise.
bool dealerTurn(Deck& deck, Player& dealer)
{
    while (dealer.score() < Settings::dealerStopsAt)
    {
        Card card { deck.dealCard() };
        dealer.addToScore(card);

        std::cout << "The dealer flips a " << card << ".  They now have: " << dealer.score() << '\n';
    }

    if (dealer.score() > Settings::bust)
    {
        std::cout << "The dealer went bust!\n";
        return true;
    }

    return false;
}

enum class GameResult
{
    playerWon,
    dealerWon,
    tie
};

GameResult playBlackjack()
{
    Deck deck{};
    deck.shuffle();

    Player dealer{};
    Card card1 { deck.dealCard() };
    dealer.addToScore(card1);
    std::cout << "The dealer is showing " << card1 << " (" << dealer.score() << ")\n";

    Player player{};
    Card card2 { deck.dealCard() };
    Card card3 { deck.dealCard() };
    player.addToScore(card2);
    player.addToScore(card3);
    std::cout << "You are showing " << card2 << ' ' << card3 << " (" << player.score() << ")\n";

    if (playerTurn(deck, player)) // if player busted
        return GameResult::dealerWon;

    if (dealerTurn(deck, dealer)) // if dealer busted
        return GameResult::playerWon;

    if (player.score() == dealer.score())
        return GameResult::tie;

    return (player.score() > dealer.score() ? GameResult::playerWon : GameResult::dealerWon);
}

int main()
{
    switch (playBlackjack())
    {
    case GameResult::playerWon:
        std::cout << "You win!\n";
        return 0;
    case GameResult::dealerWon:
        std::cout << "You lose!\n";
        return 0;
    case GameResult::tie:
        std::cout << "It's a tie.\n";
        return 0;
    }

    return 0;
}
下一课
18.1
使用选择排序对数组进行排序
返回目录
上一课
17.13
多维 std::array