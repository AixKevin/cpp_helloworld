# 5.9 — std::string_view（第二部分）

5.9 — std::string_view（第二部分）
Alex
2022 年 6 月 16 日，太平洋夏令时下午 2:19
2025 年 1 月 2 日
在之前的课程中，我们介绍了两种字符串类型：
std::string
(
5.7 -- std::string 简介
) 和
std::string_view
(
5.8 -- std::string_view 简介
)。
因为
std::string_view
是我们第一次接触视图类型，所以我们将花一些额外的时间进一步讨论它。我们将重点讨论如何安全地使用
std::string_view
，并提供一些示例来说明如何错误地使用它。最后，我们将提供一些关于何时使用
std::string
与
std::string_view
的指导原则。
所有者和视图者简介
让我们暂时插入一个类比。假设你决定要画一幅自行车的画。但是你没有自行车！你该怎么办？
嗯，你可以去当地的自行车店买一辆。你将拥有那辆自行车。这有一些好处：你现在有一辆你可以骑的自行车。你可以保证在你想要的时候自行车总是在那里。你可以装饰它，或者移动它。这种选择也有一些缺点。自行车很贵。如果你买了一辆，你现在就要对它负责。你必须定期维护它。当你最终决定不再需要它时，你必须妥善处理它。
所有权可能很昂贵。作为所有者，你有责任获取、管理和妥善处理你拥有的对象。
出门时，你瞥了一眼窗外。你注意到你的邻居把他们的自行车停在你的窗户对面。你可以直接画一幅你邻居的自行车的画（从你的窗户看）。这种选择有很多好处。你省去了购买自己自行车的费用。你不必维护它。你也不必负责处理它。当你观看完后，你可以直接拉上窗帘，继续你的生活。这结束了你对对象的视图，但对象本身不受影响。这种选择也有一些潜在的缺点。你不能画或定制你邻居的自行车。而且当你观看自行车时，你的邻居可能会决定改变自行车的外观，或者完全将它移出你的视线。你最终可能会看到一些意想不到的东西。
查看是廉价的。作为查看者，你对你正在查看的对象不承担任何责任，但你对这些对象也没有任何控制权。
std::string
是（唯一）所有者
你可能想知道为什么
std::string
会对其初始化器进行昂贵的复制。当一个对象被实例化时，会为该对象分配内存，以存储它在整个生命周期中需要使用的数据。这块内存是为该对象保留的，并保证在对象存在期间一直存在。它是一个安全的空间。
std::string
（和大多数其他对象）会将给定的初始化值复制到这块内存中，以便它们可以拥有自己独立的、稍后可以访问和操作的值。一旦初始化值被复制，该对象就不再以任何方式依赖于初始化器。
这是一件好事，因为在初始化完成后，初始化器通常是不可信的。如果你将初始化过程想象成一个初始化对象的函数调用，那么是谁传入了初始化器？调用者。当初始化完成后，控制权返回给调用者。此时，初始化语句完成，通常会发生以下两种情况之一
如果初始化器是临时值或对象，则该临时值将立即被销毁。
如果初始化器是一个变量，则调用者仍然可以访问该对象。调用者可以对该对象进行任何操作，包括修改或销毁它。
关键见解
已初始化的对象无法控制初始化完成后初始化值会发生什么。
因为
std::string
会复制初始化器，所以它不必担心初始化完成后初始化器会发生什么。初始化器可以被销毁或修改，但这不会影响
std::string
。缺点是这种独立性带来了昂贵的复制成本。
在我们的类比中，
std::string
是所有者——它负责从初始化器获取其字符串数据，管理对字符串数据的访问，并在
std::string
对象被销毁时妥善处理字符串数据。
关键见解
在编程中，当我们称一个对象为所有者时，我们通常指它是唯一所有者（除非另有说明）。唯一所有权（也称为单一所有权）确保明确谁对该数据负责。
我们并非总是需要副本
让我们重新审视上一课中的这个例子
#include <iostream>
#include <string>

void printString(std::string str) // str makes a copy of its initializer
{
    std::cout << str << '\n';
}

int main()
{
    std::string s{ "Hello, world!" };
    printString(s);

    return 0;
}
当调用
printString(s)
时，
str
会对
s
进行一次昂贵的复制。函数会打印复制的字符串，然后将其销毁。
注意，
s
已经持有我们要打印的字符串。我们是否可以直接使用
s
持有的字符串而不是复制？答案是可能的——我们需要评估三个标准
当
str
仍在使用
s
时，
s
是否可能被销毁？不会，
str
在函数结束时消亡，而
s
存在于调用者的作用域中，在函数返回之前不会被销毁。
当
str
仍在使用
s
时，
s
是否可能被修改？不会，
str
在函数结束时消亡，并且调用者在函数返回之前没有机会修改
s
。
str
是否以调用者意想不到的方式修改了字符串？不会，函数根本没有修改字符串。
由于这三个标准都为假，因此使用
s
持有的字符串而不是复制它没有任何风险。而且由于字符串复制很昂贵，为什么我们要为不需要的复制付费呢？
std::string_view
是一个视图
std::string_view
对初始化采取了不同的方法。它不是对初始化字符串进行昂贵的复制，而是创建对初始化字符串的廉价视图。然后，每当需要访问字符串时，就可以使用
std::string_view
。
在我们的类比中，
std::string_view
是一个观察者。它观察一个已经存在于其他地方的对象，并且不能修改该对象。当视图被销毁时，被观察的对象不受影响。多个观察者同时观察一个对象是可以的。
需要注意的是，
std::string_view
在其生命周期内都依赖于初始化器。如果在视图仍在使用时被视图的字符串被修改或销毁，将导致意想不到或未定义的行为。
每当我们使用视图时，我们都必须确保这些可能性不会发生。
警告
视图依赖于被视图的对象。如果在视图仍在使用时被视图的对象被修改或销毁，将导致意外或未定义的行为。
正在查看已销毁字符串的
std::string_view
有时称为**悬空**视图。
std::string_view
最适合用作只读函数参数
std::string_view
最好的用法是作为只读函数参数。这允许我们传递 C 风格字符串、
std::string
或
std::string_view
参数而无需进行复制，因为
std::string_view
将创建对该参数的视图。
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view str) // now a std::string_view, creates a view of the argument
{
    std::cout << str << '\n';
}

int main()
{
    printSV("Hello, world!"); // call with C-style string literal

    std::string s2{ "Hello, world!" };
    printSV(s2); // call with std::string

    std::string_view s3 { s2 };
    printSV(s3); // call with std::string_view
       
    return 0;
}
由于
str
函数参数在控制权返回给调用者之前被创建、初始化、使用和销毁，因此被视图的字符串（函数参数）不会在我们的
str
参数之前被修改或销毁。
我应该首选
std::string_view
还是
const std::string&
函数参数？
高级
在大多数情况下，首选
std::string_view
。我们将在
12.6 -- 按 const 左值引用传递
一课中进一步讨论此主题。
不正确地使用
std::string_view
让我们看看一些滥用
std::string_view
会给我们带来麻烦的案例。
这是我们的第一个例子
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view sv{};

    { // create a nested block
        std::string s{ "Hello, world!" }; // create a std::string local to this nested block
        sv = s; // sv is now viewing s
    } // s is destroyed here, so sv is now viewing an invalid string

    std::cout << sv << '\n'; // undefined behavior

    return 0;
}
在这个例子中，我们正在一个嵌套块中创建
std::string s
（暂时不要担心什么是嵌套块）。然后我们将
sv
设置为查看
s
。
s
在嵌套块的末尾被销毁。
sv
不知道
s
已经被销毁。当我们随后使用
sv
时，我们正在访问一个无效对象，导致未定义行为。
这是相同问题的另一个变体，我们使用函数的
std::string
返回值初始化
std::string_view
#include <iostream>
#include <string>
#include <string_view>

std::string getName()
{
    std::string s { "Alex" };
    return s;
}

int main()
{
  std::string_view name { getName() }; // name initialized with return value of function
  std::cout << name << '\n'; // undefined behavior

  return 0;
}
这与前面的示例类似。
getName()
函数返回一个包含字符串“Alex”的
std::string
。返回值是临时对象，在包含函数调用的完整表达式结束时销毁。我们必须立即使用此返回值，或将其复制以备后用。
但是
std::string_view
不会进行复制。相反，它会创建对临时返回值的视图，然后该临时值被销毁。这导致我们的
std::string_view
悬空（查看无效对象），并且打印视图会导致未定义行为。
以下是上述情况的一个不太明显的变体
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    using namespace std::string_literals;
    std::string_view name { "Alex"s }; // "Alex"s creates a temporary std::string
    std::cout << name << '\n'; // undefined behavior

    return 0;
}
一个
std::string
字面量（通过
s
字面量后缀创建）会创建一个临时的
std::string
对象。因此，在这种情况下，
"Alex"s
会创建一个临时的
std::string
，然后我们将其用作
name
的初始化器。此时，
name
正在查看临时的
std::string
。然后临时的
std::string
被销毁，导致
name
悬空。当我们随后使用
name
时，会产生未定义的行为。
警告
不要使用
std::string
字面量初始化
std::string_view
，因为这会导致
std::string_view
悬空。
用 C 风格字符串字面量或
std::string_view
字面量初始化
std::string_view
是可以的。用 C 风格字符串对象、
std::string
对象或
std::string_view
对象初始化
std::string_view
也是可以的，只要该字符串对象的生命周期长于视图。
当底层字符串被修改时，我们也可能得到未定义行为
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string s { "Hello, world!" };
    std::string_view sv { s }; // sv is now viewing s

    s = "Hello, a!";    // modifies s, which invalidates sv (s is still valid)
    std::cout << sv << '\n';   // undefined behavior

    return 0;
}
在此示例中，
sv
再次设置为查看
s
。然后
s
被修改。当
std::string
被修改时，任何查看该
std::string
的视图都可能被**失效**，这意味着这些视图现在无效或不正确。使用失效的视图将导致未定义行为。
致进阶读者
如果
std::string
重新分配内存以容纳新的字符串数据，它会将用于旧字符串数据的内存返回给操作系统。由于
std::string_view
仍在查看旧的字符串数据，它现在是悬空的（指向一个现在无效的对象）。
如果
std::string
不重新分配内存，它会将新的字符串数据复制到旧的字符串数据上（从相同的内存地址开始）。
std::string_view
现在将查看新的字符串数据（因为它被放置在它正在查看的相同内存地址），但它不会意识到
std::string
的长度可能已经改变。如果新字符串比旧字符串长，
std::string_view
现在将查看新字符串的子字符串（与旧字符串长度相同）。如果新字符串比旧字符串短，
std::string_view
现在将查看新字符串的超字符串（由整个新字符串加上字符串末尾以外内存中仍然存在的任何垃圾字符组成）。
关键见解
修改
std::string
很可能会使所有指向该
std::string
的视图失效。
重新验证无效的
std::string_view
失效的对象通常可以通过将其设置回已知的良好状态来重新验证（使其再次有效）。对于失效的
std::string_view
，我们可以通过为失效的
std::string_view
对象分配一个有效的字符串来查看来实现。
这是与之前相同的示例，但我们将重新验证
sv
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string s { "Hello, world!" };
    std::string_view sv { s }; // sv is now viewing s

    s = "Hello, universe!";    // modifies s, which invalidates sv (s is still valid)
    std::cout << sv << '\n';   // undefined behavior

    sv = s;                    // revalidate sv: sv is now viewing s again
    std::cout << sv << '\n';   // prints "Hello, universe!"

    return 0;
}
在
sv
因
s
的修改而失效后，我们通过语句
sv = s
重新验证了
sv
，这使得
sv
再次成为
s
的有效视图。当我们第二次打印
sv
时，它打印“Hello, universe!”。
小心返回
std::string_view
std::string_view
可以用作函数的返回值。然而，这通常是危险的。
因为局部变量在函数结束时被销毁，返回一个正在查看局部变量的
std::string_view
将导致返回的
std::string_view
无效，并且进一步使用该
std::string_view
将导致未定义行为。例如
#include <iostream>
#include <string>
#include <string_view>

std::string_view getBoolName(bool b)
{
    std::string t { "true" };  // local variable
    std::string f { "false" }; // local variable

    if (b)
        return t;  // return a std::string_view viewing t

    return f; // return a std::string_view viewing f
} // t and f are destroyed at the end of the function

int main()
{
    std::cout << getBoolName(true) << ' ' << getBoolName(false) << '\n'; // undefined behavior

    return 0;
}
在上面的例子中，当调用
getBoolName(true)
时，函数返回一个正在查看
t
的
std::string_view
。然而，
t
在函数结束时被销毁。这意味着返回的
std::string_view
正在查看一个已销毁的对象。因此，当打印返回的
std::string_view
时，会产生未定义行为。
您的编译器可能会或可能不会警告您此类情况。
在两种主要情况下可以安全地返回
std::string_view
。首先，由于 C 风格字符串字面量在整个程序中都存在，因此从返回类型为
std::string_view
的函数返回 C 风格字符串字面量是安全且有用的。
#include <iostream>
#include <string_view>

std::string_view getBoolName(bool b)
{
    if (b)
        return "true";  // return a std::string_view viewing "true"

    return "false"; // return a std::string_view viewing "false"
} // "true" and "false" are not destroyed at the end of the function

int main()
{
    std::cout << getBoolName(true) << ' ' << getBoolName(false) << '\n'; // ok

    return 0;
}
这会打印
true false
当调用
getBoolName(true)
时，函数将返回一个查看 C 风格字符串
"true"
的
std::string_view
。因为
"true"
在整个程序中都存在，所以当我们在
main()
中使用返回的
std::string_view
打印
"true"
时没有问题。
其次，通常可以返回
std::string_view
类型的函数参数
#include <iostream>
#include <string>
#include <string_view>

std::string_view firstAlphabetical(std::string_view s1, std::string_view s2)
{
    if (s1 < s2)
        return s1;
    return s2;
}

int main()
{
    std::string a { "World" };
    std::string b { "Hello" };

    std::cout << firstAlphabetical(a, b) << '\n'; // prints "Hello"

    return 0;
}
这为什么可以接受可能不太明显。首先，请注意参数
a
和
b
存在于调用者的作用域中。当函数被调用时，函数参数
s1
是
a
的视图，函数参数
s2
是
b
的视图。当函数返回
s1
或
s2
时，它将
a
或
b
的视图返回给调用者。由于
a
和
b
在此时仍然存在，因此使用返回的
std::string_view
来访问
a
或
b
是可以的。
这里有一个重要的微妙之处。如果参数是临时对象（将在包含函数调用的完整表达式结束时销毁），则
std::string_view
返回值必须在同一个表达式中使用。在那之后，临时对象被销毁，
std::string_view
将悬空。
警告
如果参数是一个在包含函数调用的完整表达式结束时销毁的临时变量，则返回的
std::string_view
必须立即使用，因为它在临时变量销毁后将悬空。
视图修改函数
想象一下你家里的窗户，看着街上停着一辆电动汽车。你可以透过窗户看到汽车，但你不能触摸或移动汽车。你的窗户只是提供了一个汽车的视图，汽车是一个完全独立的对象。
许多窗户都有窗帘，可以让我们修改我们的视野。我们可以拉上左边或右边的窗帘来减少我们能看到的东西。我们不会改变外面，我们只是减少可见区域。
因为
std::string_view
是一个视图，所以它包含允许我们通过“拉上窗帘”来修改视图的函数。这不会以任何方式修改被查看的字符串，只修改视图本身。
remove_prefix()
成员函数从视图的左侧移除字符。
remove_suffix()
成员函数从视图的右侧移除字符。
#include <iostream>
#include <string_view>

int main()
{
	std::string_view str{ "Peach" };
	std::cout << str << '\n';

	// Remove 1 character from the left side of the view
	str.remove_prefix(1);
	std::cout << str << '\n';

	// Remove 2 characters from the right side of the view
	str.remove_suffix(2);
	std::cout << str << '\n';

	str = "Peach"; // reset the view
	std::cout << str << '\n';

	return 0;
}
此程序生成以下输出：
Peach
each
ea
Peach
与真实的窗帘不同，一旦调用了
remove_prefix()
和
remove_suffix()
，唯一重置视图的方法是再次将源字符串重新分配给它。
std::string_view
可以查看子字符串
这引出了
std::string_view
的一个重要用途。虽然
std::string_view
可以用于查看整个字符串而无需复制，但当我们想要查看子字符串而无需复制时，它们也很有用。**子字符串**是现有字符串中连续的字符序列。例如，给定字符串“snowball”，一些子字符串是“snow”、“all”和“now”。“owl”不是“snowball”的子字符串，因为这些字符在“snowball”中不连续出现。
std::string_view
可能以空字符结尾，也可能不以空字符结尾
能够只查看较长字符串的子字符串带来了一个值得注意的后果：
std::string_view
可能以空字符结尾，也可能不以空字符结尾。
相关内容
我们在
5.2 -- 字面量
一课中介绍了什么是空终止字符串。
考虑字符串“snowball”，它是以空字符结尾的（因为它是一个 C 风格字符串字面量，总是以空字符结尾）。如果
std::string_view
查看整个字符串，那么它正在查看一个以空字符结尾的字符串。但是，如果
std::string_view
只查看子字符串“now”，那么该子字符串不是以空字符结尾的（下一个字符是‘b’）。
关键见解
C 风格字符串字面量和
std::string
始终以空字符结尾。
std::string_view
可能以空字符结尾，也可能不以空字符结尾。
在几乎所有情况下，这并不重要——
std::string_view
会跟踪它正在查看的字符串或子字符串的长度，因此它不需要空终止符。将
std::string_view
转换为
std::string
无论
std::string_view
是否以空终止都将有效。
警告
请注意不要编写任何假定
std::string_view
以空字符结尾的代码。
提示
如果您有一个未以空字符结尾的
std::string_view
，并且由于某种原因需要一个以空字符结尾的字符串，请将
std::string_view
转换为
std::string
。
何时使用
std::string
与
std::string_view
的快速指南
本指南并非旨在全面，而是旨在突出最常见的案例
变量
在以下情况下使用
std::string
变量
您需要一个可以修改的字符串。
您需要存储用户输入的文本。
您需要存储返回
std::string
的函数的返回值。
在以下情况下使用
std::string_view
变量
您需要对已存在于其他地方且在使用
std::string_view
完成之前不会被修改或销毁的字符串的全部或部分进行只读访问。
您需要 C 风格字符串的符号常量。
您需要继续查看返回 C 风格字符串或非悬空
std::string_view
的函数的返回值。
函数参数
在以下情况下使用
std::string
函数参数
函数需要修改作为参数传入的字符串而不影响调用者。这种情况很少见。
您正在使用 C++14 或更早的语言标准，并且尚不习惯使用引用。
在以下情况下使用
std::string_view
函数参数
函数需要一个只读字符串。
函数需要处理非空终止字符串。
致进阶读者
另请参阅
12.6 -- 按 const 左值引用传递
。
在以下情况下使用
const std::string&
函数参数
您正在使用 C++14 或更旧的语言标准，并且函数需要一个只读字符串来处理（因为
std::string_view
在 C++17 之前不可用）。
您正在调用需要
const std::string
、
const std::string&
或 const C 风格字符串的其他函数（因为
std::string_view
可能未以空字符结尾）。
在以下情况下使用
std::string&
函数参数
您将
std::string
用作输出参数（参见
12.13 -- 输入和输出参数
）。
您正在调用需要
std::string&
或非 const C 风格字符串的其他函数。
返回类型
在以下情况下使用
std::string
返回类型
返回值为
std::string
局部变量或函数参数。
返回值为按值返回
std::string
的函数调用或运算符。
在以下情况下使用
std::string_view
返回类型
函数返回 C 风格字符串字面量或已用 C 风格字符串字面量初始化的局部
std::string_view
。
函数返回
std::string_view
参数。
致进阶读者
有关返回引用类型的更多信息，请参阅课程
12.12 -- 按引用返回和按地址返回
。
在以下情况下使用
std::string_view
返回类型
为
std::string_view
成员编写访问器。
在以下情况下使用
std::string&
返回类型
函数返回
std::string&
参数。
在以下情况下使用
const std::string&
返回类型
函数返回
const std::string&
参数。
为
std::string
或
const std::string
成员编写访问器。
函数返回静态（局部或全局）
const std::string
。
见解
关于
std::string
需要记住的事情
初始化和复制
std::string
是昂贵的，因此尽可能避免。
避免按值传递
std::string
，因为这会创建副本。
如果可能，避免创建短生命周期的
std::string
对象。
修改
std::string
将使所有对该字符串的视图失效。
按值返回局部
std::string
是可以的。
关于
std::string_view
需要记住的事情
std::string_view
通常用于传递字符串函数参数和返回字符串字面量。
因为 C 风格字符串字面量在整个程序中都存在，所以将
std::string_view
设置为 C 风格字符串字面量总是可以的。
当一个字符串被销毁时，所有对该字符串的视图都会失效。
使用失效的视图（除了使用赋值来重新验证视图之外）将导致未定义行为。
std::string_view
可能以空字符结尾，也可能不以空字符结尾。
下一课
5.x
第 5 章总结和测验
返回目录
上一课
5.8
std::string_view 简介