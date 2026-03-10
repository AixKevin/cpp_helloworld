#include <iostream>
#include <cmath>

class Point2d
{
private:
    /* data */
    double m_x{0.0}, m_y{0.0};

public:
    Point2d() = default;
    Point2d(double x, double y) : m_x{x}, m_y{y}
    {
    }
    void print() const
    {
        std::cout << "Point2d(" << m_x << ", " << m_y << ")\n";
    }
    const double distanceTo(const Point2d &p) const
    {
        return std::sqrt((m_x - p.m_x) * (m_x - p.m_x) + (m_y - p.m_y) * (m_y - p.m_y));
    }
};

int main()
{
    Point2d first{};
    Point2d second{3.0, 4.0};

    first.print();
    second.print();

    std::cout << "Distance between two points: " << first.distanceTo(second) << '\n';

    return 0;
}
