# 23.3 — Aggregation

## Aggregation requirements

To qualify as an **aggregation**, a whole object and its parts must have the following relationship:

| Requirement | Description |
|-------------|-------------|
| **Part of the object** | The part is part of the whole object |
| **Multiple ownership allowed** | The part can belong to more than one object at a time |
| **Unmanaged existence** | The part does NOT have its existence managed by the object |
| **Unidirectional** | The part does not know about the existence of the object |

Like composition, aggregation is a **part-whole relationship** and **unidirectional**. However, unlike composition:
- Parts can belong to multiple objects simultaneously
- The whole is **not** responsible for creating/destroying the parts

## Real-life examples

### Person and Address
- An address can belong to multiple people (you and your roommate)
- The address existed before the person arrived and will exist after they leave
- The person knows their address, but the address doesn't know who lives there

### Car and Engine
- A car has an engine, but the engine can belong to other things (like the owner)
- The car is not responsible for creating/destroying the engine
- The car knows it has an engine, but the engine doesn't know it's part of the car

Aggregation models **"has-a"** relationships (a department has teachers, the car has an engine).

## Implementation

Aggregations typically use **pointer or reference members** that point to objects created outside the class scope:

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Teacher
{
private:
    std::string m_name{};

public:
    Teacher(std::string_view name) : m_name{ name } {}
    const std::string& getName() const { return m_name; }
};

class Department
{
private:
    const Teacher& m_teacher;  // Reference to external object

public:
    Department(const Teacher& teacher) : m_teacher{ teacher } {}
};

int main()
{
    Teacher bob{ "Bob" };  // Created independently
    
    {
        Department department{ bob };  // Uses reference to bob
    } // department destroyed, but bob still exists
    
    std::cout << bob.getName() << " still exists!\n";
    return 0;
}
```

## Best Practice

> **Implement the simplest relationship type that meets the needs of your program, not what seems right in real-life.**

Example:
- **Body shop simulator**: Car/Engine as aggregation (engine can be removed)
- **Racing simulation**: Car/Engine as composition (engine never exists outside car)

## Composition vs Aggregation Summary

| Feature | Composition | Aggregation |
|---------|-------------|-------------|
| Member type | Normal member variables | Pointer/reference members |
| Creation | Class creates parts | Parts created externally |
| Destruction | Class destroys parts | Parts destroyed externally |
| Ownership | Single | Can be multiple |

## std::reference_wrapper

For storing multiple references in containers (like `std::vector`), use `std::reference_wrapper`:

```cpp
#include <functional> // std::reference_wrapper
#include <vector>
#include <string>
#include <iostream>

int main()
{
    std::string tom{ "Tom" };
    std::string berta{ "Berta" };
    
    // Vector of references (via reference_wrapper)
    std::vector<std::reference_wrapper<std::string>> names{ tom, berta };
    
    std::string jim{ "Jim" };
    names.emplace_back(jim);
    
    for (auto name : names)
    {
        name.get() += " Beam";  // Use get() to access referenced object
    }
    
    std::cout << jim << '\n';  // prints "Jim Beam"
    return 0;
}
```

## Warning

Aggregations are potentially dangerous because they don't handle deallocation. If the external party forgets to clean up, **memory will leak**. **Compositions should be favored over aggregations.**

## Summary

- **Aggregation** = "has-a" relationship without managed lifetime
- Parts can belong to multiple objects
- Parts created/destroyed independently of whole
- Implemented with pointers or references
- Use `std::reference_wrapper` for containers of references
- Favor composition over aggregation when possible
