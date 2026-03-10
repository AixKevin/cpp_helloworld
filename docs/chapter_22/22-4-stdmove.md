# 22.4 — std::move

Once you start using move semantics more regularly, you'll start to find cases where you want to invoke move semantics, but the objects you have to work with are **l-values**, not r-values.

## The problem

Consider a swap function that takes l-value references:

```cpp
template <typename T>
void mySwapCopy(T& a, T& b) 
{ 
	T tmp { a }; // invokes copy constructor
	a = b; // invokes copy assignment
	b = tmp; // invokes copy assignment
}
```

This makes 3 copies, which can be inefficient for objects like `std::string`.

## std::move to the rescue

In C++11, **std::move** is a standard library function that casts (using `static_cast`) its argument into an r-value reference, so that move semantics can be invoked.

```cpp
#include <utility> // for std::move

template <typename T>
void mySwapMove(T& a, T& b) 
{ 
	T tmp { std::move(a) }; // invokes move constructor
	a = std::move(b); // invokes move assignment
	b = std::move(tmp); // invokes move assignment
}
```

This is much more efficient - the vector element can steal the string's value rather than having to copy it.

## Another example: Filling containers

```cpp
std::vector<std::string> v;
std::string str { "Knock" };

v.push_back(str); // calls l-value version - copies str
v.push_back(std::move(str)); // calls r-value version - moves str
```

## Moved-from objects are in a valid but indeterminate state

The C++ standard says: "Unless otherwise specified, moved-from objects [of types defined in the C++ standard library] shall be placed in a **valid but unspecified state**."

### What you can do with moved-from objects:
- ✅ Set or reset the value (using `operator=` or `clear()`/`reset()`)
- ✅ Test the state (e.g., using `empty()`)

### What you should avoid:
- ❌ Functions that depend on the current value (e.g., `operator[]`, `front()`)

> **Key insight**: `std::move()` gives a hint to the compiler that the programmer doesn't need the value of an object any more. Only use `std::move()` on persistent objects whose value you want to move, and do not make any assumptions about the value of the object beyond that point.

## Where else is std::move useful?

- **Sorting algorithms** - Many sorting algorithms work by swapping pairs of elements. Now we can use move semantics instead of copy semantics.
- **Moving smart pointer contents** - Move the contents managed by one smart pointer to another.

## Related content

There is a useful variant of `std::move()` called **`std::move_if_noexcept()`** that returns a movable r-value if the object has a `noexcept` move constructor, otherwise it returns a copyable l-value.

## Summary

- **std::move** converts an l-value to an r-value reference
- Use it when you want to invoke move semantics on an l-value
- Moved-from objects are left in a **valid but unspecified state**
- Safe to reset/assign moved-from objects, but don't read their values
- Essential for efficient swapping and container operations
