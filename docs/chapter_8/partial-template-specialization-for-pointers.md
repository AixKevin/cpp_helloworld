# 26.6 — 指针的模板偏特化

26.6 — 指针的模板偏特化
Alex
2016年12月5日，晚上11:15 PST
2024年3月29日
在上一课
26.4 -- 类模板特化
中，我们研究了一个简单的模板
Storage
类，以及一个针对
double
类型的特化。
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template<>
void Storage<double>::print() // fully specialized for type double
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // Define some storage units
    Storage i { 5 };
    Storage d { 6.7 }; // will cause Storage<double> to be implicitly instantiated

    // Print out some values
    i.print(); // calls Storage<int>::print (instantiated from Storage<T>)
    d.print(); // calls Storage<double>::print (called from explicit specialization of Storage<double>::print())
}
然而，这个类虽然简单，却有一个隐藏的缺陷：当
T
是指针类型时，它能编译但会发生故障。例如：
int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr };
    s.print();
    
    return 0;
}
在作者的机器上，这产生了以下结果：
0x7ffe164e0f50
发生了什么？因为
ptr
是一个
double*
，
s
的类型是
Storage<double*>
，这意味着
m_value
的类型是
double*
。当构造函数被调用时，
m_value
接收了
ptr
所持有的地址的副本，并且当调用
print()
成员函数时，打印的就是这个地址。
那么我们该如何解决这个问题呢？
一个选项是为
double*
类型添加一个完全特化：
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template<>
void Storage<double*>::print() // fully specialized for type double*
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}

template<>
void Storage<double>::print() // fully specialized for type double (for comparison, not used)
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr };
    s.print(); // calls Storage<double*>::print()
    
    return 0;
}
现在可以打印出正确的结果了：
1.200000e+00
但这只解决了当
T
类型为
double*
时的问题。那么当
T
是
int*
，或者
char*
，或者任何其他指针类型时呢？
我们真的不想为每种指针类型都创建一个完全特化。事实上，这甚至是不可能的，因为用户总是可以传入指向程序定义类型的指针。
指针的模板偏特化
你可能会想尝试创建一个函数模板，并对
T*
类型进行重载：
// doesn't work
template<typename T>
void Storage<T*>::print()
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}
这样的函数是一个部分特化模板函数，因为它限制了
T
的类型（为指针类型），但
T
仍然是一个类型模板参数。
不幸的是，这不起作用，原因很简单：截至撰写本文时 (C++23)，函数无法进行偏特化。正如我们在课程
26.5 -- 模板偏特化
中指出的，只有类才能进行偏特化。
所以我们改为偏特化
Storage
类：
#include <iostream>

template <typename T>
class Storage // This is our primary template class (same as previous)
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template <typename T> // we still have a type template parameter
class Storage<T*> // This is partially specialized for T*
{
private:
    T* m_value {};
public:
    Storage(T* value)
      : m_value { value }
    {
    }

    void print();
};

template <typename T>
void Storage<T*>::print() // This is a non-specialized function of partially specialized class Storage<T*>
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}

int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr }; // instantiates Storage<double*> from partially specialized class
    s.print(); // calls Storage<double*>::print()
    
    return 0;
}
我们将
Storage<T*>::print()
定义在类之外，只是为了展示它是如何完成的，并展示其定义与上面不起作用的部分特化函数
Storage<T*>::print()
是相同的。然而，现在
Storage<T*>
是一个部分特化类，
Storage<T*>::print()
不再是部分特化——它是一个非特化函数，这就是它被允许的原因。
值得注意的是，我们的类型模板参数被定义为
T
，而不是
T*
。这意味着
T
将被推导为非指针类型，因此我们必须在任何需要
T
的指针的地方使用
T*
。另外值得提醒的是，偏特化
Storage<T*>
需要在主模板类
Storage<T>
之后定义。
所有权和生命周期问题
上面部分特化的类
Storage<T*>
还有另一个潜在问题。因为
m_value
是
T*
，它是指向传入对象的指针。如果该对象随后被销毁，我们的
Storage<T*>
将会悬空。
核心问题是，我们的
Storage<T>
实现具有复制语义（意味着它会复制其初始化器），但
Storage<T*>
具有引用语义（意味着它引用其初始化器）。这种不一致是导致 bug 的根源。
有几种不同的方法可以处理此类问题（按复杂性递增的顺序排列）：
明确指出
Storage<T*>
是一个视图类（具有引用语义），因此调用者有责任确保被指向的对象在
Storage<T*>
存在期间保持有效。不幸的是，由于这个部分特化的类必须与主模板类同名，我们不能给它一个像
StorageView
这样的名字。因此，我们只能使用注释或其他可能被忽略的东西。这不是一个好的选择。
完全阻止使用
Storage<T*>
。我们可能不需要
Storage<T*>
存在，因为调用者可以在实例化时始终解引用指针以使用
Storage<T>
并复制值（这对于存储类来说是语义上合适的）。
然而，虽然你可以删除重载函数，但 C++ (截至 C++23) 不允许你删除类。显而易见的解决方案是部分特化
Storage<T*>
，然后做一些事情使其在模板实例化时无法编译（例如
static_assert
），这种方法有一个主要缺点：
std::nullptr_t
不是指针类型，所以
Storage<std::nullptr_t>
不会匹配
Storage<T*>
！
一个更好的解决方案是完全避免偏特化，并在我们的主模板上使用
static_assert
来确保
T
是我们允许的类型。下面是这种方法的示例：
#include <iostream>
#include <type_traits> // for std::is_pointer_v and std::is_null_pointer_v

template <typename T>
class Storage
{
    // Make sure T isn't a pointer or a std::nullptr_t
    static_assert(!std::is_pointer_v<T> && !std::is_null_pointer_v<T>, "Storage<T*> and Storage<nullptr> disallowed");

private:
    T m_value {};

public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    double d { 1.2 };

    Storage s1 { d }; // ok
    s1.print();

    Storage s2 { &d }; // static_assert because T is a pointer
    s2.print();

    Storage s3 { nullptr }; // static_assert because T is a nullptr
    s3.print();
    
    return 0;
}
让
Storage<T*>
在堆上复制对象。如果您自己进行所有堆内存管理，这需要重载构造函数、复制构造函数、复制赋值和析构函数。一个更简单的替代方法是只使用
std::unique_ptr
（我们在课程
22.5 -- std::unique_ptr
中介绍）。
#include <iostream>
#include <type_traits> // for std::is_pointer_v and std::is_null_pointer_v
#include <memory>

template <typename T>
class Storage
{
    // Make sure T isn't a pointer or a std::nullptr_t
    static_assert(!std::is_pointer_v<T> && !std::is_null_pointer_v<T>, "Storage<T*> and Storage<nullptr> disallowed");

private:
    T m_value {};

public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template <typename T>
class Storage<T*>
{
private:
    std::unique_ptr<T> m_value {}; // use std::unique_ptr to automatically deallocate when Storage is destroyed

public:
    Storage(T* value)
      : m_value { std::make_unique<T>(value ? *value : 0) } // or throw exception when !value
    {
    }

    void print()
    {
        if (m_value)
            std::cout << *m_value << '\n';
    }
};

int main()
{
    double d { 1.2 };

    Storage s1 { d }; // ok
    s1.print();

    Storage s2 { &d }; // ok, copies d on heap
    s2.print();

    return 0;
}
当您希望一个类以对最终用户完全透明的方式处理指针和非指针类型时，使用类模板偏特化来创建不同的指针和非指针实现非常有用。
下一课
26.x
第26章 总结和测验
返回目录
上一课
26.5
模板偏特化