# 23.7 — std::initializer_list

## The problem

Built-in arrays can use initializer lists:

```cpp
int array[] { 5, 4, 3, 2, 1 };  // Works!
```

But custom container classes cannot without special support:

```cpp
IntArray array { 5, 4, 3, 2, 1 };  // ERROR - no matching constructor
```

## Solution: std::initializer_list

When a compiler sees an initializer list, it converts it into a `std::initializer_list<T>` object.

```cpp
#include <initializer_list>
#include <algorithm>
#include <cassert>
#include <iostream>

class IntArray
{
private:
    int m_length {};
    int* m_data{};

public:
    IntArray() = default;
    
    IntArray(int length)
        : m_length{ length }
        , m_data{ new int[static_cast<std::size_t>(length)] {} }
    {
    }
    
    // Constructor that accepts initializer_list
    IntArray(std::initializer_list<int> list)
        : IntArray(static_cast<int>(list.size()))  // Delegate to size constructor
    {
        std::copy(list.begin(), list.end(), m_data);
    }
    
    ~IntArray() { delete[] m_data; }
    
    IntArray(const IntArray&) = delete;
    IntArray& operator=(const IntArray&) = delete;
    
    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }
    
    int getLength() const { return m_length; }
};

int main()
{
    IntArray array{ 5, 4, 3, 2, 1 };  // Now works!
    for (int count{ 0 }; count < array.getLength(); ++count)
        std::cout << array[count] << ' ';
    return 0;
}
```

## Key facts about std::initializer_list

| Fact | Description |
|------|-------------|
| **Header** | `<initializer_list>` |
| **Type parameter** | `std::initializer_list<int>`, etc. |
| **Size** | Has `size()` function (returns element count) |
| **Passed by value** | Lightweight view, copying is cheap |
| **Access** | Use `begin()`, `end()`, or range-based for |

## Accessing elements

`std::initializer_list` doesn't support `operator[]`. Use these alternatives:

```cpp
// Option 1: Range-based for loop
for (int value : list) { /* ... */ }

// Option 2: Iterator indexing
for (std::size_t count{}; count < list.size(); ++count)
{
    m_data[count] = list.begin()[count];
}
```

## Important: List initialization favors list constructors

```cpp
IntArray a1(5);   // Uses IntArray(int) - allocates array of size 5
IntArray a2{ 5 }; // Uses IntArray(initializer_list) - allocates array of size 1
```

> **Key insight**: List initialization favors matching list constructors over non-list constructors.

### Best Practice

- Use **brace initialization** `{}` when intending to call the list constructor
- Use **direct initialization** `()` when intending to call a non-list constructor

### Example with std::vector

```cpp
std::vector<int> array(5);  // 5 elements, all 0: 0 0 0 0 0
std::vector<int> array{ 5 }; // 1 element with value 5: 5
```

## Warning: Adding list constructors is dangerous

Adding a list constructor to an existing class can **silently change behavior**:

```cpp
class Foo
{
public:
    Foo(int, int) { std::cout << "Foo(int, int)\n"; }
    Foo(std::initializer_list<int>) { std::cout << "Foo(initializer_list)\n"; }
};

int main()
{
    Foo f1{ 1, 2 };  // Originally called Foo(int,int), now calls Foo(initializer_list)
}
```

## List assignment

If you provide list construction, also provide list assignment:

```cpp
IntArray& operator=(std::initializer_list<int> list)
{
    int length { static_cast<int>(list.size()) };
    if (length != m_length)
    {
        delete[] m_data;
        m_length = length;
        m_data = new int[list.size()]{};
    }
    std::copy(list.begin(), list.end(), m_data);
    return *this;
}
```

> **Best practice**: If you provide list construction, provide list assignment as well.

## Summary

- **std::initializer_list** allows list initialization for custom classes
- Lives in `<initializer_list>` header
- Lightweight view, passed by value
- Access via `begin()`, `end()`, or range-based for
- List initialization **favors list constructors**
- Provide list assignment if you provide list construction
- Adding list constructors to existing classes can break code
