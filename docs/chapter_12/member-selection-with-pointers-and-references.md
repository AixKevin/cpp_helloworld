# 13.12 — 使用指针和引用进行成员选择

13.12 — 使用指针和引用进行成员选择
Alex
2007 年 7 月 17 日，上午 11:40 PDT
2024 年 7 月 2 日
结构体及其引用的成员选择
在课程
13.7 -- 结构体、成员和成员选择介绍
中，我们展示了您可以使用成员选择运算符 (.) 来选择结构体对象中的成员
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 34, 65000.0 };

    // Use member selection operator (.) to select a member from struct object
    ++joe.age; // Joe had a birthday
    joe.wage = 68000.0; // Joe got a promotion
    
    return 0;
}
由于对象的引用就像对象本身一样，我们也可以使用成员选择运算符 (.) 来选择结构体引用中的成员
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

void printEmployee(const Employee& e)
{
    // Use member selection operator (.) to select member from reference to struct
    std::cout << "Id: " << e.id << '\n';
    std::cout << "Age: " << e.age << '\n';
    std::cout << "Wage: " << e.wage << '\n';
}

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    printEmployee(joe);

    return 0;
}
结构体指针的成员选择
但是，成员选择运算符 (.) 不能直接用于结构体指针
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << ptr.id << '\n'; // Compile error: can't use operator. with pointers

    return 0;
}
对于普通变量或引用，我们可以直接访问对象。但是，由于指针存储地址，我们首先需要对指针进行解引用以获取对象，然后才能对其进行任何操作。因此，从结构体指针访问成员的一种方法如下
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << (*ptr).id << '\n'; // Not great but works: First dereference ptr, then use member selection

    return 0;
}
然而，这有点难看，特别是我们需要用括号括住解引用操作，以便它优先于成员选择操作。
为了提供更简洁的语法，C++ 提供了一个**从指针选择成员运算符 (->)**（有时也称为**箭头运算符**），可用于从对象指针中选择成员
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << ptr->id << '\n'; // Better: use -> to select member from pointer to object

    return 0;
}
这个从指针选择成员运算符 (->) 的工作方式与成员选择运算符 (.) 相同，但在选择成员之前对指针对象进行隐式解引用。因此 `ptr->id` 等价于 `(*ptr).id`。
这个箭头运算符不仅更容易输入，而且也更不容易出错，因为间接寻址是隐式为您完成的，因此无需担心优先级问题。因此，通过指针进行成员访问时，始终使用 -> 运算符而不是 . 运算符。
最佳实践
使用指针访问成员时，请使用从指针选择成员运算符 (->) 而不是成员选择运算符 (.)。
链式 `operator->`
如果通过 `operator->` 访问的成员是指向类类型的指针，则可以在同一个表达式中再次应用 `operator->` 来访问该类类型的成员。
以下示例对此进行了说明（由读者 Luna 提供）
#include <iostream>

struct Point
{
    double x {};
    double y {};
};

struct Triangle
{
    Point* a {};
    Point* b {};
    Point* c {};
};

int main()
{
    Point a {1,2};
    Point b {3,7};
    Point c {10,2};

    Triangle tr { &a, &b, &c };
    Triangle* ptr {&tr};

    // ptr is a pointer to a Triangle, which contains members that are pointers to a Point
    // To access member y of Point c of the Triangle pointed to by ptr, the following are equivalent:

    // access via operator.
    std::cout << (*(*ptr).c).y << '\n'; // ugly!

    // access via operator->
    std::cout << ptr -> c -> y << '\n'; // much nicer
}
当连续使用多个 `operator->` 时（例如 `ptr->c->y`），表达式可能难以阅读。在成员和 `operator->` 之间添加空格（例如 `ptr -> c -> y`）可以使其更容易区分正在访问的成员和运算符。
混合使用指向成员的指针和非指针
成员选择运算符始终应用于当前选择的变量。如果您混合使用指针和普通成员变量，您会看到成员选择中 . 和 -> 都按顺序使用
#include <iostream>
#include <string>

struct Paw
{
    int claws{};
};
 
struct Animal
{
    std::string name{};
    Paw paw{};
};
 
int main()
{
    Animal puma{ "Puma", { 5 } };
 
    Animal* ptr{ &puma };
 
    // ptr is a pointer, use ->
    // paw is not a pointer, use .

    std::cout << (ptr->paw).claws << '\n';
 
    return 0;
}
请注意，在 `(ptr->paw).claws` 的情况下，括号不是必需的，因为 `operator->` 和 `operator.` 都按从左到右的顺序求值，但这确实稍微有助于提高可读性。
下一课
13.13
类模板
返回目录
上一课
13.11
结构体杂项