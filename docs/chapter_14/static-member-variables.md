# 15.6 — 静态成员变量

15.6 — 静态成员变量
Alex
2007 年 9 月 14 日，上午 9:50 PDT
2024 年 12 月 2 日
在课程
7.4 — 全局变量简介
中，我们介绍了全局变量，在课程
7.11 — 静态局部变量
中，我们介绍了静态局部变量。这两种类型的变量都具有静态持续时间，这意味着它们在程序启动时创建，并在程序结束时销毁。即使它们超出作用域，此类变量也会保留其值。
例如
#include <iostream>

int generateID()
{
    static int s_id{ 0 }; // static local variable
    return ++s_id;
}

int main()
{
    std::cout << generateID() << '\n';
    std::cout << generateID() << '\n';
    std::cout << generateID() << '\n';

    return 0;
}
这个程序打印
1
2
3
请注意，静态局部变量
s_id
在多次函数调用中都保留了其值。
类类型为
static
关键字带来了另外两种用途：静态成员变量和静态成员函数。幸运的是，这些用途相当简单。我们将在本课中讨论静态成员变量，在下一课中讨论静态成员函数。
静态成员变量
在深入探讨应用于成员变量的 static 关键字之前，首先考虑以下类
#include <iostream>

struct Something
{
    int value{ 1 };
};

int main()
{
    Something first{};
    Something second{};
    
    first.value = 2;

    std::cout << first.value << '\n';
    std::cout << second.value << '\n';

    return 0;
}
当我们实例化一个类对象时，每个对象都会获得所有普通成员变量的副本。在这种情况下，因为我们声明了两个
Something
类对象，所以我们最终得到了两个
value
的副本：
first.value
和
second.value
。
first.value
与
second.value
是不同的。因此，上面的程序打印
2
1
类的成员变量可以通过使用
static
关键字来设置为静态。与普通成员变量不同，
静态成员变量
由类的所有对象共享。考虑以下程序，与上面类似
#include <iostream>

struct Something
{
    static int s_value; // declare s_value as static (initializer moved below)
};

int Something::s_value{ 1 }; // define and initialize s_value to 1 (we'll discuss this section below)

int main()
{
    Something first{};
    Something second{};

    first.s_value = 2;

    std::cout << first.s_value << '\n';
    std::cout << second.s_value << '\n';
    return 0;
}
此程序生成以下输出：
2
2
因为
s_value
是一个静态成员变量，所以
s_value
在类的所有对象之间共享。因此，
first.s_value
与
second.s_value
是同一个变量。上面的程序表明，我们使用
first
设置的值可以使用
second
访问！
静态成员不与类对象关联
尽管您可以通过类对象访问静态成员（如上例中所示的
first.s_value
和
second.s_value
），但即使没有实例化任何类对象，静态成员也存在！这很合理：它们在程序开始时创建，在程序结束时销毁，因此它们的生命周期不像普通成员那样与类对象绑定。
本质上，静态成员是存在于类作用域区域内的全局变量。类的静态成员与命名空间中的普通变量之间几乎没有区别。
关键见解
静态成员是存在于类作用域区域内的全局变量。
因为静态成员
s_value
独立于任何类对象而存在，所以它可以直接使用类名和作用域解析运算符访问（在本例中为
Something::s_value
）
class Something
{
public:
    static int s_value; // declare s_value as static
};

int Something::s_value{ 1 }; // define and initialize s_value to 1 (we'll discuss this section below)

int main()
{
    // note: we're not instantiating any objects of type Something

    Something::s_value = 2;
    std::cout << Something::s_value << '\n';
    return 0;
}
在上面的代码片段中，
s_value
通过类名
Something
而不是通过对象引用。请注意，我们甚至没有实例化
Something
类型的对象，但我们仍然能够访问和使用
Something::s_value
。这是访问静态成员的首选方法。
最佳实践
使用类名和作用域解析运算符 (::) 访问静态成员。
定义和初始化静态成员变量
当我们在类类型中声明一个静态成员变量时，我们只是告诉编译器存在一个静态成员变量，但实际上并没有定义它（很像前向声明）。由于静态成员变量本质上是全局变量，因此您必须在类外部的全局作用域中显式定义（并可选地初始化）静态成员。
在上面的示例中，我们通过此行实现这一点
int Something::s_value{ 1 }; // define and initialize s_value to 1
这行代码有两个目的：它实例化静态成员变量（就像全局变量一样），并初始化它。在这种情况下，我们提供了初始化值
1
。如果没有提供初始化器，静态成员变量默认会进行零初始化。
请注意，此静态成员定义不受访问控制：即使它在类中声明为私有（或受保护），您也可以定义和初始化该值（因为定义不被视为一种访问形式）。
对于非模板类，如果类在头文件 (.h) 中定义，则静态成员定义通常放置在类的相关代码文件（例如
Something.cpp
）中。或者，成员也可以定义为
inline
并放置在头文件中的类定义下方（这对于仅头文件库很有用）。如果类在源 (.cpp) 文件中定义，则静态成员定义通常直接放置在类下方。不要将静态成员定义放在头文件中（很像全局变量，如果该头文件被多次包含，您最终会得到多个定义，这将导致链接器错误）。
对于模板类，（模板化的）静态成员定义通常直接放置在头文件中的模板类定义下方（这不会违反 ODR，因为此类定义是隐式内联的）。
在类定义中初始化静态成员变量
上述方法有一些捷径。首先，当静态成员是常量整数类型（包括
char
和
bool
）或 const 枚举时，静态成员可以在类定义中初始化
class Whatever
{
public:
    static const int s_value{ 4 }; // a static const int can be defined and initialized directly
};
在上面的示例中，因为静态成员变量是 const int，所以不需要显式定义行。允许使用此快捷方式，因为这些特定的 const 类型是编译时常量。
在课程
7.10 — 在多个文件之间共享全局常量（使用内联变量）
中，我们介绍了内联变量，这些变量允许有多个定义。C++17 允许静态成员成为内联变量
class Whatever
{
public:
    static inline int s_value{ 4 }; // a static inline variable can be defined and initialized directly
};
此类变量可以在类定义内部初始化，无论它们是否为常量。这是定义和初始化静态成员的首选方法。
由于
constexpr
成员在 C++17 中是隐式内联的，因此静态
constexpr
成员也可以在类定义中初始化，而无需显式使用
inline
关键字
#include <string_view>

class Whatever
{
public:
    static constexpr double s_value{ 2.2 }; // ok
    static constexpr std::string_view s_view{ "Hello" }; // this even works for classes that support constexpr initialization
};
最佳实践
将静态成员声明为
inline
或
constexpr
，以便它们可以在类定义中初始化。
静态成员变量的示例
为什么要在类中使用静态变量？一种用途是为类的每个实例分配唯一的 ID。这是一个示例
#include <iostream>

class Something
{
private:
    static inline int s_idGenerator { 1 };
    int m_id {};

public:
    // grab the next value from the id generator
    Something() : m_id { s_idGenerator++ } 
    {    
    }

    int getID() const { return m_id; }
};

int main()
{
    Something first{};
    Something second{};
    Something third{};

    std::cout << first.getID() << '\n';
    std::cout << second.getID() << '\n';
    std::cout << third.getID() << '\n';
    return 0;
}
这个程序打印
1
2
3
因为
s_idGenerator
由所有
Something
对象共享，所以当创建新的
Something
对象时，构造函数使用
s_idGenerator
的当前值初始化
m_id
，然后为下一个对象递增该值。这保证了每个实例化的
Something
对象都接收到一个唯一的 ID（按创建顺序递增）。
为每个对象赋予唯一的 ID 有助于调试，因为它可以用来区分具有相同数据的对象。在处理数据数组时尤其如此。
当类需要使用查找表（例如，用于存储一组预计算值的数组）时，静态成员变量也很有用。通过使查找表静态化，所有对象只存在一个副本，而不是为每个实例化的对象创建副本。这可以节省大量的内存。
只有静态成员才能使用类型推导（
auto
和 CTAD）
静态成员可以使用
auto
从其初始化器推导其类型，或使用类模板参数推导 (CTAD) 从初始化器推导模板类型参数。
非静态成员不能使用
auto
或 CTAD。
造成这种区别的原因非常复杂，但归结为非静态成员可能出现某些情况，导致歧义或非直观结果。静态成员不会出现这种情况。因此，非静态成员被限制使用这些功能，而静态成员则不受限制。
#include <utility> // for std::pair<T, U>

class Foo
{
private:
    auto m_x { 5 };           // auto not allowed for non-static members
    std::pair m_v { 1, 2.3 }; // CTAD not allowed for non-static members

    static inline auto s_x { 5 };           // auto allowed for static members
    static inline std::pair s_v { 1, 2.3 }; // CTAD allowed for static members

public:
    Foo() {};
};

int main()
{
    Foo foo{};
    
    return 0;
}
下一课
15.7
静态成员函数
返回目录
上一课
15.5
带有成员函数的类模板