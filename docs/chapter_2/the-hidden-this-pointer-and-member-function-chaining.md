# 15.1 — 隐藏的“this”指针和成员函数链式调用

15.1 — 隐藏的“this”指针和成员函数链式调用
Alex
2007 年 9 月 6 日，上午 10:20 PDT
2024 年 12 月 29 日
新程序员经常会问关于类的一个问题是：“当成员函数被调用时，C++ 如何追踪它是哪个对象调用的？”。
首先，让我们定义一个简单的类来操作。这个类封装了一个整数值，并提供了一些访问函数来获取和设置该值。
#include <iostream>

class Simple
{
private:
    int m_id{};
 
public:
    Simple(int id)
        : m_id{ id }
    {
    }

    int getID() const { return m_id; }
    void setID(int id) { m_id = id; }

    void print() const { std::cout << m_id; }
};

int main()
{
    Simple simple{1};
    simple.setID(2);

    simple.print();

    return 0;
}
正如你所预料的，这个程序会产生以下结果：
2
不知何故，当我们调用
simple.setID(2);
时，C++ 知道函数
setID()
应该操作对象
simple
，并且
m_id
实际上指的是
simple.m_id
。
答案是 C++ 使用了一个名为
this
的隐藏指针！在本课中，我们将更详细地探讨
this
。
隐藏的
this
指针
在每个成员函数内部，关键字
this
是一个 const 指针，它保存着当前隐式对象的地址。
大多数情况下，我们不会明确提及
this
，但为了证明我们可以这样做：
#include <iostream>

class Simple
{
private:
    int m_id{};

public:
    Simple(int id)
        : m_id{ id }
    {
    }

    int getID() const { return m_id; }
    void setID(int id) { m_id = id; }

    void print() const { std::cout << this->m_id; } // use `this` pointer to access the implicit object and operator-> to select member m_id
};

int main()
{
    Simple simple{ 1 };
    simple.setID(2);
    
    simple.print();

    return 0;
}
这与之前的例子完全相同，并打印出：
2
请注意，前两个示例中的
print()
成员函数执行的操作完全相同：
void print() const { std::cout << m_id; }       // implicit use of this
    void print() const { std::cout << this->m_id; } // explicit use of this
事实证明，前者是后者的简写。当我们编译程序时，编译器会隐式地将任何引用隐式对象的成员前面加上
this->
。这有助于使我们的代码更简洁，并避免了必须一遍又一遍地显式写入
this->
的冗余。
提醒
我们使用
->
从对象的指针中选择成员。
this->m_id
等同于
(*this).m_id
。
我们在第
13.12 课 -- 使用指针和引用进行成员选择
中介绍了
operator->
。
this
是如何设置的？
让我们仔细看看这个函数调用：
simple.setID(2);
尽管对函数
setID(2)
的调用看起来只有一个参数，但它实际上有两个！编译时，编译器将表达式
simple.setID(2);
重写如下：
Simple::setID(&simple, 2); // note that simple has been changed from an object prefix to a function argument!
请注意，这现在只是一个标准的函数调用，对象
simple
（以前是对象前缀）现在以地址形式作为参数传递给函数。
但这只是答案的一半。由于函数调用现在增加了一个参数，成员函数定义也需要修改以接受（和使用）这个参数。这是我们
setID()
的原始成员函数定义：
void setID(int id) { m_id = id; }
编译器如何重写函数是实现细节，但最终结果类似于这样：
static void setID(Simple* const this, int id) { this->m_id = id; }
注意，我们的
setId
函数有一个新的最左侧参数，名为
this
，它是一个 const 指针（这意味着它不能重新指向，但指针的内容可以修改）。
m_id
成员也被重写为
this->m_id
，使用了
this
指针。
致进阶读者
在此上下文中，
static
关键字表示该函数不与类的对象关联，而是被视为类作用域区域内的普通函数。我们在第
15.7 课 -- 静态成员函数
中介绍了静态成员函数。
总结一下
当我们调用
simple.setID(2)
时，编译器实际上调用
Simple::setID(&simple, 2)
，并且
simple
以地址传递给函数。
该函数有一个名为
this
的隐藏参数，它接收
simple
的地址。
setID()
内部的成员变量都带有
this->
前缀，它指向
simple
。所以当编译器评估
this->m_id
时，它实际上解析为
simple.m_id
。
好消息是所有这些都是自动发生的，你是否记住它的工作原理并不重要。你只需要记住所有非静态成员函数都有一个
this
指针，它指向调用该函数的对象。
关键见解
所有非静态成员函数都有一个
this
const 指针，它保存着隐式对象的地址。
this
始终指向正在操作的对象
新程序员有时会混淆有多少个
this
指针存在。每个成员函数都有一个指向隐式对象的
this
指针参数。考虑：
int main()
{
    Simple a{1}; // this = &a inside the Simple constructor
    Simple b{2}; // this = &b inside the Simple constructor
    a.setID(3); // this = &a inside member function setID()
    b.setID(4); // this = &b inside member function setID()

    return 0;
}
请注意，
this
指针交替地持有对象
a
或
b
的地址，具体取决于我们是在对象
a
还是
b
上调用了成员函数。
因为
this
只是一个函数参数（而不是成员），它不会在内存上使你的类的实例变大。
显式引用
this
大多数情况下，你不需要显式引用
this
指针。然而，在某些情况下，这样做会很有用：
首先，如果你的成员函数有一个与数据成员同名的参数，你可以通过使用
this
来消除歧义：
struct Something
{
    int data{}; // not using m_ prefix because this is a struct

    void setData(int data)
    {
        this->data = data; // this->data is the member, data is the local parameter
    }
};
这个
Something
类有一个名为
data
的成员。
setData()
函数的参数也名为
data
。在
setData()
函数中，
data
指的是函数参数（因为函数参数会遮蔽数据成员），所以如果我们想引用
data
成员，我们使用
this->data
。
一些开发者喜欢显式地将
this->
添加到所有类成员前面，以明确它们引用的是成员。我们建议你避免这样做，因为它往往会降低代码的可读性，收益甚微。使用“m_”前缀是一种更简洁的方式来区分私有成员变量和非成员（局部）变量。
返回
*this
其次，有时让成员函数将隐式对象作为返回值返回会很有用。这样做的主要原因是允许成员函数“链式调用”，这样可以在一个表达式中对同一个对象调用多个成员函数！这被称为
函数链式调用
（或
方法链式调用
）。
考虑这个常见的例子，你使用
std::cout
输出多段文本：
std::cout << "Hello, " << userName;
编译器会这样评估上面的代码片段：
(std::cout << "Hello, ") << userName;
首先，
operator<<
使用
std::cout
和字符串字面量
"Hello, "
将
"Hello, "
打印到控制台。然而，由于这是表达式的一部分，
operator<<
也需要返回一个值（或
void
）。如果
operator<<
返回
void
，你将得到以下部分评估的表达式：
void{} << userName;
这显然没有任何意义（并且编译器会抛出错误）。相反，
operator<<
返回传入的流对象，在本例中是
std::cout
。这样，在第一个
operator<<
评估之后，我们得到：
(std::cout) << userName;
然后打印用户的姓名。
通过这种方式，我们只需要指定
std::cout
一次，然后我们可以使用
operator<<
将任意数量的文本片段连接起来。每次调用
operator<<
都会返回
std::cout
，这样下一次调用
operator<<
就会将
std::cout
用作左操作数。
我们也可以在成员函数中实现这种行为。考虑以下类：
class Calc
{
private:
    int m_value{};

public:

    void add(int value) { m_value += value; }
    void sub(int value) { m_value -= value; }
    void mult(int value) { m_value *= value; }

    int getValue() const { return m_value; }
};
如果你想加 5，减 3，然后乘 4，你必须这样做：
#include <iostream>

int main()
{
    Calc calc{};
    calc.add(5); // returns void
    calc.sub(3); // returns void
    calc.mult(4); // returns void

    std::cout << calc.getValue() << '\n';

    return 0;
}
然而，如果我们将每个函数都返回
*this
的引用，我们就可以将调用链式连接起来。这是带有“可链式调用”函数的新版本
Calc
：
class Calc
{
private:
    int m_value{};

public:
    Calc& add(int value) { m_value += value; return *this; }
    Calc& sub(int value) { m_value -= value; return *this; }
    Calc& mult(int value) { m_value *= value; return *this; }

    int getValue() const { return m_value; }
};
注意，
add()
、
sub()
和
mult()
现在都通过引用返回
*this
。因此，这允许我们执行以下操作：
#include <iostream>

int main()
{
    Calc calc{};
    calc.add(5).sub(3).mult(4); // method chaining

    std::cout << calc.getValue() << '\n';

    return 0;
}
我们有效地将三行代码合并成一个表达式！让我们仔细看看它是如何工作的。
首先，调用
calc.add(5)
，它将
5
添加到
m_value
。然后
add()
返回对
*this
的引用，即对隐式对象
calc
的引用，因此
calc
将是后续评估中使用的对象。接下来，
calc.sub(3)
评估，它从
m_value
中减去
3
并再次返回
calc
。最后，
calc.mult(4)
将
m_value
乘以
4
并返回
calc
，它不再被使用，因此被忽略。
由于每个函数在执行时都修改了
calc
，现在
calc
的
m_value
包含值 (((0 + 5) - 3) * 4)，即
8
。
这可能是
this
最常见的显式用法，并且每当链式成员函数有意义时，都应该考虑使用它。
因为
this
总是指向隐式对象，所以我们在解引用它之前不需要检查它是否为空指针。
将类重置为默认状态
如果你的类有一个默认构造函数，你可能想提供一种方法将现有对象返回到其默认状态。
如前几课（
14.12 -- 委托构造函数
）所述，构造函数仅用于初始化新对象，不应直接调用。这样做会导致意外行为。
将类重置为默认状态的最佳方法是创建一个
reset()
成员函数，让该函数创建一个新对象（使用默认构造函数），然后将该新对象赋值给当前的隐式对象，如下所示：
void reset()
    {
        *this = {}; // value initialize a new object and overwrite the implicit object
    }
这是一个演示此
reset()
函数实际运行的完整程序：
#include <iostream>

class Calc
{
private:
    int m_value{};

public:
    Calc& add(int value) { m_value += value; return *this; }
    Calc& sub(int value) { m_value -= value; return *this; }
    Calc& mult(int value) { m_value *= value; return *this; }

    int getValue() const { return m_value; }

    void reset() { *this = {}; }
};


int main()
{
    Calc calc{};
    calc.add(5).sub(3).mult(4);

    std::cout << calc.getValue() << '\n'; // prints 8

    calc.reset();
    
    std::cout << calc.getValue() << '\n'; // prints 0

    return 0;
}
this
和 const 对象
对于非 const 成员函数，
this
是一个指向非 const 值的 const 指针（这意味着
this
不能指向其他东西，但指向的对象可以修改）。对于 const 成员函数，
this
是一个指向 const 值的 const 指针（这意味着指针不能指向其他东西，指向的对象也不能修改）。
尝试在 const 对象上调用非 const 成员函数时生成的错误可能有点晦涩难懂：
error C2662: 'int Something::getValue(void)': cannot convert 'this' pointer from 'const Something' to 'Something &'
error: passing 'const Something' as 'this' argument discards qualifiers [-fpermissive]
当我们对一个 const 对象调用非 const 成员函数时，隐式
this
函数参数是一个指向 *非 const* 对象的 const 指针。但是参数的类型是指向 *const* 对象的 const 指针。将指向 const 对象的指针转换为指向非 const 对象的指针需要丢弃 const 限定符，这不能隐式完成。某些编译器生成的编译错误反映了编译器抱怨被要求执行这种转换。
为什么
this
是指针而不是引用
由于
this
指针总是指向隐式对象（除非我们做了导致未定义行为的事情，否则它永远不会是空指针），你可能想知道为什么
this
是指针而不是引用。答案很简单：当
this
被添加到 C++ 时，引用还不存在。
如果
this
今天被添加到 C++ 语言中，它无疑将是一个引用而不是指针。在其他更现代的类 C++ 语言中，如 Java 和 C#，
this
被实现为引用。
下一课
15.2
类和头文件
返回目录
上一课
14.x
第 14 章总结和测验