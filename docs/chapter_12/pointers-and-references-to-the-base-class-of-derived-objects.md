# 25.1 — 派生对象的基类指针和引用

25.1 — 派生对象的基类指针和引用
Alex
2008 年 1 月 29 日，太平洋标准时间下午 3:45
2024 年 11 月 25 日
在上一章中，你学习了如何使用继承从现有类派生新类。在本章中，我们将重点关注继承最重要和最强大的一个方面——虚函数。
但在讨论什么是虚函数之前，我们首先为为什么需要它们打下基础。
在关于
派生类的构造顺序
的章节中，你了解到当你创建一个派生类时，它由多个部分组成：每个继承类一个部分，以及自身一个部分。
例如，这是一个简单的例子
#include <string_view>

class Base
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value{ value }
    {
    }

    std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived: public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

    std::string_view getName() const { return "Derived"; }
    int getValueDoubled() const { return m_value * 2; }
};
当我们创建一个 Derived 对象时，它包含一个 Base 部分（首先构造），和一个 Derived 部分（其次构造）。请记住，继承意味着两个类之间存在 is-a 关系。由于 Derived is-a Base，因此 Derived 包含一个 Base 部分是合适的。
指针、引用和派生类
我们应该很直观地能够将 Derived 指针和引用设置为 Derived 对象
#include <iostream>

int main()
{
    Derived derived{ 5 };
    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';

    Derived& rDerived{ derived };
    std::cout << "rDerived is a " << rDerived.getName() << " and has value " << rDerived.getValue() << '\n';

    Derived* pDerived{ &derived };
    std::cout << "pDerived is a " << pDerived->getName() << " and has value " << pDerived->getValue() << '\n';

    return 0;
}
这会产生以下输出
derived is a Derived and has value 5
rDerived is a Derived and has value 5
pDerived is a Derived and has value 5
然而，由于 Derived 有一个 Base 部分，一个更有趣的问题是 C++ 是否允许我们将 Base 指针或引用设置为 Derived 对象。事实证明，我们可以！
#include <iostream>

int main()
{
    Derived derived{ 5 };

    // These are both legal!
    Base& rBase{ derived }; // rBase is an lvalue reference (not an rvalue reference)
    Base* pBase{ &derived };

    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';
    std::cout << "rBase is a " << rBase.getName() << " and has value " << rBase.getValue() << '\n';
    std::cout << "pBase is a " << pBase->getName() << " and has value " << pBase->getValue() << '\n';

    return 0;
}
这会产生结果
derived is a Derived and has value 5
rBase is a Base and has value 5
pBase is a Base and has value 5
这个结果可能一开始并不完全符合你的预期！
事实证明，因为 rBase 和 pBase 是 Base 引用和指针，它们只能看到 Base 的成员（或 Base 继承的任何类）。因此，即使 Derived::getName() 遮蔽（隐藏）了 Derived 对象的 Base::getName()，Base 指针/引用也无法看到 Derived::getName()。因此，它们调用 Base::getName()，这就是 rBase 和 pBase 报告它们是 Base 而不是 Derived 的原因。
请注意，这也意味着无法使用 rBase 或 pBase 调用 Derived::getValueDoubled()。它们无法看到 Derived 中的任何内容。
这是另一个稍微复杂一点的例子，我们将在下一课中在此基础上进行构建
#include <iostream>
#include <string_view>
#include <string>

class Animal
{
protected:
    std::string m_name;

    // We're making this constructor protected because
    // we don't want people creating Animal objects directly,
    // but we still want derived classes to be able to use it.
    Animal(std::string_view name)
        : m_name{ name }
    {
    }
    
    // To prevent slicing (covered later)
    Animal(const Animal&) = delete;
    Animal& operator=(const Animal&) = delete;

public:
    std::string_view getName() const { return m_name; }
    std::string_view speak() const { return "???"; }
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const { return "Woof"; }
};

int main()
{
    const Cat cat{ "Fred" };
    std::cout << "cat is named " << cat.getName() << ", and it says " << cat.speak() << '\n';

    const Dog dog{ "Garbo" };
    std::cout << "dog is named " << dog.getName() << ", and it says " << dog.speak() << '\n';

    const Animal* pAnimal{ &cat };
    std::cout << "pAnimal is named " << pAnimal->getName() << ", and it says " << pAnimal->speak() << '\n';

    pAnimal = &dog;
    std::cout << "pAnimal is named " << pAnimal->getName() << ", and it says " << pAnimal->speak() << '\n';

    return 0;
}
这会产生结果
cat is named Fred, and it says Meow
dog is named Garbo, and it says Woof
pAnimal is named Fred, and it says ???
pAnimal is named Garbo, and it says ???
我们在这里看到了同样的问题。因为 pAnimal 是一个 Animal 指针，它只能看到类的 Animal 部分。因此，
pAnimal->speak()
调用 Animal::speak() 而不是 Dog::Speak() 或 Cat::speak() 函数。
基类指针和引用的用途
现在你可能会说：“上面的例子看起来有点傻。当我可以直接使用派生对象时，为什么我要将指针或引用设置为派生对象的基类呢？”事实证明，有很多很好的理由。
首先，假设你想编写一个函数来打印动物的名字和声音。如果不使用基类的指针，你必须使用重载函数来编写它，像这样
void report(const Cat& cat)
{
    std::cout << cat.getName() << " says " << cat.speak() << '\n';
}

void report(const Dog& dog)
{
    std::cout << dog.getName() << " says " << dog.speak() << '\n';
}
不难，但想象一下如果我们有 30 种不同的动物类型而不是 2 种会发生什么。你将不得不编写 30 个几乎相同的函数！此外，如果你添加了一种新类型的动物，你也必须为它编写一个新函数。考虑到唯一的真正区别是参数的类型，这会浪费大量时间。
然而，因为 Cat 和 Dog 都继承自 Animal，所以 Cat 和 Dog 都有一个 Animal 部分。因此，我们应该能够做类似的事情是有意义的
void report(const Animal& rAnimal)
{
    std::cout << rAnimal.getName() << " says " << rAnimal.speak() << '\n';
}
这将允许我们传入任何从 Animal 派生的类，甚至是我们在编写函数后创建的类！而不是每个派生类一个函数，我们得到一个适用于所有从 Animal 派生的类的函数！
问题当然是，因为 rAnimal 是一个 Animal 引用，
rAnimal.speak()
将调用 Animal::speak() 而不是派生版本的 speak()。
题外话…
我们还可以使用模板函数来减少需要编写的重载函数的数量
template <typename T>
void report(const T& rAnimal)
{
    std::cout << rAnimal.getName() << " says " << rAnimal.speak() << '\n';
}
虽然这有效，但它有自己的问题
不清楚
T
应该是什么类型，因为我们丢失了
T
意图是
Animal
的文档。
此函数不强制
T
是
Animal
。相反，它将接受任何包含
getName()
和
speak()
成员函数的类型的对象，无论这是否有意义。
其次，假设你有 3 只猫和 3 条狗，你想将它们放在一个数组中以便于访问。因为数组只能容纳一种类型的对象，如果没有基类的指针或引用，你将不得不为每种派生类型创建一个不同的数组，像这样
#include <array>
#include <iostream>

// Cat and Dog from the example above

int main()
{
    const auto& cats{ std::to_array<Cat>({{ "Fred" }, { "Misty" }, { "Zeke" }}) };
    const auto& dogs{ std::to_array<Dog>({{ "Garbo" }, { "Pooky" }, { "Truffle" }}) };
    
    // Before C++20
    // const std::array<Cat, 3> cats{{ { "Fred" }, { "Misty" }, { "Zeke" } }};
    // const std::array<Dog, 3> dogs{{ { "Garbo" }, { "Pooky" }, { "Truffle" } }};

    for (const auto& cat : cats)
    {
        std::cout << cat.getName() << " says " << cat.speak() << '\n';
    }

    for (const auto& dog : dogs)
    {
        std::cout << dog.getName() << " says " << dog.speak() << '\n';
    }

    return 0;
}
现在，想象一下如果你有 30 种不同类型的动物会发生什么。你需要 30 个数组，每种动物一个！
然而，因为 Cat 和 Dog 都继承自 Animal，所以我们应该能够做类似的事情是有意义的
#include <array>
#include <iostream>

// Cat and Dog from the example above

int main()
{
    const Cat fred{ "Fred" };
    const Cat misty{ "Misty" };
    const Cat zeke{ "Zeke" };

    const Dog garbo{ "Garbo" };
    const Dog pooky{ "Pooky" };
    const Dog truffle{ "Truffle" };

    // Set up an array of pointers to animals, and set those pointers to our Cat and Dog objects
    const auto animals{ std::to_array<const Animal*>({&fred, &garbo, &misty, &pooky, &truffle, &zeke }) };
    
    // Before C++20, with the array size being explicitly specified
    // const std::array<const Animal*, 6> animals{ &fred, &garbo, &misty, &pooky, &truffle, &zeke };
    
    for (const auto animal : animals)
    {
        std::cout << animal->getName() << " says " << animal->speak() << '\n';
    }

    return 0;
}
虽然这会编译和执行，但不幸的是，数组“animals”的每个元素都是指向 Animal 的指针这一事实意味着
animal->speak()
将调用 Animal::speak() 而不是我们想要的派生类的 speak() 版本。输出是
Fred says ???
Garbo says ???
Misty says ???
Pooky says ???
Truffle says ???
Zeke says ???
尽管这两种技术都可以为我们节省大量时间和精力，但它们有相同的问题。基类的指针或引用调用函数的基类版本而不是派生版本。如果有一种方法可以使这些基类指针调用函数的派生版本而不是基类版本就好了……
想猜猜虚函数是用来做什么的吗？:)
小测验时间
我们上面的 Animal/Cat/Dog 示例不起作用，因为 Animal 的引用或指针无法访问返回猫或狗正确值所需的 speak() 的派生版本。解决此问题的一种方法是使 speak() 函数返回的数据作为 Animal 基类的一部分可访问（很像 Animal 的名称可通过成员 m_name 访问）。
更新上面课程中的 Animal、Cat 和 Dog 类，向 Animal 添加一个名为 m_speak 的新成员。适当初始化它。以下程序应该正常工作
#include <array>
#include <iostream>

int main()
{
    const Cat fred{ "Fred" };
    const Cat misty{ "Misty" };
    const Cat zeke{ "Zeke" };

    const Dog garbo{ "Garbo" };
    const Dog pooky{ "Pooky" };
    const Dog truffle{ "Truffle" };

    // Set up an array of pointers to animals, and set those pointers to our Cat and Dog objects
    const auto animals{ std::to_array<const Animal*>({ &fred, &garbo, &misty, &pooky, &truffle, &zeke }) };
    
    // Before C++20, with the array size being explicitly specified
    // const std::array<const Animal*, 6> animals{ &fred, &garbo, &misty, &pooky, &truffle, &zeke };
    
    for (const auto animal : animals)
    {
        std::cout << animal->getName() << " says " << animal->speak() << '\n';
    }

    return 0;
}
显示答案
#include <array>
#include <string>
#include <string_view>
#include <iostream>

class Animal
{
protected:
    std::string m_name;
    std::string m_speak;

    // We're making this constructor protected because
    // we don't want people creating Animal objects directly,
    // but we still want derived classes to be able to use it.
    Animal(std::string_view name, std::string_view speak)
        : m_name{ name }, m_speak{ speak }
    {
    }
    
    // To prevent slicing (covered later)
    Animal(const Animal&) = delete;
    Animal& operator=(const Animal&) = delete;

public:
    std::string_view getName() const { return m_name; }
    std::string_view speak() const { return m_speak; }
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name, "Meow" }
    {
    }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name, "Woof" }
    {
    }
};

int main()
{
    const Cat fred{ "Fred" };
    const Cat misty{ "Misty" };
    const Cat zeke{ "Zeke" };

    const Dog garbo{ "Garbo" };
    const Dog pooky{ "Pooky" };
    const Dog truffle{ "Truffle" };

    // Set up an array of pointers to animals, and set those pointers to our Cat and Dog objects
    const auto animals{ std::to_array<const Animal*>({ &fred, &garbo, &misty, &pooky, &truffle, &zeke }) };
    
    // Before C++20, with the array size being explicitly specified
    // const std::array<const Animal*, 6> animals{ &fred, &garbo, &misty, &pooky, &truffle, &zeke };
    
    // animal is not a reference, because we're looping over pointers
    for (const auto animal : animals)
    {
        std::cout << animal->getName() << " says " << animal->speak() << '\n';
    }

    return 0;
}
为什么上述解决方案不是最优的？
提示：考虑 Cat 和 Dog 的未来状态，我们希望以更多方式区分 Cat 和 Dog。
提示：考虑在初始化时需要设置成员的限制。
显示答案
当前的解决方案由于多种原因不是最优的。
首先，我们需要为我们想要区分 Cat 和 Dog 的每种方式向 Animal 添加一个成员。随着时间的推移，我们的 Animal 类可能会在内存方面变得非常大，并且变得复杂！
其次，此解决方案仅在基类成员可以在初始化时确定时才有效。例如，如果 speak() 为每个 Animal 返回一个随机结果（例如，调用 Dog::speak() 可以返回“woof”、“arf”或“yip”），这种解决方案开始变得笨拙和崩溃。
第三，因为 speak() 是 Animal 的成员，所以 speak() 对于 Cat 和 Dog 将具有相同的行为（也就是说，它将始终返回 m_speak）。如果我们希望
speak()
对 Cat 和 Dog 具有不同的行为（例如，让 Dog 返回随机声音），我们必须将所有这些额外逻辑放入 Animal 中，这使得 Animal 更加复杂。
下一课
25.2
虚函数和多态
返回目录
上一课
24.x
第 24 章总结和测验