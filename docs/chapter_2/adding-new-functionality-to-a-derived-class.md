# 24.6 — 向派生类添加新功能

24.6 — 向派生类添加新功能
Alex
2008 年 1 月 17 日，太平洋标准时间下午 4:06
2023 年 9 月 11 日
在
继承简介
课程中，我们提到使用派生类的最大好处之一是能够重用已经编写的代码。您可以继承基类功能，然后添加新功能、修改现有功能或隐藏您不想要的功能。在本课程和接下来的几节课中，我们将仔细研究如何完成这些事情。
首先，让我们从一个简单的基类开始
#include <iostream>

class Base
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value { value }
    {
    }

    void identify() const { std::cout << "I am a Base\n"; }
};
现在，让我们创建一个从 Base 继承的派生类。因为我们希望派生类能够在派生对象实例化时设置 m_value 的值，所以我们将让 Derived 构造函数在初始化列表中调用 Base 构造函数。
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }
};
向派生类添加新功能
在上面的例子中，因为我们可以访问 Base 类的源代码，所以如果需要，我们可以直接向 Base 添加功能。
有时我们可能可以访问基类，但不想修改它。考虑这样一种情况：您刚刚从第三方供应商那里购买了一个代码库，但需要一些额外的功能。您可以添加到原始代码中，但这并不是最好的解决方案。如果供应商向您发送更新怎么办？您的添加项要么被覆盖，要么您必须手动将它们迁移到更新中，这既耗时又存在风险。
或者，有时甚至不可能修改基类。考虑标准库中的代码。我们无法修改作为标准库一部分的代码。但是我们可以从这些类继承，然后将我们自己的功能添加到我们的派生类中。对于提供头文件但代码是预编译的第三方库也是如此。
在这两种情况下，最好的答案是派生自己的类，并将您想要的功能添加到派生类中。
Base 类的一个明显遗漏是公开访问 m_value 的方式。我们可以通过在 Base 类中添加一个访问函数来补救这一点——但为了举例，我们将把它添加到派生类中。因为 m_value 已在 Base 类中声明为 protected，所以 Derived 可以直接访问它。
要向派生类添加新功能，只需像往常一样在派生类中声明该功能即可
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }

    int getValue() const { return m_value; }
};
现在，公共部分将能够对 Derived 类型的对象调用 getValue() 来访问 m_value 的值。
int main()
{
    Derived derived { 5 };
    std::cout << "derived has value " << derived.getValue() << '\n';

    return 0;
}
这会产生结果
derived has value 5
尽管这可能很明显，但 Base 类型的对象无法访问 Derived 中的 getValue() 函数。以下代码无效
int main()
{
    Base base { 5 };
    std::cout << "base has value " << base.getValue() << '\n';

    return 0;
}
这是因为 Base 中没有 getValue() 函数。函数 getValue() 属于 Derived。因为 Derived 是 Base，所以 Derived 可以访问 Base 中的内容。但是，Base 无法访问 Derived 中的任何内容。
下一课
24.7
调用继承函数和覆盖行为
返回目录
上一课
24.5
继承和访问说明符