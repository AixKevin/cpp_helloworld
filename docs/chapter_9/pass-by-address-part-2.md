# 12.11 — 按地址传递（第 2 部分）

12.11 — 按地址传递（第 2 部分）
Alex
2022 年 1 月 18 日，上午 10:15 PST
2024 年 4 月 25 日
本课程是
12.10 -- 按地址传递
的延续。
“可选”参数的按地址传递
按地址传递的更常见用途之一是允许函数接受“可选”参数。这通过示例比描述更容易说明
#include <iostream>

void printIDNumber(const int *id=nullptr)
{
    if (id)
        std::cout << "Your ID number is " << *id << ".\n";
    else
        std::cout << "Your ID number is not known.\n";
}

int main()
{
    printIDNumber(); // we don't know the user's ID yet

    int userid { 34 };
    printIDNumber(&userid); // we know the user's ID now

    return 0;
}
此示例输出：
Your ID number is not known.
Your ID number is 34.
在这个程序中，`printIDNumber()` 函数有一个通过地址传递并默认值为 `nullptr` 的参数。在 `main()` 内部，我们调用这个函数两次。第一次调用时，我们不知道用户的 ID，所以我们不带参数调用 `printIDNumber()`。`id` 参数默认为 `nullptr`，函数打印 `Your ID number is not known.`。第二次调用时，我们现在有一个有效的 ID，所以我们调用 `printIDNumber(&userid)`。`id` 参数接收 `userid` 的地址，所以函数打印 `Your ID number is 34.`。
然而，在许多情况下，函数重载是实现相同结果的更好替代方案。
#include <iostream>

void printIDNumber()
{
    std::cout << "Your ID is not known\n";
}

void printIDNumber(int id)
{
    std::cout << "Your ID is " << id << "\n";
}

int main()
{
    printIDNumber(); // we don't know the user's ID yet

    int userid { 34 };
    printIDNumber(userid); // we know the user is 34

    printIDNumber(62); // now also works with rvalue arguments
    
    return 0;
}
这有许多优点：我们不再需要担心空解引用，并且我们可以将字面量或其他右值作为参数传递。
更改指针参数指向的内容
当我们向函数传递一个地址时，该地址会从实参复制到指针形参中（这很好，因为复制地址很快）。现在考虑下面的程序
#include <iostream>

// [[maybe_unused]] gets rid of compiler warnings about ptr2 being set but not used
void nullify([[maybe_unused]] int* ptr2) 
{
    ptr2 = nullptr; // Make the function parameter a null pointer
}

int main()
{
    int x{ 5 };
    int* ptr{ &x }; // ptr points to x

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");

    nullify(ptr);

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");
    return 0;
}
这个程序打印
ptr is non-null
ptr is non-null
如您所见，更改指针形参持有的地址对实参持有的地址没有影响（`ptr` 仍然指向 `x`）。当函数 `nullify()` 被调用时，`ptr2` 接收传入地址的副本（在本例中，是 `ptr` 持有的地址，即 `x` 的地址）。当函数更改 `ptr2` 指向的内容时，这只会影响 `ptr2` 持有的副本。
那么，如果我们想允许一个函数改变一个指针参数所指向的内容，该怎么办呢？
按地址传递……通过引用？
是的，这是存在的。就像我们可以通过引用传递普通变量一样，我们也可以通过引用传递指针。下面是将 `ptr2` 更改为地址引用后的相同程序。
#include <iostream>

void nullify(int*& refptr) // refptr is now a reference to a pointer
{
    refptr = nullptr; // Make the function parameter a null pointer
}

int main()
{
    int x{ 5 };
    int* ptr{ &x }; // ptr points to x

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");

    nullify(ptr);

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");
    return 0;
}
这个程序打印
ptr is non-null
ptr is null
因为 `refptr` 现在是一个指针的引用，当 `ptr` 作为参数传递时，`refptr` 被绑定到 `ptr`。这意味着对 `refptr` 的任何更改都会作用于 `ptr`。
题外话…
由于指针的引用相当不常见，因此很容易混淆语法（是 `int*&` 还是 `int&*`？）。好消息是，如果您做反了，编译器会报错，因为您不能拥有指向引用的指针（因为指针必须持有对象的地址，而引用不是对象）。然后您可以将其调换过来。
为什么不再首选使用 `0` 或 `NULL`（可选）
在本小节中，我们将解释为什么不再首选使用 `0` 或 `NULL`。
字面量 `0` 既可以解释为整数字面量，也可以解释为空指针字面量。在某些情况下，我们意图哪一个可能会含糊不清——在某些此类情况下，编译器可能会在我们意图另一个时假定我们意图一个——从而导致程序行为出现意想不到的后果。
预处理器宏 `NULL` 的定义并未由语言标准定义。它可以定义为 `0`、`0L`、`((void*)0)` 或其他完全不同的东西。
在
11.1 — 函数重载简介
一课中，我们讨论了函数可以重载（只要可以通过参数的数量或类型进行区分，多个函数可以同名）。编译器可以通过函数调用中传入的实参来确定您想要哪个重载函数。
使用 `0` 或 `NULL` 时，可能会导致问题
#include <iostream>
#include <cstddef> // for NULL

void print(int x) // this function accepts an integer
{
	std::cout << "print(int): " << x << '\n';
}

void print(int* ptr) // this function accepts an integer pointer
{
	std::cout << "print(int*): " << (ptr ? "non-null\n" : "null\n");
}

int main()
{
	int x{ 5 };
	int* ptr{ &x };

	print(ptr);  // always calls print(int*) because ptr has type int* (good)
	print(0);    // always calls print(int) because 0 is an integer literal (hopefully this is what we expected)

	print(NULL); // this statement could do any of the following:
	// call print(int) (Visual Studio does this)
	// call print(int*)
	// result in an ambiguous function call compilation error (gcc and Clang do this)

	print(nullptr); // always calls print(int*)

	return 0;
}
在作者的机器上（使用 Visual Studio），这会打印
print(int*): non-null
print(int): 0
print(int): 0
print(int*): null
当将整数值 `0` 作为参数传递时，编译器将优先选择 `print(int)` 而不是 `print(int*)`。当我们意图用空指针参数调用 `print(int*)` 时，这可能导致意想不到的结果。
在 `NULL` 定义为值 `0` 的情况下，`print(NULL)` 也会调用 `print(int)`，而不是您可能期望的空指针字面量调用的 `print(int*)`。在 `NULL` 未定义为 `0` 的情况下，可能会导致其他行为，例如调用 `print(int*)` 或编译错误。
使用 `nullptr` 消除了这种歧义（它将始终调用 `print(int*)`），因为 `nullptr` 只会匹配指针类型。
std::nullptr_t (可选)
由于 `nullptr` 在函数重载中可以与整数值区分开来，因此它必须具有不同的类型。那么 `nullptr` 是什么类型呢？答案是 `nullptr` 具有类型 `std::nullptr_t`（定义在头文件 `
` 中）。`std::nullptr_t` 只能存储一个值：`nullptr`！虽然这可能看起来有点傻，但在一种情况下它很有用。如果我们想编写一个只接受 `nullptr` 字面量参数的函数，我们可以将参数设置为 `std::nullptr_t`。
#include <iostream>
#include <cstddef> // for std::nullptr_t

void print(std::nullptr_t)
{
    std::cout << "in print(std::nullptr_t)\n";
}

void print(int*)
{
    std::cout << "in print(int*)\n";
}

int main()
{
    print(nullptr); // calls print(std::nullptr_t)

    int x { 5 };
    int* ptr { &x };

    print(ptr); // calls print(int*)

    ptr = nullptr;
    print(ptr); // calls print(int*) (since ptr has type int*)

    return 0;
}
在上面的例子中，函数调用 `print(nullptr)` 解析为函数 `print(std::nullptr_t)`，而不是 `print(int*)`，因为它不需要类型转换。
唯一可能有点令人困惑的情况是当我们调用 `print(ptr)` 而 `ptr` 存储着 `nullptr` 值时。请记住，函数重载是根据类型而不是值进行匹配的，而 `ptr` 的类型是 `int*`。因此，`print(int*)` 将被匹配。在这种情况下，`print(std::nullptr_t)` 甚至没有被考虑，因为指针类型不会隐式转换为 `std::nullptr_t`。
您可能永远不需要使用这个，但以防万一，了解它还是好的。
只有按值传递
既然您已经了解了按引用、按地址和按值传递的基本区别，让我们暂时简化一下。:)
虽然编译器通常可以完全优化掉引用，但在某些情况下这是不可能的，并且实际上需要引用。引用通常由编译器使用指针实现。这意味着在幕后，按引用传递本质上只是按地址传递。
在上一课中，我们提到按地址传递只是将地址从调用方复制到被调用函数——这只是按值传递地址。
因此，我们可以得出结论，C++ 实际上一切都是按值传递的！按地址传递（和引用）的特性仅仅来自于我们可以解引用传递的地址来改变参数，而对于普通的值参数我们不能这样做！
下一课
12.12
按引用返回和按地址返回
返回目录
上一课
12.10
按地址传递