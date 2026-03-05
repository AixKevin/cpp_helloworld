# 14.8 — 数据隐藏（封装）的好处

14.8 — 数据隐藏（封装）的好处
Alex
2023 年 9 月 11 日下午 12:18 (PDT)
2025 年 2 月 20 日
在上一课（
14.5 -- 公有和私有成员以及访问说明符
）中，我们提到类的成员变量通常是私有的。首次学习类的程序员常常难以理解为什么要这样做。毕竟，将变量设为私有意味着它们无法被公有访问。往好里说，这增加了编写类的工作量。往坏里说，这可能看起来完全没有意义（特别是当我们提供公共访问函数来访问私有成员数据时）。
这个问题的答案如此基础，以至于我们将花费一整节课来讨论这个话题！
让我们从一个类比开始。
在现代生活中，我们可以接触到许多机械或电子设备。您用遥控器打开/关闭电视。您踩下油门踏板让汽车前进。您通过翻转开关打开灯。所有这些设备都有一个共同点：它们提供了一个简单的用户界面（一组按钮、一个踏板、一个开关等），让您可以执行关键操作。
这些设备实际的运作方式对您来说是隐藏的。当您按下遥控器上的按钮时，您不需要知道遥控器如何与电视通信。当您踩下汽车的油门踏板时，您不需要知道内燃机如何使车轮转动。当您拍照时，您不需要知道传感器如何收集光线并将其转化为像素化图像。
这种接口和实现的解耦非常有用，因为它允许我们使用对象而无需理解它们的工作原理——相反，我们只需理解如何与它们交互。这极大地降低了使用这些对象的复杂性，并增加了我们能够交互的对象的数量。
类类型中的实现和接口
出于类似的原因，接口和实现的解耦在编程中很有用。但首先，让我们定义一下在类类型中接口和实现分别指什么。
类类型（也称为
类接口
）的
接口
定义了类类型的用户如何与类类型的对象交互。由于只有公共成员才能从类类型外部访问，因此类类型的公共成员构成了它的接口。因此，由公共成员组成的接口有时被称为
公共接口
。
接口是类作者和类用户之间的一种隐式契约。如果现有接口发生更改，任何使用它的代码都可能中断。因此，确保我们的类类型接口设计良好且稳定（变化不大）非常重要。
类类型的
实现
由实际使类按预期行为的代码组成。这包括存储数据的成员变量，以及包含程序逻辑和操作成员变量的成员函数体。
数据隐藏
在编程中，
数据隐藏
（也称为
信息隐藏
或
数据抽象
）是一种用于通过隐藏（使其不可访问）程序定义数据类型的实现来强制执行接口和实现分离的技术。
在 C++ 类类型中实现数据隐藏很简单。首先，我们确保类类型的数据成员是私有的（以便用户不能直接访问它们）。成员函数体内部的语句已经不能直接访问用户，所以我们不需要在那里做任何其他事情。接下来，我们确保成员函数是公共的，以便用户可以调用它们。
通过遵循这些规则，我们强制类类型的用户使用公共接口来操作对象，并阻止他们直接访问实现细节。
C++ 中定义的类应该使用数据隐藏。事实上，标准库提供的所有类都正是这样做的。另一方面，结构体不应该使用数据隐藏，因为拥有非公共成员会阻止它们被视为聚合。
以这种方式定义类需要类作者做一些额外的工作。并且要求类的用户使用公共接口可能看起来比直接提供对成员变量的公共访问更繁琐。但这样做提供了大量有益的好处，有助于鼓励类的重用性和可维护性。我们将在本课的其余部分讨论这些好处。
命名法
在编程中，术语
封装
通常指以下两种情况之一：
将一个或多个项封闭在某种容器中。
将数据和用于操作该数据实例的函数捆绑在一起。
在 C++ 中，一个拥有数据和用于创建和操作该类对象的公共接口的类类型被称为封装。因为封装是数据隐藏的先决条件，并且因为数据隐藏是一项非常重要的技术，所以通常情况下，封装这个术语也包含数据隐藏。
在本教程系列中，我们假设所有封装的类都实现了数据隐藏。
数据隐藏使类更易于使用，并降低了复杂性
要使用封装的类，您不需要知道它是如何实现的。您只需要了解它的接口：哪些成员函数是公共可用的，它们接受什么参数，以及它们返回什么值。
例如
#include <iostream>
#include <string_view>

int main()
{
    std::string_view sv{ "Hello, world!" };
    std::cout << sv.length();

    return 0;
}
在这个简短的程序中，`std::string_view` 的实现细节并没有暴露给我们。我们无法看到 `std::string_view` 有多少数据成员，它们的名称是什么，或者它们的类型是什么。我们也不知道 `length()` 成员函数是如何返回被查看字符串的长度的。
最棒的是，我们不需要知道！程序就是能正常工作。我们只需要知道如何初始化一个 `std::string_view` 类型的对象，以及 `length()` 成员函数返回什么。
不必关心这些细节，极大地降低了程序的复杂性，从而减少了错误。这比任何其他原因都更重要，是封装的关键优势。
想象一下，如果必须理解 `std::string`、`std::vector` 或 `std::cout` 的实现才能使用它们，C++ 会变得多么复杂！
数据隐藏允许我们维护不变量
回顾关于类的介绍性课程（
14.2 -- 类简介
），我们引入了
类不变量
的概念，它们是对象在其生命周期内必须为真的条件，以便对象保持有效状态。
考虑以下程序
#include <iostream>
#include <string>

struct Employee // members are public by default
{
    std::string name{ "John" };
    char firstInitial{ 'J' }; // should match first initial of name

    void print() const
    {
        std::cout << "Employee " << name << " has first initial " << firstInitial << '\n';
    }
};

int main()
{
    Employee e{}; // defaults to "John" and 'J'
    e.print();

    e.name = "Mark"; // change employee's name to "Mark"
    e.print(); // prints wrong initial

    return 0;
}
这个程序打印
John has first initial J
Mark has first initial J
我们的 `Employee` 结构体有一个类不变量，即 `firstInitial` 应该始终等于 `name` 的第一个字符。如果这不成立，那么 `print()` 函数将无法正常工作。
由于 `name` 成员是公共的，`main()` 中的代码能够将 `e.name` 设置为 `"Mark"`，而 `firstInitial` 成员没有更新。我们的不变量被破坏了，第二次调用 `print()` 没有按预期工作。
当我们允许用户直接访问类的实现时，他们将负责维护所有不变量——他们可能不会这样做（无论是正确地，还是根本不这样做）。将这个负担加到用户身上会增加很多复杂性。
让我们重写这个程序，将我们的成员变量设为私有，并暴露一个成员函数来设置 Employee 的名字
#include <iostream>
#include <string>
#include <string_view>

class Employee // members are private by default
{
    std::string m_name{};
    char m_firstInitial{};

public:
    void setName(std::string_view name)
    {
        m_name = name;
        m_firstInitial = name.front(); // use std::string::front() to get first letter of `name`
    }

    void print() const
    {
        std::cout << "Employee " << m_name << " has first initial " << m_firstInitial << '\n';
    }
};

int main()
{
    Employee e{};
    e.setName("John");
    e.print();

    e.setName("Mark");
    e.print();

    return 0;
}
这个程序现在按预期工作
John has first initial J
Mark has first initial M
从用户的角度来看，唯一的变化是他们不再直接给 `name` 赋值，而是调用成员函数 `setName()`，它负责设置 `m_name` 和 `m_firstInitial`。用户不必再承担维护此不变量的负担了！
数据隐藏允许我们进行更好的错误检测（和处理）
在上面的程序中，`m_firstInitial` 必须与 `m_name` 的第一个字符匹配的不变量存在，因为 `m_firstInitial` 独立于 `m_name` 存在。我们可以通过用返回第一个首字母的成员函数替换数据成员 `m_firstInitial` 来消除这个特定的不变量
#include <iostream>
#include <string>

class Employee
{
    std::string m_name{ "John" };

public:
    void setName(std::string_view name)
    {
        m_name = name;
    }

    // use std::string::front() to get first letter of `m_name`
    char firstInitial() const { return m_name.front(); }

    void print() const
    {
        std::cout << "Employee " << m_name << " has first initial " << firstInitial() << '\n';
    }
};

int main()
{
    Employee e{}; // defaults to "John"
    e.setName("Mark");
    e.print();

    return 0;
}
然而，这个程序还有另一个类不变量。花点时间看看您是否能确定它是什么。我们在这里等着，看着这颜料变干……
答案是 `m_name` 不应该是一个空字符串（因为每个 `Employee` 都应该有一个名字）。如果 `m_name` 被设置为空字符串，不会立即发生任何坏事。但是如果随后调用 `firstInitial()`，`std::string` 的 `front()` 成员将尝试获取空字符串的第一个字母，这将导致未定义行为。
理想情况下，我们希望防止 `m_name` 永远为空。
如果用户可以公开访问 `m_name` 成员，他们可以直接设置 `m_name = ""`，我们对此无能为力。
然而，由于我们强制用户通过公共接口函数 `setName()` 设置 `m_name`，我们可以让 `setName()` 验证用户是否传入了有效名称。如果名称非空，我们可以将其赋值给 `m_name`。如果名称是空字符串，我们可以采取多种应对措施：
忽略将名称设置为“ ”的请求并返回给调用者。
断言退出。
抛出异常。
跳怪异舞。等等，不是这个。
这里的重点是，我们可以检测到误用，然后以我们认为最适当的方式处理它。如何最好地处理这些情况是另一个话题。
数据隐藏使得在不破坏现有程序的情况下更改实现细节成为可能
考虑这个简单的例子
#include <iostream>

struct Something
{
    int value1 {};
    int value2 {};
    int value3 {};
};

int main()
{
    Something something;
    something.value1 = 5;
    std::cout << something.value1 << '\n';
}
虽然这个程序运行良好，但如果我们决定改变类的实现细节，例如这样，会发生什么？
#include <iostream>

struct Something
{
    int value[3] {}; // uses an array of 3 values
};

int main()
{
    Something something;
    something.value1 = 5;
    std::cout << something.value1 << '\n';
}
我们还没有涉及到数组，但是不用担心。这里的关键是这个程序不再编译，因为名为 `value1` 的成员不再存在，并且 `main()` 中的一条语句仍然在使用该标识符。
数据隐藏赋予我们改变类实现方式的能力，而不会破坏使用这些类的程序。
这是该类的原始版本的封装版本，它使用函数访问 `m_value1`：
#include <iostream>

class Something
{
private:
    int m_value1 {};
    int m_value2 {};
    int m_value3 {};

public:
    void setValue1(int value) { m_value1 = value; }
    int getValue1() const { return m_value1; }
};

int main()
{
    Something something;
    something.setValue1(5);
    std::cout << something.getValue1() << '\n';
}
现在，让我们将类的实现改回数组：
#include <iostream>

class Something
{
private:
    int m_value[3]; // note: we changed the implementation of this class!

public:
    // We have to update any member functions to reflect the new implementation
    void setValue1(int value) { m_value[0] = value; }
    int getValue1() const { return m_value[0]; }
};

int main()
{
    // But our programs that use the class do not need to be updated!
    Something something;
    something.setValue1(5);
    std::cout << something.getValue1() << '\n';
}
因为我们没有改变类的公共接口，所以使用该接口的程序根本不需要改变，并且仍然功能相同。
类似地，如果地精半夜潜入你的房子，用不同的（但兼容的）技术替换了你电视遥控器的内部，你可能根本不会注意到！
带有接口的类更容易调试
最后，封装可以在程序出错时帮助您调试。通常，当程序无法正常工作时，是因为我们的一个成员变量被赋予了不正确的值。如果每个人都可以直接设置成员变量，那么追踪到底是哪段代码修改了成员变量导致其值错误可能会很困难。这可能涉及对修改成员变量的每个语句设置断点——而且这样的语句可能有很多。
然而，如果一个成员只能通过一个成员函数进行更改，那么您可以简单地在该函数上设置断点，并观察每个调用者如何更改值。这可以使确定罪魁祸首变得容易得多。
优先选择非成员函数而不是成员函数
在 C++ 中，如果一个函数可以合理地作为非成员函数实现，则优先将其实现为非成员函数，而不是成员函数。
这有许多好处
非成员函数不是您类接口的一部分。因此，您类的接口将更小、更直接，使类更容易理解。
非成员函数强制执行封装，因为此类函数必须通过类的公共接口工作。没有直接访问实现的诱惑，仅仅因为方便。
在对类实现进行更改时，无需考虑非成员函数（只要接口没有以不兼容的方式更改）。
非成员函数通常更容易调试。
包含应用程序特定数据和逻辑的非成员函数可以与类的可重用部分分离。
如果您有现代面向对象编程语言（如 Java 或 C#）的经验，这种做法可能会让您感到惊讶。这些语言使用不同的概念模型，其中类是宇宙的中心，一切都围绕着它。因此，这些语言将成员函数放在首位（事实上，Java 和 C# 甚至不支持非成员函数）。
最佳实践
尽可能优先将函数实现为非成员函数（特别是包含应用程序特定数据或逻辑的函数）。
提示
以下是一个关于何时将函数作为成员函数或非成员函数的简化指南：
在必须使用成员函数时才使用。C++ 要求某些类型的函数必须定义为成员。我们将在下一课讨论构造函数时看到一个例子。其他还包括析构函数、虚函数和某些运算符。
当函数需要访问不应暴露的私有（或受保护）数据时，优先选择成员函数。
否则，优先选择非成员函数（特别是对于不修改对象状态的函数）。
后两者也有例外——我们将在讨论相关主题时介绍一些。
一个常见但具有挑战性的情况是，当优先选择非成员函数需要添加访问函数来促进时。在这种情况下，您需要考虑权衡。
添加访问函数意味着创建一两个新的成员函数（getter 和可能的 setter），这会增加类接口的大小和复杂性。除非您可以在多个地方使用这些新的访问函数，否则这可能不值得。
不要为不应直接访问的数据添加访问函数（例如，因为它是一个内部状态）或会允许用户违反类不变量的数据。
相关内容
Scott Meyers 的文章
《非成员函数如何改善封装》
更详细地探讨了优先使用非成员函数的思想。
我们用三个相似的例子来说明，从最差到最佳：
#include <iostream>
#include <string>

class Yogurt
{
    std::string m_flavor{ "vanilla" };

public:
    void setFlavor(std::string_view flavor)
    {
        m_flavor = flavor;
    }

    const std::string& getFlavor() const { return m_flavor; }

    // Worst: member function print() uses direct access to m_flavor when getter exists
    void print() const
    {
        std::cout << "The yogurt has flavor " << m_flavor << '\n';
    }
};

int main()
{
    Yogurt y{};
    y.setFlavor("cherry");
    y.print();

    return 0;
}
上面是最差的版本。`print()` 成员函数直接访问 `m_flavor`，而用于获取 `flavor` 的 getter 已经存在。如果类实现更新，`print()` 也可能需要修改。`print()` 打印的字符串是应用程序特有的（使用此类的另一个应用程序可能希望打印其他内容，这将需要克隆或修改类）。
#include <iostream>
#include <string>

class Yogurt
{
    std::string m_flavor{ "vanilla" };

public:
    void setFlavor(std::string_view flavor)
    {
        m_flavor = flavor;
    }

    const std::string& getFlavor() const { return m_flavor; }

    // Better: member function print() has no direct access to members
    void print(std::string_view prefix) const
    {
        std::cout << prefix << ' ' << getFlavor() << '\n';
    }
};

int main()
{
    Yogurt y{};
    y.setFlavor("cherry");
    y.print("The yogurt has flavor");

    return 0;
}
上面的版本更好，但仍然不够好。`print()` 仍然是一个成员函数，但至少它现在不再直接访问任何数据成员。如果类实现被更新，`print()` 将需要评估以确定是否需要更新（但它不会）。`print()` 函数的前缀现在是参数化的，这允许我们将前缀移到非成员函数 `main()` 中。但该函数仍然对打印方式施加了约束（例如，它总是以“前缀、空格、风味、换行符”的形式打印）。如果这不满足给定应用程序的需求，则需要添加另一个函数。
#include <iostream>
#include <string>

class Yogurt
{
    std::string m_flavor{ "vanilla" };

public:
    void setFlavor(std::string_view flavor)
    {
        m_flavor = flavor;
    }

    const std::string& getFlavor() const { return m_flavor; }
};

// Best: non-member function print() is not part of the class interface
void print(const Yogurt& y)
{
        std::cout << "The yogurt has flavor " << y.getFlavor() << '\n';
}

int main()
{
    Yogurt y{};
    y.setFlavor("cherry");
    print(y);

    return 0;
}
上述版本是最佳的。`print()` 现在是一个非成员函数。它不直接访问任何成员。如果类实现发生变化，`print()` 根本不需要进行评估。此外，每个应用程序都可以提供自己的 `print()` 函数，按照该应用程序希望的方式进行打印。
类成员的声明顺序
在类外部编写代码时，我们必须在使用变量和函数之前声明它们。然而，在类内部，这种限制不存在。如
14.3 -- 成员函数
一课所述，我们可以按任何我们喜欢的顺序排列成员。
那么我们应该如何排序呢？
这里有两种思路
先列出您的私有成员，然后列出您的公共成员函数。这遵循传统的“先声明后使用”的风格。任何查看您的类代码的人都会在您的数据成员使用之前看到它们是如何定义的，这可以使阅读和理解实现细节更容易。
先列出您的公共成员，并将您的私有成员放在底部。因为使用您的类的人对公共接口感兴趣，所以将您的公共成员放在顶部，将他们需要的信息放在前面，并将实现细节（最不重要）放在最后。
在现代 C++ 中，第二种方法（公共成员优先）更常被推荐，特别是对于将与其他开发人员共享的代码。
最佳实践
首先声明公共成员，其次是受保护成员，最后是私有成员。这突出了公共接口，并弱化了实现细节。
作者注
本网站的大多数示例都使用了与推荐相反的声明顺序。这部分是历史原因，但我们也发现这种顺序在学习语言机制时更直观，因为我们专注于实现细节并剖析事物的工作原理。
致进阶读者
Google C++ 风格指南
推荐以下顺序：
类型和类型别名（typedef、using、enum、嵌套结构体和类，以及友元类型）
静态常量
工厂函数
构造函数和赋值运算符
析构函数
所有其他函数（静态和非静态成员函数，以及友元函数）
数据成员（静态和非静态）
下一课
14.9
构造函数简介
返回目录
上一课
14.7
返回数据成员引用的成员函数