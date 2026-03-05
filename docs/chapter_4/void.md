# 4.2 — Void

4.2 — Void
Alex
2015年2月11日，下午5:55 PST
2023年8月29日
Void 是最容易解释的数据类型。简单来说，
void
意味着“无类型”！
Void 是我们第一个不完整类型的例子。
不完整类型
是已声明但尚未定义的类型。编译器知道这类类型的存在，但没有足够的信息来确定为该类型的对象分配多少内存。
void
是故意不完整的，因为它表示缺乏类型，因此无法定义。
不完整类型不能实例化
void value; // won't work, variables can't be defined with incomplete type void
Void 通常用于几种不同的上下文。
不返回值的函数
最常见的是，
void
用于表示函数不返回值。
void writeValue(int x) // void here means no return value
{
    std::cout << "The value of x is: " << x << '\n';
    // no return statement, because this function doesn't return a value
}
如果你在这种函数中尝试使用 return 语句返回值，将会导致编译错误。
void noReturn(int x) // void here means no return value
{
    std::cout << "The value of x is: " << x << '\n';

    return 5; // error
}
在 Visual Studio 2017 中，这会产生以下错误：
error C2562: 'noReturn': 'void' function returning a value
已弃用：不带参数的函数
在 C 语言中，void 用于表示函数不带任何参数。
int getValue(void) // void here means no parameters
{
    int x{};
    std::cin >> x;

    return x;
}
尽管这在 C++ 中可以编译（出于向后兼容性原因），但这种使用关键字
void
的方式在 C++ 中被认为是已弃用的。以下代码是等效的，并且在 C++ 中更受推荐：
int getValue() // empty function parameters is an implicit void
{
    int x{};
    std::cin >> x;

    return x;
}
最佳实践
使用空参数列表而不是
void
来表示函数没有参数。
void 的其他用途
void 关键字在 C++ 中还有第三种（更高级的）用途，我们将在
19.5 — Void 指针
一节中介绍。由于我们尚未介绍什么是指针，因此你暂时无需担心这种情况。
让我们继续！
下一课
4.3
对象大小和 sizeof 运算符
返回目录
上一课
4.1
基本数据类型简介