# 22.x — Chapter 22 summary and quiz

## Chapter Summary

### Smart Pointers

A **smart pointer class** is a composition class that manages dynamically allocated memory and ensures it gets deleted when the smart pointer goes out of scope.

### Copy vs Move Semantics

| Copy Semantics | Move Semantics |
|----------------|----------------|
| Makes a copy of the object | Transfers ownership |
| Uses copy constructor/assignment | Uses move constructor/assignment |
| Safe for l-values | Safe for r-values (temporaries) |

### R-value References

- Created with double ampersand: `int&& rref{ 5 };`
- Binds only to r-values
- Extends lifetime of temporaries
- Allows modification of r-values
- **Named r-value reference variables are lvalues!**

### Key Insights

> **Move Semantics Rationale**: If the argument is an l-value, we must copy it (it may be used again). If the argument is an r-value (temporary), we can transfer its resources (it will be destroyed anyway).

> **Move Constructor Best Practice**: Always leave the moved-from object in a valid state.

### std::move

- Converts an l-value to an r-value reference
- Allows invoking move semantics on l-values
- After `std::move()`, the object is in a valid but unspecified state

### Smart Pointer Comparison

| Smart Pointer | Ownership | Use Case |
|---------------|-----------|----------|
| `std::unique_ptr` | Single, exclusive | Default choice for dynamic memory |
| `std::shared_ptr` | Multiple, shared | When multiple owners needed |
| `std::weak_ptr` | None (observer) | Break circular references |
| `std::auto_ptr` | Deprecated | **Don't use** (removed in C++17) |

### Best Practices

1. **std::unique_ptr** should be your default smart pointer
2. Use **std::make_unique()** / **std::make_shared()** for creation
3. Use **std::move()** to transfer ownership
4. Use **std::weak_ptr** to break circular references
5. Follow the **Rule of Five**: If any of copy/move/destructor are defined or deleted, all should be

### Quiz Answers

**1a) std::unique_ptr**: Use when you want a smart pointer to manage a dynamic object that is not going to be shared.

**1b) std::shared_ptr**: Use when you want a smart pointer to manage a dynamic object that may be shared. The object won't be deallocated until all `std::shared_ptr` holding it are destroyed.

**1c) std::weak_ptr**: Use when you want access to an object managed by `std::shared_ptr`, but don't want the lifetime tied to the `std::weak_ptr`.

**1d) std::auto_ptr**: Deprecated and removed in C++17. Should not be used.

**2) Why move semantics focuses on r-values**: Because r-values are temporary, we know they will be destroyed after use. When passing/returning an r-value, it's wasteful to copy and destroy the original. Instead, we can move (steal) the resources, which is more efficient.

**3) Problem with independent shared_ptr creation**: Creating two `std::shared_ptr` from the same raw pointer means they're unaware of each other. When one goes out of scope, it deallocates the resource, leaving the other with a dangling pointer. **Solution**: Create from existing `shared_ptr` or use `std::make_shared()`.
