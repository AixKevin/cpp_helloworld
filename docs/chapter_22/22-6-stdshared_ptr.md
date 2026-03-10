# 22.6 — std::shared_ptr

Unlike `std::unique_ptr`, which is designed to singly own and manage a resource, **`std::shared_ptr`** is meant to solve the case where you need **multiple smart pointers co-owning a resource**.

## Basic usage

```cpp
#include <memory>

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };
	{
		auto ptr2 { ptr1 }; // Copy - both point to same resource
		
		std::cout << "Killing one shared pointer\n";
	} // ptr2 goes out of scope, but resource NOT destroyed

	std::cout << "Killing another shared pointer\n";
	return 0;
} // ptr1 goes out of scope - NOW resource is destroyed
```

## Important: Always copy from existing shared_ptr

```cpp
// WRONG - Creates two independent shared_ptr:
Resource* res { new Resource };
std::shared_ptr<Resource> ptr1 { res };
std::shared_ptr<Resource> ptr2 { res }; // DANGER!

// RIGHT - Copy from existing shared_ptr:
auto ptr1 { std::make_shared<Resource>() };
auto ptr2 { ptr1 }; // SAFE - both aware of each other
```

> **Best practice**: Always make a copy of an existing `std::shared_ptr` if you need more than one `std::shared_ptr` pointing to the same resource.

## std::make_shared

Much like `std::make_unique()`, `std::make_shared()` is simpler, safer, and more performant.

### Why std::make_shared is more efficient

`std::shared_ptr` uses **two pointers internally**:
1. One pointer points at the resource
2. One pointer points at a **"control block"** (tracks reference count)

When using `std::make_shared()`, both can be allocated in a **single memory allocation**, leading to better performance.

## Shared pointers can be created from unique pointers

A `std::unique_ptr` can be converted into a `std::shared_ptr` via a special constructor. The contents will be **moved** to the `std::shared_ptr`.

However, `std::shared_ptr` **cannot** be safely converted to a `std::unique_ptr`.

## The perils of std::shared_ptr

With `std::shared_ptr`, you have to worry about **all** of them being properly disposed of. If **any** of the `std::shared_ptr` managing a resource are not properly destroyed, the resource will not be deallocated.

## std::shared_ptr and arrays

- **C++17 and earlier**: Does not have proper support for arrays
- **C++20**: Has support for arrays

## Summary

- **std::shared_ptr** = multiple owners of the same resource
- Resource deallocated when **last** `std::shared_ptr` is destroyed
- **Always copy** from existing `shared_ptr` (don't create independently)
- Use **std::make_shared()** for better performance
- Can be created from `std::unique_ptr` (but not vice versa)
- All owners must be properly destroyed or resource leaks
