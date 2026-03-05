# 13.y — 使用语言参考手册

13.y — 使用语言参考手册
nascardriver
2020 年 1 月 30 日，太平洋标准时间上午 9:04
2024 年 1 月 2 日
根据您在学习编程语言（特别是 C++）旅程中的阶段，LearnCpp.com 可能是您学习 C++ 或查找某些内容的唯一资源。LearnCpp.com 旨在以对初学者友好的方式解释概念，但它无法涵盖语言的方方面面。当您开始探索这些教程未涵盖的主题时，您将不可避免地遇到这些教程无法回答的问题。在这种情况下，您需要利用外部资源。
其中一个资源是
Stack Overflow
，您可以在其中提问（或者更好的是，阅读之前有人问过的相同问题的答案）。但有时，更好的第一站是参考指南。与教程不同，参考指南倾向于关注最重要的主题，并使用非正式/常用语言使学习更容易，而参考指南则使用正式术语精确描述 C++。因此，参考资料往往是全面、准确且……难以理解的。
在本课程中，我们将通过研究 3 个示例来展示如何使用
cppreference
，这是一个我们整个课程中都会引用的流行标准参考。
概述
Cppreference 会以核心语言和库的
概述
来迎接您
从这里，您可以访问 cppreference 提供的所有内容，但使用搜索功能或搜索引擎会更容易。一旦您完成了 LearnCpp.com 上的教程，概述是深入研究库并查看语言可能提供的您尚未意识到的其他内容的好地方。
表格的上半部分显示了语言中当前的功能，而下半部分显示了技术规范，这些功能可能在未来版本中添加到 C++ 中，也可能尚未完全接受到语言中。如果您想查看即将推出的新功能，这会很有用。
从 C++11 开始，cppreference 会用添加功能时所用的语言标准版本来标记所有功能。标准版本是您在上面图片中一些链接旁边看到的小绿数字。没有版本号的功能从 C++98/03 开始就可用。版本号不仅在概述中，而且在 cppreference 的任何地方，让您确切知道在特定的 C++ 版本中可以使用或不能使用什么。
警告
如果您使用搜索引擎，并且技术规范刚刚被标准接受，您可能会被链接到技术规范而不是官方参考，这两者可能有所不同。
提示
Cppreference 是 C++ 和 C 的参考手册。由于 C++ 和 C 共享一些函数名称，因此您在搜索某些内容后可能会发现自己处于 C 参考手册中。cppreference 顶部的 URL 和导航栏始终会显示您正在浏览 C 还是 C++ 参考手册。
std::string::length
我们首先研究您在之前的课程中了解的一个函数，
std::string::length
，它返回字符串的长度。
在 cppreference 的右上角，搜索“string”。这样做会显示一个长长的类型和函数列表，其中目前只有顶部是相关的。
我们本可以直接搜索“string length”，但为了在本课程中尽可能多地展示，我们选择了更长的路径。点击“Strings library”会带我们到一个页面，介绍 C++ 支持的各种字符串。
如果我们查看“std::basic_string”部分，我们可以看到一个 typedef 列表，在该列表中是 std::string。
点击“std::string”会跳转到
std::basic_string
的页面。没有
std::string
的页面，因为
std::string
是
std::basic_string<char>
的
typedef
，这再次可以在
typedef
列表中看到
<char>
表示字符串的每个字符都是
char
类型。您会注意到 C++ 提供了使用不同字符类型的其他字符串。在使用 Unicode 而不是 ASCII 时，这些字符串会很有用。
在同一页的下方，有一个
成员函数列表
（类型所具有的行为）。如果您想知道如何使用某种类型，此列表非常方便。在此列表中，您会找到一行
length
（和
size
）。
点击链接将我们带到
length
和
size
的详细函数描述，它们都做同样的事情。
每个页面的顶部都以功能和语法的简短摘要、重载或声明开头
页面标题显示了类和函数的名称以及所有模板参数。我们可以忽略这部分。标题下方，我们看到所有不同的函数重载（同名函数的不同版本）以及它们适用的语言标准。
在此之下，我们可以看到函数接受的参数，以及返回值的含义。
因为
std::string::length
是一个简单的函数，所以此页面上的内容不多。许多页面都显示了它们正在记录的功能的示例用法，此页面也是如此
当您还在学习 C++ 时，示例中会出现您以前从未见过的一些特性。如果有足够的示例，您可能能够理解其中足够多的内容，以便了解函数是如何使用的以及它做了什么。如果示例过于复杂，您可以去其他地方搜索示例，或者阅读您不理解的部分的参考资料（您可以点击示例中的函数和类型来查看它们的作用）。
现在我们知道了
std::string::length
的作用，但我们之前就知道。我们来看看一些新东西吧！
std::cin.ignore
在
9.5 — std::cin 和处理无效输入
这一课中，我们谈到了
std::cin.ignore
，它用于忽略直到换行符的所有内容。这个函数的一个参数是某个长而冗长的值。那是什么来着？你不能只用一个大数字吗？这个参数到底有什么用？让我们来弄清楚！
在 cppreference 搜索中键入“std::cin.ignore”会得到以下结果
std::cin, std::wcin
- 我们需要
.ignore
，而不是普通的
std::cin
。
std::basic_istream<CharT,Traits>::ignore
- 呃，这是什么？我们先跳过。
std::ignore
- 不，不是那个。
std::basic_istream
- 也不是那个。
它不在那里，现在怎么办？让我们去
std::cin
并从那里开始。那个页面上没有什么显而易见的东西。在顶部，我们可以看到
std::cin
和
std::wcin
的声明，它告诉我们需要包含哪个头文件才能使用
std::cin
我们可以看到
std::cin
是
std::istream
类型的一个对象。让我们点击链接到
std::istream
等等！我们之前在搜索“std::cin.ignore”时见过
std::basic_istream
。原来
istream
是
basic_istream
的 typedef 名称，所以也许我们的搜索并没有错。
向下滚动该页面，我们看到了熟悉的函数
我们已经使用过很多这些函数：
operator>>
,
get
,
getline
,
ignore
。在该页面上滚动一下，了解
std::cin
中还有哪些内容。然后点击
ignore
，因为这是我们感兴趣的。
在页面顶部是函数签名以及函数及其两个参数的作用描述。参数后的
=
符号表示一个
默认参数
（我们在
11.5 -- 默认参数
这一课中介绍）。如果我们没有为具有默认值的参数提供参数，则使用默认值。
第一个要点回答了我们所有的问题。我们可以看到
std::numeric_limits<std::streamsize>::max()
对
std::cin.ignore
具有特殊含义，即它禁用了字符计数检查。这意味着
std::cin.ignore
将继续忽略字符，直到找到分隔符，或者直到它没有字符可查看。
很多时候，如果您已经了解一个函数但忘记了参数或返回值的含义，则无需阅读函数的完整描述。在这种情况下，阅读参数或返回值的描述就足够了。
参数描述很简短。它不包含
std::numeric_limits<std::streamsize>::max()
的特殊处理或其他停止条件，但可以很好地提醒。
一个语言语法示例
除了标准库，cppreference 还记录了语言语法。这是一个有效的程序
#include <iostream>

int getUserInput()
{
  int i{};
  std::cin >> i;
  return i;
}

int main()
{
  std::cout << "How many bananas did you eat today? \n";

  if (int iBananasEaten{ getUserInput() }; iBananasEaten <= 2)
  {
    std::cout << "Yummy\n";
  }
  else
  {
    std::cout << iBananasEaten << " is a lot!\n";
  }

  return 0;  
}
为什么
if-statement
的条件中有一个变量定义？让我们使用 cppreference 通过在我们最喜欢的搜索引擎中搜索“cppreference if statement”来找出它的作用。这样做会将我们带到
if 语句
。在顶部，有一个语法参考。
看看
if-statement
的语法。如果你删掉所有可选部分，你就会得到一个你已经知道的
if-statement
。在
condition
之前，有一个可选的
init-statement
，它看起来就像上面代码中发生的那样。
if ( init-statement condition ) statement-true
if ( init-statement condition ) statement-true else statement-false
在语法参考下方，解释了语法的每个部分，包括
init-statement
。它说
init-statement
通常是一个带有初始化器的变量声明。
语法之后是
if-statements
的解释和简单示例
我们已经知道
if-statements
是如何工作的，而且示例中不包含
init-statement
，所以我们向下滚动一点，找到一个专门介绍带有初始化器的
if-statements
的部分
首先，它展示了如何编写
init-statement
而实际上不使用
init-statement
。现在我们知道问题中的代码在做什么了。它是一个正常的变量声明，只是合并到了
if-statement
中。
接下来的句子很有趣，因为它让我们知道来自
init-statement
的名称在
两个
语句（
statement-true
和
statement-false
）中都可用。这可能会令人惊讶，因为您可能原本会认为变量只在
statement-true
中可用。
init-statement
示例使用了我们尚未涵盖的特性和类型。您不必理解所有看到的内容才能理解
init-statement
的工作原理。让我们跳过所有过于令人困惑的内容，直到我们找到可以使用的内容
// Iterators, we don't know them. Skip.
if (auto it = m.find(10); it != m.end()) { return it->second.size(); }

// [10], what's that? Skip.
if (char buf[10]; std::fgets(buf, 10, stdin)) { m[0] += buf; }

// std::lock_guard, we don't know that, but it's some type. We know what types are!
if (std::lock_guard lock(mx); shared_flag) { unsafe_ping(); shared_flag = false; }

// This is easy, that's an int!
if (int s; int count = ReadBytesWithSignal(&s)) { publish(count); raise(s); }

// Whew, no thanks!
if (auto keywords = {"if", "for", "while"};
    std::any_of(keywords.begin(), keywords.end(),
                [&s](const char* kw) { return s == kw; })) {
  std::cerr << "Token must not be a keyword\n";
}
最简单的例子似乎是带有
int
的那个。然后我们看到分号后，还有另一个定义，奇怪……让我们回到
std::lock_guard
的例子。
if (std::lock_guard lock(mx); shared_flag)
{
  unsafe_ping();
  shared_flag = false;
}
由此，相对容易看出
init-statement
的工作原理。定义一些变量（
lock
），然后是分号，然后是条件。这正是我们示例中发生的情况。
关于 cppreference 准确性的警告
Cppreference 不是官方文档来源——它是一个维基。在维基中，任何人都可以添加和修改内容——内容来源于社区。尽管这意味着某人很容易添加错误信息，但这些错误信息通常会很快被发现并删除，这使得 cppreference 成为一个可靠的来源。
C++ 的唯一官方来源是
标准
（
github
上的免费草稿），它是一个正式文档，不易用作参考。
小测验时间
问题 #1
以下程序会输出什么？不要运行它，使用参考手册来弄清楚
erase
的作用。
#include <iostream>
#include <string>

int main()
{
  std::string str{ "The rice is cooking" };

  str.erase(4, 11);

  std::cout << str << '\n';

  return 0;
}
提示
当您在 cppreference 上找到
erase
时，可以忽略使用迭代器的重载。
提示
C++ 中的索引从 0 开始。“House”字符串中索引 0 的字符是 'H'，索引 1 的字符是 'o'，依此类推。
显示答案
The king
以下是您使用 cppreference 上的搜索功能到达那里（您可能通过使用搜索引擎跳过了第一步）的方法
搜索字符串
并点击“std::string”会带我们到
std::basic_string
。
滚动到“成员函数”列表，我们找到
擦除
。如上提示，使用了第一个
函数重载
。它接受 2 个
size_type
（无符号整数类型）参数。在我们的示例中，是 4 和 11。根据 (1) 的描述，它“从
index
开始删除
min(count, size() - index)
个字符”。代入我们的参数，它从索引 4 开始删除
min(11, 19 - 4) = 11
个字符。
问题 #2
在以下代码中，修改
str
，使其值为“I saw a blue car yesterday.”，而不重复字符串。例如，不要这样做
str = "I saw a blue car yesterday.";
您只需调用一个函数即可将“red”替换为“blue”。
#include <iostream>
#include <string>

int main()
{
  std::string str{ "I saw a red car yesterday." };  

  // ...

  std::cout << str << '\n'; // I saw a blue car yesterday.

  return 0;
}
显示提示
提示：
std::basic_string
显示提示
提示：
std::basic_string
的成员函数
显示提示
提示：
std::basic_string
的修饰符
显示提示
提示：
std::basic_string::replace
显示答案
#include <iostream>
#include <string>

int main()
{
  std::string str{ "I saw a red car yesterday." };  

  str.replace(8, 3, "blue");

  std::cout << str << '\n'; // I saw a blue car yesterday.

  return 0;
}
下一课
14.1
面向对象编程简介
返回目录
上一课
13.x
第 13 章总结和测验