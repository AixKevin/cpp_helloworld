# 22.7 — Circular dependency issues with std::shared_ptr and std::weak_ptr

## The problem: Circular references

When `std::shared_ptr` objects form a **circular reference**, the resources may never be deallocated.

```cpp
class Person
{
	std::string m_name;
	std::shared_ptr<Person> m_partner;

public:
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person() { std::cout << m_name << " destroyed\n"; }
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") };
	auto ricky { std::make_shared<Person>("Ricky") };
	
	// Partner them up - each points to the other
	lucy->m_partner = ricky;
	ricky->m_partner = lucy;
	
	return 0; // NEITHER is destroyed!
}
```

**Output**:
```
Lucy created
Ricky created
Lucy is now partnered with Ricky
// No destruction messages!
```

### Why this happens

- When `ricky` goes out of scope, it sees Lucy's `m_partner` still points to it → doesn't deallocate
- When `lucy` goes out of scope, it sees Ricky's `m_partner` still points to it → doesn't deallocate
- Result: **Memory leak** - both objects remain allocated

## Solution: std::weak_ptr

`std::weak_ptr` is an **observer** - it can observe and access the same object as a `std::shared_ptr`, but it is **not considered an owner**.

```cpp
class Person
{
	std::string m_name;
	std::weak_ptr<Person> m_partner; // Changed to weak_ptr!

public:
	// ... same as before ...
	
	std::shared_ptr<Person> getPartner() const 
	{ 
		return m_partner.lock(); // Convert weak_ptr to shared_ptr
	}
};
```

Now the program properly destroys both objects.

## Using std::weak_ptr

### Converting to shared_ptr

`std::weak_ptr` cannot be used directly (no `operator->`). Use `lock()` to convert it:

```cpp
auto partner = ricky->getPartner(); // Returns shared_ptr
std::cout << partner->getName() << '\n';
```

### Checking validity with expired()

`std::weak_ptr` can determine if it's pointing to a valid object:

```cpp
if (weak.expired()) // true if resource already destroyed
{
	// Handle invalid case
}
else
{
	auto shared = weak.lock(); // Safe to use
}
```

### Comparison with raw pointers

| Raw Pointer | std::weak_ptr |
|-------------|---------------|
| Can be dangling | Can detect expiration |
| No way to check validity | `expired()` tells you |
| Dereferencing = undefined behavior | `lock()` returns nullptr if expired |

## When to use each pointer type

| Pointer Type | Use Case |
|--------------|----------|
| `std::unique_ptr` | Single owner, exclusive ownership |
| `std::shared_ptr` | Multiple owners, shared ownership |
| `std::weak_ptr` | Observer, break circular references |

## Summary

- **Circular references** with `std::shared_ptr` cause memory leaks
- **std::weak_ptr** is an observer that doesn't affect reference counting
- Use `lock()` to convert `weak_ptr` to `shared_ptr` for access
- Use `expired()` to check if the resource is still valid
- `std::weak_ptr` provides safety that raw pointers lack
