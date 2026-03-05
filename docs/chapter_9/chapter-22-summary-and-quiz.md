# 22.x — 第 22 章 总结和测验

22.x — 第 22 章 总结和测验
Alex
2017 年 5 月 3 日，太平洋夏令时上午 11:28
2025 年 1 月 6 日
智能指针类是一种组合类，旨在管理动态分配的内存，并确保当智能指针对象超出作用域时内存被删除。
复制语义允许我们的类被复制。这主要通过复制构造函数和复制赋值运算符完成。
移动语义意味着类将转移对象的所有权，而不是进行复制。这主要通过移动构造函数和移动赋值运算符完成。
std::auto_ptr 已弃用，应避免使用。
右值引用是一种旨在用右值初始化的引用。右值引用使用双 & 符号创建。编写接受右值引用参数的函数是可以的，但几乎不应返回右值引用。
如果我们在构造对象或进行赋值时，参数是左值，我们唯一合理能做的就是复制左值。我们不能假设修改左值是安全的，因为它可能在程序后面再次使用。如果我们有表达式“a = b”，我们不会合理地期望 b 会以任何方式改变。
然而，如果我们在构造对象或进行赋值时，参数是右值，那么我们知道该右值只是某种临时对象。与其复制它（这可能很昂贵），我们可以简单地将其资源（这很便宜）转移到我们正在构造或赋值的对象。这样做是安全的，因为临时对象无论如何都会在表达式结束时被销毁，所以我们知道它将永远不会再被使用！
您可以使用 delete 关键字通过删除复制构造函数和复制赋值运算符来禁用您创建的类的复制语义。
std::move 允许您将左值视为右值。当我们需要对左值调用移动语义而不是复制语义时，这很有用。
std::unique_ptr 是您可能应该使用的智能指针类。它管理一个单一的不可共享资源。std::make_unique() (在 C++14 中) 应优先用于创建新的 std::unique_ptr。std::unique_ptr 禁用复制语义。
std::shared_ptr 是当您需要多个对象访问同一资源时使用的智能指针类。在管理它的最后一个 std::shared_ptr 被销毁之前，资源不会被销毁。std::make_shared() 应优先用于创建新的 std::shared_ptr。对于 std::shared_ptr，应使用复制语义来创建指向同一对象的其他 std::shared_ptr。
std::weak_ptr 是当您需要一个或多个对象能够查看和访问由 std::shared_ptr 管理的资源时使用的智能指针类，但与 std::shared_ptr 不同，std::weak_ptr 在确定资源是否应被销毁时不会被考虑。
小测验时间
解释何时应使用以下类型的指针。
1a) std::unique_ptr
显示答案
当您希望智能指针管理一个不会被共享的动态对象时，应使用 std::unique_ptr。
1b) std::shared_ptr
显示答案
当您希望智能指针管理一个可能被共享的动态对象时，应使用 std::shared_ptr。在所有持有该对象的 std::shared_ptr 被销毁之前，该对象不会被释放。
1c) std::weak_ptr
显示答案
当您希望访问由 std::shared_ptr 管理的对象，但又不想将 std::shared_ptr 的生命周期与 std::weak_ptr 的生命周期绑定时，应使用 std::weak_ptr。
1d) std::auto_ptr
显示答案
std::auto_ptr 已弃用，并在 C++17 中被移除。不应使用它。
解释为什么移动语义以右值为中心。
显示答案
因为右值是临时的，我们知道它们在使用后会被销毁。当按值传递或返回右值时，复制然后再销毁原始值是浪费的。相反，我们可以简单地移动（窃取）右值的资源，这通常更有效率。
以下代码有什么问题？更新程序以符合最佳实践。
3a)
#include <iostream>
#include <memory> // for std::shared_ptr
 
class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};
 
int main()
{
	auto* res{ new Resource{} };
	std::shared_ptr<Resource> ptr1{ res };
	std::shared_ptr<Resource> ptr2{ res };

	return 0;
}
显示答案
ptr2
是从
res
而不是从
ptr1
创建的。这意味着您现在有两个
std::shared_ptr
独立地尝试管理
Resource
（它们彼此不知道）。当其中一个超出作用域时，另一个将留下一个悬空指针。
ptr2
应改为使用
ptr1
初始化，而不是从
res
初始化。这将允许
ptr1
和
ptr2
共享
res
的所有权。应使用
std::make_shared()
而不是手动动态分配。
#include <iostream>
#include <memory> // for std::shared_ptr
 
class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};
 
int main()
{
	auto ptr1{ std::make_shared<Resource>() };
	auto ptr2{ ptr1 };

	return 0;
}
下一课
23.1
对象关系
返回目录
上一课
22.7
std::shared_ptr 和 std::weak_ptr 的循环依赖问题