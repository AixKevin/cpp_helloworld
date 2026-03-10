# 23.5 — Dependencies

## What is a dependency?

A **dependency** occurs when one object invokes another object's functionality in order to accomplish some specific task. This is a **weaker relationship than an association**, but any change to the object being depended upon may break functionality in the dependent caller.

A dependency is always **unidirectional**.

## Real-life examples

- If you break your foot, you are **dependent on crutches** to get around (but not otherwise)
- Flowers are **dependent upon bees** to pollinate them (but not otherwise)

## C++ example: std::ostream

```cpp
#include <iostream>
 
class Point
{
private:
    double m_x{}, m_y{}, m_z{};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0)
        : m_x{x}, m_y{y}, m_z{z} {}
    
    // Point has a dependency on std::ostream here
    friend std::ostream& operator<<(std::ostream& out, const Point& point);
};
 
std::ostream& operator<<(std::ostream& out, const Point& point)
{
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';
    return out;
}
 
int main()
{
    Point point1 { 2.0, 3.0, 4.0 };
    std::cout << point1;  // Program has a dependency on std::cout
    return 0;
}
```

Point isn't directly related to `std::ostream`, but it has a **dependency** on it since `operator<<` uses `std::ostream` to print.

## Dependencies vs Association

| Feature | Association | Dependency |
|---------|-------------|------------|
| **Storage** | Keeps a link as a member | Typically NOT a member |
| **Lifetime** | Link persists | Object instantiated as needed |
| **Example** | Doctor has array of Patients | operator<< uses ostream temporarily |

### Association example:
```cpp
class Doctor
{
    std::vector<Patient*> m_patients;  // Persistent link
};
```

### Dependency example:
```cpp
class Point
{
    // ostream passed as parameter, not stored
    friend std::ostream& operator<<(std::ostream& out, const Point& point);
};
```

## Key points

- Dependencies are **weaker** than associations
- The depended-on object is typically:
  - Instantiated as needed
  - Passed as a function parameter
- Not stored as a class member
- Changes to the depended-on object may break the dependent

## Summary

- **Dependency** = one object uses another to accomplish a task
- Weaker than association
- Unidirectional
- Depended-on object not stored as member
- Typically created temporarily or passed as parameter
