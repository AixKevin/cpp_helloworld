# 14.11 — 默认构造函数和默认实参

14.11 — 默认构造函数和默认实参
Alex
2023年9月11日，下午12:21 PDT
2024年9月16日
默认构造函数
是不接受任何实参的构造函数。通常，这是一个没有参数的构造函数。
这是一个包含默认构造函数的类示例
#include <iostream>

class Foo
{
public:
    Foo() // default constructor
    {
        std::cout << "Foo default constructed\n";
    }
};

int main()
{
    Foo foo{}; // No initialization values, calls Foo's default constructor

    return 0;
}
当上述程序运行时，会创建一个
Foo
类型的对象。由于没有提供初始化值，因此会调用默认构造函数
Foo()
，它会打印
Foo default constructed
类类型的值初始化与默认初始化
如果一个类类型有默认构造函数，则值初始化和默认初始化都会调用默认构造函数。因此，对于像上面示例中的
Foo
类这样的类，以下是基本等效的
Foo foo{}; // value initialization, calls Foo() default constructor
    Foo foo2;  // default initialization, calls Foo() default constructor
然而，正如我们在课程
13.9 -- 默认成员初始化
中已经介绍过的，值初始化对于聚合类型更安全。由于很难判断一个类类型是聚合类型还是非聚合类型，因此最好对所有类型都使用值初始化，而不必担心这个问题。
最佳实践
对于所有类类型，优先使用值初始化而不是默认初始化。
带有默认实参的构造函数
与所有函数一样，构造函数的最右边参数可以有默认实参。
相关内容
我们在课程
11.5 -- 默认实参
中介绍了默认实参。
例如
#include <iostream>

class Foo
{
private:
    int m_x { };
    int m_y { };

public:
    Foo(int x=0, int y=0) // has default arguments
        : m_x { x }
        , m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo1{};     // calls Foo(int, int) constructor using default arguments
    Foo foo2{6, 7}; // calls Foo(int, int) constructor

    return 0;
}
这会打印
Foo(0, 0) constructed
Foo(6, 7) constructed
如果构造函数中的所有参数都有默认实参，则该构造函数是默认构造函数（因为它可以在没有实参的情况下调用）。
我们将在下一课（
14.12 -- 委托构造函数
）中看到这有用处的示例。
重载构造函数
因为构造函数是函数，所以它们可以被重载。也就是说，我们可以有多个构造函数，以便以不同的方式构造对象
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() // default constructor
    {
        std::cout << "Foo constructed\n";
    }

    Foo(int x, int y) // non-default constructor
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo1{};     // Calls Foo() constructor
    Foo foo2{6, 7}; // Calls Foo(int, int) constructor

    return 0;
}
上述推论是，一个类应该只有一个默认构造函数。如果提供了多个默认构造函数，编译器将无法消除歧义，无法确定应该使用哪个构造函数
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() // default constructor
    {
        std::cout << "Foo constructed\n";
    }

    Foo(int x=1, int y=2) // default constructor
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo{}; // compile error: ambiguous constructor function call

    return 0;
}
在上面的示例中，我们实例化
foo
时没有传入任何实参，因此编译器会寻找一个默认构造函数。它会找到两个，并且无法消除歧义，无法确定应该使用哪个构造函数。这将导致编译错误。
隐式默认构造函数
如果一个非聚合类类型对象没有用户声明的构造函数，编译器将生成一个公共默认构造函数（以便该类可以进行值或默认初始化）。这个构造函数被称为
隐式默认构造函数
。
考虑以下示例
#include <iostream>

class Foo
{
private:
    int m_x{};
    int m_y{};

    // Note: no constructors declared
};

int main()
{
    Foo foo{};

    return 0;
}
这个类没有用户声明的构造函数，因此编译器将为我们生成一个隐式默认构造函数。该构造函数将用于实例化
foo{}
。
隐式默认构造函数等同于一个没有参数、没有成员初始化列表，并且构造函数体中没有语句的构造函数。换句话说，对于上面的
Foo
类，编译器生成了以下代码
public:
    Foo() // implicitly generated default constructor
    {
    }
隐式默认构造函数主要在我们没有数据成员的类中很有用。如果一个类有数据成员，我们可能希望它们可以通过用户提供的值进行初始化，而隐式默认构造函数不足以满足此要求。
使用
= default
生成显式默认构造函数
在我们需要编写一个等同于隐式生成的默认构造函数的情况下，我们可以转而告诉编译器为我们生成一个默认构造函数。这个构造函数被称为
显式默认构造函数
，它可以通过使用
= default
语法生成
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() = default; // generates an explicitly defaulted default constructor

    Foo(int x, int y)
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo{}; // calls Foo() default constructor

    return 0;
}
在上面的示例中，由于我们有一个用户声明的构造函数（
Foo(int, int)
），通常不会隐式生成默认构造函数。然而，因为我们告诉编译器生成这样一个构造函数，它就会生成。这个构造函数随后将被我们的
foo{}
实例化所使用。
最佳实践
优先使用显式默认构造函数（
= default
）而不是空体的默认构造函数。
显式默认构造函数与空的自定义构造函数
至少有两种情况下，显式默认构造函数的行为与空的自定义构造函数不同。
当对一个类进行值初始化时，如果该类有一个用户定义的默认构造函数，则对象将进行默认初始化。然而，如果该类有一个非用户提供的默认构造函数（即，一个隐式定义或使用
= default
定义的默认构造函数），则对象在默认初始化之前将被零初始化。
#include <iostream>

class User
{
private:
    int m_a; // note: no default initialization value
    int m_b {};

public:
    User() {} // user-defined empty constructor

    int a() const { return m_a; }
    int b() const { return m_b; }
};

class Default
{
private:
    int m_a; // note: no default initialization value
    int m_b {};

public:
    Default() = default; // explicitly defaulted default constructor

    int a() const { return m_a; }
    int b() const { return m_b; }
};

class Implicit
{
private:
    int m_a; // note: no default initialization value
    int m_b {};

public:
    // implicit default constructor

    int a() const { return m_a; }
    int b() const { return m_b; }
};

int main()
{
    User user{}; // default initialized
    std::cout << user.a() << ' ' << user.b() << '\n';

    Default def{}; // zero initialized, then default initialized
    std::cout << def.a() << ' ' << def.b() << '\n';

    Implicit imp{}; // zero initialized, then default initialized
    std::cout << imp.a() << ' ' << imp.b() << '\n';

    return 0;
}
在作者的机器上，这会打印出
782510864 0
0 0
0 0
注意
user.a
在默认初始化之前没有零初始化，因此保持未初始化状态。
实际上，这应该不重要，因为您应该为所有数据成员提供默认成员初始化器！
提示
对于没有用户提供的默认构造函数的类，值初始化将首先零初始化该类，而默认初始化则不会。鉴于此，默认初始化可能比值初始化性能更高（但安全性较低）。如果您想在代码中初始化大量没有用户提供的默认构造函数的对象，并且需要榨取每一丝性能，那么将这些对象更改为默认初始化可能值得探索。或者，您可以尝试将类更改为具有空体的默认构造函数。这在使用值初始化时避免了零初始化的情况，但可能会抑制其他优化。
在 C++20 之前，带有用户定义默认构造函数（即使其为空体）的类会使其成为非聚合类型，而显式默认的默认构造函数则不会。假设该类原本是聚合类型，前者会导致该类使用列表初始化而不是聚合初始化。从 C++20 开始，这种不一致性得到了解决，因此两者都使该类成为非聚合类型。
仅在有意义时创建默认构造函数
默认构造函数允许我们在没有用户提供的初始化值的情况下创建非聚合类类型的对象。因此，只有当使用所有默认值创建类类型对象有意义时，类才应该提供默认构造函数。
例如
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    Fraction() = default;
    Fraction(int numerator, int denominator)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f1 {3, 5};
    f1.print();

    Fraction f2 {}; // will get Fraction 0/1
    f2.print();

    return 0;
}
对于表示分数的类，允许用户创建没有初始化器的 Fraction 对象是有意义的（在这种情况下，用户将得到分数 0/1）。
现在考虑这个类
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{ };
    int m_id{ };

public:
    Employee(std::string_view name, int id)
        : m_name{ name }
        , m_id{ id }
    {
    }

    void print() const
    {
        std::cout << "Employee(" << m_name << ", " << m_id << ")\n";
    }
};

int main()
{
    Employee e1 { "Joe", 1 };
    e1.print();

    Employee e2 {}; // compile error: no matching constructor
    e2.print();

    return 0;
}
对于代表雇员的类，允许创建没有姓名的雇员是没有意义的。因此，这样的类不应该有默认构造函数，这样如果类的用户试图这样做，就会导致编译错误。
下一课
14.12
委托构造函数
返回目录
上一课
14.10
构造函数成员初始化列表