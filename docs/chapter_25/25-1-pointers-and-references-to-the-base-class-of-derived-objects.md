# 25.1 — Pointers and references to the base class of derived objects

In the previous chapter, you learned all about how to use inheritance to derive new classes from existing classes. In this chapter, we are going to focus on one of the most important and powerful aspects of inheritance -- virtual functions.

But before we discuss what virtual functions are, let's first set the table for why we need them.

In the chapter on construction of derived classes, you learned that when you create a derived class, it is composed of multiple parts: one part for each inherited class, and a part for itself.

For example, here's a simple case:

```cpp
#include <string_view>

class Base
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value{ value }
    {
    }

    std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived: public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

    std::string_view getName() const { return "Derived"; }
    int getValueDoubled() const { return m_value * 2; }
};
```

When we create a Derived object, it contains a Base part (which is constructed first), and a Derived part (which is constructed second). Remember that inheritance implies an is-a relationship between two classes. Since a Derived is-a Base, it is appropriate that Derived contain a Base part.

**Pointers, references, and derived classes**

It should be fairly intuitive that we can set Derived pointers and references to Derived objects. However, since Derived has a Base part, a more interesting question is whether C++ will let us set a Base pointer or reference to a Derived object. It turns out, we can!

```cpp
#include <iostream>

int main()
{
    Derived derived{ 5 };

    // These are both legal!
    Base& rBase{ derived }; // rBase is an lvalue reference (not an rvalue reference)
    Base* pBase{ &derived };

    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';
    std::cout << "rBase is a " << rBase.getName() << " and has value " << rBase.getValue() << '\n';
    std::cout << "pBase is a " << pBase->getName() << " and has value " << pBase->getValue() << '\n';

    return 0;
}
```

This produces the result:

derived is a Derived and has value 5
rBase is a Base and has value 5
pBase is a Base and has value 5

This result may not be quite what you were expecting at first!

It turns out that because rBase and pBase are a Base reference and pointer, they can only see members of Base (or any classes that Base inherited). So even though Derived::getName() shadows (hides) Base::getName() for Derived objects, the Base pointer/reference can not see Derived::getName(). Consequently, they call Base::getName(), which is why rBase and pBase report that they are a Base rather than a Derived.

Note that this also means it is not possible to call Derived::getValueDoubled() using rBase or pBase. They are unable to see anything in Derived.

**Use for pointers and references to base classes**

Now you might be saying, "The above examples seem kind of silly. Why would I set a pointer or reference to the base class of a derived object when I can just use the derived object?" It turns out that there are quite a few good reasons.

First, let's say you wanted to write a function that printed an animal's name and sound. Without using a pointer to a base class, you'd have to write it using overloaded functions. However, because Cat and Dog are derived from Animal, Cat and Dog have an Animal part. Therefore, it makes sense that we should be able to do something like this:

```cpp
void report(const Animal& rAnimal)
{
    std::cout << rAnimal.getName() << " says " << rAnimal.speak() << '\n';
}
```

This would let us pass in any class derived from Animal, even ones that we created after we wrote the function! Instead of one function per derived class, we get one function that works with all classes derived from Animal!

The problem is, of course, that because rAnimal is an Animal reference, `rAnimal.speak()` will call Animal::speak() instead of the derived version of speak().

Second, let's say you had 3 cats and 3 dogs that you wanted to keep in an array for easy access. Because arrays can only hold objects of one type, without a pointer or reference to a base class, you'd have to create a different array for each derived type. However, because both Cat and Dog are derived from Animal, it makes sense that we should be able to do something like this:

```cpp
// Set up an array of pointers to animals, and set those pointers to our Cat and Dog objects
const auto animals{ std::to_array<const Animal*>({&fred, &garbo, &misty, &pooky, &truffle, &zeke }) };

for (const auto animal : animals)
{
    std::cout << animal->getName() << " says " << animal->speak() << '\n';
}
```

While this compiles and executes, unfortunately the fact that each element of array "animals" is a pointer to an Animal means that `animal->speak()` will call Animal::speak() instead of the derived class version of speak() that we want.

Although both of these techniques could save us a lot of time and energy, they have the same problem. The pointer or reference to the base class calls the base version of the function rather than the derived version. If only there was some way to make those base pointers call the derived version of a function instead of the base version…

Want to take a guess what virtual functions are for? :)
