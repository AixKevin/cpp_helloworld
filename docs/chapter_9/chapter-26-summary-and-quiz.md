# 26.x — 第 26 章总结与测验

26.x — 第 26 章总结与测验
Alex
2016 年 12 月 19 日，太平洋标准时间下午 2:07
2023 年 9 月 11 日
模板允许我们使用占位符类型编写函数或类，这样我们就可以使用不同的类型“模板化”出相同版本的函数或类。已被实例化的函数或类称为函数实例或类实例。
所有模板函数或类都必须以模板参数声明开头，该声明告诉编译器后续的函数或类是模板函数或类。在模板参数声明中，指定模板类型参数或表达式参数。模板类型参数只是占位符类型，通常命名为 T、T1、T2 或其他单个字母名称（例如 S）。表达式参数通常是整型，但可以是函数、类对象或成员函数的指针或引用。
拆分模板类定义和成员函数定义不像普通类那样工作——你不能将类定义放在头文件中，将成员函数定义放在 .cpp 文件中。通常最好将它们都放在头文件中，成员函数定义放在类定义下方。
当我们需要为特定类型覆盖模板函数或类的默认行为时，可以使用模板特化。如果所有类型都被覆盖，则称为完全特化。类还支持部分特化，即只特化部分模板参数。函数不能部分特化。
C++ 标准库中的许多类都使用模板，包括 std::array 和 std::vector。模板通常用于实现容器类，因此容器可以编写一次并与任何适当的类型一起使用。
小测验时间
有时定义成对的数据很有用。编写一个名为 Pair1 的模板类，允许用户定义一个模板类型，该类型用于这对值中的两个值。以下函数应该可以工作
int main()
{
	Pair1<int> p1 { 5, 8 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair1<double> p2 { 2.3, 4.5 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
并打印
Pair: 5 8
Pair: 2.3 4.5
显示答案
#include <iostream>

template <typename T>
class Pair1
{
private:
	T m_x {};
	T m_y {};

public:
	Pair1(const T& x, const T& y)
		: m_x{ x }, m_y{ y }
	{
	}

	T& first() { return m_x; }
	T& second() { return m_y; }
	const T& first() const { return m_x; }
	const T& second() const { return m_y; }
};

int main()
{
	Pair1<int> p1 { 5, 8 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair1<double> p2 { 2.3, 4.5 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
编写一个 Pair 类，允许您为这对值中的两个值指定单独的类型。
注意：我们将此类与前一个类命名不同，因为 C++ 当前不允许您“重载”仅在模板参数数量或类型上有所不同的类。
以下程序应该可以工作
int main()
{
	Pair<int, double> p1 { 5, 6.7 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair<double, int> p2 { 2.3, 4 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
并打印
Pair: 5 6.7
Pair: 2.3 4
提示：要使用两种不同的类型定义模板，请在模板参数声明中用逗号分隔这两种类型。有关更多信息，请参阅第
11.8 课——具有多个模板类型的函数模板
。
显示答案
#include <iostream>

template <typename T, typename S>
class Pair
{
private:
	T m_x;
	S m_y;

public:
	Pair(const T& x, const S& y)
		: m_x{x}, m_y{y}
	{
	}

	T& first() { return m_x; }
	S& second() { return m_y; }
	const T& first() const { return m_x; }
	const S& second() const { return m_y; }
};

int main()
{
	Pair<int, double> p1 { 5, 6.7 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair<double, int> p2 { 2.3, 4 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
字符串值对是一种特殊类型的对，其中第一个值始终是字符串类型，第二个值可以是任何类型。编写一个名为 StringValuePair 的模板类，该类继承自部分特化的 Pair 类（使用 std::string 作为第一个类型，并允许用户指定第二个类型）。
以下程序应该运行
int main()
{
	StringValuePair<int> svp { "Hello", 5 };
	std::cout << "Pair: " << svp.first() << ' ' << svp.second() << '\n';

	return 0;
}
并打印
Pair: Hello 5
提示：当您从 StringValuePair 构造函数调用 Pair 构造函数时，不要忘记将模板参数作为 Pair 类名的一部分。
显示答案
#include <iostream>
#include <string>
#include <string_view>

template <typename T, typename S>
class Pair
{
private:
	T m_x{};
	S m_y{};

public:
	Pair(const T& x, const S& y)
		: m_x{ x }, m_y{ y }
	{
	}

	T& first() { return m_x; }
	S& second() { return m_y; }
	const T& first() const { return m_x; }
	const S& second() const { return m_y; }
};

template <typename S>
class StringValuePair : public Pair<std::string, S>
{
public:
	StringValuePair(std::string_view key, const S& value)
                // a std::string_view won't implicitly convert to a std::string, we must be explicit
		: Pair<std::string, S>{ static_cast<std::string>(key), value }
	{
	}
};

int main()
{
	StringValuePair<int> svp{ "Hello", 5 };
	std::cout << "Pair: " << svp.first() << ' ' << svp.second() << '\n';

	return 0;
}
下一课
27.1
异常的必要性
返回目录
上一课
26.6
指针的部分模板特化