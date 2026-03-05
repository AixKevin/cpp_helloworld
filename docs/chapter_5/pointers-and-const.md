# 12.9 — 指针和 const

12.9 — 指针和 const
Alex
2007年7月16日，下午1:40 PDT
2025年2月12日
考虑以下代码片段
int main()
{
    int x { 5 };
    int* ptr { &x }; // ptr is a normal (non-const) pointer

    int y { 6 };
    ptr = &y; // we can point at another value

    *ptr = 7; // we can change the value at the address being held

    return 0;
}
对于普通（非 const）指针，我们可以改变指针指向的内容（通过给指针赋值一个新地址来持有）或者改变所持地址的值（通过给解引用指针赋值一个新值）。
然而，如果我们要指向的值是 const，会发生什么？
int main()
{
    const int x { 5 }; // x is now const
    int* ptr { &x };   // compile error: cannot convert from const int* to int*

    return 0;
}
上面的片段将无法编译——我们不能将普通指针设置为指向 const 变量。这是有道理的：const 变量是其值不能改变的变量。允许程序员将非 const 指针设置为 const 值将允许程序员解引用指针并改变该值。这将违反变量的 const 属性。
指向 const 值 的指针
一个
指向 const 值 的指针
（有时简称
pointer to const
）是一个（非 const）指针，它指向一个常量值。
要声明一个指向 const 值 的指针，请在指针的数据类型前使用
const
关键字
int main()
{
    const int x{ 5 };
    const int* ptr { &x }; // okay: ptr is pointing to a "const int"

    *ptr = 6; // not allowed: we can't change a const value

    return 0;
}
在上面的例子中，
ptr
指向一个
const int
。因为被指向的数据类型是 const，所以被指向的值不能改变。
然而，因为指向 const 的指针本身不是 const（它只是指向一个 const 值），我们可以通过给指针赋值一个新地址来改变指针指向的内容
int main()
{
    const int x{ 5 };
    const int* ptr { &x }; // ptr points to const int x

    const int y{ 6 };
    ptr = &y; // okay: ptr now points at const int y

    return 0;
}
就像 const 引用一样，指向 const 的指针也可以指向非 const 变量。指向 const 的指针将所指向的值视为常量，无论该地址处的对象最初是否定义为 const
int main()
{
    int x{ 5 }; // non-const
    const int* ptr { &x }; // ptr points to a "const int"

    *ptr = 6;  // not allowed: ptr points to a "const int" so we can't change the value through ptr
    x = 6; // allowed: the value is still non-const when accessed through non-const identifier x

    return 0;
}
Const 指针
我们也可以使指针本身是常量。一个
const 指针
是一个在初始化后其地址不能改变的指针。
要声明一个 const 指针，请在指针声明中的星号后使用
const
关键字
int main()
{
    int x{ 5 };
    int* const ptr { &x }; // const after the asterisk means this is a const pointer

    return 0;
}
在上述情况下，
ptr
是一个指向（非 const）int 值的 const 指针。
就像普通的 const 变量一样，const 指针必须在定义时初始化，并且该值不能通过赋值改变
int main()
{
    int x{ 5 };
    int y{ 6 };

    int* const ptr { &x }; // okay: the const pointer is initialized to the address of x
    ptr = &y; // error: once initialized, a const pointer can not be changed.

    return 0;
}
然而，因为被指向的
值
是非 const 的，所以可以通过解引用 const 指针来改变被指向的值
int main()
{
    int x{ 5 };
    int* const ptr { &x }; // ptr will always point to x

    *ptr = 6; // okay: the value being pointed to is non-const

    return 0;
}
指向 const 值 的 Const 指针
最后，可以通过在类型前和星号后都使用
const
关键字来声明一个
指向 const 值 的 const 指针
int main()
{
    int value { 5 };
    const int* const ptr { &value }; // a const pointer to a const value

    return 0;
}
一个指向 const 值 的 const 指针不能改变其地址，也不能通过该指针改变它所指向的值。它只能被解引用以获取它所指向的值。
指针和 const 回顾
总而言之，你只需要记住4条规则，它们非常符合逻辑
非 const 指针（例如
int* ptr
）可以被赋值另一个地址以改变它指向的内容。
const 指针（例如
int* const ptr
）总是指向相同的地址，并且此地址不能改变。
指向非 const 值 的指针（例如
int* ptr
）可以改变它所指向的值。这些不能指向 const 值。
指向 const 值 的指针（例如
const int* ptr
）在通过指针访问时将该值视为 const，因此不能改变它所指向的值。这些可以指向 const 或非 const 左值（但不能指向右值，因为它们没有地址）。
保持声明语法清晰可能有些挑战
星号前的
const
（例如
const int* ptr
）与被指向的类型相关联。因此，这是一个指向 const 值 的指针，并且该值不能通过指针修改。
星号后的
const
（例如
int* const ptr
）与指针本身相关联。因此，此指针不能被赋值新地址。
int main()
{
    int v{ 5 };
   
    int* ptr0 { &v };             // points to an "int" but is not const itself.  We can modify the value or the address.
    const int* ptr1 { &v };       // points to a "const int" but is not const itself.  We can only modify the address.
    int* const ptr2 { &v };       // points to an "int" and is const itself.   We can only modify the value.
    const int* const ptr3 { &v }; // points to a "const int" and is const itself.  We can't modify the value nor the address.

    // if the const is on the left side of the *, the const belongs to the value
    // if the const is on the right side of the *, the const belongs to the pointer

    return 0;
}
下一课
12.10
按地址传递
返回目录
上一课
12.8
空指针