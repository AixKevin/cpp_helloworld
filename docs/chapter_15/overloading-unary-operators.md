# 21.6 — 重载一元运算符 +、- 和 !

21.6 — 重载一元运算符 +、- 和 !
Alex
2007 年 10 月 8 日，下午 3:09 PDT
2023 年 11 月 25 日
重载一元运算符
与你目前为止看到的不同，正号（+）、负号（-）和逻辑非（!）运算符都是一元运算符，这意味着它们只作用于一个操作数。因为它们只作用于被应用的对象，所以一元运算符重载通常作为成员函数实现。所有这三个运算符都以相同的方式实现。
让我们看看如何在我们之前示例中使用的 Cents 类上实现 operator-
#include <iostream>

class Cents
{
private:
    int m_cents {};
 
public:
    Cents(int cents): m_cents{cents} {}
 
    // Overload -Cents as a member function
    Cents operator-() const;

    int getCents() const { return m_cents; }
};
 
// note: this function is a member function!
Cents Cents::operator-() const
{
    return -m_cents; // since return type is a Cents, this does an implicit conversion from int to Cents using the Cents(int) constructor
}

int main()
{
    const Cents nickle{ 5 };
    std::cout << "A nickle of debt is worth " << (-nickle).getCents() << " cents\n";

    return 0;
}
这应该很简单。我们重载的负号运算符 (-) 是一个作为成员函数实现的一元运算符，因此它不带参数（它作用于 *this 对象）。它返回一个 Cents 对象，该对象是原始 Cents 值的取反。因为 operator- 不修改 Cents 对象，所以我们可以（并且应该）将其设为 const 函数（这样它就可以在 const Cents 对象上调用）。
请注意，负号运算符- 和减号运算符- 之间没有混淆，因为它们的参数数量不同。
这是另一个例子。! 运算符是逻辑非运算符——如果一个表达式计算结果为“真”，operator! 将返回假，反之亦然。我们通常会看到它应用于布尔变量以测试它们是否为真
if (!isHappy)
    std::cout << "I am not happy!\n";
else
    std::cout << "I am so happy!\n";
对于整数，0 评估为假，其他任何值评估为真，因此应用于整数的 operator! 将对整数值 0 返回真，否则返回假。
扩展这个概念，我们可以说如果对象的状态是“假”、“零”或默认初始化状态，那么 operator! 应该评估为真。
以下示例展示了用户定义的 Point 类的 operator- 和 operator! 的重载
#include <iostream>

class Point
{
private:
    double m_x {};
    double m_y {};
    double m_z {};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0):
        m_x{x}, m_y{y}, m_z{z}
    {
    }
 
    // Convert a Point into its negative equivalent
    Point operator- () const;

    // Return true if the point is set at the origin
    bool operator! () const;
 
    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }
};

// Convert a Point into its negative equivalent 
Point Point::operator- () const
{
    return { -m_x, -m_y, -m_z };
}

// Return true if the point is set at the origin, false otherwise
bool Point::operator! () const
{
    return (m_x == 0.0 && m_y == 0.0 && m_z == 0.0);
}

int main()
{
    Point point{}; // use default constructor to set to (0.0, 0.0, 0.0)

    if (!point)
        std::cout << "point is set at the origin.\n";
    else
        std::cout << "point is not set at the origin.\n";

    return 0;
}
此类的重载 operator! 在 Point 设置为坐标 (0.0, 0.0, 0.0) 的默认值时返回布尔值“真”。因此，以上代码产生的结果是
point is set at the origin.
小测验时间
为 Point 类实现重载的一元 `operator+`。一元 `operator+` 只返回它的操作数（它不将负值变为正值）。
显示答案
这是显而易见的解决方案
Point Point::operator+ () const
{
    return { m_x, m_y, m_z };
}
但是因为我们返回的 Point 正是我们正在操作的那个，所以下面的代码也有效
Point Point::operator+ () const
{
    return *this;
}
注意，这里我们通过值返回一个副本，而不是 const 引用。这是因为此函数的使用者可能期望返回的对象是可修改的。
下一课
21.7
重载比较运算符
返回目录
上一课
21.5
使用成员函数重载运算符