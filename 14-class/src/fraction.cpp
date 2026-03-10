#include <iostream>

class Fraction
{
private:
    int m_numerator{0};
    int m_denominator{1};

public:
    explicit Fraction(int x=0, int y=1) : m_numerator{x}, m_denominator{y} {}
    void getFraction()
    {
        std::cout << "Enter a value for numerator: ";
        std::cin >> m_numerator;
        std::cout << "Enter a value for denominator: ";
        std::cin >> m_denominator;
        std::cout << '\n';
    }
    void print() const
    {
        std::cout << m_numerator << '/' << m_denominator << '\n';
    }
    const Fraction multiply(const Fraction &f1) const
    {
        return Fraction{f1.m_numerator * m_numerator, f1.m_denominator * m_denominator};
    }
};

int main()
{
    Fraction f1;
    f1.getFraction();
    Fraction f2;
    f2.getFraction();

    std::cout << "Your fractions multiplied together: ";

    // Fraction f3{f1.multiply(f2)};
    // f3.print();
    f1.multiply(f2).print();

    return 0;
}
