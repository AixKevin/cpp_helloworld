# 14.1 — 面向对象编程简介

14.1 — 面向对象编程简介
Alex
2007 年 8 月 23 日，太平洋夏令时上午 10:54
2023 年 9 月 15 日
过程式编程
回到第
1.3 课 -- 对象和变量简介
，我们将在 C++ 中定义一个对象为“一块可用于存储值的内存”。一个有名称的对象被称为变量。我们的 C++ 程序由指令的顺序列表组成，这些指令定义数据（通过对象）以及对数据执行的操作（通过包含语句和表达式的函数）。
到目前为止，我们一直在做一种称为过程式编程的编程类型。在**过程式编程**中，重点是创建“过程”（在 C++ 中称为函数），以实现我们的程序逻辑。我们将数据对象传递给这些函数，这些函数对数据执行操作，然后可能返回一个结果供调用者使用。
在过程式编程中，函数和这些函数操作的数据是独立的实体。程序员负责将函数和数据组合在一起以产生所需的结果。这导致代码看起来像这样
eat(you, apple);
现在，环顾四周——你所看到的都是对象：书本、建筑物、食物，甚至是你自己。这些对象有两个主要组成部分：1) 若干相关属性（例如重量、颜色、大小、固体性、形状等），以及 2) 若干可以展示的行为（例如被打开、使其他东西变热等）。这些属性和行为是密不可分的。
在编程中，属性由对象表示，行为由函数表示。因此，过程式编程对现实的表示相当糟糕，因为它将属性（对象）和行为（函数）分开了。
什么是面向对象编程？
在**面向对象编程**（通常缩写为 OOP）中，重点是创建程序定义的数据类型，这些类型包含属性和一组定义明确的行为。OOP 中的“对象”一词指的是我们可以从这些类型实例化的对象。
这导致代码看起来更像这样
you.eat(apple);
这使得主语（`you`）、正在调用的行为（`eat()`）以及该行为的辅助对象（`apple`）更加清晰。
由于属性和行为不再分离，对象更易于模块化，这使得我们的程序更易于编写和理解，并提供了更高程度的代码可重用性。这些对象还提供了一种更直观的方式来处理我们的数据，通过允许我们定义如何与对象交互以及它们如何与其他对象交互。
我们将在下一课中讨论如何创建此类对象。
一个过程式 vs. 类 OOP 的例子
这是一个用过程式编程风格编写的简短程序，它打印动物的名称和腿的数量
#include <iostream>
#include <string_view>

enum AnimalType
{
    cat,
    dog,
    chicken,
};

constexpr std::string_view animalName(AnimalType type)
{
    switch (type)
    {
    case cat: return "cat";
    case dog: return "dog";
    case chicken: return "chicken";
    default:  return "";
    }
}

constexpr int numLegs(AnimalType type)
{
    switch (type)
    {
    case cat: return 4;
    case dog: return 4;
    case chicken: return 2;
    default:  return 0;
    }
}


int main()
{
    constexpr AnimalType animal{ cat };
    std::cout << "A " << animalName(animal) << " has " << numLegs(animal) << " legs\n";

    return 0;
}
在这个程序中，我们编写了函数，允许我们获取动物的腿的数量和动物的名称。
虽然这完全可以正常工作，但考虑一下当我们想要更新此程序，使我们的动物现在成为一条 `snake` 时会发生什么。要将蛇添加到我们的代码中，我们需要修改 `AnimalType`、`numLegs()` 和 `animalName()`。如果这是一个更大的代码库，我们还需要更新任何其他使用 `AnimalType` 的函数——如果 `AnimalType` 在很多地方使用，那可能需要修改很多代码（并且可能导致错误）。
现在让我们用更面向对象的方式来编写相同的程序（产生相同的输出）
#include <iostream>
#include <string_view>

struct Cat
{
    std::string_view name{ "cat" };
    int numLegs{ 4 };
};

struct Dog
{
    std::string_view name{ "dog" };
    int numLegs{ 4 };
};

struct Chicken
{
    std::string_view name{ "chicken" };
    int numLegs{ 2 };
};

int main()
{
    constexpr Cat animal;
    std::cout << "a " << animal.name << " has " << animal.numLegs << " legs\n";

    return 0;
}
在这个例子中，每种动物都是它自己的程序定义类型，该类型管理与该动物相关的一切（在本例中，只是跟踪名称和腿的数量）。
现在考虑我们想把动物更新为蛇的情况。我们所要做的就是创建一个 `Snake` 类型并使用它来代替 `Cat`。几乎不需要改变现有的代码，这意味着损坏现有功能的风险大大降低。
如上所述，我们的 `Cat`、`Dog` 和 `Chicken` 示例有很多重复（因为每个都定义了完全相同的成员集）。在这种情况下，创建一个通用的 `Animal` 结构并为每种动物创建一个实例可能更可取。但是如果我们想为 `Chicken` 添加一个不适用于其他动物的新成员（例如 `wormsPerDay`）怎么办？使用一个通用的 `Animal` 结构，所有动物都会得到那个成员。而使用我们的 OOP 模型，我们可以将该成员限制为 `Chicken` 对象。
OOP 还带来其他好处
在学校里，当你提交编程作业时，你的工作基本就完成了。你的教授或助教将运行你的代码，看看它是否产生正确的结果。它要么正确，要么不正确，你也会据此获得相应的分数。你的代码很可能在那时就被丢弃了。
另一方面，当你将代码提交到其他开发人员使用的仓库，或者提交到真实用户使用的应用程序时，情况就完全不同了。新的操作系统或软件版本可能会破坏你的代码。用户会发现你犯的一些逻辑错误。商业伙伴会要求增加新的功能。其他开发人员需要扩展你的代码而不会破坏它。你的代码需要能够进化，可能还会大幅进化，而且需要以最少的时间投入、最少的麻烦和最少的破坏来完成。
解决这些问题的最佳方法是尽可能地保持代码模块化（并且没有冗余）。为了实现这一点，OOP 还引入了许多其他有用的概念：继承、封装、抽象和多态。
作者注
语言设计者有一个哲学：当一个大词能表达意思时，绝不使用一个小词。
还有，为什么“缩写”这个词这么长？
我们将在适当的时候介绍所有这些内容，以及它们如何帮助您的代码减少冗余，并使其更易于修改和扩展。一旦您正确熟悉并掌握了 OOP，您可能再也不想回到纯过程式编程了。
话虽如此，OOP 并没有取代过程式编程——相反，它为您提供了编程工具箱中额外的工具，以便在需要时管理复杂性。
“对象”一词
请注意，“对象”一词有点重载，这导致了一些混淆。在传统编程中，对象是存储值的内存片段。仅此而已。在面向对象编程中，“对象”意味着它既是传统编程意义上的对象，又结合了属性和行为。在本教程中，我们将倾向于使用“对象”一词的传统含义，并在特指 OOP 对象时优先使用“类对象”一词。
小测验时间
问题 #1
更新上面动物过程式示例，实例化一条蛇而不是猫。
显示答案
#include <iostream>
#include <string_view>

enum AnimalType
{
    cat,
    dog,
    chicken,
    snake,
};

constexpr std::string_view animalName(AnimalType type)
{
    switch (type)
    {
    case cat: return "cat";
    case dog: return "dog";
    case chicken: return "chicken";
    case snake: return "snake";
    default:  return "";
    }
}

constexpr int numLegs(AnimalType type)
{
    switch (type)
    {
    case cat: return 4;
    case dog: return 4;
    case chicken: return 2;
    case snake: return 0;

    default:  return 0;
    }
}


int main()
{
    constexpr AnimalType animal{ snake };
    std::cout << "A " << animalName(animal) << " has " << numLegs(animal) << " legs\n";

    return 0;
}
问题 #2
更新上面动物 OOP 风格示例，实例化一条蛇而不是猫。
显示答案
#include <iostream>
#include <string_view>

struct Cat
{
    std::string_view name{ "cat" };
    int numLegs{ 4 };
};

struct Dog
{
    std::string_view name{ "dog" };
    int numLegs{ 4 };
};

struct Chicken
{
    std::string_view name{ "chicken" };
    int numLegs{ 2 };
};

struct Snake
{
    std::string_view name{ "snake" };
    int numLegs{ 0 };
};

int main()
{
    constexpr Snake animal;
    std::cout << "a " << animal.name << " has " << animal.numLegs << " legs\n";

    return 0;
}
下一课
14.2
类简介
返回目录
上一课
13.y
使用语言参考