# 2.x — 第2章总结和测验

2.x — 第2章总结和测验
Alex
2019 年 2 月 1 日，太平洋标准时间上午 10:56
2024 年 4 月 26 日
章节回顾
函数
是一系列可重用的语句，旨在完成特定工作。你自己编写的函数称为
用户定义
函数。
函数调用
是告诉 CPU 执行函数的表达式。发起函数调用的函数是
调用者
，被调用的函数是
被调用者
或
被调用
函数。执行函数调用时不要忘记包含括号。
函数定义中的花括号和语句称为
函数体
。
返回值的函数称为
返回值函数
。函数的
返回类型
表示函数将返回的值的类型。
return 语句
确定返回给调用者的特定
返回值
。返回值从函数复制回调用者——此过程称为
按值返回
。如果非 void 函数未能返回值，将导致未定义行为。
函数
main
的返回值称为
状态码
，它告诉操作系统（以及调用你的程序的任何其他程序）你的程序是否成功执行。根据约定，返回值为 0 表示成功，非零返回值表示失败。
实践
DRY
编程——“不要重复自己”。利用变量和函数来删除冗余代码。
返回类型为
void
的函数不向调用者返回值。不返回值的函数称为
void 函数
或
不返回值函数
。void 函数不能在需要值的地方调用。
函数中不是最后一条语句的 return 语句称为
提前返回
。这样的语句会使函数立即返回给调用者。
函数参数
是函数中使用的变量，其值由函数的调用者提供。
实参
是从调用者传递给函数的特定值。当实参被复制到参数中时，这称为
按值传递
。
函数参数和函数体内部定义的变量称为
局部变量
。变量存在的时间称为其
生命周期
。变量在
运行时
创建和销毁，即程序运行时。变量的
作用域
决定了它在哪里可以被看到和使用。当变量可以被看到和使用时，我们称其为
在作用域内
。当它不能被看到时，它就不能被使用，我们称其为
超出作用域
。作用域是
编译时
属性，这意味着它在编译时强制执行。
空白字符
是指用于格式化目的的字符。在 C++ 中，这包括空格、制表符和换行符。
前向声明
允许我们在实际定义标识符之前告诉编译器标识符的存在。要为函数编写前向声明，我们使用
函数原型
，它包括函数的返回类型、名称和参数，但没有函数体，后跟一个分号。
定义
实际上实现了（对于函数和类型）或实例化了（对于变量）一个标识符。
声明
是告诉编译器标识符存在的语句。在 C++ 中，所有定义都充当声明。
纯声明
是那些不是定义的声明（例如函数原型）。
大多数非平凡程序包含多个文件。
当以编译器或链接器无法区分的方式将两个标识符引入同一程序时，编译器或链接器将由于
命名冲突
而报错。
命名空间
保证命名空间内的所有标识符都是唯一的。std 命名空间就是这样一个命名空间。
预处理器
是在代码编译之前运行的一个过程。
指令
是给预处理器的特殊指令。指令以 # 符号开头并以换行符结尾。
宏
是定义如何将输入文本转换为替换输出文本的规则。
头文件
是旨在将声明传播到代码文件的文件。使用
#include
指令时，
#include
指令被包含文件的内容替换。包含头文件时，包含系统头文件（例如 C++ 标准库中的头文件）时使用尖括号，包含用户定义头文件（你编写的头文件）时使用双引号。包含系统头文件时，如果存在，请包含不带 .h 扩展名的版本。
头文件卫士
防止头文件的内容被多次包含到给定的代码文件中。它们不能防止头文件的内容被包含到多个不同的代码文件中。
小测验时间
请务必使用编辑器的自动格式化功能，以保持格式一致性并使代码更易于阅读。
问题 #1
编写一个单文件程序（名为 main.cpp），它从用户那里读取两个单独的整数，将它们相加，然后输出答案。该程序应使用三个函数
应使用名为“readNumber”的函数从用户那里获取（并返回）一个整数。
应使用名为“writeAnswer”的函数输出答案。此函数应接受一个参数，并且没有返回值。
应使用 main() 函数将上述函数连接在一起。
显示提示
提示：你不需要编写单独的函数来执行加法（直接使用 operator+ 即可）。
显示提示
提示：你需要调用 readNumber() 两次。
显示答案
main.cpp
#include <iostream>

int readNumber()
{
    std::cout << "Enter a number to add: ";
    int x {};
    std::cin >> x;
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The answer is " << x << '\n';
}

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x + y); // using operator+ to pass the sum of x and y to writeAnswer()
    return 0;
}
问题 #2
修改你在练习 #1 中编写的程序，以便 readNumber() 和 writeAnswer() 位于名为“io.cpp”的单独文件中。使用前向声明从 main() 访问它们。
如果你遇到问题，请确保“io.cpp”已正确添加到你的项目中，以便它被编译。
显示答案
io.cpp
#include <iostream>

int readNumber()
{
    std::cout << "Enter a number to add: ";
    int x {};
    std::cin >> x;
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The answer is " << x << '\n';
}
main.cpp
// We don't need to #include <iostream> since main.cpp doesn't use any input/output functionality

// These are the forward declarations for the functions in io.cpp
int readNumber();
void writeAnswer(int x);

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x+y);
    return 0;
}
问题 #3
修改你在 #2 中编写的程序，使其使用头文件（名为 io.h）访问函数，而不是直接在你的代码 (.cpp) 文件中使用前向声明。确保你的头文件使用头文件卫士。
显示答案
io.h
#ifndef IO_H
#define IO_H

int readNumber();
void writeAnswer(int x);

#endif
io.cpp
#include "io.h"
#include <iostream>

int readNumber()
{
    std::cout << "Enter a number to add: ";
    int x {};
    std::cin >> x;
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The answer is " << x << '\n';
}
main.cpp
#include "io.h"

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x+y);
    return 0;
}
虽然技术上
io.cpp
不需要包含
io.h
，但代码文件包含其配对头文件是最佳实践。这在课程
2.11 -- 头文件
中有所介绍。
如果你编译程序并出现以下错误之一
unresolved external symbol "int __cdecl readNumber(void)" (?readNumber@@YAHXZ)
undefined reference to `readNumber()'
那么你可能忘记将
io.cpp
包含在你的项目中，因此
readNumber()
（和
writeAnswer()
）的定义没有被编译到你的项目中。
下一课
3.1
语法和语义错误
返回目录
上一课
2.13
如何设计你的第一个程序