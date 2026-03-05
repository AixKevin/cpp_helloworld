# 12.12 — 按引用返回和按地址返回

12.12 — 按引用返回和按地址返回
Alex
2008 年 2 月 25 日，太平洋标准时间晚上 9:04
2025 年 1 月 3 日
在之前的课程中，我们讨论过，当按值传递参数时，参数的副本会被复制到函数参数中。对于基本类型（复制开销小），这没问题。但对于类类型（如
std::string
），复制通常开销很大。我们可以通过使用按（const）引用传递（或按地址传递）来避免昂贵的复制。
当按值返回时，我们会遇到类似的情况：返回值的副本会被传递回调用者。如果函数的返回类型是类类型，这可能会很昂贵。
std::string returnByValue(); // returns a copy of a std::string (expensive)
按引用返回
在我们将类类型返回给调用者的情况下，我们可能（或可能不）希望按引用返回。
按引用返回
返回一个绑定到被返回对象的引用，这避免了创建返回值的副本。要按引用返回，我们只需将函数的返回值定义为引用类型即可。
std::string&       returnByReference(); // returns a reference to an existing std::string (cheap)
const std::string& returnByReferenceToConst(); // returns a const reference to an existing std::string (cheap)
这是一个演示按引用返回机制的学术程序。
#include <iostream>
#include <string>

const std::string& getProgramName() // returns a const reference
{
    static const std::string s_programName { "Calculator" }; // has static duration, destroyed at end of program

    return s_programName;
}

int main()
{
    std::cout << "This program is named " << getProgramName();

    return 0;
}
这个程序打印
This program is named Calculator
因为
getProgramName()
返回一个 const 引用，当执行
return s_programName
行时，
getProgramName()
将返回一个对
s_programName
的 const 引用（从而避免了创建副本）。然后，调用者可以使用该 const 引用来访问
s_programName
的值，该值将被打印出来。
按引用返回的对象在函数返回后必须存在。
使用按引用返回有一个主要的注意事项：程序员**必须**确保被引用的对象比返回引用的函数存在时间更长。否则，返回的引用将悬空（引用已被销毁的对象），使用该引用将导致未定义行为。
在上面的程序中，因为
s_programName
具有静态持续时间，所以
s_programName
将一直存在直到程序结束。当
main()
访问返回的引用时，它实际上是在访问
s_programName
，这没问题，因为
s_programName
不会在稍后被销毁。
现在让我们修改上面的程序，以展示当我们的函数返回一个悬空引用时会发生什么。
#include <iostream>
#include <string>

const std::string& getProgramName()
{
    const std::string programName { "Calculator" }; // now a non-static local variable, destroyed when function ends

    return programName;
}

int main()
{
    std::cout << "This program is named " << getProgramName(); // undefined behavior

    return 0;
}
此程序的结果是未定义的。当
getProgramName()
返回时，会返回一个绑定到局部变量
programName
的引用。然后，因为
programName
是一个具有自动持续时间的局部变量，
programName
在函数结束时被销毁。这意味着返回的引用现在悬空，在
main()
函数中使用
programName
会导致未定义行为。
如果你尝试按引用返回局部变量，现代编译器会产生警告或错误（因此上面的程序甚至可能无法编译），但编译器有时难以检测更复杂的情况。
警告
按引用返回的对象必须在返回引用的函数的范围之外存在，否则将导致悬空引用。切勿按引用返回（非静态）局部变量或临时对象。
生命周期延长不跨函数边界工作
让我们看一个按引用返回临时对象的例子。
#include <iostream>

const int& returnByConstReference()
{
    return 5; // returns const reference to temporary object
}

int main()
{
    const int& ref { returnByConstReference() };

    std::cout << ref; // undefined behavior

    return 0;
}
在上述程序中，
returnByConstReference()
返回一个整数字面量，但函数的返回类型是
const int&
。这导致创建并返回一个绑定到持有值 5 的临时对象的临时引用。此返回的引用被复制到调用者范围内的临时引用中。然后临时对象超出作用域，使调用者范围内的临时引用悬空。
当调用者范围内的临时引用绑定到 const 引用变量
ref
（在
main()
中）时，延长临时对象的生命周期已经太晚了——因为它已经被销毁。因此
ref
是一个悬空引用，使用
ref
的值将导致未定义行为。
这是一个不那么明显的、同样不起作用的例子。
#include <iostream>

const int& returnByConstReference(const int& ref)
{
    return ref;
}

int main()
{
    // case 1: direct binding
    const int& ref1 { 5 }; // extends lifetime
    std::cout << ref1 << '\n'; // okay

    // case 2: indirect binding
    const int& ref2 { returnByConstReference(5) }; // binds to dangling reference
    std::cout << ref2 << '\n'; // undefined behavior

    return 0;
}
在情况 2 中，创建了一个临时对象来保存值
5
，函数参数
ref
绑定到该对象。函数只是将此引用返回给调用者，然后调用者使用该引用初始化
ref2
。因为这不是与临时对象的直接绑定（因为引用是通过函数跳过的），所以生命周期延长不适用。这导致
ref2
悬空，其后续使用是未定义的行为。
警告
引用生命周期延长不跨函数边界工作。
不要按引用返回非 const 静态局部变量。
在上面的原始示例中，我们按引用返回了一个 const 静态局部变量，以一种简单的方式说明按引用返回的机制。然而，按引用返回非 const 静态局部变量是非常非惯用的，通常应避免。下面是一个简化示例，说明了可能发生的一个此类问题。
#include <iostream>
#include <string>

const int& getNextId()
{
    static int s_x{ 0 }; // note: variable is non-const
    ++s_x; // generate the next id
    return s_x; // and return a reference to it
}

int main()
{
    const int& id1 { getNextId() }; // id1 is a reference
    const int& id2 { getNextId() }; // id2 is a reference

    std::cout << id1 << id2 << '\n';

    return 0;
}
这个程序打印
22
发生这种情况是因为
id1
和
id2
引用同一个对象（静态变量
s_x
），所以当任何东西（例如
getNextId()
）修改该值时，所有引用现在都访问修改后的值。
上述示例可以通过将
id1
和
id2
设为普通变量（而不是引用）来修复，以便它们保存返回值的副本而不是对
s_x
的引用。
致进阶读者
这里是另一个不那么明显的相同问题的例子。
#include <iostream>
#include <string>
#include <string_view>

std::string& getName()
{
    static std::string s_name{};
    std::cout << "Enter a name: ";
    std::cin >> s_name;
    return s_name;
}

void printFirstAlphabetical(const std::string& s1, const std::string& s2)
{
    if (s1 < s2)
        std::cout << s1 << " comes before " << s2 << '\n';
    else
        std::cout << s2 << " comes before " << s1 << '\n';
}

int main()
{
    printFirstAlphabetical(getName(), getName());
    
    return 0;
}
以下是此程序的一次运行结果：
Enter a name: Dave
Enter a name: Stan
Stan comes before Stan
在此示例中，
getName()
返回对静态局部变量
s_name
的引用。用对
s_name
的引用初始化
const std::string&
会导致该
std::string&
绑定到
s_name
（而不是创建它的副本）。
因此，
s1
和
s2
都最终查看
s_name
（它被赋予了我们输入的最后一个名称）。
请注意，如果我们改用
std::string_view
参数，当底层
std::string
改变时，第一个
std::string_view
参数将失效。
返回非 const 静态局部变量引用的程序经常遇到的另一个问题是，没有标准化的方法可以将
s_x
重置回默认状态。此类程序必须使用非传统解决方案（例如重置函数参数），或者只能通过退出并重新启动程序来重置。
最佳实践
避免返回对非 const 局部静态变量的引用。
有时会返回对*常量*局部静态变量的 const 引用，如果被按引用返回的局部变量创建和/或初始化成本很高（这样我们就不必在每次函数调用时重新创建变量）。但这很少见。
有时也会返回对*常量*全局变量的 const 引用，作为封装访问全局变量的一种方式。我们在
第 7.8 课 -- 为什么（非 const）全局变量是邪恶的
中讨论了这一点。如果故意小心使用，这也是可以的。
用返回的引用给普通变量赋值/初始化会创建一个副本
如果一个函数返回一个引用，并且该引用用于初始化或赋值给一个非引用变量，则返回值将被复制（就像它是按值返回一样）。
#include <iostream>
#include <string>

const int& getNextId()
{
    static int s_x{ 0 };
    ++s_x;
    return s_x;
}

int main()
{
    const int id1 { getNextId() }; // id1 is a normal variable now and receives a copy of the value returned by reference from getNextId()
    const int id2 { getNextId() }; // id2 is a normal variable now and receives a copy of the value returned by reference from getNextId()

    std::cout << id1 << id2 << '\n';

    return 0;
}
在上面的示例中，
getNextId()
返回一个引用，但
id1
和
id2
是非引用变量。在这种情况下，返回引用的值被复制到普通变量中。因此，此程序打印：
12
还要注意，如果程序返回一个悬空引用，那么在进行复制之前，该引用就会悬空，这将导致未定义行为。
#include <iostream>
#include <string>

const std::string& getProgramName() // will return a const reference
{
    const std::string programName{ "Calculator" };

    return programName;
}

int main()
{
    std::string name { getProgramName() }; // makes a copy of a dangling reference
    std::cout << "This program is named " << name << '\n'; // undefined behavior

    return 0;
}
按引用返回引用参数是可以的。
有许多情况下按引用返回对象是有意义的，我们将在未来的课程中遇到许多此类情况。但是，现在我们可以展示一个有用的例子。
如果一个参数通过引用传递给函数，那么通过引用返回该参数是安全的。这很有道理：为了将参数传递给函数，参数必须存在于调用者的作用域中。当被调用的函数返回时，该对象仍必须存在于调用者的作用域中。
这是一个此类函数的简单示例。
#include <iostream>
#include <string>

// Takes two std::string objects, returns the one that comes first alphabetically
const std::string& firstAlphabetical(const std::string& a, const std::string& b)
{
	return (a < b) ? a : b; // We can use operator< on std::string to determine which comes first alphabetically
}

int main()
{
	std::string hello { "Hello" };
	std::string world { "World" };

	std::cout << firstAlphabetical(hello, world) << '\n';

	return 0;
}
这会打印
Hello
在上面的函数中，调用者通过 const 引用传入两个 std::string 对象，其中按字母顺序排在前面的字符串会通过 const 引用传回。如果我们使用按值传递和按值返回，我们最多会创建 3 个 std::string 副本（每个参数一个，返回值一个）。通过使用按引用传递/按引用返回，我们可以避免这些副本。
通过 const 引用传递的右值可以安全地通过 const 引用返回。
当一个 const 引用参数的实参是一个右值时，仍然可以通过 const 引用返回该参数。
这是因为右值直到创建它们的完整表达式结束时才会被销毁。
首先，让我们看看这个例子。
#include <iostream>
#include <string>

std::string getHello()
{
    return "Hello"; // implicit conversion to std::string
}

int main()
{
    const std::string s{ getHello() };

    std::cout << s;
    
    return 0;
}
在这种情况下，
getHello()
按值返回一个
std::string
，它是一个右值。这个右值接着被用来初始化
s
。在
s
初始化之后，创建右值的表达式已经完成求值，右值被销毁。
现在让我们看一个类似的例子。
#include <iostream>
#include <string>

const std::string& foo(const std::string& s)
{
    return s;
}

std::string getHello()
{
    return "Hello"; // implicit conversion to std::string
}

int main()
{
    const std::string s{ foo(getHello()) };

    std::cout << s;
    
    return 0;
}
在这种情况下，唯一的区别是右值通过 const 引用传递给
foo()
，然后通过 const 引用返回给调用者，然后才用于初始化
s
。其他一切都完全相同。
我们在
第 14.6 课 -- 访问函数
中讨论了类似的情况。
调用者可以通过引用修改值
当一个参数通过非 const 引用传递给函数时，函数可以使用该引用修改参数的值。
类似地，当一个非 const 引用从函数返回时，调用者可以使用该引用修改被返回的值。
这是一个说明性示例。
#include <iostream>

// takes two integers by non-const reference, and returns the greater by reference
int& max(int& x, int& y)
{
    return (x > y) ? x : y;
}

int main()
{
    int a{ 5 };
    int b{ 6 };

    max(a, b) = 7; // sets the greater of a or b to 7

    std::cout << a << b << '\n';
        
    return 0;
}
在上面的程序中，
max(a, b)
调用
max()
函数，其中
a
和
b
作为参数。引用参数
x
绑定到参数
a
，引用参数
y
绑定到参数
b
。函数然后确定
x
(
5
) 和
y
(
6
) 中哪个更大。在这种情况下，是
y
，所以函数将
y
（它仍然绑定到
b
）返回给调用者。然后调用者将值
7
赋值给这个返回的引用。
因此，表达式
max(a, b) = 7
有效地解析为
b = 7
。
这会打印
57
按地址返回
按地址返回
的工作方式几乎与按引用返回相同，只是返回的是对象的指针而不是对象的引用。按地址返回与按引用返回具有相同的主要注意事项——按地址返回的对象必须比返回地址的函数的范围更长，否则调用者将收到一个悬空指针。
按地址返回相对于按引用返回的主要优点是，如果没有有效的对象可返回，我们可以让函数返回
nullptr
。例如，假设我们有一个学生列表要搜索。如果我们找到我们要找的学生，我们可以返回一个指向代表匹配学生的对象的指针。如果找不到任何匹配的学生，我们可以返回
nullptr
以指示未找到匹配的学生对象。
按地址返回的主要缺点是，调用者必须记住在解引用返回值之前进行
nullptr
检查，否则可能会发生空指针解引用并导致未定义行为。由于此危险，除非需要返回“无对象”的能力，否则应优先选择按引用返回而不是按地址返回。
最佳实践
除非返回“无对象”（使用
nullptr
）的能力很重要，否则优先选择按引用返回而不是按地址返回。
相关内容
如果你需要返回“无对象”或值（而不是对象）的能力，
12.15 -- std::optional
描述了一个很好的替代方案。
相关内容
有关何时返回
std::string_view
与
const std::string&
的快速指南，请参阅
5.9 -- std::string_view（第 2 部分）
。
下一课
12.13
输入和输出参数
返回目录
上一课
12.11
按地址传递（第 2 部分）