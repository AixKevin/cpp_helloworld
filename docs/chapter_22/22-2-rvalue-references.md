# 22.2 — R-value references

In chapter 12, we introduced the concept of value categories (lvalues and rvalues), which is a property of expressions that helps determine whether an expression resolves to a value, function, or object.

## L-value references recap

Prior to C++11, only one type of reference existed in C++, and so it was just called a "reference". However, in C++11, it's called an l-value reference. L-value references can only be initialized with modifiable l-values.

| L-value reference | Can be initialized with | Can modify |
|-------------------|------------------------|------------|
| Non-const | Modifiable l-values | Yes |
| Non-const | Non-modifiable l-values | No |
| Non-const | R-values | No |
| To const | Modifiable l-values | No |
| To const | Non-modifiable l-values | No |
| To const | R-values | No |

## R-value references

C++11 adds a new type of reference called an **r-value reference**. An r-value reference is a reference that is designed to be initialized with an r-value (only). While an l-value reference is created using a single ampersand, an r-value reference is created using a double ampersand:

```cpp
int x{ 5 };
int& lref{ x }; // l-value reference initialized with l-value x
int&& rref{ 5 }; // r-value reference initialized with r-value 5
```

| R-value reference | Can be initialized with | Can modify |
|-------------------|------------------------|------------|
| Non-const | Modifiable l-values | No |
| Non-const | Non-modifiable l-values | No |
| Non-const | R-values | Yes |
| To const | R-values | No |

R-value references have two properties that are useful:
1. They extend the lifespan of the object they are initialized with to the lifespan of the r-value reference
2. Non-const r-value references allow you to modify the r-value

## R-value references as function parameters

R-value references are more often used as function parameters. This is most useful for function overloads when you want to have different behavior for l-value and r-value arguments.

```cpp
#include <iostream>

void fun(const int& lref) // l-value arguments will select this function
{
	std::cout << "l-value reference to const: " << lref << '\n';
}

void fun(int&& rref) // r-value arguments will select this function
{
	std::cout << "r-value reference: " << rref << '\n';
}

int main()
{
	int x{ 5 };
	fun(x); // l-value argument calls l-value version of function
	fun(5); // r-value argument calls r-value version of function

	return 0;
}
```

## Important: Rvalue reference variables are lvalues

Although variable `ref` has type `int&&`, when used in an expression it is an lvalue (as are all named variables). The type of an object and its value category are independent.

## Returning an r-value reference

You should almost never return an r-value reference, for the same reason you should almost never return an l-value reference. In most cases, you'll end up returning a hanging reference when the referenced object goes out of scope at the end of the function.

## Summary

- **R-value references** are created with `&&` and bind only to r-values
- They extend the lifetime of temporaries and allow modification
- Named r-value reference variables are actually lvalues
- Useful for function overloading to distinguish lvalue/rvalue arguments
- Should almost never be returned from functions
