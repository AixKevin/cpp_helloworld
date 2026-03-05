# 17.6 — std::array 和枚举

17.6 — std::array 和枚举
Alex
2023 年 9 月 11 日下午 3:52 (PDT)
2025 年 2 月 1 日
在
16.9 课 —— 使用枚举器进行数组索引和长度
中，我们讨论了数组和枚举。
现在我们的工具包中有了
constexpr std::array
，我们将继续讨论并展示一些额外的技巧。
使用静态断言确保数组初始化器数量正确
使用 CTAD 初始化
constexpr std::array
时，编译器会根据初始化器的数量推断数组的长度。如果提供的初始化器少于应有的数量，数组将比预期短，并且对其进行索引可能会导致未定义行为。
例如
#include <array>
#include <iostream>

enum StudentNames
{
    kenny, // 0
    kyle, // 1
    stan, // 2
    butters, // 3
    cartman, // 4
    max_students // 5
};

int main()
{
    constexpr std::array testScores { 78, 94, 66, 77 }; // oops, only 4 values

    std::cout << "Cartman got a score of " << testScores[StudentNames::cartman] << '\n'; // undefined behavior due to invalid index

    return 0;
}
无论何时，只要
constexpr std::array
中的初始化器数量可以合理地进行健全性检查，您都可以使用静态断言进行检查
#include <array>
#include <iostream>

enum StudentNames
{
    kenny, // 0
    kyle, // 1
    stan, // 2
    butters, // 3
    cartman, // 4
    max_students // 5
};

int main()
{
    constexpr std::array testScores { 78, 94, 66, 77 };

    // Ensure the number of test scores is the same as the number of students
    static_assert(std::size(testScores) == max_students); // compile error: static_assert condition failed

    std::cout << "Cartman got a score of " << testScores[StudentNames::cartman] << '\n';

    return 0;
}
这样，如果您稍后添加了一个新的枚举器，但忘记为
testScores
添加相应的初始化器，程序将无法编译。
您还可以使用静态断言来确保两个不同的
constexpr std::array
具有相同的长度。
使用 constexpr 数组改进枚举输入和输出
在
13.5 课 —— I/O 运算符重载简介
中，我们介绍了几种输入和输出枚举器名称的方法。为了协助完成此任务，我们有辅助函数将枚举器转换为字符串，反之亦然。这些函数各有自己的（重复的）字符串字面量集，我们必须专门编写逻辑来检查每个
constexpr std::string_view getPetName(Pet pet)
{
    switch (pet)
    {
    case cat:   return "cat";
    case dog:   return "dog";
    case pig:   return "pig";
    case whale: return "whale";
    default:    return "???";
    }
}

constexpr std::optional<Pet> getPetFromString(std::string_view sv)
{
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;

    return {};
}
这意味着如果我们要添加一个新的枚举器，我们必须记住更新这些函数。
让我们稍微改进一下这些函数。在枚举器的值从 0 开始并按顺序递增的情况下（大多数枚举都是如此），我们可以使用一个数组来保存每个枚举器的名称。
这使我们能够做两件事
使用枚举器的值索引数组以获取该枚举器的名称。
使用循环遍历所有名称，并能够根据索引将名称与枚举器关联起来。
#include <array>
#include <iostream>
#include <string>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // use sv suffix so std::array will infer type as std::string_view
    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // Make sure we've defined strings for all our colors
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    // We can index the array using the enumerator to get the name of the enumerator
    return Color::colorName[static_cast<std::size_t>(color)];
}

// Teach operator<< how to print a Color
// std::ostream is the type of std::cout
// The return type and parameter type are references (to prevent copies from being made)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

// Teach operator>> how to input a Color by name
// We pass color by non-const reference so we can have the function modify its value
std::istream& operator>> (std::istream& in, Color::Type& color)
{
    std::string input {};
    std::getline(in >> std::ws, input);

    // Iterate through the list of names to see if we can find a matching name
    for (std::size_t index=0; index < Color::colorName.size(); ++index)
    {
        if (input == Color::colorName[index])
        {
            // If we found a matching name, we can get the enumerator value based on its index
            color = static_cast<Color::Type>(index);
            return in;
        }
    }

    // We didn't find a match, so input must have been invalid
    // so we will set input stream to fail state
    in.setstate(std::ios_base::failbit);

    // On an extraction failure, operator>> zero-initializes fundamental types
    // Uncomment the following line to make this operator do the same thing
    // color = {};
    return in;
}

int main()
{
    auto shirt{ Color::blue };
    std::cout << "Your shirt is " << shirt << '\n';

    std::cout << "Enter a new color: ";
    std::cin >> shirt;
    if (!std::cin)
        std::cout << "Invalid\n";
    else
        std::cout << "Your shirt is now " << shirt << '\n';

    return 0;
}
这会打印
Your shirt is blue
Enter a new color: red
Your shirt is now red
基于范围的 for 循环和枚举
有时我们会遇到需要遍历枚举的枚举器的情况。虽然我们可以使用带有整数索引的 for 循环来实现这一点，但这可能需要大量将整数索引静态转换为我们的枚举类型。
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // use sv suffix so std::array will infer type as std::string_view
    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // Make sure we've defined strings for all our colors
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

// Teach operator<< how to print a Color
// std::ostream is the type of std::cout
// The return type and parameter type are references (to prevent copies from being made)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    // Use a for loop to iterate through all our colors
    for (int i=0; i < Color::max_colors; ++i )
        std::cout << static_cast<Color::Type>(i) << '\n';

    return 0;
}
不幸的是，基于范围的 for 循环不允许您遍历枚举的枚举器
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // use sv suffix so std::array will infer type as std::string_view
    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // Make sure we've defined strings for all our colors
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

// Teach operator<< how to print a Color
// std::ostream is the type of std::cout
// The return type and parameter type are references (to prevent copies from being made)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    for (auto c: Color::Type) // compile error: can't traverse enumeration
        std::cout << c < '\n';

    return 0;
}
对此有许多创造性的解决方案。由于我们可以在数组上使用基于范围的 for 循环，最直接的解决方案之一是创建一个包含每个枚举器的
constexpr std::array
，然后遍历它。此方法仅在枚举器具有唯一值时有效。
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,     // 0
        red,       // 1
        blue,      // 2
        max_colors // 3
    };

    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };
    static_assert(std::size(colorName) == max_colors);

    constexpr std::array types { black, red, blue }; // A std::array containing all our enumerators
    static_assert(std::size(types) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

// Teach operator<< how to print a Color
// std::ostream is the type of std::cout
// The return type and parameter type are references (to prevent copies from being made)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    for (auto c: Color::types) // ok: we can do a range-based for on a std::array
        std::cout << c << '\n';

    return 0;
}
在上面的示例中，由于
Color::types
的元素类型是
Color::Type
，变量
c
将被推导为
Color::Type
，这正是我们想要的！
这会打印
black
red
blue
小测验时间
定义一个名为
Animal
的命名空间。在其中，定义一个枚举，包含以下动物：鸡、狗、猫、大象、鸭子和蛇。还要创建一个名为
Data
的结构体，用于存储每种动物的名称、腿的数量以及它发出的声音。创建一个
std::array
的 Data，并为每种动物填充一个 Data 元素。
要求用户输入动物的名称。如果名称与我们的动物之一不匹配，请告知他们。否则，打印该动物的数据。然后打印所有不匹配用户输入的其他动物的数据。
例如
Enter an animal: dog
A dog has 4 legs and says woof.

Here is the data for the rest of the animals:
A chicken has 2 legs and says cluck.
A cat has 4 legs and says meow.
A elephant has 4 legs and says pawoo.
A duck has 2 legs and says quack.
A snake has 0 legs and says hissss.
Enter an animal: frog
That animal couldn't be found.

Here is the data for the rest of the animals:
A chicken has 2 legs and says cluck.
A dog has 4 legs and says woof.
A cat has 4 legs and says meow.
A elephant has 4 legs and says pawoo.
A duck has 2 legs and says quack.
A snake has 0 legs and says hissss.
问题 #1
显示答案
#include <array>
#include <iostream>
#include <string>
#include <string_view>

namespace Animal
{
    enum Type
    {
        chicken,
        dog,
        cat,
        elephant,
        duck,
        snake,
        max_animals
    };

    struct Data
    {
        std::string_view name{};
        int legs{};
        std::string_view sound{};
    };

    constexpr std::array types { chicken, dog, cat, elephant, duck, snake };
    constexpr std::array data {
        Data{ "chicken",    2, "cluck" },
        Data{ "dog",        4, "woof" },
        Data{ "cat",        4, "meow" },
        Data{ "elephant",   4, "pawoo" },
        Data{ "duck",       2, "quack" },
        Data{ "snake",      0, "hissss" },
    };

    static_assert(std::size(types) == max_animals);
    static_assert(std::size(data) == max_animals);
}

// Teach operator>> how to input an Animal by name
// We pass animal by non-const reference so we can have the function modify its value
std::istream& operator>> (std::istream& in, Animal::Type& animal)
{
    std::string input {};
    std::getline(in >> std::ws, input);

    // See if we can find a match
    for (std::size_t index=0; index < Animal::data.size(); ++index)
    {
        if (input == Animal::data[index].name)
        {
            animal = static_cast<Animal::Type>(index);
            return in;
        }
    }

    // We didn't find a match, so input must have been invalid
    // so we will set input stream to fail state
    in.setstate(std::ios_base::failbit);
    return in;
}

void printAnimalData(Animal::Type type)
{
    const Animal::Data& animal { Animal::data[type] };
    std::cout << "A " << animal.name << " has " << animal.legs << " legs and says " << animal.sound << ".\n";    
}

int main()
{
    std::cout << "Enter an animal: ";
    Animal::Type type{};
    std::cin >> type;

    // If users input didn't match
    if (!std::cin)
    {
        std::cin.clear();
        std::cout << "That animal couldn't be found.\n";
        type = Animal::max_animals; // set to invalid option so we don't match below
    }
    else
        printAnimalData(type);


    std::cout << "\nHere is the data for the rest of the animals:\n";
    for (auto a : Animal::types)
    {
        if (a != type)
            printAnimalData(a);
    }

    return 0;
}
下一课
17.7
C 风格数组简介
返回目录
上一课
17.5
通过 std::reference_wrapper 使用引用数组