# 24.9 — 多重继承

24.9 — 多重继承
Alex
2008 年 1 月 24 日，太平洋标准时间下午 3:39
2024 年 7 月 11 日
到目前为止，我们介绍的所有继承示例都是单一继承——也就是说，每个继承类只有一个父类。然而，C++ 提供了多重继承的能力。
多重继承
允许派生类从多个父类继承成员。
假设我们想编写一个程序来跟踪一群老师。老师是人。然而，老师也是雇员（如果他们为自己工作，他们就是自己的雇主）。多重继承可以用来创建一个 Teacher 类，它同时继承 Person 和 Employee 的属性。要使用多重继承，只需指定每个基类（就像单一继承一样），并用逗号分隔。
#include <string>
#include <string_view>

class Person
{
private:
    std::string m_name{};
    int m_age{};

public:
    Person(std::string_view name, int age)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

class Employee
{
private:
    std::string m_employer{};
    double m_wage{};

public:
    Employee(std::string_view employer, double wage)
        : m_employer{ employer }, m_wage{ wage }
    {
    }

    const std::string& getEmployer() const { return m_employer; }
    double getWage() const { return m_wage; }
};

// Teacher publicly inherits Person and Employee
class Teacher : public Person, public Employee
{
private:
    int m_teachesGrade{};

public:
    Teacher(std::string_view name, int age, std::string_view employer, double wage, int teachesGrade)
        : Person{ name, age }, Employee{ employer, wage }, m_teachesGrade{ teachesGrade }
    {
    }
};

int main()
{
    Teacher t{ "Mary", 45, "Boo", 14.3, 8 };

    return 0;
}
混入（Mixins）
混入
（也拼作 “mix-in”）是一个小类，可以从中继承以向类添加属性。混入这个名字表示该类旨在混入其他类中，而不是单独实例化。
在以下示例中，`Box`、`Label` 和 `Tooltip` 类是混入，我们从中继承以创建一个新的 `Button` 类。
// h/t to reader Waldo for this example
#include <string>

struct Point2D
{
	int x{};
	int y{};
};

class Box // mixin Box class
{
public:
	void setTopLeft(Point2D point) { m_topLeft = point; }
	void setBottomRight(Point2D point) { m_bottomRight = point; }
private:
	Point2D m_topLeft{};
	Point2D m_bottomRight{};
};

class Label // mixin Label class
{
public:
	void setText(const std::string_view str) { m_text = str; }
	void setFontSize(int fontSize) { m_fontSize = fontSize; }
private:
	std::string m_text{};
	int m_fontSize{};
};

class Tooltip // mixin Tooltip class
{
public:
	void setText(const std::string_view str) { m_text = str; }
private:
	std::string m_text{};
};

class Button : public Box, public Label, public Tooltip {}; // Button using three mixins

int main()
{
	Button button{};
	button.Box::setTopLeft({ 1, 1 });
	button.Box::setBottomRight({ 10, 10 });
	button.Label::setText("Submit");
	button.Label::setFontSize(6);
	button.Tooltip::setText("Submit the form to the server");
}
您可能想知道为什么我们使用显式的 `Box::`、`Label::` 和 `Tooltip::` 作用域解析前缀，而这在大多数情况下是不必要的。
`Label::setText()` 和 `Tooltip::setText()` 具有相同的原型。如果我们调用 `button.setText()`，编译器将产生一个模糊的函数调用编译错误。在这种情况下，我们必须使用前缀来消除歧义，表明我们想要哪个版本。
在非模糊的情况下，使用混入名称可以提供关于函数调用适用于哪个混入的文档，这有助于使我们的代码更易于理解。
非模糊的情况如果将来我们添加额外的混入，可能会变得模糊。使用显式前缀有助于防止这种情况发生。
致进阶读者
因为混入旨在向派生类添加功能，而不是提供接口，所以混入通常不使用虚函数（在下一章中介绍）。相反，如果混入类需要以特定方式定制，通常使用模板。因此，混入类通常是模板化的。
也许令人惊讶的是，派生类可以使用派生类作为模板类型参数从混入基类继承。这种继承被称为
奇异递归模板模式
（简称 CRTP），它看起来像这样
// The Curiously Recurring Template Pattern (CRTP)

template <class T>
class Mixin
{
    // Mixin<T> can use template type parameter T to access members of Derived
    // via (static_cast<T*>(this))
};

class Derived : public Mixin<Derived>
{
};
您可以在
此处
找到一个使用 CRTP 的简单示例。
多重继承的问题
虽然多重继承看起来像是单一继承的简单扩展，但多重继承引入了许多问题，这些问题会显著增加程序的复杂性并使其成为维护噩梦。让我们看看其中的一些情况。
首先，当多个基类包含同名函数时，可能会导致歧义。例如
#include <iostream>

class USBDevice
{
private:
    long m_id {};

public:
    USBDevice(long id)
        : m_id { id }
    {
    }

    long getID() const { return m_id; }
};

class NetworkDevice
{
private:
    long m_id {};

public:
    NetworkDevice(long id)
        : m_id { id }
    {
    }

    long getID() const { return m_id; }
};

class WirelessAdapter: public USBDevice, public NetworkDevice
{
public:
    WirelessAdapter(long usbId, long networkId)
        : USBDevice { usbId }, NetworkDevice { networkId }
    {
    }
};

int main()
{
    WirelessAdapter c54G { 5442, 181742 };
    std::cout << c54G.getID(); // Which getID() do we call?

    return 0;
}
当 `c54G.getID()` 被编译时，编译器会查找 WirelessAdapter 是否包含名为 getID() 的函数。它没有。然后编译器会查找任何父类是否有名为 getID() 的函数。看到这里的问题了吗？问题是 c54G 实际上包含两个 getID() 函数：一个从 USBDevice 继承，一个从 NetworkDevice 继承。因此，这个函数调用是模糊的，如果您尝试编译它，您将收到一个编译器错误。
然而，有一种方法可以解决这个问题：您可以明确指定您打算调用哪个版本
int main()
{
    WirelessAdapter c54G { 5442, 181742 };
    std::cout << c54G.USBDevice::getID();

    return 0;
}
虽然这个变通方法很简单，但当您的类从四个或六个基类继承，而这些基类本身又从其他类继承时，您可以看到事情会变得多么复杂。随着您继承的类越来越多，命名冲突的可能性呈指数级增长，并且这些命名冲突中的每一个都需要明确解决。
其次，更严重的是
菱形问题
，作者喜欢称之为“毁灭菱形”。当一个类多重继承自两个类，而这两个类都继承自一个单一基类时，就会发生这种情况。这导致了一种菱形继承模式。
例如，考虑以下一组类
class PoweredDevice
{
};

class Scanner: public PoweredDevice
{
};

class Printer: public PoweredDevice
{
};

class Copier: public Scanner, public Printer
{
};
扫描仪和打印机都是带电设备，因此它们都派生自 PoweredDevice。然而，复印机结合了扫描仪和打印机的功能。
在这种情况下会出现许多问题，包括 Copier 应该拥有 PoweredDevice 的一个副本还是两个副本，以及如何解决某些类型的模糊引用。虽然这些问题中的大多数可以通过明确的作用域来解决，但为了应对增加的复杂性而添加到类中的维护开销可能会导致开发时间飙升。我们将在下一章（第
25.8 节——虚基类
）中讨论更多解决菱形问题的方法。
多重继承是否弊大于利？
事实证明，大多数可以通过多重继承解决的问题也可以通过单一继承解决。许多面向对象语言（例如 Smalltalk、PHP）甚至不支持多重继承。许多相对现代的语言，如 Java 和 C#，限制类只能单一继承普通类，但允许多重继承接口类（我们将在后面讨论）。这些语言不允许多重继承的主要思想是，它只会使语言过于复杂，并最终导致比解决更多的问题。
许多作者和经验丰富的程序员认为，C++ 中的多重继承应不惜一切代价避免，因为它带来了许多潜在问题。作者不赞同这种做法，因为在某些时候和某些情况下，多重继承是最佳选择。然而，多重继承应极其谨慎地使用。
有趣的是，您已经在不知不觉中使用了使用多重继承编写的类：iostream 库对象 std::cin 和 std::cout 都是使用多重继承实现的！
最佳实践
避免多重继承，除非替代方案导致更高的复杂性。
下一课
24.x
第 24 章总结与测验
返回目录
上一课
24.8
隐藏继承功能