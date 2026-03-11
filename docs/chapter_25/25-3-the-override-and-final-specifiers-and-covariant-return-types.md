# 25.3 — The override and final specifiers, and covariant return types

To address some common challenges with inheritance, C++ has two inheritance-related identifiers: `override` and `final`. Note that these identifiers are not keywords -- they are normal words that have special meaning only when used in certain contexts.

## The override specifier

As we mentioned in the previous lesson, a derived class virtual function is only considered an override if its signature and return types match exactly. That can lead to inadvertent issues, where a function that was intended to be an override actually isn't.

To help address the issue of functions that are meant to be overrides but aren't, the `override` specifier can be applied to any virtual function to tell the compiler to enforce that the function is an override. The `override` specifier is placed at the end of a member function declaration (in the same place where a function-level `const` goes). If a member function is `const` and an override, the `const` must come before `override`.

If a function marked as `override` does not override a base class function (or is applied to a non-virtual function), the compiler will flag the function as an error.

Because there is no performance penalty for using the override specifier and it helps ensure you've actually overridden the function you think you have, all virtual override functions should be tagged using the override specifier. Additionally, because the override specifier implies virtual, there's no need to tag functions using the override specifier with the virtual keyword.

**Best practice**

Use the virtual keyword on virtual functions in a base class.

Use the override specifier (but not the virtual keyword) on override functions in derived classes. This includes virtual destructors.

**Rule**

If a member function is both `const` and an `override`, the `const` must be listed first. `const override` is correct, `override const` is not.

## The final specifier

There may be cases where you don't want someone to be able to override a virtual function, or inherit from a class. The final specifier can be used to tell the compiler to enforce this. If the user tries to override a function or inherit from a class that has been specified as final, the compiler will give a compile error.

In the case where we want to restrict the user from overriding a function, the **final specifier** is used in the same place the override specifier is.

In the case where we want to prevent inheriting from a class, the final specifier is applied after the class name.

## Covariant return types

There is one special case in which a derived class virtual function override can have a different return type than the base class and still be considered a matching override. If the return type of a virtual function is a pointer or a reference to some class, override functions can return a pointer or reference to a derived class. These are called **covariant return types**.
