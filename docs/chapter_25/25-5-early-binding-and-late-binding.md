# 25.5 — Early binding and late binding

In this lesson, we are going to take a closer look at how virtual functions are implemented. While this information is not strictly necessary to effectively use virtual functions, it is interesting.

## Binding and dispatching

Our programs contain many names (identifiers, keywords, etc…). Each name has a set of associated properties.

In general programming, **binding** is the process of associating names with such properties. **Function binding** (or **method binding**) is the process that determines what function definition is associated with a function call. The process of actually invoking a bound function is called **dispatching**.

## Early binding

Most of the function calls the compiler encounters will be direct function calls. A direct function call is a statement that directly calls a function.

In C++, when a direct call is made to a non-member function or a non-virtual member function, the compiler can determine which function definition should be matched to the call. This is sometimes called **early binding** (or **static binding**), as it can be performed at compile-time. The compiler (or linker) can then generate machine language instructions that tells the CPU to jump directly to the address of the function.

Calls to overloaded functions and function templates can also be resolved at compile-time.

## Late binding

In some cases, a function call can't be resolved until runtime. In C++, this is sometimes known as **late binding** (or in the case of virtual function resolution, **dynamic dispatch**).

In C++, one way to get late binding is to use function pointers. To review function pointers briefly, a function pointer is a type of pointer that points to a function instead of a variable. The function that a function pointer points to can be called by using the function call operator `()` on the pointer.

Calling a function via a function pointer is also known as an indirect function call. At the point where the function is called, the compiler does not know at compile-time what function is being called. Instead, at runtime, an indirect function call is made to whatever function exists at the address held by the function pointer.

Late binding is slightly less efficient since it involves an extra level of indirection. With early binding, the CPU can jump directly to the function's address. With late binding, the program has to read the address held in the pointer and then jump to that address. This involves one extra step, making it slightly slower. However, the advantage of late binding is that it is more flexible than early binding, because decisions about what function to call do not need to be made until runtime.

In the next lesson, we'll take a look at how late binding is used to implement virtual functions.
