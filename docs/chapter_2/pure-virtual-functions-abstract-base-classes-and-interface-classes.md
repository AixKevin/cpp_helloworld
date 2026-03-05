# 25.7 — 纯虚函数、抽象基类和接口类

25.7 — 纯虚函数、抽象基类和接口类
Alex
2008 年 2 月 13 日下午 4:09（太平洋标准时间）
2024 年 10 月 1 日
纯虚（抽象）函数和抽象基类
到目前为止，我们编写的所有虚函数都包含函数体（定义）。然而，C++ 允许你创建一种特殊类型的虚函数，称为
纯虚函数
（或
抽象函数
），它根本没有函数体！纯虚函数仅仅充当一个占位符，旨在由派生类重新定义。
要创建纯虚函数，我们只需将函数赋值为 0，而不是为函数定义函数体。
#include <string_view>

class Base
{
public:
    std::string_view sayHi() const { return "Hi"; } // a normal non-virtual function    

    virtual std::string_view getName() const { return "Base"; } // a normal virtual function

    virtual int getValue() const = 0; // a pure virtual function

    int doSomething() = 0; // Compile error: can not set non-virtual functions to 0
};
当我们向类中添加纯虚函数时，我们实际上是在说：“这个函数应该由派生类来实现”。
使用纯虚函数有两个主要后果：首先，任何带有一个或多个纯虚函数的类都将成为
抽象基类
，这意味着它不能被实例化！考虑一下如果我们可以创建 Base 的实例会发生什么
int main()
{
    Base base {}; // We can't instantiate an abstract base class, but for the sake of example, pretend this was allowed
    base.getValue(); // what would this do?

    return 0;
}
因为 getValue() 没有定义，那么 base.getValue() 会解析成什么呢？
其次，任何派生类都必须为此函数定义一个函数体，否则该派生类也将被视为抽象基类。
纯虚函数示例
让我们看一个纯虚函数的实际示例。在上一课中，我们编写了一个简单的 Animal 基类，并从中派生了 Cat 和 Dog 类。这是我们留下的代码
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // We're making this constructor protected because
    // we don't want people creating Animal objects directly,
    // but we still want derived classes to be able to use it.
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }
    
    virtual ~Animal() = default;
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const override { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const override { return "Woof"; }
};
我们通过将构造函数设置为 protected 来阻止人们分配 Animal 类型的对象。然而，仍然可以创建不重新定义函数 speak() 的派生类。
例如
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // We're making this constructor protected because
    // we don't want people creating Animal objects directly,
    // but we still want derived classes to be able to use it.
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }
    
    virtual ~Animal() = default;
};

class Cow : public Animal
{
public:
    Cow(std::string_view name)
        : Animal{ name }
    {
    }

    // We forgot to redefine speak
};

int main()
{
    Cow cow{"Betsy"};
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
这将打印
Betsy says ???
发生了什么？我们忘记重新定义函数 speak()，所以 cow.Speak() 解析为 Animal.speak()，这不是我们想要的。
解决此问题的更好方法是使用纯虚函数
#include <string>
#include <string_view>

class Animal // This Animal is an abstract base class
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // note that speak is now a pure virtual function
    
    virtual ~Animal() = default;
};
这里有几点需要注意。首先，speak() 现在是一个纯虚函数。这意味着 Animal 现在是一个抽象基类，不能被实例化。因此，我们不再需要将构造函数设置为 protected（尽管这样做也无妨）。其次，因为我们的 Cow 类是从 Animal 派生而来，但我们没有定义 Cow::speak()，所以 Cow 也是一个抽象基类。现在当我们尝试编译这段代码时
#include <iostream>
#include <string>
#include <string_view>

class Animal // This Animal is an abstract base class
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // note that speak is now a pure virtual function
    
    virtual ~Animal() = default;
};

class Cow: public Animal
{
public:
    Cow(std::string_view name)
        : Animal{ name }
    {
    }

    // We forgot to redefine speak
};

int main()
{
    Cow cow{ "Betsy" };
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
编译器会给出错误，因为 Cow 是一个抽象基类，我们不能创建抽象基类的实例
prog.cc:35:9: error: variable type 'Cow' is an abstract class
   35 |     Cow cow{ "Betsy" };
      |         ^
prog.cc:17:30: note: unimplemented pure virtual method 'speak' in 'Cow'
   17 |     virtual std::string_view speak() const = 0; // note that speak is now a pure virtual function
      |                              ^
这告诉我们，只有当 Cow 为 speak() 提供函数体时，我们才能实例化 Cow。
我们继续这样做
#include <iostream>
#include <string>
#include <string_view>

class Animal // This Animal is an abstract base class
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // note that speak is now a pure virtual function
    
    virtual ~Animal() = default;
};

class Cow: public Animal
{
public:
    Cow(std::string_view name)
        : Animal(name)
    {
    }

    std::string_view speak() const override { return "Moo"; }
};

int main()
{
    Cow cow{ "Betsy" };
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
现在这个程序将编译并打印
Betsy says Moo
纯虚函数在我们想在基类中放置一个函数，但只有派生类知道它应该返回什么时非常有用。纯虚函数使得基类不能被实例化，并且派生类在实例化之前被迫定义这些函数。这有助于确保派生类不会忘记重新定义基类期望它们重新定义的函数。
就像普通的虚函数一样，纯虚函数可以使用对基类的引用（或指针）来调用
int main()
{
    Cow cow{ "Betsy" };
    Animal& a{ cow };

    std::cout << a.speak(); // resolves to Cow::speak(), prints "Moo"

    return 0;
}
在上面的示例中，
a.speak()
通过虚函数解析解析为
Cow::speak()
。
提醒
任何带有纯虚函数的类也应该有一个虚析构函数。
带定义的纯虚函数
事实证明，我们可以创建带定义的纯虚函数
#include <string>
#include <string_view>

class Animal // This Animal is an abstract base class
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() { return m_name; }
    virtual std::string_view speak() const = 0; // The = 0 means this function is pure virtual
    
    virtual ~Animal() = default;
};

std::string_view Animal::speak() const  // even though it has a definition
{
    return "buzz";
}
在这种情况下，speak() 仍然被认为是纯虚函数，因为有“= 0”（即使它已经被赋予了定义），并且 Animal 仍然被认为是抽象基类（因此不能被实例化）。任何继承自 Animal 的类都需要为 speak() 提供自己的定义，否则它也将被视为抽象基类。
在为纯虚函数提供定义时，定义必须单独提供（不能是内联的）。
对于 Visual Studio 用户
Visual Studio 允许纯虚函数声明即定义，例如
virtual std::string_view speak() const = 0
{
  return "buzz";
}
这不符合 C++ 标准，并且无法禁用。
当您希望基类为函数提供默认实现，但仍强制任何派生类提供自己的实现时，此范例会很有用。但是，如果派生类对基类提供的默认实现感到满意，它可以直接调用基类实现。例如
#include <iostream>
#include <string>
#include <string_view>

class Animal // This Animal is an abstract base class
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name(name)
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // note that speak is a pure virtual function
    
    virtual ~Animal() = default;
};

std::string_view Animal::speak() const
{
    return "buzz"; // some default implementation
}

class Dragonfly: public Animal
{

public:
    Dragonfly(std::string_view name)
        : Animal{name}
    {
    }

    std::string_view speak() const override// this class is no longer abstract because we defined this function
    {
        return Animal::speak(); // use Animal's default implementation
    }
};

int main()
{
    Dragonfly dfly{"Sally"};
    std::cout << dfly.getName() << " says " << dfly.speak() << '\n';

    return 0;
}
上面的代码打印
Sally says buzz
此功能并不常用。
析构函数可以设为纯虚函数，但必须给出定义，以便在派生对象被销毁时可以调用它。
接口类
一个
接口类
是没有成员变量，并且其中
所有
函数都是纯虚函数的类！接口在您希望定义派生类必须实现的功能，但将派生类如何实现该功能的细节完全留给派生类时非常有用。
接口类通常以 I 开头命名。这是一个示例接口类
#include <string_view>

class IErrorLog
{
public:
    virtual bool openLog(std::string_view filename) = 0;
    virtual bool closeLog() = 0;

    virtual bool writeError(std::string_view errorMessage) = 0;

    virtual ~IErrorLog() {} // make a virtual destructor in case we delete an IErrorLog pointer, so the proper derived destructor is called
};
任何继承自 IErrorLog 的类都必须为所有三个函数提供实现才能被实例化。您可以派生一个名为 FileErrorLog 的类，其中 openLog() 打开磁盘上的文件，closeLog() 关闭文件，writeError() 将消息写入文件。您可以派生另一个名为 ScreenErrorLog 的类，其中 openLog() 和 closeLog() 不执行任何操作，writeError() 在屏幕上的弹出消息框中打印消息。
现在，假设您需要编写一些使用错误日志的代码。如果您编写的代码直接包含 FileErrorLog 或 ScreenErrorLog，那么您实际上只能使用那种错误日志（至少无需重新编码您的程序）。例如，以下函数实际上强制 mySqrt() 的调用者使用 FileErrorLog，这可能不是他们想要的。
#include <cmath> // for sqrt()

double mySqrt(double value, FileErrorLog& log)
{
    if (value < 0.0)
    {
        log.writeError("Tried to take square root of value less than 0");
        return 0.0;
    }

    return std::sqrt(value);
}
实现此功能的更好方法是使用 IErrorLog
#include <cmath> // for sqrt()
double mySqrt(double value, IErrorLog& log)
{
    if (value < 0.0)
    {
        log.writeError("Tried to take square root of value less than 0");
        return 0.0;
    }

    return std::sqrt(value);
}
现在，调用者可以传入符合 IErrorLog 接口的
任何
类。如果他们想将错误记录到文件中，他们可以传入 FileErrorLog 的实例。如果他们想将其记录到屏幕上，他们可以传入 ScreenErrorLog 的实例。或者如果他们想做一些你甚至没有想到的事情，例如在发生错误时向某人发送电子邮件，他们可以从 IErrorLog 派生一个新类（例如 EmailErrorLog）并使用该类的实例！通过使用 IErrorLog，您的函数变得更独立和灵活。
别忘了为你的接口类包含一个虚析构函数，这样如果一个指向接口的指针被删除，就会调用正确的派生析构函数。
接口类已变得极其流行，因为它们易于使用、易于扩展且易于维护。事实上，一些现代语言，例如 Java 和 C#，已经添加了一个“interface”关键字，允许程序员直接定义一个接口类，而无需明确将所有成员函数标记为抽象。此外，尽管 Java 和 C# 不允许您在普通类上使用多重继承，但它们允许您多重继承任意数量的接口。因为接口没有数据也没有函数体，它们避免了多重继承的许多传统问题，同时仍然提供了很大的灵活性。
纯虚函数与虚函数表
为了保持一致性，抽象类仍然拥有虚函数表。抽象类的构造函数或析构函数可以调用虚函数，并且它需要解析到正确的函数（在同一个类中，因为派生类要么尚未构造，要么已被销毁）。
对于带有纯虚函数的类，虚函数表条目通常会包含一个空指针，或指向一个打印错误的通用函数（有时此函数名为 __purecall）。
下一课
25.8
虚基类
返回目录
上一课
25.6
虚函数表