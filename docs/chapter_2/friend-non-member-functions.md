# 15.8 — 友元非成员函数

15.8 — 友元非成员函数
Alex
2007 年 9 月 20 日，太平洋夏令时下午 2:04
2024 年 5 月 8 日
本章和上一章的大部分内容，我们一直在宣扬访问控制的优点，它提供了一种机制来控制谁可以访问类的各种成员。私有成员只能由类的其他成员访问，而公共成员可以被所有人访问。在课程
14.6 -- 访问函数
中，我们讨论了将数据设为私有并为非成员创建公共接口的好处。
然而，在某些情况下，这种安排要么不足够，要么不理想。
例如，考虑一个专注于管理某些数据集的存储类。现在，假设您还想显示这些数据，但是处理显示的代​​码将会有很多选项，因此很复杂。您可以将存储管理函数和显示管理函数都放在同一个类中，但这会使事情变得混乱并导致复杂的接口。您也可以将它们分开：存储类管理存储，而其他显示类管理所有显示功能。这创建了良好的职责分离。但是显示类将无法访问存储类的私有成员，并且可能无法完成其工作。
或者，在某些情况下，在语法上，我们可能更倾向于使用非成员函数而不是成员函数（我们将在下面展示一个示例）。在重载运算符时，这通常是这种情况，我们将在未来的课程中讨论这个主题。但非成员函数有相同的问题——它们无法访问类的私有成员。
如果访问函数（或其他公共成员函数）已经存在并且足以实现我们试图实现的任何功能，那么很好——我们可以（并且应该）只使用它们。但在某些情况下，这些函数不存在。那该怎么办？
一种选择是向类中添加新的成员函数，以允许其他类或非成员函数完成它们原本无法完成的任何工作。但我们可能不希望允许公共访问此类事物——也许这些事物高度依赖于实现，或者容易被滥用。
我们真正需要的是一种在逐案基础上颠覆访问控制系统的方法。
友谊是魔法
我们挑战的答案是友谊。
在类的主体内，
友元声明
（使用
friend
关键字）可用于告诉编译器某个其他类或函数现在是友元。在 C++ 中，
友元
是一个类或函数（成员或非成员），它被授予对另一个类的私有和受保护成员的完全访问权限。通过这种方式，一个类可以有选择地授予其他类或函数对其成员的完全访问权限，而不会影响其他任何内容。
关键见解
友元总是由其成员将被访问的类授予（而不是由希望访问的类或函数授予）。在访问控制和授予友元之间，类总是保留控制谁可以访问其成员的能力。
例如，如果我们的存储类将显示类设为友元，那么显示类将能够直接访问存储类的所有成员。显示类可以使用这种直接访问来实现存储类的显示，同时保持结构上的分离。
友元声明不受访问控制的影响，因此它在类主体内的任何位置放置都无关紧要。
现在我们了解了什么是友元，接下来我们看看授予非成员函数、成员函数和其他类友元的具体示例。我们将在本课程中讨论友元非成员函数，然后在下一课程
15.9 -- 友元类和友元成员函数
中看看友元类和友元成员函数。
友元非成员函数
友元函数
是一个函数（成员或非成员），它可以像类的成员一样访问类的私有和受保护成员。在所有其他方面，友元函数是一个普通函数。
让我们看一个简单类将非成员函数设为友元的例子
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }

    // Here is the friend declaration that makes non-member function void print(const Accumulator& accumulator) a friend of Accumulator
    friend void print(const Accumulator& accumulator);
};

void print(const Accumulator& accumulator)
{
    // Because print() is a friend of Accumulator
    // it can access the private members of Accumulator
    std::cout << accumulator.m_value;
}

int main()
{
    Accumulator acc{};
    acc.add(5); // add 5 to the accumulator

    print(acc); // call the print() non-member function

    return 0;
}
在此示例中，我们声明了一个名为
print()
的非成员函数，它接受一个
Accumulator
类的对象。由于
print()
不是 Accumulator 类的成员，它通常无法访问私有成员
m_value
。但是，Accumulator 类有一个友元声明，将
print(const Accumulator& accumulator)
设为友元，现在这是允许的。
请注意，由于
print()
是一个非成员函数（因此没有隐式对象），我们必须显式地将一个
Accumulator
对象传递给
print()
才能进行操作。
在类内部定义友元非成员
就像成员函数可以根据需要在类内部定义一样，友元非成员函数也可以在类内部定义。以下示例在
Accumulator
类内部定义了友元非成员函数
print()
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }

    // Friend functions defined inside a class are non-member functions
    friend void print(const Accumulator& accumulator)
    {
        // Because print() is a friend of Accumulator
        // it can access the private members of Accumulator
        std::cout << accumulator.m_value;
    }
};

int main()
{
    Accumulator acc{};
    acc.add(5); // add 5 to the accumulator

    print(acc); // call the print() non-member function

    return 0;
}
虽然您可能认为因为
print()
定义在
Accumulator
内部，所以
print()
是
Accumulator
的成员，但事实并非如此。因为
print()
被定义为友元，所以它被视为一个非成员函数（就像它是在
Accumulator
外部定义的一样）。
语法上更倾向于友元非成员函数
在本课的引言中，我们提到有时我们可能更倾向于使用非成员函数而不是成员函数。现在让我们举一个例子。
#include <iostream>

class Value
{
private:
    int m_value{};

public:
    explicit Value(int v): m_value { v }  { }

    bool isEqualToMember(const Value& v) const;
    friend bool isEqualToNonmember(const Value& v1, const Value& v2);
};

bool Value::isEqualToMember(const Value& v) const
{
    return m_value == v.m_value;
}

bool isEqualToNonmember(const Value& v1, const Value& v2)
{
    return v1.m_value == v2.m_value;
}

int main()
{
    Value v1 { 5 };
    Value v2 { 6 };

    std::cout << v1.isEqualToMember(v2) << '\n';
    std::cout << isEqualToNonmember(v1, v2) << '\n';

    return 0;
}
在此示例中，我们定义了两个检查两个
Value
对象是否相等的类似函数。
isEqualToMember()
是一个成员函数，而
isEqualToNonmember()
是一个非成员函数。让我们重点关注这些函数的定义方式。
在
isEqualToMember()
中，我们隐式传递一个对象，显式传递另一个对象。函数的实现反映了这一点，我们必须在心理上调和
m_value
属于隐式对象，而
v.m_value
属于显式参数。
在
isEqualToNonmember()
中，两个对象都显式传递。这使得函数实现中的并行性更好，因为
m_value
成员总是显式地带有显式参数前缀。
您可能仍然更喜欢调用语法
v1.isEqualToMember(v2)
而不是
isEqualToNonmember(v1, v2)
。但是当我们学习运算符重载时，我们将再次讨论这个主题。
多个友元
一个函数可以同时是多个类的友元。例如，考虑以下示例
#include <iostream>

class Humidity; // forward declaration of Humidity

class Temperature
{
private:
    int m_temp { 0 };
public:
    explicit Temperature(int temp) : m_temp { temp } { }

    friend void printWeather(const Temperature& temperature, const Humidity& humidity); // forward declaration needed for this line
};

class Humidity
{
private:
    int m_humidity { 0 };
public:
    explicit Humidity(int humidity) : m_humidity { humidity } {  }

    friend void printWeather(const Temperature& temperature, const Humidity& humidity);
};

void printWeather(const Temperature& temperature, const Humidity& humidity)
{
    std::cout << "The temperature is " << temperature.m_temp <<
       " and the humidity is " << humidity.m_humidity << '\n';
}

int main()
{
    Humidity hum { 10 };
    Temperature temp { 12 };

    printWeather(temp, hum);

    return 0;
}
关于这个例子有三点值得注意。首先，因为
printWeather()
对
Humidity
和
Temperature
的使用程度相同，所以将其作为其中任何一个的成员都没有真正意义。非成员函数效果更好。其次，因为
printWeather()
是
Humidity
和
Temperature
的友元，它可以访问这两个类的对象的私有数据。最后，请注意示例顶部的以下行
class Humidity;
这是
class Humidity
的前向声明。类前向声明的作用与函数前向声明相同——它们告诉编译器稍后将定义一个标识符。然而，与函数不同，类没有返回类型或参数，所以类前向声明总是简单的
class ClassName
（除非它们是类模板）。
如果没有这行代码，编译器在解析
Temperature
中的友元声明时会告诉我们它不知道
Humidity
是什么。
友元关系难道不会违反数据隐藏原则吗？
不会。友元关系是由执行数据隐藏的类授予的，期望友元将访问其私有成员。将友元视为类本身的扩展，具有所有相同的访问权限。因此，访问是预期行为，而不是违规。
正确使用友元关系可以通过在设计角度合理时允许功能分离（而不是为了访问控制原因而将它们保持在一起）来使程序更易于维护。或者当使用非成员函数而不是成员函数更有意义时。
然而，由于友元直接访问类的实现，因此类的实现的更改通常也需要友元的更改。如果一个类有许多友元（或者这些友元也有友元），这可能会导致连锁反应。
在实现友元函数时，尽可能优先使用公共接口而不是直接访问成员。这将有助于使您的友元函数免受未来实现更改的影响，并减少后续需要修改和/或重新测试的代码。
最佳实践
友元函数应尽可能优先使用类接口而不是直接访问。
优先选择非友元函数而非友元函数
在课程
14.8 -- 数据隐藏（封装）的好处
中，我们提到我们应该优先使用非成员函数而不是成员函数。出于同样的原因，我们应该优先使用非友元函数而不是友元函数。
例如，在以下示例中，如果
Accumulator
的实现发生更改（例如，我们重命名
m_value
），则
print()
的实现也需要更改
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 }; // if we rename this

public:
    void add(int value) { m_value += value; } // we need to modify this

    friend void print(const Accumulator& accumulator);
};

void print(const Accumulator& accumulator)
{
    std::cout << accumulator.m_value; // and we need to modify this
}

int main()
{
    Accumulator acc{};
    acc.add(5); // add 5 to the accumulator

    print(acc); // call the print() non-member function

    return 0;
}
更好的方法如下
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }
    int value() const { return m_value; } // added this reasonable access function
};

void print(const Accumulator& accumulator) // no longer a friend of Accumulator
{
    std::cout << accumulator.value(); // use access function instead of direct access
}

int main()
{
    Accumulator acc{};
    acc.add(5); // add 5 to the accumulator

    print(acc); // call the print() non-member function

    return 0;
}
在这个例子中，
print()
使用访问函数
value()
来获取
m_value
的值，而不是直接访问
m_value
。现在，如果
Accumulator
的实现发生变化，
print()
将不需要更新。
最佳实践
尽可能且合理地将函数实现为非友元。
向现有类的公共接口添加新成员时要谨慎，因为每个函数（即使是微不足道的函数）都会增加一定程度的混乱和复杂性。在上面
Accumulator
的例子中，拥有一个访问函数来获取当前累积值是完全合理的。在更复杂的情况下，可能更倾向于使用友元关系，而不是向类的接口添加许多新的访问函数。
下一课
15.9
友元类和友元成员函数
返回目录
上一课
15.7
静态成员函数