# 20.7 — Lambda 捕获

20.7 — Lambda 捕获
nascardriver
2020 年 1 月 3 日，太平洋标准时间上午 5:19
2024 年 12 月 4 日
捕获子句和值捕获
在上一课（
20.6 -- Lambda（匿名函数）简介
）中，我们介绍了这个例子
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  auto found{ std::find_if(arr.begin(), arr.end(),
                           [](std::string_view str)
                           {
                             return str.find("nut") != std::string_view::npos;
                           }) };

  if (found == arr.end())
  {
    std::cout << "No nuts\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
现在，让我们修改一下坚果示例，让用户选择要搜索的子字符串。这不像你想象的那么直观。
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>
#include <string>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  // Ask the user what to search for.
  std::cout << "search for: ";

  std::string search{};
  std::cin >> search;

  auto found{ std::find_if(arr.begin(), arr.end(), [](std::string_view str) {
    // Search for @search rather than "nut".
    return str.find(search) != std::string_view::npos; // Error: search not accessible in this scope
  }) };

  if (found == arr.end())
  {
    std::cout << "Not found\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
此代码无法编译。与嵌套块不同，在嵌套块中，外部块中可访问的任何标识符在嵌套块中都可访问，而 lambda 只能访问在 lambda 之外定义的某些类型的对象。这包括
具有静态（或线程局部）存储持续时间的对象（包括全局变量和静态局部变量）
constexpr 对象（显式或隐式）
由于
search
不满足这些要求，因此 lambda 无法看到它。
提示
Lambda 只能访问在 lambda 外部定义的某些类型的对象，包括那些具有静态存储持续时间（例如全局变量和静态局部变量）和 constexpr 对象。
要从 lambda 内部访问
search
，我们需要使用捕获子句。
捕获子句
捕获子句
用于（间接地）授予 lambda 访问其通常无法访问的周围作用域中的变量的权限。我们所需要做的就是将我们想要从 lambda 内部访问的实体列为捕获子句的一部分。在这种情况下，我们希望授予 lambda 访问变量
search
的值的权限，因此我们将其添加到捕获子句中
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>
#include <string>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  std::cout << "search for: ";

  std::string search{};
  std::cin >> search;

  // Capture @search                                vvvvvv
  auto found{ std::find_if(arr.begin(), arr.end(), [search](std::string_view str) {
    return str.find(search) != std::string_view::npos;
  }) };

  if (found == arr.end())
  {
    std::cout << "Not found\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
用户现在可以搜索我们数组中的元素。
输出
search for: nana
Found banana
那么捕获实际上是如何工作的？
虽然上面的示例中的 lambda 看起来是直接访问
main
的
search
变量的值，但事实并非如此。Lambda 可能看起来像嵌套块，但它们的工作方式略有不同（这种区别很重要）。
当执行 lambda 定义时，对于 lambda 捕获的每个变量，都会在该 lambda 内部创建该变量的克隆（具有相同的名称）。这些克隆变量在此点从同名外部作用域变量进行初始化。
因此，在上面的示例中，当创建 lambda 对象时，lambda 会获得其自己的名为
search
的克隆变量。此克隆的
search
具有与
main
的
search
相同的值，因此它的行为就像我们正在访问
main
的
search
，但我们不是。
虽然这些克隆变量具有相同的名称，但它们不一定具有与原始变量相同的类型。我们将在本课的后续部分中探讨这一点。
关键见解
lambda 的捕获变量是外部作用域变量的
副本
，而不是实际变量。
致进阶读者
虽然 lambda 看起来像函数，但它们实际上是可以像函数一样调用的对象（这些被称为
函数对象
——我们将在以后的课程中讨论如何从头开始创建自己的函数对象）。
当编译器遇到 lambda 定义时，它会为 lambda 创建一个自定义对象定义。每个捕获的变量都成为对象的数据成员。
在运行时，当遇到 lambda 定义时，会实例化 lambda 对象，并在此时初始化 lambda 的成员。
捕获默认情况下被视为 const
调用 lambda 时，会调用
operator()
。默认情况下，此
operator()
将捕获视为 const，这意味着 lambda 不允许修改这些捕获。
在以下示例中，我们捕获变量
ammo
并尝试递减它。
#include <iostream>

int main()
{
  int ammo{ 10 };

  // Define a lambda and store it in a variable called "shoot".
  auto shoot{
    [ammo]() {
      // Illegal, ammo cannot be modified.
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  // Call the lambda
  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
上面的代码无法编译，因为
ammo
在 lambda 内部被视为 const。
可变捕获
为了允许修改已捕获的变量，我们可以将 lambda 标记为
mutable
#include <iostream>

int main()
{
  int ammo{ 10 };

  auto shoot{
    [ammo]() mutable { // now mutable
      // We're allowed to modify ammo now
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  shoot();
  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
输出
Pew! 9 shot(s) left.
Pew! 8 shot(s) left.
10 shot(s) left
虽然现在可以编译，但仍然存在逻辑错误。发生了什么？当 lambda 被调用时，lambda 捕获了
ammo
的
副本
。当 lambda 将
ammo
从
10
递减到
9
再到
8
时，它递减的是它自己的副本，而不是
main()
中原始的
ammo
值。
请注意，
ammo
的值在对 lambda 的调用之间保持不变！
警告
因为捕获的变量是 lambda 对象的成员，所以它们的值在对 lambda 的多次调用中都是持久的！
按引用捕获
就像函数可以更改通过引用传递的参数的值一样，我们也可以通过引用捕获变量，以允许 lambda 影响参数的值。
要通过引用捕获变量，我们在捕获中的变量名前加上一个与号 (
&
)。与按值捕获的变量不同，按引用捕获的变量是非 const 的，除非它们捕获的变量是
const
。在通常首选通过引用将参数传递给函数时（例如，对于非基本类型），应优先使用按引用捕获而不是按值捕获。
这是上面用
ammo
按引用捕获的代码
#include <iostream>

int main()
{
  int ammo{ 10 };

  auto shoot{
    // We don't need mutable anymore
    [&ammo]() { // &ammo means ammo is captured by reference
      // Changes to ammo will affect main's ammo
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
这会产生预期的结果
Pew! 9 shot(s) left.
9 shot(s) left
现在，让我们使用引用捕获来计算
std::sort
排序数组时进行了多少次比较。
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Car
{
  std::string_view make{};
  std::string_view model{};
};

int main()
{
  std::array<Car, 3> cars{ { { "Volkswagen", "Golf" },
                             { "Toyota", "Corolla" },
                             { "Honda", "Civic" } } };

  int comparisons{ 0 };

  std::sort(cars.begin(), cars.end(),
    // Capture @comparisons by reference.
    [&comparisons](const auto& a, const auto& b) {
      // We captured comparisons by reference. We can modify it without "mutable".
      ++comparisons;

      // Sort the cars by their make.
      return a.make < b.make;
  });

  std::cout << "Comparisons: " << comparisons << '\n';

  for (const auto& car : cars)
  {
    std::cout << car.make << ' ' << car.model << '\n';
  }

  return 0;
}
可能的输出
Comparisons: 2
Honda Civic
Toyota Corolla
Volkswagen Golf
捕获多个变量
可以通过用逗号分隔来捕获多个变量。这可以包括按值捕获或按引用捕获的变量的混合
int health{ 33 };
int armor{ 100 };
std::vector<CEnemy> enemies{};

// Capture health and armor by value, and enemies by reference.
[health, armor, &enemies](){};
默认捕获
必须显式列出要捕获的变量可能会很麻烦。如果修改 lambda，您可能会忘记添加或删除捕获的变量。幸运的是，我们可以借助编译器的帮助来自动生成我们需要捕获的变量列表。
默认捕获
（也称为
捕获默认值
）捕获 lambda 中提到的所有变量。如果使用默认捕获，则 lambda 中未提及的变量不会被捕获。
要按值捕获所有使用的变量，请使用捕获值
=
。
要按引用捕获所有使用的变量，请使用捕获值
&
。
这是一个使用默认按值捕获的示例
#include <algorithm>
#include <array>
#include <iostream>

int main()
{
  std::array areas{ 100, 25, 121, 40, 56 };

  int width{};
  int height{};

  std::cout << "Enter width and height: ";
  std::cin >> width >> height;

  auto found{ std::find_if(areas.begin(), areas.end(),
                           [=](int knownArea) { // will default capture width and height by value
                             return width * height == knownArea; // because they're mentioned here
                           }) };

  if (found == areas.end())
  {
    std::cout << "I don't know this area :(\n";
  }
  else
  {
    std::cout << "Area found :)\n";
  }

  return 0;
}
默认捕获可以与普通捕获混合使用。我们可以按值捕获一些变量，按引用捕获另一些变量，但每个变量只能捕获一次。
int health{ 33 };
int armor{ 100 };
std::vector<CEnemy> enemies{};

// Capture health and armor by value, and enemies by reference.
[health, armor, &enemies](){};

// Capture enemies by reference and everything else by value.
[=, &enemies](){};

// Capture armor by value and everything else by reference.
[&, armor](){};

// Illegal, we already said we want to capture everything by reference.
[&, &armor](){};

// Illegal, we already said we want to capture everything by value.
[=, armor](){};

// Illegal, armor appears twice.
[armor, &health, &armor](){};

// Illegal, the default capture has to be the first element in the capture group.
[armor, &](){};
在 lambda-capture 中定义新变量
有时我们希望捕获一个略微修改的变量，或者声明一个只在 lambda 作用域中可见的新变量。我们可以通过在 lambda-capture 中定义变量而不指定其类型来做到这一点。
#include <array>
#include <iostream>
#include <algorithm>

int main()
{
  std::array areas{ 100, 25, 121, 40, 56 };

  int width{};
  int height{};

  std::cout << "Enter width and height: ";
  std::cin >> width >> height;

  // We store areas, but the user entered width and height.
  // We need to calculate the area before we can search for it.
  auto found{ std::find_if(areas.begin(), areas.end(),
                           // Declare a new variable that's visible only to the lambda.
                           // The type of userArea is automatically deduced to int.
                           [userArea{ width * height }](int knownArea) {
                             return userArea == knownArea;
                           }) };

  if (found == areas.end())
  {
    std::cout << "I don't know this area :(\n";
  }
  else
  {
    std::cout << "Area found :)\n";
  }

  return 0;
}
userArea
只会在 lambda 定义时计算一次。计算出的面积存储在 lambda 对象中，并且对于每次调用都是相同的。如果 lambda 是可变的并修改了在捕获中定义的变量，则原始值将被覆盖。
最佳实践
仅当变量的值很短且类型明确时才在捕获中初始化变量。否则，最好在 lambda 外部定义变量并捕获它。
悬空捕获变量
变量在定义 lambda 的点处被捕获。如果通过引用捕获的变量在 lambda 之前死亡，则 lambda 将保留一个悬空引用。
例如
#include <iostream>
#include <string>

// returns a lambda
auto makeWalrus(const std::string& name)
{
  // Capture name by reference and return the lambda.
  return [&]() {
    std::cout << "I am a walrus, my name is " << name << '\n'; // Undefined behavior
  };
}

int main()
{
  // Create a new walrus whose name is Roofus.
  // sayName is the lambda returned by makeWalrus.
  auto sayName{ makeWalrus("Roofus") };

  // Call the lambda function that makeWalrus returned.
  sayName();

  return 0;
}
对
makeWalrus()
的调用从字符串字面量
"Roofus"
创建一个临时的
std::string
。
makeWalrus()
中的 lambda 通过引用捕获临时字符串。临时字符串在包含对
makeWalrus()
的调用的完整表达式的末尾死亡，但 lambda
sayName
在此之后仍然引用它。因此，当我们调用
sayName
时，访问了悬空引用，导致未定义的行为。
请注意，如果
"Roofus"
按值传递给
makeWalrus()
，也会发生这种情况。参数
name
在
makeWalrus()
结束时死亡，并且 lambda 仍然保留一个悬空引用。
警告
当您通过引用捕获变量时要格外小心，尤其是使用默认引用捕获时。捕获的变量必须比 lambda 的生命周期长。
如果希望捕获的
name
在使用 lambda 时有效，则需要将其按值捕获（显式或使用默认按值捕获）。
可变 lambda 的意外副本
因为 lambda 是对象，所以它们可以被复制。在某些情况下，这可能会导致问题。考虑以下代码
#include <iostream>

int main()
{
  int i{ 0 };

  // Create a new lambda named count
  auto count{ [i]() mutable {
    std::cout << ++i << '\n';
  } };

  count(); // invoke count

  auto otherCount{ count }; // create a copy of count

  // invoke both count and the copy
  count();
  otherCount();

  return 0;
}
输出
1
2
2
代码不是打印 1、2、3，而是两次打印 2。当我们创建
otherCount
作为
count
的副本时，我们创建了
count
当前状态的副本。
count
的
i
是 1，所以
otherCount
的
i
也是 1。由于
otherCount
是
count
的副本，它们各自拥有自己的
i
。
现在让我们看一个稍微不那么明显的例子
#include <iostream>
#include <functional>

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // Increments and prints its local copy of @i.
    auto count{ [i]() mutable {
      std::cout << ++i << '\n';
    } };

    myInvoke(count);
    myInvoke(count);
    myInvoke(count);

    return 0;
}
输出
1
1
1
这以更模糊的形式展现了与前一个示例相同的问题。
当我们调用
myInvoke(count)
时，编译器会发现
count
（具有 lambda 类型）与引用参数类型 (
std::function<void()>
) 不匹配。它会将 lambda 转换为临时
std::function
，以便引用参数可以绑定到它，这将创建 lambda 的副本。因此，我们对
fn()
的调用实际上是在作为临时
std::function
的一部分存在的 lambda 副本上执行，而不是实际的 lambda。
如果我们需要传递一个可变 lambda，并且希望避免意外复制的可能性，有两种选择。一种选择是改用非捕获 lambda——在上述情况下，我们可以删除捕获并改用静态局部变量来跟踪我们的状态。但是静态局部变量可能难以跟踪并降低代码的可读性。一个更好的选择是首先防止创建 lambda 的副本。但是，由于我们无法影响
std::function
（或其他标准库函数或对象）的实现方式，我们该如何做到这一点？
一个选项（感谢读者 Dck）是立即将我们的 lambda 放入
std::function
中。这样，当我们调用
myInvoke()
时，引用参数
fn
可以绑定到我们的
std::function
，并且不会创建临时副本
#include <iostream>
#include <functional>

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // Increments and prints its local copy of @i.
    std::function count{ [i]() mutable { // lambda object stored in a std::function
      std::cout << ++i << '\n';
    } };

    myInvoke(count); // doesn't create copy when called
    myInvoke(count); // doesn't create copy when called
    myInvoke(count); // doesn't create copy when called

    return 0;
}
我们的输出现在符合预期
1
2
3
另一种解决方案是使用引用包装器。C++ 提供了一个方便的类型（作为 <functional> 头文件的一部分），称为
std::reference_wrapper
，它允许我们将普通类型视为引用。为了更方便，可以使用
std::ref()
函数创建
std::reference_wrapper
。通过将我们的 lambda 包装在
std::reference_wrapper
中，每当有人尝试复制我们的 lambda 时，他们都会复制
reference_wrapper
（避免复制 lambda）。
这是我们使用
std::ref
更新后的代码
#include <iostream>
#include <functional> // includes std::reference_wrapper and std::ref

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // Increments and prints its local copy of @i.
    auto count{ [i]() mutable {
      std::cout << ++i << '\n';
    } };

    // std::ref(count) ensures count is treated like a reference
    // thus, anything that tries to copy count will actually copy the reference
    // ensuring that only one count exists
    myInvoke(std::ref(count));
    myInvoke(std::ref(count));
    myInvoke(std::ref(count));

    return 0;
}
我们的输出现在符合预期
1
2
3
这种方法有趣之处在于，即使
myInvoke
按值（而不是按引用）接收
fn
，它也有效！
规则
标准库函数可能会复制函数对象（提醒：lambda 是函数对象）。如果您想提供带有可变捕获变量的 lambda，请使用
std::ref
通过引用传递它们。
最佳实践
尽量避免使用可变 lambda。不可变 lambda 更易于理解，并且不会出现上述问题以及在添加并行执行时出现的更危险的问题。
小测验时间
问题 #1
以下哪些变量可以在
main
中的 lambda 中使用而无需显式捕获它们？
int i{};
static int j{};

int getValue()
{
  return 0;
}

int main()
{
  int a{};
  constexpr int b{};
  static int c{};
  static constexpr int d{};
  const int e{};
  const int f{ getValue() };
  static const int g{}; 
  static const int h{ getValue() }; 

  [](){
    // Try to use the variables without explicitly capturing them.
    a;
    b;
    c;
    d;
    e;
    f;
    g;
    h;
    i;
    j;
  }();

  return 0;
}
显示答案
变量
无需显式捕获即可使用
a
否。
a
具有自动存储持续时间。
b
是。
b
可以在常量表达式中使用。
c
是。
c
具有静态存储持续时间。
d
是。
e
是。
e
可以在常量表达式中使用。
f
否。
f
的值取决于
getValue
，这可能需要程序运行。
g
是。
h
是。
h
具有静态存储持续时间。
i
是。
i
是一个全局变量。
j
是。
j
在整个文件中都可访问。
问题 #2
以下代码会打印什么？不要运行代码，在脑海中推导出来。
#include <iostream>
#include <string>

int main()
{
  std::string favoriteFruit{ "grapes" };

  auto printFavoriteFruit{
    [=]() {
      std::cout << "I like " << favoriteFruit << '\n';
    }
  };

  favoriteFruit = "bananas with chocolate";

  printFavoriteFruit();

  return 0;
}
显示答案
I like grapes
printFavoriteFruit
按值捕获了
favoriteFruit
。修改
main
的
favoriteFruit
不会影响 lambda 的
favoriteFruit
。
问题 #3
我们将编写一个关于平方数（通过整数自身相乘生成的数字 (1, 4, 9, 16, 25, ...)）的小游戏。
设置游戏
要求用户输入一个起始数字（例如 3）。
询问用户要生成多少个值。
选择一个介于 2 和 4 之间的随机整数。这是乘数。
生成用户指示的值数量。从起始数字开始，每个值都应该是下一个平方数，乘以乘数。
玩游戏
用户输入一个猜测。
如果猜测与任何生成的值匹配，则该值将从列表中删除，用户可以再次猜测。
如果用户猜出所有生成的值，他们就赢了。
如果猜测与生成的值不匹配，则用户输了，程序会告诉他们最接近的未猜测值。
以下是一些示例会话，可让您更好地了解游戏的运作方式
Start where? 4
How many? 5
I generated 5 square numbers. Do you know what each number is after multiplying it by 2?
> 32
Nice! 4 number(s) left.
> 72
Nice! 3 number(s) left.
> 50
Nice! 2 number(s) left.
> 126
126 is wrong! Try 128 next time.
从 4 开始，程序生成接下来的 5 个平方数：16、25、36、49、64
程序选择 2 作为随机乘数，因此每个平方数乘以 2：32、50、72、98、128
现在用户可以猜测了。
32 在列表中。
72 在列表中。
126 不在列表中，因此用户输了。最接近的未猜测数字是 128。
Start where? 1
How many? 3
I generated 3 square numbers. Do you know what each number is after multiplying it by 4?
> 4
Nice! 2 number(s) left.
> 16
Nice! 1 number(s) left.
> 36
Nice! You found all numbers, good job!
从 1 开始，程序生成接下来的 3 个平方数：1、4、9
程序选择 4 作为随机乘数，因此每个平方数乘以 4：4、16、36
用户正确猜出所有数字并赢得游戏。
提示
使用 Random.h（
8.15 -- 全局随机数 (Random.h)
）生成随机数。
使用
std::find()
（
18.3 -- 标准库算法简介
）在列表中搜索数字。
使用
std::vector::erase()
删除元素，例如
auto found{ std::find(/* ... */) };

// Make sure the element was found

myVector.erase(found);
使用
std::min_element
和 lambda 查找最接近用户猜测的数字。
std::min_element
的工作原理类似于上一测验中的
std::max_element
。
显示提示
提示：使用 <cmath> 中的
std::abs
计算两个数字之间的正差。
int distance{ std::abs(3 - 5) }; // 2
显示答案
#include <algorithm> // std::find, std::min_element
#include <cmath> // std::abs
#include <cstddef> // std::size_t
#include <iostream>
#include <vector>
#include "Random.h"

using Numbers = std::vector<int>;

namespace config
{
    constexpr int multiplierMin{ 2 };
    constexpr int multiplierMax{ 6 };
}

// Generates @count numbers starting at @start*@start and multiplies
// every square number by @multiplier.
Numbers generateNumbers(int start, int count, int multiplier)
{
    Numbers numbers(static_cast<std::size_t>(count));

    for (int index = 0; index < count; ++index)
    {
        std::size_t uindex{ static_cast<std::size_t>(index) };
        numbers[uindex] = (start + index) * (start + index) * multiplier;
    }

    return numbers;
}

// Asks the user to input starting number, then generates array of numbers
Numbers setupGame()
{
    int start{};
    std::cout << "Start where? ";
    std::cin >> start;

    int count{};
    std::cout << "How many? ";
    std::cin >> count;

    int multiplier{ Random::get(config::multiplierMin, config::multiplierMax) };

    std::cout << "I generated " << count
        << " square numbers. Do you know what each number is after multiplying it by "
        << multiplier << "?\n";

    return generateNumbers(start, count, multiplier);
}

// Returns the user's guess
int getUserGuess()
{
    int guess{};

    std::cout << "> ";
    std::cin >> guess;

    return guess;
}

// Searches for the value @guess in @numbers and removes it.
// Returns true if the value was found. False otherwise.
bool findAndRemove(Numbers& numbers, int guess)
{
    auto found{ std::find(numbers.begin(), numbers.end(), guess) };

    if (found == numbers.end())
        return false;

    numbers.erase(found);
    return true;
}

// Finds the value in @numbers that is closest to @guess.
int findClosestNumber(const Numbers& numbers, int guess)
{
    return *std::min_element(numbers.begin(), numbers.end(),
        [=](int a, int b)
        {
            return std::abs(a - guess) < std::abs(b - guess);
        });
}


// Called when the user guesses a number correctly.
void printSuccess(const Numbers& numbers)
{
    std::cout << "Nice! ";

    if (numbers.size() == 0)
    {
        std::cout << "You found all numbers, good job!\n";
    }
    else
    {
        std::cout << numbers.size() << " number(s) left.\n";
    }
}

// Called when the user guesses a number that is not in the numbers.
void printFailure(const Numbers& numbers, int guess)
{
    int closest{ findClosestNumber(numbers, guess) };

    std::cout << guess << " is wrong!\n";

    std::cout << "Try " << closest << " next time.\n";
}

int main()
{
    Numbers numbers{ setupGame() };

    while (true)
    {
        int guess{ getUserGuess() };

        if (!findAndRemove(numbers, guess))
        {
            printFailure(numbers, guess);
            break;
        }
        
        printSuccess(numbers);
        if (numbers.size() == 0)
            break;
    }

    return 0;
}
下一课
20.x
第 20 章总结和测验
返回目录
上一课
20.6
Lambda（匿名函数）简介