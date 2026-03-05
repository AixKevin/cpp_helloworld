# 13.6 — 作用域枚举 (enum class)

13.6 — 作用域枚举 (enum class)
Alex
2015年4月23日，下午4:22 PDT
2025年2月11日
虽然无作用域枚举在 C++ 中是不同的类型，但它们不是类型安全的，在某些情况下会允许你做一些没有意义的事情。考虑以下情况：
#include <iostream>

int main()
{
    enum Color
    {
        red,
        blue,
    };

    enum Fruit
    {
        banana,
        apple,
    };
	
    Color color { red };
    Fruit fruit { banana };

    if (color == fruit) // The compiler will compare color and fruit as integers
        std::cout << "color and fruit are equal\n"; // and find they are equal!
    else
        std::cout << "color and fruit are not equal\n";

    return 0;
}
这会打印
color and fruit are equal
当
color
和
fruit
进行比较时，编译器会查看它是否知道如何比较
Color
和
Fruit
。它不知道。接下来，它会尝试将
Color
和/或
Fruit
转换为整数，以查看是否能找到匹配项。最终编译器会确定，如果将两者都转换为整数，就可以进行比较。由于
color
和
fruit
都设置为转换为整数值
0
的枚举器，因此
color
将等于
fruit
。
这在语义上没有意义，因为
color
和
fruit
来自不同的枚举，并且不打算进行比较。对于标准枚举器，没有简单的方法可以防止这种情况。
由于这些挑战以及命名空间污染问题（在全局作用域中定义的无作用域枚举将其枚举器放入全局命名空间），C++ 设计者认为，更清晰的枚举解决方案将会有用。
作用域枚举
该解决方案是
作用域枚举
（在 C++ 中常被称为
enum class
，原因很快就会明了）。
作用域枚举的工作方式类似于无作用域枚举（
13.2 -- 无作用域枚举
），但有两个主要区别：它们不会隐式转换为整数，并且枚举器
只
放在枚举的作用域区域内（而不是放在定义枚举的作用域区域内）。
要创建作用域枚举，我们使用关键字
enum class
。作用域枚举定义的其余部分与无作用域枚举定义相同。这是一个例子：
#include <iostream>
int main()
{
    enum class Color // "enum class" defines this as a scoped enumeration rather than an unscoped enumeration
    {
        red, // red is considered part of Color's scope region
        blue,
    };

    enum class Fruit
    {
        banana, // banana is considered part of Fruit's scope region
        apple,
    };

    Color color { Color::red }; // note: red is not directly accessible, we have to use Color::red
    Fruit fruit { Fruit::banana }; // note: banana is not directly accessible, we have to use Fruit::banana
	
    if (color == fruit) // compile error: the compiler doesn't know how to compare different types Color and Fruit
        std::cout << "color and fruit are equal\n";
    else
        std::cout << "color and fruit are not equal\n";

    return 0;
}
此程序在第19行产生编译错误，因为作用域枚举不会转换为可以与另一种类型进行比较的任何类型。
题外话…
class
关键字（以及
static
关键字）是 C++ 语言中最重载的关键字之一，根据上下文可以有不同的含义。尽管作用域枚举使用
class
关键字，但它们不被认为是“类类型”（“类类型”保留给结构体、类和联合体）。
enum struct
在这种情况下也有效，并且与
enum class
行为相同。但是，使用
enum struct
是非惯用的，因此请避免使用它。
作用域枚举定义自己的作用域区域
与无作用域枚举不同，无作用域枚举将其枚举器放在与枚举本身相同的范围中，而作用域枚举将其枚举器
只
放在枚举的作用域区域中。换句话说，作用域枚举充当其枚举器的命名空间。这种内置命名空间有助于减少全局命名空间污染以及在全局范围中使用作用域枚举时可能发生的名称冲突。
要访问作用域枚举器，我们像它在与作用域枚举同名的命名空间中一样访问它：
#include <iostream>

int main()
{
    enum class Color // "enum class" defines this as a scoped enum rather than an unscoped enum
    {
        red, // red is considered part of Color's scope region
        blue,
    };

    std::cout << red << '\n';        // compile error: red not defined in this scope region
    std::cout << Color::red << '\n'; // compile error: std::cout doesn't know how to print this (will not implicitly convert to int)

    Color color { Color::blue }; // okay

    return 0;
}
因为作用域枚举为其枚举器提供了自己的隐式命名空间，所以没有必要将作用域枚举放在另一个作用域区域（例如命名空间）内，除非有其他令人信服的理由这样做，因为它将是多余的。
作用域枚举不会隐式转换为整数
与非作用域枚举器不同，作用域枚举器不会隐式转换为整数。在大多数情况下，这是一件好事，因为它很少有意义，并且有助于防止语义错误，例如比较来自不同枚举的枚举器，或表达式如
red + 5
。
请注意，您仍然可以比较来自同一作用域枚举中的枚举器（因为它们是相同类型的）：
#include <iostream>
int main()
{
    enum class Color
    {
        red,
        blue,
    };

    Color shirt { Color::red };

    if (shirt == Color::red) // this Color to Color comparison is okay
        std::cout << "The shirt is red!\n";
    else if (shirt == Color::blue)
        std::cout << "The shirt is blue!\n";

    return 0;
}
偶尔会有一些情况，将作用域枚举器视为整数值很有用。在这些情况下，您可以使用
static_cast
将作用域枚举器显式转换为整数。在 C++23 中更好的选择是使用
std::to_underlying()
（在 <utility> 头文件中定义），它将枚举器转换为枚举底层类型的值。
#include <iostream>
#include <utility> // for std::to_underlying() (C++23)

int main()
{
    enum class Color
    {
        red,
        blue,
    };

    Color color { Color::blue };

    std::cout << color << '\n'; // won't work, because there's no implicit conversion to int
    std::cout << static_cast<int>(color) << '\n';   // explicit conversion to int, will print 1
    std::cout << std::to_underlying(color) << '\n'; // convert to underlying type, will print 1 (C++23)

    return 0;
}
反过来，您也可以
static_cast
一个整数到作用域枚举器，这在从用户输入时很有用。
#include <iostream>

int main()
{
    enum class Pet
    {
        cat, // assigned 0
        dog, // assigned 1
        pig, // assigned 2
        whale, // assigned 3
    };

    std::cout << "Enter a pet (0=cat, 1=dog, 2=pig, 3=whale): ";

    int input{};
    std::cin >> input; // input an integer

    Pet pet{ static_cast<Pet>(input) }; // static_cast our integer to a Pet

    return 0;
}
从 C++17 开始，您可以使用整数值对作用域枚举进行列表初始化，而无需使用 static_cast（与无作用域枚举不同，您无需指定基类型）。
// using enum class Pet from prior example
   Pet pet { 1 }; // okay
最佳实践
优先使用作用域枚举而不是无作用域枚举，除非有充分的理由不这样做。
尽管作用域枚举提供了许多优点，但在 C++ 中，无作用域枚举仍然被普遍使用，因为在某些情况下，我们希望进行隐式转换为 int（过多的 static_casting 会让人感到恼火），并且我们不需要额外的命名空间。
简化作用域枚举到整数的转换（高级）
作用域枚举很棒，但缺乏隐式转换为整数的功能有时会成为一个痛点。如果我们需要经常将作用域枚举转换为整数（例如，我们想将作用域枚举用作数组索引的情况），每次需要转换时都必须使用 static_cast 会显著地使代码混乱。
如果您发现自己处于需要更方便地将作用域枚举转换为整数的情况，一个有用的技巧是重载一元
operator+
来执行此转换。
#include <iostream>
#include <type_traits> // for std::underlying_type_t

enum class Animals
{
    chicken, // 0
    dog, // 1
    cat, // 2
    elephant, // 3
    duck, // 4
    snake, // 5

    maxAnimals,
};

// Overload the unary + operator to convert an enum to the underlying type
// adapted from https://stackoverflow.com/a/42198760, thanks to Pixelchemist for the idea
// In C++23, you can #include <utility> and return std::to_underlying(a) instead
template <typename T>
constexpr auto operator+(T a) noexcept
{
    return static_cast<std::underlying_type_t<T>>(a);
}

int main()
{
    std::cout << +Animals::elephant << '\n'; // convert Animals::elephant to an integer using unary operator+

    return 0;
}
这会打印
3
此方法可防止意外的隐式转换为整型，但提供了一种在需要时显式请求此类转换的便捷方式。
using enum
语句
C++20
在 C++20 中引入的
using enum
语句将枚举中的所有枚举器导入到当前作用域。当与枚举类类型一起使用时，这允许我们访问枚举类枚举器，而无需在每个枚举器前加上枚举类的名称。
这在某些情况下很有用，否则我们会有许多相同、重复的前缀，例如在 switch 语句中：
#include <iostream>
#include <string_view>

enum class Color
{
    black,
    red,
    blue,
};

constexpr std::string_view getColor(Color color)
{
    using enum Color; // bring all Color enumerators into current scope (C++20)
    // We can now access the enumerators of Color without using a Color:: prefix

    switch (color)
    {
    case black: return "black"; // note: black instead of Color::black
    case red:   return "red";
    case blue:  return "blue";
    default:    return "???";
    }
}

int main()
{
    Color shirt{ Color::blue };

    std::cout << "Your shirt is " << getColor(shirt) << '\n';

    return 0;
}
在上面的例子中，
Color
是一个枚举类，所以我们通常会使用完全限定名（例如
Color::blue
）来访问枚举器。然而，在函数
getColor()
中，我们添加了语句
using enum Color;
，这允许我们访问这些枚举器而不需要
Color::
前缀。
这使我们避免了在 switch 语句中出现多个、冗余的、显而易见的前缀。
小测验时间
问题 #1
定义一个名为 Animal 的枚举类，其中包含以下动物：pig（猪）、chicken（鸡）、goat（山羊）、cat（猫）、dog（狗）、duck（鸭）。编写一个名为 getAnimalName() 的函数，它接受一个 Animal 参数并使用 switch 语句返回该动物的名称作为 std::string_view（如果使用 C++14，则为 std::string）。编写另一个名为 printNumberOfLegs() 的函数，它使用 switch 语句打印每种动物行走的腿数。确保这两个函数都有一个 default 情况，打印错误消息。从 main() 调用 printNumberOfLegs()，传入一只猫和一只鸡。你的输出应该如下所示：
A cat has 4 legs.
A chicken has 2 legs.
显示答案
#include <iostream>
#include <string_view> // C++17
//#include <string> // for C++14

enum class Animal
{
    pig,
    chicken,
    goat,
    cat,
    dog,
    duck,
};

constexpr std::string_view getAnimalName(Animal animal) // C++17
// const std::string getAnimalName(Animal animal) // C++14
{
    // If C++20 capable, could use `using enum Animal` here to reduce Animal prefix redundancy
    switch (animal)
    {
        case Animal::chicken:
            return "chicken";
        case Animal::duck:
            return "duck";
        case Animal::pig:
            return "pig";
        case Animal::goat:
            return "goat";
        case Animal::cat:
            return "cat";
        case Animal::dog:
            return "dog";

        default:
            return "???";
    }
}

void printNumberOfLegs(Animal animal)
{
    std::cout << "A " << getAnimalName(animal) << " has ";

    // If C++20 capable, could use `using enum Animal` here to reduce Animal prefix redundancy
    switch (animal)
    {
        case Animal::chicken:
        case Animal::duck:
            std::cout << 2;
            break;

        case Animal::pig:
        case Animal::goat:
        case Animal::cat:
        case Animal::dog:
            std::cout << 4;
            break;

        default:
            std::cout << "???";
            break;
    }

    std::cout << " legs.\n";
}

int main()
{
    printNumberOfLegs(Animal::cat);
    printNumberOfLegs(Animal::chicken);

    return 0;
}
下一课
13.7
结构体、成员和成员选择简介
返回目录
上一课
13.5
I/O 运算符重载简介