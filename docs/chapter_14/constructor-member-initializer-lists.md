# 14.10 — 构造函数成员初始化列表

14.10 — 构造函数成员初始化列表
Alex
2007 年 11 月 13 日，太平洋标准时间上午 10:03
2025 年 2 月 5 日
本课程将继续我们从课程
14.9 -- 构造函数简介
中开始的构造函数介绍。
通过成员初始化列表进行成员初始化
要让构造函数初始化成员，我们使用**成员初始化列表**（通常称为“成员初始化列表”）。不要将此与用于使用值列表初始化聚合的类似名称的“初始化列表”混淆。
成员初始化列表最好通过示例学习。在以下示例中，我们的
Foo(int, int)
构造函数已更新为使用成员初始化列表来初始化
m_x
和
m_y
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo(int x, int y)
        : m_x { x }, m_y { y } // here's our member initialization list
    {
        std::cout << "Foo(" << x << ", " << y << ") constructed\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo{ 6, 7 };
    foo.print();

    return 0;
}
成员初始化列表定义在构造函数参数之后。它以冒号 (:) 开头，然后列出要初始化的每个成员以及该变量的初始化值，用逗号分隔。您必须在此处使用直接初始化形式（最好使用花括号，但圆括号也可以）——使用复制初始化（带等号）在此处不起作用。另请注意，成员初始化列表不以分号结尾。
此程序生成以下输出：
Foo(6, 7) constructed
Foo(6, 7)
当
foo
被实例化时，初始化列表中的成员将用指定的初始化值进行初始化。在这种情况下，成员初始化列表将
m_x
初始化为
x
的值（即
6
），将
m_y
初始化为
y
的值（即
7
）。然后运行构造函数的主体。
调用
print()
成员函数时，您可以看到
m_x
的值仍然是
6
，
m_y
的值仍然是
7
。
成员初始化列表格式
C++ 提供了很大的自由度来根据您的喜好格式化您的成员初始化列表，因为它不关心您将冒号、逗号或空格放在哪里。
以下样式都有效（您在实践中可能会看到所有三种）
Foo(int x, int y) : m_x { x }, m_y { y }
    {
    }
Foo(int x, int y) :
        m_x { x },
        m_y { y }
    {
    }
Foo(int x, int y)
        : m_x { x }
        , m_y { y }
    {
    }
我们建议使用上面的第三种样式
将冒号放在构造函数名称后的行上，因为这可以清晰地将成员初始化列表与函数原型分开。
缩进您的成员初始化列表，以便更容易看到函数名称。
如果成员初始化列表很短/很简单，所有初始化器都可以放在一行上
Foo(int x, int y)
        : m_x { x }, m_y { y }
    {
    }
否则（或者如果您愿意），每个成员和初始化器对可以放在单独的行上（以逗号开头以保持对齐）
Foo(int x, int y)
        : m_x { x }
        , m_y { y }
    {
    }
成员初始化顺序
由于 C++ 标准规定，成员初始化列表中的成员总是按照它们在类中定义的顺序进行初始化（而不是按照它们在成员初始化列表中定义的顺序）。
在上面的示例中，因为
m_x
在类定义中定义在
m_y
之前，所以
m_x
将首先被初始化（即使它没有在成员初始化列表中首先列出）。
因为我们直观地期望变量从左到右初始化，这可能会导致出现细微的错误。考虑以下示例
#include <algorithm> // for std::max
#include <iostream>

class Foo
{
private:
    int m_x{};
    int m_y{};

public:
    Foo(int x, int y)
        : m_y { std::max(x, y) }, m_x { m_y } // issue on this line
    {
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo { 6, 7 };
    foo.print();

    return 0;
}
在上面的示例中，我们的目的是计算传入的初始化值中较大的值（通过
std::max(x, y)
），然后使用此值初始化
m_x
和
m_y
。然而，在作者的机器上，打印出以下结果
Foo(-858993460, 7)
发生了什么？尽管
m_y
在成员初始化列表中首先列出，但由于
m_x
在类中首先定义，
m_x
会首先被初始化。并且
m_x
被初始化为
m_y
的值，而
m_y
尚未初始化。最后，
m_y
被初始化为初始化值中较大的一个。
为了帮助防止此类错误，成员初始化列表中的成员应按照它们在类中定义的顺序进行列出。如果成员未按顺序初始化，某些编译器会发出警告。
最佳实践
成员初始化列表中的成员变量应按照它们在类中定义的顺序进行列出。
最好避免使用其他成员的值来初始化成员（如果可能）。这样，即使您在初始化顺序上犯了错误，也无关紧要，因为初始化值之间没有依赖关系。
成员初始化列表与默认成员初始化器
成员可以通过几种不同的方式初始化
如果成员在成员初始化列表中列出，则使用该初始化值
否则，如果成员具有默认成员初始化器，则使用该初始化值
否则，成员将进行默认初始化。
这意味着如果一个成员既有默认成员初始化器又在构造函数的成员初始化列表中列出，则成员初始化列表的值优先。
这是一个显示所有三种初始化方法的示例
#include <iostream>

class Foo
{
private:
    int m_x {};    // default member initializer (will be ignored)
    int m_y { 2 }; // default member initializer (will be used)
    int m_z;      // no initializer

public:
    Foo(int x)
        : m_x { x } // member initializer list
    {
        std::cout << "Foo constructed\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ", " << m_z << ")\n";
    }
};

int main()
{
    Foo foo { 6 };
    foo.print();

    return 0;
}
在作者的机器上，此输出为
Foo constructed
Foo(6, 2, -858993460)
这是正在发生的事情。当
foo
被构造时，只有
m_x
出现在成员初始化列表中，所以
m_x
首先被初始化为
6
。
m_y
不在成员初始化列表中，但它有一个默认成员初始化器，所以它被初始化为
2
。
m_z
既不在成员初始化列表中，也没有默认成员初始化器，所以它被默认初始化（对于基本类型，这意味着它未初始化）。因此，当我们打印
m_z
的值时，我们得到未定义行为。
构造函数函数体
构造函数函数体通常留空。这是因为我们主要使用构造函数进行初始化，而初始化是通过成员初始化列表完成的。如果只需要做这些，那么构造函数体中就不需要任何语句。
但是，由于构造函数体中的语句在成员初始化列表执行之后执行，我们可以添加语句来执行任何其他所需的设置任务。在上面的示例中，我们向控制台打印一些内容以表明构造函数已执行，但我们可以执行其他操作，例如打开文件或数据库、分配内存等…
新程序员有时会使用构造函数体来为成员赋值
#include <iostream>

class Foo
{
private:
    int m_x { 0 };
    int m_y { 1 };

public:
    Foo(int x, int y)
    {
        m_x = x; // incorrect: this is an assignment, not an initialization
        m_y = y; // incorrect: this is an assignment, not an initialization
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo { 6, 7 };
    foo.print();

    return 0;
}
虽然在这种简单情况下会产生预期的结果，但在成员需要初始化的情况下（例如对于 const 或引用数据成员），赋值将不起作用。
关键见解
一旦成员初始化列表执行完毕，对象就被视为已初始化。一旦函数体执行完毕，对象就被视为已构造。
最佳实践
建议使用成员初始化列表来初始化成员，而不是在构造函数体中赋值。
检测和处理构造函数的无效参数
考虑以下 Fraction 类
class Fraction
{
private:
    int m_numerator {};
    int m_denominator {};

public:
    Fraction(int numerator, int denominator):
        m_numerator { numerator }, m_denominator { denominator }
    {
    }
};
由于分数是分子除以分母，分数的分母不能为零（否则会得到除以零，这在数学上是未定义的）。换句话说，这个类有一个不变式，即
m_denominator
不能为
0
。
相关内容
我们在课程
14.2 -- 类简介
中讨论了类不变式。
那么当用户尝试创建一个分母为零的分数时（例如
Fraction f { 1, 0 };
），我们该怎么做呢？
在成员初始化列表中，我们检测和处理错误的工具非常有限。我们可以使用条件运算符来检测错误，但那又如何呢？
class Fraction
{
private:
    int m_numerator {};
    int m_denominator {};

public:
    Fraction(int numerator, int denominator):
        m_numerator { numerator }, m_denominator { denominator != 0.0 ? denominator : ??? } // what do we do here?
    {
    }
};
我们可以将分母更改为有效值，但这样用户将得到一个不包含他们要求的值的
Fraction
，并且我们没有任何方法通知他们我们做了意想不到的事情。因此，我们通常不会尝试在成员初始化列表中进行任何类型的验证——我们只会用传入的值初始化成员，然后尝试处理这种情况。
在构造函数体内，我们可以使用语句，因此有更多的选项来检测和处理错误。这是一个断言或静态断言传入的参数在语义上有效的好地方，但这并不能真正处理生产构建中的运行时错误。
当构造函数无法构造语义上有效的对象时，我们说它失败了。
当构造函数失败时（前奏）
在课程
9.4 -- 检测和处理错误
中，我们介绍了错误处理的主题，并讨论了一些处理函数因发生错误而无法继续执行的情况的选项。由于构造函数是函数，它们容易受到相同问题的影响。
在该课程中，我们提出了 4 种处理此类错误的策略
在函数内部解决错误。
将错误返回给调用者处理。
中止程序。
抛出异常。
在大多数情况下，我们没有足够的信息完全在构造函数内部解决此类问题。所以解决问题通常不是一个选项。
对于非成员函数和非特殊成员函数，我们可以将错误返回给调用者处理。但是构造函数没有返回值，所以我们没有很好的方法来做到这一点。在某些情况下，我们可以添加一个
isValid()
成员函数（或重载转换为
bool
）来返回对象当前是否处于有效状态。例如，
Fraction
的
isValid()
函数在
m_denominator != 0.0
时返回
true
。但这意味​​着调用者必须记住在每次创建新的
Fraction
时都实际调用该函数。并且拥有可访问的语义无效对象很可能导致错误。所以虽然这比没有好，但它不是一个很好的选择。
在某些类型的程序中，我们可以直接停止整个程序，然后让用户使用正确的输入重新运行程序……但在大多数情况下，这是不可接受的。所以可能不是。
这就剩下抛出异常了。异常会完全中止构造过程，这意味着用户永远无法访问语义无效的对象。因此在大多数情况下，抛出异常是处理这些情况的最佳方法。
关键见解
当构造函数失败（且无法恢复）时，抛出异常通常是最好的做法。我们将在课程
27.5 -- 异常、类和继承
和
27.7 -- 函数 try 块
中进一步讨论。
作者注
目前，我们通常假设我们的类对象的构造成功创建了一个语义有效的对象。
致进阶读者
如果异常不可能或不被期望（无论是您决定不使用它们还是您尚未了解它们），还有另一个合理的选择。不是让用户直接创建类，而是提供一个函数，该函数要么返回一个类的实例，要么指示失败。
在以下示例中，我们的
createFraction()
函数返回一个
std::optional<Fraction>
，其中可选地包含一个有效的
Fraction
。如果包含，那么我们可以使用该
Fraction
。如果不是，那么调用者可以检测到并处理它。我们在课程
12.15 -- std::optional
中介绍了
std::optional
，并在课程
15.8 -- 友元非成员函数
中介绍了友元函数。
#include <iostream>
#include <optional>

class Fraction
{
private:
    int m_numerator { 0 };
    int m_denominator { 1 };

    // private constructor can't be called by public
    Fraction(int numerator, int denominator):
        m_numerator { numerator }, m_denominator { denominator }
    {
    }

public:
    // Allow this function to access private members
    friend std::optional<Fraction> createFraction(int numerator, int denominator);
};

std::optional<Fraction> createFraction(int numerator, int denominator)
{
    if (denominator == 0)
        return {};
    
    return Fraction{numerator, denominator};
}

int main()
{
    auto f1 { createFraction(0, 1) };
    if (f1)
    {
        std::cout << "Fraction created\n";
    }

    auto f2 { createFraction(0, 0) };
    if (!f2)
    {
        std::cout << "Bad fraction\n";
    }   
}
小测验时间
问题 #1
编写一个名为 Ball 的类。Ball 应该有两个私有成员变量，一个用于存储颜色，一个用于存储半径。还要编写一个函数来打印球的颜色和半径。
以下示例程序应该可以编译
int main()
{
	Ball blue { "blue", 10.0 };
	print(blue);

	Ball red { "red", 12.0 };
	print(red);

	return 0;
}
并产生结果
Ball(blue, 10)
Ball(red, 12)
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Ball
{
private:
	std::string m_color { "none" };
	double m_radius { 0.0 };

public:
	Ball(std::string_view color, double radius)
		: m_color { color }
		, m_radius { radius }
	{
	}

	const std::string& getColor() const { return m_color; }
	double getRadius() const { return m_radius; }
};

void print(const Ball& ball)
{
    std::cout << "Ball(" << ball.getColor() << ", " << ball.getRadius() << ")\n";
}

int main()
{
	Ball blue { "blue", 10.0 };
	print(blue);

	Ball red { "red", 12.0 };
	print(red);

	return 0;
}
问题 #2
为什么我们将
print()
设为非成员函数而不是成员函数？
显示答案
这方面的理由在课程
14.8 -- 数据隐藏（封装）的好处
中给出。
问题 #3
为什么我们将
m_color
设为
std::string
而不是
std::string_view
？
显示答案
在这个特定的示例中，这无关紧要（因为我们的颜色参数是 C 风格字符串字面量，它们不会超出作用域）。
但在概念上，我们希望我们的
Ball
类是传入颜色的所有者。如果
m_color
是
std::string_view
，那么传入一个临时对象作为颜色参数（例如从函数返回的
std::string
）会在临时颜色参数销毁时使
m_color
悬空。
我们在课程
13.11 -- 结构体杂项
中更详细地讨论了这种情况（并展示了一个示例）。
下一课
14.11
默认构造函数和默认参数
返回目录
上一课
14.9
构造函数简介