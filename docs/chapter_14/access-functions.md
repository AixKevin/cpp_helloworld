# 14.6 — 访问函数

14.6 — 访问函数
Alex
2007 年 9 月 4 日，太平洋时间下午 2:21
2024 年 12 月 29 日
在上一课
14.5 -- 公有和私有成员以及访问说明符
中，我们讨论了公有和私有访问级别。提醒一下，类通常将其数据成员设为私有，私有成员不能被公有直接访问。
考虑以下
Date
类
#include <iostream>

class Date
{
private:
    int m_year{ 2020 };
    int m_month{ 10 };
    int m_day{ 14 };

public:
    void print() const
    {
        std::cout << m_year << '/' << m_month << '/' << m_day << '\n';
    }
};

int main()
{
    Date d{};  // create a Date object
    d.print(); // print the date

    return 0;
}
虽然这个类提供了一个
print()
成员函数来打印整个日期，但这可能不足以满足用户的需求。例如，如果
Date
对象的用户想要获取年份呢？或者将年份更改为不同的值？他们将无法做到，因为
m_year
是私有的（因此不能被公有直接访问）。
对于某些类，能够获取或设置私有成员变量的值是适当的（在类所做的事情的上下文中）。
访问函数
访问函数
是一个简单的公有成员函数，其作用是检索或更改私有成员变量的值。
访问函数有两种：getter 和 setter。
Getter
（有时也称为
访问器
）是返回私有成员变量值的公有成员函数。
Setter
（有时也称为
修改器
）是设置私有成员变量值的公有成员函数。
命名法
“修改器”这个术语经常与“setter”互换使用。但更广泛地说，
修改器
是任何修改（改变）对象状态的成员函数。根据这个定义，setter 是一种特定类型的修改器。但是，也可能有非 setter 函数符合修改器的条件。
Getter 通常是 const 的，因此它们可以在 const 和非 const 对象上调用。Setter 应该是非 const 的，这样它们才能修改数据成员。
为了说明目的，让我们更新我们的
Date
类，使其具有一套完整的 getter 和 setter
#include <iostream>

class Date
{
private:
    int m_year { 2020 };
    int m_month { 10 };
    int m_day { 14 };

public:
    void print()
    {
        std::cout << m_year << '/' << m_month << '/' << m_day << '\n';
    }

    int getYear() const { return m_year; }        // getter for year
    void setYear(int year) { m_year = year; }     // setter for year

    int getMonth() const  { return m_month; }     // getter for month
    void setMonth(int month) { m_month = month; } // setter for month

    int getDay() const { return m_day; }          // getter for day
    void setDay(int day) { m_day = day; }         // setter for day
};

int main()
{
    Date d{};
    d.setYear(2021);
    std::cout << "The year is: " << d.getYear() << '\n';

    return 0;
}
这会打印
The year is: 2021
访问函数命名
访问函数的命名没有共同的约定。但是，有一些命名约定比其他更受欢迎。
前缀为“get”和“set”
int getDay() const { return m_day; }  // getter
    void setDay(int day) { m_day = day; } // setter
使用“get”和“set”前缀的优点是，它清楚地表明这些是访问函数（并且调用成本应该很低）。
无前缀
int day() const { return m_day; }  // getter
    void day(int day) { m_day = day; } // setter
这种风格更简洁，并且对 getter 和 setter 使用相同的名称（依靠函数重载来区分两者）。C++ 标准库使用此约定。
无前缀约定的缺点是，它不特别明显地表明这正在设置 day 成员的值
d.day(5); // does this look like it's setting the day member to 5?
关键见解
将私有数据成员前缀为“m_”的最佳原因之一是避免数据成员和 getter 具有相同的名称（C++ 不支持，但 Java 等其他语言支持）。
仅“set”前缀
int day() const { return m_day; }     // getter
    void setDay(int day) { m_day = day; } // setter
上述选择哪种取决于个人偏好。但是，我们强烈建议为 setter 使用“set”前缀。Getter 可以使用“get”前缀或无前缀。
提示
在 setter 上使用“set”前缀，使其更明显它们正在更改对象的状态。
Getter 应该按值或按 const 左值引用返回
Getter 应该提供数据“只读”访问。因此，最佳实践是它们应该按值返回（如果复制成员的成本很低）或按 const 左值引用返回（如果复制成员的成本很高）。
因为通过引用返回数据成员是一个非平凡的主题，我们将在
14.7 -- 返回数据成员引用的成员函数
一课中更详细地介绍该主题。
访问函数注意事项
关于应该使用或避免使用访问函数的情况有很多讨论。许多开发人员会认为使用访问函数违反了良好的类设计（一个可以轻松填满一整本书的主题）。
目前，我们建议采用务实的方法。在创建类时，考虑以下几点
如果您的类没有不变量并且需要大量访问函数，请考虑使用结构体（其数据成员是公有的）并直接访问成员。
优先实现行为或动作而不是访问函数。例如，而不是
setAlive(bool)
setter，实现
kill()
和
revive()
函数。
仅在公有合理需要获取或设置单个成员值的情况下才提供访问函数。
如果我们要为数据提供公有访问函数，为什么还要将数据设为私有？
很高兴你问了。我们将在即将到来的
14.8 -- 数据隐藏（封装）的好处
一课中回答这个问题。
下一课
14.7
返回数据成员引用的成员函数
返回目录
上一课
14.5
公有和私有成员以及访问说明符