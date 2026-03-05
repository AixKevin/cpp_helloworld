# 13.5 — I/O 运算符重载简介

13.5 — I/O 运算符重载简介
Alex
2024年3月25日，下午2:51 PDT
2024年10月28日
在上一课 (
13.4 -- 枚举与字符串之间的转换
) 中，我们展示了这个例子，我们使用了一个函数将枚举转换为等效的字符串
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
尽管上面的例子运行良好，但有两个缺点
我们必须记住我们创建的函数名，以便获取枚举器名称。
不得不调用这样的函数会增加我们输出语句的冗余。
理想情况下，如果我们可以以某种方式教会
operator<<
输出枚举，这样我们就可以做类似
std::cout << shirt
的事情并让它按照我们期望的方式工作，那就太好了。
运算符重载简介
在
11.1 -- 函数重载简介
课中，我们介绍了函数重载，它允许我们创建多个同名函数，只要每个函数都有唯一的函数原型。使用函数重载，我们可以创建适用于不同数据类型的函数变体，而无需为每个变体想出唯一的名称。
类似地，C++ 也支持**运算符重载**，它允许我们定义现有运算符的重载，以便我们可以使这些运算符与我们程序定义的数据类型一起工作。
基本运算符重载相当简单
使用运算符的名称作为函数的名称来定义函数。
为每个操作数添加适当类型的参数（从左到右）。其中一个参数必须是用户定义类型（类类型或枚举类型），否则编译器将报错。
将返回类型设置为有意义的任何类型。
使用返回语句返回操作的结果。
当编译器在表达式中遇到运算符的使用，并且一个或多个操作数是用户定义类型时，编译器将检查是否存在可以用来解析该调用的重载运算符函数。例如，给定表达式
x + y
，编译器将使用函数重载解析来查看是否存在可以用来评估该操作的
operator+(x, y)
函数调用。如果找到了非模糊的
operator+
函数，它将被调用，并且操作结果作为返回值返回。
相关内容
我们将在
第 21 章
中更详细地介绍运算符重载。
致进阶读者
运算符也可以重载为最左侧操作数的成员函数。我们将在
21.5 -- 使用成员函数重载运算符
课中讨论这一点。
重载
operator<<
以打印枚举器
在继续之前，让我们快速回顾一下
operator<<
在用于输出时是如何工作的。
考虑一个简单的表达式，例如
std::cout << 5
。
std::cout
的类型是
std::ostream
（标准库中的用户定义类型），
5
是
int
类型的字面量。
当评估此表达式时，编译器将查找可以处理
std::ostream
和
int
类型参数的重载
operator<<
函数。它将找到这样一个函数（也作为标准 I/O 库的一部分定义）并调用它。在该函数内部，
std::cout
用于将
x
输出到控制台（具体实现方式由实现定义）。最后，
operator<<
函数返回其左操作数（在本例中为
std::cout
），以便后续的
operator<<
调用可以被链式调用。
考虑到以上内容，让我们实现
operator<<
的重载来打印一个
Color
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

// Teach operator<< how to print a Color
// std::ostream is the type of std::cout, std::cerr, etc...
// The return type and parameter type are references (to prevent copies from being made)
std::ostream& operator<<(std::ostream& out, Color color)
{
    out << getColorName(color); // print our color's name to whatever output stream out 
    return out;                 // operator<< conventionally returns its left operand

    // The above can be condensed to the following single line:
    // return out << getColorName(color)
}

int main()
{
	Color shirt{ blue };
	std::cout << "Your shirt is " << shirt << '\n'; // it works!

	return 0;
}
这会打印
Your shirt is blue
让我们来详细分析一下我们重载的运算符函数。首先，函数名为
operator<<
，因为这是我们要重载的运算符的名称。
operator<<
有两个参数。左参数（将与左操作数匹配）是我们的输出流，其类型为
std::ostream
。我们在这里使用非 const 引用传递，因为我们不想在函数调用时复制
std::ostream
对象，但
std::ostream
对象需要被修改才能进行输出。右参数（将与右操作数匹配）是我们的
Color
对象。由于
operator<<
通常返回其左操作数，因此返回类型与左操作数的类型匹配，即
std::ostream&
。
现在让我们看看实现。
std::ostream
对象已经知道如何使用
operator<<
打印
std::string_view
（这是标准库的一部分）。因此
out << getColorName(color)
只是将我们的颜色的名称作为
std::string_view
获取，然后将其打印到输出流。
请注意，我们的实现使用参数
out
而不是
std::cout
，因为我们希望允许调用者决定他们将输出到哪个输出流（例如
std::cerr << color
应该输出到
std::cerr
，而不是
std::cout
）。
返回左操作数也很简单。左操作数是参数
out
，所以我们只需返回
out
。
综合起来：当我们调用
std::cout << shirt
时，编译器将看到我们已经重载了
operator<<
来处理
Color
类型的对象。然后调用我们重载的
operator<<
函数，将
std::cout
作为
out
参数，并将我们的
shirt
变量（值为
blue
）作为
color
参数。由于
out
是
std::cout
的引用，而
color
是枚举器
blue
的副本，表达式
out << getColorName(color)
会在控制台打印
"blue"
。最后，
out
被返回给调用者，以防我们想链式输出更多内容。
重载
operator>>
以输入枚举器
类似于我们上面能够教
operator<<
输出枚举的方式，我们也可以教
operator>>
如何输入枚举
#include <iostream>
#include <limits>
#include <optional>
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
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;

    return {};
}

// pet is an in/out parameter
std::istream& operator>>(std::istream& in, Pet& pet)
{
    std::string s{};
    in >> s; // get input string from user

    std::optional<Pet> match { getPetFromString(s) };
    if (match) // if we found a match
    {
        pet = *match; // dereference std::optional to get matching enumerator
        return in;
    }

    // We didn't find a match, so input must have been invalid
    // so we will set input stream to fail state
    in.setstate(std::ios_base::failbit);
    
    // On an extraction failure, operator>> zero-initializes fundamental types
    // Uncomment the following line to make this operator do the same thing
    // pet = {};

    return in;
}

int main()
{
    std::cout << "Enter a pet: cat, dog, pig, or whale: ";
    Pet pet{};
    std::cin >> pet;
        
    if (std::cin) // if we found a match
        std::cout << "You chose: " << getPetName(pet) << '\n';
    else
    {
        std::cin.clear(); // reset the input stream to good
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Your pet was not valid\n";
    }

    return 0;
}
与输出情况相比，这里有几点值得注意。首先，
std::cin
的类型是
std::istream
，所以我们使用
std::istream&
作为左参数和返回值的类型，而不是
std::ostream&
。其次，
pet
参数是一个非 const 引用。这允许我们的
operator>>
在提取成功时修改传入的右操作数的值。
关键见解
我们的右操作数（
pet
）是一个出参。我们在
12.13 -- 入参和出参
课中介绍了出参。
如果
pet
是值参数而不是引用参数，那么我们的
operator>>
函数最终会将新值赋给右操作数的副本，而不是实际的右操作数。在这种情况下，我们希望修改右操作数。
在函数内部，我们使用
operator>>
输入一个
std::string
（它已经知道如何做到这一点）。如果用户输入的值与我们的宠物之一匹配，那么我们可以将
pet
分配给适当的枚举器并返回左操作数（
in
）。
如果用户没有输入有效的宠物，那么我们通过将
std::cin
置于“失败模式”来处理这种情况。这是
std::cin
在提取失败时通常进入的状态。调用者随后可以检查
std::cin
以查看提取是成功还是失败。
相关内容
在
17.6 -- std::array 和枚举
课中，我们展示了如何使用
std::array
来减少输入和输出运算符的冗余，并避免在添加新的枚举器时不得不修改它们。
下一课
13.6
作用域枚举 (enum 类)
返回目录
上一课
13.4
枚举与字符串之间的转换