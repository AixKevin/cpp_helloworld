# 5.x — 第5章总结和测验

5.x — 第5章总结和测验
Alex
2023年10月23日，太平洋夏令时下午1:50
2024年12月2日
章节回顾
常量
是在程序执行期间不能更改的值。C++ 支持两种类型的常量：命名常量和字面量。
命名常量
是与标识符关联的常量值。
字面量常量
是未与标识符关联的常量值。
其值不能更改的变量称为
常量变量
。
const
关键字可用于使变量成为常量。常量变量必须初始化。避免在按值传递或按值返回时使用
const
。
类型限定符
是应用于类型以修改该类型行为方式的关键字。截至 C++23，C++ 仅支持
const
和
volatile
作为类型限定符。
常量表达式
是可以在编译时求值的表达式。不是常量表达式的表达式有时称为
运行时表达式
。
编译时常量
是其值在编译时已知的常量。
运行时常量
是其初始化值直到运行时才已知的常量。
constexpr
变量必须是编译时常量，并用常量表达式初始化。函数参数不能是 constexpr。
字面量
是直接插入到代码中的值。字面量具有类型，字面量后缀可用于将字面量的类型从默认类型更改。
魔法数字
是字面量（通常是数字），其含义不明确或以后可能需要更改。不要在代码中使用魔法数字。相反，请使用符号常量。
在日常生活中，我们使用有10个数字的
十进制
数进行计数。计算机使用只有2个数字的
二进制
。C++ 还支持
八进制
（基数8）和
十六进制
（基数16）。这些都是
数字系统
的示例，数字系统是用于表示数字的符号（数字）的集合。
字符串
是用于表示文本（例如名称、单词和句子）的连续字符集合。字符串字面量始终放置在双引号之间。C++ 中的字符串字面量是 C 风格字符串，它们具有难以处理的奇怪类型。
std::string
提供了一种简单安全地处理文本字符串的方法。std::string 位于 <string> 头文件中。
std::string
的初始化（或赋值）和复制成本很高。
std::string_view
提供对现有字符串（C 风格字符串字面量、std::string 或 char 数组）的只读访问，而不进行复制。正在查看已销毁字符串的
std::string_view
有时称为
悬空
视图。当
std::string
被修改时，所有对该
std::string
的视图都将
失效
，这意味着这些视图现在无效。使用失效的视图（除了重新验证它）将产生未定义的行为。
由于 C 风格字符串字面量存在于整个程序中，因此可以将
std::string_view
设置为 C 风格字符串字面量，甚至可以从函数返回此类
std::string_view
。
子字符串
是现有字符串中连续的字符序列。
小测验时间
问题 #1
为什么命名常量通常比字面量常量更好？
显示答案
在程序中使用字面量常量（也称为魔法数字）会使程序更难理解和修改。符号常量有助于说明数字实际代表什么，并且在声明处更改符号常量会更改其所有使用位置的值。
为什么 const/constexpr 变量通常比 #defined 符号常量更好？
显示答案
#define 常量不会出现在调试器中，并且更容易出现命名冲突。
问题 #2
在以下代码中找出3个问题
#include <cstdint> // for std::uint8_t
#include <iostream>

int main()
{
  std::cout << "How old are you?\n";

  std::uint8_t age{};
  std::cin >> age;

  std::cout << "Allowed to drive a car in Texas: ";

  if (age >= 16)
      std::cout << "Yes";
  else
      std::cout << "No";

  std::cout << '.\n';

  return 0;
}
期望的示例输出
How old are you?
6
Allowed to drive a car in Texas: No
How old are you?
19
Allowed to drive a car in Texas: Yes
显示答案
在第8行，
age
被定义为
std::uint8_t
。因为
std::uint8_t
通常被定义为 char 类型，所以在此处使用它会导致程序表现得像我们正在输入和输出 char 值而不是数值。例如，如果用户输入他们的年龄为“18”，则只会提取字符
'1'
。因为
1
的 ASCII 值为
49
，所以用户将被视为49岁。应该使用常规的
int
来存储年龄，因为年龄不需要特定的最小整数宽度。我们还可以删除
#include <cstdint>
。
在第13行，我们使用了魔法数字
16
。尽管
16
的含义从其使用上下文来看很清楚，但最好使用值为
16
的
constexpr
变量。
在第18行，
'.\n'
是一个多字符字面量，它将打印错误的值。它应该用双引号括起来 (
".\n"
)。
问题 #3
std::string
和
std::string_view
之间主要区别是什么？
使用
std::string_view
时会发生什么问题？
显示答案
std::string
提供可修改的字符串。它的初始化和复制成本很高。
std::string_view
提供对其他位置存在的字符串的只读视图。它的初始化和复制成本低。当被查看的字符串在查看它的
std::string_view
之前被销毁时，
std::string_view
可能很危险。
问题 #4
编写一个程序，询问两个人的姓名和年龄，然后打印出谁更年长。
这是程序的一次运行示例输出
Enter the name of person #1: John Bacon
Enter the age of John Bacon: 37
Enter the name of person #2: David Jenkins
Enter the age of David Jenkins: 44
David Jenkins (age 44) is older than John Bacon (age 37).
显示提示
提示：使用
std::getline()
输入人物姓名
显示答案
#include <iostream>
#include <string>
#include <string_view>

std::string getName(int num)
{
    std::cout << "Enter the name of person #" << num << ": ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // read a full line of text into name

    return name;
}

int getAge(std::string_view sv)
{
    std::cout << "Enter the age of " << sv << ": ";
    int age{};
    std::cin >> age;

    return age;
}

void printOlder(std::string_view name1, int age1, std::string_view name2, int age2)
{
    if (age1 > age2)
        std::cout << name1 << " (age " << age1 <<") is older than " << name2 << " (age " << age2 <<").\n";
    else
        std::cout << name2 << " (age " << age2 <<") is older than " << name1 << " (age " << age1 <<").\n";
}

int main()
{
    const std::string name1{ getName(1) };
    const int age1 { getAge(name1) };
    
    const std::string name2{ getName(2) };
    const int age2 { getAge(name2) };

    printOlder(name1, age1, name2, age2);

    return 0;
}
问题 #5
在上述测验的解决方案中，为什么
main
中的变量
age1
不能是 constexpr？
显示答案
constexpr 变量需要一个常量表达式初始化器，并且在常量表达式中不允许调用
getAge()
。因此，我们只能将变量设为 const。
下一课
6.1
运算符优先级和结合性
返回目录
上一课
5.9
std::string_view（第二部分）