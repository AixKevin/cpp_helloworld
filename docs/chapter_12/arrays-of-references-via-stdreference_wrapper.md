# 17.5 — 通过 std::reference_wrapper 实现引用数组

17.5 — 通过 std::reference_wrapper 实现引用数组
Alex
2023年9月11日，太平洋夏令时下午3:50
2023年10月14日
在上一课中，我们提到数组可以包含任何对象类型的元素。这包括基本类型（例如 int）和复合类型（例如指向 int 的指针）的对象。
#include <array>
#include <iostream>
#include <vector>

int main()
{
    int x { 1 };
    int y { 2 };

    [[maybe_unused]] std::array valarr { x, y };   // an array of int values
    [[maybe_unused]] std::vector ptrarr { &x, &y }; // a vector of int pointers
    
    return 0;
}
然而，由于引用不是对象，所以你不能创建引用数组。数组的元素也必须是可赋值的，而引用不能被重新指定目标。
#include <array>
#include <iostream>

int main()
{
    int x { 1 };
    int y { 2 };

    [[maybe_unused]] std::array<int&, 2> refarr { x, y }; // compile error: cannot define array of references

    int& ref1 { x };
    int& ref2 { y };
    [[maybe_unused]] std::array valarr { ref1, ref2 }; // ok: this is actually a std::array<int, 2>, not an array of references

    return 0;
}
在本课中，我们将在示例中使用
std::array
，但这同样适用于所有数组类型。
但是，如果你想要一个引用数组，有一个变通方法。
std::reference_wrapper
std::reference_wrapper
是一个标准库类模板，位于
头文件中。它接受一个类型模板参数 T，然后表现得像一个可修改的 T 的左值引用。
关于
std::reference_wrapper
有几点值得注意：
Operator=
将重新指定
std::reference_wrapper
的目标（改变它引用的对象）。
std::reference_wrapper
将隐式转换为
T&
。
get()
成员函数可用于获取
T&
。当我们想要更新被引用对象的值时，这非常有用。
这是一个简单的例子
#include <array>
#include <functional> // for std::reference_wrapper
#include <iostream>

int main()
{
    int x { 1 };
    int y { 2 };
    int z { 3 };

    std::array<std::reference_wrapper<int>, 3> arr { x, y, z };
    
    arr[1].get() = 5; // modify the object in array element 1

    std::cout << arr[1] << y << '\n'; // show that we modified arr[1] and y, prints 55
    
    return 0;
}
这个例子打印出以下内容
55
请注意，我们必须使用
arr[1].get() = 5
而不是
arr[1] = 5
。后者是模糊的，因为编译器无法判断我们是打算将
std::reference_wrapper
重新指定为值 5（无论如何这都是非法的）还是更改被引用的值。使用
get()
可以消除这种歧义。
当打印
arr[1]
时，编译器会意识到它无法打印
std::reference_wrapper
，所以它会将其隐式转换为
int&
，而
int&
是可以打印的。所以我们在这里不需要使用
get()
。
std::ref
和
std::cref
在 C++17 之前，CTAD（类模板参数推导）不存在，所以类类型的所有模板参数都需要明确列出。因此，要创建一个
std::reference_wrapper
，你可以这样做：
int x { 5 };

    std::reference_wrapper<int> ref1 { x };        // C++11
    auto ref2 { std::reference_wrapper<int>{ x }}; // C++11
冗长的名称加上必须明确列出模板参数，创建许多这样的引用包装器可能很麻烦。
为了简化操作，提供了
std::ref()
和
std::cref()
函数作为快捷方式，用于创建
std::reference_wrapper
和
const std::reference_wrapper
包装的对象。请注意，这些函数可以与
auto
一起使用，以避免不得不显式指定模板参数。
int x { 5 };
    auto ref { std::ref(x) };   // C++11, deduces to std::reference_wrapper<int>
    auto cref { std::cref(x) }; // C++11, deduces to std::reference_wrapper<const int>
当然，现在 C++17 中有了 CTAD，我们也可以这样做
std::reference_wrapper ref1 { x };        // C++17
    auto ref2 { std::reference_wrapper{ x }}; // C++17
但由于
std::ref()
和
std::cref()
输入更短，它们仍然被广泛用于创建
std::reference_wrapper
对象。
下一课
17.6
std::array 和枚举
返回目录
上一课
17.4
类类型的 std::array 和花括号省略