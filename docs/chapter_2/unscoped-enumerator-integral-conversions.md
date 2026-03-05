# 13.3 — 无作用域枚举器整数转换

13.3 — 无作用域枚举器整数转换
Alex
2022年1月18日，太平洋标准时间上午10:20
2024年7月31日
在上一课（
13.2 -- 无作用域枚举
）中，我们提到枚举器是符号常量。当时我们没有告诉您的是，这些枚举器的值是整数类型。
这与字符（
4.11 -- 字符
）的情况类似。考虑
char ch { 'A' };
一个字符实际上只是一个1字节的整数值，字符
'A'
被转换为一个整数值（在本例中为
65
）并存储。
当我们定义一个枚举时，每个枚举器都会根据其在枚举器列表中的位置自动关联一个整数值。默认情况下，第一个枚举器被赋予整数值
0
，每个后续枚举器的值比前一个枚举器大1。
enum Color
{
    black,   // 0
    red,     // 1
    blue,    // 2
    green,   // 3
    white,   // 4
    cyan,    // 5
    yellow,  // 6
    magenta, // 7
};

int main()
{
    Color shirt{ blue }; // shirt actually stores integral value 2

    return 0;
}
可以显式定义枚举器的值。这些整数值可以是正数或负数，并且可以与其他枚举器共享相同的值。任何未定义的枚举器都会被赋予比前一个枚举器大1的值。
enum Animal
{
    cat = -3,    // values can be negative
    dog,         // -2
    pig,         // -1
    horse = 5,
    giraffe = 5, // shares same value as horse
    chicken,     // 6 
};
请注意，在这种情况下，
horse
和
giraffe
被赋予了相同的值。当这种情况发生时，枚举器变得非互斥——本质上，
horse
和
giraffe
是可以互换的。尽管C++允许，但通常应避免在同一个枚举中为两个枚举器分配相同的值。
大多数情况下，枚举器的默认值正是您想要的，因此除非您有特殊原因，否则不要提供自己的值。
最佳实践
除非您有令人信服的理由，否则请避免为您的枚举器分配显式值。
值初始化枚举
如果枚举被零初始化（当我们使用值初始化时发生），枚举将被赋予值
0
，即使没有相应的枚举器具有该值。
#include <iostream>

enum Animal
{
    cat = -3,    // -3
    dog,         // -2
    pig,         // -1
    // note: no enumerator with value 0 in this list
    horse = 5,   // 5
    giraffe = 5, // 5
    chicken,     // 6 
};

int main()
{
    Animal a {}; // value-initialization zero-initializes a to value 0
    std::cout << a; // prints 0

    return 0;
}
这有两个语义后果：
如果存在值为0的枚举器，则值初始化将枚举默认为该枚举器的含义。例如，使用前面的
enum Color
示例，值初始化的
Color
将默认为
black
）。因此，考虑将值为0的枚举器设为表示枚举最佳默认含义的枚举器是个好主意。
像这样可能会导致问题
enum UniverseResult
{
    destroyUniverse, // default value (0)
    saveUniverse
};
如果不存在值为0的枚举器，则值初始化很容易创建语义上无效的枚举。在这种情况下，我们建议添加一个值为0的“无效”或“未知”枚举器，以便您有该状态含义的文档，以及可以显式处理的该状态的名称。
enum Winner
{
    winnerUnknown, // default value (0)
    player1,
    player2,
};

// somewhere later in your code
if (w == winnerUnknown) // handle case appropriately
最佳实践
将表示0的枚举器作为枚举的最佳默认含义。如果没有好的默认含义，请考虑添加一个值为0的“无效”或“未知”枚举器，以便该状态得到明确文档，并在适当的地方进行明确处理。
无作用域枚举将隐式转换为整数值
尽管枚举存储整数值，但它们不被视为整数类型（它们是复合类型）。然而，无作用域枚举将隐式转换为整数值。因为枚举器是编译时常量，所以这是一个constexpr转换（我们在
10.4 -- 窄化转换、列表初始化和constexpr初始化器
中介绍这些内容）。
考虑以下程序
#include <iostream>

enum Color
{
    black, // assigned 0
    red, // assigned 1
    blue, // assigned 2
    green, // assigned 3
    white, // assigned 4
    cyan, // assigned 5
    yellow, // assigned 6
    magenta, // assigned 7
};

int main()
{
    Color shirt{ blue };

    std::cout << "Your shirt is " << shirt << '\n'; // what does this do?

    return 0;
}
由于枚举类型持有整数值，正如您所期望的，这将打印
Your shirt is 2
当枚举类型在函数调用中或与运算符一起使用时，编译器将首先尝试查找与枚举类型匹配的函数或运算符。例如，当编译器尝试编译
std::cout << shirt
时，编译器将首先查看
operator<<
是否知道如何将
Color
类型的对象（因为
shirt
是
Color
类型）打印到
std::cout
。它不知道。
由于编译器找不到匹配项，它将检查
operator<<
是否知道如何打印无作用域枚举转换为的整数类型的对象。由于它知道，
shirt
中的值被转换为整数值并打印为整数值
2
。
相关内容
我们在
13.4 -- 将枚举转换为字符串以及从字符串转换枚举
中展示了如何将枚举转换为字符串。
我们在
13.5 -- I/O运算符重载简介
中教
std::cout
如何打印枚举器。
枚举大小和底层类型（基）
枚举器的值是整数类型。但是是哪种整数类型？用于表示枚举器值的特定整数类型称为枚举的
底层类型
（或
基
）。
对于无作用域枚举，C++标准没有指定应使用哪种特定整数类型作为底层类型，因此选择是实现定义的。大多数编译器将使用
int
作为底层类型（这意味着无作用域枚举的大小将与
int
相同），除非需要更大的类型来存储枚举器值。但您不应假定这对于每个编译器或平台都成立。
可以显式指定枚举的底层类型。底层类型必须是整数类型。例如，如果您在某些对带宽敏感的环境中工作（例如通过网络发送数据），您可能希望为枚举指定一个较小的类型
#include <cstdint>  // for std::int8_t
#include <iostream>

// Use an 8-bit integer as the enum underlying type
enum Color : std::int8_t
{
    black,
    red,
    blue,
};

int main()
{
    Color c{ black };
    std::cout << sizeof(c) << '\n'; // prints 1 (byte)

    return 0;
}
最佳实践
仅在必要时指定枚举的基类型。
警告
由于
std::int8_t
和
std::uint8_t
通常是char类型的类型别名，因此将这些类型中的任何一个用作枚举基很可能导致枚举器打印为char值而不是int值。
整数到无作用域枚举器转换
虽然编译器会隐式将无作用域枚举转换为整数，但它
不会
隐式将整数转换为无作用域枚举。以下内容将产生编译错误
enum Pet // no specified base
{
    cat, // assigned 0
    dog, // assigned 1
    pig, // assigned 2
    whale, // assigned 3
};

int main()
{
    Pet pet { 2 }; // compile error: integer value 2 won't implicitly convert to a Pet
    pet = 3;       // compile error: integer value 3 won't implicitly convert to a Pet

    return 0;
}
有两种方法可以解决这个问题。
首先，您可以使用
static_cast
显式将整数转换为无作用域枚举器
enum Pet // no specified base
{
    cat, // assigned 0
    dog, // assigned 1
    pig, // assigned 2
    whale, // assigned 3
};

int main()
{
    Pet pet { static_cast<Pet>(2) }; // convert integer 2 to a Pet
    pet = static_cast<Pet>(3);       // our pig evolved into a whale!

    return 0;
}
我们将在
13.4 -- 将枚举转换为字符串以及从字符串转换枚举
中看到一个我们利用此功能的示例。
将任何由目标枚举的枚举器表示的整数值进行static_cast是安全的。由于我们的
Pet
枚举具有值
0
、
1
、
2
和
3
的枚举器，因此将整数值
0
、
1
、
2
和
3
static_cast为
Pet
是有效的。
将任何在目标枚举底层类型范围内的整数值进行static_cast也是安全的，即使没有枚举器表示该值。将值static_cast到底层类型范围之外将导致未定义行为。
致进阶读者
如果枚举具有显式定义的底层类型，则枚举的范围与底层类型的范围相同。
如果枚举没有显式底层类型，情况会有点复杂。在这种情况下，编译器可以选择底层类型，并且它可以选择任何有符号或无符号类型，只要所有枚举器的值都适合该类型。鉴于此，只有当整数值适合能够容纳所有枚举器值的最小位数范围时，才能安全地进行static_cast。
让我们用两个例子来说明这一点
对于值为2、9和12的枚举器，这些枚举器最小可以容纳在一个范围为0到15的无符号4位整数类型中。因此，只有将整数值0到15static_cast为这种枚举类型才是安全的。
对于值为-28、2和6的枚举器，这些枚举器最小可以容纳在一个范围为-32到31的有符号6位整数类型中。因此，只有将整数值-32到31static_cast为这种枚举类型才是安全的。
其次，从C++17开始，如果无作用域枚举具有显式指定的基，则编译器将允许您使用整数值列表初始化无作用域枚举
enum Pet: int // we've specified a base
{
    cat, // assigned 0
    dog, // assigned 1
    pig, // assigned 2
    whale, // assigned 3
};

int main()
{
    Pet pet1 { 2 }; // ok: can brace initialize unscoped enumeration with specified base with integer (C++17)
    Pet pet2 (2);   // compile error: cannot direct initialize with integer
    Pet pet3 = 2;   // compile error: cannot copy initialize with integer

    pet1 = 3;       // compile error: cannot assign with integer

    return 0;
}
小测验时间
问题 #1
对或错。枚举器可以是
给定整数值
显示答案
对
没有给定显式值
显示答案
对。未显式赋值的枚举器将隐式赋值为前一个枚举器的整数值 + 1。如果没有前一个枚举器，则枚举器将取值为0。
给定浮点值
显示答案
错
给定负值
显示答案
对
给定非唯一值
显示答案
对
给定先前枚举器的值（例如 magenta = red）
显示答案
对。枚举器不必是唯一的。由于枚举器隐式转换为整数，并且整数可以赋给枚举器，因此枚举器可以用其他枚举器初始化（尽管通常没有多少理由这样做！）。
给定非 constexpr 值
显示答案
错。由于枚举器是 constexpr，它们的值也必须是 constexpr。
下一课
13.4
将枚举转换为字符串以及从字符串转换枚举
返回目录
上一课
13.2
无作用域枚举