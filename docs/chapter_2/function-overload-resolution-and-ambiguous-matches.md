# 11.3 — 函数重载决议与歧义匹配

11.3 — 函数重载决议与歧义匹配
Alex
2021年6月17日，太平洋夏令时下午5:44
2025年1月17日
在上一课（
11.2 -- 函数重载区分
）中，我们讨论了函数的哪些属性用于区分彼此重载的函数。如果一个重载函数没有与同名的其他重载函数正确区分，那么编译器将发出编译错误。
然而，拥有一组区分开的重载函数只是故事的一半。当进行任何函数调用时，编译器还必须确保能够找到匹配的函数声明。
对于非重载函数（具有唯一名称的函数），只有一个函数可能匹配函数调用。该函数要么匹配（或者在应用类型转换后可以匹配），要么不匹配（并导致编译错误）。对于重载函数，可能有许多函数可以匹配函数调用。由于函数调用只能解析为其中之一，因此编译器必须确定哪个重载函数是最佳匹配。将函数调用与特定重载函数匹配的过程称为
重载决议
。
在函数参数类型和函数形参类型完全匹配的简单情况下，这（通常）是直接的。
#include <iostream>

void print(int x)
{
     std::cout << x << '\n';
}

void print(double d)
{
     std::cout << d << '\n';
}

int main()
{
     print(5); // 5 is an int, so this matches print(int)
     print(6.7); // 6.7 is a double, so this matches print(double)

     return 0;
}
但是，在函数调用中的实参类型与任何重载函数中的形参类型不完全匹配的情况下会发生什么呢？例如：
#include <iostream>

void print(int x)
{
     std::cout << x << '\n';
}

void print(double d)
{
     std::cout << d << '\n';
}

int main()
{
     print('a'); // char does not match int or double, so what happens?
     print(5L); // long does not match int or double, so what happens?

     return 0;
}
仅仅因为这里没有完全匹配，并不意味着找不到匹配项——毕竟，一个
char
或
long
可以隐式类型转换为
int
或
double
。但在每种情况下，哪种转换是最好的呢？
在本课中，我们将探讨编译器如何将给定的函数调用与特定的重载函数匹配。
解析重载函数调用
当对重载函数进行函数调用时，编译器会按顺序执行一系列规则，以确定（如果有）哪个重载函数是最佳匹配（我们将在下面的下一节中介绍这些步骤）。
在每个步骤中，编译器都会对函数调用中的实参应用许多不同的类型转换。对于应用的每个转换，编译器都会检查是否有任何重载函数现在是匹配项。在所有不同的类型转换都已应用并检查了匹配项之后，该步骤就完成了。结果将是三种可能结果之一：
没有找到匹配函数。编译器移动到序列中的下一个步骤。
找到一个匹配函数。此函数被认为是最佳匹配。匹配过程现在完成，后续步骤不执行。
找到多个匹配函数。编译器将发出歧义匹配编译错误。我们稍后将进一步讨论这种情况。
如果编译器在未找到匹配项的情况下到达整个序列的末尾，它将生成一个编译错误，指出无法为该函数调用找到匹配的重载函数。
参数匹配序列
步骤1）编译器尝试查找精确匹配。这分两个阶段进行。首先，编译器将查看是否存在一个重载函数，其中函数调用中实参的类型与重载函数中形参的类型完全匹配。例如：
void foo(int)
{
}

void foo(double)
{
}

int main()
{
    foo(0);   // exact match with foo(int)
    foo(3.4); // exact match with foo(double)

    return 0;
}
因为函数调用
foo(0)
中的
0
是
int
类型，所以编译器将查找是否已声明了
foo(int)
重载。既然已经声明，编译器确定
foo(int)
是一个精确匹配。
其次，编译器将对函数调用中的实参应用一些平凡转换。
平凡转换
是一组特定的转换规则，它们将为了查找匹配而修改类型（不修改值）。这包括：
左值到右值转换
限定符转换（例如，非const到const）
非引用到引用转换
例如
void foo(const int)
{
}

void foo(const double&) // double& is a reference to a double
{
}

int main()
{
    int x { 1 };
    foo(x); // x trivially converted from int to const int

    double d { 2.3 };
    foo(d); // d trivially converted from double to const double& (non-ref to ref conversion)

    return 0;
}
在上面的例子中，我们调用了
foo(x)
，其中
x
是一个
int
。编译器将把
x
从
int
平凡转换为
const int
，然后它与
foo(const int)
匹配。我们还调用了
foo(d)
，其中
d
是一个
double
。编译器将把
d
从
double
平凡转换为
const double&
，然后它与
foo(const double&)
匹配。
相关内容
我们在课程
12.3 -- 左值引用
中介绍引用。
通过平凡转换实现的匹配被认为是精确匹配。这意味着以下程序会导致歧义匹配：
void foo(int)
{
}

void foo(const int&) // int& is a reference to a int
{
}

int main()
{
    int x { 1 };
    foo(x); // ambiguous match with foo(int) and foo(const int&)

    return 0;
}
步骤2）如果未找到精确匹配，编译器会尝试通过对参数应用数值提升来查找匹配项。在课程（
10.1 -- 隐式类型转换
）中，我们介绍了某些窄整型和浮点型如何自动提升为更宽的类型，例如
int
或
double
。如果在数值提升后找到了匹配项，则函数调用将被解析。
例如
void foo(int)
{
}

void foo(double)
{
}

int main()
{
    foo('a');  // promoted to match foo(int)
    foo(true); // promoted to match foo(int)
    foo(4.5f); // promoted to match foo(double)

    return 0;
}
对于
foo('a')
，由于在前一步中无法找到
foo(char)
的精确匹配，编译器将
char 'a'
提升为
int
，并查找匹配。这与
foo(int)
匹配，因此函数调用解析为
foo(int)
。
步骤3）如果通过数值提升未找到匹配项，编译器会尝试通过对实参应用数值转换（
10.3 -- 数值转换
）来查找匹配项。
例如
#include <string> // for std::string

void foo(double)
{
}

void foo(std::string)
{
}

int main()
{
    foo('a'); // 'a' converted to match foo(double)

    return 0;
}
在这种情况下，因为没有 `foo(char)`（精确匹配），也没有 `foo(int)`（提升匹配），所以 `'a'` 被数值转换为 `double` 并与 `foo(double)` 匹配。
关键见解
通过应用数值提升进行的匹配优先于通过应用数值转换进行的任何匹配。
步骤4）如果通过数值转换未找到匹配项，编译器会尝试通过任何用户定义的转换来查找匹配项。尽管我们尚未介绍用户定义的转换，但某些类型（例如类）可以定义到其他类型的转换，这些转换可以隐式调用。这里有一个例子，只是为了说明这一点：
// We haven't covered classes yet, so don't worry if this doesn't make sense
class X // this defines a new type called X
{
public:
    operator int() { return 0; } // Here's a user-defined conversion from X to int
};

void foo(int)
{
}

void foo(double)
{
}

int main()
{
    X x; // Here, we're creating an object of type X (named x)
    foo(x); // x is converted to type int using the user-defined conversion from X to int

    return 0;
}
在此示例中，编译器将首先检查是否存在
foo(X)
的精确匹配。我们尚未定义。接下来，编译器将检查
x
是否可以进行数值提升，但它不能。然后编译器将检查
x
是否可以进行数值转换，它也无法。最后，编译器将查找任何用户定义的转换。因为我们已经定义了从
X
到
int
的用户定义转换，所以编译器会将
X
转换为
int
以匹配
foo(int)
。
应用用户定义转换后，编译器可能会应用额外的隐式提升或转换来寻找匹配。因此，如果我们的用户定义转换是类型`char`而不是`int`，编译器将使用用户定义转换到`char`，然后将结果提升为`int`以匹配。
相关内容
我们在课程
21.11 -- 重载类型转换运算符
中讨论如何为类类型创建用户定义转换（通过重载类型转换运算符）。
致进阶读者
类的构造函数也充当从其他类型到该类类型的用户定义转换，可以在此步骤中使用以查找匹配函数。
步骤5）如果通过用户定义转换未找到匹配项，编译器将查找使用省略号的匹配函数。
相关内容
我们在
20.5 -- 省略号（以及为何避免它们）
课程中涵盖省略号。
步骤6）如果此时尚未找到匹配项，编译器将放弃并发出编译错误，指出无法找到匹配函数。
歧义匹配
对于非重载函数，每个函数调用要么解析为一个函数，要么找不到匹配项，编译器将发出编译错误。
void foo()
{
}

int main()
{
     foo(); // okay: match found
     goo(); // compile error: no match found

     return 0;
}
对于重载函数，还有第三种可能的结果：可能找到“歧义匹配”。当编译器在同一步骤中找到两个或多个可以匹配的函数时，就会发生
歧义匹配
。当发生这种情况时，编译器将停止匹配并发出编译错误，指出它找到了一个歧义函数调用。
由于每个重载函数都必须被区分才能编译，您可能会想，函数调用怎么可能导致多个匹配呢？让我们看一个例子来解释这一点：
void foo(int)
{
}

void foo(double)
{
}

int main()
{
    foo(5L); // 5L is type long

    return 0;
}
由于字面量
5L
是
long
类型，编译器会首先查找是否能找到
foo(long)
的精确匹配，但找不到。接下来，编译器会尝试数值提升，但
long
类型的值不能提升，因此这里也没有匹配。
此后，编译器将尝试通过对`long`参数应用数值转换来查找匹配项。在检查所有数值转换规则的过程中，编译器将找到两个潜在的匹配项。如果`long`参数被数值转换为`int`，则函数调用将匹配`foo(int)`。如果`long`参数被转换为`double`，则它将匹配`foo(double)`。由于通过数值转换找到了两个可能的匹配项，因此该函数调用被认为是歧义的。
在 Visual Studio 2019 上，这会导致以下错误消息：
error C2668: 'foo': ambiguous call to overloaded function
message : could be 'void foo(double)'
message : or       'void foo(int)'
message : while trying to match the argument list '(long)'
关键见解
如果编译器在给定步骤中找到多个匹配项，则会导致歧义函数调用。这意味着在给定步骤中，任何匹配项都不比同一步骤中的任何其他匹配项更好。
以下是另一个导致歧义匹配的示例：
void foo(unsigned int)
{
}

void foo(float)
{
}

int main()
{ 
    foo(0);       // int can be numerically converted to unsigned int or to float
    foo(3.14159); // double can be numerically converted to unsigned int or to float

    return 0;
}
尽管您可能期望`0`解析为`foo(unsigned int)`，`3.14159`解析为`foo(float)`，但这两个调用都导致了歧义匹配。`int`值`0`可以数值转换为`unsigned int`或`float`，因此任一重载都同样匹配，结果是歧义函数调用。
同样适用于将`double`转换为`float`或`unsigned int`。两者都是数值转换，因此任一重载都同样匹配，结果再次具有歧义性。
致进阶读者
默认参数也可能导致歧义匹配。我们将在课程
11.5 -- 默认参数
中介绍此类情况。
解决歧义匹配
由于歧义匹配是编译时错误，因此在程序编译之前需要消除歧义匹配。有几种方法可以解决歧义匹配：
通常，最好的方法是简单地定义一个新的重载函数，该函数采用与您尝试调用该函数时完全相同的参数类型。然后 C++ 将能够为函数调用找到精确匹配。
或者，显式地将歧义参数进行类型转换，使其与您要调用的函数类型匹配。例如，要在上面的示例中使`foo(0)`匹配`foo(unsigned int)`，您可以这样做：
int x{ 0 };
foo(static_cast<unsigned int>(x)); // will call foo(unsigned int)
如果您的参数是字面量，您可以使用字面量后缀来确保您的字面量被解释为正确的类型。
foo(0u); // will call foo(unsigned int) since 'u' suffix is unsigned int, so this is now an exact match
最常用后缀的列表可以在课程
5.2 -- 字面量
中找到。
具有多个参数的函数匹配
如果存在多个实参，编译器会依次对每个实参应用匹配规则。选择的函数是每个实参的匹配程度至少与其他所有函数一样好，并且至少有一个实参的匹配程度优于所有其他函数。换句话说，选择的函数必须至少对一个形参比所有其他候选函数提供更好的匹配，并且对所有其他形参没有更差的匹配。
如果找到这样的函数，则它明确且无歧义地是最佳选择。如果找不到这样的函数，则该调用将被视为歧义（或不匹配）。
例如
#include <iostream>

void print(char, int)
{
	std::cout << 'a' << '\n';
}

void print(char, double)
{
	std::cout << 'b' << '\n';
}

void print(char, float)
{
	std::cout << 'c' << '\n';
}

int main()
{
	print('x', 'a');

	return 0;
}
在上面的程序中，所有函数都精确匹配第一个参数。然而，顶部的函数通过提升匹配第二个参数，而其他函数需要转换。因此，`print(char, int)`是明确无歧义的最佳匹配。
下一课
11.4
删除函数
返回目录
上一课
11.2
函数重载区分