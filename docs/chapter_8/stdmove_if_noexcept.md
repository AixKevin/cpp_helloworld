# 27.10 — std::move_if_noexcept

27.10 — std::move_if_noexcept
Alex
2020 年 8 月 16 日，太平洋夏令时下午 3:28
2024 年 8 月 15 日
（感谢读者 Koe 提供了本课程的初稿！）
在
22.4 — std::move
课程中，我们介绍了
std::move
，它将其左值参数转换为右值，以便我们可以调用移动语义。在
27.9 — 异常规范与 noexcept
课程中，我们介绍了
noexcept
异常说明符和运算符。本课程基于这两个概念进行构建。
我们还介绍了“强异常保证”，它保证如果一个函数被异常中断，不会发生内存泄漏，并且程序状态不会改变。特别是，所有构造函数都应遵守强异常保证，以便在对象构造失败时，程序的其余部分不会处于更改状态。
移动构造函数的异常问题
考虑我们正在复制某个对象的情况，并且复制由于某种原因失败（例如机器内存不足）。在这种情况下，被复制的对象不会受到任何损害，因为源对象不需要修改来创建副本。我们可以丢弃失败的副本，然后继续。遵守了“强异常保证”。
现在考虑我们正在移动一个对象的情况。移动操作将给定资源的所有权从源对象转移到目标对象。如果移动操作在所有权转移发生后被异常中断，则我们的源对象将处于修改状态。如果源对象是临时对象并且无论如何都将在移动后被丢弃，这不是问题——但对于非临时对象，我们现在已经损坏了源对象。为了遵守“强异常保证”，我们需要将资源移回源对象，但如果第一次移动失败，也不能保证移回会成功。
我们如何为移动构造函数提供“强异常保证”？在移动构造函数的主体中避免抛出异常很简单，但移动构造函数可能会调用其他“可能抛出”的构造函数。以
std::pair
的移动构造函数为例，它必须尝试将源对中的每个子对象移动到新的对对象中。
// Example move constructor definition for std::pair
// Take in an 'old' pair, and then move construct the new pair's 'first' and 'second' subobjects from the 'old' ones
template <typename T1, typename T2>
pair<T1,T2>::pair(pair&& old)
  : first(std::move(old.first)),
    second(std::move(old.second))
{}
现在让我们使用两个类，
MoveClass
和
CopyClass
，我们将它们“配对”在一起以演示移动构造函数的“强异常保证”问题。
#include <iostream>
#include <utility> // For std::pair, std::make_pair, std::move, std::move_if_noexcept
#include <stdexcept> // std::runtime_error

class MoveClass
{
private:
  int* m_resource{};

public:
  MoveClass() = default;

  MoveClass(int resource)
    : m_resource{ new int{ resource } }
  {}

  // Copy constructor
  MoveClass(const MoveClass& that)
  {
    // deep copy
    if (that.m_resource != nullptr)
    {
      m_resource = new int{ *that.m_resource };
    }
  }

  // Move constructor
  MoveClass(MoveClass&& that) noexcept
    : m_resource{ that.m_resource }
  {
    that.m_resource = nullptr;
  }

  ~MoveClass()
  {
    std::cout << "destroying " << *this << '\n';

    delete m_resource;
  }

  friend std::ostream& operator<<(std::ostream& out, const MoveClass& moveClass)
  {
    out << "MoveClass(";

    if (moveClass.m_resource == nullptr)
    {
      out << "empty";
    }
    else
    {
      out << *moveClass.m_resource;
    }

    out << ')';
    
    return out;
  }
};


class CopyClass
{
public:
  bool m_throw{};

  CopyClass() = default;

  // Copy constructor throws an exception when copying from
  // a CopyClass object where its m_throw is 'true'
  CopyClass(const CopyClass& that)
    : m_throw{ that.m_throw }
  {
    if (m_throw)
    {
      throw std::runtime_error{ "abort!" };
    }
  }
};

int main()
{
  // We can make a std::pair without any problems:
  std::pair my_pair{ MoveClass{ 13 }, CopyClass{} };

  std::cout << "my_pair.first: " << my_pair.first << '\n';

  // But the problem arises when we try to move that pair into another pair.
  try
  {
    my_pair.second.m_throw = true; // To trigger copy constructor exception

    // The following line will throw an exception
    std::pair moved_pair{ std::move(my_pair) }; // We'll comment out this line later
    // std::pair moved_pair{ std::move_if_noexcept(my_pair) }; // We'll uncomment this later

    std::cout << "moved pair exists\n"; // Never prints
  }
  catch (const std::exception& ex)
  {
      std::cerr << "Error found: " << ex.what() << '\n';
  }

  std::cout << "my_pair.first: " << my_pair.first << '\n';

  return 0;
}
上面的程序打印
destroying MoveClass(empty)
my_pair.first: MoveClass(13)
destroying MoveClass(13)
Error found: abort!
my_pair.first: MoveClass(empty)
destroying MoveClass(empty)
让我们看看发生了什么。第一行打印显示，用于初始化
my_pair
的临时
MoveClass
对象在
my_pair
实例化语句执行后立即被销毁。它是“空的”，因为
my_pair
中的
MoveClass
子对象是从它移动构造的，下一行显示
my_pair.first
包含值为
13
的
MoveClass
对象，证明了这一点。
第三行变得有趣。我们通过复制构造其
CopyClass
子对象（它没有移动构造函数）创建了
moved_pair
，但由于我们更改了布尔标志，该复制构造抛出了异常。
moved_pair
的构造被异常中止，其已构造的成员被销毁。在这种情况下，
MoveClass
成员被销毁，打印出
destroying MoveClass(13) variable
。接下来我们看到
main()
打印的
Error found: abort!
消息。
当我们再次尝试打印
my_pair.first
时，它显示
MoveClass
成员为空。由于
moved_pair
是用
std::move
初始化的，所以
MoveClass
成员（它有一个移动构造函数）被移动构造，并且
my_pair.first
被置空。
最后，
my_pair
在 main() 结束时被销毁。
总结上述结果：
std::pair
的移动构造函数使用了
CopyClass
的抛出复制构造函数。此复制构造函数抛出了异常，导致
moved_pair
的创建中止，并且
my_pair.first
被永久损坏。“强异常保证”没有得到维护。
std::move_if_noexcept 来拯救
请注意，如果
std::pair
尝试进行复制而不是移动，则可以避免上述问题。在这种情况下，
moved_pair
将无法构造，但
my_pair
不会被更改。
但复制而不是移动会带来性能成本，我们不希望为所有对象支付此成本——理想情况下，如果可以安全地执行，我们希望进行移动，否则进行复制。
幸运的是，C++ 有两种机制，当它们结合使用时，可以让我们做到这一点。首先，因为
noexcept
函数是无抛出/无失败的，所以它们隐式满足“强异常保证”的标准。因此，
noexcept
移动构造函数保证成功。
其次，我们可以使用标准库函数
std::move_if_noexcept()
来确定是执行移动还是复制。
std::move_if_noexcept
是
std::move
的对应物，使用方式相同。
如果编译器可以判断传递给
std::move_if_noexcept
的对象在移动构造时不会抛出异常（或者如果该对象是仅移动且没有复制构造函数），则
std::move_if_noexcept
将与
std::move()
表现相同（并返回转换为右值的对象）。否则，
std::move_if_noexcept
将返回对象的普通左值引用。
关键见解
如果对象具有
noexcept
移动构造函数，则
std::move_if_noexcept
将返回一个可移动的右值，否则将返回一个可复制的左值。我们可以将
noexcept
说明符与
std::move_if_noexcept
结合使用，仅在存在强异常保证时使用移动语义（否则使用复制语义）。
让我们按如下方式更新上一个示例中的代码
//std::pair moved_pair{std::move(my_pair)}; // comment out this line now
std::pair moved_pair{std::move_if_noexcept(my_pair)}; // and uncomment this line
再次运行程序打印
destroying MoveClass(empty)
my_pair.first: MoveClass(13)
destroying MoveClass(13)
Error found: abort!
my_pair.first: MoveClass(13)
destroying MoveClass(13)
如您所见，在抛出异常后，子对象
my_pair.first
仍然指向值
13
。
std::pair
的移动构造函数不是
noexcept
（从 C++20 开始），因此
std::move_if_noexcept
将
my_pair
作为左值引用返回。这导致
moved_pair
通过复制构造函数（而不是移动构造函数）创建。复制构造函数可以安全地抛出，因为它不修改源对象。
标准库经常使用
std::move_if_noexcept
来优化
noexcept
函数。例如，如果元素类型具有
noexcept
移动构造函数，则
std::vector::resize
将使用移动语义，否则使用复制语义。这意味着
std::vector
通常在使用具有
noexcept
移动构造函数的对象时操作更快。
警告
如果某个类型既有潜在抛出移动语义又删除了复制语义（复制构造函数和复制赋值运算符不可用），则
std::move_if_noexcept
将放弃强保证并调用移动语义。这种对强保证的条件放弃在标准库容器类中无处不在，因为它们经常使用
std::move_if_noexcept
。
下一课
27.x
第 27 章总结与测验
返回目录
上一课
27.9
异常规范与 noexcept