# 21.8 — 重载递增和递减运算符

21.8 — 重载递增和递减运算符
Alex
2007年10月15日，太平洋时间上午8:19
2023年11月25日
重载增量 (
++
) 和减量 (
--
) 运算符非常简单，只有一个小例外。增量和减量运算符实际上有两种版本：前缀增量和减量（例如
++x; --y;
）以及后缀增量和减量（例如
x++; y--;
）。
因为增量和减量运算符都是一元运算符，并且它们会修改其操作数，所以最好将它们重载为成员函数。我们先处理前缀版本，因为它们最直接。
重载前缀增量和减量
前缀增量和减量的重载方式与任何普通的一元运算符完全相同。我们将通过一个例子来完成
#include <iostream>

class Digit
{
private:
    int m_digit{};
public:
    Digit(int digit=0)
        : m_digit{digit}
    {
    }

    Digit& operator++();
    Digit& operator--();

    friend std::ostream& operator<< (std::ostream& out, const Digit& d);
};

Digit& Digit::operator++()
{
    // If our number is already at 9, wrap around to 0
    if (m_digit == 9)
        m_digit = 0;
    // otherwise just increment to next number
    else
        ++m_digit;

    return *this;
}

Digit& Digit::operator--()
{
    // If our number is already at 0, wrap around to 9
    if (m_digit == 0)
        m_digit = 9;
    // otherwise just decrement to next number
    else
        --m_digit;

    return *this;
}

std::ostream& operator<< (std::ostream& out, const Digit& d)
{
	out << d.m_digit;
	return out;
}

int main()
{
    Digit digit { 8 };

    std::cout << digit;
    std::cout << ++digit;
    std::cout << ++digit;
    std::cout << --digit;
    std::cout << --digit;

    return 0;
}
我们的 Digit 类包含一个介于 0 到 9 之间的数字。我们已经重载了增量和减量，以便它们增加/减少数字，如果数字超出范围，则会循环。
此示例输出：
89098
请注意，我们返回 *this。重载的增量和减量运算符返回当前隐式对象，因此可以“链式”连接多个运算符。
重载后缀增量和减量
通常，当函数的名称相同但参数数量或类型不同时，可以重载函数。然而，考虑前缀和后缀增量和减量运算符的情况。两者都具有相同的名称（例如 operator++），都是一元的，并且都接受一个相同类型的参数。那么，在重载时如何区分两者呢？
C++ 语言规范提供了一个特殊情况，它给出了答案：编译器会检查重载运算符是否有一个 int 参数。如果重载运算符有一个 int 参数，则该运算符是后缀重载。如果重载运算符没有参数，则该运算符是前缀重载。
以下是上述 Digit 类，带有前缀和后缀重载
class Digit
{
private:
    int m_digit{};
public:
    Digit(int digit=0)
        : m_digit{digit}
    {
    }

    Digit& operator++(); // prefix has no parameter
    Digit& operator--(); // prefix has no parameter

    Digit operator++(int); // postfix has an int parameter
    Digit operator--(int); // postfix has an int parameter

    friend std::ostream& operator<< (std::ostream& out, const Digit& d);
};

// No parameter means this is prefix operator++
Digit& Digit::operator++()
{
    // If our number is already at 9, wrap around to 0
    if (m_digit == 9)
        m_digit = 0;
    // otherwise just increment to next number
    else
        ++m_digit;

    return *this;
}

// No parameter means this is prefix operator--
Digit& Digit::operator--()
{
    // If our number is already at 0, wrap around to 9
    if (m_digit == 0)
        m_digit = 9;
    // otherwise just decrement to next number
    else
        --m_digit;

    return *this;
}

// int parameter means this is postfix operator++
Digit Digit::operator++(int)
{
    // Create a temporary variable with our current digit
    Digit temp{*this};

    // Use prefix operator to increment this digit
    ++(*this); // apply operator

    // return temporary result
    return temp; // return saved state
}

// int parameter means this is postfix operator--
Digit Digit::operator--(int)
{
    // Create a temporary variable with our current digit
    Digit temp{*this};

    // Use prefix operator to decrement this digit
    --(*this); // apply operator

    // return temporary result
    return temp; // return saved state
}

std::ostream& operator<< (std::ostream& out, const Digit& d)
{
	out << d.m_digit;
	return out;
}

int main()
{
    Digit digit { 5 };

    std::cout << digit;
    std::cout << ++digit; // calls Digit::operator++();
    std::cout << digit++; // calls Digit::operator++(int);
    std::cout << digit;
    std::cout << --digit; // calls Digit::operator--();
    std::cout << digit--; // calls Digit::operator--(int);
    std::cout << digit;

    return 0;
}
这会打印
5667665
这里有一些有趣的事情。首先，请注意我们通过在后缀版本上提供一个整数虚拟参数来区分前缀和后缀运算符。其次，由于虚拟参数在函数实现中未使用，我们甚至没有给它命名。这告诉编译器将此变量视为一个占位符，这意味着它不会警告我们声明了一个变量但从未使用过它。
第三，请注意前缀和后缀运算符执行相同的工作——它们都增加或减少对象。两者的区别在于它们返回的值。重载的前缀运算符返回对象在增量或减量之后的状态。因此，重载它们相当简单。我们只需增量或减量我们的成员变量，然后返回 *this。
另一方面，后缀运算符需要返回对象在增量或减量*之前*的状态。这导致了一个难题——如果我们增量或减量对象，我们将无法返回对象在增量或减量之前的状态。另一方面，如果我们返回对象在增量或减量之前的状态，则增量或减量将永远不会被调用。
解决此问题的典型方法是使用一个临时变量，该变量保存对象在增量或减量之前的值。然后可以对对象本身进行增量或减量。最后，将临时变量返回给调用者。通过这种方式，调用者接收到对象在增量或减量之前的一个副本，但对象本身已进行增量或减量。请注意，这意味着重载运算符的返回值必须是非引用，因为我们不能返回对函数退出时将被销毁的局部变量的引用。另请注意，这意味着后缀运算符通常比前缀运算符效率低，因为实例化临时变量并通过值而不是引用返回会增加开销。
最后，请注意我们编写了后增量和后减量，使其调用前增量和前减量来完成大部分工作。这减少了重复代码，并使我们的类在将来更容易修改。
下一课
21.9
重载下标运算符
返回目录
上一课
21.7
重载比较运算符