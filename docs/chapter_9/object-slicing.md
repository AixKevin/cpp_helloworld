# 25.9 — 对象切片

25.9 — 对象切片
Alex
2016年11月19日，太平洋标准时间下午1:10
2024年10月28日
我们回到之前看过的例子
#include <iostream>
#include <string_view>

class Base
{
protected:
    int m_value{};
 
public:
    Base(int value)
        : m_value{ value }
    {
    }

    virtual ~Base() = default;

    virtual std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};
 
class Derived: public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }
 
   std::string_view getName() const override { return "Derived"; }
};

int main()
{
    Derived derived{ 5 };
    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';
 
    Base& ref{ derived };
    std::cout << "ref is a " << ref.getName() << " and has value " << ref.getValue() << '\n';
 
    Base* ptr{ &derived };
    std::cout << "ptr is a " << ptr->getName() << " and has value " << ptr->getValue() << '\n';
 
    return 0;
}
在上面的例子中，ref 引用了 derived，ptr 指向了 derived，derived 有一个 Base 部分和一个 Derived 部分。由于 ref 和 ptr 的类型都是 Base，ref 和 ptr 只能看到 derived 的 Base 部分——derived 的 Derived 部分仍然存在，但无法通过 ref 或 ptr 看到。然而，通过使用虚函数，我们可以访问函数的“最派生”版本。因此，上面的程序打印
derived is a Derived and has value 5
ref is a Derived and has value 5
ptr is a Derived and has value 5
但是，如果不是将 Base 引用或指针设置为 Derived 对象，而是简单地将 Derived 对象“赋值”给 Base 对象，会发生什么？
int main()
{
    Derived derived{ 5 };
    Base base{ derived }; // what happens here?
    std::cout << "base is a " << base.getName() << " and has value " << base.getValue() << '\n';

    return 0;
}
请记住，derived 有一个 Base 部分和一个 Derived 部分。当我们把一个 Derived 对象赋值给一个 Base 对象时，只有 Derived 对象的 Base 部分被复制。Derived 部分则不会被复制。在上面的例子中，base 接收了 derived 的 Base 部分的副本，但没有接收 Derived 部分。那个 Derived 部分实际上已经被“切掉”了。因此，将一个 Derived 类对象赋值给一个 Base 类对象被称为 **对象切片**（或简称切片）。
因为 base 过去是而且现在仍然只是一个 Base，Base 的虚指针仍然指向 Base。因此，base.getName() 解析为 Base::getName()。
上面的例子打印：
base is a Base and has value 5
如果谨慎使用，切片可能是无害的。但是，如果使用不当，切片可能会以多种不同的方式导致意外结果。让我们检查其中一些情况。
切片和函数
现在，你可能会觉得上面的例子有点傻。毕竟，为什么要那样把 derived 赋值给 base 呢？你可能不会那样做。然而，切片在函数中意外发生的可能性要大得多。
考虑以下函数
void printName(const Base base) // note: base passed by value, not reference
{
    std::cout << "I am a " << base.getName() << '\n';
}
这是一个相当简单的函数，带有一个按值传递的 const base 对象参数。如果我们这样调用这个函数
int main()
{
    Derived d{ 5 };
    printName(d); // oops, didn't realize this was pass by value on the calling end

    return 0;
}
当你编写这个程序时，你可能没有注意到 base 是一个值参数，而不是引用。因此，当调用 printName(d) 时，虽然我们可能期望 base.getName() 调用虚函数 getName() 并打印“I am a Derived”，但这并没有发生。相反，Derived 对象 d 被切片，只有 Base 部分被复制到 base 参数中。当 base.getName() 执行时，即使 getName() 函数是虚化的，也没有 Derived 部分可供它解析。因此，这个程序打印
I am a Base
在这种情况下，发生的事情很明显，但是如果你的函数没有打印任何识别信息，那么追踪错误可能会很困难。
当然，通过将函数参数设为引用而不是按值传递，可以很容易地避免这里的切片（这也是将类按引用而不是按值传递的一个好主意）。
void printName(const Base& base) // note: base now passed by reference
{
    std::cout << "I am a " << base.getName() << '\n';
}

int main()
{
    Derived d{ 5 };
    printName(d);

    return 0;
}
这会打印
I am a Derived
切片向量
新程序员在切片方面遇到麻烦的另一个领域是尝试使用 `std::vector` 实现多态性。考虑以下程序
#include <vector>

int main()
{
	std::vector<Base> v{};
	v.push_back(Base{ 5 });    // add a Base object to our vector
	v.push_back(Derived{ 6 }); // add a Derived object to our vector

        // Print out all of the elements in our vector
	for (const auto& element : v)
		std::cout << "I am a " << element.getName() << " with value " << element.getValue() << '\n';

	return 0;
}
这个程序编译得很好。但是运行时，它打印
I am a Base with value 5
I am a Base with value 6
与前面的例子类似，因为 `std::vector` 被声明为 `Base` 类型的向量，所以当 `Derived(6)` 被添加到向量中时，它被切片了。
解决这个问题有点困难。许多新程序员尝试创建对象的 `std::vector` 引用，像这样
std::vector<Base&> v{};
不幸的是，这无法编译。`std::vector` 的元素必须是可赋值的，而引用不能被重新赋值（只能初始化）。
一种解决方法是创建一个指针向量
#include <iostream>
#include <vector>

int main()
{
	std::vector<Base*> v{};
	
	Base b{ 5 }; // b and d can't be anonymous objects
	Derived d{ 6 };

	v.push_back(&b); // add a Base object to our vector
	v.push_back(&d); // add a Derived object to our vector

	// Print out all of the elements in our vector
	for (const auto* element : v)
		std::cout << "I am a " << element->getName() << " with value " << element->getValue() << '\n';

	return 0;
}
这会打印
I am a Base with value 5
I am a Derived with value 6
这确实有效！关于这一点有几点说明。首先，nullptr 现在是一个有效选项，这可能合乎心意，也可能不合心意。其次，你现在必须处理指针语义，这可能很麻烦。但好处是使用指针可以我们将动态分配的对象放入向量中（只是别忘了明确删除它们）。
另一个选项是使用 `std::reference_wrapper`，这是一个模仿可重新赋值引用的类
#include <functional> // for std::reference_wrapper
#include <iostream>
#include <string_view>
#include <vector>

class Base
{
protected:
    int m_value{};

public:
    Base(int value)
        : m_value{ value }
    {
    }
    virtual ~Base() = default;

    virtual std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived : public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

    std::string_view getName() const override { return "Derived"; }
};

int main()
{
	std::vector<std::reference_wrapper<Base>> v{}; // a vector of reassignable references to Base

	Base b{ 5 }; // b and d can't be anonymous objects
	Derived d{ 6 };

	v.push_back(b); // add a Base object to our vector
	v.push_back(d); // add a Derived object to our vector

	// Print out all of the elements in our vector
	// we use .get() to get our element out of the std::reference_wrapper
	for (const auto& element : v) // element has type const std::reference_wrapper<Base>&
		std::cout << "I am a " << element.get().getName() << " with value " << element.get().getValue() << '\n';

	return 0;
}
弗兰肯斯坦对象
在上面的例子中，我们看到了切片导致错误结果的情况，因为派生类被切掉了。现在我们来看看另一种危险的情况，即派生对象仍然存在！
考虑以下代码：
int main()
{
    Derived d1{ 5 };
    Derived d2{ 6 };
    Base& b{ d2 };

    b = d1; // this line is problematic

    return 0;
}
函数中的前三行非常简单。创建两个派生对象，并将一个基类引用设置为第二个对象。
第四行是出错的地方。由于 b 指向 d2，而我们将 d1 赋值给 b，你可能会认为结果是 d1 会被复制到 d2 中——如果 b 是 Derived 类型，确实会这样。但是 b 是 Base 类型，而且 C++ 为类提供的 `operator=` 默认情况下不是虚函数。因此，会调用复制 Base 类的赋值运算符，并且只有 d1 的 Base 部分被复制到 d2 中。
结果，你会发现 d2 现在拥有 d1 的 Base 部分和 d2 的 Derived 部分。在这个特定的例子中，这没有问题（因为 Derived 类没有自己的数据），但在大多数情况下，你将只是创建了一个弗兰肯斯坦对象——由多个对象的部件组成。
更糟糕的是，没有简单的方法可以阻止这种情况发生（除了尽可能避免这种赋值）。
提示
如果基类不是为自身实例化而设计的（例如，它只是一个接口类），可以通过使基类不可复制（通过删除基类复制构造函数和基类赋值运算符）来避免切片。
总结
尽管 C++ 支持通过对象切片将派生对象赋值给基对象，但通常情况下，这只会带来麻烦，你应该尽量避免切片。确保你的函数参数是引用（或指针），并尽量避免在派生类中使用任何形式的按值传递。
下一课
25.10
动态转换
返回目录
上一课
25.8
虚基类