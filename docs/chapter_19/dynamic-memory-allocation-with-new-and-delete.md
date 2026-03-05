# 19.1 — 使用 new 和 delete 进行动态内存分配

19.1 — 使用 new 和 delete 进行动态内存分配
Alex
2007 年 7 月 13 日下午 5:24 PDT
2025 年 1 月 1 日
动态内存分配的必要性
C++ 支持三种基本的内存分配类型，其中您已经了解了两种。
静态内存分配
发生于静态变量和全局变量。这些类型的变量的内存会在程序运行时分配一次，并在程序的整个生命周期内持续存在。
自动内存分配
发生于函数参数和局部变量。这些类型的变量的内存会在进入相关代码块时分配，并在退出代码块时释放，可根据需要多次进行。
动态内存分配
是本文的主题。
静态分配和自动分配都有两个共同点
变量/数组的大小必须在编译时已知。
内存的分配和释放是自动发生的（当变量被实例化/销毁时）。
大多数情况下，这都很好。然而，您会遇到一些情况，其中一个或两个约束会引起问题，通常是在处理外部（用户或文件）输入时。
例如，我们可能想用一个字符串来保存某人的名字，但我们不知道他们的名字有多长，直到他们输入。或者我们可能想从磁盘读取一些记录，但我们事先不知道有多少记录。或者我们可能正在创建一个游戏，其中有可变数量的怪物（随着一些怪物死亡和新怪物生成而变化）试图杀死玩家。
如果所有内容的大小都必须在编译时声明，我们能做的最好就是猜测我们需要的变量的最大大小，并希望这足够了。
char name[25]; // let's hope their name is less than 25 chars!
Record record[500]; // let's hope there are less than 500 records!
Monster monster[40]; // 40 monsters maximum
Polygon rendering[30000]; // this 3d rendering better not have more than 30,000 polygons!
这至少有四个原因是一个糟糕的解决方案
首先，如果变量没有实际使用，会导致内存浪费。例如，如果我们为每个名字分配 25 个字符，但名字平均只有 12 个字符长，那么我们使用的内存量是我们实际所需的两倍多。或者考虑上面提到的渲染数组：如果一个渲染只使用 10,000 个多边形，那么我们就有 20,000 个多边形的内存没有被使用！
其次，我们如何判断内存的哪些部分实际被使用了？对于字符串，很简单：以 \0 开头的字符串显然没有被使用。但是 monster[24] 呢？它现在是活的还是死的？它甚至一开始有没有被初始化？这就需要某种方式来判断每个怪物的状态，这增加了复杂性并可能占用额外的内存。
第三，大多数普通变量（包括固定大小的数组）都分配在内存中称为
栈
的部分。程序的栈内存量通常很小——Visual Studio 默认栈大小为 1MB。如果超过此数字，将导致栈溢出，操作系统可能会关闭程序。
在 Visual Studio 上，运行此程序时您可以看到这种情况发生
int main()
{
    int array[1000000]; // allocate 1 million integers (probably 4MB of memory)
}
仅限于 1MB 内存对于许多程序来说都会有问题，尤其是那些处理图形的程序。
第四，也是最重要的一点，它可能导致人为限制和/或数组溢出。当用户尝试从磁盘读取 600 条记录，但我们只分配了最多 500 条记录的内存时，会发生什么？要么我们必须给用户一个错误，只读取 500 条记录，或者（在最糟糕的情况下，我们根本不处理这种情况）记录数组溢出，然后发生一些糟糕的事情。
幸运的是，这些问题可以通过动态内存分配轻松解决。
动态内存分配
是运行中的程序在需要时向操作系统请求内存的一种方式。这部分内存不是来自程序的有限栈内存——相反，它是从操作系统管理的一个更大的内存池中分配的，这个池叫做
堆
。在现代机器上，堆的大小可以是千兆字节。
动态分配单个变量
要动态分配
单个
变量，我们使用
new
运算符的标量（非数组）形式
new int; // dynamically allocate an integer (and discard the result)
在上述情况下，我们向操作系统请求一个整数大小的内存。new 运算符使用该内存创建对象，然后返回一个包含已分配内存
地址
的指针。
通常，我们会将返回值分配给自己的指针变量，以便以后可以访问已分配的内存。
int* ptr{ new int }; // dynamically allocate an integer and assign the address to ptr so we can access it later
然后我们可以解引用指针来访问内存
*ptr = 7; // assign value of 7 to allocated memory
如果之前不清楚，现在至少应该清楚指针在什么情况下是有用的。如果没有指针来保存刚分配的内存的地址，我们就无法访问为我们刚分配的内存！
请注意，访问堆分配的对象通常比访问栈分配的对象慢。因为编译器知道栈分配对象的地址，它可以直接转到该地址获取值。堆分配的对象通常通过指针访问。这需要两个步骤：一个获取对象的地址（来自指针），另一个获取值。
动态内存分配是如何工作的？
您的计算机有可供应用程序使用的内存（可能很多）。当您运行应用程序时，您的操作系统会将应用程序加载到部分内存中。您的应用程序使用的这部分内存被划分为不同的区域，每个区域都有不同的用途。一个区域包含您的代码。另一个区域用于正常操作（跟踪调用了哪些函数、创建和销毁全局和局部变量等）。我们稍后会详细讨论这些。然而，大部分可用内存只是在那里等待被分配给请求它的程序。
当您动态分配内存时，您是在请求操作系统为您的程序预留一部分内存。如果它能满足此请求，它将返回该内存的地址给您的应用程序。从那时起，您的应用程序可以随意使用该内存。当您的应用程序使用完内存后，它可以将内存返回给操作系统，以便分配给其他程序。
与静态或自动内存不同，程序本身负责请求和处置动态分配的内存。
关键见解
栈对象的分配和释放是自动完成的。我们不需要处理内存地址——编译器编写的代码可以为我们完成。
堆对象的分配和释放不是自动完成的。我们需要参与。这意味着我们需要一种明确的方式来引用特定的堆分配对象，以便在准备好时请求销毁它。我们引用这些对象的方式是通过内存地址。
当我们使用运算符 new 时，它会返回一个包含新分配对象的内存地址的指针。我们通常希望将其存储在一个指针中，以便以后可以使用该地址来访问对象（并最终请求其销毁）。
初始化动态分配的变量
动态分配变量时，您也可以通过直接初始化或统一初始化来初始化它
int* ptr1{ new int (5) }; // use direct initialization
int* ptr2{ new int { 6 } }; // use uniform initialization
删除单个变量
当我们完成一个动态分配的变量时，我们需要明确告诉 C++ 释放内存以供重用。对于单个变量，这是通过
delete
运算符的标量（非数组）形式完成的。
// assume ptr has previously been allocated with operator new
delete ptr; // return the memory pointed to by ptr to the operating system
ptr = nullptr; // set ptr to be a null pointer
删除内存意味着什么？
delete 运算符并没有
实际
删除任何东西。它只是将被指向的内存返回给操作系统。然后，操作系统可以自由地将该内存重新分配给另一个应用程序（或稍后再次分配给此应用程序）。
尽管语法看起来像是我们在删除一个
变量
，但事实并非如此！指针变量仍然具有与以前相同的范围，并且可以像任何其他变量一样被赋一个新值（例如 `nullptr`）。
请注意，删除不指向动态分配内存的指针可能会导致不良后果。
悬空指针
C++ 不对已释放内存的内容或被删除指针的值做出任何保证。在大多数情况下，返回给操作系统的内存将包含与返回前相同的值，并且指针将继续指向现在已释放的内存。
指向已释放内存的指针称为
悬空指针
。解引用或删除悬空指针将导致未定义行为。考虑以下程序
#include <iostream>

int main()
{
    int* ptr{ new int }; // dynamically allocate an integer
    *ptr = 7; // put a value in that memory location

    delete ptr; // return the memory to the operating system.  ptr is now a dangling pointer.

    std::cout << *ptr; // Dereferencing a dangling pointer will cause undefined behavior
    delete ptr; // trying to deallocate the memory again will also lead to undefined behavior.

    return 0;
}
在上面的程序中，先前分配给内存的值 7 可能仍然存在，但该内存地址的值也可能已经改变。内存也可能被分配给另一个应用程序（或用于操作系统的自身用途），并且尝试访问该内存将导致操作系统关闭程序。
解除分配内存可能会创建多个悬空指针。请考虑以下示例：
#include <iostream>

int main()
{
    int* ptr{ new int{} }; // dynamically allocate an integer
    int* otherPtr{ ptr }; // otherPtr is now pointed at that same memory location

    delete ptr; // return the memory to the operating system.  ptr and otherPtr are now dangling pointers.
    ptr = nullptr; // ptr is now a nullptr

    // however, otherPtr is still a dangling pointer!

    return 0;
}
这里有几项最佳实践可以提供帮助。
首先，尽量避免让多个指针指向同一块动态内存。如果无法避免，请明确哪个指针“拥有”该内存（并负责删除它），以及哪些指针只是访问它。
其次，当你删除一个指针时，如果该指针没有立即超出作用域，请将该指针设置为 nullptr。我们稍后会详细讨论空指针以及它们为什么有用。
最佳实践
将已删除的指针设置为 nullptr，除非它们会立即超出作用域。
运算符 new 可能会失败
向操作系统请求内存时，在极少数情况下，操作系统可能没有内存来满足该请求。
默认情况下，如果 new 失败，则会抛出 `bad_alloc` 异常。如果此异常未正确处理（并且不会，因为我们尚未涵盖异常或异常处理），程序将简单地因未处理的异常错误而终止（崩溃）。
在许多情况下，new 抛出异常（或您的程序崩溃）是不可取的，因此 new 还有另一种形式，可以用来告诉 new 在无法分配内存时返回一个空指针。这可以通过在 new 关键字和分配类型之间添加常量 `std::nothrow` 来实现。
int* value { new (std::nothrow) int }; // value will be set to a null pointer if the integer allocation fails
在上面的例子中，如果 new 无法分配内存，它将返回一个空指针而不是已分配内存的地址。
请注意，如果您随后尝试解引用此指针，将导致未定义行为（最有可能的是，您的程序会崩溃）。因此，最佳实践是在使用分配的内存之前，检查所有内存请求以确保它们确实成功。
int* value { new (std::nothrow) int{} }; // ask for an integer's worth of memory
if (!value) // handle case where new returned null
{
    // Do error handling here
    std::cerr << "Could not allocate memory\n";
}
因为向 new 请求内存很少失败（在开发环境中几乎从不失败），所以很容易忘记进行此检查！
空指针与动态内存分配
空指针（设置为 nullptr 的指针）在处理动态内存分配时特别有用。在动态内存分配的上下文中，空指针基本表示“此指针未分配内存”。这允许我们进行有条件地分配内存等操作。
// If ptr isn't already allocated, allocate it
if (!ptr)
    ptr = new int;
删除空指针没有任何效果。因此，没有必要进行以下操作
if (ptr) // if ptr is not a null pointer
    delete ptr; // delete it
// otherwise do nothing
相反，你可以直接写
delete ptr;
如果 `ptr` 非空，则动态分配的内存将被删除。如果 `ptr` 为空，则不会发生任何事情。
最佳实践
删除空指针是允许的，并且没有任何效果。不需要对您的删除语句进行条件判断。
内存泄漏
动态分配的内存会一直保持分配状态，直到它被显式释放或程序结束（操作系统会清理它，前提是您的操作系统支持此功能）。然而，用于保存动态分配内存地址的指针遵循局部变量的正常作用域规则。这种不匹配会带来有趣的问题。
考虑以下函数
void doSomething()
{
    int* ptr{ new int{} };
}
此函数动态分配一个整数，但从不使用 delete 释放它。因为指针变量只是普通变量，当函数结束时，ptr 将超出作用域。并且因为 ptr 是唯一持有动态分配整数地址的变量，当 ptr 被销毁时，不再有对动态分配内存的引用。这意味着程序现在“丢失”了动态分配内存的地址。结果，这个动态分配的整数无法被删除。
这称为
内存泄漏
。当您的程序在将一部分动态分配的内存返回给操作系统之前丢失了它的地址时，就会发生内存泄漏。发生这种情况时，您的程序无法删除动态分配的内存，因为它不再知道它在哪里。操作系统也无法使用这部分内存，因为该内存被认为是您的程序仍在使用的。
内存泄漏在程序运行时会吞噬可用内存，不仅减少了该程序的可用内存，也减少了其他程序的可用内存。存在严重内存泄漏问题的程序可能会耗尽所有可用内存，导致整个机器运行缓慢甚至崩溃。只有当您的程序终止后，操作系统才能清理并“回收”所有泄漏的内存。
尽管内存泄漏可能由指针超出作用域引起，但还有其他方式可能导致内存泄漏。例如，如果持有动态分配内存地址的指针被赋予另一个值，就可能发生内存泄漏
int value = 5;
int* ptr{ new int{} }; // allocate memory
ptr = &value; // old address lost, memory leak results
这可以通过在重新分配指针之前将其删除来解决
int value{ 5 };
int* ptr{ new int{} }; // allocate memory
delete ptr; // return memory back to operating system
ptr = &value; // reassign pointer to address of value
与此相关的是，也可能通过重复分配导致内存泄漏
int* ptr{ new int{} };
ptr = new int{}; // old address lost, memory leak results
第二次分配返回的地址会覆盖第一次分配的地址。因此，第一次分配就变成了内存泄漏！
同样，这可以通过确保在重新分配指针之前将其删除来避免。
总结
运算符 `new` 和 `delete` 允许我们为程序动态分配单个变量。
动态分配的内存具有动态持续时间，并且会一直保持分配状态，直到您解除分配它或程序终止。
请注意不要解引用悬空指针或空指针。
在下一课中，我们将探讨如何使用 new 和 delete 来分配和删除数组。
下一课
19.2
动态分配数组
返回目录
上一课
18.4
代码计时