# 24.5 — 继承和访问修饰符

24.5 — 继承和访问修饰符
Alex
2008 年 1 月 14 日，下午 1:09 PST
2023 年 9 月 11 日
在本章之前的课程中，您已经了解了一些关于基本继承是如何工作的知识。到目前为止，我们所有的示例都使用了公有继承。也就是说，我们的派生类公有继承基类。
在本课中，我们将更深入地探讨公有继承，以及另外两种继承（私有和保护）。我们还将探讨不同类型的继承如何与访问修饰符交互，以允许或限制对成员的访问。
到目前为止，您已经了解了私有（private）和公有（public）访问修饰符，它们决定了谁可以访问类的成员。快速回顾一下，公有成员可以被任何人访问。私有成员只能被同一类的成员函数或友元访问。这意味着派生类不能直接访问基类的私有成员！
class Base
{
private:
    int m_private {}; // can only be accessed by Base members and friends (not derived classes)
public:
    int m_public {}; // can be accessed by anybody
};
这相当直接，您现在应该已经很习惯了。
保护（protected）访问修饰符
在处理继承类时，事情会变得稍微复杂一些。
C++ 有第三个我们尚未讨论的访问修饰符，因为它只在继承上下文中才有用。**保护（protected）**访问修饰符允许成员所属的类、友元和派生类访问该成员。但是，保护成员不能从类外部访问。
class Base
{
public:
    int m_public {}; // can be accessed by anybody
protected:
    int m_protected {}; // can be accessed by Base members, friends, and derived classes
private:
    int m_private {}; // can only be accessed by Base members and friends (but not derived classes)
};

class Derived: public Base
{
public:
    Derived()
    {
        m_public = 1; // allowed: can access public base members from derived class
        m_protected = 2; // allowed: can access protected base members from derived class
        m_private = 3; // not allowed: can not access private base members from derived class
    }
};

int main()
{
    Base base;
    base.m_public = 1; // allowed: can access public members from outside class
    base.m_protected = 2; // not allowed: can not access protected members from outside class
    base.m_private = 3; // not allowed: can not access private members from outside class

    return 0;
}
在上面的示例中，您可以看到受保护的基类成员 `m_protected` 可以被派生类直接访问，但不能被公有部分访问。
那么我什么时候应该使用保护访问修饰符呢？
在基类中使用保护属性，派生类可以直接访问该成员。这意味着如果您稍后更改该保护属性的任何内容（类型、值的含义等），您可能需要同时更改基类和所有派生类。
因此，当您（或您的团队）将从自己的类派生，并且派生类的数量合理时，使用保护访问修饰符最有用。这样，如果您更改基类的实现，并且因此需要更新派生类，您可以自己进行更新（并且不会花费太长时间，因为派生类的数量有限）。
将您的成员设为私有意味着公有和派生类不能直接更改基类。这有利于将公有或派生类与实现更改隔离开来，并确保不变量得到妥善维护。但是，这也意味着您的类可能需要更大的公有（或保护）接口来支持公有或派生类操作所需的所有函数，这本身就需要构建、测试和维护成本。
通常，如果可以的话，最好将您的成员设为私有，并且只在计划有派生类且构建和维护这些私有成员的接口成本过高时才使用保护。
最佳实践
优先使用私有成员而不是保护成员。
不同类型的继承及其对访问的影响
首先，类有三种不同的继承方式：公有（public）、保护（protected）和私有（private）。
为此，只需在选择要继承的类时指定所需的访问类型即可
// Inherit from Base publicly
class Pub: public Base
{
};

// Inherit from Base protectedly
class Pro: protected Base
{
};

// Inherit from Base privately
class Pri: private Base
{
};

class Def: Base // Defaults to private inheritance
{
};
如果您不选择继承类型，C++ 默认使用私有继承（就像成员默认使用私有访问一样，如果您不另行指定）。
这给我们带来了 9 种组合：3 种成员访问修饰符（public、private 和 protected）和 3 种继承类型（public、private 和 protected）。
那么这些有什么区别呢？简而言之，当成员被继承时，继承成员的访问修饰符可能会根据所使用的继承类型而改变（仅在派生类中）。换句话说，在基类中是公有或保护的成员可能会在派生类中改变访问修饰符。
这可能看起来有点令人困惑，但并没有那么糟糕。我们将在本课的其余部分详细探讨这一点。
在逐步查看示例时，请记住以下规则
一个类总是可以访问其自己的（非继承的）成员。
公有部分根据其访问的类的访问修饰符来访问类的成员。
派生类根据从父类继承的访问修饰符访问继承成员。这取决于所使用的访问修饰符和继承类型。
公有继承
公有继承是迄今为止最常用的继承类型。事实上，您很少会看到或使用其他类型的继承，因此您的主要重点应该放在理解本节。幸运的是，公有继承也是最容易理解的。当您公有继承一个基类时，继承的公有成员保持公有，继承的保护成员保持保护。继承的私有成员，因为它们在基类中是私有的而无法访问，所以仍然无法访问。
基类中的访问修饰符
公有继承时的访问修饰符
公共
公共
受保护的
受保护的
私有的
不可访问
这是一个示例，展示了事情是如何工作的
class Base
{
public:
    int m_public {};
protected:
    int m_protected {};
private:
    int m_private {};
};

class Pub: public Base // note: public inheritance
{
    // Public inheritance means:
    // Public inherited members stay public (so m_public is treated as public)
    // Protected inherited members stay protected (so m_protected is treated as protected)
    // Private inherited members stay inaccessible (so m_private is inaccessible)
public:
    Pub()
    {
        m_public = 1; // okay: m_public was inherited as public
        m_protected = 2; // okay: m_protected was inherited as protected
        m_private = 3; // not okay: m_private is inaccessible from derived class
    }
};

int main()
{
    // Outside access uses the access specifiers of the class being accessed.
    Base base;
    base.m_public = 1; // okay: m_public is public in Base
    base.m_protected = 2; // not okay: m_protected is protected in Base
    base.m_private = 3; // not okay: m_private is private in Base

    Pub pub;
    pub.m_public = 1; // okay: m_public is public in Pub
    pub.m_protected = 2; // not okay: m_protected is protected in Pub
    pub.m_private = 3; // not okay: m_private is inaccessible in Pub

    return 0;
}
这与上面我们介绍保护访问修饰符的示例相同，只是我们也实例化了派生类，只是为了表明在公有继承的情况下，基类和派生类中的行为是相同的。
除非您有特殊原因，否则您应该使用公有继承。
最佳实践
除非您有特殊原因，否则请使用公有继承。
保护继承
保护继承是最不常见的继承方法。除了在非常特殊的情况下，它几乎从不使用。通过保护继承，公有和保护成员变为保护，私有成员保持不可访问。
由于这种形式的继承非常罕见，我们将跳过示例，只用表格总结
基类中的访问修饰符
保护继承时的访问修饰符
公共
受保护的
受保护的
受保护的
私有的
不可访问
私有继承
通过私有继承，基类的所有成员都作为私有成员继承。这意味着私有成员无法访问，保护成员和公有成员变为私有。
请注意，这不影响派生类访问从其父类继承的成员的方式！它只影响试图通过派生类访问这些成员的代码。
class Base
{
public:
    int m_public {};
protected:
    int m_protected {};
private:
    int m_private {};
};

class Pri: private Base // note: private inheritance
{
    // Private inheritance means:
    // Public inherited members become private (so m_public is treated as private)
    // Protected inherited members become private (so m_protected is treated as private)
    // Private inherited members stay inaccessible (so m_private is inaccessible)
public:
    Pri()
    {
        m_public = 1; // okay: m_public is now private in Pri
        m_protected = 2; // okay: m_protected is now private in Pri
        m_private = 3; // not okay: derived classes can't access private members in the base class
    }
};

int main()
{
    // Outside access uses the access specifiers of the class being accessed.
    // In this case, the access specifiers of base.
    Base base;
    base.m_public = 1; // okay: m_public is public in Base
    base.m_protected = 2; // not okay: m_protected is protected in Base
    base.m_private = 3; // not okay: m_private is private in Base

    Pri pri;
    pri.m_public = 1; // not okay: m_public is now private in Pri
    pri.m_protected = 2; // not okay: m_protected is now private in Pri
    pri.m_private = 3; // not okay: m_private is inaccessible in Pri

    return 0;
}
以表格形式总结
基类中的访问修饰符
私有继承时的访问修饰符
公共
私有的
受保护的
私有的
私有的
不可访问
当派生类与基类没有明显的关联，但内部使用基类实现时，私有继承可能很有用。在这种情况下，我们可能不希望基类的公有接口通过派生类的对象暴露出来（如果公有继承就会这样）。
实际上，私有继承很少使用。
最后一个例子
class Base
{
public:
	int m_public {};
protected:
	int m_protected {};
private:
	int m_private {};
};
基类可以无限制地访问其自身成员。公有部分只能访问 `m_public`。派生类可以访问 `m_public` 和 `m_protected`。
class D2 : private Base // note: private inheritance
{
	// Private inheritance means:
	// Public inherited members become private
	// Protected inherited members become private
	// Private inherited members stay inaccessible
public:
	int m_public2 {};
protected:
	int m_protected2 {};
private:
	int m_private2 {};
};
D2 可以无限制地访问其自身成员。D2 可以访问 Base 的 `m_public` 和 `m_protected` 成员，但不能访问 `m_private`。因为 D2 私有继承了 Base，所以通过 D2 访问 `m_public` 和 `m_protected` 时，它们现在被视为私有。这意味着公有部分在使用 D2 对象时无法访问这些变量，从 D2 派生的任何类也无法访问。
class D3 : public D2
{
	// Public inheritance means:
	// Public inherited members stay public
	// Protected inherited members stay protected
	// Private inherited members stay inaccessible
public:
	int m_public3 {};
protected:
	int m_protected3 {};
private:
	int m_private3 {};
};
D3 可以无限制地访问其自身成员。D3 可以访问 D2 的 `m_public2` 和 `m_protected2` 成员，但不能访问 `m_private2`。因为 D3 公有继承了 D2，所以通过 D3 访问 `m_public2` 和 `m_protected2` 时，它们保留其访问修饰符。D3 无法访问 Base 的 `m_private`，它在 Base 中已经是私有的。它也无法访问 Base 的 `m_protected` 或 `m_public`，当 D2 继承它们时，两者都变为私有。
总结
访问修饰符、继承类型和派生类之间的交互方式造成了很多混淆。为了尽可能地澄清问题
首先，一个类（及其友元）总是可以访问其自身非继承的成员。访问修饰符只影响外部人员和派生类是否可以访问这些成员。
其次，当派生类继承成员时，这些成员可能会在派生类中改变访问修饰符。这不影响派生类自身的（非继承的）成员（它们有自己的访问修饰符）。它只影响外部人员和从派生类派生的类是否可以访问这些继承成员。
这是所有访问修饰符和继承类型组合的表格
基类中的访问修饰符
公有继承时的访问修饰符
私有继承时的访问修饰符
保护继承时的访问修饰符
公共
公共
私有的
受保护的
受保护的
受保护的
私有的
受保护的
私有的
不可访问
不可访问
不可访问
最后一点，尽管在上面的示例中，我们只展示了使用成员变量的示例，但这些访问规则适用于所有成员（例如成员函数和在类中声明的类型）。
下一课
24.6
向派生类添加新功能
返回目录
上一课
24.4
派生类的构造函数和初始化