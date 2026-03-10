# 22.5 — std::unique_ptr

`std::unique_ptr` is the C++11 replacement for `std::auto_ptr`. It should be used to manage any dynamically allocated object that is **not shared by multiple objects**. That is, `std::unique_ptr` should completely own the object it manages.

## Basic usage

```cpp
#include <memory> // for std::unique_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	std::unique_ptr<Resource> res{ new Resource() };
	return 0;
} // res goes out of scope here, and the Resource is destroyed
```

## Move semantics

Unlike `std::auto_ptr`, `std::unique_ptr` properly implements move semantics. Copy semantics are disabled.

```cpp
std::unique_ptr<Resource> res1{ new Resource{} };
std::unique_ptr<Resource> res2{};

// res2 = res1; // Won't compile: copy assignment is disabled
res2 = std::move(res1); // res2 assumes ownership, res1 is set to null
```

## Accessing the managed object

`std::unique_ptr` has overloaded `operator*` and `operator->`. Always check if it's valid first:

```cpp
if (res) // use implicit cast to bool
	std::cout << *res << '\n';
```

## std::unique_ptr and arrays

`std::unique_ptr` is smart enough to know whether to use scalar delete or array delete. However, **favor `std::array`, `std::vector`, or `std::string`** over smart pointers managing arrays.

## std::make_unique (C++14)

```cpp
auto f1{ std::make_unique<Fraction>(3, 5) }; // Single object
auto f2{ std::make_unique<Fraction[]>(4) };  // Array
```

**Best practice**: Use `std::make_unique()` instead of creating `std::unique_ptr` and using `new` yourself. It's simpler, safer, and avoids exception safety issues.

## Returning std::unique_ptr from a function

`std::unique_ptr` can be safely returned from a function by value:

```cpp
std::unique_ptr<Resource> createResource()
{
     return std::make_unique<Resource>();
}
```

## Passing std::unique_ptr to a function

- **To transfer ownership**: Pass by value (use `std::move`)
- **To use without ownership**: Pass the resource itself (by pointer or reference)

```cpp
void useResource(const Resource* res) // Better - function is agnostic
{
	if (res)
		std::cout << *res << '\n';
}

// Call with:
useResource(ptr.get()); // get() returns raw pointer
```

## std::unique_ptr and classes

You can use `std::unique_ptr` as a composition member. The destructor will automatically clean up.

## Misusing std::unique_ptr

**Don't**:
1. Let multiple objects manage the same resource
2. Manually delete the resource out from underneath the `std::unique_ptr`

Both cases lead to undefined behavior. `std::make_unique()` prevents these issues.

## Summary

- **std::unique_ptr** = exclusive ownership of a dynamically allocated resource
- **Copy semantics disabled**, move semantics enabled
- Use **std::make_unique()** (C++14) for creation
- Can be returned by value safely
- Pass raw pointer (`get()`) when function doesn't need ownership
- Never let multiple objects manage the same resource
