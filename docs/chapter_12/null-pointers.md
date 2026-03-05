# 12.8 — 空指针

12.8 — 空指针
Alex
2015年8月12日，太平洋夏令时下午12:53
2025年2月5日
在上一课（
12.7 -- 指针简介
）中，我们介绍了指针的基础知识，指针是保存另一个对象地址的对象。可以使用解引用运算符 (*) 解引用此地址以获取该地址处的对象
#include <iostream>

int main()
{
    int x{ 5 };
    std::cout << x << '\n'; // print the value of variable x

    int* ptr{ &x }; // ptr holds the address of x
    std::cout << *ptr << '\n'; // use dereference operator to print the value of the object at the address that ptr is holding (which is x's address)

    return 0;
}
上面的例子打印：
5
5
在上一课中，我们还提到指针不需要指向任何东西。在本课中，我们将进一步探讨此类指针（以及指向空值的各种含义）。
空指针
除了内存地址之外，指针还可以保存一个额外的值：空值。
空值
（通常缩写为
空
）是一个特殊值，表示某个东西没有值。当指针持有空值时，意味着该指针不指向任何东西。这样的指针称为
空指针
。
创建空指针最简单的方法是使用值初始化
int main()
{
    int* ptr {}; // ptr is now a null pointer, and is not holding an address
 
    return 0;
}
最佳实践
如果您没有用有效对象的地址初始化您的指针，请对其进行值初始化（使其成为空指针）。
因为我们可以使用赋值来改变指针指向的内容，所以最初设置为空的指针以后可以更改为指向有效对象
#include <iostream>

int main()
{
    int* ptr {}; // ptr is a null pointer, and is not holding an address

    int x { 5 };
    ptr = &x; // ptr now pointing at object x (no longer a null pointer)

    std::cout << *ptr << '\n'; // print value of x through dereferenced ptr
 
    return 0;
}
nullptr 关键字
与关键字
true
和
false
表示布尔字面值一样，
nullptr
关键字表示空指针字面值。我们可以使用
nullptr
来显式初始化或赋值指针为空值。
int main()
{
    int* ptr { nullptr }; // can use nullptr to initialize a pointer to be a null pointer

    int value { 5 };
    int* ptr2 { &value }; // ptr2 is a valid pointer
    ptr2 = nullptr; // Can assign nullptr to make the pointer a null pointer

    someFunction(nullptr); // we can also pass nullptr to a function that has a pointer parameter

    return 0;
}
在上面的示例中，我们使用赋值将
ptr2
的值设置为
nullptr
，使
ptr2
成为空指针。
最佳实践
当您需要空指针字面值进行初始化、赋值或将空指针传递给函数时，请使用
nullptr
。
解引用空指针会导致未定义行为
就像解引用悬空（或野）指针会导致未定义行为一样，解引用空指针也会导致未定义行为。在大多数情况下，它会使您的应用程序崩溃。
以下程序演示了这一点，当您运行它时，它可能会崩溃或异常终止您的应用程序（来吧，试试吧，它不会损害您的机器）
#include <iostream>

int main()
{
    int* ptr {}; // Create a null pointer
    std::cout << *ptr << '\n'; // Dereference the null pointer

    return 0;
}
从概念上讲，这很有意义。解引用指针意味着“转到指针指向的地址并访问那里的值”。空指针持有空值，这在语义上意味着指针不指向任何东西。那么它会访问什么值呢？
意外解引用空指针和悬空指针是 C++ 程序员最常见的错误之一，并且可能是 C++ 程序在实践中崩溃的最常见原因。
警告
无论何时使用指针，您都需要格外小心，确保您的代码没有解引用空指针或悬空指针，因为这会导致未定义行为（可能是应用程序崩溃）。
检查空指针
就像我们可以使用条件来测试布尔值为
true
或
false
一样，我们可以使用条件来测试指针的值是否为
nullptr
#include <iostream>

int main()
{
    int x { 5 };
    int* ptr { &x };

    if (ptr == nullptr) // explicit test for equivalence
        std::cout << "ptr is null\n";
    else
        std::cout << "ptr is non-null\n";

    int* nullPtr {};
    std::cout << "nullPtr is " << (nullPtr==nullptr ? "null\n" : "non-null\n"); // explicit test for equivalence

    return 0;
}
上面的程序打印
ptr is non-null
nullPtr is null
在课程
4.9 -- 布尔值
中，我们注意到整数值将隐式转换为布尔值：整数值
0
转换为布尔值
false
，任何其他整数值转换为布尔值
true
。
类似地，指针也会隐式转换为布尔值：空指针转换为布尔值
false
，非空指针转换为布尔值
true
。这使我们能够跳过显式测试
nullptr
，而只使用隐式转换为布尔值来测试指针是否为空指针。以下程序与前一个程序等效
#include <iostream>

int main()
{
    int x { 5 };
    int* ptr { &x };

    // pointers convert to Boolean false if they are null, and Boolean true if they are non-null
    if (ptr) // implicit conversion to Boolean
        std::cout << "ptr is non-null\n";
    else
        std::cout << "ptr is null\n";

    int* nullPtr {};
    std::cout << "nullPtr is " << (nullPtr ? "non-null\n" : "null\n"); // implicit conversion to Boolean

    return 0;
}
警告
条件只能用于区分空指针和非空指针。没有方便的方法可以确定非空指针是否指向有效对象或悬空（指向无效对象）。
使用 nullptr 避免悬空指针
上面我们提到，解引用为空或悬空的指针会导致未定义行为。因此，我们需要确保我们的代码不做这些事情。
我们可以通过使用条件来确保指针在尝试解引用之前是非空的，从而轻松避免解引用空指针
// Assume ptr is some pointer that may or may not be a null pointer
if (ptr) // if ptr is not a null pointer
    std::cout << *ptr << '\n'; // okay to dereference
else
    // do something else that doesn't involve dereferencing ptr (print an error message, do nothing at all, etc...)
但是悬空指针呢？因为没有办法检测指针是否悬空，所以我们首先需要避免程序中出现任何悬空指针。我们通过确保任何不指向有效对象的指针都设置为
nullptr
来做到这一点。
这样，在解引用指针之前，我们只需要测试它是否为空——如果它非空，我们假设指针没有悬空。
最佳实践
指针应要么保存有效对象的地址，要么设置为 nullptr。这样我们只需要测试指针是否为空，并且可以假设任何非空指针都是有效的。
不幸的是，避免悬空指针并不总是那么容易：当对象被销毁时，指向该对象的任何指针都将悬空。此类指针
不会
自动置空！程序员有责任确保所有指向刚刚销毁的对象的指针都正确设置为
nullptr
。
警告
当对象被销毁时，指向被销毁对象的任何指针都将悬空（它们不会自动设置为
nullptr
）。您有责任检测这些情况并确保随后将这些指针设置为
nullptr
。
遗留空指针字面值：0 和 NULL
在旧代码中，您可能会看到另外两个字面值而不是
nullptr
。
第一个是字面值
0
。在指针的上下文中，字面值
0
被特别定义为空值，并且是唯一可以将整数字面值赋值给指针的情况。
int main()
{
    float* ptr { 0 };  // ptr is now a null pointer (for example only, don't do this)

    float* ptr2; // ptr2 is uninitialized
    ptr2 = 0; // ptr2 is now a null pointer (for example only, don't do this)

    return 0;
}
题外话…
在现代架构上，地址
0
通常用于表示空指针。但是，C++ 标准不保证此值，并且某些架构使用其他值。字面值
0
，当在空指针上下文中使用时，将转换为架构用于表示空指针的任何地址。
此外，还有一个名为
NULL
的预处理器宏（在
头文件中定义）。此宏继承自 C，在 C 中通常用于指示空指针。
#include <cstddef> // for NULL

int main()
{
    double* ptr { NULL }; // ptr is a null pointer

    double* ptr2; // ptr2 is uninitialized
    ptr2 = NULL; // ptr2 is now a null pointer

    return 0;
}
在现代 C++ 中应避免使用
0
和
NULL
（改用
nullptr
）。我们在课程
12.11 -- 按地址传递（第2部分）
中讨论了原因。
尽可能优先使用引用而不是指针
指针和引用都使我们能够间接访问其他对象。
指针具有能够改变它们所指向的对象以及指向空值的附加能力。然而，这些指针能力也固有地危险：空指针有被解引用的风险，而改变指针所指向对象的能力会使创建悬空指针更容易
int main()
{
    int* ptr { };
    
    {
        int x{ 5 };
        ptr = &x; // assign the pointer to an object that will be destroyed (not possible with a reference)
    } // ptr is now dangling and pointing to invalid object

    if (ptr) // condition evaluates to true because ptr is not nullptr
        std::cout << *ptr; // undefined behavior

    return 0;
}
由于引用不能绑定到空，我们不必担心空引用。而且由于引用在创建时必须绑定到有效对象，并且之后不能重新绑定，因此创建悬空引用更困难。
由于引用更安全，因此应优先使用引用而不是指针，除非需要指针提供的附加功能。
最佳实践
除非需要指针提供的附加功能，否则优先使用引用而不是指针。
一个笑话
你听说过空指针的笑话吗？
没关系，你不会解引用它。
小测验时间
问题 #1
1a) 我们能否确定指针是否为空指针？如果能，怎么确定？
显示答案
是的，我们可以对指针使用条件（if 语句或条件运算符）。如果指针为空指针，则转换为布尔值
false
，否则转换为
true
。
1b) 我们能否确定非空指针是有效的还是悬空的？如果能，怎么确定？
显示答案
没有简单的方法可以确定这一点。
问题 #2
对于每个子项，回答所描述的操作是否会导致：可预测、未定义或可能未定义的行为。如果答案是“可能未定义”，请澄清何时。
假设提到的任何对象都是指针可以指向的类型。
2a) 将对象的地址赋值给非 const 指针
显示答案
可预测。这只是将地址复制到指针对象中。
2b) 将 nullptr 赋值给指针
显示答案
可预测。
2c) 解引用指向有效对象的指针
显示答案
可预测。
2d) 解引用悬空指针
显示答案
未定义。
2e) 解引用空指针
显示答案
未定义。
2f) 解引用非空指针
显示答案
可能未定义，如果指针是悬空的。
问题 #3
为什么我们应该将不指向有效对象的指针设置为“nullptr”？
显示答案
我们无法确定非空指针是有效的还是悬空的，访问悬空指针将导致未定义行为。因此，我们需要确保我们的程序中没有任何悬空指针。
如果我们确保所有指针都指向有效对象或设置为
nullptr
，那么我们可以使用条件来测试空值，以确保我们不解引用空指针，并假设所有非空指针都指向有效对象。
下一课
12.9
指针与 const
返回目录
上一课
12.7
指针简介