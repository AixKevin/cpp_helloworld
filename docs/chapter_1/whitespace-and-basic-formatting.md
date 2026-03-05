# 1.8 — 空白字符和基本格式

1.8 — 空白字符和基本格式
Alex
2007 年 6 月 1 日，下午 5:22 PDT
2024 年 1 月 23 日
空白字符（Whitespace）
是一个术语，指的是用于格式化目的的字符。在 C++ 中，这主要指空格、制表符和换行符。C++ 中的空白字符通常用于 3 种情况：分隔某些语言元素、文本内部以及格式化代码。
某些语言元素必须用空白字符分隔
语言的语法要求某些元素必须用空白字符分隔。这主要发生在两个关键字或标识符必须连续放置时，以便编译器能够区分它们。
例如，变量声明必须用空白字符分隔
int x; // int and x must be whitespace separated
如果我们键入
intx
，编译器会将其解释为一个标识符，然后抱怨它不知道标识符
intx
是什么。
再举一个例子，函数的返回类型和名称必须用空白字符分隔
int main(); // int and main must be whitespace separated
当需要空白字符作为分隔符时，编译器不关心使用了多少空白字符，只要存在一些即可。
以下变量定义都有效
int x;
int                y;
            int 
z;
在某些情况下，换行符用作分隔符。单行注释以换行符终止。
例如，做这样的事情会让你陷入麻烦
std::cout << "Hello world!"; // This is part of the comment and
this is not part of the comment
预处理指令（例如
#include <iostream>
）必须放在单独的行上
#include <iostream>
#include <string>
带引号的文本会按字面意义处理空白字符
在带引号的文本内部，空白字符的数量会按字面意义处理。
std::cout << "Hello world!";
与此不同
std::cout << "Hello          world!";
带引号的文本中不允许换行
std::cout << "Hello
     world!"; // Not allowed!
仅用空白字符（空格、制表符或换行符）分隔的带引号文本将被连接起来
std::cout << "Hello "
     "world!"; // prints "Hello world!"
使用空白字符格式化代码
否则，空白字符通常会被忽略。这意味着我们可以随意使用空白字符来格式化我们的代码，使其更易于阅读。
例如，下面这段代码很难阅读
#include <iostream>
int main(){std::cout<<"Hello world";return 0;}
下面这段代码好一些（但仍然很密集）
#include <iostream>
int main() {
std::cout << "Hello world";
return 0;
}
下面这段代码甚至更好
#include <iostream>

int main()
{
    std::cout << "Hello world";

    return 0;
}
语句如果需要，可以分成多行
#include <iostream>

int main()
{
    std::cout
        << "Hello world"; // works fine
    return 0;
}
这对于特别长的语句很有用。
基本格式
与某些其他语言不同，C++ 不对程序员强制执行任何格式限制。因此，我们说 C++ 是一种空白字符独立的语言。
这喜忧参半。一方面，拥有做任何你想做的事情的自由是件好事。另一方面，多年来已经开发出许多不同的 C++ 程序格式化方法，你会发现（有时是显著且令人分心的）关于哪种方法最好的分歧。我们的基本经验法则是，最好的风格是那些能产生最可读代码并提供最大一致性的风格。
以下是我们对基本格式的建议
使用制表符或空格进行缩进都可以（大多数 IDE 都有一个设置，可以将制表符按键转换为适当数量的空格）。喜欢使用空格的开发者倾向于这样做，因为这确保了无论使用哪个编辑器或设置，代码都能精确地对齐。支持使用制表符的人想知道，既然有专门用于缩进的字符，为什么不使用它呢，尤其是你可以将宽度设置为你喜欢的任何值。这里没有正确答案——争论它就像争论蛋糕还是派更好。最终取决于个人偏好。
无论哪种方式，我们建议您将制表符设置为 4 个空格的缩进。有些 IDE 默认设置为 3 个空格的缩进，这也可以。
函数大括号有两种常规样式。
许多开发人员更喜欢将开大括号放在与语句同一行
int main() {
    // statements here
}
这样做的理由是它减少了垂直空白（因为你不需要为开大括号专门占用一整行），这样你就可以在屏幕上容纳更多代码。这增强了代码理解，因为你不需要滚动太多就能理解代码正在做什么。
然而，在本系列教程中，我们将使用常见的替代方案，即开大括号出现在它自己的行上
int main()
{
    // statements here
}
这增强了可读性，并且更不容易出错，因为你的大括号对应该始终以相同的级别缩进。如果由于大括号不匹配而导致编译器错误，则很容易看出问题所在。
花括号内的每个语句都应该比其所属函数的开花括号向内缩进一个制表符。例如
int main()
{
    std::cout << "Hello world!\n"; // tabbed in one tab (4 spaces)
    std::cout << "Nice to meet you.\n"; // tabbed in one tab (4 spaces)
}
行不应该太长。通常，80 个字符是行最大长度的事实标准。如果一行会更长，它应该（在合理的位置）分成多行。这可以通过将后续每行额外缩进一个制表符来完成，或者如果行相似，通过与上面一行对齐（哪种更容易阅读就用哪种）。
int main()
{
    std::cout << "This is a really, really, really, really, really, really, really, " 
        "really long line\n"; // one extra indentation for continuation line

    std::cout << "This is another really, really, really, really, really, really, really, "
                 "really long line\n"; // text aligned with the previous line for continuation line

    std::cout << "This one is short\n";
}
这使得您的行更易于阅读。在现代宽屏显示器上，它还允许您将两个具有相似代码的窗口并排放置，从而更轻松地进行比较。
最佳实践
考虑将行长度保持在 80 个字符或更少。
提示
许多编辑器都有内置功能（或插件/扩展），可以在给定列（例如 80 个字符处）显示一条线（称为“列参考线”），因此您可以轻松查看何时行变得太长。要查看您的编辑器是否支持此功能，请搜索您的编辑器名称 + “Column guide”。
如果长行被运算符（例如 << 或 +）分割，则运算符应放在下一行的开头，而不是当前行的末尾
std::cout << 3 + 4
        + 5 + 6
        * 7 * 8;
这有助于更清楚地表明后续行是前一行的延续，并允许您将运算符左对齐，从而更易于阅读。
使用空白字符，通过对齐值或注释，或在代码块之间添加间距，使您的代码更易于阅读。
更难阅读
cost = 57;
pricePerItem = 24;
value = 5;
numberOfItems = 17;
更易阅读
cost          = 57;
pricePerItem  = 24;
value         = 5;
numberOfItems = 17;
更难阅读
std::cout << "Hello world!\n"; // cout lives in the iostream library
std::cout << "It is very nice to meet you!\n"; // these comments make the code hard to read
std::cout << "Yeah!\n"; // especially when lines are different lengths
更易阅读
std::cout << "Hello world!\n";                  // cout lives in the iostream library
std::cout << "It is very nice to meet you!\n";  // these comments are easier to read
std::cout << "Yeah!\n";                         // especially when all lined up
更难阅读
// cout lives in the iostream library
std::cout << "Hello world!\n";
// these comments make the code hard to read
std::cout << "It is very nice to meet you!\n";
// especially when all bunched together
std::cout << "Yeah!\n";
更易阅读
// cout lives in the iostream library
std::cout << "Hello world!\n";

// these comments are easier to read
std::cout << "It is very nice to meet you!\n";

// when separated by whitespace
std::cout << "Yeah!\n";
我们将在本教程中遵循这些约定，它们将成为您的第二天性。随着我们向您介绍新主题，我们也会引入与这些功能相关的新样式建议。
最终，C++ 赋予您选择最适合您或您认为最好的风格的权力。然而，我们强烈建议您采用我们示例中使用的相同风格。它已经通过数千名程序员数十亿行代码的实战检验，并针对成功进行了优化。
一个例外：如果您正在别人的代码库中工作，请采用他们的风格。保持一致性优于您的个人偏好。
最佳实践
在现有项目中工作时，请与已采用的任何样式保持一致。
自动格式化
大多数现代 IDE 会在您输入代码时帮助您格式化代码（例如，当您创建一个函数时，IDE 会自动缩进函数体内的语句）。
但是，随着您添加或删除代码，或更改 IDE 的默认格式，或粘贴具有不同格式的代码块，格式可能会被打乱。修复部分或整个文件的格式可能会令人头疼。幸运的是，现代 IDE 通常包含自动格式化功能，可以重新格式化选择（用鼠标高亮显示）或整个文件。
对于 Visual Studio 用户
在 Visual Studio 中，自动格式化选项可以在
编辑 > 高级 > 格式化文档
和
编辑 > 高级 > 格式化选择
下找到。
对于 Code::Blocks 用户
在 Code::Blocks 中，自动格式化选项可以在
右键单击 > 使用 AStyle 格式化
下找到。
为了方便访问，我们建议为自动格式化活动文件添加键盘快捷键。
还有一些外部工具可以用于自动格式化代码。
clang-format
是一个流行的工具。
最佳实践
强烈建议使用自动格式化功能来保持代码格式风格的一致性。
样式指南
样式指南
是一份简洁、有主见的文档，包含（有时是任意的）编程约定、格式化指南和最佳实践。样式指南的目标是确保项目中所有开发人员以一致的方式进行编程。
一些常用的 C++ 样式指南包括
C++ 核心准则
，由 Bjarne Stroustrup 和 Herb Sutter 维护。
谷歌
.
LLVM
GCC/GNU
我们通常倾向于 C++ 核心准则，因为它们是最新的且适用范围广。
下一课
1.9
字面量和运算符简介
返回目录
上一课
1.7
关键字和标识符命名