# 13.4 — 将枚举类型与字符串相互转换

13.4 — 将枚举类型与字符串相互转换
Alex
2024年3月25日，太平洋夏令时下午2:51
2025年2月13日
在上一课（
13.3 -- 无作用域枚举成员的整型转换
）中，我们展示了一个这样的例子：
#include <iostream>

enum Color
{
    black, // 0
    red,   // 1
    blue,  // 2
};

int main()
{
    Color shirt{ blue };

    std::cout << "Your shirt is " << shirt << '\n';

    return 0;
}
这会打印
Your shirt is 2
因为
operator<<
不知道如何打印
Color
，所以编译器会隐式地将
Color
转换为一个整型值并打印出来。
大多数情况下，将枚举类型打印为整型值（例如
2
）并不是我们想要的。相反，我们通常希望打印枚举成员所代表的名称（例如
blue
）。C++ 没有提供开箱即用的方法来实现这一点，所以我们必须自己寻找解决方案。幸运的是，这并不是很困难。
获取枚举成员的名称
获取枚举成员名称的典型方法是编写一个函数，允许我们传入一个枚举成员并以字符串形式返回该枚举成员的名称。但这需要某种方法来确定对于给定的枚举成员应该返回哪个字符串。
有两种常见的方法可以做到这一点。
在课程
8.5 -- Switch 语句基础
中，我们提到 switch 语句可以切换整型值或枚举值。在下面的例子中，我们使用 switch 语句来选择一个枚举成员并返回该枚举成员对应的颜色字符串字面量：
#include <iostream>
#include <string_view>

enum Color
{
    black,
    red,
    blue,
};

constexpr std::string_view getColorName(Color color)
{
    switch (color)
    {
    case black: return "black";
    case red:   return "red";
    case blue:  return "blue";
    default:    return "???";
    }
}

int main()
{
    constexpr Color shirt{ blue };

    std::cout << "Your shirt is " << getColorName(shirt) << '\n';

    return 0;
}
这会打印
Your shirt is blue
在上面的例子中，我们对
color
进行切换，它保存着我们传入的枚举成员。在 switch 内部，我们为
Color
的每个枚举成员都有一个 case 标签。每个 case 都将适当的颜色名称作为 C 风格字符串字面量返回。这个 C 风格字符串字面量会被隐式转换为
std::string_view
，然后返回给调用者。我们还有一个 default case，它返回
"???"
，以防用户传入我们不期望的值。
提醒
由于 C 风格字符串字面量在整个程序中都存在，所以返回一个正在查看 C 风格字符串字面量的
std::string_view
是没问题的。当
std::string_view
被复制回调用者时，被查看的 C 风格字符串字面量仍然存在。
这个函数是 constexpr，因此我们可以在常量表达式中使用颜色的名称。
相关内容
constexpr 函数在课程
F.1 -- Constexpr 函数
中有所介绍。
虽然这让我们能够获取枚举成员的名称，但如果我们想将该名称打印到控制台，执行
std::cout << getColorName(shirt)
不如
std::cout << shirt
那么好。我们将在即将到来的课程
13.5 -- I/O 运算符重载简介
中教
std::cout
如何打印枚举类型。
解决将枚举成员映射到字符串的第二个方法是使用数组。我们将在课程
17.6 -- std::array 和枚举类型
中介绍这一点。
无作用域枚举成员输入
现在我们来看一个输入的情况。在下面的例子中，我们定义了一个
Pet
枚举。因为
Pet
是一个程序定义的类型，所以语言不知道如何使用
std::cin
输入一个
Pet
：
#include <iostream>

enum Pet
{
    cat,   // 0
    dog,   // 1
    pig,   // 2
    whale, // 3
};

int main()
{
    Pet pet { pig };
    std::cin >> pet; // compile error: std::cin doesn't know how to input a Pet

    return 0;
}
一个简单的解决方法是读取一个整数，然后使用
static_cast
将整数转换为适当枚举类型的枚举成员：
#include <iostream>
#include <string_view>

enum Pet
{
    cat,   // 0
    dog,   // 1
    pig,   // 2
    whale, // 3
};

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

int main()
{
    std::cout << "Enter a pet (0=cat, 1=dog, 2=pig, 3=whale): ";

    int input{};
    std::cin >> input; // input an integer

    if (input < 0 || input > 3)
        std::cout << "You entered an invalid pet\n";
    else
    {
        Pet pet{ static_cast<Pet>(input) }; // static_cast our integer to a Pet
        std::cout << "You entered: " << getPetName(pet) << '\n';
    }

    return 0;
}
虽然这可行，但有点笨拙。另请注意，我们应该只在知道
input
在枚举成员范围内时才进行
static_cast<Pet>(input)
。
从字符串获取枚举类型
如果用户能够输入代表枚举成员的字符串（例如“pig”），并且我们可以将该字符串转换为适当的
Pet
枚举成员，那将比输入数字更好。然而，这样做需要我们解决几个挑战。
首先，我们无法对字符串进行 switch，所以我们需要使用其他方式来匹配用户传入的字符串。这里最简单的方法是使用一系列 if 语句。
其次，如果用户传入无效字符串，我们应该返回哪个
Pet
枚举成员？一个选项是添加一个枚举成员来表示“无/无效”，并返回该值。然而，更好的选项是在这里使用
std::optional
。
相关内容
我们在课程
12.15 -- std::optional
中介绍了
std::optional
。
#include <iostream>
#include <optional> // for std::optional
#include <string>
#include <string_view>

enum Pet
{
    cat,   // 0
    dog,   // 1
    pig,   // 2
    whale, // 3
};

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
    // We can only switch on an integral value (or enum), not a string
    // so we have to use if-statements here
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;
    
    return {};
}

int main()
{
    std::cout << "Enter a pet: cat, dog, pig, or whale: ";
    std::string s{};
    std::cin >> s;
        
    std::optional<Pet> pet { getPetFromString(s) };

    if (!pet)
        std::cout << "You entered an invalid pet\n";
    else
        std::cout << "You entered: " << getPetName(*pet) << '\n';

    return 0;
}
在上述解决方案中，我们使用一系列 if-else 语句进行字符串比较。如果用户的输入字符串与枚举成员字符串匹配，我们返回相应的枚举成员。如果没有字符串匹配，我们返回
{}
，这意味着“没有值”。
致进阶读者
请注意，上述解决方案仅匹配小写字母。如果您想匹配任何字母大小写，可以使用以下函数将用户输入转换为小写：
#include <algorithm> // for std::transform
#include <cctype>    // for std::tolower
#include <iterator>  // for std::back_inserter
#include <string>
#include <string_view>

// This function returns a std::string that is the lower-case version of the std::string_view passed in.
// Only 1:1 character mapping can be performed by this function
std::string toASCIILowerCase(std::string_view sv)
{
    std::string lower{};
    std::transform(sv.begin(), sv.end(), std::back_inserter(lower),
        [](char c)
        { 
            return static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        });
    return lower;
}
此函数遍历
std::string_view sv
中的每个字符，使用
std::tolower()
（借助 lambda）将其转换为小写字符，然后将该小写字符附加到
lower
。
我们在课程
20.6 -- Lambda 表达式（匿名函数）简介
中介绍了 lambda 表达式。
与输出情况类似，如果我们能直接
std::cin >> pet
会更好。我们将在即将到来的课程
13.5 -- I/O 运算符重载简介
中介绍这一点。
下一课
13.5
I/O 运算符重载简介
返回目录
上一课
13.3
无作用域枚举成员的整型转换