# 21.3 — 使用普通函数重载运算符

21.3 — 使用普通函数重载运算符
Alex
2016 年 5 月 23 日，下午 4:27 PDT
2023 年 9 月 11 日
在上一课中，我们将 operator+ 重载为友元函数
#include <iostream>
 
class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}

  // add Cents + Cents using a friend function
  friend Cents operator+(const Cents& c1, const Cents& c2);

  int getCents() const { return m_cents; }
};
 
// note: this function is not a member function!
Cents operator+(const Cents& c1, const Cents& c2)
{
  // use the Cents constructor and operator+(int, int)
  // we can access m_cents directly because this is a friend function
  return { c1.m_cents + c2.m_cents };
}
 
int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 };
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
使用友元函数重载运算符很方便，因为它允许你直接访问正在操作的类的内部成员。在上面的初始 Cents 示例中，我们的友元函数版本的 operator+ 直接访问了成员变量 m_cents。
但是，如果你不需要那种访问，你可以将重载的运算符编写为普通函数。请注意，上面的 Cents 类包含一个访问函数 (getCents())，它允许我们访问 m_cents，而无需直接访问私有成员。因此，我们可以将重载的 operator+ 编写为非友元函数
#include <iostream>

class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}

  int getCents() const { return m_cents; }
};

// note: this function is not a member function nor a friend function!
Cents operator+(const Cents& c1, const Cents& c2)
{
  // use the Cents constructor and operator+(int, int)
  // we don't need direct access to private members here
  return Cents{ c1.getCents() + c2.getCents() };
}

int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 };
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
由于普通函数和友元函数的工作方式几乎相同（它们只是对私有成员的访问级别不同），我们通常不会区分它们。唯一的区别是类内部的友元函数声明也充当原型。对于普通函数版本，你需要提供自己的函数原型。
Cents.h
#ifndef CENTS_H
#define CENTS_H

class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}
  
  int getCents() const { return m_cents; }
};

// Need to explicitly provide prototype for operator+ so uses of operator+ in other files know this overload exists
Cents operator+(const Cents& c1, const Cents& c2);

#endif
Cents.cpp
#include "Cents.h"

// note: this function is not a member function nor a friend function!
Cents operator+(const Cents& c1, const Cents& c2)
{
  // use the Cents constructor and operator+(int, int)
  // we don't need direct access to private members here
  return { c1.getCents() + c2.getCents() };
}
main.cpp
#include "Cents.h"
#include <iostream>

int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 }; // without the prototype in Cents.h, this would fail to compile
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
通常，如果可以通过现有成员函数实现，应优先选择普通函数而不是友元函数（越少的函数触及类的内部，就越好）。但是，不要为了将运算符重载为普通函数而不是友元函数而添加额外的访问函数！
最佳实践
如果可以在不添加额外函数的情况下实现，请优先将运算符重载为普通函数而不是友元函数。
下一课
21.4
重载 I/O 运算符
返回目录
上一课
21.2
使用友元函数重载算术运算符