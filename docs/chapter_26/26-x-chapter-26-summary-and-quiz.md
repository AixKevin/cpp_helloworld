# 26.x — Chapter 26 summary and quiz

Templates allow us to write functions or classes using placeholder types, so that we can stencil out identical versions of the function or class using different types. A function or class that has been instantiated is called a function or class instance.

All template functions or classes must start with a template parameter declaration that tells the compiler that the following function or class is a template function or class. Within the template parameter declaration, the template type parameters or expression parameters are specified. Template type parameters are just placeholder types, normally named T, T1, T2, or other single letter names (e.g. S). Expression parameters are usually integral types, but can be a pointer or reference to a function, class object, or member function.

Splitting up template class definition and member function definitions doesn't work like normal classes -- you can't put your class definition in a header and member function definitions in a .cpp file. It's usually best to keep all of them in a header file, with the member function definitions underneath the class.

Template specialization can be used when we want to override the default behavior from the templated function or class for a specific type. If all types are overridden, this is called full specialization. Classes also support partial specialization, where only some of the templated parameters are specialized. Functions can not be partially specialized.

Many classes in the C++ standard library use templates, including std::array and std::vector. Templates are often used for implementing container classes, so a container can be written once and used with any appropriate type.

## Quiz time

**Question 1**: It's sometimes useful to define data that travels in pairs. Write a templated class named Pair1 that allows the user to define one template type that is used for both values in the pair.

**Question 2**: Write a Pair class that allows you to specify separate types for each of the two values in the pair.

**Question 3**: A string-value pair is a special type of pair where the first value is always a string type, and the second value can be any type. Write a template class named StringValuePair that inherits from a partially specialized Pair class (using std::string as the first type, and allowing the user to specify the second type).
