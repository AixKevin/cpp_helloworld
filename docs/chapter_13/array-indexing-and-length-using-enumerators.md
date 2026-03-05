# 16.9 — 使用枚举器进行数组索引和长度

16.9 — 使用枚举器进行数组索引和长度
Alex
2023 年 9 月 11 日下午 2:43 PDT
2024 年 5 月 8 日
数组最大的文档问题之一是整数索引没有向程序员提供关于索引含义的任何信息。
考虑一个存储 5 个考试成绩的数组
#include <vector>

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };

    testScores[2] = 76; // who does this represent?
}
testScores[2]
代表哪个学生？这不清楚。
使用无作用域枚举器进行索引
在课程
16.3 -- std::vector 和无符号长度及下标问题
中，我们花了很多时间讨论
std::vector
::operator[]
（以及其他可下标的 C++ 容器类）的索引类型是
size_type
，通常是
std::size_t
的别名。因此，我们的索引要么是
std::size_t
类型，要么是可转换为
std::size_t
的类型。
由于无作用域枚举会隐式转换为
std::size_t
，这意味着我们可以使用无作用域枚举作为数组索引来帮助记录索引的含义
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };

    testScores[Students::stan] = 76; // we are now updating the test score belonging to stan

    return 0;
}
通过这种方式，每个数组元素代表什么就清楚得多了。
由于枚举器是隐式 constexpr，因此枚举器到无符号整数类型的转换不被认为是窄化转换，从而避免了有符号/无符号索引问题。
使用非 constexpr 无作用域枚举进行索引
无作用域枚举的基础类型是实现定义的（因此，可以是带符号或无符号的整数类型）。由于枚举器是隐式 constexpr，只要我们坚持使用无作用域枚举器进行索引，就不会遇到符号转换问题。
但是，如果我们定义一个枚举类型的非 constexpr 变量，然后尝试用它来索引
std::vector
，那么在默认无作用域枚举为有符号类型的任何平台上，我们可能会收到符号转换警告
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };
    Students::Names name { Students::stan }; // non-constexpr

    testScores[name] = 76; // may trigger a sign conversion warning if Student::Names defaults to a signed underlying type

    return 0;
}
在这种特殊情况下，我们可以将
name
设置为 constexpr（以便从 constexpr 有符号整数类型到
std::size_t
的转换不是窄化转换）。但是，当我们的初始化器不是常量表达式时，这就不起作用了。
另一种选择是显式指定枚举的基础类型为无符号 int
#include <vector>

namespace Students
{
    enum Names : unsigned int // explicitly specifies the underlying type is unsigned int
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };
    Students::Names name { Students::stan }; // non-constexpr

    testScores[name] = 76; // not a sign conversion since name is unsigned

    return 0;
}
在上面的例子中，由于
name
现在保证是
unsigned int
，它可以转换为
std::size_t
而不会出现符号转换问题。
使用计数枚举器
请注意，我们在枚举器列表的末尾定义了一个额外的枚举器，名为
max_students
。如果所有先前的枚举器都使用默认值（推荐这样做），则此枚举器的默认值将与前面枚举器的计数匹配。在上面的示例中，
max_students
的值为
5
，因为之前定义了 5 个枚举器。非正式地，我们称之为
计数枚举器
，因为它的值表示先前定义的枚举器的计数。
然后，此计数枚举器可以在我们需要先前枚举器计数的任何地方使用。例如
#include <iostream>
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        // add future enumerators here
        max_students // 5
    };
}

int main()
{
    std::vector<int> testScores(Students::max_students); // Create a vector with 5 elements

    testScores[Students::stan] = 76; // we are now updating the test score belonging to stan

    std::cout << "The class has " << Students::max_students << " students\n";

    return 0;
}
我们在两个地方使用
max_students
：首先，我们创建一个长度为
max_students
的
std::vector
，因此该向量每个学生将有一个元素。我们还使用
max_students
来打印学生人数。
这种技术也很不错，因为如果以后添加另一个枚举器（就在
max_students
之前），那么
max_students
将自动增加一个，并且所有使用
max_students
的数组都将更新为使用新长度而无需进一步修改。
#include <vector>
#include <iostream>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        wendy, // 5 (added)
        // add future enumerators here
        max_students // now 6
    };
}

int main()
{
    std::vector<int> testScores(Students::max_students); // will now allocate 6 elements

    testScores[Students::stan] = 76; // still works

    std::cout << "The class has " << Students::max_students << " students\n";

    return 0;
}
使用计数枚举器断言数组长度
通常，我们使用初始化列表创建数组，并打算使用枚举器索引该数组。在这种情况下，断言容器的大小等于我们的计数枚举器会很有用。如果此断言触发，则我们的枚举器列表存在某种错误，或者我们提供了错误的初始化器数量。当向枚举添加新枚举器但未向数组添加新初始化值时，这很容易发生。
例如
#include <cassert>
#include <iostream>
#include <vector>

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
    std::vector testScores { 78, 94, 66, 77, 14 };

    // Ensure the number of test scores is the same as the number of students
    assert(std::size(testScores) == max_students);

    return 0;
}
提示
如果你的数组是 constexpr，那么你应该改用
static_assert
。
std::vector
不支持 constexpr，但
std::array
（和 C 风格数组）支持。
我们将在课程
17.3 -- 传递和返回 std::array
中进一步讨论。
最佳实践
使用
static_assert
确保你的 constexpr 数组的长度与你的计数枚举器匹配。
使用
assert
确保你的非 constexpr 数组的长度与你的计数枚举器匹配。
数组和枚举类
由于无作用域枚举会用其枚举器污染它们所定义的命名空间，因此在枚举尚未包含在另一个作用域区域（例如命名空间或类）中的情况下，最好使用枚举类。
然而，由于枚举类没有隐式转换为整数类型，当我们尝试将它们的枚举器用作数组索引时，我们会遇到问题
#include <iostream>
#include <vector>

enum class StudentNames // now an enum class
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
    // compile error: no conversion from StudentNames to std::size_t
    std::vector<int> testScores(StudentNames::max_students);

    // compile error: no conversion from StudentNames to std::size_t
    testScores[StudentNames::stan] = 76;

    // compile error: no conversion from StudentNames to any type that operator<< can output
    std::cout << "The class has " << StudentNames::max_students << " students\n";

    return 0;
}
有几种方法可以解决这个问题。最明显的是，我们可以将枚举器
static_cast
到一个整数
#include <iostream>
#include <vector>

enum class StudentNames
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
    std::vector<int> testScores(static_cast<int>(StudentNames::max_students));

    testScores[static_cast<int>(StudentNames::stan)] = 76;

    std::cout << "The class has " << static_cast<int>(StudentNames::max_students) << " students\n";

    return 0;
}
然而，这不仅打字麻烦，而且还会大大使我们的代码混乱。
更好的选择是使用我们在课程
13.6 -- 有作用域枚举（枚举类）
中介绍的辅助函数，该函数允许我们使用一元
operator+
将枚举类的枚举器转换为整数值。
#include <iostream>
#include <type_traits> // for std::underlying_type_t
#include <vector>

enum class StudentNames
{
    kenny, // 0
    kyle, // 1
    stan, // 2
    butters, // 3
    cartman, // 4
    max_students // 5
};

// Overload the unary + operator to convert StudentNames to the underlying type
constexpr auto operator+(StudentNames a) noexcept
{
    return static_cast<std::underlying_type_t<StudentNames>>(a);
}

int main()
{
    std::vector<int> testScores(+StudentNames::max_students);

    testScores[+StudentNames::stan] = 76;

    std::cout << "The class has " << +StudentNames::max_students << " students\n";

    return 0;
}
但是，如果你要进行大量枚举器到整数的转换，那么最好还是在命名空间（或类）中使用标准枚举。
小测验时间
问题 #1
创建一个程序定义的枚举（在命名空间中），包含以下动物的名称：鸡、狗、猫、大象、鸭子和蛇。定义一个数组，每个动物一个元素，并使用初始化列表将每个元素初始化为该动物的腿数。断言该数组具有正确数量的初始化器。
编写一个 main() 函数，使用枚举器打印大象的腿数。
显示答案
#include <cassert>
#include <iostream>
#include <vector>

namespace Animals
{
    enum Animals
    {
        chicken,
        dog,
        cat,
        elephant,
        duck,
        snake,
        max_animals
    };

    const std::vector legs{ 2, 4, 4, 4, 2, 0 };
}

int main()
{
    // Ensure the number of legs is the same as the number of animals
    assert(std::size(Animals::legs) == Animals::max_animals);

    std::cout << "An elephant has " << Animals::legs[Animals::elephant] << " legs.\n";

    return 0;
}
下一课
16.10
std::vector 的大小调整和容量
返回目录
上一课
16.8
基于范围的 for 循环 (for-each)