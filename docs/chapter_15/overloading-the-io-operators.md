# 21.4 — 重载 I/O 运算符

21.4 — 重载 I/O 运算符
Alex
2007 年 10 月 1 日，下午 4:41 PDT
2025 年 1 月 29 日
对于具有多个成员变量的类，将每个单独的变量打印到屏幕上会很快变得乏味。例如，考虑以下类
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }
};
如果你想将这个类的实例打印到屏幕上，你必须这样做
Point point { 5.0, 6.0, 7.0 };

std::cout << "Point(" << point.getX() << ", " <<
    point.getY() << ", " <<
    point.getZ() << ')';
当然，将其作为可重用函数更有意义。在之前的示例中，你已经看到我们创建了像这样工作的
print()
函数
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }

    void print() const
    {
        std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ')';
    }
};
虽然这要好得多，但它仍然有一些缺点。因为
print()
返回
void
，所以它不能在输出语句中间调用。相反，你必须这样做
int main()
{
    const Point point { 5.0, 6.0, 7.0 };

    std::cout << "My point is: ";
    point.print();
    std::cout << " in Cartesian space.\n";
}
如果能简单地输入
Point point{5.0, 6.0, 7.0};
cout << "My point is: " << point << " in Cartesian space.\n";
并获得相同的结果，那会容易得多。这样就无需将输出分解为多个语句，也无需记住打印函数的名称。
幸运的是，通过重载
operator<<
，你可以做到！
重载
operator<<
重载
operator<<
类似于重载 operator+ (它们都是二元运算符)，只是参数类型不同。
考虑表达式
std::cout << point
。如果运算符是
<<
，那么操作数是什么？左操作数是
std::cout
对象，右操作数是你的
Point
类对象。
std::cout
实际上是
std::ostream
类型的一个对象。因此，我们的重载函数将如下所示
// std::ostream is the type for object std::cout
friend std::ostream& operator<< (std::ostream& out, const Point& point);
为我们的
Point
类实现
operator<<
非常简单——因为 C++ 已经知道如何使用
operator<<
输出双精度浮点数，并且我们的所有成员都是双精度浮点数，我们可以简单地使用
operator<<
来输出
Point
的数据成员。下面是上面带有重载
operator<<
的
Point
类。
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // Since operator<< is a friend of the Point class, we can access Point's members directly.
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')'; // actual output done here

    return out; // return std::ostream so we can chain calls to operator<<
}

int main()
{
    const Point point1 { 2.0, 3.0, 4.0 };

    std::cout << point1 << '\n';

    return 0;
}
这非常简单——注意我们的输出行与我们之前编写的
print()
函数中的行有多么相似。最显著的区别是
std::cout
变成了参数
out
（当函数被调用时，它将是
std::cout
的引用）。
这里最棘手的部分是返回类型。对于算术运算符，我们通过值计算并返回一个单一答案（因为我们正在创建并返回一个新结果）。但是，如果你尝试按值返回
std::ostream
，你将得到一个编译错误。这是因为
std::ostream
明确禁止被复制。
在这种情况下，我们将左侧参数作为引用返回。这不仅可以防止
std::ostream
的副本生成，还可以让我们“链式”地连接输出命令，例如
std::cout << point << '\n'
。
考虑一下如果我们的
operator<<
返回
void
会发生什么。当编译器评估
std::cout << point << '\n'
时，由于优先级/结合性规则，它将此表达式评估为
(std::cout << point) << '\n';
。
std::cout << point
将调用我们返回 void 的重载
operator<<
函数，该函数返回
void
。然后部分评估的表达式变为：
void << '\n';
，这没有任何意义！
通过将 `out` 参数作为返回类型返回，`(std::cout << point)` 返回 `std::cout`。然后我们部分求值的表达式变为：`std::cout << '\n';`，然后该表达式本身也会被求值！
任何时候我们希望重载的二元运算符以这种方式可链式调用时，都应该返回左操作数（通过引用）。在这种情况下，通过引用返回左侧参数是可以的——因为左侧参数是由调用函数传入的，所以当被调用函数返回时，它必须仍然存在。因此，我们不必担心引用在运算符返回时将超出作用域并被销毁的东西。
为了证明它有效，请考虑以下示例，该示例使用上面编写的带有重载
operator<<
的 Point 类
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // Since operator<< is a friend of the Point class, we can access Point's members directly.
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';

    return out;
}

int main()
{
    Point point1 { 2.0, 3.5, 4.0 };
    Point point2 { 6.0, 7.5, 8.0 };

    std::cout << point1 << ' ' << point2 << '\n';

    return 0;
}
这会产生以下结果
Point(2, 3.5, 4) Point(6, 7.5, 8)
在上面的例子中，
operator<<
是一个友元，因为它需要直接访问
Point
的成员。然而，如果可以通过 getter 访问成员，那么
operator<<
可以作为非友元实现。
重载
operator>>
还可以重载输入运算符。这与重载输出运算符的方式类似。你需要知道的关键是
std::cin
是
std::istream
类型的一个对象。下面是我们的
Point
类，并添加了重载的
operator>>
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
    friend std::istream& operator>> (std::istream& out, Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // Since operator<< is a friend of the Point class, we can access Point's members directly.
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';

    return out;
}

// note that point must be non-const so we can modify the object
std::istream& operator>> (std::istream& in, Point& point)
{
    // This version subject to partial extraction issues (see below)
    in >> point.m_x >> point.m_y >> point.m_z;

    return in;
}

int main()
{
    std::cout << "Enter a point: ";

    Point point{ 1.0, 2.0, 3.0 }; // non-zero test data
    std::cin >> point;

    std::cout << "You entered: " << point << '\n';

    return 0;
}
假设用户输入 `4.0 5.6 7.26`，程序将产生以下结果
You entered: Point(4, 5.6, 7.26)
现在让我们看看当用户输入
4.0b 5.6 7.26
时会发生什么（注意
4.0
后面的
b
）
You entered: Point(4, 0, 3)
我们的点现在是一个奇怪的混合体，由用户输入的一个值 (
4.0
)、一个已零初始化值 (
0.0
) 和一个未受输入函数影响的值 (
3.0
) 组成。这…不太好！
防止部分提取
当我们提取单个值时，只有两种可能的结果：提取失败或成功。然而，当我们在输入操作中提取多个值时，事情会变得有点复杂。
上述
operator>>
的实现可能导致部分提取。这正是我们在输入
4.0b 5.6 7.26
时所看到的。向
x_y
的提取成功地从用户输入中提取了
4.0
，在输入流中留下了
b 5.6 7.26
。向
m_y
的提取未能提取
b
，因此
m_y
被复制赋值为
0.0
，并且输入流被设置为失败模式。由于我们尚未清除失败模式，因此向
m_z
的提取立即中止，并且
m_z
在尝试提取之前的值仍然保留（
3.0
）。
在任何情况下，这都不是一个理想的结果。在某些情况下，它甚至可能主动危险。想象一下，我们正在为一个 `Fraction` 对象编写 `operator>>`。在成功提取分子后，对分母的失败提取会将分母设置为 `0.0`，这可能稍后导致除以零并导致应用程序崩溃。
那么我们如何避免这种情况呢？一种方法是使我们的操作具有事务性。**事务性操作**必须完全成功或完全失败——不允许部分成功或失败。这有时被称为“全有或全无”。如果在事务的任何一点发生故障，则必须撤销操作之前所做的更改。
关键见解
事务在现实生活中无处不在。考虑我想将钱从一个银行账户转到另一个银行账户的情况。这需要两个步骤：首先，必须从一个账户中扣除钱，然后必须将钱记入另一个账户。在执行此操作时，有三种可能性
扣款步骤失败（例如，资金不足）。交易失败，两个账户余额均未反映转账。
贷记步骤失败（例如，由于技术问题）。在这种情况下，必须撤销已成功完成的扣款。事务失败，两个账户余额均未反映转账。
两个步骤都成功。交易成功，两个账户余额都反映了转账。
最终结果是只有两种可能：转账完全失败，账户余额不变；或者转账成功，账户余额都发生变化。
让我们将重载的 `Point` `operator>>` 重新实现为事务操作
// note that point must be non-const so we can modify the object
// note that this implementation is a non-friend
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    if (in >> x >> y >> z)      // if all extractions succeeded
        point = Point{x, y, z}; // overwrite our existing point
        
    return in;
}
在这个实现中，我们没有直接用用户的输入覆盖数据成员。相反，我们正在将用户的输入提取到临时变量（
x
、
y
和
z
）中。一旦所有提取尝试都完成，我们就会检查所有提取是否成功。如果成功，那么我们就会一起更新
Point
的所有成员。否则，我们不会更新任何成员。
提示
if (in >> x >> y >> z)
等价于
in >> x >> y >> z; if (in)
。请记住，每次提取都返回
in
，这样就可以将多个提取链接在一起。单语句版本使用从最后一次提取返回的
in
作为 if 语句的条件，而多语句版本则明确使用
in
。
提示
事务操作可以使用多种不同的策略实现。例如
成功时更改：存储每个子操作的结果。如果所有子操作都成功，则将相关数据替换为存储的结果。这是我们在上面的 `Point` 示例中使用的策略。
失败时恢复：复制任何可能被更改的数据。如果任何子操作失败，可以通过复制的数据来恢复之前子操作所做的更改。
失败时回滚：如果任何子操作失败，则撤销每个先前的子操作（使用相反的子操作）。此策略常用于数据库，其中数据量过大无法备份，且子操作的结果无法存储。
虽然上述 `operator>>` 防止了部分提取，但它与基本类型 `operator>>` 的工作方式不一致。当提取到具有基本类型的对象失败时，对象不会保持不变——它会被复制赋值为 `0`（这确保了对象在提取尝试之前未初始化的情况下具有一些一致的值）。因此，为了保持一致性，你可能希望在提取失败时将对象重置为默认状态（至少在存在这种情况下）。
以下是 `operator>>` 的另一种版本，如果任何提取失败，它会将 `Point` 重置为其默认状态
// note that point must be non-const so we can modify the object
// note that this implementation is a non-friend
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    in >> x >> y >> z;
    point = in ? Point{x, y, z} : Point{};
        
    return in;
}
作者注
这样的操作在技术上不再是事务性的（因为失败不会“什么都不做”）。似乎没有一个通用的术语来描述保证没有部分结果的操作。也许是“不可分割操作”。
处理语义无效的输入
提取可能会以不同的方式失败。
在
operator>>
只是未能向变量提取任何内容的情况下，
std::cin
将自动进入失败模式（我们将在
第 9.5 课——std::cin 和处理无效输入
中讨论）。此函数的调用者可以检查
std::cin
以查看它是否失败并酌情处理该情况。
但是，如果用户输入了一个可提取但语义无效的值（例如，分母为
0
的
Fraction
）怎么办？因为
std::cin
确实提取了一些东西，它不会自动进入失败模式。然后调用者可能不会意识到出了问题。
为了解决这个问题，我们可以让重载的
operator>>
判断提取的任何值是否语义无效，如果是，则手动将输入流置于失败模式。这可以通过调用
std::cin.setstate(std::ios_base::failbit);
来实现。
下面是一个用于 `Point` 的事务性重载 `operator>>` 的示例，如果用户输入可提取的负值，它将导致输入流进入失败模式
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    in >> x >> y >> z;
    if (x < 0.0 || y < 0.0 || z < 0.0)       // if any extractable input is negative
        in.setstate(std::ios_base::failbit); // set failure mode manually
    point = in ? Point{x, y, z} : Point{};
       
    return in;
}
总结
重载
operator<<
和
operator>>
使您可以轻松地将类输出到屏幕并从控制台接受用户输入。
小测验时间
问题 #1
取下面的 Fraction 类，并为其添加重载的
operator<<
和
operator>>
。你的
operator>>
应避免部分提取，并在用户输入分母为
0
时失败。它不应在失败时将 Fraction 重置为默认值。
以下程序应编译通过
int main()
{
	Fraction f1{};
	std::cout << "Enter fraction 1: ";
	std::cin >> f1;

	Fraction f2{};
	std::cout << "Enter fraction 2: ";
	std::cin >> f2;

	std::cout << f1 << " * " << f2 << " is " << f1 * f2 << '\n'; // note: The result of f1 * f2 is an r-value

	return 0;
}
并产生结果
Enter fraction 1: 2/3
Enter fraction 2: 3/8
2/3 * 3/8 is 1/4
这是 Fraction 类
#include <iostream>
#include <numeric> // for std::gcd
 
class Fraction
{
private:
	int m_numerator{};
	int m_denominator{};
 
public:
	Fraction(int numerator=0, int denominator=1):
		m_numerator{numerator}, m_denominator{denominator}
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
 
	friend Fraction operator*(const Fraction& f1, const Fraction& f2);
	friend Fraction operator*(const Fraction& f1, int value);
	friend Fraction operator*(int value, const Fraction& f1);
 
	void print() const
	{
		std::cout << m_numerator << '/' << m_denominator << '\n';
	}
};
 
Fraction operator*(const Fraction& f1, const Fraction& f2)
{
	return Fraction { f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}
 
Fraction operator*(const Fraction& f1, int value)
{
	return Fraction { f1.m_numerator * value, f1.m_denominator };
}
 
Fraction operator*(int value, const Fraction& f1)
{
	return Fraction { f1.m_numerator * value, f1.m_denominator };
}
如果你使用的是 C++17 之前的编译器，可以将 std::gcd 替换为以下函数
#include <cmath>
 
int gcd(int a, int b) {
    return (b == 0) ? std::abs(a) : gcd(b, a % b);
}
显示答案
#include <iostream>
#include <limits>
#include <numeric> // for std::gcd

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    Fraction(int numerator=0, int denominator = 1) :
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

    friend Fraction operator*(const Fraction& f1, const Fraction& f2);
    friend Fraction operator*(const Fraction& f1, int value);
    friend Fraction operator*(int value, const Fraction& f1);

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);

    void print() const
    {
        std::cout << m_numerator << '/' << m_denominator << '\n';
    }
};

Fraction operator*(const Fraction& f1, const Fraction& f2)
{
    return Fraction { f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}

Fraction operator*(const Fraction& f1, int value)
{
    return Fraction { f1.m_numerator * value, f1.m_denominator };
}

Fraction operator*(int value, const Fraction& f1)
{
    return Fraction { f1.m_numerator * value, f1.m_denominator };
}

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
    out << f1.m_numerator << '/' << f1.m_denominator;
    return out;
}

std::istream& operator>>(std::istream& in, Fraction& f1)
{
    int numerator {};
    char ignore {};
    int denominator {};
    
    in >> numerator >> ignore >> denominator;
    if (denominator == 0)                       // if our denominator is semantically invalid
        in.setstate(std::ios_base::failbit);    // set failure mode manually
    if (in)                                     // if we're not in failure mode
        f1 = Fraction {numerator, denominator}; // update our object to the extracted values

    return in;
}

int main()
{
    Fraction f1{};
    std::cout << "Enter fraction 1: ";
    std::cin >> f1;

    Fraction f2{};
    std::cout << "Enter fraction 2: ";
    std::cin >> f2;

    std::cout << f1 << " * " << f2 << " is " << f1 * f2 << '\n'; // note: The result of f1 * f2 is an r-value

    return 0;
}
下一课
21.5
使用成员函数重载运算符
返回目录
上一课
21.3
使用普通函数重载运算符