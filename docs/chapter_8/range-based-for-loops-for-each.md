# 16.8 — 基于范围的 for 循环 (for-each)

16.8 — 基于范围的 for 循环 (for-each)
Alex
2015 年 7 月 31 日，下午 5:25 PDT
2024 年 12 月 28 日
在课程
16.6 -- 数组和循环
中，我们展示了使用 for 循环以循环变量作为索引遍历数组中每个元素的示例。下面是另一个这样的示例：
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    std::size_t length { fibonacci.size() };
    for (std::size_t index { 0 }; index < length; ++index)
       std::cout << fibonacci[index] << ' ';

    std::cout << '\n';

    return 0;
}
尽管 for 循环提供了一种方便灵活的方式来遍历数组，但它们也容易出错，容易出现差一错误，并且受数组索引符号问题的影响（在课程
16.7 -- 数组、循环和符号挑战解决方案
中讨论过）。
因为正向遍历数组是一种常见的操作，C++ 支持另一种 for 循环，称为
基于范围的 for 循环
（有时也称为
for-each 循环
），它允许遍历容器而无需显式索引。基于范围的 for 循环更简单、更安全，并且适用于 C++ 中的所有常见数组类型（包括
std::vector
、
std::array
和 C 风格数组）。
基于范围的 for 循环
基于范围的 for
语句的语法如下所示：
for (element_declaration : array_object)
   statement;
当遇到基于范围的 for 循环时，循环将遍历
array_object
中的每个元素。对于每次迭代，当前数组元素的值将分配给
element_declaration
中声明的变量，然后
statement
将执行。
为获得最佳结果，
element_declaration
应与数组元素具有相同的类型，否则将发生类型转换。
这是一个简单的示例，它使用
基于范围的 for
循环打印名为
fibonacci
的数组中的所有元素：
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (int num : fibonacci) // iterate over array fibonacci and copy each value into `num`
       std::cout << num << ' '; // print the current value of `num`

    std::cout << '\n';

    return 0;
}
这会打印
0 1 1 2 3 5 8 13 21 34 55 89
请注意，此示例不需要我们使用数组的长度，也不需要我们索引数组！
让我们仔细看看这是如何工作的。这个基于范围的 for 循环将遍历
fibonacci
的所有元素。在第一次迭代中，变量
num
被赋予第一个元素的值 (
0
)。然后程序执行关联的语句，将
num
的值 (
0
) 打印到控制台。在第二次迭代中，
num
被赋予第二个元素的值 (
1
)。关联的语句再次执行，打印
1
。基于范围的 for 循环继续依次遍历每个数组元素，为每个元素执行关联的语句，直到数组中没有元素可迭代。此时，循环终止，程序继续执行（打印一个换行符，然后向操作系统返回
0
）。
关键见解
声明的元素（在前面的示例中为
num
）不是数组索引。相反，它被赋予正在迭代的数组元素的值。
因为
num
被赋予数组元素的值，这意味着数组元素被复制（这对于某些类型可能很昂贵）。
最佳实践
在遍历容器时，优先使用基于范围的 for 循环而不是常规 for 循环。
基于范围的 for 循环和空容器
在要遍历的容器没有元素的情况下，基于范围的 for 循环的主体将简单地不执行：
#include <iostream>
#include <vector>

int main()
{
    std::vector empty { };

    for (int num : empty)
       std::cout << "Hi mom!\n";

    return 0;
}
上面的示例没有打印任何内容。对不起，妈妈！
基于范围的 for 循环和使用
auto
关键字的类型推导
因为
element_declaration
应该与数组元素具有相同的类型（以防止发生类型转换），所以这是使用
auto
关键字并让编译器为我们推导数组元素类型的理想情况。这样我们就不必冗余地指定类型，并且没有意外输入错误（以及“误打字”，哈！）的风险。
这是与上面相同的示例，但使用
auto
作为
num
的类型：
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (auto num : fibonacci) // compiler will deduce type of num to be `int`
       std::cout << num << ' ';

    std::cout << '\n';

    return 0;
}
因为
std::vector fibonacci
的元素类型是
int
，所以
num
将被推导为
int
。
最佳实践
将类型推导 (
auto
) 与基于范围的 for 循环一起使用，让编译器推导数组元素的类型。
使用
auto
的另一个好处是，如果数组的元素类型发生更新（例如从
int
到
long
），
auto
将自动推导更新后的元素类型，确保它们保持同步（并防止发生类型转换）。
使用引用避免元素复制
考虑以下基于范围的 for 循环，它遍历
std::string
数组：
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" };

    for (auto word : words)
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
对于此循环的每次迭代，
words
数组中的下一个
std::string
元素将被分配（复制）到变量
word
中。复制
std::string
很昂贵，这就是我们通常通过 const 引用将
std::string
传递给函数的原因。除非我们确实需要复制，否则我们希望避免复制昂贵的东西。在这种情况下，我们只是打印复制的值，然后复制被销毁。如果我们可以避免复制并只引用实际的数组元素，那就更好了。
幸运的是，我们可以通过将
element_declaration
设为（const）引用来做到这一点：
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" };

    for (const auto& word : words) // word is now a const reference
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
在上面的示例中，
word
现在是 const 引用。在此循环的每次迭代中，
word
将绑定到下一个数组元素。这允许我们访问数组元素的值而无需进行昂贵的复制。
如果引用是非 const 的，它也可以用于更改数组中的值（如果我们的
element_declaration
是值的副本，则无法做到）。
何时使用
auto
vs
auto&
vs
const auto&
通常，对于易于复制的类型，我们使用
auto
；当我们想要修改元素时，使用
auto&
；对于复制成本高的类型，使用
const auto&
。但是对于基于范围的 for 循环，许多开发人员认为最好始终使用
const auto&
，因为它更具前瞻性。
例如，考虑以下示例：
#include <iostream>
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> words{ "peter", "likes", "frozen", "yogurt" }; // elements are type std::string_view

    for (auto word : words) // We normally pass string_view by value, so we'll use auto here
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
在此示例中，我们有一个包含
std::string_view
对象的
std::vector
。由于
std::string_view
通常通过值传递，因此使用
auto
似乎是合适的。
但考虑如果
words
后来更新为
std::string
数组而不是
std::string_view
数组会发生什么。
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" }; // obvious we should update this

    for (auto word : words) // Probably not obvious we should update this too
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
基于范围的 for 循环将正常编译和执行，但
word
现在将被推导为
std::string
，并且因为我们正在使用
auto
，我们的循环将静默地对
std::string
元素进行昂贵的复制。我们刚刚遭受了巨大的性能损失！
有几种合理的方法可以确保这种情况不会发生：
不要在基于范围的 for 循环中使用类型推导。如果我们将元素类型明确指定为
std::string_view
，那么当数组稍后更新为
std::string
时，
std::string
元素将隐式转换为
std::string_view
，这没有问题。如果数组更新为不可转换的其他类型，编译器将报错，我们可以在那时找出合适的处理方式。但如果元素类型是可转换的，那么编译器将静默执行转换，我们可能不会意识到我们正在做一些次优的事情。
当您不想处理副本时，在使用基于范围的 for 循环进行类型推导时，使用
const auto&
而不是
auto
。通过引用而不是通过值访问元素的性能损失可能很小，这可以防止如果元素类型稍后更改为复制成本高的类型，可能导致巨大的性能损失。
最佳实践
对于基于范围的 for 循环，最好将元素类型定义为：
auto
当您想要修改元素的副本时。
auto&
当您想要修改原始元素时。
const auto&
否则（当您只需要查看原始元素时）。
基于范围的 for 循环和其他标准容器类型
基于范围的 for 循环适用于各种数组类型，包括（未衰退的）C 风格数组、
std::array
、
std::vector
、链表、树和映射。我们还没有涵盖这些，所以如果您不知道这些是什么，请不要担心。请记住，
基于范围的 for
循环提供了一种灵活通用的方式来遍历不仅仅是
std::vector
。
#include <array>
#include <iostream>

int main()
{
    std::array fibonacci{ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 }; // note use of std::array here

    for (auto number : fibonacci)
    {
        std::cout << number << ' ';
    }

    std::cout << '\n';

    return 0;
}
致进阶读者
基于范围的 for 循环不适用于衰退的 C 风格数组。这是因为基于范围的 for 循环需要知道数组的长度才能知道遍历何时完成，而衰退的 C 风格数组不包含此信息。
基于范围的 for 循环也不适用于枚举。我们将在课程
17.6 -- std::array 和枚举
中展示一种解决此问题的方法。
获取当前元素的索引
基于范围的 for 循环不提供直接获取当前元素数组索引的方法。这是因为基于范围的 for 循环可以迭代的许多结构（例如
std::list
）不支持索引。
然而，由于基于范围的 for 循环始终向前迭代且不跳过元素，因此您始终可以声明（并递增）自己的计数器。但是，如果您要这样做，您应该考虑是使用普通 for 循环还是基于范围的 for 循环更好。
反向基于范围的 for 循环
C++20
基于范围的 for 循环只按正向顺序迭代。然而，在某些情况下，我们希望反向遍历数组。在 C++20 之前，基于范围的 for 循环不容易用于此目的，必须采用其他解决方案（通常是普通的 for 循环）。
然而，从 C++20 开始，您可以使用 Ranges 库的
std::views::reverse
功能来创建可以遍历的元素的反向视图：
#include <iostream>
#include <ranges> // C++20
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> words{ "Alex", "Bobby", "Chad", "Dave" }; // sorted in alphabetical order

    for (const auto& word : std::views::reverse(words)) // create a reverse view
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
这会打印
Dave
Chad
Bobby
Alex
我们还没有涵盖 Ranges 库，所以暂时将其视为一个有用的“魔法”。
小测验时间
问题 #1
定义一个包含以下名称的
std::vector
：“Alex”、“Betty”、“Caroline”、“Dave”、“Emily”、“Fred”、“Greg”和“Holly”。要求用户输入一个名称。使用基于范围的 for 循环查看用户输入的名称是否在数组中。
样本输出
Enter a name: Betty
Betty was found.
Enter a name: Megatron
Megatron was not found.
提示：使用
std::string
来保存用户输入的字符串。
提示：
std::string_view
复制成本很低。
显示答案
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> names{ "Alex", "Betty", "Caroline", "Dave",
        "Emily", "Fred", "Greg", "Holly" };
	
    std::cout << "Enter a name: ";
    std::string username{};
    std::cin >> username;

    bool found{ false };

    // We will be explicit about expecting `name` to be a std::string_view here
    // That way if `names` is ever changed to an expensive to copy type
    // (like std::string), we won't end up making expensive copies.
    for (std::string_view name : names)
    {
        if (name == username)
        {
            found = true;
            break;
        }
    }

    if (found)
        std::cout << username << " was found.\n";
    else
        std::cout << username << " was not found.\n";

    return 0;
}
问题 #2
修改您的测验 1 解决方案。在此版本中，创建一个名为
isValueInArray()
的函数模板（而不是普通函数），它接受两个参数：一个
std::vector
和一个值。如果该值在数组中，函数应返回
true
，否则返回
false
。从
main()
调用该函数，并将名称数组和用户输入的名称传递给它。
提醒
使用模板参数推导（当未显式指定模板类型参数时）的函数模板不会进行转换以匹配模板类型参数。调用要么匹配模板（并且可以推导出模板类型），要么不匹配。
具有显式指定模板类型参数的函数模板将转换参数以匹配参数类型（因为类型已知）。
显示答案
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

template <typename T>
bool isValueInArray(const std::vector<T>& arr, const T& value )
{
    // we'll use a reference since we don't know if T is expensive to copy
    for (const auto& a : arr)
    {
        if (a == value)
            return true;
    }

    return false;
}

int main()
{
    std::vector<std::string_view> names{ "Alex", "Betty", "Caroline", "Dave",
        "Emily", "Fred", "Greg", "Holly" };
	
    std::cout << "Enter a name: ";
    std::string username{};
    std::cin >> username;

    // By explicitly specifying std::string_view as a function template argument,
    // the compiler will implicitly convert username to `std::string_view` to match the parameter type.
    bool found{ isValueInArray<std::string_view>(names, username) };

    // The following is also okay.  If we rely on template argument deduction instead, the compiler 
    // won't do implicit conversions, so we need to make sure `username` has the expected type.
    // bool found{ isValueInArray(names, static_cast<std::string_view>(username)) };

    if (found)
        std::cout << username << " was found.\n";
    else
        std::cout << username << " was not found.\n";

    return 0;
}
下一课
16.9
使用枚举器进行数组索引和长度
返回目录
上一课
16.7
数组、循环和符号挑战解决方案