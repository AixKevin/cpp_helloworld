# 13.2 — 无作用域枚举

13.2 — 无作用域枚举
Alex
2007 年 6 月 19 日，下午 8:24 PDT
2024 年 10 月 28 日
C++ 包含许多有用的基本数据类型和复合数据类型（我们在
4.1 -- 基本数据类型简介
和
12.1 -- 复合数据类型简介
课程中介绍过）。但这些类型并不总是足以满足我们想要做的各种事情。
例如，假设您正在编写一个程序，需要跟踪苹果是红色、黄色还是绿色，或者衬衫的颜色（从预设的颜色列表中选择）。如果只有基本类型可用，您将如何做到这一点？
您可以将颜色存储为整数值，使用某种隐式映射（0 = 红色，1 = 绿色，2 = 蓝色）
int main()
{
    int appleColor{ 0 }; // my apple is red
    int shirtColor{ 1 }; // my shirt is green

    return 0;
}
但这根本不直观，我们已经讨论过为什么魔术数字不好（
5.2 -- 字面量
）。我们可以通过使用符号常量来摆脱魔术数字
constexpr int red{ 0 };
constexpr int green{ 1 };
constexpr int blue{ 2 };

int main()
{
    int appleColor{ red };
    int shirtColor{ green };

    return 0;
}
虽然这在阅读上有所改进，但程序员仍然需要推断出 `appleColor` 和 `shirtColor`（它们是 `int` 类型）是为了保存颜色符号常量集合中定义的值（这些常量可能在其他地方定义，很可能在单独的文件中）。
我们可以通过使用类型别名使这个程序更清晰一些
using Color = int; // define a type alias named Color

// The following color values should be used for a Color
constexpr Color red{ 0 };
constexpr Color green{ 1 };
constexpr Color blue{ 2 };

int main()
{
    Color appleColor{ red };
    Color shirtColor{ green };

    return 0;
}
我们越来越接近了。阅读此代码的人仍然需要理解这些颜色符号常量旨在与 `Color` 类型的变量一起使用，但至少现在该类型有一个唯一的名称，因此搜索 `Color` 的人能够找到相关联的符号常量集。
然而，因为 `Color` 只是 `int` 的别名，我们仍然存在一个问题，即没有任何东西强制正确使用这些颜色符号常量。我们仍然可以这样做
Color eyeColor{ 8 }; // syntactically valid, semantically meaningless
此外，如果我们在调试器中调试这些变量，我们将只看到颜色的整数值（例如 `0`），而不是符号意义（`red`），这可能会使判断程序是否正确变得更加困难。
幸运的是，我们可以做得更好。
作为启发，考虑 `bool` 类型。`bool` 尤其有趣之处在于它只有两个定义的值：`true` 和 `false`。我们可以直接使用 `true` 或 `false`（作为字面量），或者我们可以实例化一个 `bool` 对象并让它保存这两个值中的任何一个。此外，编译器能够将 `bool` 与其他类型区分开来。这意味着我们可以重载函数，并自定义这些函数在传递 `bool` 值时的行为。
如果我们能够定义自己的自定义类型，其中*我们*可以定义与该类型关联的命名值集，那么我们将拥有优雅地解决上述挑战的完美工具……
枚举
**枚举**（也称为**枚举类型**或**enum**）是一种复合数据类型，其值被限制为一组命名的符号常量（称为**枚举器**）。
C++ 支持两种枚举：无作用域枚举（我们现在将介绍）和有作用域枚举（我们将在本章稍后介绍）。
由于枚举是程序定义的类型（
13.1 -- 程序定义（用户定义）类型简介
），因此在使用它之前需要完全定义每个枚举（前向声明不足）。
无作用域枚举
无作用域枚举通过 `enum` 关键字定义。
枚举类型最好通过示例来教授，所以让我们定义一个可以保存一些颜色值的无作用域枚举。我们将在下面解释它如何工作。
// Define a new unscoped enumeration named Color
enum Color
{
    // Here are the enumerators
    // These symbolic constants define all the possible values this type can hold
    // Each enumerator is separated by a comma, not a semicolon
    red,
    green,
    blue, // trailing comma optional but recommended
}; // the enum definition must end with a semicolon

int main()
{
    // Define a few variables of enumerated type Color
    Color apple { red };   // my apple is red
    Color shirt { green }; // my shirt is green
    Color cup { blue };    // my cup is blue

    Color socks { white }; // error: white is not an enumerator of Color
    Color hat { 2 };       // error: 2 is not an enumerator of Color

    return 0;
}
我们首先使用 `enum` 关键字告诉编译器我们正在定义一个名为 `Color` 的无作用域枚举。
在一对花括号内，我们定义 `Color` 类型的枚举器：`red`、`green` 和 `blue`。这些枚举器定义了 `Color` 类型被限制的特定值。每个枚举器必须用逗号分隔（而不是分号）——最后一个枚举器后面的逗号是可选的，但为了保持一致性建议使用。
最常见的是每行定义一个枚举器，但在简单情况下（枚举器数量少且不需要注释），它们可以全部定义在同一行。
`Color` 的类型定义以分号结束。我们现在已经完全定义了枚举类型 `Color` 是什么！
在 `main()` 中，我们实例化了三个 `Color` 类型的变量：`apple` 用颜色 `red` 初始化，`shirt` 用颜色 `green` 初始化，`cup` 用颜色 `blue` 初始化。为每个对象分配内存。请注意，枚举类型的初始化器必须是该类型定义的枚举器之一。变量 `socks` 和 `hat` 导致编译错误，因为初始化器 `white` 和 `2` 不是 `Color` 的枚举器。
枚举器是隐式 constexpr。
提醒
快速回顾一下术语
**枚举**或**枚举类型**是程序定义类型本身（例如 `Color`）。
**枚举器**是属于枚举的特定命名值（例如 `red`）。
命名枚举和枚举器
按照惯例，枚举类型的名称以大写字母开头（所有程序定义类型都是如此）。
警告
枚举不一定要命名，但在现代 C++ 中应避免使用未命名枚举。
枚举器必须命名。不幸的是，没有常见的枚举器命名约定。常见的选择包括小写字母开头（例如 red）、大写字母开头（Red）、全大写（RED）、带前缀的全大写（COLOR_RED），或带“k”前缀并驼峰命名（kColorRed）。
现代 C++ 指南通常建议避免使用全大写命名约定，因为全大写通常用于预处理器宏，并且可能发生冲突。我们还建议避免使用以大写字母开头的约定，因为以大写字母开头的名称通常保留给程序定义类型。
最佳实践
将枚举类型命名为以大写字母开头。将枚举器命名为以小写字母开头。
枚举类型是不同的类型
您创建的每个枚举类型都被视为**不同的类型**，这意味着编译器可以将其与其他类型区分开来（与 typedef 或类型别名不同，它们被视为与其别名类型不相同）。
由于枚举类型是不同的，因此在一个枚举类型中定义的枚举器不能与另一个枚举类型的对象一起使用
enum Pet
{
    cat,
    dog,
    pig,
    whale,
};

enum Color
{
    black,
    red,
    blue,
};

int main()
{
    Pet myPet { black }; // compile error: black is not an enumerator of Pet
    Color shirt { pig }; // compile error: pig is not an enumerator of Color

    return 0;
}
你可能无论如何都不想要一件猪衬衫。
使用枚举
由于枚举器具有描述性，它们有助于增强代码文档和可读性。枚举类型最适用于当您有一小组相关的常量，并且对象一次只需要保存其中一个值时。
常用的枚举包括星期几、基点方向和一副扑克牌中的花色
enum DaysOfWeek
{
    sunday,
    monday,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday,
};

enum CardinalDirections
{
    north,
    east,
    south,
    west,
};

enum CardSuits
{
    clubs,
    diamonds,
    hearts,
    spades,
};
有时函数会向调用者返回一个状态码，以指示函数是否成功执行或遇到错误。传统上，小的负数用于表示不同的可能错误代码。例如
int readFileContents()
{
    if (!openFile())
        return -1;
    if (!readFile())
        return -2;
    if (!parseFile())
        return -3;

    return 0; // success
}
然而，像这样使用魔术数字并不具有描述性。更好的方法是使用枚举类型
enum FileReadResult
{
    readResultSuccess,
    readResultErrorFileOpen,
    readResultErrorFileRead,
    readResultErrorFileParse,
};

FileReadResult readFileContents()
{
    if (!openFile())
        return readResultErrorFileOpen;
    if (!readFile())
        return readResultErrorFileRead;
    if (!parseFile())
        return readResultErrorFileParse;

    return readResultSuccess;
}
然后调用者可以将函数的返回值与适当的枚举器进行测试，这比测试返回结果是否为特定整数值更容易理解。
if (readFileContents() == readResultSuccess)
{
    // do something
}
else
{
    // print error message
}
枚举类型在游戏中也可以很好地利用，用于识别不同类型的物品、怪物或地形。基本上，任何一小组相关对象都可以。
例如
enum ItemType
{
	sword,
	torch,
	potion,
};

int main()
{
	ItemType holding{ torch };

	return 0;
}
当用户需要在两个或多个选项之间进行选择时，枚举类型也可以作为有用的函数参数
enum SortOrder
{
    alphabetical,
    alphabeticalReverse,
    numerical,
};

void sortData(SortOrder order)
{
    switch (order)
    {
        case alphabetical:
            // sort data in forwards alphabetical order
            break;
        case alphabeticalReverse:
            // sort data in backwards alphabetical order
            break;
        case numerical:
            // sort data numerically
            break;
    }
}
许多语言使用枚举来定义布尔值——毕竟，布尔值本质上只是一个包含两个枚举器 `false` 和 `true` 的枚举！然而，在 C++ 中，`true` 和 `false` 被定义为关键字而不是枚举器。
由于枚举很小且复制成本低，因此按值传递（和返回）它们是没问题的。
在课程
O.1 -- 位标志和通过 std::bitset 进行位操作
中，我们讨论了位标志。枚举也可以用来定义一组相关的位标志位置，以便与 `std::bitset` 一起使用
#include <bitset>
#include <iostream>

namespace Flags
{
    enum State
    {
        isHungry,
        isSad,
        isMad,
        isHappy,
        isLaughing,
        isAsleep,
        isDead,
        isCrying,
    };
}

int main()
{
    std::bitset<8> me{};
    me.set(Flags::isHappy);
    me.set(Flags::isLaughing);

    std::cout << std::boolalpha; // print bool as true/false

    // Query a few states (we use the any() function to see if any bits remain set)
    std::cout << "I am happy? " << me.test(Flags::isHappy) << '\n';
    std::cout << "I am laughing? " << me.test(Flags::isLaughing) << '\n';

    return 0;
}
如果你想知道我们如何在预期整数值的地方使用枚举器，无作用域枚举器会隐式转换为整数值。我们将在下一课（
13.3 -- 无作用域枚举器整数转换
）中进一步探讨这一点。
无作用域枚举的作用域
无作用域枚举之所以这样命名，是因为它们将其枚举器名称放入与枚举定义本身相同的范围（而不是像命名空间那样创建新的范围区域）。
例如，给定这个程序
enum Color // this enum is defined in the global namespace
{
    red, // so red is put into the global namespace
    green,
    blue, 
};

int main()
{
    Color apple { red }; // my apple is red

    return 0;
}
`Color` 枚举在全局作用域中定义。因此，所有枚举名称（`red`、`green` 和 `blue`）也进入全局作用域。这会污染全局作用域并显著增加命名冲突的可能性。
这带来的一个后果是，在同一作用域内的多个枚举中不能使用相同的枚举器名称
enum Color
{
    red,
    green,
    blue, // blue is put into the global namespace
};

enum Feeling
{
    happy,
    tired,
    blue, // error: naming collision with the above blue
};

int main()
{
    Color apple { red }; // my apple is red
    Feeling me { happy }; // I'm happy right now (even though my program doesn't compile)

    return 0;
}
在上面的示例中，两个无作用域枚举（`Color` 和 `Feeling`）都将名称 `blue` 的枚举器放入全局作用域。这导致命名冲突和随后的编译错误。
无作用域枚举也为其枚举器提供了一个命名作用域区域（就像命名空间充当其内部声明的名称的命名作用域区域一样）。这意味着我们可以按如下方式访问无作用域枚举的枚举器
enum Color
{
    red,
    green,
    blue, // blue is put into the global namespace
};

int main()
{
    Color apple { red }; // okay, accessing enumerator from global namespace
    Color raspberry { Color::red }; // also okay, accessing enumerator from scope of Color

    return 0;
}
通常情况下，无作用域枚举器在访问时不需要使用作用域解析运算符。
避免枚举器命名冲突
有几种常见的避免无作用域枚举器命名冲突的方法。
一种选择是在每个枚举器前加上枚举本身的名称
enum Color
{
    color_red,
    color_blue,
    color_green,
};

enum Feeling
{
    feeling_happy,
    feeling_tired,
    feeling_blue, // no longer has a naming collision with color_blue
};

int main()
{
    Color paint { color_blue };
    Feeling me { feeling_blue };

    return 0;
}
这仍然会污染命名空间，但通过使名称更长、更独特来降低命名冲突的可能性。
一个更好的选择是将枚举类型放在提供单独作用域区域的内部，例如命名空间
namespace Color
{
    // The names Color, red, blue, and green are defined inside namespace Color
    enum Color
    {
        red,
        green,
        blue,
    };
}

namespace Feeling
{
    enum Feeling
    {
        happy,
        tired,
        blue, // Feeling::blue doesn't collide with Color::blue
    };
}

int main()
{
    Color::Color paint{ Color::blue };
    Feeling::Feeling me{ Feeling::blue };

    return 0;
}
这意味着我们现在必须在我们的枚举和枚举器名称前加上作用域区域的名称。
致进阶读者
类也提供作用域区域，通常将与类相关的枚举类型放在类的作用域区域内。我们将在
15.3 -- 嵌套类型（成员类型）
课程中讨论这一点。
一个相关的选项是使用有作用域枚举（它定义自己的作用域区域）。我们将在稍后讨论有作用域枚举（
13.6 -- 有作用域枚举（枚举类）
）。
最佳实践
优先将您的枚举放在命名作用域区域（例如命名空间或类）内，这样枚举器就不会污染全局命名空间。
或者，如果枚举仅在单个函数体内使用，则应在函数内部定义枚举。这会将枚举及其枚举器的作用域限制在该函数内。此类枚举的枚举器将遮蔽全局作用域中定义的同名枚举器。
与枚举器比较
我们可以使用相等运算符（`operator==` 和 `operator!=`）来测试枚举是否具有特定枚举器的值。
#include <iostream>

enum Color
{
    red,
    green,
    blue,
};

int main()
{
    Color shirt{ blue };

    if (shirt == blue) // if the shirt is blue
        std::cout << "Your shirt is blue!";
    else
        std::cout << "Your shirt is not blue!";

    return 0;
}
在上面的示例中，我们使用 if 语句来测试 `shirt` 是否等于枚举器 `blue`。这为我们提供了一种根据枚举持有的枚举器来条件化程序行为的方法。
我们将在下一课中更多地利用这一点。
小测验时间
问题 #1
定义一个名为 `MonsterType` 的无作用域枚举类型，用于选择以下怪物种族：orc、goblin、troll、ogre 和 skeleton。
显示答案
enum MonsterType
{
    orc,
    goblin,
    troll,
    ogre,
    skeleton,
};
问题 #2
将 `MonsterType` 枚举放在一个命名空间中。然后，创建一个 `main()` 函数并实例化一个 `troll`。程序应该编译。
显示答案
namespace Monster
{
    enum MonsterType
    {
        orc,
        goblin,
        troll,
        ogre,
        skeleton,
    };
}

int main()
{
    // We use [[maybe_unused]] to avoid warnings about unused variables
    // You could also output the monster instead
    [[maybe_unused]] Monster::MonsterType monster{ Monster::troll };

    return 0;
}
由于 `MonsterType` 是一个无作用域枚举，它的枚举器（例如 `troll`）被放置在枚举本身的命名空间中（在本例中是 `namespace Monster`）。因此，我们可以将 `troll` 作为 `Monster::troll` 访问。
由于无作用域枚举也将其枚举器放入自己的命名空间中，因此 `troll` 也可以作为 `Monster::MonsterType::troll` 访问。然而，这样做并没有实际好处。
下一课
13.3
无作用域枚举器整数转换
返回目录
上一课
13.1
程序定义（用户定义）类型简介