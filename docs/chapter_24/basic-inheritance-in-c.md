# 24.2 — C++ 中的基本继承

24.2 — C++ 中的基本继承
Alex
2008 年 1 月 4 日，太平洋标准时间下午 12:28
2023 年 9 月 11 日
既然我们已经抽象地讨论了什么是继承，现在让我们来谈谈它在 C++ 中是如何使用的。
C++ 中的继承发生在类之间。在继承（“is-a”关系）中，被继承的类称为**父类**、**基类**或**超类**，而执行继承的类称为**子类**、**派生类**或**子类型**。
在上面的图表中，Fruit 是父类，Apple 和 Banana 都是子类。
在此图表中，Triangle 既是子类（对 Shape 而言），也是父类（对 Right Triangle 而言）。
子类从父类继承行为（成员函数）和属性（成员变量）（受我们将在未来课程中介绍的一些访问限制的约束）。
这些变量和函数成为派生类的成员。
由于子类是完整的类，它们当然可以拥有自己的特定于该类的成员。我们稍后会看到一个例子。
一个 Person 类
这是一个简单的类，用于表示一个通用的人
#include <string>
#include <string_view>

class Person
{
// In this example, we're making our members public for simplicity
public: 
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};
由于这个 Person 类旨在表示一个通用的人，我们只定义了任何类型的人都会共有的成员。每个人（无论性别、职业等）都有姓名和年龄，所以这里就表示了这些。
请注意，在此示例中，我们已将所有变量和函数设为 public。这纯粹是为了现在保持这些示例的简单性。通常我们会将变量设为 private。我们将在本章后面讨论访问控制以及它们如何与继承交互。
一个 BaseballPlayer 类
假设我们想编写一个程序来跟踪一些棒球运动员的信息。棒球运动员需要包含特定于棒球运动员的信息——例如，我们可能希望存储球员的击球平均值和他们击出的本垒打数量。
这是我们未完成的 BaseballPlayer 类
class BaseballPlayer
{
// In this example, we're making our members public for simplicity
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};
现在，我们还想跟踪棒球运动员的姓名和年龄，而我们已经将这些信息作为 Person 类的一部分。
我们有三种选择来将姓名和年龄添加到 BaseballPlayer
直接将姓名和年龄作为成员添加到 BaseballPlayer 类。这可能是最差的选择，因为我们正在复制代码 Person 类中已经存在的代码。对 Person 的任何更新也必须在 BaseballPlayer 中进行。
使用组合将 Person 作为 BaseballPlayer 的成员添加。但我们必须问自己，“一个 BaseballPlayer 是否拥有一个 Person”？不，它没有。所以这不是正确的范式。
让 BaseballPlayer 从 Person 继承这些属性。请记住，继承代表“is-a”关系。一个 BaseballPlayer 是一个人吗？是的。所以继承是一个不错的选择。
使 BaseballPlayer 成为派生类
要让 BaseballPlayer 继承自我们的 Person 类，语法相当简单。在 `class BaseballPlayer` 声明之后，我们使用冒号、单词“public”以及我们希望继承的类的名称。这称为*公共继承*。我们将在未来的课程中详细讨论公共继承的含义。
// BaseballPlayer publicly inheriting Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};
使用派生图，我们的继承看起来像这样
当 BaseballPlayer 从 Person 继承时，BaseballPlayer 获取 Person 的成员函数和变量。此外，BaseballPlayer 定义了它自己的两个成员：m_battingAverage 和 m_homeRuns。这是有道理的，因为这些属性是 BaseballPlayer 特有的，而不是任何 Person 特有的。
因此，BaseballPlayer 对象将拥有 4 个成员变量：来自 BaseballPlayer 的 m_battingAverage 和 m_homeRuns，以及来自 Person 的 m_name 和 m_age。
这很容易证明
#include <iostream>
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{name}, m_age{age}
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};

// BaseballPlayer publicly inheriting Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};

int main()
{
    // Create a new BaseballPlayer object
    BaseballPlayer joe{};
    // Assign it a name (we can do this directly because m_name is public)
    joe.m_name = "Joe";
    // Print out the name
    std::cout << joe.getName() << '\n'; // use the getName() function we've acquired from the Person base class

    return 0;
}
打印值为
Joe
这可以编译并运行，因为 joe 是一个 BaseballPlayer，并且所有 BaseballPlayer 对象都拥有从 Person 类继承的 m_name 成员变量和 getName() 成员函数。
一个 Employee 派生类
现在我们再写一个也继承自 Person 的类。这次，我们将编写一个 Employee 类。一个 Employee “是”一个人，所以使用继承是合适的
// Employee publicly inherits from Person
class Employee: public Person
{
public:
    double m_hourlySalary{};
    long m_employeeID{};

    Employee(double hourlySalary = 0.0, long employeeID = 0)
        : m_hourlySalary{hourlySalary}, m_employeeID{employeeID}
    {
    }

    void printNameAndSalary() const
    {
        std::cout << m_name << ": " << m_hourlySalary << '\n';
    }
};
Employee 从 Person 继承 m_name 和 m_age（以及两个访问函数），并添加了它自己的另外两个成员变量和一个成员函数。请注意，printNameAndSalary() 使用了它所属类（Employee::m_hourlySalary）和父类（Person::m_name）的变量。
这给了我们一个派生图，如下所示
请注意，Employee 和 BaseballPlayer 之间没有直接关系，尽管它们都继承自 Person。
这是使用 Employee 的完整示例
#include <iostream>
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{name}, m_age{age}
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};

// Employee publicly inherits from Person
class Employee: public Person
{
public:
    double m_hourlySalary{};
    long m_employeeID{};

    Employee(double hourlySalary = 0.0, long employeeID = 0)
        : m_hourlySalary{hourlySalary}, m_employeeID{employeeID}
    {
    }

    void printNameAndSalary() const
    {
        std::cout << m_name << ": " << m_hourlySalary << '\n';
    }
};

int main()
{
    Employee frank{20.25, 12345};
    frank.m_name = "Frank"; // we can do this because m_name is public

    frank.printNameAndSalary();
    
    return 0;
}
这会打印
Frank: 20.25
继承链
可以从本身派生自另一个类的类继承。这样做没有什么值得注意或特别之处——一切都按上述示例进行。
例如，我们来编写一个 Supervisor 类。一个 Supervisor 是一个 Employee，而一个 Employee 是一个 Person。我们已经编写了一个 Employee 类，所以让我们将其作为派生 Supervisor 的基类
class Supervisor: public Employee
{
public:
    // This Supervisor can oversee a max of 5 employees
    long m_overseesIDs[5]{};
};
现在我们的派生图看起来像这样
所有 Supervisor 对象都继承了来自 Employee 和 Person 的函数和变量，并添加了它们自己的 m_overseesIDs 成员变量。
通过构建这样的继承链，我们可以创建一组可重用的类，它们在顶部非常通用，并在继承的每个级别上变得越来越具体。
这种继承有什么用处？
从基类继承意味着我们不必在派生类中重新定义基类的信息。我们通过继承自动接收基类的成员函数和成员变量，然后只需添加我们想要的额外函数或成员变量。这不仅节省了工作，还意味着如果我们更新或修改基类（例如添加新函数或修复错误），我们所有的派生类都将自动继承这些更改！
例如，如果我们向 Person 添加一个新函数，那么 Employee、Supervisor 和 BaseballPlayer 将自动获得访问权限。如果我们将新变量添加到 Employee，那么 Supervisor 也会获得访问权限。这使我们能够以简单、直观且低维护的方式构建新类！
总结
继承允许我们通过让其他类继承它们的成员来重用类。在未来的课程中，我们将继续探讨这是如何工作的。
下一课
24.3
派生类的构造顺序
返回目录
上一课
24.1
继承简介