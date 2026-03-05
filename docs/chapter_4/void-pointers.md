# 19.5 — Void 指针

19.5 — Void 指针
Alex
2007 年 7 月 19 日，太平洋时间下午 2:07
2023 年 9 月 29 日
void 指针
，也称为泛型指针，是一种特殊类型的指针，可以指向任何数据类型的对象！void 指针的声明方式与普通指针相同，使用 void 关键字作为指针的类型。
void* ptr {}; // ptr is a void pointer
void 指针可以指向任何数据类型的对象。
int nValue {};
float fValue {};

struct Something
{
    int n;
    float f;
};

Something sValue {};

void* ptr {};
ptr = &nValue; // valid
ptr = &fValue; // valid
ptr = &sValue; // valid
然而，由于 void 指针不知道它指向的对象类型，因此解引用 void 指针是非法的。相反，void 指针必须首先被转换为另一种指针类型，然后才能执行解引用。
int value{ 5 };
void* voidPtr{ &value };

// std::cout << *voidPtr << '\n'; // illegal: dereference of void pointer

int* intPtr{ static_cast<int*>(voidPtr) }; // however, if we cast our void pointer to an int pointer...

std::cout << *intPtr << '\n'; // then we can dereference the result
这会打印
5
下一个显而易见的问题是：如果 void 指针不知道它指向什么，我们怎么知道要将它转换为哪种类型？最终，这取决于你来跟踪。
这是一个 void 指针的用法示例。
#include <cassert>
#include <iostream>

enum class Type
{
    tInt, // note: we can't use "int" here because it's a keyword, so we'll use "tInt" instead
    tFloat,
    tCString
};

void printValue(void* ptr, Type type)
{
    switch (type)
    {
    case Type::tInt:
        std::cout << *static_cast<int*>(ptr) << '\n'; // cast to int pointer and perform indirection
        break;
    case Type::tFloat:
        std::cout << *static_cast<float*>(ptr) << '\n'; // cast to float pointer and perform indirection
        break;
    case Type::tCString:
        std::cout << static_cast<char*>(ptr) << '\n'; // cast to char pointer (no indirection)
        // std::cout will treat char* as a C-style string
        // if we were to perform indirection through the result, then we'd just print the single char that ptr is pointing to
        break;
    default:
        std::cerr << "printValue(): invalid type provided\n"; 
        assert(false && "type not found");
        break;
    }
}

int main()
{
    int nValue{ 5 };
    float fValue{ 7.5f };
    char szValue[]{ "Mollie" };

    printValue(&nValue, Type::tInt);
    printValue(&fValue, Type::tFloat);
    printValue(szValue, Type::tCString);

    return 0;
}
这个程序打印
5
7.5
Mollie
void 指针杂项
void 指针可以设置为 null 值。
void* ptr{ nullptr }; // ptr is a void pointer that is currently a null pointer
因为 void 指针不知道它指向的对象类型，所以删除 void 指针会导致未定义的行为。如果需要删除 void 指针，请先将其 `static_cast` 回适当的类型。
无法对 void 指针进行指针算术。这是因为指针算术要求指针知道它指向的对象的大小，以便它可以适当地递增或递减指针。
请注意，不存在 void 引用。这是因为 void 引用将是 `void &` 类型，并且不知道它引用的值的类型。
总结
一般来说，除非绝对必要，否则最好避免使用 void 指针，因为它们实际上允许您避免类型检查。这使您可能会无意中做一些没有意义的事情，而编译器不会抱怨。例如，以下是有效的：
int nValue{ 5 };
    printValue(&nValue, Type::tCString);
但谁知道结果会是什么！
尽管上述函数看起来是一种处理多种数据类型的巧妙方式，但 C++ 实际上提供了一种更好的方法来做同样的事情（通过函数重载），它保留了类型检查以帮助防止误用。许多其他曾经使用 void 指针来处理多种数据类型的地方，现在最好使用模板来完成，模板也提供了强大的类型检查。
然而，偶尔，您可能仍然会发现 void 指针的合理用途。只需确保首先没有更好的（更安全的）方法来使用其他语言机制来做同样的事情！
小测验时间
问题 #1
void 指针和空指针有什么区别？
显示答案
void 指针是一种可以指向任何类型对象，但不知道它指向什么类型的指针。void 指针必须明确地转换为另一种指针类型才能执行间接寻址。空指针是不指向任何地址的指针。void 指针可以是空指针。
因此，void 指针指的是指针的类型，而空指针指的是指针的值（地址）。
下一课
20.1
函数指针
返回目录
上一课
19.4
指向指针的指针和动态多维数组