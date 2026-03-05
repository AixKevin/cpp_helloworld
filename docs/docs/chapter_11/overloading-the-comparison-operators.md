# 21.7 — 重载比较运算符

21.7 — 重载比较运算符
Alex
2007 年 10 月 4 日，下午 5:10 PDT
2024 年 2 月 7 日
在课程
6.7 -- 关系运算符和浮点比较
中，我们讨论了六个比较运算符。重载这些比较运算符相对简单（看到我做了什么吗？），因为它们遵循我们重载其他运算符时看到的相同模式。
因为比较运算符都是二元运算符，并且不修改其左操作数，所以我们将把重载的比较运算符设为友元函数。
这是一个带有重载的 operator== 和 operator!= 的 Car 类示例。
#include <iostream>
#include <string>
#include <string_view>

class Car
{
private:
    std::string m_make;
    std::string m_model;

public:
    Car(std::string_view make, std::string_view model)
        : m_make{ make }, m_model{ model }
    {
    }

    friend bool operator== (const Car& c1, const Car& c2);
    friend bool operator!= (const Car& c1, const Car& c2);
};

bool operator== (const Car& c1, const Car& c2)
{
    return (c1.m_make == c2.m_make &&
            c1.m_model == c2.m_model);
}

bool operator!= (const Car& c1, const Car& c2)
{
    return (c1.m_make != c2.m_make ||
            c1.m_model != c2.m_model);
}

int main()
{
    Car corolla{ "Toyota", "Corolla" };
    Car camry{ "Toyota", "Camry" };

    if (corolla == camry)
        std::cout << "a Corolla and Camry are the same.\n";

    if (corolla != camry)
        std::cout << "a Corolla and Camry are not the same.\n";

    return 0;
}
这里的代码应该很简单。
那 operator< 和 operator> 呢？一辆汽车比另一辆汽车大或小是什么意思？我们通常不会这样考虑汽车。由于 operator< 和 operator> 的结果不会立即直观，最好将这些运算符保持未定义状态。
最佳实践
只定义对你的类有直观意义的重载运算符。
然而，上述建议有一个常见的例外。如果我们想对汽车列表进行排序怎么办？在这种情况下，我们可能希望重载比较运算符以返回你最可能希望进行排序的成员（或多个成员）。例如，用于汽车的重载 operator< 可能会根据品牌和型号按字母顺序排序。
标准库中的一些容器类（包含其他类的集合的类）需要重载 operator<，以便它们可以保持元素排序。
这是一个重载所有 6 个逻辑比较运算符的不同示例
#include <iostream>

class Cents
{
private:
    int m_cents;
 
public:
    Cents(int cents)
	: m_cents{ cents }
	{}
 
    friend bool operator== (const Cents& c1, const Cents& c2);
    friend bool operator!= (const Cents& c1, const Cents& c2);

    friend bool operator< (const Cents& c1, const Cents& c2);
    friend bool operator> (const Cents& c1, const Cents& c2);

    friend bool operator<= (const Cents& c1, const Cents& c2);
    friend bool operator>= (const Cents& c1, const Cents& c2);
};

bool operator== (const Cents& c1, const Cents& c2)
{
    return c1.m_cents == c2.m_cents;
}

bool operator!= (const Cents& c1, const Cents& c2)
{
    return c1.m_cents != c2.m_cents;
}

bool operator> (const Cents& c1, const Cents& c2)
{
    return c1.m_cents > c2.m_cents;
}

bool operator< (const Cents& c1, const Cents& c2)
{
    return c1.m_cents < c2.m_cents;
}

bool operator<= (const Cents& c1, const Cents& c2)
{
    return c1.m_cents <= c2.m_cents;
}

bool operator>= (const Cents& c1, const Cents& c2)
{
    return c1.m_cents >= c2.m_cents;
}

int main()
{
    Cents dime{ 10 };
    Cents nickel{ 5 };
 
    if (nickel > dime)
        std::cout << "a nickel is greater than a dime.\n";
    if (nickel >= dime)
        std::cout << "a nickel is greater than or equal to a dime.\n";
    if (nickel < dime)
        std::cout << "a dime is greater than a nickel.\n";
    if (nickel <= dime)
        std::cout << "a dime is greater than or equal to a nickel.\n";
    if (nickel == dime)
        std::cout << "a dime is equal to a nickel.\n";
    if (nickel != dime)
        std::cout << "a dime is not equal to a nickel.\n";

    return 0;
}
这也非常简单。
最小化比较冗余
在上面的示例中，请注意每个重载比较运算符的实现是多么相似。重载比较运算符往往具有高度的冗余，实现越复杂，冗余就越多。
幸运的是，许多比较运算符可以使用其他比较运算符来实现
operator!= 可以实现为 !(operator==)
operator> 可以实现为 operator<，参数顺序颠倒
operator>= 可以实现为 !(operator<)
operator<= 可以实现为 !(operator>)
这意味着我们只需要为 operator== 和 operator< 实现逻辑，然后其他四个比较运算符就可以用这两个运算符来定义！这是一个更新的 Cents 示例，说明了这一点
#include <iostream>

class Cents
{
private:
    int m_cents;

public:
    Cents(int cents)
        : m_cents{ cents }
    {}

    friend bool operator== (const Cents& c1, const Cents& c2) { return c1.m_cents == c2.m_cents; }
    friend bool operator!= (const Cents& c1, const Cents& c2) { return !(operator==(c1, c2)); }

    friend bool operator< (const Cents& c1, const Cents& c2) { return c1.m_cents < c2.m_cents; }
    friend bool operator> (const Cents& c1, const Cents& c2) { return operator<(c2, c1); }

    friend bool operator<= (const Cents& c1, const Cents& c2) { return !(operator>(c1, c2)); }
    friend bool operator>= (const Cents& c1, const Cents& c2) { return !(operator<(c1, c2)); }

};

int main()
{
    Cents dime{ 10 };
    Cents nickel{ 5 };

    if (nickel > dime)
        std::cout << "a nickel is greater than a dime.\n";
    if (nickel >= dime)
        std::cout << "a nickel is greater than or equal to a dime.\n";
    if (nickel < dime)
        std::cout << "a dime is greater than a nickel.\n";
    if (nickel <= dime)
        std::cout << "a dime is greater than or equal to a nickel.\n";
    if (nickel == dime)
        std::cout << "a dime is equal to a nickel.\n";
    if (nickel != dime)
        std::cout << "a dime is not equal to a nickel.\n";

    return 0;
}
这样，如果我们需要更改任何内容，我们只需要更新 operator== 和 operator<，而不是所有六个比较运算符！
飞船运算符 <=>
C++20
C++20 引入了飞船运算符 (
operator<=>
)，它允许我们将需要编写的比较函数数量最多减少到 2 个，有时甚至只剩下 1 个！
作者注
我们打算很快就这个话题增加一堂新课。在此之前，请将此视为激发你兴趣的东西——但你必须去其他网站才能发现更多。
小测验时间
将六个比较运算符添加到 Fraction 类中，以便以下程序能够编译
#include <iostream>
#include <numeric> // for std::gcd

class Fraction
{
private:
	int m_numerator{};
	int m_denominator{};

public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
		// We put reduce() in the constructor to ensure any new fractions we make get reduced!
		// Any fractions that are overwritten will need to be re-reduced
		reduce();
	}

	void reduce()
	{
		int gcd{ std::gcd(m_numerator, m_denominator) };
		if (gcd)
		{
			m_numerator /= gcd;
			m_denominator /= gcd;
		}
	}

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

int main()
{
	Fraction f1{ 3, 2 };
	Fraction f2{ 5, 8 };

	std::cout << f1 << ((f1 == f2) ? " == " : " not == ") << f2 << '\n';
	std::cout << f1 << ((f1 != f2) ? " != " : " not != ") << f2 << '\n';
	std::cout << f1 << ((f1 < f2) ? " < " : " not < ") << f2 << '\n';
	std::cout << f1 << ((f1 > f2) ? " > " : " not > ") << f2 << '\n';
	std::cout << f1 << ((f1 <= f2) ? " <= " : " not <= ") << f2 << '\n';
	std::cout << f1 << ((f1 >= f2) ? " >= " : " not >= ") << f2 << '\n';
	return 0;
}
如果你使用的是 C++17 之前的编译器，可以将 std::gcd 替换为此函数
#include <cmath>
 
int gcd(int a, int b) {
    return (b == 0) ? std::abs(a) : gcd(b, a % b);
}
显示答案
#include <iostream>
#include <numeric> // for std::gcd

class Fraction
{
private:
	int m_numerator{};
	int m_denominator{};

public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
		// We put reduce() in the constructor to ensure any new fractions we make get reduced!
		// Any fractions that are overwritten will need to be re-reduced
		reduce();
	}

	void reduce()
	{
		int gcd{ std::gcd(m_numerator, m_denominator) };
		if (gcd)
		{
			m_numerator /= gcd;
			m_denominator /= gcd;
		}
	}

	friend bool operator== (const Fraction& f1, const Fraction& f2);
	friend bool operator!= (const Fraction& f1, const Fraction& f2);

	friend bool operator< (const Fraction& f1, const Fraction& f2);
	friend bool operator> (const Fraction& f1, const Fraction& f2);

	friend bool operator<= (const Fraction& f1, const Fraction& f2);
	friend bool operator>= (const Fraction& f1, const Fraction& f2);

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

bool operator== (const Fraction& f1, const Fraction& f2)
{
	return (f1.m_numerator == f2.m_numerator) && (f1.m_denominator == f2.m_denominator);
}

bool operator!= (const Fraction& f1, const Fraction& f2)
{
	return !(operator==(f1, f2));
}

bool operator< (const Fraction& f1, const Fraction& f2)
{
	return (f1.m_numerator * f2.m_denominator < f2.m_numerator * f1.m_denominator);
}

bool operator> (const Fraction& f1, const Fraction& f2)
{
	return operator<(f2, f1);
}

bool operator<= (const Fraction& f1, const Fraction& f2)
{
	return !(operator>(f1, f2));
}

bool operator>= (const Fraction& f1, const Fraction& f2)
{
	return !(operator<(f1, f2));
}

int main()
{
	Fraction f1{ 3, 2 };
	Fraction f2{ 5, 8 };

	std::cout << f1 << ((f1 == f2) ? " == " : " not == ") << f2 << '\n';
	std::cout << f1 << ((f1 != f2) ? " != " : " not != ") << f2 << '\n';
	std::cout << f1 << ((f1 < f2) ? " < " : " not < ") << f2 << '\n';
	std::cout << f1 << ((f1 > f2) ? " > " : " not > ") << f2 << '\n';
	std::cout << f1 << ((f1 <= f2) ? " <= " : " not <= ") << f2 << '\n';
	std::cout << f1 << ((f1 >= f2) ? " >= " : " not >= ") << f2 << '\n';

	return 0;
}
将重载的 operator<< 和 operator< 添加到课程顶部的 Car 类中，以便以下程序能够编译
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main()
{
  std::vector<Car> cars{
    { "Toyota", "Corolla" },
    { "Honda", "Accord" },
    { "Toyota", "Camry" },
    { "Honda", "Civic" }
  };

  std::sort(cars.begin(), cars.end()); // requires an overloaded operator<

  for (const auto& car : cars)
    std::cout << car << '\n'; // requires an overloaded operator<<

  return 0;
}
此程序应生成以下输出
(Honda, Accord)
(Honda, Civic)
(Toyota, Camry)
(Toyota, Corolla)
如果您需要回顾 std::sort，我们在课程
18.1 -- 使用选择排序对数组进行排序
中讨论过它。
显示答案
#include <algorithm>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Car
{
private:
    std::string m_make;
    std::string m_model;

public:
    Car(std::string_view make, std::string_view model)
        : m_make{ make }, m_model{ model }
    {
    }

    friend bool operator==(const Car& c1, const Car& c2);
    friend bool operator!=(const Car& c1, const Car& c2);

    friend std::ostream& operator<<(std::ostream& out, const Car& c)
    {
        out << '(' << c.m_make << ", " << c.m_model << ')';
        return out;
    }

    // h/t to reader Olivier for the initial version of the function
    friend bool operator<(const Car& c1, const Car& c2)
    {
        if (c1.m_make != c2.m_make) // If the car is not the same make...
            return c1.m_make < c2.m_make; // ...then compare the make

        return c1.m_model < c2.m_model; // otherwise compare the model
    }
};

bool operator==(const Car& c1, const Car& c2)
{
    return c1.m_make == c2.m_make && c1.m_model == c2.m_model;
}

bool operator!= (const Car& c1, const Car& c2)
{
    return !operator==(c1, c2);
}

int main()
{
    std::vector<Car> cars{
      { "Toyota", "Corolla" },
      { "Honda", "Accord" },
      { "Toyota", "Camry" },
      { "Honda", "Civic" }
    };

    std::sort(cars.begin(), cars.end()); // requires an overloaded Car::operator<

    for (const auto& car : cars)
        std::cout << car << '\n'; // requires an overloaded Car::operator<<

    return 0;
}
下一课
21.8
重载递增和递减运算符
返回目录
上一课
21.6
重载一元运算符 +, -, 和 !