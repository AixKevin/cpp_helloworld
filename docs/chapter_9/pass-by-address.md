# 12.10 — 按地址传递

12.10 — 按地址传递
Alex
2007 年 7 月 25 日，下午 4:14 PDT
2025 年 2 月 13 日
在之前的课程中，我们学习了两种不同的向函数传递参数的方式：按值传递（
2.4 -- 函数参数和实参简介
）和按引用传递（
12.5 -- 按左值引用传递
）。
这是一个示例程序，展示了
std::string
对象按值传递和按引用传递的情况
#include <iostream>
#include <string>

void printByValue(std::string val) // The function parameter is a copy of str
{
    std::cout << val << '\n'; // print the value via the copy
}

void printByReference(const std::string& ref) // The function parameter is a reference that binds to str
{
    std::cout << ref << '\n'; // print the value via the reference
}

int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // pass str by value, makes a copy of str
    printByReference(str); // pass str by reference, does not make a copy of str

    return 0;
}
当我们按值传递参数
str
时，函数参数
val
接收到参数的一个副本。由于参数是参数的副本，对
val
的任何更改都将作用于副本，而不是原始参数。
当我们按引用传递参数
str
时，引用参数
ref
绑定到实际参数。这避免了创建参数的副本。由于我们的引用参数是 const，我们不允许更改
ref
。但是，如果
ref
不是 const，我们对
ref
所做的任何更改都会更改
str
。
在这两种情况下，调用者都提供实际对象 (
str
) 作为参数传递给函数调用。
按地址传递
C++ 提供了第三种向函数传递值的方式，称为按地址传递。使用
按地址传递
，调用者不是提供一个对象作为参数，而是提供一个对象的
地址
（通过指针）。这个指针（持有对象的地址）被复制到被调用函数的指针参数中（该参数现在也持有对象的地址）。然后函数可以解引用该指针以访问其地址被传递的对象。
这是上述程序的一个版本，增加了按地址传递的变体
#include <iostream>
#include <string>

void printByValue(std::string val) // The function parameter is a copy of str
{
    std::cout << val << '\n'; // print the value via the copy
}

void printByReference(const std::string& ref) // The function parameter is a reference that binds to str
{
    std::cout << ref << '\n'; // print the value via the reference
}

void printByAddress(const std::string* ptr) // The function parameter is a pointer that holds the address of str
{
    std::cout << *ptr << '\n'; // print the value via the dereferenced pointer
}

int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // pass str by value, makes a copy of str
    printByReference(str); // pass str by reference, does not make a copy of str
    printByAddress(&str); // pass str by address, does not make a copy of str

    return 0;
}
请注意这三个版本是多么相似。让我们更详细地探讨按地址传递的版本。
首先，因为我们希望
printByAddress()
函数使用按地址传递，所以我们将函数参数设为名为
ptr
的指针。由于
printByAddress()
将以只读方式使用
ptr
，因此
ptr
是指向 const 值的指针。
void printByAddress(const std::string* ptr)
{
    std::cout << *ptr << '\n'; // print the value via the dereferenced pointer
}
在
printByAddress()
函数内部，我们解引用
ptr
参数以访问所指向对象的值。
其次，当函数被调用时，我们不能仅仅传入
str
对象——我们需要传入
str
的地址。最简单的方法是使用取地址运算符 (
&
) 来获取一个持有
str
地址的指针
printByAddress(&str); // use address-of operator (&) to get pointer holding address of str
当此调用执行时，
&str
将创建一个持有
str
地址的指针。然后，作为函数调用的一部分，此地址被复制到函数参数
ptr
中。因为
ptr
现在持有
str
的地址，当函数解引用
ptr
时，它将获得
str
的值，函数将其打印到控制台。
就是这样。
尽管在上面的示例中我们使用取地址运算符来获取
str
的地址，但是如果我们已经有一个持有
str
地址的指针变量，我们可以改用它
int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // pass str by value, makes a copy of str
    printByReference(str); // pass str by reference, does not make a copy of str
    printByAddress(&str); // pass str by address, does not make a copy of str

    std::string* ptr { &str }; // define a pointer variable holding the address of str
    printByAddress(ptr); // pass str by address, does not make a copy of str    

    return 0;
}
命名法
当我们使用
operator&
将变量的地址作为参数传递时，我们说该变量是按地址传递的。
当我们有一个持有对象地址的指针变量，并且我们将该指针作为参数传递给同类型的参数时，我们说该对象是按地址传递的，并且该指针是按值传递的。
按地址传递不会复制所指向的对象
考虑以下语句
std::string str{ "Hello, world!" };
printByAddress(&str); // use address-of operator (&) to get pointer holding address of str
正如我们在
12.5 -- 按左值引用传递
中指出的，复制
std::string
是昂贵的，所以我们希望避免这种情况。当我们按地址传递
std::string
时，我们没有复制实际的
std::string
对象——我们只是将指针（持有对象的地址）从调用者复制到被调用函数。由于地址通常只有 4 或 8 字节，指针也只有 4 或 8 字节，所以复制指针总是很快的。
因此，就像按引用传递一样，按地址传递也很快，并避免了复制参数对象。
按地址传递允许函数修改参数的值
当我们按地址传递一个对象时，函数会收到传递对象的地址，它可以通过解引用来访问。因为这是实际传递的参数对象的地址（而不是对象的副本），如果函数参数是指向非 const 的指针，函数可以通过指针参数修改参数
#include <iostream>

void changeValue(int* ptr) // note: ptr is a pointer to non-const in this example
{
    *ptr = 6; // change the value to 6
}

int main()
{
    int x{ 5 };

    std::cout << "x = " << x << '\n';

    changeValue(&x); // we're passing the address of x to the function

    std::cout << "x = " << x << '\n';

    return 0;
}
这会打印
x = 5
x = 6
正如你所看到的，参数被修改了，并且这种修改在
changeValue()
运行结束后仍然存在。
如果函数不应该修改传入的对象，则函数参数应设为指向 const 的指针
void changeValue(const int* ptr) // note: ptr is now a pointer to a const
{
    *ptr = 6; // error: can not change const value
}
与我们通常不将常规（非指针、非引用）函数参数设为
const
（在
5.1 -- 常量变量（命名常量）
中讨论）的许多原因相同，我们通常也不将指针函数参数设为
const
。让我们提出两个断言
用于使指针函数参数成为 const 指针的
const
关键字提供的价值很小（因为它对调用者没有影响，并且主要用作指针不会改变的文档）。
用于区分指向 const 的指针和可以修改传入对象的指向非 const 的指针的
const
关键字具有重要意义（因为调用者需要知道函数是否可以更改参数的值）。
如果我们只使用非 const 指针函数参数，那么所有
const
的使用都具有重要意义。一旦我们开始为 const 指针函数参数使用
const
，那么就很难判断给定的
const
使用是否具有重要意义。更重要的是，它也使得更难注意到指向非 const 的指针参数。例如
void foo(const char* source, char* dest, int count);             // Using non-const pointers, all consts are significant.
void foo(const char* const source, char* const dest, int count); // Using const pointers, `dest` being a pointer-to-non-const may go unnoticed amongst the sea of spurious consts.
在前一种情况下，很容易看出
source
是指向 const 的指针，而
dest
是指向非 const 的指针。在后一种情况下，很难看出
dest
是指向非 const 的 const 指针，它的指向对象可以被函数修改！
最佳实践
优先使用指向 const 的函数参数，而不是指向非 const 的函数参数，除非函数需要修改传入的对象。
除非有特定原因，否则不要将函数参数设为 const 指针。
空值检查
现在考虑这个看似无害的程序
#include <iostream>

void print(int* ptr)
{
	std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	print(&x);

	int* myPtr {};
	print(myPtr);

	return 0;
}
当程序运行时，它将打印值
5
，然后很可能崩溃。
在对
print(myPtr)
的调用中，
myPtr
是一个空指针，因此函数参数
ptr
也将是一个空指针。当这个空指针在函数体内被解引用时，会导致未定义行为。
当按地址传递参数时，在解引用值之前应注意确保指针不是空指针。一种方法是使用条件语句
#include <iostream>

void print(int* ptr)
{
    if (ptr) // if ptr is not a null pointer
    {
        std::cout << *ptr << '\n';
    }
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
在上面的程序中，我们在解引用
ptr
之前对其进行测试，以确保它不为空。虽然这对于这样简单的函数来说没问题，但在更复杂的函数中，这可能导致冗余逻辑（多次测试 ptr 是否不为空）或函数主要逻辑的嵌套（如果包含在一个块中）。
在大多数情况下，更有效的方法是做相反的事情：测试函数参数是否为空作为前置条件（
9.6 -- 断言和静态断言
），并立即处理负面情况
#include <iostream>

void print(int* ptr)
{
    if (!ptr) // if ptr is a null pointer, early return back to the caller
        return;

    // if we reached this point, we can assume ptr is valid
    // so no more testing or nesting required

    std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
如果永远不应将空指针传递给函数，则可以使用
assert
（我们在
9.6 -- 断言和静态断言
课程中介绍过）代替（或同时使用）（因为断言旨在记录永远不应该发生的事情）
#include <iostream>
#include <cassert>

void print(const int* ptr) // now a pointer to a const int
{
	assert(ptr); // fail the program in debug mode if a null pointer is passed (since this should never happen)

	// (optionally) handle this as an error case in production mode so we don't crash if it does happen
	if (!ptr)
		return;

	std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
优先使用按 (const) 引用传递
请注意，上面示例中的函数
print()
对空值的处理不佳——它实际上只是中止了函数。鉴于此，为什么要允许用户传入空值呢？按引用传递与按地址传递具有相同的优点，并且没有意外解引用空指针的风险。
按 const 引用传递比按地址传递有其他一些优势。
首先，由于按地址传递的对象必须有地址，因此只有左值可以按地址传递（因为右值没有地址）。按 const 引用传递更灵活，因为它既可以接受左值也可以接受右值
#include <iostream>

void printByValue(int val) // The function parameter is a copy of the argument
{
    std::cout << val << '\n'; // print the value via the copy
}

void printByReference(const int& ref) // The function parameter is a reference that binds to the argument
{
    std::cout << ref << '\n'; // print the value via the reference
}

void printByAddress(const int* ptr) // The function parameter is a pointer that holds the address of the argument
{
    std::cout << *ptr << '\n'; // print the value via the dereferenced pointer
}

int main()
{
    printByValue(5);     // valid (but makes a copy)
    printByReference(5); // valid (because the parameter is a const reference)
    printByAddress(&5);  // error: can't take address of r-value

    return 0;
}
其次，按引用传递的语法是自然的，因为我们可以直接传入字面量或对象。而按地址传递，我们的代码会充斥着大量的 & 和 *。
在现代 C++ 中，大多数可以通过按地址传递完成的事情都可以通过其他方法更好地完成。遵循这条常见的格言：“能按引用传递时就按引用传递，必须按地址传递时才按地址传递”。
最佳实践
除非有特定原因，否则优先使用按引用传递而非按地址传递。
下一课
12.11
按地址传递（第二部分）
返回目录
上一课
12.9
指针和常量