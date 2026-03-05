# 2.2 — 函数返回值（值返回函数）

2.2 — 函数返回值（值返回函数）
Alex
2019 年 2 月 1 日，上午 10:29（太平洋标准时间）
2025 年 2 月 5 日
考虑以下程序
#include <iostream>

int main()
{
	// get a value from the user
	std::cout << "Enter an integer: ";
	int num{};
	std::cin >> num;

	// print the value doubled
	std::cout << num << " doubled is: " << num * 2 << '\n';

	return 0;
}
该程序由两个概念部分组成：首先，我们从用户那里获取一个值。然后我们告诉用户该值的两倍是多少。
尽管这个程序非常简单，我们不需要将其拆分成多个函数，但如果我们想这样做呢？从用户那里获取整数值是一个定义明确的任务，我们希望程序能够完成，因此它将成为一个很好的函数候选。
那么我们来编写一个程序来实现它
// This program doesn't work
#include <iostream>

void getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  
}

int main()
{
	getValueFromUser(); // Ask user for input

	int num{}; // How do we get the value from getValueFromUser() and use it to initialize this variable?

	std::cout << num << " doubled is: " << num * 2 << '\n';

	return 0;
}
虽然这个程序是一个很好的尝试，但它并不完全奏效。
当函数
getValueFromUser
被调用时，用户被要求输入一个整数，正如预期。但当
getValueFromUser
终止并将控制权返回给
main
时，用户输入的值就丢失了。变量
num
从未用用户输入的值进行初始化，因此程序总是打印答案
0
。
我们缺少的是一种方法，让
getValueFromUser
将用户输入的值返回给
main
，以便
main
可以使用该数据。
返回值
当您编写用户定义函数时，您可以决定您的函数是否将值返回给调用者。要将值返回给调用者，需要两件事。
首先，您的函数必须指明将返回的值的类型。这是通过设置函数的**返回类型**来完成的，返回类型是在函数名称之前定义的类型。在上面的示例中，函数
getValueFromUser
的返回类型是
void
（表示不会向调用者返回任何值），函数
main
的返回类型是
int
（表示将向调用者返回
int
类型的值）。请注意，这并不决定返回的具体值——它只决定将返回**什么类型**的值。
相关内容
我们将在下一课（
2.3 -- Void 函数（无返回值函数）
）中进一步探讨返回
void
的函数。
其次，在将返回值的函数内部，我们使用**返回语句**来指示返回给调用者的特定值。返回语句由
return
关键字后跟一个表达式（有时称为**返回表达式**）组成，以分号结尾。
当返回语句执行时
返回表达式被求值以生成一个值。
返回表达式生成的值被复制回调用者。此副本称为函数的**返回值**。
函数退出，控制权返回给调用者。
将复制的值返回给调用者的过程称为**按值返回**。
命名法
返回表达式产生要返回的值。返回值是该值的副本。
值返回函数每次被调用时都会返回一个值。
让我们看一个返回整数值的简单函数，以及一个调用它的示例程序
#include <iostream>

// int is the return type
// A return type of int means the function will return some integer value to the caller (the specific value is not specified here)
int returnFive()
{
    // the return statement provides the value that will be returned
    return 5; // return the value 5 back to the caller
}

int main()
{
    std::cout << returnFive() << '\n'; // prints 5
    std::cout << returnFive() + 2 << '\n'; // prints 7

    returnFive(); // okay: the value 5 is returned, but is ignored since main() doesn't do anything with it

    return 0;
}
运行时，此程序打印
5
7
执行从
main
的顶部开始。在第一个语句中，函数调用
returnFive()
被求值，这导致函数
returnFive()
被调用。返回表达式
5
被求值以产生值
5
，该值被返回给调用者并通过
std::cout
打印到控制台。
在第二个函数调用中，函数调用
returnFive
被求值，这导致函数
returnFive
再次被调用。函数
returnFive
将值
5
返回给调用者。表达式
5 + 2
被求值以产生结果
7
，然后通过
std::cout
打印到控制台。
在第三个语句中，函数
returnFive
再次被调用，导致值
5
返回给调用者。但是，函数
main
没有对返回值进行任何操作，因此没有发生任何事情（返回值被忽略）。
注意：除非调用者通过
std::cout
将返回值发送到控制台，否则返回值将不会被打印。在上面的最后一种情况中，返回值没有发送到
std::cout
，因此没有打印任何内容。
提示
当被调用的函数返回一个值时，调用者可以决定在表达式或语句中使用该值（例如，通过使用它初始化一个变量，或将其发送到
std::cout
）或忽略它（不做任何其他操作）。如果调用者忽略返回值，则它将被丢弃（不对其进行任何操作）。
修复我们的挑战程序
考虑到这一点，我们可以修复本课开头介绍的程序
#include <iostream>

int getValueFromUser() // this function now returns an integer value
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input; // return the value the user entered back to the caller
}

int main()
{
	int num { getValueFromUser() }; // initialize num with the return value of getValueFromUser()

	std::cout << num << " doubled is: " << num * 2 << '\n';

	return 0;
}
当这个程序执行时，
main
中的第一个语句将创建一个名为
num
的
int
变量。当程序初始化
num
时，它将看到有一个函数调用
getValueFromUser()
，因此它将执行该函数。函数
getValueFromUser
要求用户输入一个值，然后将该值返回给调用者（
main()
）。这个返回值用作变量
num
的初始值。然后
num
可以在
main()
中根据需要多次使用。
提示
如果您需要多次使用函数调用的返回值，请使用返回值初始化一个变量，然后根据需要多次使用该变量。
自行编译此程序并运行几次，以证明它有效。
重新审视 main()
您现在拥有理解
main()
函数实际工作方式的概念工具。当程序执行时，操作系统会调用
main()
函数。执行然后跳到
main()
的顶部。
main()
中的语句按顺序执行。最后，
main()
返回一个整数值（通常为
0
），然后您的程序终止。
在 C++ 中，对
main()
有两个特殊要求
main()
必须返回一个
int
。
禁止显式调用
main()
。
void foo()
{
    main(); // Compile error: main not allowed to be called explicitly
}

void main() // Compile error: main not allowed to have non-int return type
{
    foo();
}
关键见解
C 允许显式调用
main()
，因此一些 C++ 编译器会为了兼容性而允许这样做。
目前，您还应该将
main()
函数定义在代码文件的底部，其他函数之下，并避免显式调用它。
致进阶读者
一个常见的误解是
main
总是第一个执行的函数。
全局变量在
main
执行之前初始化。如果此类变量的初始化程序调用了一个函数，那么该函数将在
main
之前执行。我们在课程
7.4 -- 全局变量简介
中讨论全局变量。
状态码
您可能想知道为什么我们从
main()
返回 0，以及何时我们可能返回其他值。
main()
的返回值有时称为**状态码**（或不常见地称为**退出码**，或很少称为**返回码**）。状态码用于表示您的程序是否成功。
按照约定，状态码
0
表示程序正常运行（表示程序已执行并按预期运行）。
最佳实践
如果程序正常运行，您的
main
函数应返回
0
。
非零状态码通常用于表示某种类型的故障（虽然这在大多数操作系统上运行良好，但严格来说，它不保证可移植）。
致进阶读者
C++ 标准只定义了 3 个状态码的含义：
0
、
EXIT_SUCCESS
和
EXIT_FAILURE
。
0
和
EXIT_SUCCESS
都表示程序成功执行。
EXIT_FAILURE
表示程序未成功执行。
EXIT_SUCCESS
和
EXIT_FAILURE
是在 <cstdlib> 头文件中定义的预处理器宏
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE

int main()
{
    return EXIT_SUCCESS;
}
如果您想最大限度地提高可移植性，您应该只使用
0
或
EXIT_SUCCESS
来表示成功终止，或使用
EXIT_FAILURE
来表示不成功终止。
我们在课程
2.10 -- 预处理器简介
中介绍了预处理器和预处理器宏。
题外话…
状态码被传递回操作系统。操作系统通常会将状态码提供给启动返回状态码的程序。这为任何启动另一个程序的程序提供了一个粗略的机制，以确定启动的程序是否成功运行。
一个不返回值的有返回值函数将产生未定义行为
返回值的函数称为**值返回函数**。如果返回类型不是
void
，则函数是值返回函数。
值返回函数*必须*返回该类型的值（使用返回语句），否则将导致未定义行为。
相关内容
我们在课程
1.6 -- 未初始化变量和未定义行为
中讨论了未定义行为。
这是一个产生未定义行为的函数示例
#include <iostream>

int getValueFromUserUB() // this function returns an integer value
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;

	// note: no return statement
}

int main()
{
	int num { getValueFromUserUB() }; // initialize num with the return value of getValueFromUserUB()

	std::cout << num << " doubled is: " << num * 2 << '\n';

	return 0;
}
现代编译器应该生成一个警告，因为
getValueFromUserUB
被定义为返回一个
int
但没有提供返回语句。运行这样的程序将产生未定义行为，因为
getValueFromUserUB()
是一个值返回函数，但它不返回值。
在大多数情况下，编译器会检测您是否忘记返回值。但是，在某些复杂的情况下，编译器可能无法正确确定您的函数是否在所有情况下都返回值，因此您不应依赖此功能。
最佳实践
确保您的非 void 返回类型的函数在所有情况下都返回值。
值返回函数未返回值将导致未定义行为。
如果未提供返回语句，函数 main 将隐式返回 0
值返回函数必须通过返回语句返回值这一规则的唯一例外是
main()
函数。如果未提供返回语句，
main()
函数将隐式返回值
0
。话虽如此，最好显式地从
main
返回一个值，既是为了表明您的意图，也是为了与其他函数保持一致性（如果未指定返回值，它们将表现出未定义行为）。
函数只能返回单个值
值返回函数每次被调用时只能向调用者返回一个值。
请注意，返回语句中提供的值不需要是字面值——它可以是任何有效表达式的结果，包括变量，甚至是对另一个返回值的函数的调用。在上面的
getValueFromUser()
示例中，我们返回了一个变量
input
，它保存了用户输入的值。
有各种方法可以解决函数只能返回单个值的限制，我们将在未来的课程中介绍这些方法。
函数作者可以决定返回值的含义
函数返回值的含义由函数作者决定。一些函数使用返回值作为状态码，以指示它们是否成功或失败。其他函数返回一个计算或选定的值。其他函数不返回任何内容（我们将在下一课中看到这些示例）。
由于这里可能性繁多，因此最好用注释来记录您的函数，说明返回值的含义。例如
// Function asks user to enter a value
// Return value is the integer entered by the user from the keyboard
int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input; // return the value the user entered back to the caller
}
复用函数
现在我们可以举一个函数复用的好例子。考虑下面的程序
#include <iostream>

int main()
{
	int x{};
	std::cout << "Enter an integer: ";
	std::cin >> x; 

	int y{};
	std::cout << "Enter an integer: ";
	std::cin >> y; 

	std::cout << x << " + " << y << " = " << x + y << '\n';

	return 0;
}
虽然这个程序可以工作，但它有点多余。事实上，这个程序违反了良好编程的核心原则之一：**不要重复自己**（通常缩写为 **DRY**）。
为什么重复代码不好？如果我们要将文本“输入一个整数：”更改为其他内容，我们必须在两个位置进行更新。如果我们要初始化 10 个变量而不是 2 个呢？那将是大量的冗余代码（使我们的程序更长，更难理解），并且有很多出现打字错误的空间。
让我们更新这个程序，使用我们上面开发的
getValueFromUser
函数
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
    int x{ getValueFromUser() }; // first call to getValueFromUser
    int y{ getValueFromUser() }; // second call to getValueFromUser

    std::cout << x << " + " << y << " = " << x + y << '\n';

    return 0;
}
此程序生成以下输出：
Enter an integer: 5
Enter an integer: 7
5 + 7 = 12
在此程序中，我们两次调用
getValueFromUser
，一次用于初始化变量
x
，一次用于初始化变量
y
。这使我们不必复制获取用户输入的代码，并减少了出错的可能性。一旦我们知道
getValueFromUser
有效，我们就可以根据需要多次调用它。
这就是模块化编程的精髓：能够编写一个函数，测试它，确保它有效，然后知道我们可以根据需要多次重用它，并且它将继续有效（只要我们不修改函数——此时我们将不得不重新测试它）。
最佳实践
遵循 DRY：“不要重复自己”。如果您需要多次做某事，请考虑如何修改代码以尽可能地消除冗余。变量可用于存储需要多次使用的计算结果（这样我们就不必重复计算）。函数可用于定义我们希望多次执行的语句序列。循环（我们将在后面的章节中介绍）可用于多次执行语句。
像所有最佳实践一样，DRY 旨在作为指导方针，而不是绝对的。读者 Yariv 已经
指出
，当代码被拆分成过小的片段时，DRY 可能会损害整体理解。
题外话…
DRY 的（挖苦的）反义词是 WET（“写两次所有东西”）。
总结
返回值提供了一种让函数向函数调用者返回单个值的方法。
函数提供了一种最小化程序冗余的方法。
小测验时间
问题 #1
检查（不要编译）以下每个程序。确定程序将输出什么，或者程序是否会生成编译器错误。
假设您已关闭“将警告视为错误”。
1a)
#include <iostream>

int return7()
{
    return 7;
}

int return9()
{
    return 9;
}

int main()
{
    std::cout << return7() + return9() << '\n';

    return 0;
}
显示答案
此程序打印数字 16。
1b)
#include <iostream>

int return7()
{
    return 7;

    int return9()
    {
        return 9;
    }
}

int main()
{
    std::cout << return7() + return9() << '\n';

    return 0;
}
显示答案
此程序将无法编译。不允许嵌套函数。
1c)
#include <iostream>

int return7()
{
    return 7;
}

int return9()
{
    return 9;
}

int main()
{
    return7();
    return9();

    return 0;
}
显示答案
此程序编译但没有产生任何输出。函数的返回值没有用于任何目的（因此被丢弃）。
1d)
#include <iostream>

int getNumbers()
{
    return 5;
    return 7;
}

int main()
{
    std::cout << getNumbers() << '\n';
    std::cout << getNumbers() << '\n';

    return 0;
}
显示答案
此程序打印 5 两次（在单独的行上）。每次调用
getNumbers()
函数时，
return 5;
语句都会执行，程序将值 5 返回给调用者。
return 7;
语句永远不会执行。
1e)
#include <iostream>

int return 5()
{
    return 5;
}

int main()
{
    std::cout << return 5() << '\n';

    return 0;
}
显示答案
此程序将无法编译，因为函数名称无效。我们在课程
1.7 -- 关键字和命名标识符
中讨论了命名规则。
问题 #2
“DRY”代表什么，以及为什么它是一种值得遵循的有用实践？
显示答案
DRY 代表“不要重复自己”。这是一种通过编写代码以最大限度地减少冗余的实践。这使您的程序更简洁、更不容易出错且更易于维护。
下一课
2.3
Void 函数（无返回值函数）
返回目录
上一课
2.1
函数简介