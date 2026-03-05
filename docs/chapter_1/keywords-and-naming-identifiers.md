# 1.7 — 关键词和命名标识符

1.7 — 关键词和命名标识符
Alex
2007 年 6 月 5 日，太平洋夏令时下午 6:44
2025 年 1 月 18 日
关键词
C++ 为自己保留了一组 92 个单词（截至 C++23）。这些单词被称为
关键词
（或保留字），每个关键词在 C++ 语言中都有特殊的含义。
以下是所有 C++ 关键词的列表（直至 C++23）：
alignas
alignof
and
and_eq
asm
auto
bitand
bitor
bool
break
case
catch
char
char8_t (自 C++20 起)
char16_t
char32_t
class
compl
concept (自 C++20 起)
const
consteval (自 C++20 起)
constexpr
constinit (自 C++20 起)
const_cast
continue
co_await (自 C++20 起)
co_return (自 C++20 起)
co_yield (自 C++20 起)
decltype
default
delete
do
double
dynamic_cast
else
enum
explicit
export
extern
false
float
for
friend
goto
if
inline
int
long
mutable
namespace
new
noexcept
not
not_eq
nullptr
operator
或
or_eq
private
protected
public
register
reinterpret_cast
requires (自 C++20 起)
return
short
signed
sizeof
static
static_assert
static_cast
struct
switch
template
this
thread_local
throw
true
try
typedef
typeid
typename
union
unsigned
using
virtual
void
volatile
wchar_t
while
xor
xor_eq
标记为 (C++20) 的关键词是在 C++20 中添加的。如果您的编译器不符合 C++20 标准（或者具有 C++20 功能但默认已关闭），这些关键词可能无法使用。
C++ 还定义了特殊标识符：
override
、
final
、
import
和
module
。这些词在特定上下文中具有特殊含义，但在其他情况下不被保留。
您已经遇到过其中一些关键词，包括
int
和
return
。连同运算符集，这些关键词和特殊标识符定义了 C++ 的整个语言（预处理命令除外）。由于关键词和特殊标识符具有特殊含义，您的 IDE 可能会更改这些词的文本颜色，使其与其他标识符区分开来。
当您完成本教程系列时，您将了解几乎所有这些词的用途！
标识符命名规则
提醒一下，变量（或函数、类型或其他类型的项）的名称称为标识符。C++ 赋予您很大的灵活性，可以按您的意愿命名标识符。但是，命名标识符时必须遵循一些规则：
标识符不能是关键词。关键词是保留的。
标识符只能由字母（小写或大写）、数字和下划线字符组成。这意味着名称不能包含符号（下划线除外）和空格（空格或制表符）。
标识符必须以字母（小写或大写）或下划线开头。不能以数字开头。
C++ 区分大小写，因此区分小写字母和大写字母。
nvalue
不同于
nValue
，也不同于
NVALUE
。
标识符命名最佳实践
现在您知道了如何
可以
命名变量，接下来我们来谈谈您
应该
如何命名变量（或函数）。
在 C++ 中，约定俗成的是变量名应以小写字母开头。如果变量名是单个单词或缩写，则整个名称应以小写字母书写。
int value; // conventional

int Value; // unconventional (should start with lower case letter)
int VALUE; // unconventional (should start with lower case letter and be in all lower case)
int VaLuE; // unconventional (see your psychiatrist) ;)
通常，函数名也以小写字母开头（尽管这一点存在一些争议）。我们将遵循此约定，因为函数
main
（所有程序都必须有）以小写字母开头，C++ 标准库中的所有函数也是如此。
以大写字母开头的标识符名称通常用于用户定义的类型（例如结构体、类和枚举，所有这些我们将在稍后介绍）。
如果变量或函数名是多词的，有两种常见的约定：单词用下划线分隔（有时称为 snake_case），或者采用驼峰式命名（有时称为 camelCase，因为大写字母像骆驼的驼峰一样突起）。
int my_variable_name;   // conventional (separated by underscores/snake_case)
int my_function_name(); // conventional (separated by underscores/snake_case)

int myVariableName;     // conventional (intercapped/camelCase)
int myFunctionName();   // conventional (intercapped/camelCase)

int my variable name;   // invalid (whitespace not allowed)
int my function name(); // invalid (whitespace not allowed) 

int MyVariableName;     // unconventional (should start with lower case letter)
int MyFunctionName();   // unconventional (should start with lower case letter)
在本教程中，我们通常会使用驼峰式命名方法，因为它更容易阅读（在密集的代码块中，很容易将下划线误认为空格）。但两种方式都很常见——C++ 标准库对变量和函数都使用下划线方法。有时您会看到两者的混合使用：变量使用下划线，函数使用驼峰式命名。
值得注意的是，如果您在别人的代码中工作，通常认为匹配您正在处理的代码风格比严格遵循上述命名约定更好。
最佳实践
在现有程序中工作时，请使用该程序的约定（即使它们不符合现代最佳实践）。当您编写新程序时，请使用现代最佳实践。
避免标识符以下划线开头。尽管在语法上合法，但这些名称通常保留供操作系统、库和/或编译器使用。
您的标识符名称应清楚地表明它们所持有的值的含义（特别是当单位不明显时）。标识符的命名方式应有助于对您的代码一无所知的人尽快理解它。3 个月后，当您再次查看程序时，您会忘记它是如何工作的，您会感谢自己选择了有意义的变量名。
然而，给一个简单的标识符起一个过于复杂的名称，与给一个不简单的标识符起一个不恰当的名称一样，几乎都会妨碍对程序整体的理解。一个好的经验法则是，标识符的长度应与其特异性和可访问性成比例。这意味着：
只存在于几条语句中的标识符（例如，在短函数的函数体中）可以有较短的名称。
可从任何地方访问的标识符可能受益于更长的名称。
表示非特定数字的标识符（例如，用户提供的任何内容）可以有较短的名称。
表示特定值的标识符（例如，内缝的长度以毫米计）应该有更长的名称。
int ccount
不好
"count" 之前的 "c" 代表什么？
int customerCount
好
清楚我们正在计数什么
int i
两者皆可
如果用途微不足道则可以，否则不好
int index
两者皆可
如果索引对象显而易见则可以
int totalScore
两者皆可
如果只有一项被评分则可以，否则过于模糊
int _count
不好
不要以下划线开头命名
int count
两者皆可
如果计数对象显而易见则可以
int data
不好
什么类型的数据？
int time
不好
是以秒、分还是小时为单位？
int minutesElapsed
两者皆可
如果 elapsed 的起点显而易见则可以
int x1, x2
两者皆可
如果用途微不足道则可以，否则不好
int userinput1, userinput2
不好
名称过长导致难以区分两者
int numApples
好
描述性强
int monstersKilled
好
描述性强
避免缩写，除非它们常见且明确（例如
num
、
cm
、
idx
）。
关键见解
代码的阅读频率高于编写频率，因此编写代码时节省的任何时间都将被每个读者（包括未来的您）在阅读时浪费掉。如果您想更快地编写代码，请使用编辑器的自动补全功能。
对于变量声明，使用注释来描述变量的用途，或者解释任何可能不明显的地方，这会很有用。例如，假设我们声明了一个变量，用于存储一段文本中的字符数。文本“Hello World！”有 10、11 还是 12 个字符？这取决于我们是否包含空白符或标点符号。与其将变量命名为
numCharsIncludingWhitespaceAndPunctuation
（这太长了），不如在声明行上或上方放置一个恰当的注释，这将有助于用户理解：
// a count of the number of chars in a piece of text, including whitespace and punctuation
int numChars {};
小测验时间
问题 #1
根据变量的
推荐
命名方式，指出每个变量名是符合约定（遵循最佳实践）、不符合约定（编译器接受但不遵循最佳实践），还是无效（无法编译），并说明原因。
int sum {};
（假设要计算的和是显而易见的）
显示答案
符合约定。
int _apples {};
显示答案
不符合约定——变量名不应以下划线开头。
int VALUE {};
显示答案
不符合约定——单词名称应全部小写。
int my variable name {};
显示答案
无效——变量名不能包含空格。
int TotalCustomers {};
显示答案
不符合约定——变量名应以小写字母开头。
int void {};
显示答案
无效——void 是关键词。
int numFruit {};
显示答案
符合约定。
int 3some {};
显示答案
无效——变量名不能以数字开头。
int meters_of_pipe {};
显示答案
符合约定。
下一课
1.8
空白符和基本格式
返回目录
上一课
1.6
未初始化变量和未定义行为