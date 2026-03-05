# 14.7 — 成员函数返回数据成员的引用

14.7 — 成员函数返回数据成员的引用
Alex
2023年10月5日，太平洋夏令时12:55
2024年3月29日
在第
12.12 课 — 通过引用返回和通过地址返回
中，我们讨论了通过引用返回。特别地，我们指出：“通过引用返回的对象在函数返回后必须存在”。这意味着我们不应该通过引用返回局部变量，因为局部变量被销毁后引用将悬空。但是，通常可以通过引用返回通过引用传递的函数参数，或者具有静态持续时间的变量（无论是静态局部变量还是全局变量），因为它们通常在函数返回后不会被销毁。
例如
// Takes two std::string objects, returns the one that comes first alphabetically
const std::string& firstAlphabetical(const std::string& a, const std::string& b)
{
	return (a < b) ? a : b; // We can use operator< on std::string to determine which comes first alphabetically
}

int main()
{
	std::string hello { "Hello" };
	std::string world { "World" };

	std::cout << firstAlphabetical(hello, world); // either hello or world will be returned by reference

	return 0;
}
成员函数也可以通过引用返回，它们遵循与非成员函数相同的安全返回引用规则。然而，成员函数有一个我们需要讨论的额外情况：成员函数返回数据成员的引用。
这在 getter 访问函数中最常见，因此我们将使用 getter 成员函数来说明这个主题。但请注意，这个主题适用于任何返回数据成员引用的成员函数。
按值返回数据成员可能开销很大
考虑以下示例
#include <iostream>
#include <string>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	std::string getName() const { return m_name; } //  getter returns by value
};

int main()
{
	Employee joe{};
	joe.setName("Joe");
	std::cout << joe.getName();

	return 0;
}
在此示例中，
getName()
访问函数按值返回
std::string m_name
。
虽然这是最安全的方法，但也意味着每次调用
getName()
时都会对
m_name
进行一次昂贵的复制。由于访问函数倾向于被大量调用，这通常不是最佳选择。
通过左值引用返回数据成员
成员函数也可以通过（const）左值引用返回数据成员。
数据成员与包含它们的对象具有相同的生命周期。由于成员函数总是对一个对象调用，并且该对象必须存在于调用者的作用域中，因此成员函数通常可以安全地通过（const）左值引用返回数据成员（因为通过引用返回的成员在函数返回时仍将存在于调用者的作用域中）。
让我们更新上面的示例，以便
getName()
通过 const 左值引用返回
m_name
#include <iostream>
#include <string>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	const std::string& getName() const { return m_name; } //  getter returns by const reference
};

int main()
{
	Employee joe{}; // joe exists until end of function
	joe.setName("Joe");

	std::cout << joe.getName(); // returns joe.m_name by reference

	return 0;
}
现在，当调用
joe.getName()
时，
joe.m_name
通过引用返回给调用者，避免了复制。然后调用者使用此引用将
joe.m_name
打印到控制台。
因为
joe
在调用者的作用域中一直存在到
main()
函数的末尾，所以对
joe.m_name
的引用在相同持续时间内也有效。
关键见解
返回对数据成员的（const）左值引用是可以的。隐式对象（包含数据成员）在函数返回后仍存在于调用者的作用域中，因此任何返回的引用都将有效。
返回数据成员引用的成员函数的返回类型应与数据成员的类型匹配
一般来说，通过引用返回的成员函数的返回类型应与要返回的数据成员的类型匹配。在上面的示例中，
m_name
的类型是
std::string
，因此
getName()
返回
const std::string&
。
返回
std::string_view
将需要在每次调用函数时创建并返回一个临时
std::string_view
。这是不必要的低效。如果调用者想要一个
std::string_view
，他们可以自己进行转换。
最佳实践
返回引用的成员函数应返回与要返回的数据成员相同类型的引用，以避免不必要的转换。
对于 getter，使用
auto
让编译器从返回的成员推断返回类型是一种有用的方法，可以确保不发生转换
#include <iostream>
#include <string>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	const auto& getName() const { return m_name; } // uses `auto` to deduce return type from m_name
};

int main()
{
	Employee joe{}; // joe exists until end of function
	joe.setName("Joe");

	std::cout << joe.getName(); // returns joe.m_name by reference

	return 0;
}
相关内容
我们在第
10.9 课 — 函数的类型推导
中介绍了
auto
返回类型。
然而，从文档角度来看，使用
auto
返回类型会模糊 getter 的返回类型。例如
const auto& getName() const { return m_name; } // uses `auto` to deduce return type from m_name
不清楚此函数实际返回何种类型的字符串（它可能是
std::string
、
std::string_view
、C 风格字符串或完全不同的东西！）。
因此，我们通常更喜欢显式返回类型。
右值隐式对象和按引用返回
有一种情况我们需要稍微小心。在上面的示例中，
joe
是一个左值对象，它一直存在到函数结束。因此，
joe.getName()
返回的引用也将在函数结束之前有效。
但是，如果我们的隐式对象是右值呢（例如某些按值返回的函数的返回值）？右值对象在创建它们的完整表达式结束时被销毁。当右值对象被销毁时，对该右值成员的任何引用都将失效并悬空，使用此类引用将导致未定义行为。
因此，对右值对象成员的引用只能在创建右值对象的完整表达式中安全使用。
提示
我们在第
1.10 课 — 表达式简介
中介绍了什么是完整表达式。
警告
右值对象在其创建的完整表达式结束时被销毁。此时，对右值对象成员的任何引用都将悬空。
对右值对象成员的引用只能在创建右值对象的完整表达式中安全使用。
让我们探讨一些相关情况
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	const std::string& getName() const { return m_name; } //  getter returns by const reference
};

// createEmployee() returns an Employee by value (which means the returned value is an rvalue)
Employee createEmployee(std::string_view name)
{
	Employee e;
	e.setName(name);
	return e;
}

int main()
{
	// Case 1: okay: use returned reference to member of rvalue class object in same expression
	std::cout << createEmployee("Frank").getName();

	// Case 2: bad: save returned reference to member of rvalue class object for use later
	const std::string& ref { createEmployee("Garbo").getName() }; // reference becomes dangling when return value of createEmployee() is destroyed
	std::cout << ref; // undefined behavior

	// Case 3: okay: copy referenced value to local variable for use later
	std::string val { createEmployee("Hans").getName() }; // makes copy of referenced member
	std::cout << val; // okay: val is independent of referenced member

	return 0;
}
当调用
createEmployee()
时，它将按值返回一个
Employee
对象。这个返回的
Employee
对象是一个右值，它将一直存在到包含
createEmployee()
调用的完整表达式结束。当该右值对象被销毁时，对该对象成员的任何引用都将变为悬空。
在情况 1 中，我们调用
createEmployee("Frank")
，它返回一个右值
Employee
对象。然后我们在这个右值对象上调用
getName()
，它返回对
m_name
的引用。然后立即使用此引用将名称打印到控制台。此时，包含
createEmployee("Frank")
调用的完整表达式结束，并且右值对象及其成员被销毁。由于右值对象或其成员在此之后不再使用，因此此情况是没问题的。
在情况 2 中，我们遇到了问题。首先，
createEmployee("Garbo")
返回一个右值对象。然后我们调用
getName()
来获取对该右值的
m_name
成员的引用。然后使用此
m_name
成员初始化
ref
。此时，包含
createEmployee("Garbo")
调用的完整表达式结束，并且右值对象及其成员被销毁。这使得
ref
悬空。因此，当我们在后续语句中使用
ref
时，我们正在访问一个悬空引用，并导致未定义行为。
关键见解
完整表达式的求值在作为初始化器的任何完整表达式的使用之后结束。这允许对象用相同类型的右值初始化（因为右值在初始化发生后才会被销毁）。
但是，如果我们想从一个按引用返回成员的函数中保存一个值以供以后使用呢？我们可以使用返回的引用来初始化一个非引用局部变量，而不是使用返回的引用来初始化一个局部引用变量。
在情况 3 中，我们使用返回的引用来初始化非引用局部变量
val
。这将导致被引用的成员被复制到
val
中。初始化后，
val
独立于引用而存在。因此，当右值对象随后被销毁时，
val
不受影响。因此，
val
可以在将来的语句中毫无问题地输出。
安全地使用按引用返回的成员函数
尽管右值隐式对象存在潜在危险，但习惯上 getter 会按 const 引用而不是按值返回昂贵的类型。
鉴于此，让我们讨论如何安全地使用此类函数的返回值。上面示例中的三种情况说明了三个关键点
优先立即使用按引用返回的成员函数的返回值（情况 1 所示）。由于这适用于左值和右值对象，因此如果您始终这样做，您将避免麻烦。
不要“保存”返回的引用以供以后使用（情况 2 所示），除非您确定隐式对象是左值。如果对右值隐式对象执行此操作，则在使用现在悬空的引用时将导致未定义行为。
如果您确实需要保留返回的引用以供以后使用，并且不确定隐式对象是否是左值，则将返回的引用用作非引用局部变量的初始化器，这将把被引用的成员复制到局部变量中（情况 3 所示）。
最佳实践
优先立即使用按引用返回的成员函数的返回值，以避免隐式对象是右值时出现悬空引用问题。
不要返回私有数据成员的非 const 引用
因为引用就像被引用的对象一样，所以返回非 const 引用的成员函数提供对该成员的直接访问（即使该成员是私有的）。
例如
#include <iostream>

class Foo
{
private:
    int m_value{ 4 }; // private member

public:
    int& value() { return m_value; } // returns a non-const reference (don't do this)
};

int main()
{
    Foo f{};                // f.m_value is initialized to default value 4
    f.value() = 5;          // The equivalent of m_value = 5
    std::cout << f.value(); // prints 5

    return 0;
}
因为
value()
返回对
m_value
的非 const 引用，所以调用者可以使用该引用直接访问（并更改
m_value
的值）。
这允许调用者规避访问控制系统。
const 成员函数不能返回数据成员的非 const 引用
const 成员函数不允许返回成员的非 const 引用。这是有道理的——const 成员函数不允许修改对象的 states，也不允许调用会修改对象 state 的函数。它不应该做任何可能导致对象修改的事情。
如果 const 成员函数被允许返回成员的非 const 引用，它将为调用者提供直接修改该成员的方法。这违反了 const 成员函数的意图。
下一课
14.8
数据隐藏（封装）的好处
返回目录
上一课
14.6
访问函数