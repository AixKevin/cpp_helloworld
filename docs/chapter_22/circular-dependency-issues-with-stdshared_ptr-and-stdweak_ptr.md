# 22.7 — std::shared_ptr 的循环依赖问题和 std::weak_ptr

22.7 — std::shared_ptr 的循环依赖问题和 std::weak_ptr
Alex
2017年3月21日，太平洋夏令时下午5:44
2024年7月22日
在上一课中，我们看到了 std::shared_ptr 如何允许我们有多个智能指针共同拥有同一资源。然而，在某些情况下，这可能会出现问题。考虑以下情况：两个独立对象中的共享指针互相指向对方
#include <iostream>
#include <memory> // for std::shared_ptr
#include <string>

class Person
{
	std::string m_name;
	std::shared_ptr<Person> m_partner; // initially created empty

public:
		
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") }; // create a Person named "Lucy"
	auto ricky { std::make_shared<Person>("Ricky") }; // create a Person named "Ricky"

	partnerUp(lucy, ricky); // Make "Lucy" point to "Ricky" and vice-versa

	return 0;
}
在上面的例子中，我们使用 make_shared() 动态分配了两个人，“Lucy”和“Ricky”（以确保 lucy 和 ricky 在 main() 结束时被销毁）。然后我们让他们成为伙伴。这将“Lucy”中的 std::shared_ptr 设置为指向“Ricky”，将“Ricky”中的 std::shared_ptr 设置为指向“Lucy”。共享指针旨在共享，因此 lucy 共享指针和 Rick 的 m_partner 共享指针都指向“Lucy”（反之亦然）是没有问题的。
然而，这个程序并没有按预期执行
Lucy created
Ricky created
Lucy is now partnered with Ricky
就是这样。没有发生任何解分配。哦哦。发生了什么？
调用 partnerUp() 后，有两个共享指针指向“Ricky”（ricky 和 Lucy 的 m_partner），有两个共享指针指向“Lucy”（lucy 和 Ricky 的 m_partner）。
在 main() 结束时，ricky 共享指针首先超出范围。当发生这种情况时，ricky 会检查是否有其他共享指针共同拥有“Ricky”这个人。有（Lucy 的 m_partner）。因此，它不会解分配“Ricky”（如果解分配了，那么 Lucy 的 m_partner 就会变成一个悬空指针）。此时，我们现在有一个指向“Ricky”的共享指针（Lucy 的 m_partner）和两个指向“Lucy”的共享指针（lucy 和 Ricky 的 m_partner）。
接下来，lucy 共享指针超出范围，同样的事情发生了。共享指针 lucy 检查是否有其他共享指针共同拥有“Lucy”这个人。有（Ricky 的 m_partner），所以“Lucy”没有被解分配。此时，有一个指向“Lucy”的共享指针（Ricky 的 m_partner）和一个指向“Ricky”的共享指针（Lucy 的 m_partner）。
然后程序结束——“Lucy”和“Ricky”都没有被解分配！本质上，“Lucy”阻止了“Ricky”被销毁，而“Ricky”阻止了“Lucy”被销毁。
事实证明，只要共享指针形成循环引用，就会发生这种情况。
循环引用
循环引用
（也称为
循环引用
或
环
）是一系列引用，其中每个对象引用下一个对象，并且最后一个对象引用回第一个对象，从而形成一个引用循环。这些引用不必是实际的 C++ 引用——它们可以是指针、唯一 ID 或任何其他标识特定对象的方法。
在共享指针的上下文中，引用将是指针。
这正是我们在上述情况中看到的：“Lucy”指向“Ricky”，而“Ricky”指向“Lucy”。如果PointersA指向B，B指向C，C指向A，三个指针也会出现同样的情况。共享指针形成循环的实际效果是，每个对象都保持下一个对象存活——最后一个对象保持第一个对象存活。因此，系列中的任何对象都无法被释放，因为它们都认为其他对象仍然需要它！
一个简化的情况
事实证明，即使是单个 std::shared_ptr 也会发生这种循环引用问题——一个引用包含它的对象的 std::shared_ptr 仍然是一个循环（只是一个简化的循环）。尽管这在实践中不太可能发生，但我们将向您展示以增加理解
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource
{
public:
	std::shared_ptr<Resource> m_ptr {}; // initially created empty
	
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };

	ptr1->m_ptr = ptr1; // m_ptr is now sharing the Resource that contains it

	return 0;
}
在上面的示例中，当 ptr1 超出作用域时，Resource 未被解除分配，因为 Resource 的 m_ptr 正在共享 Resource。此时，释放 Resource 的唯一方法是将 m_ptr 设置为其他值（这样就没有东西再共享 Resource 了）。但是我们无法访问 m_ptr，因为 ptr1 超出作用域，所以我们不再有办法做到这一点。Resource 已经成为内存泄漏。
因此，程序打印
Resource acquired
就是这样。
那么 std::weak_ptr 到底有什么用呢？
std::weak_ptr 的设计是为了解决上述“循环所有权”问题。std::weak_ptr 是一个观察者——它可以观察和访问与 std::shared_ptr（或其他 std::weak_ptr）相同的对象，但它不被视为所有者。请记住，当 std::shared_ptr 超出作用域时，它只考虑是否有其他 std::shared_ptr 共同拥有该对象。std::weak_ptr 不计入其中！
让我们用 std::weak_ptr 来解决我们的人际问题
#include <iostream>
#include <memory> // for std::shared_ptr and std::weak_ptr
#include <string>

class Person
{
	std::string m_name;
	std::weak_ptr<Person> m_partner; // note: This is now a std::weak_ptr

public:
		
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") };
	auto ricky { std::make_shared<Person>("Ricky") };

	partnerUp(lucy, ricky);

	return 0;
}
此代码运行正常
Lucy created
Ricky created
Lucy is now partnered with Ricky
Ricky destroyed
Lucy destroyed
功能上，它与有问题的示例几乎完全相同。然而，现在当 ricky 超出作用域时，它会发现没有其他 std::shared_ptr 指向“Ricky”（“Lucy”中的 std::weak_ptr 不计入其中）。因此，它将解分配“Ricky”。lucy 也是如此。
使用 std::weak_ptr
std::weak_ptr 的一个缺点是 std::weak_ptr 不能直接使用（它们没有 operator->）。要使用 std::weak_ptr，您必须首先将其转换为 std::shared_ptr。然后您可以使用 std::shared_ptr。要将 std::weak_ptr 转换为 std::shared_ptr，您可以使用 lock() 成员函数。下面是上述示例，更新后展示了这一点
#include <iostream>
#include <memory> // for std::shared_ptr and std::weak_ptr
#include <string>

class Person
{
	std::string m_name;
	std::weak_ptr<Person> m_partner; // note: This is now a std::weak_ptr

public:

	Person(const std::string &name) : m_name(name)
	{
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}

	std::shared_ptr<Person> getPartner() const { return m_partner.lock(); } // use lock() to convert weak_ptr to shared_ptr
	const std::string& getName() const { return m_name; }
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") };
	auto ricky { std::make_shared<Person>("Ricky") };

	partnerUp(lucy, ricky);

	auto partner = ricky->getPartner(); // get shared_ptr to Ricky's partner
	std::cout << ricky->getName() << "'s partner is: " << partner->getName() << '\n';

	return 0;
}
这会打印
Lucy created
Ricky created
Lucy is now partnered with Ricky
Ricky's partner is: Lucy
Ricky destroyed
Lucy destroyed
我们不必担心 std::shared_ptr 变量“partner”的循环依赖关系，因为它只是函数内部的局部变量。它最终会在函数结束时超出范围，并且引用计数将减 1。
使用 std::weak_ptr 避免悬空指针
考虑一个普通“愚蠢”指针持有某个对象的地址，然后该对象被销毁的情况。这样的指针是悬空的，解引用该指针将导致未定义行为。不幸的是，我们无法判断持有非空地址的指针是否悬空。这是愚蠢指针危险的重要原因。
因为 std::weak_ptr 不会保持拥有的资源存活，所以 std::weak_ptr 同样可能指向已被 std::shared_ptr 解分配的资源。然而，std::weak_ptr 有一个巧妙的技巧——因为它有权访问对象的引用计数，所以它可以确定它是否指向有效对象！如果引用计数非零，则资源仍然有效。如果引用计数为零，则资源已被销毁。
测试 std::weak_ptr 是否有效的最简单方法是使用
expired()
成员函数，如果 std::weak_ptr 指向无效对象，则返回
true
，否则返回
false
。
以下是一个简单示例，展示了这种行为差异
// h/t to reader Waldo for an early version of this example
#include <iostream>
#include <memory>

class Resource
{
public:
	Resource() { std::cerr << "Resource acquired\n"; }
	~Resource() { std::cerr << "Resource destroyed\n"; }
};

// Returns a std::weak_ptr to an invalid object
std::weak_ptr<Resource> getWeakPtr()
{
	auto ptr{ std::make_shared<Resource>() };
	return std::weak_ptr<Resource>{ ptr };
} // ptr goes out of scope, Resource destroyed

// Returns a dumb pointer to an invalid object
Resource* getDumbPtr()
{
	auto ptr{ std::make_unique<Resource>() };
	return ptr.get();
} // ptr goes out of scope, Resource destroyed

int main()
{
	auto dumb{ getDumbPtr() };
	std::cout << "Our dumb ptr is: " << ((dumb == nullptr) ? "nullptr\n" : "non-null\n");

	auto weak{ getWeakPtr() };
	std::cout << "Our weak ptr is: " << ((weak.expired()) ? "expired\n" : "valid\n");

	return 0;
}
这会打印
Resource acquired
Resource destroyed
Our dumb ptr is: non-null
Resource acquired
Resource destroyed
Our weak ptr is: expired
getDumbPtr()
和
getWeakPtr()
都使用智能指针来分配 Resource——此智能指针确保分配的 Resource 将在函数结束时被销毁。当
getDumbPtr()
返回 Resource* 时，它返回一个悬空指针（因为 std::unique_ptr 在函数结束时销毁了 Resource）。当
getWeakPtr()
返回 std::weak_ptr 时，该 std::weak_ptr 同样指向一个无效对象（因为 std::shared_ptr 在函数结束时销毁了 Resource）。
在 main() 中，我们首先测试返回的哑指针是否为
nullptr
。因为哑指针仍然持有已释放资源的地址，所以此测试失败。
main()
无法判断此指针是否悬空。在这种情况下，因为它是悬空指针，如果我们解引用此指针，将导致未定义行为。
接下来，我们测试
weak.expired()
是否为
true
。由于
weak
指向的对象的引用计数为
0
（因为指向的对象已经销毁），所以这解析为
true
。
main()
中的代码因此可以判断
weak
指向一个无效对象，我们可以根据需要有条件地编写代码！
请注意，如果 std::weak_ptr 已过期，则不应对其调用
lock()
，因为所指向的对象已经销毁，因此没有可共享的对象。如果您对已过期的 std::weak_ptr 调用
lock()
，它将返回一个指向
nullptr
的 std::shared_ptr。
总结
当您需要多个可以共同拥有资源的智能指针时，可以使用 std::shared_ptr。当最后一个 std::shared_ptr 超出作用域时，资源将被解除分配。当您希望智能指针可以查看和使用共享资源，但不参与该资源的所有权时，可以使用 std::weak_ptr。
小测验时间
问题 #1
修复“简化情况”部分中呈现的程序，以便 Resource 得到正确解除分配。不要修改
main()
中的代码。
为方便参考，此处再次列出该程序
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource
{
public:
	std::shared_ptr<Resource> m_ptr {}; // initially created empty
	
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };

	ptr1->m_ptr = ptr1; // m_ptr is now sharing the Resource that contains it

	return 0;
}
显示答案
#include <iostream>
#include <memory> // for std::shared_ptr and std::weak_ptr

class Resource
{
public:
	std::weak_ptr<Resource> m_ptr {}; // use std::weak_ptr so m_ptr doesn't keep the Resource alive
	
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };

	ptr1->m_ptr = ptr1; // m_ptr is now sharing the Resource that contains it

	return 0;
}
下一课
22.x
第 22 章总结与测验
返回目录
上一课
22.6
std::shared_ptr