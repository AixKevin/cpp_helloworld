# 21.11 — 重载类型转换

21.11 — 重载类型转换
Alex
2007年10月30日，太平洋夏令时下午12:54
2025年3月14日
在课程
10.6 -- 显式类型转换（强制类型转换）和static_cast
中，你学习了C++允许你将一种数据类型转换为另一种。以下示例展示了一个int如何被转换为一个double
int n{ 5 };
auto d{ static_cast<double>(n) }; // int cast to a double
C++已经知道如何在内置数据类型之间进行转换。然而，默认情况下，C++不知道如何转换我们程序中定义的任何类。
在课程
14.16 -- 转换构造函数和explicit关键字
中，我们展示了如何使用转换构造函数从另一种类型的对象创建类类型对象。但这仅适用于目标类型是可修改的类类型，以便添加这样的构造函数。如果不是这种情况呢？
请看下面的类
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};
这个类非常简单：它将一些美分（cents）作为一个整数存储，并提供了访问函数来获取和设置美分数量。它还提供了一个构造函数，用于将`int`转换为`Cents`。
如果我们可以将`int`转换为`Cents`（通过构造函数），那么我们可能也希望提供一种方式将`Cents`转换回`int`。在某些情况下，这可能不合意，但在本例中它是有意义的。
作者注
一首诗
将我们的整数转换为美分
将使用一个同意的构造函数
当然，美分转整数也说得通
但编译器会报错并阻止。
为了允许这种转换事件
我们给予编译器我们的同意
然后定义如何，出于所有意图
我们可以转换这些类型的内容。
那么绕过
编译器静态类型防御的语法是什么？
我们很快就会详细说明，因此
你将不再被蒙在鼓里。
一种不太好的方法是使用转换函数。在这个例子中，我们使用成员函数`getCents()`将我们的`Cents`变量“转换”回一个`int`，这样我们就可以使用`printInt()`打印它。
#include <iostream>

void printInt(int value)
{
    std::cout << value;
}

int main()
{
    Cents cents{ 7 };
    printInt(cents.getCents()); // print 7

    std::cout << '\n';

    return 0;
}
虽然这个函数能产生我们想要的结果，但它并不是真正的转换，因为编译器不会理解它应该使用这个函数进行类型转换或隐式转换。这也意味着如果我们进行大量的 `Cents` 到 `int` 的转换，我们的代码将充斥着对 `getCents()` 的调用，这很混乱。
我们还能做什么？
重载类型转换
这就是重载类型转换运算符发挥作用的地方。这种类型转换可以被显式地（通过强制类型转换）或隐式地（由编译器）用于按需执行转换。
让我们展示如何重载类型转换来定义从`Cents`到`int`的转换
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    // Overloaded int cast
    operator int() const { return m_cents; }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};
为此，我们编写了一个新的重载运算符，名为`operator int()`。请注意，在`operator`单词和我们正在转换的类型之间有一个空格。
这里有几点值得注意：
重载类型转换必须是非静态成员，并且应该是`const`，以便可以与`const`对象一起使用。
重载类型转换没有显式参数，因为无法将显式参数传递给它们。它们仍然有一个隐藏的`*this`参数，指向隐式对象（即要转换的对象）。
重载类型转换不声明返回类型。转换的名称（例如 int）用作返回类型，因为它是唯一允许的返回类型。这避免了声明中的冗余。
现在在我们的例子中，我们可以像这样调用`printInt()`
#include <iostream>

int main()
{
    Cents cents{ 7 };
    printInt(cents); // print 7

    std::cout << '\n';

    return 0;
}
编译器首先会注意到函数`printInt()`有一个`int`参数。然后它会注意到变量`cents`不是`int`类型。最后，它会查看我们是否提供了将`Cents`转换为`int`的方法。由于我们提供了，它将调用我们的`operator int()`函数，该函数返回一个`int`，并且返回的`int`将被传递给`printInt()`。
这种类型转换也可以通过`static_cast`显式调用
std::cout << static_cast<int>(cents);
您可以为您希望的任何数据类型提供重载类型转换，包括您自己程序定义的数据类型！
这是一个名为`Dollars`的新类，它提供了重载的`Cents`转换
class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

     // Allow us to convert Dollars into Cents
     operator Cents() const { return Cents{ m_dollars * 100 }; }
};
这允许我们直接将`Dollars`对象转换为`Cents`对象！这使得你可以这样做：
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    // Overloaded int cast
    operator int() const { return m_cents; }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};

class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

    // Allow us to convert Dollars into Cents
    operator Cents() const { return Cents { m_dollars * 100 }; }
};

void printCents(Cents cents)
{
    std::cout << cents; // cents will be implicitly cast to an int here
}

int main()
{
    Dollars dollars{ 9 };
    printCents(dollars); // dollars will be implicitly cast to a Cents here

    std::cout << '\n';

    return 0;
}
因此，这个程序将打印出以下值：
900
这是有道理的，因为9美元就是900美分！
尽管这证明了这种事情是可能的，但在这种情况下，为`Dollars`添加一个转换构造函数（参数类型为`Cents`）实际上是更可取的。我们将在下面讨论原因。
显式类型转换
就像我们可以将构造函数声明为`explicit`以阻止其用于隐式转换一样，我们也可以出于同样的原因将重载类型转换声明为`explicit`。显式类型转换只能通过强制转换（例如`static_cast`）或某种形式的直接初始化（括号或花括号）来调用。在复制初始化时，它们不被考虑。
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    explicit operator int() const { return m_cents; } // now marked as explicit

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};

class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

    operator Cents() const { return Cents { m_dollars * 100 }; }
};

void printCents(Cents cents)
{
//  std::cout << cents;                   // no longer works because cents won't implicit convert to an int
    std::cout << static_cast<int>(cents); // we can use an explicit cast instead
}

int main()
{
    Dollars dollars{ 9 };
    printCents(dollars); // implicit conversion from Dollars to Cents okay because its not marked as explicit

    std::cout << '\n';

    return 0;
}
类型转换通常应标记为显式。但在以下情况下可以例外：当转换能够廉价地转换为类似的自定义类型时。我们的`Dollars::operator Cents()`类型转换未标记为显式，因为没有理由不允许在预期`Cents`的地方使用`Dollars`对象。
最佳实践
就像单参数转换构造函数应该标记为`explicit`一样，类型转换也应该标记为`explicit`，除非要转换的类型与目标类型本质上是同义的。
何时使用转换构造函数与重载类型转换
重载类型转换和转换构造函数执行类似的功能
转换构造函数是类类型 B 的成员函数，它定义了如何从 A 创建 B。
重载类型转换是类类型 A 的成员函数，它定义了如何将 A 转换为 B。
在这两种情况下，我们都以 A 开头，并以 B 结尾。两者之间的主要区别在于 A 或 B 拥有转换发生的方式。
由于这两种方式都需要定义成员函数，因此它们只能用于可修改的类类型。如果 A 不是可修改的类类型，则不能使用重载类型转换。如果 B 不是可修改的类类型，则不能使用转换构造函数。如果两者都不是可修改的类类型，则需要使用非成员转换函数。
在 A 和 B 都是可修改的类类型的情况下，我们可以使用其中任何一种。但由于我们只需要一种，我们应该优先选择哪一种呢？
通常，转换构造函数优于重载类型转换。在其他条件相同的情况下，一个类类型拥有自己的构造方式，而不是依赖另一个类来创建和初始化它，会更清晰。
最佳实践
在可能的情况下，优先使用转换构造函数，避免使用重载类型转换。
在少数情况下，应改用重载类型转换：
当提供到基本类型的转换时（因为不能为这些类型定义构造函数）。最常见的是，它们用于提供到`bool`的转换，以便在需要将对象用于条件语句时使用。
当转换返回引用或常量引用时。
当提供到您无法添加成员的类型的转换时（例如，转换为`std::vector`，因为您也无法为这些类型定义构造函数）。
当你不希望被构造的类型知道被转换的类型时。这有助于避免循环依赖。
关于最后一点的例子，`std::string`有一个构造函数可以从`std::string_view`创建一个`std::string`。这意味着`
`必须包含`
`。如果`std::string_view`有一个构造函数可以从`std::string`创建一个`std::string_view`，那么`
`就需要包含`
`，这将导致头文件之间的循环依赖。
相反，`std::string`有一个重载类型转换，用于处理从`std::string`到`std::string_view`的转换（这是可以的，因为它已经包含了`
`）。`std::string_view`完全不知道`std::string`，因此不需要包含`
`。通过这种方式，避免了循环依赖。
当针对同一转换同时定义了转换构造函数和重载类型转换时，两者都会在重载解析期间被考虑。根据重载类型转换是否为 const、被转换对象是否为 const，以及使用了何种类型转换或初始化（复制初始化 vs 直接初始化），可能会选择其中一个函数（这可能导致类型转换优先于转换构造函数被选中），或者结果可能不明确（导致编译错误）。因此，您应该避免同时定义可以用于同一转换的重载类型转换和转换构造函数。
最佳实践
当您需要定义如何将类型 A 转换为类型 B 时
如果 B 是可以修改的类类型，则优先使用转换构造函数从 A 创建 B。
否则，如果 A 是可以修改的类类型，则使用重载类型转换将 A 转换为 B。
否则，使用非成员函数将 A 转换为 B。
下一课
21.12
重载赋值运算符
返回目录
上一课
21.10
重载括号运算符