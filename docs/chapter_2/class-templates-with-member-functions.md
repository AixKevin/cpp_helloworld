# 15.5 — 带有成员函数的类模板

15.5 — 带有成员函数的类模板
Alex
2023 年 9 月 11 日下午 12:59 PDT
2024 年 8 月 6 日
在
11.6 -- 函数模板
这一课中，我们了解了函数模板。
template <typename T> // this is the template parameter declaration
T max(T x, T y) // this is the function template definition for max<T>
{
    return (x < y) ? y : x;
}
通过函数模板，我们可以定义类型模板参数（例如
typename T
），然后将它们用作函数参数的类型（
T x, T y
）。
在
13.13 -- 类模板
这一课中，我们介绍了类模板，它允许我们使用类型模板参数作为类类型（struct、class 和 union）的数据成员的类型。
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// Here's a deduction guide for our Pair (required in C++17 or older)
// Pair objects initialized with arguments of type T and T should deduce to Pair<T>
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 5, 6 };        // instantiates Pair<int> and creates object p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // instantiates Pair<double> and creates object p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // creates object p3 using prior definition for Pair<double>
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
相关内容
我们在
13.14 -- 类模板参数推导（CTAD）和推导指南
这一课中讨论了推导指南。
在本课中，我们将结合函数模板和类模板的元素，更深入地研究带有成员函数的类模板。
成员函数中的类型模板参数
作为类模板参数声明一部分定义的类型模板参数，既可以用于数据成员的类型，也可以用于成员函数参数的类型。
在下面的例子中，我们重写了上面的
Pair
类模板，将其从 struct 转换为 class。
#include <ios>       // for std::boolalpha
#include <iostream>

template <typename T>
class Pair
{
private:
    T m_first{};
    T m_second{};

public:
    // When we define a member function inside the class definition,
    // the template parameter declaration belonging to the class applies
    Pair(const T& first, const T& second)
        : m_first{ first }
        , m_second{ second }
    {
    }

    bool isEqual(const Pair<T>& pair);
};

// When we define a member function outside the class definition,
// we need to resupply a template parameter declaration
template <typename T>
bool Pair<T>::isEqual(const Pair<T>& pair)
{
    return m_first == pair.m_first && m_second == pair.m_second;
}

int main()
{
    Pair p1{ 5, 6 }; // uses CTAD to infer type Pair<int>
    std::cout << std::boolalpha << "isEqual(5, 6): " << p1.isEqual( Pair{5, 6} ) << '\n';
    std::cout << std::boolalpha << "isEqual(5, 7): " << p1.isEqual( Pair{5, 7} ) << '\n';

    return 0;
}
上面应该很简单，但有几点值得注意。
首先，由于我们的类有私有成员，它不是一个聚合体，因此不能使用聚合初始化。相反，我们必须使用构造函数来初始化我们的类对象。
由于我们的类数据成员的类型是
T
，我们将构造函数的参数类型设置为
const T&
，这样用户可以提供相同类型的初始化值。因为
T
复制起来可能很昂贵，所以通过 const 引用传递比通过值传递更安全。
请注意，当我们在类模板定义内部定义成员函数时，我们不需要为成员函数提供模板参数声明。此类成员函数隐式使用类模板参数声明。
其次，我们不需要推导指南来使 CTAD 与非聚合类一起工作。匹配的构造函数为编译器提供了从初始化器推导模板参数所需的信息。
第三，让我们更仔细地看看在类模板定义之外定义类模板成员函数的情况。
template <typename T>
bool Pair<T>::isEqual(const Pair<T>& pair)
{
    return m_first == pair.m_first && m_second == pair.m_second;
}
由于此成员函数定义与类模板定义是分开的，我们需要重新提供模板参数声明（
template <typename T>
），以便编译器知道
T
是什么。
此外，当我们在类之外定义成员函数时，我们需要使用类模板的完全模板化名称来限定成员函数名（
Pair<T>::isEqual
，而不是
Pair::isEqual
）。
注入类名
在之前的课程中，我们提到构造函数的名称必须与类的名称匹配。但在上面
Pair<T>
的类模板中，我们将构造函数命名为
Pair
，而不是
Pair<T>
。尽管名称不匹配，但它仍然有效。
在类的作用域内，类的非限定名称被称为**注入类名**。在类模板中，注入类名充当完全模板化名称的简写。
因为
Pair
是
Pair<T>
的注入类名，所以在
Pair<T>
类模板的作用域内，任何使用
Pair
的地方都将被视为我们写了
Pair<T>
。因此，尽管我们将构造函数命名为
Pair
，但编译器将其视为我们写了
Pair<T>
。现在名称匹配了！
这意味着我们也可以这样定义
isEqual()
成员函数：
template <typename T>
bool Pair<T>::isEqual(const Pair& pair) // note the parameter has type Pair, not Pair<T>
{
    return m_first == pair.m_first && m_second == pair.m_second;
}
因为这是
Pair<T>
的成员函数定义，我们处于
Pair<T>
类模板的作用域内。因此，任何使用
Pair
的地方都是
Pair<T>
的简写！
关键见解
在
13.14 -- 类模板参数推导（CTAD）和推导指南
这一课中，我们注意到 CTAD 不适用于函数参数（因为它属于参数推导，而不是类型参数推导）。然而，将注入类名用作函数参数是可以的，因为它是完全模板化名称的简写，而不是 CTAD 的使用。
在类外部定义类模板成员函数的位置
对于类模板的成员函数，编译器需要同时看到类定义（以确保成员函数模板被声明为类的一部分）和模板成员函数定义（以知道如何实例化模板）。因此，我们通常希望在同一位置定义类及其成员函数模板。
当成员函数模板在类定义**内部**定义时，模板成员函数定义是类定义的一部分，因此在任何可以看到类定义的地方，也可以看到模板成员函数定义。这使得事情变得容易（代价是使我们的类定义变得混乱）。
当成员函数模板在类定义**外部**定义时，通常应将其定义在类定义紧下方。这样，在任何可以看到类定义的地方，紧随类定义之后的成员函数模板定义也将被看到。
在类通常在头文件中定义的情况下，这意味着在类外部定义的任何成员函数模板也应在同一头文件中、类定义下方进行定义。
关键见解
在
11.7 -- 函数模板实例化
这一课中，我们注意到从模板隐式实例化的函数是隐式内联的。这包括非成员函数和成员函数模板。因此，将头文件中定义的成员函数模板包含到多个代码文件中没有问题，因为从这些模板实例化的函数将是隐式内联的（并且链接器将对其进行去重）。
最佳实践
在类定义之外定义的任何成员函数模板都应紧邻类定义下方（在同一文件中）进行定义。
小测验时间
问题 #1
编写一个名为 `Triad` 的类模板，它有 3 个具有独立类型模板参数的私有数据成员。该类应该有一个构造函数、访问函数和一个在类外部定义的 `print()` 成员函数。
以下程序应该编译并运行
#include <iostream>
#include <string>

int main()
{
	Triad<int, int, int> t1{ 1, 2, 3 };
	t1.print();
	std::cout << '\n';
	std::cout << t1.first() << '\n';

	using namespace std::literals::string_literals;
	const Triad t2{ 1, 2.3, "Hello"s };
	t2.print();
	std::cout << '\n';

	return 0;
}
并产生输出
[1, 2, 3]
1
[1, 2.3, Hello]
显示答案
#include <iostream>
#include <string>

template <typename T, typename U, typename V>
class Triad
{
private:
	T m_first{};
	U m_second{};
	V m_third{};

public:
	Triad(const T& first, const U& second, const V& third)
		: m_first{ first }
		, m_second{ second }
		, m_third{ third }
	{
	}

	const T& first() const { return m_first; }
	const U& second() const { return m_second; }
	const V& third() const { return m_third; }

	void print() const;
};

template <typename T, typename U, typename V>
void Triad<T, U, V>::print() const
{
	std::cout << '[' << m_first << ", " << m_second << ", " << m_third << ']' ;
}

int main()
{
	Triad<int, int, int> t1{ 1, 2, 3 };
	t1.print();
	std::cout << '\n';
	std::cout << t1.first() << '\n';

	using namespace std::literals::string_literals;
	const Triad t2{ 1, 2.3, "Hello"s };
	t2.print();
	std::cout << '\n';

	return 0;
}
问题 #2
如果我们将
print()
函数声明和定义中的
const
删除，程序将不再编译。为什么会这样？
显示答案
t2
是一个 const 对象，因此只能对
t2
调用 const 成员函数。如果我们将
print()
设为非 const 成员函数，那么
t2
将不允许调用它。这是因为非 const 成员函数可能会修改隐式对象，这将违反 const 对象的常量性（在这种情况下是
t2
）。
下一课
15.6
静态成员变量
返回目录
上一课
15.4
析构函数简介