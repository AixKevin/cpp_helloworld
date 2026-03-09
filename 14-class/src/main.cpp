#include <iostream>

class Fraction
{
private:
    int m_numerator{0};
    int m_denominator{1};

public:
    Fraction(int num = 0, int den = 1)
        : m_numerator{num}, m_denominator{den}
    {
    }

    Fraction(const Fraction &fraction)
        : m_numerator{fraction.m_numerator}, m_denominator{fraction.m_denominator}
    {
        std::cout << "Copy constructor called\n";
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", "
                  << m_denominator << ")\n";
    }
};

Fraction generateFraction(int n, int d)
{
    Fraction f{n, d};
    return f; // 拷贝 1：返回临时对象
}

void printFraction(Fraction f) // 按值传递
{
    f.print();
}

int main()
{
    Fraction f2{generateFraction(1, 2)}; // 拷贝 2：临时对象→f2
    printFraction(f2);                   // 拷贝 3：f2→函数参数
}
