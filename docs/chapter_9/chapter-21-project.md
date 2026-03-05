# 21.y — 第 21 章项目

21.y — 第 21 章项目
Alex
2023 年 3 月 30 日，下午 1:02 PDT
2024 年 9 月 13 日
向读者 Avtem 致敬，感谢他构思并合作完成了这个项目。
项目时间
让我们来实现经典游戏
15 拼图
！
在 15 拼图中，你开始时是一个随机的 4×4 格子，其中有 15 个瓷砖编号从 1 到 15，缺少一个瓷砖。
例如
15   1   4
  2   5   9  12
  7   8  11  14
 10  13   6   3
在这个拼图中，缺失的瓷砖位于左上角。
在游戏的每一回合中，你都会选择一个与缺失瓷砖相邻的瓷砖，并将其滑入缺失瓷砖所在的位置。
游戏的目标是滑动瓷砖，直到它们按数字顺序排列，缺失的瓷砖位于右下角
1   2   3   4
  5   6   7   8
  9  10  11  12
 13  14  15
你可以在
这个网站
上玩几回合。这将帮助你理解这个游戏是如何运作的以及如何实现它。
在我们的游戏中，每一回合用户将输入一个字母命令。有 5 个有效命令
w - 向上滑动瓷砖
a - 向左滑动瓷砖
s - 向下滑动瓷砖
d - 向右滑动瓷砖
q - 退出游戏
由于这将是一个更长的程序，我们将分阶段开发它。
还有一点：在每个步骤中，我们将呈现两件事：一个
目标
和
任务
。目标定义了该步骤试图实现的结果，以及任何其他相关信息。任务提供了有关如何实现目标的详细信息和提示。
任务最初将隐藏起来，以鼓励你尝试仅使用目标和示例输出或示例程序来完成每个步骤。如果你不确定如何开始，或者感到卡住，可以取消隐藏任务。它们应该能帮助你前进。
> 步骤 #1
由于这将是一个更大的程序，让我们从设计练习开始。
作者注
如果你在程序预先设计方面经验不足，你可能会觉得这有点困难。这是预料之中的。重要的是你参与并学习，而不是你是否做得对。
我们将在后续步骤中详细介绍所有这些项目，因此如果你感到完全不知所措，请随意跳过此步骤。
目标：记录此程序的主要需求，并从高层次规划程序结构。我们将分三部分完成此操作。
A) 你的程序需要做哪些顶层事情？这里有一些可以帮助你入门
棋盘相关
显示游戏棋盘
…
用户相关
从用户获取命令
…
显示答案
棋盘相关
显示游戏棋盘
显示单个瓷砖
随机化起始状态
滑动瓷砖
确定是否达到胜利条件
用户相关
从用户获取命令
处理无效输入
允许用户在获胜前退出
B) 你将使用哪些主要类或命名空间来实现步骤 1 中列出的项目？另外，你的 main() 函数将做什么？
您可以创建一张图表，或者使用两个这样的表格
主要类/命名空间/主函数
实现顶层项目
成员
类 Board
显示游戏棋盘
…
…
函数 main
主游戏逻辑循环
…
…
显示答案
主要类/命名空间/主函数
实现顶层项目
成员（类型）
类 Board
显示游戏棋盘
随机化起始状态
滑动瓷砖
确定是否达到胜利条件
Tile 的二维数组
类 Tile
显示单个瓷砖
int 显示数字
命名空间 UserInput
从用户获取命令
处理无效输入
无
函数 main()
主游戏逻辑循环
允许用户在获胜前退出
无
以下是上述选择背后的理由。
class Board
: 我们的游戏是一个 4×4 的棋盘。这个类的主要目的是存储和管理二维瓷砖数组。这个类还负责随机化、移动瓷砖、显示棋盘以及检查棋盘是否已解决。
class Tile
：这个类表示游戏棋盘中的一个瓷砖。在这里使用类允许我们重载输出运算符，以我们想要的格式输出瓷砖。它还允许我们拥有命名良好的成员函数，这将提高与单个瓷砖相关的代码的可读性。
namespace UserInput
：这个命名空间有用于从用户获取输入、检查用户输入是否有效以及处理无效输入的函数。因为它没有任何状态，所以我们不需要在这里使用类。
函数 main()
：这是我们的主游戏循环将编写的地方。它将处理游戏棋盘的设置、协调检索用户输入和命令处理，以及处理退出条件（当用户获胜或输入退出命令时）。
我们还将使用两个辅助类。这些类的必要性可能乍一看并不明显，所以如果你没有想到类似的东西，也不用担心。通常，辅助类的必要性（或好处）直到你深入实现程序之后才会显现出来。
C) (额外加分) 你能想到任何有助于使上述实现更容易或更具凝聚力的辅助类或功能吗？
显示答案
辅助类/命名空间
这有什么帮助？
成员（类型）
类 Point
索引游戏棋盘瓷砖
int x 轴和 y 轴坐标
类 Direction
使方向命令的工作更轻松、更直观
枚举 direction
class Point
：访问我们二维瓷砖数组中的特定瓷砖将需要两个索引。我们可以将它们视为 {x 轴，y 轴} 索引对。这个 Point 类实现了这样一个索引对，以便于传递或返回一对索引。
class Direction
：用户将通过键盘输入单字母（char）命令来向基本方向滑动瓷砖（例如
'w'
=向上，
'a'
=向左）。将这些字符命令转换为 Direction 对象（表示基本方向）将使我们的代码更直观，并防止我们的代码中散布着字符字面量（
Direction::left
比
'a'
更有意义）。
如果你觉得这个练习很难，没关系。这里的目标主要是让你在开始动手之前思考一下你要做什么。
现在，是时候开始实施了！
> 步骤 #2
目标：能够在屏幕上显示单个瓷砖。
我们的游戏棋盘是一个 4×4 的瓷砖网格，可以滑动。因此，拥有一个表示我们 4×4 网格上的编号瓷砖或缺失瓷砖的
Tile
类将很有用。每个瓷砖都应该能够
给定一个数字或设置为缺失的瓷砖
确定它是否是缺失的瓷砖。
以适当的间距绘制到控制台（以便在显示棋盘时瓷砖能够对齐）。请参阅下面的示例输出，了解瓷砖应如何间隔的示例。
显示任务
我们的
Tile
类应该具有以下功能
一个默认构造函数。
一个构造函数，允许我们创建一个带有显示值的 Tile。因为我们不使用
0
作为显示值，所以我们可以使用值
0
来标识我们缺失的 Tile。
一个
getNum()
访问函数，返回瓷砖所持有的值。
一个
isEmpty()
成员函数，返回一个布尔值，指示当前瓷砖是否是缺失瓷砖。
一个重载的
operator<<
，它将显示瓷砖所持有的值。
以下代码应该能够编译并在代码下方产生您可以看到的输出结果
int main()
{
    Tile tile1{ 10 };
    Tile tile2{ 8 };
    Tile tile3{ 0 }; // the missing tile
    Tile tile4{ 1 };

    std::cout << "0123456789ABCDEF\n"; // to make it easy to see how many spaces are in the next line
    std::cout << tile1 << tile2 << tile3 << tile4 << '\n';
    
    std::cout << std::boolalpha << tile1.isEmpty() << ' ' << tile3.isEmpty() << '\n';
    std::cout << "Tile 2 has number: " << tile2.getNum() << "\nTile 4 has number: " << tile4.getNum() << '\n';
    
    return 0;
}
预期输出（注意空格）
0123456789ABCDEF
 10   8       1 
false true
Tile 2 has number: 8
Tile 4 has number: 1
显示答案
#include <iostream>

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }

    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

int main()
{
    Tile tile1{ 10 };
    Tile tile2{ 8 };
    Tile tile3{ 0 }; // the missing tile
    Tile tile4{ 1 };

    std::cout << "0123456789ABCDEF\n"; // to make it easy to see how many spaces are in the next line
    std::cout << tile1 << tile2 << tile3 << tile4 << '\n';

    std::cout << std::boolalpha << tile1.isEmpty() << ' ' << tile3.isEmpty() << '\n';
    std::cout << "Tile 2 has number: " << tile2.getNum() << "\nTile 4 has number: " << tile4.getNum() << '\n';

    return 0;
}
> 步骤 #3
目标：创建一个已解决的棋盘（4×4 瓷砖网格）并将其显示在屏幕上。
定义一个表示 4×4 瓷砖网格的 `Board` 类。新创建的 `Board` 对象应处于已解决状态。要显示棋盘，首先打印 `g_consoleLines`（在下面的代码片段中定义）空行，然后打印棋盘本身。这样做将确保任何先前的输出都被推出视野，以便只有当前棋盘在控制台上可见。
为什么要以已解决状态启动棋盘？当你购买这些拼图的实体版本时，拼图通常以已解决状态开始——你必须手动将它们打乱（通过滑动瓷砖）才能尝试解决它们。我们将在程序中模仿这个过程（我们将在未来的步骤中进行打乱）。
显示任务
`Board` 类应具有以下功能
一个
constexpr
符号常量，设置为网格的大小（您可以假设网格是正方形的）。
一个
Tile
对象的二维数组，它将存储我们的 16 个数字。这些数字应以已解决的状态开始。
一个默认构造函数。
一个重载的
operator<<
，它将打印 N 个空行（其中 N =
g_consoleLines
的值），然后将棋盘绘制到控制台。
以下程序应该运行
// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

// Your code goes here

int main()
{
    Board board{};
    std::cout << board;

    return 0;
}
并输出以下内容
1   2   3   4
  5   6   7   8
  9  10  11  12
 13  14  15
显示答案
#include <iostream>

// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }
    
    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

class Board
{
public:

    Board() = default;

    friend std::ostream& operator<<(std::ostream& stream, const Board& board)
    {
        // Before drawing always print some empty lines
        // so that only one board appears at a time
        // and it's always shown at the bottom of the window
        // because console window scrolls automatically when there is no
        // enough space. 
        for (int i = 0; i < g_consoleLines; ++i)
            std::cout << '\n';

        for (int y = 0; y < s_size; ++y)
        {
            for (int x = 0; x < s_size; ++x)
                stream << board.m_tiles[y][x];
            stream << '\n';
        }

        return stream;
    }

private:
    static constexpr int s_size { 4 };
    Tile m_tiles[s_size][s_size]{
        Tile{ 1 }, Tile { 2 }, Tile { 3 } , Tile { 4 },
        Tile { 5 } , Tile { 6 }, Tile { 7 }, Tile { 8 },
        Tile { 9 }, Tile { 10 }, Tile { 11 }, Tile { 12 },
        Tile { 13 }, Tile { 14 }, Tile { 15 }, Tile { 0 } };
};

int main()
{
    Board board{};
    std::cout << board;

    return 0;
}
> 第4步
目标：在此步骤中，我们将允许用户重复输入游戏命令，处理无效输入，并实现退出游戏命令。
以下是我们的游戏将支持的 5 个命令（每个命令都将作为单个字符输入）
‘w’ - 向上滑动瓷砖
‘a’ - 向左滑动瓷砖
‘s’ - 向下滑动瓷砖
‘d’ - 向右滑动瓷砖
‘q’ - 退出游戏
当用户运行游戏时，将发生以下情况
(已解决的)棋盘应打印到控制台。
程序应反复从用户获取有效的游戏命令。如果用户输入无效命令或冗余输入，则忽略它。
对于每个有效的游戏命令
打印
"有效命令: "
和用户输入的字符。
如果命令是退出命令，则同时打印
"\n\n再见!\n\n"
，然后退出应用程序。
由于我们的用户输入例程不需要维护任何状态，请将它们实现在名为
UserInput
的命名空间中。
显示任务
实现
UserInput
命名空间
创建一个名为
getCommandFromUser()
的函数。从用户读取一个字符。如果该字符不是有效的游戏命令，则清除任何额外的冗余输入，并从用户读取另一个字符。重复此操作，直到输入有效的游戏命令。将有效的命令返回给调用者。
创建尽可能多的辅助函数。
在 main() 中
实现一个无限循环。在循环内部，获取一个有效的游戏命令，然后根据上述要求处理命令。
程序的输出应与以下内容匹配
1   2   3   4
  5   6   7   8
  9  10  11  12
 13  14  15
w
Valid command: w
a
Valid command: a
s
Valid command: s
d
Valid command: d
f
g
h
Valid command: q


Bye!
显示答案
#include <iostream>
#include <limits>

// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

namespace UserInput
{
    bool isValidCommand(char ch)
    {
        return ch == 'w'
            || ch == 'a'
            || ch == 's'
            || ch == 'd'
            || ch == 'q';
    }

    void ignoreLine()
    {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    char getCharacter()
    {
        char operation{};
        std::cin >> operation;
        ignoreLine(); // remove any extraneous input
        return operation;
    }

    char getCommandFromUser()
    {
        char ch{};
        while (!isValidCommand(ch))
            ch = getCharacter();

        return ch;
    }
};

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }
    
    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

class Board
{
public:

    Board() = default;

    friend std::ostream& operator<<(std::ostream& stream, const Board& board)
    {
        // Before drawing always print some empty lines
        // so that only one board appears at a time
        // and it's always shown at the bottom of the window
        // because console window scrolls automatically when there is no
        // enough space. 
        for (int i = 0; i < g_consoleLines; ++i)
            std::cout << '\n';

        for (int y = 0; y < s_size; ++y)
        {
            for (int x = 0; x < s_size; ++x)
                stream << board.m_tiles[y][x];
            stream << '\n';
        }

        return stream;
    }

private:
    static constexpr int s_size { 4 };
    Tile m_tiles[s_size][s_size]{
        Tile{ 1 }, Tile { 2 }, Tile { 3 } , Tile { 4 },
        Tile { 5 } , Tile { 6 }, Tile { 7 }, Tile { 8 },
        Tile { 9 }, Tile { 10 }, Tile { 11 }, Tile { 12 },
        Tile { 13 }, Tile { 14 }, Tile { 15 }, Tile { 0 } };
};

int main()
{
    Board board{};
    std::cout << board;

    while (true)
    {
        char ch{ UserInput::getCommandFromUser() };

        // If we reach the line below, "ch" will ALWAYS be a correct command!
        std::cout << "Valid command: " << ch << '\n';
        
        // Handle non-direction commands
        if (ch == 'q')
        {
            std::cout << "\n\nBye!\n\n";
            return 0;
        }
    }

    return 0;
}
> 步骤 #5
目标：实现一个辅助类，使我们更容易处理方向命令。
在完成上一步之后，我们可以接受用户的命令（以字符“w”、“a”、“s”、“d”和“q”的形式）。这些字符在我们的代码中本质上是魔法数字。虽然在我们的
UserInput
命名空间和函数
main()
中处理这些命令是可行的，但我们不希望将它们传播到整个程序中。例如，
Board
类不应该知道“s”是什么意思。
实现一个名为
Direction
的辅助类，它将允许我们创建表示基本方向（上、左、下或右）的对象。
operator-
应返回相反的方向，
operator<<
应将方向打印到控制台。我们还需要一个成员函数，它将返回一个包含随机方向的 Direction 对象。最后，向
UserInput
命名空间添加一个函数，用于将方向性游戏命令（“w”、“a”、“s”或“d”）转换为 Direction 对象。
我们越能使用
Direction
而不是方向性游戏命令，我们的代码就越容易阅读和理解。
显示任务
实现
Direction
类，它具有
一个名为
Type
的公共嵌套枚举，包含枚举器
up
、
down
、
left
、
right
和
maxDirections
。
一个存储实际方向的私有成员。
一个单参数构造函数，允许我们使用
Type
初始化器初始化
Direction
。
一个重载的
operator-
，它接受一个 Direction 并返回相反的 Direction。
一个重载的
operator<<
，它将方向名称输出到控制台。
一个静态函数，返回一个带有随机
Type
的 Direction。您可以使用
“Random.h”
头文件中的
Random::get()
函数来生成随机数。
此外，在
UserInput
命名空间中，添加以下内容
一个将方向游戏命令（字符）转换为 Direction 对象的函数。
最后，修改您在上一步中编写的程序，使其输出与以下内容匹配
1   2   3   4
  5   6   7   8
  9  10  11  12
 13  14  15
Generating random direction... up
Generating random direction... down
Generating random direction... up
Generating random direction... left

Enter a command: w
You entered direction: up
a
You entered direction: left
s
You entered direction: down
d
You entered direction: right
q


Bye!
显示答案
#include <cassert>
#include <iostream>
#include <limits>
#include "Random.h"

// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

class Direction
{
public:
    enum Type
    {
        up,
        down,
        left,
        right,
        maxDirections,
    };

    Direction(Type type)
        :m_type(type)
    {
    }

    Type getType() const
    {
        return m_type;
    }

    Direction operator-() const
    {
        switch (m_type)
        {
        case up:    return Direction{ down };
        case down:  return Direction{ up };
        case left:  return Direction{ right };
        case right: return Direction{ left };
        default:    break;
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ up };
    }
 
    static Direction getRandomDirection()
    {
        Type random{ static_cast<Type>(Random::get(0, Type::maxDirections - 1)) };
        return Direction{ random };
    }

private:
    Type m_type{};
};

std::ostream& operator<<(std::ostream& stream, Direction dir)
{
    switch (dir.getType())
    {
    case Direction::up:     return (stream << "up");
    case Direction::down:   return (stream << "down");
    case Direction::left:   return (stream << "left");
    case Direction::right:  return (stream << "right");
    default:                break;
    }

    assert(0 && "Unsupported direction was passed!");
    return (stream << "unknown direction");
}

namespace UserInput
{
    bool isValidCommand(char ch)
    {
        return ch == 'w'
            || ch == 'a'
            || ch == 's'
            || ch == 'd'
            || ch == 'q';
    }

    void ignoreLine()
    {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    char getCharacter()
    {
        char operation{};
        std::cin >> operation;
        ignoreLine(); // remove any extraneous input
        return operation;
    }

    char getCommandFromUser()
    {
        char ch{};
        while (!isValidCommand(ch))
            ch = getCharacter();

        return ch;
    }

    Direction charToDirection(char ch)
    {
        switch (ch)
        {
        case 'w': return Direction{ Direction::up };
        case 's': return Direction{ Direction::down };
        case 'a': return Direction{ Direction::left };
        case 'd': return Direction{ Direction::right };
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ Direction::up };
    }
};

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }
    
    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

class Board
{
public:

    Board() = default;

    static void printEmptyLines(int count)
    {
        for (int i = 0; i < count; ++i)
            std::cout << '\n';
    }

    friend std::ostream& operator<<(std::ostream& stream, const Board& board)
    {
        // Before drawing always print some empty lines
        // so that only one board appears at a time
        // and it's always shown at the bottom of the window
        // because console window scrolls automatically when there is no
        // enough space. 
        for (int i = 0; i < g_consoleLines; ++i)
            std::cout << '\n';

        for (int y = 0; y < s_size; ++y)
        {
            for (int x = 0; x < s_size; ++x)
                stream << board.m_tiles[y][x];
            stream << '\n';
        }

        return stream;
    }

private:
    static constexpr int s_size { 4 };
    Tile m_tiles[s_size][s_size]{
        Tile{ 1 }, Tile { 2 }, Tile { 3 } , Tile { 4 },
        Tile { 5 } , Tile { 6 }, Tile { 7 }, Tile { 8 },
        Tile { 9 }, Tile { 10 }, Tile { 11 }, Tile { 12 },
        Tile { 13 }, Tile { 14 }, Tile { 15 }, Tile { 0 } };
};

int main()
{
    Board board{};
    std::cout << board;

    std::cout << "Generating random direction... " << Direction::getRandomDirection() << '\n';
    std::cout << "Generating random direction... " << Direction::getRandomDirection() << '\n';
    std::cout << "Generating random direction... " << Direction::getRandomDirection() << '\n';
    std::cout << "Generating random direction... " << Direction::getRandomDirection() << "\n\n";

    std::cout << "Enter a command: ";
    while (true)
    {
        char ch{ UserInput::getCommandFromUser() };

        // Handle non-direction commands
        if (ch == 'q')
        {
            std::cout << "\n\nBye!\n\n";
            return 0;
        }

        // Handle direction commands
        Direction dir{ UserInput::charToDirection(ch) };

        std::cout << "You entered direction: " << dir << '\n';
    }

    return 0;
}
> 步骤 #6
目标：实现一个辅助类，使我们更容易索引游戏棋盘中的瓷砖。
我们的游戏棋盘是一个 4×4 的
Tile
网格，我们将其存储在
Board
类的二维数组成员
m_tiles
中。我们将使用其 {x, y} 坐标访问给定的瓷砖。例如，左上角的瓷砖坐标为 {0, 0}。其右侧的瓷砖坐标为 {1, 0}（x 变为 1，y 保持 0）。其下方一个的瓷砖坐标为 {1, 1}。
由于我们将大量使用坐标，因此创建一个名为
Point
的辅助类，用于存储 {x, y} 坐标对。我们应该能够比较两个 Point 对象是否相等和不相等。还要实现一个名为
getAdjacentPoint
的成员函数，它将 Direction 对象作为参数并返回该方向的 Point。例如，
Point{1, 1}.getAdjacentPoint(Direction::right)
==
Point{2, 1}
。
显示任务
实现一个名为
Point
的结构体。它应该包含
两个公共数据成员，用于存储 x 轴和 y 轴坐标。
一个重载的
operator==
和
operator!=
，用于比较两组坐标。
一个常量成员函数
Point getAdjacentPoint(Direction)
，返回 Direction 参数方向上的 Point。这里不需要进行任何有效性检查。
我们在这里使用结构体而不是类，因为 Point 是一个简单的数据捆绑，封装带来的好处很小。
保存您上一步的
main()
函数，您将在下一步中再次用到它。
以下代码应该运行并为每个测试用例打印
true
// Your code goes here

// Note: save your main() from the prior step, as you'll need it again in the next step
int main()
{
    std::cout << std::boolalpha;
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::up)    == Point{ 1, 0 }) << '\n';
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::down)  == Point{ 1, 2 }) << '\n';
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::left)  == Point{ 0, 1 }) << '\n';
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::right) == Point{ 2, 1 }) << '\n';
    std::cout << (Point{ 1, 1 } != Point{ 2, 1 }) << '\n';
    std::cout << (Point{ 1, 1 } != Point{ 1, 2 }) << '\n';
    std::cout << !(Point{ 1, 1 } != Point{ 1, 1 }) << '\n';

    return 0;
}
显示答案
#include <array>
#include <cassert>
#include <iostream>
#include <limits>
#include "Random.h"

// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

class Direction
{
public:
    enum Type
    {
        up,
        down,
        left,
        right,
        maxDirections,
    };

    Direction(Type type)
        :m_type(type)
    {
    }

    Type getType() const
    {
        return m_type;
    }

    Direction operator-() const
    {
        switch (m_type)
        {
        case up:    return Direction{ down };
        case down:  return Direction{ up };
        case left:  return Direction{ right };
        case right: return Direction{ left };
        default:    break;
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ up };
    }

    static Direction getRandomDirection()
    {
        Type random{ static_cast<Type>(Random::get(0, Type::maxDirections - 1)) };
        return Direction{ random };
    }

private:
    Type m_type{};
};


std::ostream& operator<<(std::ostream& stream, Direction dir)
{
    switch (dir.getType())
    {
    case Direction::up:     return (stream << "up");
    case Direction::down:   return (stream << "down");
    case Direction::left:   return (stream << "left");
    case Direction::right:  return (stream << "right");
    default:                break;
    }

    assert(0 && "Unsupported direction was passed!");
    return (stream << "unknown direction");
}

struct Point
{
    int x{};
    int y{};

    friend bool operator==(Point p1, Point p2)
    {
        return p1.x == p2.x && p1.y == p2.y;
    }

    friend bool operator!=(Point p1, Point p2)
    {
        return !(p1 == p2);
    }

    Point getAdjacentPoint(Direction dir) const
    {
        switch (dir.getType())
        {
        case Direction::up:     return Point{ x,     y - 1 };
        case Direction::down:   return Point{ x,     y + 1 };
        case Direction::left:   return Point{ x - 1, y };
        case Direction::right:  return Point{ x + 1, y };
        default:                break;
        }

        assert(0 && "Unsupported direction was passed!");
        return *this;
    }
};

namespace UserInput
{
    bool isValidCommand(char ch)
    {
        return ch == 'w'
            || ch == 'a'
            || ch == 's'
            || ch == 'd'
            || ch == 'q';
    }

    void ignoreLine()
    {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    char getCharacter()
    {
        char operation{};
        std::cin >> operation;
        ignoreLine(); // remove any extraneous input
        return operation;
    }

    char getCommandFromUser()
    {
        char ch{};
        while (!isValidCommand(ch))
            ch = getCharacter();

        return ch;
    }

    Direction charToDirection(char ch)
    {
        switch (ch)
        {
        case 'w': return Direction{ Direction::up };
        case 's': return Direction{ Direction::down };
        case 'a': return Direction{ Direction::left };
        case 'd': return Direction{ Direction::right };
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ Direction::up };
    }
};

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }
    
    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

class Board
{
public:

    Board() = default;

    static void printEmptyLines(int count)
    {
        for (int i = 0; i < count; ++i)
            std::cout << '\n';
    }

    friend std::ostream& operator<<(std::ostream& stream, const Board& board)
    {
        // Before drawing always print some empty lines
        // so that only one board appears at a time
        // and it's always shown at the bottom of the window
        // because console window scrolls automatically when there is no
        // enough space. 
        for (int i = 0; i < g_consoleLines; ++i)
            std::cout << '\n';

        for (int y = 0; y < s_size; ++y)
        {
            for (int x = 0; x < s_size; ++x)
                stream << board.m_tiles[y][x];
            stream << '\n';
        }

        return stream;
    }

private:
    static constexpr int s_size { 4 };
    Tile m_tiles[s_size][s_size]{
        Tile{ 1 }, Tile { 2 }, Tile { 3 } , Tile { 4 },
        Tile { 5 } , Tile { 6 }, Tile { 7 }, Tile { 8 },
        Tile { 9 }, Tile { 10 }, Tile { 11 }, Tile { 12 },
        Tile { 13 }, Tile { 14 }, Tile { 15 }, Tile { 0 } };
};

int main()
{
    std::cout << std::boolalpha;
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::up)    == Point{ 1, 0 }) << '\n';
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::down)  == Point{ 1, 2 }) << '\n';
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::left)  == Point{ 0, 1 }) << '\n';
    std::cout << (Point{ 1, 1 }.getAdjacentPoint(Direction::right) == Point{ 2, 1 }) << '\n';
    std::cout << (Point{ 1, 1 } != Point{ 2, 1 }) << '\n';
    std::cout << (Point{ 1, 1 } != Point{ 1, 2 }) << '\n';
    std::cout << !(Point{ 1, 1 } != Point{ 1, 1 }) << '\n';

    return 0;
}
> 步骤 #7
目标：添加玩家在棋盘上滑动瓷砖的功能。
首先，我们应该更仔细地了解滑动瓷砖是如何实际运作的
给定一个看起来像这样的拼图状态
15   1   4
  2   5   9  12
  7   8  11  14
 10  13   6   3
当用户在键盘上输入“w”时，唯一可以向上移动的瓷砖是瓷砖
2
。
移动瓷砖后，棋盘看起来像这样
2  15   1   4
      5   9  12
  7   8  11  14
 10  13   6   3
所以，本质上发生的是我们将空瓷砖与瓷砖
2
交换了。
让我们将这个过程概括一下。当用户输入一个方向命令时，我们需要
找到空的瓷砖。
从空瓷砖开始，找到与用户输入方向相反的相邻瓷砖。
如果相邻瓷砖有效（没有超出网格），则交换空瓷砖和相邻瓷砖。
如果相邻瓷砖无效，则不执行任何操作。
通过向
Board
类添加一个成员函数
moveTile(Direction)
来实现此功能。将其添加到步骤 5 的游戏循环中。如果用户成功滑动了瓷砖，游戏应重新绘制更新后的棋盘。
显示任务
在我们的
Board
类中实现以下成员函数
一个返回布尔值的函数，指示给定的 Point 是否有效（在我们的 Board 内）。
一个找到并返回空瓷砖位置作为
Point
的函数。我们可以只跟踪空瓷砖的位置，但这会引入类不变性，并且在需要时找到空瓷砖的成本并不高。
一个根据其 Point 索引交换两个瓷砖的函数。
一个
moveTile(Direction dir)
函数，它将尝试向给定方向移动瓷砖，如果成功则返回
true
。此函数应实现上述过程。
修改步骤 5 中的
main()
函数，以便在输入方向命令时调用
moveTile()
。如果移动成功，则重新绘制棋盘。
显示答案
#include <array>
#include <cassert>
#include <iostream>
#include <limits>
#include "Random.h"

// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

class Direction
{
public:
    enum Type
    {
        up,
        down,
        left,
        right,
        maxDirections,
    };

    Direction(Type type)
        :m_type(type)
    {
    }

    Type getType() const
    {
        return m_type;
    }

    Direction operator-() const
    {
        switch (m_type)
        {
        case up:    return Direction{ down };
        case down:  return Direction{ up };
        case left:  return Direction{ right };
        case right: return Direction{ left };
        default:    break;
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ up };
    }

    static Direction getRandomDirection()
    {
        Type random{ static_cast<Type>(Random::get(0, Type::maxDirections - 1)) };
        return Direction{ random };
    }

private:
    Type m_type{};
};


std::ostream& operator<<(std::ostream& stream, Direction dir)
{
    switch (dir.getType())
    {
    case Direction::up:     return (stream << "up");
    case Direction::down:   return (stream << "down");
    case Direction::left:   return (stream << "left");
    case Direction::right:  return (stream << "right");
    default:                break;
    }

    assert(0 && "Unsupported direction was passed!");
    return (stream << "unknown direction");
}

struct Point
{
    int x{};
    int y{};

    friend bool operator==(Point p1, Point p2)
    {
        return p1.x == p2.x && p1.y == p2.y;
    }

    friend bool operator!=(Point p1, Point p2)
    {
        return !(p1 == p2);
    }

    Point getAdjacentPoint(Direction dir) const
    {
        switch (dir.getType())
        {
        case Direction::up:     return Point{ x,     y - 1 };
        case Direction::down:   return Point{ x,     y + 1 };
        case Direction::left:   return Point{ x - 1, y };
        case Direction::right:  return Point{ x + 1, y };
        default:                break;
        }

        assert(0 && "Unsupported direction was passed!");
        return *this;
    }
};

namespace UserInput
{
    bool isValidCommand(char ch)
    {
        return ch == 'w'
            || ch == 'a'
            || ch == 's'
            || ch == 'd'
            || ch == 'q';
    }

    void ignoreLine()
    {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    char getCharacter()
    {
        char operation{};
        std::cin >> operation;
        ignoreLine(); // remove any extraneous input
        return operation;
    }

    char getCommandFromUser()
    {
        char ch{};
        while (!isValidCommand(ch))
            ch = getCharacter();

        return ch;
    }

    Direction charToDirection(char ch)
    {
        switch (ch)
        {
        case 'w': return Direction{ Direction::up };
        case 's': return Direction{ Direction::down };
        case 'a': return Direction{ Direction::left };
        case 'd': return Direction{ Direction::right };
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ Direction::up };
    }
};

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }

    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

class Board
{
public:

    Board() = default;

    static void printEmptyLines(int count)
    {
        for (int i = 0; i < count; ++i)
            std::cout << '\n';
    }

    friend std::ostream& operator<<(std::ostream& stream, const Board& board)
    {
        // Before drawing always print some empty lines
        // so that only one board appears at a time
        // and it's always shown at the bottom of the window
        // because console window scrolls automatically when there is no
        // enough space. 
        for (int i = 0; i < g_consoleLines; ++i)
            std::cout << '\n';

        for (int y = 0; y < s_size; ++y)
        {
            for (int x = 0; x < s_size; ++x)
                stream << board.m_tiles[y][x];
            stream << '\n';
        }

        return stream;
    }

    Point getEmptyTilePos() const
    {
        for (int y = 0; y < s_size; ++y)
            for (int x = 0; x < s_size; ++x)
                if (m_tiles[y][x].isEmpty())
                    return { x,y };

        assert(0 && "There is no empty tile in the board!!!");
        return { -1,-1 };
    }

    static bool isValidTilePos(Point pt)
    {
        return (pt.x >= 0 && pt.x < s_size)
            && (pt.y >= 0 && pt.y < s_size);
    }

    void swapTiles(Point pt1, Point pt2)
    {
        std::swap(m_tiles[pt1.y][pt1.x], m_tiles[pt2.y][pt2.x]);
    }

    // returns true if user moved successfully
    bool moveTile(Direction dir)
    {
        Point emptyTile{ getEmptyTilePos() };
        Point adj{ emptyTile.getAdjacentPoint(-dir) };

        if (!isValidTilePos(adj))
            return false;

        swapTiles(adj, emptyTile);
        return true;
    }

private:
    static const int s_size { 4 };
    Tile m_tiles[s_size][s_size]{
        Tile{ 1 }, Tile { 2 }, Tile { 3 } , Tile { 4 },
        Tile { 5 } , Tile { 6 }, Tile { 7 }, Tile { 8 },
        Tile { 9 }, Tile { 10 }, Tile { 11 }, Tile { 12 },
        Tile { 13 }, Tile { 14 }, Tile { 15 }, Tile { 0 } };
};

int main()
{
    Board board{};
    std::cout << board;

    std::cout << "Enter a command: ";
    while (true)
    {
        char ch{ UserInput::getCommandFromUser() };

        // Handle non-direction commands
        if (ch == 'q')
        {
            std::cout << "\n\nBye!\n\n";
            return 0;
        }

        // Handle direction commands
        Direction dir{ UserInput::charToDirection(ch) };

        bool userMoved { board.moveTile(dir) };
        if (userMoved)
            std::cout << board;
    }

    return 0;
}
> 步骤 #8
目标：在此步骤中，我们将完成游戏。随机化游戏棋盘的初始状态。另外，检测用户何时获胜，之后我们可以打印胜利消息并退出游戏。
我们需要注意如何随机化我们的拼图，因为并非每个拼图都可解。例如，这个拼图无法解开
1   2   3   4 
  5   6   7   8
  9  10  11  12
 13  15  14
如果我们只是盲目地随机化拼图中的数字，则有可能生成一个不可解的拼图。对于实体版本的拼图，我们会通过随机滑动瓷砖直到瓷砖充分混合来随机化拼图。这种随机化拼图的解决方案是向与最初随机化时滑动的方向相反的方向滑动每个瓷砖。因此，以这种方式随机化拼图总是会生成一个可解的拼图。
我们可以让我们的程序以相同的方式随机化棋盘。
一旦用户解决了拼图，程序应打印
"\n\n你赢了!\n\n"
，然后正常退出。
显示任务
向
Board
类添加一个
randomize()
成员函数，它将随机化游戏棋盘中的瓷砖。选择一个随机方向，如果相邻点有效，则向该方向滑动一个瓷砖。这样做 1000 次足以打乱棋盘。
在
Board
类中实现
operator==
，它将比较两个给定棋盘的瓷砖是否相同。
向
Board
类添加
playerWon()
成员函数，如果当前游戏板已解决，则返回 true。您可以使用您实现的
operator==
来比较当前游戏板与已解决的游戏板。请记住，
Board
对象以已解决状态开始，因此如果您需要一个已解决的游戏板，只需对
Board
对象进行值初始化即可！
更新您的 main() 函数以集成 randomize() 和 playerWon()。
这是我们 15 拼图游戏的完整解决方案
显示答案
#include <array>
#include <cassert>
#include <iostream>
#include <limits>
#include "Random.h"

// Increase amount of new lines if your board isn't
// at the very bottom of the console
constexpr int g_consoleLines{ 25 };

class Direction
{
public:
    enum Type
    {
        up,
        down,
        left,
        right,
        maxDirections,
    };

    Direction(Type type)
        :m_type(type)
    {
    }
    Type getType() const
    {
        return m_type;
    }

    Direction operator-() const
    {
        switch (m_type)
        {
        case up:    return Direction{ down };
        case down:  return Direction{ up };
        case left:  return Direction{ right };
        case right: return Direction{ left };
        default:    break;
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ up };
    }

    static Direction getRandomDirection()
    {
        Type random{ static_cast<Type>(Random::get(0, Type::maxDirections - 1)) };
        return Direction{ random };
    }

private:
    Type m_type{};
};

std::ostream& operator<<(std::ostream& stream, Direction dir)
{
    switch (dir.getType())
    {
    case Direction::up:     return (stream << "up");
    case Direction::down:   return (stream << "down");
    case Direction::left:   return (stream << "left");
    case Direction::right:  return (stream << "right");
    default:                break;
    }

    assert(0 && "Unsupported direction was passed!");
    return (stream << "unknown direction");
}

struct Point
{
    int x{};
    int y{};

    friend bool operator==(Point p1, Point p2)
    {
        return p1.x == p2.x && p1.y == p2.y;
    }

    friend bool operator!=(Point p1, Point p2)
    {
        return !(p1 == p2);
    }

    Point getAdjacentPoint(Direction dir) const
    {
        switch (dir.getType())
        {
        case Direction::up:     return Point{ x,     y - 1 };
        case Direction::down:   return Point{ x,     y + 1 };
        case Direction::left:   return Point{ x - 1, y };
        case Direction::right:  return Point{ x + 1, y };
        default:                break;
        }

        assert(0 && "Unsupported direction was passed!");
        return *this;
    }
};

namespace UserInput
{
    bool isValidCommand(char ch)
    {
        return ch == 'w'
            || ch == 'a'
            || ch == 's'
            || ch == 'd'
            || ch == 'q';
    }

    void ignoreLine()
    {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    char getCharacter()
    {
        char operation{};
        std::cin >> operation;
        ignoreLine(); // remove any extraneous input
        return operation;
    }

    char getCommandFromUser()
    {
        char ch{};
        while (!isValidCommand(ch))
            ch = getCharacter();

        return ch;
    }

    Direction charToDirection(char ch)
    {
        switch (ch)
        {
        case 'w': return Direction{ Direction::up };
        case 's': return Direction{ Direction::down };
        case 'a': return Direction{ Direction::left };
        case 'd': return Direction{ Direction::right };
        }

        assert(0 && "Unsupported direction was passed!");
        return Direction{ Direction::up };
    }
};

class Tile
{
public:
    Tile() = default;
    explicit Tile(int number)
        :m_num(number)
    {
    }

    bool isEmpty() const
    {
        return m_num == 0;
    }

    int getNum() const { return m_num; }

private:
    int m_num { 0 };
};

std::ostream& operator<<(std::ostream& stream, Tile tile)
{
    if (tile.getNum() > 9) // if two digit number
        stream << " " << tile.getNum() << " ";
    else if (tile.getNum() > 0) // if one digit number
        stream << "  " << tile.getNum() << " ";
    else if (tile.getNum() == 0) // if empty spot
        stream << "    ";
    return stream;
}

class Board
{
public:

    Board() = default;

    static void printEmptyLines(int count)
    {
        for (int i = 0; i < count; ++i)
            std::cout << '\n';
    }

    friend std::ostream& operator<<(std::ostream& stream, const Board& board)
    {
        // Before drawing always print some empty lines
        // so that only one board appears at a time
        // and it's always shown at the bottom of the window
        // because console window scrolls automatically when there is no
        // enough space. 
        for (int i = 0; i < g_consoleLines; ++i)
            std::cout << '\n';

        for (int y = 0; y < s_size; ++y)
        {
            for (int x = 0; x < s_size; ++x)
                stream << board.m_tiles[y][x];
            stream << '\n';
        }

        return stream;
    }

    Point getEmptyTilePos() const
    {
        for (int y = 0; y < s_size; ++y)
            for (int x = 0; x < s_size; ++x)
                if (m_tiles[y][x].isEmpty())
                    return { x,y };

        assert(0 && "There is no empty tile in the board!!!");
        return { -1,-1 };
    }

    static bool isValidTilePos(Point pt)
    {
        return (pt.x >= 0 && pt.x < s_size)
            && (pt.y >= 0 && pt.y < s_size);
    }

    void swapTiles(Point pt1, Point pt2)
    {
        std::swap(m_tiles[pt1.y][pt1.x], m_tiles[pt2.y][pt2.x]);
    }

    // Compare two boards to see if they are equal
    friend bool operator==(const Board& f1, const Board& f2)
    {
        for (int y = 0; y < s_size; ++y)
            for (int x = 0; x < s_size; ++x)
                if (f1.m_tiles[y][x].getNum() != f2.m_tiles[y][x].getNum())
                    return false;

        return true;
    }

    // returns true if user moved successfully
    bool moveTile(Direction dir)
    {
        Point emptyTile{ getEmptyTilePos() };
        Point adj{ emptyTile.getAdjacentPoint(-dir) };

        if (!isValidTilePos(adj))
            return false;

        swapTiles(adj, emptyTile);
        return true;
    }

    bool playerWon() const
    {
        static Board s_solved{};  // generate a solved board
        return s_solved == *this; // player wins if current board == solved board
    }

    void randomize()
    {
        // Move empty tile randomly 1000 times
        // (just like you would do in real life)
        for (int i = 0; i < 1000; )
        {
            // If we are able to successfully move a tile, count this
            if (moveTile(Direction::getRandomDirection()))
                ++i;
        }
    }

private:
    static const int s_size { 4 };
    Tile m_tiles[s_size][s_size]{
        Tile{ 1 }, Tile { 2 }, Tile { 3 } , Tile { 4 },
        Tile { 5 } , Tile { 6 }, Tile { 7 }, Tile { 8 },
        Tile { 9 }, Tile { 10 }, Tile { 11 }, Tile { 12 },
        Tile { 13 }, Tile { 14 }, Tile { 15 }, Tile { 0 } };
};

int main()
{
    Board board{};
    board.randomize();
    std::cout << board;

    while (!board.playerWon())
    {
        char ch{ UserInput::getCommandFromUser() };

        // Handle non-direction commands
        if (ch == 'q')
        {
            std::cout << "\n\nBye!\n\n";
            return 0;
        }

        // Handle direction commands
        Direction dir{ UserInput::charToDirection(ch) };

        bool userMoved{ board.moveTile(dir) };
        if (userMoved)
            std::cout << board;
    }

    std::cout << "\n\nYou won!\n\n";
    return 0;
}
下一课
22.1
智能指针和移动语义简介
返回目录
上一课
21.x
第 21 章总结与测验