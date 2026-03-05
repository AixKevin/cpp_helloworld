# 21.14 — 重载运算符与函数模板

21.14 — 重载运算符与函数模板
Alex
2008年4月29日，太平洋夏令时晚上8:14
2023年9月11日
在课程
11.7 -- 函数模板实例化
中，我们讨论了编译器如何使用函数模板来实例化函数，然后编译这些函数。我们还指出，如果函数模板中的代码试图执行实际类型不支持的操作（例如将整数值
1
添加到
std::string
），这些函数可能无法编译。
在本课程中，我们将看几个例子，这些例子中，由于我们的实际类类型不支持某些运算符，实例化函数将无法编译，并展示我们如何定义这些运算符，以便实例化函数能够编译。
运算符、函数调用和函数模板
首先，让我们创建一个简单的类
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};
并定义一个
max
函数模板
template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}
现在，让我们看看当我们尝试使用
Cents
类型的对象调用
max()
时会发生什么
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};

template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}

int main()
{
    Cents nickel{ 5 };
    Cents dime{ 10 };

    Cents bigger { max(nickel, dime) };
    std::cout << bigger << " is bigger\n";

    return 0;
}
C++将为max()创建一个模板实例，如下所示
template <>
const Cents& max(const Cents& x, const Cents& y)
{
    return (x < y) ? y : x;
}
然后它会尝试编译这个函数。看到问题了吗？当
x
和
y
是
Cents
类型时，C++不知道如何评估
x < y
！因此，这将导致编译错误。
为了解决这个问题，只需为我们希望与
max
一起使用的任何类重载
operator<
#include <iostream>

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }
    
    friend bool operator< (const Cents& c1, const Cents& c2)
    {
        return (c1.m_cents < c2.m_cents);
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};

template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}

int main()
{
    Cents nickel{ 5 };
    Cents dime { 10 };

    Cents bigger { max(nickel, dime) };
    std::cout << bigger << " is bigger\n";

    return 0;
}
这按预期工作，并打印出
10 is bigger
另一个例子
我们再看一个函数模板因缺少重载运算符而无法工作的例子。
以下函数模板将计算数组中多个对象的平均值
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

int main()
{
    int intArray[] { 5, 3, 2, 1, 4 };
    std::cout << average(intArray, 5) << '\n';

    double doubleArray[] { 3.12, 3.45, 9.23, 6.34 };
    std::cout << average(doubleArray, 4) << '\n';

    return 0;
}
这产生的值是
3
5.535
正如你所看到的，它对内置类型工作得很好！
现在让我们看看当我们对
Cents
类调用此函数时会发生什么
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
编译器会疯狂地产生大量的错误消息！第一个错误消息会是这样的
error C2679: binary << : no operator found which takes a right-hand operand of type Cents (or there is no acceptable conversion)
记住
average()
返回一个
Cents
对象，我们正尝试使用
operator<<
将该对象流式输出到
std::cout
。然而，我们还没有为我们的
Cents
类定义
operator<<
。让我们来定义它
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Cents& cents)
    {
        out << cents.m_cents << " cents ";
        return out;
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
如果我们再次编译，我们将得到另一个错误
error C2676: binary += : Cents does not define this operator or a conversion to a type acceptable to the predefined operator
此错误实际上是由我们调用
average(const Cents*, int)
时创建的函数模板实例引起的。请记住，当我们调用模板函数时，编译器会“模板化”一个函数的副本，其中模板类型参数（占位符类型）已被函数调用中的实际类型替换。这是当
T
是
Cents
对象时
average()
的函数模板实例
template <>
Cents average(const Cents* myArray, int numValues)
{
    Cents sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}
我们收到错误消息的原因是以下这行代码
sum += myArray[count];
在这种情况下，
sum
是一个
Cents
对象，但是我们还没有为
Cents
对象定义
operator+=
！我们需要定义这个函数才能让
average()
与
Cents
一起工作。展望未来，我们可以看到
average()
也使用了
operator/=
，所以我们也要定义它
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Cents& cents)
    {
        out << cents.m_cents << " cents ";
        return out;
    }

    Cents& operator+= (const Cents &cents)
    {
        m_cents += cents.m_cents;
        return *this;
    }

    Cents& operator/= (int x)
    {
        m_cents /= x;
        return *this;
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
最后，我们的代码将编译并运行！结果如下
11 cents
请注意，我们根本不需要修改
average()
就能使其与
Cents
类型的对象一起工作。我们只需为
Cents
类定义用于实现
average()
的运算符，其余的由编译器处理！
下一课
21.x
第21章 总结与测验
返回目录
上一课
21.13
浅拷贝与深拷贝