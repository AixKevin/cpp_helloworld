# 23.3 — 聚合

23.3 — 聚合
Alex
2007 年 12 月 7 日，下午 12:43 PST
2024 年 4 月 16 日
在上一课
23.2 -- 组合
中，我们提到对象组合是将简单对象组合成复杂对象的过程。我们还讨论了一种对象组合类型，称为组合。在组合关系中，整体对象负责部分的生命周期。
在本课中，我们将探讨对象组合的另一种子类型，称为聚合。
聚合
要符合
聚合
的条件，整体对象及其部分必须具有以下关系：
部分（成员）是对象（类）的一部分
部分（成员）可以（如果需要）同时属于多个对象（类）
部分（成员）的生命周期
不
由对象（类）管理
部分（成员）不知道对象（类）的存在
像组合一样，聚合仍然是一种部分-整体关系，其中部分包含在整体中，并且它是一种单向关系。然而，与组合不同的是，部分可以同时属于多个对象，并且整体对象不负责部分的生命周期。当创建聚合时，聚合不负责创建部分。当聚合被销毁时，聚合不负责销毁部分。
例如，考虑一个人和他们的家庭住址之间的关系。在这个例子中，为了简单起见，我们假设每个人都有一个地址。然而，这个地址可以同时属于多个人：例如，你和你的室友或重要他人。但是，这个地址不由这个人管理——这个地址可能在人到来之前就已经存在，并且在人离开之后仍然存在。此外，一个人知道他们住在哪个地址，但地址不知道有哪些人住在那里。因此，这是一种聚合关系。
或者，考虑一辆汽车和一台发动机。汽车发动机是汽车的一部分。尽管发动机属于汽车，它也可以属于其他事物，比如汽车的所有者。汽车不负责发动机的创建或销毁。虽然汽车知道它有一台发动机（它必须有才能行驶），但发动机不知道它是汽车的一部分。
在对物理对象进行建模时，“销毁”这个词的使用可能有点棘手。有人可能会争辩说：“如果一颗流星从天而降，砸毁了汽车，汽车的零部件不也会被销毁吗？” 是的，当然。但那是流星的错。重要的是，汽车不负责销毁其零部件（但外部力量可能会）。
我们可以说聚合模型“拥有”关系（一个部门有教师，一辆汽车有发动机）。
与组合类似，聚合的部件可以是单一的或多个的。
实现聚合
因为聚合与组合相似，它们都是部分-整体关系，所以它们的实现几乎相同，它们之间的区别主要是语义上的。在组合中，我们通常使用普通成员变量（或由组合类处理分配和解除分配过程的指针）将部分添加到组合中。
在聚合中，我们也以成员变量的形式添加部分。然而，这些成员变量通常是指向在类范围之外创建的对象的引用或指针。因此，聚合通常要么将要指向的对象作为构造函数参数，要么它开始时为空，子对象稍后通过访问函数或运算符添加。
因为这些部分存在于类的作用域之外，所以当类被销毁时，指针或引用成员变量将被销毁（但不会被删除）。因此，部分本身仍将存在。
让我们更详细地看看教师和系部的例子。在这个例子中，我们将做一些简化：首先，系部只容纳一名教师。其次，教师不会知道他们属于哪个系部。
#include <iostream>
#include <string>
#include <string_view>

class Teacher
{
private:
  std::string m_name{};

public:
  Teacher(std::string_view name)
      : m_name{ name }
  {
  }

  const std::string& getName() const { return m_name; }
};

class Department
{
private:
  const Teacher& m_teacher; // This dept holds only one teacher for simplicity, but it could hold many teachers

public:
  Department(const Teacher& teacher)
      : m_teacher{ teacher }
  {
  }
};

int main()
{
  // Create a teacher outside the scope of the Department
  Teacher bob{ "Bob" }; // create a teacher

  {
    // Create a department and use the constructor parameter to pass
    // the teacher to it.
    Department department{ bob };

  } // department goes out of scope here and is destroyed

  // bob still exists here, but the department doesn't

  std::cout << bob.getName() << " still exists!\n";

  return 0;
}
在这种情况下，
bob
独立于
department
创建，然后作为参数传递给
department
的构造函数。当
department
被销毁时，
m_teacher
引用被销毁，但教师本身并没有被销毁，所以它仍然存在，直到稍后在
main()
中被独立销毁。
为您的建模选择正确的关系
虽然在上面的例子中，教师不知道他们为哪个部门工作可能看起来有点傻，但在特定程序的上下文中这可能完全没问题。当你确定要实现哪种关系时，实现满足你需求的最简单的关系，而不是在现实生活中看起来最适合的关系。
例如，如果你正在编写一个汽车修理厂模拟器，你可能希望将汽车和发动机实现为聚合，这样发动机就可以被拆卸并放在某个架子上以备后用。然而，如果你正在编写一个赛车模拟器，你可能希望将汽车和发动机实现为组合，因为在这种情况下，发动机永远不会存在于汽车之外。
最佳实践
实现满足程序需求的最简单关系类型，而不是在现实生活中看起来正确的关系类型。
组合与聚合总结
组合
通常使用普通成员变量
如果类本身处理对象分配/解除分配，则可以使用指针成员
负责部分的创建/销毁
聚合
通常使用指向或引用聚合类范围之外对象的指针或引用成员
不负责创建/销毁部分
值得注意的是，组合和聚合的概念可以在同一个类中自由混合。编写一个类，它负责某些部分的创建/销毁，但不负责其他部分，这是完全可能的。例如，我们的 Department 类可以有一个名称和一个 Teacher。名称很可能通过组合添加到 Department 中，并与 Department 一起创建和销毁。另一方面，Teacher 将通过聚合添加到 Department 中，并独立创建/销毁。
虽然聚合非常有用，但它们也可能更危险，因为聚合不处理其部分的解除分配。解除分配留给外部方进行。如果外部方不再拥有指向已放弃部分的指针或引用，或者它只是忘记进行清理（假设类会处理），那么就会发生内存泄漏。
因此，应优先使用组合而非聚合。
一些警告/勘误
由于各种历史和上下文原因，与组合不同，聚合的定义不精确——所以您可能会看到其他参考资料以与我们不同的方式定义它。这没关系，请注意即可。
最后一点：在
13.7 -- 结构体、成员和成员选择简介
一课中，我们将聚合数据类型（例如结构体和类）定义为将多个变量组合在一起的数据类型。您还可能会在 C++ 学习过程中遇到以下术语
聚合类
它被定义为没有提供构造函数、析构函数或重载赋值，所有成员都是公共的，并且不使用继承的结构体或类——本质上是一个普通的旧数据结构体。尽管名称相似，但“聚合”和“聚合类”是不同的，不应混淆。
std::reference_wrapper
在上面的
Department
/
Teacher
示例中，我们在
Department
中使用了一个引用来存储
Teacher
。如果只有一个
Teacher
，这很好用，但是如果一个 Department 有多个 Teacher 怎么办？我们希望将这些 Teacher 存储在某种列表中（例如
std::vector
），但是固定大小的数组和各种标准库列表不能持有引用（因为列表元素必须是可赋值的，而引用不能被重新赋值）。
std::vector<const Teacher&> m_teachers{}; // Illegal
我们可以使用指针而不是引用，但这会增加存储或传递空指针的可能性。在
Department
/
Teacher
示例中，我们不希望允许空指针。为了解决这个问题，有
std::reference_wrapper
。
本质上，
std::reference_wrapper
是一个类，它表现得像一个引用，但也允许赋值和复制，因此它与
std::vector
等列表兼容。
好消息是，您无需真正理解它的工作原理即可使用它。您只需要知道三件事：
std::reference_wrapper
位于 <functional> 头文件中。
当您创建
std::reference_wrapper
封装的对象时，该对象不能是匿名对象（因为匿名对象具有表达式作用域，这会导致引用悬空）。
当您想从
std::reference_wrapper
中取回对象时，请使用
get()
成员函数。
这是一个在
std::vector
中使用
std::reference_wrapper
的示例
#include <functional> // std::reference_wrapper
#include <iostream>
#include <vector>
#include <string>

int main()
{
  std::string tom{ "Tom" };
  std::string berta{ "Berta" };

  std::vector<std::reference_wrapper<std::string>> names{ tom, berta }; // these strings are stored by reference, not value

  std::string jim{ "Jim" };

  names.emplace_back(jim);

  for (auto name : names)
  {
    // Use the get() member function to get the referenced string.
    name.get() += " Beam";
  }

  std::cout << jim << '\n'; // prints Jim Beam

  return 0;
}
要创建 const 引用向量，我们必须在
std::string
之前添加 const，如下所示：
// Vector of const references to std::string
std::vector<std::reference_wrapper<const std::string>> names{ tom, berta };
小测验时间
问题 #1
您更倾向于将以下各项实现为组合还是聚合？
a) 一个有颜色的球
b) 一个雇佣多人的雇主
c) 大学里的各个系
d) 你的年龄
e) 一袋弹珠
显示答案
a) 组合：颜色是球的固有属性。
b) 聚合：雇主开始时没有员工，而且它破产时也希望不会销毁所有员工。
c) 组合：没有大学，系无法存在。
d) 组合：你的年龄是你的固有属性。
e) 聚合：袋子和里面的弹珠独立存在。
问题 #2
更新
Department
/
Teacher
示例，使其能够处理多个教师。以下代码应能执行：
#include <iostream>

// ...

int main()
{
  // Create a teacher outside the scope of the Department
  Teacher t1{ "Bob" };
  Teacher t2{ "Frank" };
  Teacher t3{ "Beth" };

  {
    // Create a department and add some Teachers to it
    Department department{}; // create an empty Department

    department.add(t1);
    department.add(t2);
    department.add(t3);

    std::cout << department;

  } // department goes out of scope here and is destroyed

  std::cout << t1.getName() << " still exists!\n";
  std::cout << t2.getName() << " still exists!\n";
  std::cout << t3.getName() << " still exists!\n";

  return 0;
}
这应该打印
Department: Bob Frank Beth
Bob still exists!
Frank still exists!
Beth still exists!
显示提示
提示：将教师存储在
std::vector
中
std::vector<std::reference_wrapper<const Teacher>> m_teachers{};
显示答案
#include <functional> // std::reference_wrapper
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Teacher
{
private:
  std::string m_name{};

public:
  Teacher(std::string_view name)
      : m_name{ name }
  {
  }

  const std::string& getName() const { return m_name; }
};

class Department
{
private:
  std::vector<std::reference_wrapper<const Teacher>> m_teachers{};

public:
  Department() = default;

  // Pass by regular reference. The user of the Department class shouldn't care
  // about how it's implemented.
  void add(const Teacher& teacher)
  {
    m_teachers.emplace_back(teacher);
  }

  friend std::ostream& operator<<(std::ostream& out, const Department& department)
  {
    out << "Department: ";

    for (const auto& teacher : department.m_teachers)
    {
      out << teacher.get().getName() << ' ';
    }

    out << '\n';

    return out;
  }
};

int main()
{
  // Create a teacher outside the scope of the Department
  Teacher t1{ "Bob" };
  Teacher t2{ "Frank" };
  Teacher t3{ "Beth" };

  {
    // Create a department and add some Teachers to it
    Department department{}; // create an empty Department

    department.add(t1);
    department.add(t2);
    department.add(t3);

    std::cout << department;

  } // department goes out of scope here and is destroyed

  std::cout << t1.getName() << " still exists!\n";
  std::cout << t2.getName() << " still exists!\n";
  std::cout << t3.getName() << " still exists!\n";

  return 0;
}
下一课
23.4
关联
返回目录
上一课
23.2
组合