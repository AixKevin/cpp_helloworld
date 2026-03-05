# 20.6 — Lambda（匿名函数）简介

20.6 — Lambda（匿名函数）简介
nascardriver
2020 年 1 月 3 日，上午 5:19 PST
2024 年 6 月 14 日
考虑我们在课程
18.3 — 标准库算法简介
中介绍的这段代码片段
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

// Our function will return true if the element matches
bool containsNut(std::string_view str)
{
    // std::string_view::find returns std::string_view::npos if it doesn't find
    // the substring. Otherwise it returns the index where the substring occurs
    // in str.
    return str.find("nut") != std::string_view::npos;
}

int main()
{
    constexpr std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

    // Scan our array to see if any elements contain the "nut" substring
    auto found{ std::find_if(arr.begin(), arr.end(), containsNut) };

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
这段代码在字符串数组中搜索第一个包含子字符串“nut”的元素。因此，它产生的结果是
Found walnut
虽然它有效，但可以改进。
这里问题的症结在于
std::find_if
要求我们传递一个函数指针。因此，我们被迫定义一个只使用一次的函数，该函数必须有一个名称，并且必须放在全局作用域中（因为函数不能嵌套！）。这个函数也如此简短，以至于从一行代码中辨别其功能几乎比从名称和注释中更容易。
Lambda 是匿名函数
lambda 表达式
（也称为
lambda
或
闭包
）允许我们在另一个函数内部定义一个匿名函数。嵌套很重要，因为它允许我们避免命名空间污染，并将函数尽可能地定义在使用它的位置附近（提供额外的上下文）。
lambda 的语法是 C++ 中比较奇怪的东西之一，需要一些时间来适应。lambda 的形式是
[ captureClause ] ( parameters ) -> returnType
{
    statements;
}
如果不需要捕获，捕获子句可以为空。
如果不需要参数，参数列表可以为空。除非指定了返回类型，否则也可以完全省略。
返回类型是可选的，如果省略，将假定为
auto
（因此使用类型推导来确定返回类型）。虽然我们之前提到过应该避免函数返回类型的类型推导，但在这种情况下，使用它是可以的（因为这些函数通常非常简单）。
另请注意，lambda（作为匿名函数）没有名称，所以我们不需要提供一个。
题外话…
这意味着一个简单的 lambda 定义如下
#include <iostream>

int main()
{
  [] {}; // a lambda with an omitted return type, no captures, and omitted parameters.

  return 0;
}
让我们使用 lambda 重写上面的例子
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  // Define the function right where we use it.
  auto found{ std::find_if(arr.begin(), arr.end(),
                           [](std::string_view str) // here's our lambda, no capture clause
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
这就像函数指针的情况一样有效，并产生相同的结果
Found walnut
请注意我们的 lambda 与
containsNut
函数多么相似。它们都具有相同的参数和函数体。lambda 没有捕获子句（我们将在下一课中解释什么是捕获子句），因为它不需要。并且我们在 lambda 中省略了尾随返回类型（为了简洁），但是由于
operator!=
返回一个
bool
，我们的 lambda 也会返回一个
bool
。
最佳实践
遵循在最小作用域中定义事物并最接近首次使用的最佳实践，当我们需要一个简单的一次性函数作为参数传递给其他函数时，lambda 优于普通函数。
Lambda 的类型
在上面的例子中，我们直接在需要它的地方定义了一个 lambda。这种使用 lambda 的方式有时被称为
函数字面量
。
然而，在与使用它的同一行编写 lambda 有时会使代码更难阅读。就像我们可以用字面值（或函数指针）初始化一个变量供以后使用一样，我们也可以用 lambda 定义初始化一个 lambda 变量，然后供以后使用。命名 lambda 和一个好的函数名可以使代码更易读。
例如，在下面的代码片段中，我们使用
std::all_of
来检查数组的所有元素是否都是偶数
// Bad: We have to read the lambda to understand what's happening.
return std::all_of(array.begin(), array.end(), [](int i){ return ((i % 2) == 0); });
我们可以通过以下方式提高其可读性
// Good: Instead, we can store the lambda in a named variable and pass it to the function.
auto isEven{
  [](int i)
  {
    return (i % 2) == 0;
  }
};

return std::all_of(array.begin(), array.end(), isEven);
注意最后一行读起来多好：“返回数组中是否
所有
元素都是
偶数
”
关键见解
将 lambda 存储在变量中为我们提供了一种为 lambda 赋予有用名称的方法，这有助于使我们的代码更易读。
将 lambda 存储在变量中也为我们提供了一种多次使用该 lambda 的方法。
但是 lambda
isEven
的类型是什么？
事实证明，lambda 没有我们可以明确使用的类型。当我们编写 lambda 时，编译器会为该 lambda 生成一个独一无二的类型，该类型不会暴露给我们。
致进阶读者
实际上，lambda 不是函数（这也是它们避免 C++ 不支持嵌套函数的限制的部分原因）。它们是一种特殊类型的对象，称为函数对象（functor）。函数对象是包含重载的
operator()
的对象，这使得它们可以像函数一样被调用。
尽管我们不知道 lambda 的类型，但有几种方法可以存储 lambda 以供定义后使用。如果 lambda 有一个空的捕获子句（方括号 [] 之间没有任何内容），我们可以使用一个普通的函数指针。
std::function
或通过
auto
关键字进行类型推导也可以（即使 lambda 有一个非空的捕获子句）。
#include <functional>

int main()
{
  // A regular function pointer. Only works with an empty capture clause (empty []).
  double (*addNumbers1)(double, double){
    [](double a, double b) {
      return a + b;
    }
  };

  addNumbers1(1, 2);

  // Using std::function. The lambda could have a non-empty capture clause (discussed next lesson).
  std::function addNumbers2{ // note: pre-C++17, use std::function<double(double, double)> instead
    [](double a, double b) {
      return a + b;
    }
  };

  addNumbers2(3, 4);

  // Using auto. Stores the lambda with its real type.
  auto addNumbers3{
    [](double a, double b) {
      return a + b;
    }
  };

  addNumbers3(5, 6);

  return 0;
}
使用 lambda 实际类型的唯一方法是通过
auto
。与
std::function
相比，
auto
的优点是没有开销。
如果我们想将 lambda 传递给函数怎么办？有 4 种选择
#include <functional>
#include <iostream>

// Case 1: use a `std::function` parameter
void repeat1(int repetitions, const std::function<void(int)>& fn)
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);
}

// Case 2: use a function template with a type template parameter
template <typename T>
void repeat2(int repetitions, const T& fn)
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);
}

// Case 3: use the abbreviated function template syntax (C++20)
void repeat3(int repetitions, const auto& fn)
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);
}

// Case 4: use function pointer (only for lambda with no captures)
void repeat4(int repetitions, void (*fn)(int))
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);   
}

int main()
{
    auto lambda = [](int i)
    {
        std::cout << i << '\n';
    };

    repeat1(3, lambda);
    repeat2(3, lambda);
    repeat3(3, lambda);
    repeat4(3, lambda);

    return 0;
}
在情况 1 中，我们的函数参数是
std::function
。这很好，因为我们可以明确地看到
std::function
的参数和返回类型。然而，这要求在每次调用函数时将 lambda 隐式转换，这会增加一些开销。这种方法还有一个好处，如果需要，可以将其分离为声明（在头文件中）和定义（在 .cpp 文件中）。
在情况 2 中，我们使用带有类型模板参数
T
的函数模板。当函数被调用时，将实例化一个函数，其中
T
与 lambda 的实际类型匹配。这更高效，但
T
的参数和返回类型不明显。
在情况 3 中，我们使用 C++20 的
auto
来调用缩写的函数模板语法。这会生成一个与情况 2 相同的函数模板。
在情况 4 中，函数参数是函数指针。由于没有捕获的 lambda 会隐式转换为函数指针，因此我们可以将没有捕获的 lambda 传递给此函数。
最佳实践
将 lambda 存储在变量中时，将
auto
用作变量的类型。
将 lambda 传递给函数时
如果支持 C++20，则将
auto
用作参数类型。
否则，使用带有类型模板参数或
std::function
参数的函数（如果 lambda 没有捕获，则使用函数指针）。
泛型 Lambda
在大多数情况下，lambda 参数遵循与普通函数参数相同的规则。
一个值得注意的例外是，自 C++14 以来，我们允许对参数使用
auto
（注意：在 C++20 中，普通函数也可以对参数使用
auto
）。当 lambda 有一个或多个
auto
参数时，编译器将根据对 lambda 的调用推断所需的参数类型。
因为带有一个或多个
auto
参数的 lambda 可以与各种类型一起工作，所以它们被称为
泛型 lambda
。
致进阶读者
在 lambda 的上下文中，
auto
只是模板参数的缩写。
让我们看一个泛型 lambda
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array months{ // pre-C++17 use std::array<const char*, 12>
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  };

  // Search for two consecutive months that start with the same letter.
  const auto sameLetter{ std::adjacent_find(months.begin(), months.end(),
                                      [](const auto& a, const auto& b) {
                                        return a[0] == b[0];
                                      }) };

  // Make sure that two months were found.
  if (sameLetter != months.end())
  {
    // std::next returns the next iterator after sameLetter
    std::cout << *sameLetter << " and " << *std::next(sameLetter)
              << " start with the same letter\n";
  }

  return 0;
}
输出
June and July start with the same letter
在上面的例子中，我们使用
auto
参数通过
const
引用捕获我们的字符串。因为所有字符串类型都允许通过
operator[]
访问其单个字符，所以我们无需关心用户是传入
std::string
、C 风格字符串还是其他类型。这允许我们编写一个可以接受其中任何一个的 lambda，这意味着如果我们稍后更改
months
的类型，我们无需重写 lambda。
然而，
auto
并非总是最佳选择。考虑
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array months{ // pre-C++17 use std::array<const char*, 12>
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  };

  // Count how many months consist of 5 letters
  const auto fiveLetterMonths{ std::count_if(months.begin(), months.end(),
                                       [](std::string_view str) {
                                         return str.length() == 5;
                                       }) };

  std::cout << "There are " << fiveLetterMonths << " months with 5 letters\n";

  return 0;
}
输出
There are 2 months with 5 letters
在此示例中，使用
auto
将推断出
const char*
类型。C 风格字符串不易处理（除了使用
operator[]
）。在这种情况下，我们更喜欢将参数明确定义为
std::string_view
，这使我们能够更轻松地处理底层数据（例如，我们可以向 string_view 请求其长度，即使用户传入的是 C 风格数组）。
Constexpr Lambda
从 C++17 开始，如果 lambda 的结果满足常量表达式的要求，它将隐式为 constexpr。这通常需要两件事
lambda 必须不捕获任何变量，或者所有捕获都必须是 constexpr。
lambda 调用的函数必须是 constexpr。请注意，许多标准库算法和数学函数直到 C++20 或 C++23 才被设为 constexpr。
在上面的例子中，我们的 lambda 在 C++17 中不会隐式为 constexpr，但在 C++20 中会（因为
std::count_if
在 C++20 中被设为 constexpr）。这意味着在 C++20 中我们可以将
fiveLetterMonths
设为 constexpr
constexpr auto fiveLetterMonths{ std::count_if(months.begin(), months.end(),
                                       [](std::string_view str) {
                                         return str.length() == 5;
                                       }) };
泛型 lambda 和静态变量
在课程
11.7 — 函数模板实例化
中，我们讨论了当函数模板包含静态局部变量时，从该模板实例化的每个函数将拥有自己的独立静态局部变量。如果这不是预期的，可能会导致问题。
泛型 lambda 的工作方式相同：对于
auto
解析到的每种不同类型，都会生成一个唯一的 lambda。
以下示例展示了一个泛型 lambda 如何变成两个不同的 lambda
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  // Print a value and count how many times @print has been called.
  auto print{
    [](auto value) {
      static int callCount{ 0 };
      std::cout << callCount++ << ": " << value << '\n';
    }
  };

  print("hello"); // 0: hello
  print("world"); // 1: world

  print(1); // 0: 1
  print(2); // 1: 2

  print("ding dong"); // 2: ding dong

  return 0;
}
输出
0: hello
1: world
0: 1
1: 2
2: ding dong
在上面的例子中，我们定义了一个 lambda，然后用两个不同的参数（一个字符串字面量参数和一个整数参数）调用它。这会生成两个不同版本的 lambda（一个带字符串字面量参数，一个带整数参数）。
大多数情况下，这无关紧要。但是，请注意，如果泛型 lambda 使用静态持续时间变量，则这些变量不会在生成的 lambda 之间共享。
我们可以在上面的示例中看到这一点，其中每种类型（字符串字面量和整数）都有自己独特的计数！尽管我们只编写了一次 lambda，但生成了两个 lambda——每个都有自己的
callCount
版本。要在两个生成的 lambda 之间共享计数器，我们必须在 lambda 外部定义一个全局变量或一个
static
局部变量。正如您从前面的课程中了解到的，全局变量和静态局部变量都可能导致问题，并使代码更难理解。在下一课讨论 lambda 捕获之后，我们将能够避免这些变量。
返回类型推导和尾随返回类型
如果使用返回类型推导，lambda 的返回类型将从 lambda 内部的
return
语句中推导出来，并且 lambda 中的所有返回语句都必须返回相同的类型（否则编译器将不知道优先选择哪个）。
例如
#include <iostream>

int main()
{
  auto divide{ [](int x, int y, bool intDivision) { // note: no specified return type
    if (intDivision)
      return x / y; // return type is int
    else
      return static_cast<double>(x) / y; // ERROR: return type doesn't match previous return type
  } };

  std::cout << divide(3, 2, true) << '\n';
  std::cout << divide(3, 2, false) << '\n';

  return 0;
}
这会产生一个编译错误，因为第一个返回语句的返回类型 (int) 与第二个返回语句的返回类型 (double) 不匹配。
在返回不同类型的情况下，我们有两种选择
进行显式类型转换，使所有返回类型匹配，或
显式指定 lambda 的返回类型，并让编译器进行隐式转换。
第二种情况通常是更好的选择
#include <iostream>

int main()
{
  // note: explicitly specifying this returns a double
  auto divide{ [](int x, int y, bool intDivision) -> double {
    if (intDivision)
      return x / y; // will do an implicit conversion of result to double
    else
      return static_cast<double>(x) / y;
  } };

  std::cout << divide(3, 2, true) << '\n';
  std::cout << divide(3, 2, false) << '\n';

  return 0;
}
这样，如果您决定更改返回类型，通常只需更改 lambda 的返回类型，而无需修改 lambda 主体。
标准库函数对象
对于常见的操作（例如加法、否定或比较），您无需编写自己的 lambda，因为标准库附带了许多可用于代替 lambda 的基本可调用对象。这些对象在
<functional>
头文件中定义。
在下面的例子中
#include <algorithm>
#include <array>
#include <iostream>

bool greater(int a, int b)
{
  // Order @a before @b if @a is greater than @b.
  return a > b;
}

int main()
{
  std::array arr{ 13, 90, 99, 5, 40, 80 };

  // Pass greater to std::sort
  std::sort(arr.begin(), arr.end(), greater);

  for (int i : arr)
  {
    std::cout << i << ' ';
  }

  std::cout << '\n';

  return 0;
}
输出
99 90 80 40 13 5
我们可以使用
std::greater
而不是将我们的
greater
函数转换为 lambda（这会稍微模糊其含义）。
#include <algorithm>
#include <array>
#include <iostream>
#include <functional> // for std::greater

int main()
{
  std::array arr{ 13, 90, 99, 5, 40, 80 };

  // Pass std::greater to std::sort
  std::sort(arr.begin(), arr.end(), std::greater{}); // note: need curly braces to instantiate object

  for (int i : arr)
  {
    std::cout << i << ' ';
  }

  std::cout << '\n';

  return 0;
}
输出
99 90 80 40 13 5
总结
与使用循环的解决方案相比，Lambda 和算法库可能看起来不必要地复杂。然而，这种组合只需几行代码即可实现一些非常强大的操作，并且比编写自己的循环更具可读性。最重要的是，算法库具有强大且易于使用的并行性，这是循环无法实现的。升级使用库函数的源代码比升级使用循环的代码更容易。
Lambda 很好用，但它们不能在所有情况下取代普通函数。对于非琐碎和可重用的情况，优先使用普通函数。
小测验时间
问题 #1
创建一个
struct Student
来存储学生的姓名和分数。创建一个学生数组并使用
std::max_element
查找分数最高的学生，然后打印该学生的姓名。
std::max_element
接受列表的
begin
和
end
，以及一个接受 2 个参数并返回
true
（如果第一个参数小于第二个）的函数。
给定以下数组
std::array<Student, 8> arr{
  { { "Albert", 3 },
    { "Ben", 5 },
    { "Christine", 2 },
    { "Dan", 8 }, // Dan has the most points (8).
    { "Enchilada", 4 },
    { "Francis", 1 },
    { "Greg", 3 },
    { "Hagrid", 5 } }
};
您的程序应该打印
Dan is the best student
显示提示
提示
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Student
{
  std::string_view name{};
  int points{};
};

int main()
{
  constexpr std::array<Student, 8> arr{
    { { "Albert", 3 },
      { "Ben", 5 },
      { "Christine", 2 },
      { "Dan", 8 },
      { "Enchilada", 4 },
      { "Francis", 1 },
      { "Greg", 3 },
      { "Hagrid", 5 } }
  };

  const auto best{
    std::max_element(arr.begin(), arr.end(), /* lambda */) // returns an iterator
  };

  std::cout << best->name << " is the best student\n"; // must dereference iterator to get element

  return 0;
}
显示答案
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Student
{
  std::string_view name{};
  int points{};
};

int main()
{
  constexpr std::array<Student, 8> arr{
    { { "Albert", 3 },
      { "Ben", 5 },
      { "Christine", 2 },
      { "Dan", 8 },
      { "Enchilada", 4 },
      { "Francis", 1 },
      { "Greg", 3 },
      { "Hagrid", 5 } }
  };

  const auto best { // returns an iterator
    std::max_element(arr.begin(), arr.end(), [](const auto& a, const auto& b) {
      return a.points < b.points;
    })
  };

  std::cout << best->name << " is the best student\n"; // must dereference iterator to get element

  return 0;
}
问题 #2
在以下代码中使用
std::sort
和 lambda，按平均温度升序对季节进行排序。
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Season
{
  std::string_view name{};
  double averageTemperature{};
};

int main()
{
  std::array<Season, 4> seasons{
    { { "Spring", 285.0 },
      { "Summer", 296.0 },
      { "Fall", 288.0 },
      { "Winter", 263.0 } }
  };

  /*
   * Use std::sort here
   */

  for (const auto& season : seasons)
  {
    std::cout << season.name << '\n';
  }

  return 0;
}
程序应打印
Winter
Spring
Fall
Summer
显示答案
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Season
{
  std::string_view name{};
  double averageTemperature{};
};

int main()
{
  std::array<Season, 4> seasons{
    { { "Spring", 285.0 },
      { "Summer", 296.0 },
      { "Fall", 288.0 },
      { "Winter", 263.0 } }
  };

  // We can compare averageTemperature of the two arguments to
  // sort the array.
  std::sort(seasons.begin(), seasons.end(),
            [](const auto& a, const auto& b) {
              return a.averageTemperature < b.averageTemperature;
            });

  for (const auto& season : seasons)
  {
    std::cout << season.name << '\n';
  }

  return 0;
}
下一课
20.7
Lambda 捕获
返回目录
上一课
20.5
省略号（以及为什么要避免它们）