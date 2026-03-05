# 2.5 — 局部作用域简介

2.5 — 局部作用域简介
Alex
2015年2月8日, 下午5:06 PST
2025年1月1日
局部变量
在函数体内部定义的变量称为
局部变量
（与
全局变量
相对，我们将在未来的章节中讨论全局变量）。
int add(int x, int y)
{
    int z{ x + y }; // z is a local variable

    return z;
}
函数形参通常也被认为是局部变量，我们也将它们包含在内。
int add(int x, int y) // function parameters x and y are local variables
{
    int z{ x + y };

    return z;
}
在本课中，我们将更详细地探讨局部变量的一些属性。
局部变量的生命周期
在课程
1.3 -- 对象和变量简介
中，我们讨论了像
int x;
这样的变量定义如何导致变量在执行此语句时被实例化。函数形参在进入函数时被创建和初始化，而函数体内的变量则在定义点被创建和初始化。
例如
int add(int x, int y) // x and y created and initialized here
{ 
    int z{ x + y };   // z created and initialized here

    return z;
}
自然的后续问题是，“那么实例化的变量何时被销毁？”。局部变量在其定义所在的大括号集合的末尾，以与创建相反的顺序被销毁（对于函数形参，则是在函数末尾）。
int add(int x, int y)
{ 
    int z{ x + y };

    return z;
} // z, y, and x destroyed here
就像一个人的寿命被定义为从出生到死亡之间的时间一样，一个对象的
生命周期
被定义为从其创建到销毁之间的时间。请注意，变量的创建和销毁发生在程序运行时（称为 runtime），而不是在编译时。因此，生命周期是一个运行时属性。
致进阶读者
上述关于创建、初始化和销毁的规则是保证。也就是说，对象必须不晚于其定义点被创建和初始化，并且不早于其定义所在的大括号集合的末尾（或者，对于函数形参，是在函数末尾）被销毁。
实际上，C++ 规范给予编译器很大的灵活性来决定局部变量何时被创建和销毁。为了优化目的，对象可能会被更早地创建，或者更晚地被销毁。最常见的情况是，局部变量在函数进入时被创建，在函数退出时以与创建相反的顺序被销毁。我们将在未来的课程中，当我们谈论调用栈时，更详细地讨论这一点。
这是一个稍复杂一点的程序，演示了名为
x
的变量的生命周期。
#include <iostream>

void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    int x{ 0 };    // x's lifetime begins here

    doSomething(); // x is still alive during this function call

    return 0;
} // x's lifetime ends here
在上面的程序中，
x
的生命周期从其定义点开始，直到函数
main
结束。这包括在执行函数
doSomething
期间所花费的时间。
当一个对象被销毁时会发生什么？
在大多数情况下，什么都不会发生。被销毁的对象只是变得无效了。
致进阶读者
如果对象是类类型对象，在销毁之前，会调用一个名为析构函数的特殊函数。在许多情况下，析构函数什么也不做，这种情况下不会产生任何开销。我们将在课程
15.4 -- 析构函数简介
中介绍析构函数。
在对象被销毁后对其进行任何使用都将导致未定义行为。
在销毁后的某个时间点，对象使用的内存将被
释放
（deallocated，即腾出以供重用）。
局部作用域（块作用域）
一个标识符的
作用域
决定了该标识符在源代码中可以在哪里被看到和使用。当一个标识符可以被看到和使用时，我们说它
在作用域内
。当一个标识符无法被看到时，我们不能使用它，我们说它
在作用域外
。作用域是一个编译时属性，尝试使用一个不在作用域内的标识符将导致编译错误。
局部变量的标识符具有局部作用域。具有
局部作用域
（技术上称为
块作用域
）的标识符从其定义点开始，直到包含该标识符的最内层大括号对的末尾（对于函数形参，则是在函数末尾）都是可用的。这确保了局部变量不能在其定义点之前被使用（即使编译器选择在此之前创建它们），也不能在它们被销毁后使用。在一个函数中定义的局部变量在被调用的其他函数中也不在作用域内。
这是一个演示名为
x
的变量作用域的程序。
#include <iostream>

// x is not in scope anywhere in this function
void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    // x can not be used here because it's not in scope yet

    int x{ 0 }; // x enters scope here and can now be used within this function

    doSomething();

    return 0;
} // x goes out of scope here and can no longer be used
在上面的程序中，变量
x
在其定义点进入作用域。
x
在包含该标识符的最内层大括号对的末尾，也就是函数
main()
的右花括号处，离开作用域。请注意，变量
x
在函数
doSomething
的任何地方都不在作用域内。函数
main
调用函数
doSomething
这个事实在这种情况下是无关紧要的。
“在作用域外” vs “离开作用域”
术语“在作用域外”（out of scope）和“离开作用域”（going out of scope）可能会让新程序员感到困惑。
一个标识符在代码中任何无法被访问的地方都
在作用域外
。在上面的例子中，标识符
x
从其定义点到
main
函数结束都在作用域内。标识符
x
在该代码区域之外都
在作用域外
。
术语“离开作用域”通常应用于对象而非标识符。我们说一个对象在其实例化所在的作用域的末尾（右花括号）
离开作用域
。在上面的例子中，名为
x
的对象在函数
main
的末尾
离开作用域
。
一个局部变量的生命周期在它离开作用域的点结束，所以局部变量在此时被销毁。
请注意，并非所有类型的变量都在离开作用域时被销毁。我们将在未来的课程中看到这些例子。
另一个例子
这是一个稍复杂一点的例子。记住，生命周期是运行时属性，而作用域是编译时属性，所以尽管我们在同一个程序中讨论它们，但它们是在不同阶段被强制执行的。
#include <iostream>

int add(int x, int y) // x and y are created and enter scope here
{
    // x and y are usable only within add()
    return x + y;
} // y and x go out of scope and are destroyed here

int main()
{
    int a{ 5 }; // a is created, initialized, and enters scope here
    int b{ 6 }; // b is created, initialized, and enters scope here

    // a and b are usable only within main()

    std::cout << add(a, b) << '\n'; // calls add(5, 6), where x=5 and y=6

    return 0;
} // b and a go out of scope and are destroyed here
形参
x
和
y
在
add
函数被调用时创建，只能在函数
add
内部被看到/使用，并在
add
结束时被销毁。变量
a
和
b
在函数
main
内部创建，只能在函数
main
内部被看到/使用，并在
main
结束时被销毁。
为了增进你对这一切如何协同工作的理解，让我们更详细地跟踪这个程序的执行过程。以下是按顺序发生的事件：
执行从
main
的顶部开始。
main
的变量
a
被创建并赋值为
5
。
main
的变量
b
被创建并赋值为
6
。
函数
add
被调用，实参值为
5
和
6
。
add
的形参
x
和
y
被创建并分别用值
5
和
6
进行初始化。
表达式
x + y
被求值，产生值
11
。
add
将值
11
复制回调用者
main
。
add
的形参
y
和
x
被销毁。
main
将
11
打印到控制台。
main
返回
0
给操作系统。
main
的变量
b
和
a
被销毁。
然后程序结束。
请注意，如果函数
add
被调用两次，形参
x
和
y
将被创建和销毁两次——每次调用一次。在一个有很多函数和函数调用的程序中，变量的创建和销毁会频繁发生。
函数分离
在上面的例子中，很容易看出变量
a
和
b
与
x
和
y
是不同的变量。
现在考虑以下类似程序：
#include <iostream>

int add(int x, int y) // add's x and y are created and enter scope here
{
    // add's x and y are visible/usable within this function only
    return x + y;
} // add's y and x go out of scope and are destroyed here

int main()
{
    int x{ 5 }; // main's x is created, initialized, and enters scope here
    int y{ 6 }; // main's y is created, initialized, and enters scope here

    // main's x and y are usable within this function only
    std::cout << add(x, y) << '\n'; // calls function add() with x=5 and y=6

    return 0;
} // main's y and x go out of scope and are destroyed here
在这个例子中，我们所做的只是将函数
main
内部的变量
a
和
b
的名称更改为
x
和
y
。这个程序编译和运行的结果完全相同，即使函数
main
和
add
都拥有名为
x
和
y
的变量。为什么这样可以呢？
首先，我们需要认识到，尽管函数
main
和
add
都拥有名为
x
和
y
的变量，但这些变量是不同的。函数
main
中的
x
和
y
与函数
add
中的
x
和
y
没有任何关系——它们只是碰巧同名而已。
其次，当在函数
main
内部时，名称
x
和
y
指的是 main 的局部作用域变量
x
和
y
。这些变量只能在
main
内部被看到（和使用）。同样，当在函数
add
内部时，名称
x
和
y
指的是函数形参
x
和
y
，它们只能在
add
内部被看到（和使用）。
简而言之，
add
和
main
都不知道对方函数有同名的变量。因为作用域不重叠，所以编译器在任何时候都很清楚指的是哪个
x
和
y
。
关键见解
用于函数形参或在函数体内声明的变量的名称仅在声明它们的函数内部可见。这意味着函数内的局部变量可以随意命名，而无需考虑其他函数中变量的名称。这有助于保持函数的独立性。
我们将在未来的章节中更多地讨论局部作用域和其他类型的作用域。
在哪里定义局部变量
在现代 C++ 中，最佳实践是函数体内的局部变量应该定义在尽可能靠近其首次使用的地方。
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";
	int x{};       // x defined here
	std::cin >> x; // and used here

	std::cout << "Enter another integer: ";
	int y{};       // y defined here
	std::cin >> y; // and used here

	int sum{ x + y }; // sum can be initialized with intended value
	std::cout << "The sum is: " << sum << '\n';

	return 0;
}
在上面的例子中，每个变量都在其首次使用前被定义。对此无需过于严格——如果你更喜欢交换第 5 行和第 6 行，那也没关系。
最佳实践
将你的局部变量定义在尽可能靠近其首次使用的地方。
题外话…
由于旧式、更原始的编译器的限制，C 语言曾经要求所有局部变量都必须在函数的顶部定义。使用该风格的等效 C++ 程序如下所示：
#include <iostream>

int main()
{
	int x{}, y{}, sum{}; // how are these used?

	std::cout << "Enter an integer: ";
	std::cin >> x;

	std::cout << "Enter another integer: ";
	std::cin >> y;

	sum = x + y;
	std::cout << "The sum is: " << sum << '\n';

	return 0;
}
这种风格由于几个原因而不够理想：
这些变量的预期用途在定义点并不明显。你必须扫描整个函数来确定每个变量在哪里以及如何使用。
预期的初始化值可能在函数顶部不可用（例如，我们无法将
sum
初始化为其预期值，因为我们还不知道
x
和
y
的值）。
变量的初始化器与其首次使用之间可能有很多行。如果我们不记得它被初始化为什么值，我们就必须滚动回函数顶部，这会分散注意力。
这个限制在 C99 语言标准中被取消了。
何时使用函数形参 vs 局部变量
因为函数形参和局部变量都可以在函数体内使用，新程序员有时很难理解何时应该使用哪一个。当调用者将通过实参传入初始化值时，应使用函数形参。否则，应使用局部变量。
当应该使用局部变量时却使用函数形参，会导致代码看起来像这样：
#include <iostream>

int getValueFromUser(int val) // val is a function parameter
{
    std::cout << "Enter a value: ";
    std::cin >> val;
    return val;
}

int main()
{
    int x {};
    int num { getValueFromUser(x) }; // main must pass x as an argument

    std::cout << "You entered " << num << '\n';

    return 0;
}
在上面的例子中，
getValueFromUser()
将
val
定义为一个函数形参。因此，
main()
必须定义
x
，以便有东西可以作为实参传递。然而，
x
的实际值从未被使用，而
val
被初始化的值也从未被使用。让调用者定义并传递一个从未被使用的变量增加了不必要的复杂性。
正确的写法如下：
#include <iostream>

int getValueFromUser()
{
    int val {}; // val is a local variable
    std::cout << "Enter a value: ";
    std::cin >> val;
    return val;
}

int main()
{
    int num { getValueFromUser() }; // main does not need to pass anything

    std::cout << "You entered " << num << '\n';

    return 0;
}
在这个例子中，
val
现在是一个局部变量。
main()
现在更简单了，因为它不需要定义或传递变量来调用
getValueFromUser()
。
最佳实践
当函数内需要一个变量时
当调用者将通过实参传入变量的初始化值时，使用函数形参。
否则，使用局部变量。
临时对象简介
一个
临时对象
（有时也称为
匿名对象
）是一个未命名的对象，用于存放一个仅在短时间内需要的值。临时对象在需要时由编译器生成。
有很多不同的方式可以创建临时值，但这里有一个常见的例子：
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;

	return input; // return the value of input back to the caller
}

int main()
{
	std::cout << getValueFromUser() << '\n'; // where does the returned value get stored?

	return 0;
}
在上面的程序中，函数
getValueFromUser()
将局部变量
input
中存储的值返回给调用者。因为
input
将在函数结束时被销毁，调用者会收到该值的一个副本，这样即使在
input
被销毁后，它仍然有一个可以使用的值。
但是复制回调用者的值存储在哪里呢？我们没有在
main()
中定义任何变量。答案是返回值存储在一个临时对象中。然后这个临时对象被传递给
std::cout
进行打印。
关键见解
按值返回会向调用者返回一个临时对象（其中包含返回值的副本）。
临时对象完全没有作用域（这是合理的，因为作用域是标识符的属性，而临时对象没有标识符）。
临时对象在它们被创建的完整表达式结束时被销毁。这意味着临时对象总是在下一个语句执行之前被销毁。
在我们上面的例子中，为保存
getValueFromUser()
的返回值而创建的临时对象在
std::cout << getValueFromUser() << '\n'
执行后被销毁。
在用临时对象来初始化一个变量的情况下，初始化发生在临时对象销毁之前。
在现代 C++ 中（尤其是自 C++17 以来），编译器有很多技巧来避免在以前需要生成临时对象的地方生成它们。例如，当我们使用一个返回值来初始化一个变量时，这通常会导致创建一个持有返回值的临时对象，然后用这个临时对象来初始化变量。然而，在现代 C++ 中，编译器通常会跳过创建临时对象，直接用返回值来初始化变量。
同样，在上面的例子中，由于
getValueFromUser()
的返回值被立即输出，编译器可以跳过在
main()
中创建和销毁临时对象，并使用
getValueFromUser()
的返回值直接初始化
operator<<
的参数。
小测验时间
问题 #1
下面的程序会打印什么？
#include <iostream>

void doIt(int x)
{
    int y{ 4 };
    std::cout << "doIt: x = " << x << " y = " << y << '\n';

    x = 3;
    std::cout << "doIt: x = " << x << " y = " << y << '\n';
}

int main()
{
    int x{ 1 };
    int y{ 2 };

    std::cout << "main: x = " << x << " y = " << y << '\n';

    doIt(x);

    std::cout << "main: x = " << x << " y = " << y << '\n';

    return 0;
}
显示答案
main: x = 1 y = 2
doIt: x = 1 y = 4
doIt: x = 3 y = 4
main: x = 1 y = 2
这是这个程序中发生的事情：
执行从
main
的顶部开始
main
的变量
x
被创建并初始化为值
1
main
的变量
y
被创建并初始化为值
2
std::cout
打印
main: x = 1 y = 2
调用
doIt
，实参为
1
doIt
的形参
x
被创建并初始化为值
1
doIt
的变量
y
被创建并初始化为值
4
doIt
打印
doIt: x = 1 y = 4
doIt
的变量
x
被赋予新值
3
std::cout
打印
doIt: x = 3 y = 4
doIt
的
y
和
x
被销毁
std::cout
打印
main: x = 1 y = 2
main
返回
0
给操作系统
main
的
y
和
x
被销毁
请注意，即使
doIt
的变量
x
和
y
的值被初始化或赋值为与
main
中的不同，
main
的
x
和
y
也不受影响，因为它们是不同的变量。
下一课
2.6
函数为何有用以及如何有效使用它们
返回目录
上一课
2.4
函数形参与实参简介