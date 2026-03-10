# 23.6 — Container classes

## What is a container class?

A **container class** is a class designed to hold and organize multiple instances of another type. Container classes implement a **"member-of"** relationship.

### Real-life analogy:
- Breakfast cereal comes in a box
- Book pages come inside a cover and binding
- You store items in containers in your garage

Containers help **organize and store items** put inside them.

## Standard container functionality

Most well-defined containers include:

| Function | Purpose |
|----------|---------|
| Constructor | Create an empty container |
| Insert | Add a new object |
| Remove | Remove an object |
| Size | Report number of objects |
| Clear | Empty the container |
| Access | Access stored objects |
| Sort | (Optional) Sort elements |

## Types of containers

| Type | Description | Memory |
|------|-------------|--------|
| **Value containers** | Store **copies** of objects | Composition |
| **Reference containers** | Store **pointers/references** | Aggregation |

C++ containers typically hold **one type of data** (unlike some other languages).

## Example: IntArray container class

```cpp
#ifndef INTARRAY_H
#define INTARRAY_H

#include <algorithm>
#include <cassert>
#include <cstddef>

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;
    
    IntArray(int length) : m_length{ length }
    {
        assert(length >= 0);
        if (length > 0)
            m_data = new int[static_cast<std::size_t>(length)]{};
    }
    
    ~IntArray() { delete[] m_data; }
    
    IntArray(const IntArray& a) : IntArray(a.getLength())
    {
        std::copy_n(a.m_data, m_length, m_data);
    }
    
    IntArray& operator=(const IntArray& a)
    {
        if (&a == this) return *this;
        reallocate(a.getLength());
        std::copy_n(a.m_data, m_length, m_data);
        return *this;
    }
    
    void erase()
    {
        delete[] m_data;
        m_data = nullptr;
        m_length = 0;
    }
    
    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }
    
    void reallocate(int newLength)
    {
        erase();
        if (newLength <= 0) return;
        m_data = new int[static_cast<std::size_t>(newLength)];
        m_length = newLength;
    }
    
    void resize(int newLength)
    {
        if (newLength == m_length) return;
        if (newLength <= 0) { erase(); return; }
        
        int* data{ new int[static_cast<std::size_t>(newLength)] };
        if (m_length > 0)
        {
            int elementsToCopy = (newLength > m_length) ? m_length : newLength;
            std::copy_n(m_data, elementsToCopy, data);
        }
        delete[] m_data;
        m_data = data;
        m_length = newLength;
    }
    
    void insertBefore(int value, int index)
    {
        assert(index >= 0 && index <= m_length);
        int* data{ new int[static_cast<std::size_t>(m_length+1)] };
        std::copy_n(m_data, index, data);
        data[index] = value;
        std::copy_n(m_data + index, m_length - index, data + index + 1);
        delete[] m_data;
        m_data = data;
        ++m_length;
    }
    
    void remove(int index)
    {
        assert(index >= 0 && index < m_length);
        if (m_length == 1) { erase(); return; }
        
        int* data{ new int[static_cast<std::size_t>(m_length-1)] };
        std::copy_n(m_data, index, data);
        std::copy_n(m_data + index + 1, m_length - index - 1, data + index);
        delete[] m_data;
        m_data = data;
        --m_length;
    }
    
    int getLength() const { return m_length; }
};

#endif
```

## Best Practice

> If a class in the standard library meets your needs, **use that instead of creating your own**. For example, use `std::vector<int>` instead of IntArray.

## Advanced improvements

- Make it a template class for any copyable type
- Add const overloads for const containers
- Add move semantics (move constructor/assignment)
- Move elements instead of copying when possible
- Provide exception safety guarantees

## Summary

- **Container class** = holds multiple instances of another type
- **Value containers** store copies (composition)
- **Reference containers** store pointers/references (aggregation)
- Implement standard operations: insert, remove, access, size, etc.
- Prefer standard library containers when available
