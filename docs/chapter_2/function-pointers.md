# 20.1 — 函数指针

20.1 — 函数指针
Alex
2007 年 8 月 8 日，下午 4:52 PDT
2024 年 12 月 14 日
在
12.7 -- 指针简介
课程中，你学习了指针是存储另一个变量地址的变量。函数指针也类似，只不过它们指向函数而不是变量！
考虑以下函数
int foo()
{
    return 5;
}
标识符
foo()
是函数的名称。但函数是什么类型呢？函数有自己的函数类型——在本例中，是一个返回整数且不带参数的函数类型。就像变量一样，函数也存在于内存中分配的地址（使它们成为左值）。
当通过
operator()
调用函数时，执行会跳转到被调用函数的地址。
int foo() // code for foo starts at memory address 0x002717f0
{
    return 5;
}

int main()
{
    foo(); // jump to address 0x002717f0

    return 0;
}
在你的编程生涯中（如果你还没有），你可能会犯一个简单的错误。
#include <iostream>

int foo() // code starts at memory address 0x002717f0
{
    return 5;
}

int main()
{
    std::cout << foo << '\n'; // we meant to call foo(), but instead we're printing foo itself!

    return 0;
}
我们没有调用函数
foo()
并打印返回值，而是无意中将函数
foo
直接发送到了
std::cout
。在这种情况下会发生什么？
当通过名称（不带括号）引用函数时，C++ 会将函数转换为函数指针（持有函数的地址）。然后
operator<<
尝试打印函数指针，但由于
operator<<
不知道如何打印函数指针，因此它会失败。标准规定在这种情况下，
foo
应该转换为
bool
（
operator<<
知道如何打印
bool
）。由于
foo
的函数指针是非空指针，它应该总是评估为布尔
true
。因此，这应该打印。
1
提示
一些编译器（例如 Visual Studio）有一个编译器扩展，可以打印函数的地址。
0x002717f0
如果你的平台不打印函数的地址，而你希望它打印，你可以尝试通过将函数转换为 void 指针并打印它来强制实现。
#include <iostream>

int foo() // code starts at memory address 0x002717f0
{
    return 5;
}

int main()
{
    std::cout << reinterpret_cast<void*>(foo) << '\n'; // Tell C++ to interpret function foo as a void pointer (implementation-defined behavior)

    return 0;
}
这是实现定义的行为，因此它可能不适用于所有平台。
就像可以声明指向普通变量的非常量指针一样，也可以声明指向函数的非常量指针。在本课的其余部分，我们将探讨这些函数指针及其用途。函数指针是一个相当高级的主题，对于那些只想了解 C++ 基础知识的人来说，本课的其余部分可以安全地跳过或略读。
指向函数的指针
创建非 const 函数指针的语法是你在 C++ 中见过的最难看的语法之一。
// fcnPtr is a pointer to a function that takes no arguments and returns an integer
int (*fcnPtr)();
在上面的代码片段中，fcnPtr 是一个指向无参数并返回整数的函数的指针。fcnPtr 可以指向任何匹配此类型的函数。
围绕 *fcnPtr 的括号是必要的，因为优先级原因，
int* fcnPtr()
将被解释为名为 fcnPtr 的函数的向前声明，该函数不带参数并返回指向整数的指针。
要创建一个 const 函数指针，const 放在星号之后。
int (*const fcnPtr)();
如果你将 const 放在 int 之前，那将表示被指向的函数将返回一个 const int。
提示
函数指针的语法可能难以理解。以下文章演示了一种解析此类声明的方法：
https://c-faq.cn/decl/spiral.anderson.html
https://web.archive.org/web/20110818081319/http://ieng9.ucsd.edu/~cs30x/rt_lt.rule.html
将函数赋值给函数指针
函数指针可以用函数初始化（非 const 函数指针可以被赋值一个函数）。就像指向变量的指针一样，我们也可以使用 &foo 来获取指向 foo 的函数指针。
int foo()
{
    return 5;
}

int goo()
{
    return 6;
}

int main()
{
    int (*fcnPtr)(){ &foo }; // fcnPtr points to function foo
    fcnPtr = &goo; // fcnPtr now points to function goo

    return 0;
}
一个常见的错误是这样做：
fcnPtr = goo();
这试图将对函数 goo() 的调用（类型为
int
）的返回值赋给 fcnPtr（它期望一个类型为
int(*)()
的值），这不是我们想要的。我们希望 fcnPtr 被赋值为函数 goo 的地址，而不是函数 goo() 的返回值。因此不需要括号。
注意，函数指针的类型（参数和返回类型）必须与函数的类型匹配。以下是一些示例：
// function prototypes
int foo();
double goo();
int hoo(int x);

// function pointer initializers
int (*fcnPtr1)(){ &foo };    // okay
int (*fcnPtr2)(){ &goo };    // wrong -- return types don't match!
double (*fcnPtr4)(){ &goo }; // okay
fcnPtr1 = &hoo;              // wrong -- fcnPtr1 has no parameters, but hoo() does
int (*fcnPtr3)(int){ &hoo }; // okay
与基本类型不同，C++ **会** 在需要时隐式地将函数转换为函数指针（因此你不需要使用取地址运算符 (&) 来获取函数的地址）。但是，函数指针不会转换为 void 指针，反之亦然（尽管某些编译器如 Visual Studio 可能会允许这样做）。
// function prototypes
	int foo();

	// function initializations
	int (*fcnPtr5)() { foo }; // okay, foo implicitly converts to function pointer to foo
	void* vPtr { foo };       // not okay, though some compilers may allow
函数指针也可以初始化或赋值为 nullptr。
int (*fcnptr)() { nullptr }; // okay
使用函数指针调用函数
使用函数指针的另一个主要功能是使用它实际调用函数。有两种方法可以做到这一点。第一种是通过显式解引用：
int foo(int x)
{
    return x;
}

int main()
{
    int (*fcnPtr)(int){ &foo }; // Initialize fcnPtr with function foo
    (*fcnPtr)(5); // call function foo(5) through fcnPtr.

    return 0;
}
第二种方式是通过隐式解引用：
int foo(int x)
{
    return x;
}

int main()
{
    int (*fcnPtr)(int){ &foo }; // Initialize fcnPtr with function foo
    fcnPtr(5); // call function foo(5) through fcnPtr.

    return 0;
}
如你所见，隐式解引用方法看起来就像一个普通的函数调用——这正是你所期望的，因为普通函数名无论如何都是指向函数的指针！然而，一些旧的编译器不支持隐式解引用方法，但所有现代编译器都应该支持。
另请注意，由于函数指针可以设置为 nullptr，因此在调用它之前断言或有条件地测试你的函数指针是否为空指针是个好主意。就像普通指针一样，解引用空函数指针会导致未定义行为。
int foo(int x)
{
    return x;
}

int main()
{
    int (*fcnPtr)(int){ &foo }; // Initialize fcnPtr with function foo
    if (fcnPtr) // make sure fcnPtr isn't a null pointer    
        fcnPtr(5); // otherwise this will lead to undefined behavior

    return 0;
}
通过函数指针调用的函数不支持默认参数
高级
当编译器遇到带有或不带默认参数的普通函数调用时，它会重写函数调用以包含默认参数。此过程发生在编译时，因此只能应用于可在编译时解析的函数。
然而，当通过函数指针调用函数时，它在运行时解析。在这种情况下，不会重写函数调用以包含默认参数。
关键见解
因为解析发生在运行时，所以当通过函数指针调用函数时，默认参数不会被解析。
这意味着我们可以使用函数指针来消除函数调用中的歧义，否则该调用会因为默认参数而产生歧义。在下面的示例中，我们展示了两种实现方法：
#include <iostream>

void print(int x)
{
    std::cout << "print(int)\n";
}

void print(int x, int y = 10)
{
    std::cout << "print(int, int)\n";
}

int main()
{
//    print(1); // ambiguous function call

    // Deconstructed method
    using vnptr = void(*)(int); // define a type alias for a function pointer to a void(int) function
    vnptr pi { print }; // initialize our function pointer with function print
    pi(1); // call the print(int) function through the function pointer

    // Concise method
    static_cast<void(*)(int)>(print)(1); // call void(int) version of print with argument 1
    
    return 0;
}
将函数作为参数传递给其他函数
使用函数指针最有用的事情之一是，将一个函数作为参数传递给另一个函数。用作另一个函数参数的函数有时被称为**回调函数**。
考虑这样一种情况：你正在编写一个函数来执行某项任务（例如对数组进行排序），但你希望用户能够定义该任务的特定部分如何执行（例如数组是按升序还是降序排序）。让我们更详细地研究一下这个专门应用于排序的问题，作为一个可以推广到其他类似问题的示例。
许多基于比较的排序算法都基于类似的概念：排序算法遍历数字列表，对成对的数字进行比较，并根据这些比较的结果重新排列数字。因此，通过改变比较方式，我们可以在不影响排序代码其余部分的情况下改变算法的排序方式。
这是我们上一课的选择排序例程：
#include <utility> // for std::swap

void SelectionSort(int* array, int size)
{
    if (!array)
        return;

    // Step through each element of the array
    for (int startIndex{ 0 }; startIndex < (size - 1); ++startIndex)
    {
        // smallestIndex is the index of the smallest element we've encountered so far.
        int smallestIndex{ startIndex };
 
        // Look for smallest element remaining in the array (starting at startIndex+1)
        for (int currentIndex{ startIndex + 1 }; currentIndex < size; ++currentIndex)
        {
            // If the current element is smaller than our previously found smallest
            if (array[smallestIndex] > array[currentIndex]) // COMPARISON DONE HERE
            {
                // This is the new smallest number for this iteration
                smallestIndex = currentIndex;
            }
        }
 
        // Swap our start element with our smallest element
        std::swap(array[startIndex], array[smallestIndex]);
    }
}
让我们用一个函数来替换那个比较，进行比较。因为我们的比较函数将比较两个整数并返回一个布尔值来指示元素是否应该交换，它将看起来像这样：
bool ascending(int x, int y)
{
    return x > y; // swap if the first element is greater than the second
}
这是我们使用 `ascending()` 函数进行比较的选择排序例程。
#include <utility> // for std::swap

void SelectionSort(int* array, int size)
{
    if (!array)
        return;

    // Step through each element of the array
    for (int startIndex{ 0 }; startIndex < (size - 1); ++startIndex)
    {
        // smallestIndex is the index of the smallest element we've encountered so far.
        int smallestIndex{ startIndex };
 
        // Look for smallest element remaining in the array (starting at startIndex+1)
        for (int currentIndex{ startIndex + 1 }; currentIndex < size; ++currentIndex)
        {
            // If the current element is smaller than our previously found smallest
            if (ascending(array[smallestIndex], array[currentIndex])) // COMPARISON DONE HERE
            {
                // This is the new smallest number for this iteration
                smallestIndex = currentIndex;
            }
        }
 
        // Swap our start element with our smallest element
        std::swap(array[startIndex], array[smallestIndex]);
    }
}
现在，为了让调用者决定如何进行排序，我们不再使用我们自己硬编码的比较函数，而是允许调用者提供他们自己的排序函数！这是通过函数指针完成的。
因为调用者的比较函数将比较两个整数并返回一个布尔值，所以指向此类函数的指针将如下所示：
bool (*comparisonFcn)(int, int);
因此，我们将允许调用者将指向其所需比较函数的指针作为第三个参数传递给我们的排序例程，然后我们将使用调用者的函数进行比较。
这是一个选择排序的完整示例，它使用函数指针参数进行用户定义的比较，以及如何调用它的示例：
#include <utility> // for std::swap
#include <iostream>

// Note our user-defined comparison is the third parameter
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int))
{
    if (!array || !comparisonFcn)
        return;

    // Step through each element of the array
    for (int startIndex{ 0 }; startIndex < (size - 1); ++startIndex)
    {
        // bestIndex is the index of the smallest/largest element we've encountered so far.
        int bestIndex{ startIndex };
 
        // Look for smallest/largest element remaining in the array (starting at startIndex+1)
        for (int currentIndex{ startIndex + 1 }; currentIndex < size; ++currentIndex)
        {
            // If the current element is smaller/larger than our previously found smallest
            if (comparisonFcn(array[bestIndex], array[currentIndex])) // COMPARISON DONE HERE
            {
                // This is the new smallest/largest number for this iteration
                bestIndex = currentIndex;
            }
        }
 
        // Swap our start element with our smallest/largest element
        std::swap(array[startIndex], array[bestIndex]);
    }
}

// Here is a comparison function that sorts in ascending order
// (Note: it's exactly the same as the previous ascending() function)
bool ascending(int x, int y)
{
    return x > y; // swap if the first element is greater than the second
}

// Here is a comparison function that sorts in descending order
bool descending(int x, int y)
{
    return x < y; // swap if the second element is greater than the first
}

// This function prints out the values in the array
void printArray(int* array, int size)
{
    if (!array)
        return;

    for (int index{ 0 }; index < size; ++index)
    {
        std::cout << array[index] << ' ';
    }
    
    std::cout << '\n';
}

int main()
{
    int array[9]{ 3, 7, 9, 5, 6, 1, 8, 2, 4 };

    // Sort the array in descending order using the descending() function
    selectionSort(array, 9, descending);
    printArray(array, 9);

    // Sort the array in ascending order using the ascending() function
    selectionSort(array, 9, ascending);
    printArray(array, 9);

    return 0;
}
这个程序产生的结果是
9 8 7 6 5 4 3 2 1
1 2 3 4 5 6 7 8 9
是不是很酷？我们已经赋予调用者控制我们的选择排序工作方式的能力。
调用者甚至可以定义自己的“奇怪”比较函数：
bool evensFirst(int x, int y)
{
	// if x is even and y is odd, x goes first (no swap needed)
	if ((x % 2 == 0) && !(y % 2 == 0))
		return false;
 
	// if x is odd and y is even, y goes first (swap needed)
	if (!(x % 2 == 0) && (y % 2 == 0))
		return true;

        // otherwise sort in ascending order
	return ascending(x, y);
}

int main()
{
    int array[9]{ 3, 7, 9, 5, 6, 1, 8, 2, 4 };

    selectionSort(array, 9, evensFirst);
    printArray(array, 9);

    return 0;
}
以上片段产生以下结果：
2 4 6 8 1 3 5 7 9
如你所见，在这种情况下使用函数指针提供了一种很好的方式，允许调用者将自己的功能“挂钩”到你之前编写和测试过的代码中，这有助于促进代码重用！以前，如果你想按降序排列一个数组，按升序排列另一个数组，你需要多个版本的排序例程。现在你可以有一个版本，可以按调用者希望的任何方式进行排序！
注意：如果函数参数是函数类型，它将被转换为指向该函数类型的指针。这意味着
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int))
可以等效地写成
void selectionSort(int* array, int size, bool comparisonFcn(int, int))
这只适用于函数参数，因此用途有限。对于非函数参数，后者被解释为前向声明。
bool (*ptr)(int, int); // definition of function pointer ptr
    bool fcn(int, int);    // forward declaration of function fcn
提供默认函数
如果你允许调用者传入一个函数作为参数，那么提供一些标准函数供调用者使用通常会很方便。例如，在上面的选择排序示例中，提供 ascending() 和 descending() 函数以及 selectionSort() 函数将使调用者的生活更轻松，因为他们不必每次都重写 ascending() 或 descending()。
你甚至可以将其中一个设置为默认参数。
// Default the sort to ascending sort
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int) = ascending);
在这种情况下，只要用户正常调用 `selectionSort` (而不是通过函数指针)，`comparisonFcn` 参数就会默认为 `ascending`。你需要确保 `ascending` 函数在此之前已声明，否则编译器会报错，因为它不知道 `ascending` 是什么。
使用类型别名美化函数指针
让我们面对现实吧——指向函数的指针的语法很丑陋。然而，类型别名可以用来使指向函数的指针看起来更像普通变量。
using ValidateFunction = bool(*)(int, int);
这定义了一个名为“ValidateFunction”的类型别名，它是一个指向函数的指针，该函数接受两个 int 并返回一个 bool。
现在，无需这样做：
bool validate(int x, int y, bool (*fcnPtr)(int, int)); // ugly
你可以这样做：
bool validate(int x, int y, ValidateFunction pfcn) // clean
使用 std::function
定义和存储函数指针的另一种方法是使用 `std::function`，它是标准库 `
` 头文件的一部分。要使用此方法定义函数指针，请声明一个 `std::function` 对象，如下所示：
#include <functional>
bool validate(int x, int y, std::function<bool(int, int)> fcn); // std::function method that returns a bool and takes two int parameters
如你所见，返回类型和参数都放在尖括号内，参数则放在括号内。如果没有参数，括号可以留空。
使用 `std::function` 更新我们之前的示例
#include <functional>
#include <iostream>

int foo()
{
    return 5;
}

int goo()
{
    return 6;
}

int main()
{
    std::function<int()> fcnPtr{ &foo }; // declare function pointer that returns an int and takes no parameters
    fcnPtr = &goo; // fcnPtr now points to function goo
    std::cout << fcnPtr() << '\n'; // call the function just like normal

    std::function fcnPtr2{ &foo }; // can also use CTAD to infer template arguments

    return 0;
}
类型别名 `std::function` 有助于提高可读性。
using ValidateFunctionRaw = bool(*)(int, int); // type alias to raw function pointer
using ValidateFunction = std::function<bool(int, int)>; // type alias to std::function
另请注意，`std::function` 只允许通过隐式解引用（例如 `fcnPtr()`）调用函数，而不允许通过显式解引用（例如 `(*fcnPtr)()`）调用函数。
在定义类型别名时，我们必须显式指定任何模板参数。在这种情况下，我们不能使用 CTAD，因为没有初始化器可以从中推导出模板参数。
函数指针的类型推断
就像 `auto` 关键字可以用来推断普通变量的类型一样，`auto` 关键字也可以推断函数指针的类型。
#include <iostream>

int foo(int x)
{
	return x;
}

int main()
{
	auto fcnPtr{ &foo };
	std::cout << fcnPtr(5) << '\n';

	return 0;
}
这与你所期望的完全一样，而且语法非常简洁。缺点是，当然，关于函数参数类型和返回类型的所有细节都隐藏起来了，因此在使用函数调用或使用其返回值时更容易出错。
总结
函数指针主要在你想将函数存储在数组（或其他结构）中，或者需要将函数作为参数传递给另一个函数时非常有用。因为声明函数指针的原始语法丑陋且容易出错，我们推荐使用 `std::function`。在函数指针类型只使用一次的地方（例如，单个参数或返回值），可以直接使用 `std::function`。在函数指针类型多次使用的地方，`std::function` 的类型别名是更好的选择（以避免重复自己）。
小测验时间
在这个测验中，我们将使用函数指针编写一个我们基本计算器的版本。
1a) 编写一个简短的程序，要求用户输入两个整数和一个数学运算符（'+'、'-'、'*'、'/'）。确保用户输入有效的运算符。
显示答案
#include <iostream>

int getInteger()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;
    return x;
}

char getOperation()
{
    char op{};

    do
    {   
        std::cout << "Enter an operation ('+', '-', '*', '/'): ";
        std::cin >> op;
    }
    while (op!='+' && op!='-' && op!='*' && op!='/');

    return op;
}

int main()
{
    int x{ getInteger() };
    char op{ getOperation() };
    int y{ getInteger() };

    return 0;
}
1b) 编写名为 add()、subtract()、multiply() 和 divide() 的函数。这些函数应接受两个整数参数并返回一个整数。
显示答案
int add(int x, int y)
{
    return x + y;
}

int subtract(int x, int y)
{
    return x - y;
}

int multiply(int x, int y)
{
    return x * y;
}

int divide(int x, int y)
{
    return x / y;
}
1c) 创建一个名为 `ArithmeticFunction` 的类型别名，用于指向接受两个整数参数并返回整数的函数。使用 `std::function`，并包含适当的头文件。
显示答案
#include <functional>
using ArithmeticFunction = std::function<int(int, int)>;
1d) 编写一个名为 `getArithmeticFunction()` 的函数，它接受一个运算符字符并返回相应的函数指针。
显示答案
ArithmeticFunction getArithmeticFunction(char op)
{
    switch (op)
    {
    case '+': return &add;
    case '-': return &subtract;
    case '*': return &multiply;
    case '/': return &divide;
    }

    return nullptr;
}
1e) 修改你的 `main()` 函数来调用 `getArithmeticFunction()`。使用你的输入调用该函数的返回值并打印结果。
显示答案
#include <iostream>

int main()
{
    int x{ getInteger() };
    char op{ getOperation() };
    int y{ getInteger() };

    ArithmeticFunction fcn{ getArithmeticFunction(op) };
    if (fcn)
        std::cout << x << ' ' << op << ' ' << y << " = " << fcn(x, y) << '\n';

    return 0;
}
这是完整的程序：
显示答案
#include <iostream>
#include <functional>

int getInteger()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;
    return x;
}

char getOperation()
{
    char op{};

    do
    {   
        std::cout << "Enter an operation ('+', '-', '*', '/'): ";
        std::cin >> op;
    }
    while (op!='+' && op!='-' && op!='*' && op!='/');

    return op;
}

int add(int x, int y)
{
    return x + y;
}

int subtract(int x, int y)
{
    return x - y;
}

int multiply(int x, int y)
{
    return x * y;
}

int divide(int x, int y)
{
    return x / y;
}

using ArithmeticFunction = std::function<int(int, int)>;

ArithmeticFunction getArithmeticFunction(char op)
{
    switch (op)
    {
    case '+': return &add;
    case '-': return &subtract;
    case '*': return &multiply;
    case '/': return &divide;
    }

    return nullptr;
}

int main()
{
    int x{ getInteger() };
    char op{ getOperation() };
    int y{ getInteger() };

    ArithmeticFunction fcn{ getArithmeticFunction(op) };
    if (fcn)
        std::cout << x << ' ' << op << ' ' << y << " = " << fcn(x, y) << '\n';

    return 0;
}
下一课
20.2
栈和堆
返回目录
上一课
19.5
空指针