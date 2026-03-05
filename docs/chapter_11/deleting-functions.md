# 11.4 — 删除函数

11.4 — 删除函数
Alex
2023年10月10日，太平洋夏令时下午1:26
2023年12月28日
在某些情况下，当使用特定类型的值调用函数时，可能会编写出行为不符合预期的函数。
考虑以下示例
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(5);    // okay: prints 5
    printInt('a');  // prints 97 -- does this make sense?
    printInt(true); // print 1 -- does this make sense?
    
    return 0;
}
此示例输出：
5
97
1
虽然
printInt(5)
显然没问题，但其他两个对
printInt()
的调用则更值得商榷。对于
printInt('a')
，编译器会确定它可以将
'a'
提升为 int 值
97
，以便将函数调用与函数定义匹配。它会将
true
提升为 int 值
1
。而且它会毫无抱怨地这样做。
假设我们认为用
char
或
bool
类型的值调用
printInt()
没有意义。我们能做些什么呢？
使用
= delete
说明符删除函数
在某些情况下，我们明确不希望某个函数被调用，我们可以通过使用
= delete
说明符将该函数定义为已删除。如果编译器将函数调用与已删除的函数匹配，编译将因编译错误而中止。
这是上述使用此语法更新后的版本：
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

void printInt(char) = delete; // calls to this function will halt compilation
void printInt(bool) = delete; // calls to this function will halt compilation

int main()
{
    printInt(97);   // okay

    printInt('a');  // compile error: function deleted
    printInt(true); // compile error: function deleted

    printInt(5.0);  // compile error: ambiguous match
    
    return 0;
}
让我们快速查看其中一些情况。首先，
printInt('a')
直接匹配
printInt(char)
，而后者已被删除。因此，编译器会产生一个编译错误。
printInt(true)
直接匹配
printInt(bool)
，而后者已被删除，因此也会产生一个编译错误。
printInt(5.0)
是一个有趣的案例，可能会产生意想不到的结果。首先，编译器检查是否存在精确匹配的
printInt(double)
。不存在。接下来，编译器尝试找到最佳匹配。尽管
printInt(int)
是唯一未删除的函数，但已删除的函数在函数重载解析中仍被视为候选者。由于这些函数中没有一个明确是最佳匹配，因此编译器将发出一个歧义匹配编译错误。
关键见解
= delete
意味着“我禁止这样做”，而不是“这不存在”。
已删除的函数参与函数重载解析的所有阶段（不仅仅是精确匹配阶段）。如果选择了已删除的函数，则会导致编译错误。
致进阶读者
其他类型的函数也可以类似地删除。
我们在第
14.14 课 -- 复制构造函数介绍
中讨论删除成员函数，在第
11.7 课 -- 函数模板实例化
中讨论删除函数模板特化。
删除所有不匹配的重载
高级
删除一堆单独的函数重载效果很好，但可能很冗长。有时我们希望某个函数只被参数类型与函数参数精确匹配的参数调用。我们可以通过使用函数模板（在即将到来的第
11.6 课 -- 函数模板
中介绍）来实现这一点，如下所示：
#include <iostream>

// This function will take precedence for arguments of type int
void printInt(int x)
{
    std::cout << x << '\n';
}

// This function template will take precedence for arguments of other types
// Since this function template is deleted, calls to it will halt compilation
template <typename T>
void printInt(T x) = delete;

int main()
{
    printInt(97);   // okay
    printInt('a');  // compile error
    printInt(true); // compile error
    
    return 0;
}
下一课
11.5
默认参数
返回目录
上一课
11.3
函数重载解析和歧义匹配