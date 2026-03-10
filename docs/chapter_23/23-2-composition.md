# 23.2 — Composition

## Object composition

**Object composition** is the process of building complex objects from simpler ones. This process models a **"has-a"** relationship between two objects.

### Examples from real life:
- A car is built using a metal frame, engine, tires, transmission, steering wheel, etc.
- A personal computer is built from CPU, motherboard, memory, etc.
- You are built from smaller parts: head, body, legs, arms, etc.

The complex object is called the **whole** or **parent**. The simpler object is called the **part**, **child**, or **component**.

## Types of object composition

There are two subtypes: **composition** and **aggregation**.

## Composition requirements

To qualify as a **composition**, an object and a part must have the following relationship:

| Requirement | Description |
|-------------|-------------|
| **Part of the object** | The part is part of the whole object |
| **Single ownership** | The part can only belong to one object at a time |
| **Managed existence** | The part has its existence managed by the object |
| **Unidirectional** | The part does not know about the existence of the object |

### Real-life example: Body and Heart

A heart is a **part of** a person's body:
- The heart can only be part of one body at a time
- When the body is created, the heart is created; when the body dies, the heart dies
- The heart operates unaware it's part of a larger structure

This is sometimes called a **"death relationship"** because composition manages the lifetime of its parts.

## Implementation

Compositions are typically created as structs or classes with normal data members:

```cpp
class Fraction
{
private:
    int m_numerator;
    int m_denominator;
 
public:
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{ numerator }, m_denominator{ denominator }
    {
    }
};
```

The numerator and denominator:
- Are part of the Fraction
- Cannot belong to more than one Fraction at a time
- Don't know they are part of a Fraction
- Are created/destroyed with the Fraction

## Example: Creature and Point2D

```cpp
// Point2D.h
class Point2D
{
private:
    int m_x;
    int m_y;

public:
    Point2D() : m_x{ 0 }, m_y{ 0 } {}
    Point2D(int x, int y) : m_x{ x }, m_y{ y } {}
    
    void setPoint(int x, int y) { m_x = x; m_y = y; }
    friend std::ostream& operator<<(std::ostream& out, const Point2D& point);
};

// Creature.h
class Creature
{
private:
    std::string m_name;
    Point2D m_location;  // Composition - Creature owns Point2D

public:
    Creature(std::string_view name, const Point2D& location)
        : m_name{ name }, m_location{ location } {}
    
    void moveTo(int x, int y) { m_location.setPoint(x, y); }
};
```

## Benefits of using class members

1. **Simplicity**: Each class focuses on one task well
2. **Reusability**: Point2D can be reused in other applications
3. **Delegation**: Outer class delegates tasks to members who know how to do them

> **Tip**: Each class should be built to accomplish a single task. Either storage/manipulation of data (Point2D, std::string), OR coordination of members (Creature). Ideally not both.

## Variants on composition

- May defer creation of parts until needed (e.g., string class allocating memory only when data is assigned)
- May use a part given as input rather than creating it
- May delegate destruction to another object (e.g., garbage collection)

The key point: **The composition should manage its parts without the user needing to manage anything.**

## Summary

- **Composition** = "part-of" relationship with managed lifetime
- Parts can only belong to one whole at a time
- Whole manages creation/destruction of parts
- Unidirectional relationship (part doesn't know about whole)
- Implemented with normal member variables
- Favor composition when possible - it's straightforward and robust
