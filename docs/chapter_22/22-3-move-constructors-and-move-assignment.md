# 22.3 — Move constructors and move assignment

C++11 defines two new functions in service of move semantics: a **move constructor** and a **move assignment operator**. Whereas the goal of the copy constructor and copy assignment is to make a copy of one object to another, the goal of the move constructor and move assignment is to **move ownership of the resources from one object to another** (which is typically much less expensive than making a copy).

## Defining move constructors and move assignment

The copy flavors of these functions take a `const l-value reference` parameter, while the move flavors use `non-const rvalue reference` parameters.

```cpp
template<typename T>
class Auto_ptr4
{
	T* m_ptr {};
public:
	Auto_ptr4(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr4()
	{
		delete m_ptr;
	}

	// Copy constructor - Do deep copy
	Auto_ptr4(const Auto_ptr4& a)
	{
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}

	// Move constructor - Transfer ownership
	Auto_ptr4(Auto_ptr4&& a) noexcept
		: m_ptr { a.m_ptr }
	{
		a.m_ptr = nullptr; // Leave source in valid state
	}

	// Copy assignment - Do deep copy
	Auto_ptr4& operator=(const Auto_ptr4& a)
	{
		if (&a == this)
			return *this;
		delete m_ptr;
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
		return *this;
	}

	// Move assignment - Transfer ownership
	Auto_ptr4& operator=(Auto_ptr4&& a) noexcept
	{
		if (&a == this)
			return *this;
		delete m_ptr;
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr; // Leave source in valid state
		return *this;
	}
};
```

## When are move constructor and move assignment called?

The move constructor and move assignment are called when:
- Those functions have been defined
- The argument for construction or assignment is an rvalue

The copy constructor and copy assignment are used otherwise.

## Implicit move constructor and move assignment

The compiler will create an implicit move constructor and move assignment if:
- There are no user-declared copy constructors or copy assignment operators
- There are no user-declared move constructors or move assignment operators
- There is no user-declared destructor

**Warning**: The implicit move constructor and move assignment will **copy pointers, not move them**! If you want to move a pointer member, you will need to define the move constructor and move assignment yourself.

## Key insight behind move semantics

If we construct an object where the argument is an **l-value**, we can only copy it (we can't assume it's safe to alter the l-value).

If we construct an object where the argument is an **r-value**, we know that r-value is just a temporary. Instead of copying it, we can simply transfer its resources. This is safe because the temporary will be destroyed at the end of the expression anyway!

> **Key insight**: Move semantics is an optimization opportunity.

## Move functions should leave both objects in a valid state

When implementing move semantics, it is important to ensure the **moved-from object is left in a valid state**, so that it will destruct properly (without creating undefined behavior).

## Automatic l-values returned by value may be moved

The C++ specification has a special rule that says **automatic objects returned from a function by value can be moved even if they are l-values**. This makes sense since the variable was going to be destroyed at the end of the function anyway!

## Disabling copying

In move-enabled classes, it is sometimes desirable to delete the copy constructor and copy assignment functions:

```cpp
Auto_ptr5(const Auto_ptr5& a) = delete;
Auto_ptr5& operator=(const Auto_ptr5& a) = delete;
```

## Rule of Five

The **rule of five** says that if the copy constructor, copy assignment, move constructor, move assignment, or destructor are defined or deleted, then **each of those functions should be defined or deleted**.

## Performance comparison

In a test with a dynamic array of 1 million integers:
- **Copy semantics**: 0.00825559 seconds
- **Move semantics**: 0.0056 seconds
- **Improvement**: ~32% faster!

## Summary

- **Move constructor/assignment** transfer ownership instead of copying
- Use `noexcept` for move operations
- Always leave moved-from objects in a valid state
- Compiler can move l-value return values automatically
- Follow the **rule of five** for proper resource management
- Move semantics provides significant performance improvements
