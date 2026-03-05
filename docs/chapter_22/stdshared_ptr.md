# 22.6 — std::shared_ptr

22.6 — std::shared_ptr
Alex
2017 年 3 月 16 日，太平洋夏令时下午 4:04
2024 年 6 月 2 日
与旨在单独拥有和管理资源的 std::unique_ptr 不同，std::shared_ptr 用于解决需要多个智能指针共同拥有资源的情况。
这意味着可以有多个 std::shared_ptr 指向同一个资源。在内部，std::shared_ptr 会跟踪有多少个 std::shared_ptr 共享该资源。只要至少有一个 std::shared_ptr 指向该资源，即使单个 std::shared_ptr 被销毁，该资源也不会被释放。一旦管理该资源的最后一个 std::shared_ptr 超出作用域（或被重新分配指向其他对象），该资源就会被释放。
与 std::unique_ptr 一样，std::shared_ptr 位于 `
` 头文件中。
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
	// allocate a Resource object and have it owned by std::shared_ptr
	Resource* res { new Resource };
	std::shared_ptr<Resource> ptr1{ res };
	{
		std::shared_ptr<Resource> ptr2 { ptr1 }; // make another std::shared_ptr pointing to the same thing

		std::cout << "Killing one shared pointer\n";
	} // ptr2 goes out of scope here, but nothing happens

	std::cout << "Killing another shared pointer\n";

	return 0;
} // ptr1 goes out of scope here, and the allocated Resource is destroyed
这会打印
Resource acquired
Killing one shared pointer
Killing another shared pointer
Resource destroyed
在上面的代码中，我们创建了一个动态的 Resource 对象，并设置一个名为 ptr1 的 std::shared_ptr 来管理它。在嵌套块中，我们使用复制构造函数创建第二个 std::shared_ptr (ptr2)，它指向相同的 Resource。当 ptr2 超出作用域时，Resource 不会被释放，因为 ptr1 仍然指向 Resource。当 ptr1 超出作用域时，ptr1 注意到没有更多的 std::shared_ptr 管理 Resource，因此它会释放 Resource。
请注意，我们从第一个共享指针创建了第二个共享指针。这很重要。考虑以下类似的程序
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
	Resource* res { new Resource };
	std::shared_ptr<Resource> ptr1 { res };
	{
		std::shared_ptr<Resource> ptr2 { res }; // create ptr2 directly from res (instead of ptr1)

		std::cout << "Killing one shared pointer\n";
	} // ptr2 goes out of scope here, and the allocated Resource is destroyed

	std::cout << "Killing another shared pointer\n";

	return 0;
} // ptr1 goes out of scope here, and the allocated Resource is destroyed again
这个程序打印
Resource acquired
Killing one shared pointer
Resource destroyed
Killing another shared pointer
Resource destroyed
然后崩溃（至少在作者的机器上）。
这里的区别在于我们独立创建了两个 std::shared_ptr。因此，尽管它们都指向同一个 Resource，但它们彼此不知道。当 ptr2 超出作用域时，它认为自己是 Resource 的唯一所有者，并释放了它。当 ptr1 稍后超出作用域时，它也这么认为，并尝试再次删除 Resource。然后就出问题了。
幸运的是，这很容易避免：如果需要多个 std::shared_ptr 指向给定资源，请复制一个现有的 std::shared_ptr。
最佳实践
如果需要多个 std::shared_ptr 指向同一个资源，请始终复制一个现有的 std::shared_ptr。
就像 std::unique_ptr 一样，std::shared_ptr 可以是空指针，因此在使用它之前请检查以确保其有效。
std::make_shared
就像 std::make_unique() 可以在 C++14 中用于创建 std::unique_ptr 一样，std::make_shared() 可以（也应该）用于创建 std::shared_ptr。std::make_shared() 在 C++11 中可用。
这是我们使用 std::make_shared() 的原始示例
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
	// allocate a Resource object and have it owned by std::shared_ptr
	auto ptr1 { std::make_shared<Resource>() };
	{
		auto ptr2 { ptr1 }; // create ptr2 using copy of ptr1

		std::cout << "Killing one shared pointer\n";
	} // ptr2 goes out of scope here, but nothing happens

	std::cout << "Killing another shared pointer\n";

	return 0;
} // ptr1 goes out of scope here, and the allocated Resource is destroyed
使用 std::make_shared() 的原因与 std::make_unique() 相同——std::make_shared() 更简单、更安全（使用此方法无法创建两个独立的 std::shared_ptr 指向同一个资源但彼此不知道）。但是，std::make_shared() 的性能也比不使用它更好。其原因在于 std::shared_ptr 跟踪有多少指针指向给定资源的方式。
深入探讨 std::shared_ptr
与内部使用单个指针的 std::unique_ptr 不同，std::shared_ptr 内部使用两个指针。一个指针指向被管理的资源。另一个指针指向“控制块”，它是一个动态分配的对象，用于跟踪大量信息，包括有多少个 std::shared_ptr 指向该资源。当通过 std::shared_ptr 构造函数创建 std::shared_ptr 时，被管理对象（通常是传入的）和控制块（由构造函数创建）的内存是单独分配的。但是，在使用 std::make_shared() 时，这可以优化为单个内存分配，从而带来更好的性能。
这也解释了为什么独立创建两个指向同一资源的 std::shared_ptr 会给我们带来麻烦。每个 std::shared_ptr 都会有一个指针指向该资源。但是，每个 std::shared_ptr 都会独立分配自己的控制块，这会表明它是拥有该资源的唯一指针。因此，当该 std::shared_ptr 超出作用域时，它将释放该资源，而没有意识到还有其他 std::shared_ptr 也在尝试管理该资源。
然而，当使用复制赋值克隆 std::shared_ptr 时，控制块中的数据可以被适当更新，以表明现在有额外的 std::shared_ptr 共同管理该资源。
共享指针可以从唯一指针创建
std::unique_ptr 可以通过接受 std::unique_ptr 右值的特殊 std::shared_ptr 构造函数转换为 std::shared_ptr。std::unique_ptr 的内容将被移动到 std::shared_ptr。
然而，std::shared_ptr 不能安全地转换为 std::unique_ptr。这意味着，如果您正在创建一个将返回智能指针的函数，最好返回 std::unique_ptr，并在适当的时候将其赋值给 std::shared_ptr。
std::shared_ptr 的危险
std::shared_ptr 存在一些与 std::unique_ptr 相同的挑战——如果 std::shared_ptr 没有正确处理（要么因为它被动态分配但从未删除，要么它是被动态分配但从未删除的对象的一部分），那么它所管理的资源也不会被释放。对于 std::unique_ptr，您只需担心一个智能指针是否被正确处理。对于 std::shared_ptr，您必须担心所有这些指针。如果管理资源的任何 std::shared_ptr 没有被正确销毁，资源将无法正确释放。
std::shared_ptr 和数组
在 C++17 及更早版本中，std::shared_ptr 不支持管理数组，不应用于管理 C 风格数组。自 C++20 起，std::shared_ptr 支持数组。
总结
std::shared_ptr 专为需要多个智能指针共同管理同一资源的情况而设计。当管理该资源的最后一个 std::shared_ptr 被销毁时，该资源将被释放。
下一课
22.7
std::shared_ptr 和 std::weak_ptr 中的循环依赖问题
返回目录
上一课
22.5
std::unique_ptr