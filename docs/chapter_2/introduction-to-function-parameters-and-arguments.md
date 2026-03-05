# 2.4 — 函数参数和实参简介

2.4 — 函数参数和实参简介
Alex
2015 年 1 月 25 日，太平洋标准时间下午 12:12
2025 年 2 月 18 日
在上一课中，我们学习了函数可以将值返回给函数的调用者。我们利用这一点创建了一个模块化的
getValueFromUser
函数，并在本程序中使用它。
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

int main()
{
	int num { getValueFromUser() };

	std::cout << num << " doubled is: " << num * 2 << '\n';

	return 0;
}
然而，如果我们也想将输出行放入自己的函数中，该怎么办？你可能会尝试这样做：
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

// This function won't compile
void printDouble()
{
	std::cout << num << " doubled is: " << num * 2 << '\n';
}

int main()
{
	int num { getValueFromUser() };

	printDouble();

	return 0;
}
这无法编译，因为函数
printDouble
不知道标识符
num
是什么。你可能会尝试在函数 printDouble() 内部将 num 定义为变量：
void printDouble()
{
	int num{}; // we added this line
	std::cout << num << " doubled is: " << num * 2 << '\n';
}
虽然这解决了编译错误并使程序能够编译，但程序仍然无法正常工作（它总是打印“0 doubled is: 0”）。这里问题的核心是函数
printDouble
无法访问用户输入的值。
我们需要某种方法将变量
num
的值传递给函数
printDouble
，以便
printDouble
可以在函数体中使用该值。
函数参数和实参
在许多情况下，能够将信息传递给被调用的函数以使函数具有可处理的数据是很有用的。例如，如果我们要编写一个函数来添加两个数字，我们需要某种方式告诉函数在调用它时要添加哪两个数字。否则，函数怎么会知道要添加什么呢？我们通过函数参数和实参来实现这一点。
函数参数
是用于函数头中的变量。函数参数的工作方式与函数内部定义的变量几乎相同，但有一个区别：它们使用函数调用者提供的值进行初始化。
函数参数在函数头中定义，方法是将它们放在函数名后的括号之间，多个参数之间用逗号分隔。
以下是一些具有不同数量参数的函数示例：
// This function takes no parameters
// It does not rely on the caller for anything
void doPrint()
{
    std::cout << "In doPrint()\n";
}

// This function takes one integer parameter named x
// The caller will supply the value of x
void printValue(int x)
{
    std::cout << x << '\n';
}

// This function has two integer parameters, one named x, and one named y
// The caller will supply the value of both x and y
int add(int x, int y)
{
    return x + y;
}
实参
是函数调用时从调用者传递给函数的值。
doPrint(); // this call has no arguments
printValue(6); // 6 is the argument passed to function printValue()
add(2, 3); // 2 and 3 are the arguments passed to function add()
请注意，多个实参也用逗号分隔。
参数和实参如何协同工作
当调用函数时，函数的所有参数都作为变量创建，并且每个实参的值都被**复制**到匹配的参数中（使用复制初始化）。这个过程称为**按值传递**。利用按值传递的函数参数称为**值参数**。
例如
#include <iostream>

// This function has two integer parameters, one named x, and one named y
// The values of x and y are passed in by the caller
void printValues(int x, int y)
{
    std::cout << x << '\n';
    std::cout << y << '\n';
}

int main()
{
    printValues(6, 7); // This function call has two arguments, 6 and 7

    return 0;
}
当函数
printValues
使用实参
6
和
7
调用时，
printValues
的参数
x
被创建并初始化为值
6
，
printValues
的参数
y
被创建并初始化为值
7
。
这会产生以下输出：
6
7
请注意，实参的数量通常必须与函数参数的数量匹配，否则编译器将抛出错误。传递给函数的实参可以是任何有效的表达式（因为实参本质上只是参数的初始化器，而初始化器可以是任何有效的表达式）。
修复我们的挑战程序
我们现在拥有修复本课开头提出的程序所需的工具。
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

void printDouble(int value) // This function now has an integer parameter
{
	std::cout << value << " doubled is: " << value * 2 << '\n';
}

int main()
{
	int num { getValueFromUser() };

	printDouble(num);

	return 0;
}
在此程序中，变量
num
首先用用户输入的值进行初始化。然后，调用函数
printDouble
，并且实参
num
的值被复制到函数
printDouble
的
value
参数中。函数
printDouble
然后使用参数
value
的值。
使用返回值作为实参
在上述问题中，我们可以看到变量
num
只使用一次，用于将函数
getValueFromUser
的返回值传输到对函数
printDouble
的调用的实参中。
我们可以稍微简化上面的例子，如下所示：
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

void printDouble(int value)
{
	std::cout << value << " doubled is: " << value * 2 << '\n';
}

int main()
{
	printDouble(getValueFromUser());

	return 0;
}
现在，我们直接将函数
getValueFromUser
的返回值作为实参传递给函数
printDouble
！
尽管此程序更简洁（并明确表示用户读取的值将不再用于其他任何目的），但您可能还会觉得这种“紧凑语法”有点难以阅读。如果您更喜欢使用变量的版本，那也没关系。
参数和返回值如何协同工作
通过同时使用参数和返回值，我们可以创建接收数据作为输入，对其进行一些计算，并将结果返回给调用者的函数。
这是一个非常简单的函数示例，它将两个数字相加并将结果返回给调用者。
#include <iostream>

// add() takes two integers as parameters, and returns the result of their sum
// The values of x and y are determined by the function that calls add()
int add(int x, int y)
{
    return x + y;
}

// main takes no parameters
int main()
{
    std::cout << add(4, 5) << '\n'; // Arguments 4 and 5 are passed to function add()
    return 0;
}
执行从
main
的顶部开始。当
add(4, 5)
被评估时，函数
add
被调用，参数
x
被初始化为值
4
，参数
y
被初始化为值
5
。
函数
add
中的
return 语句
评估
x + y
以产生值
9
，然后将其返回给
main
。然后，这个值
9
被发送到
std::cout
以打印到控制台。
输出
9
以图示形式表示：
更多例子
让我们看一些更多的函数调用
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int multiply(int z, int w)
{
    return z * w;
}

int main()
{
    std::cout << add(4, 5) << '\n'; // within add() x=4, y=5, so x+y=9
    std::cout << add(1 + 2, 3 * 4) << '\n'; // within add() x=3, y=12, so x+y=15

    int a{ 5 };
    std::cout << add(a, a) << '\n'; // evaluates (5 + 5)

    std::cout << add(1, multiply(2, 3)) << '\n'; // evaluates 1 + (2 * 3)
    std::cout << add(1, add(2, 3)) << '\n'; // evaluates 1 + (2 + 3)

    return 0;
}
此程序产生以下输出
9
15
10
7
6
第一个语句很简单。
在第二个语句中，实参是在传递之前进行求值的表达式。在这种情况下，
1 + 2
求值为
3
，因此
3
被复制到参数
x
。
3 * 4
求值为
12
，因此
12
被复制到参数
y
。
add(3, 12)
解析为
15
。
接下来的两组语句也相对容易
int a{ 5 };
    std::cout << add(a, a) << '\n'; // evaluates (5 + 5)
在这种情况下，调用
add()
时，变量
a
的值被复制到参数
x
和
y
中。由于
a
的值为
5
，因此
add(a, a)
=
add(5, 5)
，解析为值
10
。
让我们来看看这组中第一个棘手的语句。
std::cout << add(1, multiply(2, 3)) << '\n'; // evaluates 1 + (2 * 3)
当函数
add
执行时，程序需要确定参数
x
和
y
的值是什么。
x
很简单，因为我们只传递了整数
1
。为了获得参数
y
的值，它需要首先评估
multiply(2, 3)
。程序调用
multiply
并初始化
z
=
2
和
w
=
3
，所以
multiply(2, 3)
返回整数值
6
。这个返回值
6
现在可以用于初始化
add
函数的
y
参数。
add(1, 6)
返回整数
7
，然后将其传递给 std::cout 进行打印。
不那么冗长地说：
add(1, multiply(2, 3))
评估为
add(1, 6)
评估为
7
下面的语句看起来很棘手，因为传递给
add
的其中一个实参是另一个
add
调用。
std::cout << add(1, add(2, 3)) << '\n'; // evaluates 1 + (2 + 3)
但是这种情况与前面的情况完全相同。add(2, 3) 首先解析，结果是返回值
5
。现在它可以解析 add(1, 5)，它评估为值
6
，然后将其传递给 std::cout 进行打印。
更简洁地说：
add(1, add(2, 3))
评估为
add(1, 5)
=> 评估为
6
未引用参数和未命名参数
在某些情况下，您会遇到函数体中未使用的参数。这些参数称为
未引用参数
。
一个简单的例子：
void doSomething(int count) // warning: unreferenced parameter count
{
    // This function used to do something with count but it is not used any longer
}

int main()
{
    doSomething(4);

    return 0;
}
就像未使用的局部变量一样，您的编译器可能会警告变量
count
已定义但未使用。
在函数定义中，函数参数的名称是可选的。因此，在函数参数需要存在但未在函数体中使用的情况下，您可以直接省略名称。没有名称的参数称为**未命名参数**。
void doSomething(int) // ok: unnamed parameter will not generate warning
{
}
Google C++ 风格指南建议使用注释来记录未命名参数的用途。
void doSomething(int /*count*/)
{
}
作者注
你可能想知道我们为什么要写一个带有未使用参数值的函数。这种情况最常发生在以下类似情况中：
假设我们有一个带有一个参数的函数。后来，函数以某种方式更新，并且不再需要该参数的值。如果现在未使用的函数参数被简单地移除，那么对该函数的每个现有调用都将中断（因为函数调用将提供比函数可接受的更多参数）。这将要求我们找到对该函数的每个调用并移除不需要的参数。这可能需要大量工作（并需要大量重新测试）。甚至可能无法做到（在我们无法控制所有调用函数的代码的情况下）。因此，我们可以保留参数不变，只是让它什么都不做。
致进阶读者
发生这种情况的其他情况：
运算符
++
和
--
有前缀和后缀变体（例如
++foo
vs
foo++
）。未引用函数参数用于区分此类运算符的重载是针对前缀情况还是后缀情况。我们将在第
21.8 课 -- 重载递增和递减运算符
中介绍这一点。
当我们需要从类型（而不是值）的类型模板参数确定某些内容时。
作者注
如果未命名参数对您来说仍然没有意义，请不要担心。我们将在未来的课程中再次遇到它们，届时我们将有更多的上下文来解释它们何时有用。
最佳实践
当函数参数存在但未在函数体中使用时，请不要为其命名。您可以选择在注释中放置一个名称。
总结
函数参数和返回值是编写可重用函数的关键机制，因为它允许我们编写能够执行任务并将检索或计算的结果返回给调用者，而无需事先知道具体的输入或输出是什么。
小测验时间
问题 #1
这段程序片段有什么问题？
#include <iostream>

void multiply(int x, int y)
{
    return x * y;
}

int main()
{
    std::cout << multiply(4, 5) << '\n';

    return 0;
}
显示答案
multiply() 的返回类型为 void，这意味着它是一个不返回值的函数。由于该函数试图返回一个值（通过 return 语句），因此该函数将产生一个编译错误。返回类型应该是 int。
问题 #2
这段程序片段有什么两处错误？
#include <iostream>

int multiply(int x, int y)
{
    int product { x * y };
}

int main()
{
    std::cout << multiply(4) << '\n';

    return 0;
}
显示答案
问题 1：main() 向 multiply() 传递了一个实参，但 multiply() 需要两个实参。问题 2：multiply() 没有 return 语句。
问题 #3
以下程序打印什么值？
#include <iostream>

int add(int x, int y, int z)
{
    return x + y + z;
}

int multiply(int x, int y)
{
    return x * y;
}

int main()
{
    std::cout << multiply(add(1, 2, 3), 4) << '\n';

    return 0;
}
显示答案
调用 multiply，其中 x = add(1, 2, 3)，y = 4。首先，CPU 解析 x = add(1, 2, 3)，它返回 1 + 2 + 3，即 x = 6。multiply(6, 4) = 24，这就是答案。
问题 #4
编写一个名为 doubleNumber() 的函数，它接受一个整数参数。该函数应返回参数值的两倍。
显示答案
int doubleNumber(int x)
{
    return 2 * x;
}
问题 #5
编写一个完整的程序，从用户那里读取一个整数，使用你在上一个测验问题中编写的 doubleNumber() 函数将其加倍，然后将加倍后的值打印到控制台。
显示答案
#include <iostream>

int doubleNumber(int x)
{
    return 2 * x;
}

int main()
{
    std::cout << "Enter an integer value: ";
    int x{};
    std::cin >> x;
    std::cout << doubleNumber(x) << '\n';

    return 0;
}
注意：您可能会想到其他（类似）的解决方案。在 C++ 中，通常有多种方法可以做同样的事情。
下一课
2.5
局部作用域简介
返回目录
上一课
2.3
Void 函数（不返回值函数）