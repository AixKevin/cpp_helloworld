# 25.10 — Dynamic casting

Way back in lesson 10.6 -- Explicit type conversion (casting) and static_cast, we examined the concept of casting, and the use of static_cast to convert variables from one type to another.

In this lesson, we'll continue by examining another type of cast: dynamic_cast.

## The need for dynamic_cast

When dealing with polymorphism, you'll often encounter cases where you have a pointer to a base class, but you want to access some information that exists only in a derived class.

We know that C++ will implicitly let you convert a Derived pointer into a Base pointer. This process is sometimes called **upcasting**. However, what if there was a way to convert a Base pointer back into a Derived pointer? Then we could call derived-class-specific functions directly using that pointer, and not have to worry about virtual function resolution at all.

## dynamic_cast

C++ provides a casting operator named **dynamic_cast** that can be used for just this purpose. Although dynamic casts have a few different capabilities, by far the most common use for dynamic casting is for converting base-class pointers into derived-class pointers. This process is called **downcasting**.

Using dynamic_cast works just like static_cast.

## dynamic_cast failure

The above example works because the base pointer is actually pointing to a Derived object, so converting it into a Derived pointer is successful.

However, we've made quite a dangerous assumption: that the base pointer is pointing to a Derived object. What if it wasn't pointing to a Derived object? In that case, when we try to dynamic_cast that to a Derived, it will fail, because the conversion can't be made.

If a dynamic_cast fails, the result of the conversion will be a null pointer.

**Rule**

Always ensure your dynamic casts actually succeeded by checking for a null pointer result.

Note that because dynamic_cast does some consistency checking at runtime (to ensure the conversion can be made), use of dynamic_cast does incur a performance penalty.

Also note that there are several cases where downcasting using dynamic_cast will not work:

1. With protected or private inheritance.
2. For classes that do not declare or inherit any virtual functions (and thus don't have a virtual table).
3. In certain cases involving virtual base classes.

## Downcasting with static_cast

It turns out that downcasting can also be done with static_cast. The main difference is that static_cast does no runtime type checking to ensure that what you're doing makes sense. This makes using static_cast faster, but more dangerous. If you cast a Base* to a Derived*, it will "succeed" even if the Base pointer isn't pointing to a Derived object. This will result in undefined behavior when you try to access the resulting Derived pointer.

## dynamic_cast and references

Although all of the above examples show dynamic casting of pointers (which is more common), dynamic_cast can also be used for references. This works analogously to how dynamic_cast works with pointers.

Because C++ does not have a "null reference", dynamic_cast can't return a null reference upon failure. Instead, if the dynamic_cast of a reference fails, an exception of type std::bad_cast is thrown.

## dynamic_cast vs static_cast

New programmers are sometimes confused about when to use static_cast vs dynamic_cast. The answer is quite simple: use static_cast unless you're downcasting, in which case dynamic_cast is usually a better choice. However, you should also consider avoiding casting altogether and just use virtual functions.

## Downcasting vs virtual functions

There are some developers who believe dynamic_cast is evil and indicative of a bad class design. Instead, these programmers say you should use virtual functions.

In general, using a virtual function *should* be preferred over downcasting. However, there are times when downcasting is the better choice:

- When you can not modify the base class to add a virtual function (e.g. because the base class is part of the standard library)
- When you need access to something that is derived-class specific (e.g. an access function that only exists in the derived class)
- When adding a virtual function to your base class doesn't make sense (e.g. there is no appropriate value for the base class to return). Using a pure virtual function may be an option here if you don't need to instantiate the base class.

**A warning about dynamic_cast and RTTI**

Run-time type information (RTTI) is a feature of C++ that exposes information about an object's data type at runtime. This capability is leveraged by dynamic_cast. Because RTTI has a pretty significant space performance cost, some compilers allow you to turn RTTI off as an optimization. Needless to say, if you do this, dynamic_cast won't function correctly.
