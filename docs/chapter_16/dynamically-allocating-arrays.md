# 19.2 — 动态分配数组

19.2 — 动态分配数组
Alex
2015 年 8 月 18 日，太平洋夏令时下午 1:52
2023 年 11 月 20 日
除了动态分配单个值，我们还可以动态分配变量数组。与固定大小数组（数组大小必须在编译时固定）不同，动态分配数组允许我们在运行时选择数组长度（这意味着我们的长度不需要是 constexpr）。
作者注
在这些课程中，我们将动态分配 C 风格数组，这是最常见的动态分配数组类型。
虽然您可以动态分配 `std::array`，但在这种情况下，通常最好使用非动态分配的 `std::vector`。
要动态分配数组，我们使用 new 和 delete 的数组形式（通常称为 new[] 和 delete[]）
#include <cstddef>
#include <iostream>

int main()
{
    std::cout << "Enter a positive integer: ";
    std::size_t length{};
    std::cin >> length;

    int* array{ new int[length]{} }; // use array new.  Note that length does not need to be constant!

    std::cout << "I just allocated an array of integers of length " << length << '\n';

    array[0] = 5; // set element 0 to value 5

    delete[] array; // use array delete to deallocate array

    // we don't need to set array to nullptr/0 here because it's going out of scope immediately after this anyway

    return 0;
}
因为我们正在分配一个数组，C++ 知道它应该使用 new 的数组版本而不是 new 的标量版本。本质上，即使 [] 没有放在 new 关键字旁边，也会调用 new[] 运算符。
动态分配数组的长度类型为 `std::size_t`。如果您使用非 constexpr int，则需要 `static_cast` 到 `std::size_t`，因为这被认为是窄化转换，否则您的编译器会发出警告。
请注意，由于此内存是从与固定数组使用的内存不同的位置分配的，因此数组的大小可以非常大。您可以运行上面的程序并分配一个长度为 1,000,000（甚至可能 100,000,000）的数组而不会出现问题。试试看！因此，需要在 C++ 中分配大量内存的程序通常会动态分配。
动态删除数组
删除动态分配的数组时，我们必须使用 delete 的数组版本，即 delete[]。
这告诉 CPU 需要清理多个变量而不是单个变量。新程序员在处理动态内存分配时最常见的错误之一是删除动态分配的数组时使用 delete 而不是 delete[]。对数组使用 delete 的标量版本将导致未定义行为，例如数据损坏、内存泄漏、崩溃或其他问题。
关于 array delete[]，一个经常被问到的问题是：“array delete 如何知道要删除多少内存？” 答案是 array new[] 会跟踪为变量分配了多少内存，以便 array delete[] 可以删除正确的数量。不幸的是，这个大小/长度对程序员来说是不可访问的。
动态数组几乎与固定数组相同
在
第 17.8 课 -- C 风格数组衰减
中，您了解到固定数组保存了第一个数组元素的内存地址。您还了解到固定数组可以衰减为指向数组第一个元素的指针。在这种衰减形式中，固定数组的长度不可用（因此也无法通过 sizeof() 获取数组大小），但除此之外几乎没有区别。
动态数组最初是一个指向数组第一个元素的指针。因此，它具有相同的限制，即它不知道自己的长度或大小。动态数组的功能与衰减的固定数组相同，只是程序员需要通过 delete[] 关键字负责释放动态数组。
初始化动态分配数组
如果您想将动态分配的数组初始化为 0，语法非常简单
int* array{ new int[length]{} };
在 C++11 之前，没有简单的方法将动态数组初始化为非零值（初始化列表只适用于固定数组）。这意味着您必须遍历数组并显式分配元素值。
int* array = new int[5];
array[0] = 9;
array[1] = 7;
array[2] = 5;
array[3] = 3;
array[4] = 1;
超级烦人！
但是，从 C++11 开始，现在可以使用初始化列表初始化动态数组！
int fixedArray[5] = { 9, 7, 5, 3, 1 }; // initialize a fixed array before C++11
int* array{ new int[5]{ 9, 7, 5, 3, 1 } }; // initialize a dynamic array since C++11
// To prevent writing the type twice, we can use auto. This is often done for types with long names.
auto* array{ new int[5]{ 9, 7, 5, 3, 1 } };
请注意，此语法在数组长度和初始化列表之间没有 operator=。
为了一致性，固定数组也可以使用统一初始化进行初始化
int fixedArray[]{ 9, 7, 5, 3, 1 }; // initialize a fixed array in C++11
char fixedArray[]{ "Hello, world!" }; // initialize a fixed array in C++11
显式声明数组大小是可选的。
调整数组大小
动态分配数组允许您在分配时设置数组长度。但是，C++ 不提供内置方法来调整已分配数组的大小。可以通过动态分配新数组、复制元素和删除旧数组来解决此限制。但是，这容易出错，特别是当元素类型是类时（它们有关于如何创建的特殊规则）。
因此，我们建议您避免自己这样做。请改用 `std::vector`。
小测验时间
问题 #1
编写一个程序，该程序
询问用户希望输入多少个名称。
动态分配一个 `std::string` 数组。
要求用户输入每个名称。
调用 `std::sort` 对名称进行排序（请参阅
18.1 -- 使用选择排序对数组进行排序
和
17.9 -- 指针算术和下标
）
打印排序后的名称列表。
`std::string` 支持通过比较运算符 < 和 > 比较字符串。您无需手动实现字符串比较。
您的输出应与此匹配
How many names would you like to enter? 5
Enter name #1: Jason
Enter name #2: Mark
Enter name #3: Alex
Enter name #4: Chris
Enter name #5: John

Here is your sorted list:
Name #1: Alex
Name #2: Chris
Name #3: Jason
Name #4: John
Name #5: Mark
提醒
您可以使用 `std::getline()` 读取包含空格的名称（请参阅
第 5.7 课 -- std::string 简介
）。
提醒
要将 `std::sort()` 与指向数组的指针一起使用，请手动计算 begin 和 end
std::sort(array, array + arrayLength);
显示答案
#include <algorithm> // std::sort
#include <cstddef>
#include <iostream>
#include <string>

std::size_t getNameCount()
{
    std::cout << "How many names would you like to enter? ";
    std::size_t length{};
    std::cin >> length;

    return length;
}

// Asks user to enter all the names
void getNames(std::string* names, std::size_t length)
{
    for (std::size_t i{ 0 }; i < length; ++i)
    {
        std::cout << "Enter name #" << i + 1 << ": ";
        std::getline(std::cin >> std::ws, names[i]);
    }
}

// Prints the sorted names
void printNames(std::string* names, std::size_t length)
{
    std::cout << "\nHere is your sorted list:\n";

    for (std::size_t i{ 0 }; i < length; ++i)
        std::cout << "Name #" << i + 1 << ": " << names[i] << '\n';
}

int main()
{
    std::size_t length{ getNameCount() };

    // Allocate an array to hold the names
    auto* names{ new std::string[length]{} };

    getNames(names, length);

    // Sort the array
    std::sort(names, names + length);

    printNames(names, length);

    // don't forget to use array delete
    delete[] names;
    // we don't need to set names to nullptr/0 here because it's going to go out
    // of scope immediately after this anyway.

    return 0;
}
下一课
19.3
析构函数
返回目录
上一课
19.1
使用 new 和 delete 进行动态内存分配