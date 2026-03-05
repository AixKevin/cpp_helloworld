# 15.10 — 引用限定符

15.10 — 引用限定符
Alex
2023 年 10 月 5 日，太平洋时间下午 12:59
2024 年 9 月 25 日
作者注
这是一个可选课程。我们建议您粗略阅读以熟悉材料，但无需全面理解即可继续学习后续课程。
在
第 14.7 课——返回数据成员引用的成员函数
中，我们讨论了当隐式对象是右值时，调用返回数据成员引用的访问函数可能很危险。这里快速回顾一下
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
	std::string m_name{};

public:
	Employee(std::string_view name): m_name { name } {}
	const std::string& getName() const { return m_name; } //  getter returns by const reference
};

// createEmployee() returns an Employee by value (which means the returned value is an rvalue)
Employee createEmployee(std::string_view name)
{
	Employee e { name };
	return e;
}

int main()
{
	// Case 1: okay: use returned reference to member of rvalue class object in same expression
	std::cout << createEmployee("Frank").getName() << '\n';

	// Case 2: bad: save returned reference to member of rvalue class object for use later
	const std::string& ref { createEmployee("Garbo").getName() }; // reference becomes dangling when return value of createEmployee() is destroyed
	std::cout << ref << '\n'; // undefined behavior

	return 0;
}
在案例 2 中，从
createEmployee("Garbo")
返回的右值对象在初始化
ref
后被销毁，导致
ref
引用了一个刚刚被销毁的数据成员。随后使用
ref
会导致未定义行为。
这带来了一个难题。
如果我们的
getName()
函数按值返回，当隐式对象是右值时这是安全的，但当隐式对象是左值时（这是最常见的情况）会进行昂贵且不必要的复制。
如果我们的
getName()
函数按 const 引用返回，这是高效的（因为没有复制
std::string
），但当隐式对象是右值时可能会被误用（导致未定义行为）。
由于成员函数通常在左值隐式对象上调用，因此传统选择是按 const 引用返回，并简单地避免在隐式对象是右值的情况下误用返回的引用。
引用限定符
上述挑战的根源在于我们只希望一个函数服务于两种不同的情况（一种是隐式对象是左值，另一种是隐式对象是右值）。对一种情况最优的方案对另一种情况来说并不理想。
为了帮助解决此类问题，C++11 引入了一个鲜为人知的功能，称为
引用限定符
，它允许我们根据成员函数是在左值还是右值隐式对象上调用来重载它。使用此功能，我们可以创建两个版本的
getName()
——一个用于隐式对象是左值的情况，一个用于隐式对象是右值的情况。
首先，让我们从
getName()
的非引用限定版本开始
const std::string& getName() const { return m_name; } // callable with both lvalue and rvalue implicit objects
要对该函数进行引用限定，我们为仅匹配左值隐式对象的重载添加
&
限定符，为仅匹配右值隐式对象的重载添加
&&
限定符
const std::string& getName() const &  { return m_name; } //  & qualifier overloads function to match only lvalue implicit objects, returns by reference
std::string        getName() const && { return m_name; } // && qualifier overloads function to match only rvalue implicit objects, returns by value
因为这些函数是不同的重载，它们可以有不同的返回类型！我们的左值限定重载按 const 引用返回，而我们的右值限定重载按值返回。
以下是上述的完整示例
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
	std::string m_name{};

public:
	Employee(std::string_view name): m_name { name } {}

	const std::string& getName() const &  { return m_name; } //  & qualifier overloads function to match only lvalue implicit objects
	std::string        getName() const && { return m_name; } // && qualifier overloads function to match only rvalue implicit objects
};

// createEmployee() returns an Employee by value (which means the returned value is an rvalue)
Employee createEmployee(std::string_view name)
{
	Employee e { name };
	return e;
}

int main()
{
	Employee joe { "Joe" };
	std::cout << joe.getName() << '\n'; // Joe is an lvalue, so this calls std::string& getName() & (returns a reference)
    
	std::cout << createEmployee("Frank").getName() << '\n'; // Frank is an rvalue, so this calls std::string getName() && (makes a copy)

	return 0;
}
这使我们能够在隐式对象是左值时执行高性能操作，并在隐式对象是右值时执行安全操作。
致进阶读者
当隐式对象是非 const 临时对象时，上述
getName()
的右值重载可能从性能角度来看次优。在这种情况下，隐式对象无论如何都会在表达式结束时销毁。因此，与其让右值 getter 返回成员的（可能昂贵的）副本，不如让它尝试移动成员（使用
std::move
）。
这可以通过为非 const 右值添加以下重载的 getter 来实现
// If the implicit object is a non-const rvalue, use std::move to try to move m_name
	std::string getName() && { return std::move(m_name); }
这可以与 const 右值 getter 共存，或者您可以只使用这个（因为 const 右值相当不常见）。
我们在
第 22.4 课——std::move
中介绍
std::move
。
关于引用限定成员函数的一些注意事项
首先，对于给定函数，非引用限定重载和引用限定重载不能共存。只能使用其中一个。
其次，类似于 const 左值引用可以绑定到右值，如果只存在 const 左值限定函数，它将接受左值或右值隐式对象。
第三，任何限定重载都可以被显式删除（使用
= delete
），这会阻止对该函数的调用。例如，删除右值限定版本会阻止该函数与右值隐式对象一起使用。
那么为什么我们不建议使用引用限定符呢？
虽然引用限定符很巧妙，但以这种方式使用它们有一些缺点。
为每个返回引用的 getter 添加右值重载会增加类的混乱，以缓解不常见且通过良好习惯容易避免的情况。
右值重载按值返回意味着我们必须支付复制（或移动）的成本，即使在我们可以安全地使用引用的情况下（例如，课程顶部示例中的案例 1）。
此外
大多数 C++ 开发人员不了解此功能（这可能导致使用中的错误或效率低下）。
标准库通常不使用此功能。
基于以上所有内容，我们不建议将引用限定符作为最佳实践。相反，我们建议始终立即使用访问函数的结果，而不是保存返回的引用以供以后使用。
下一课
15.x
第 15 章总结与测验
返回目录
上一课
15.9
友元类和友元成员函数