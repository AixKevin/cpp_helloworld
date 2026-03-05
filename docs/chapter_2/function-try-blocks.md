# 27.7 — 函数 try 块

27.7 — 函数 try 块
Alex
2017 年 2 月 6 日，下午 2:22 PST
2024 年 12 月 19 日
在大多数情况下，try 和 catch 块运行良好，但在一种特殊情况下，它们不足以应对。考虑以下示例：
#include <iostream>

class A
{
private:
	int m_x;
public:
	A(int x) : m_x{x}
	{
		if (x <= 0)
			throw 1; // Exception thrown here
	}
};

class B : public A
{
public:
	B(int x) : A{x} // A initialized in member initializer list of B
	{
		// What happens if creation of A fails and we want to handle it here?
	}
};

int main()
{
	try
	{
		B b{0};
	}
	catch (int)
	{
		std::cout << "Oops\n";
	}
}
在上面的例子中，派生类 B 调用基类构造函数 A，A 可能会抛出异常。由于对象 b 的创建被放在一个 try 块内（在函数 main() 中），如果 A 抛出异常，main 的 try 块将捕获它。因此，这个程序打印：
Oops
但是，如果我们想在 B 内部捕获异常呢？对基类构造函数 A 的调用是通过成员初始化列表发生的，在 B 构造函数的函数体被调用之前。没有办法用标准 try 块将其包装起来。
在这种情况下，我们必须使用一个稍微修改过的 try 块，称为
函数 try 块
。
函数 try 块
函数 try 块旨在允许您在整个函数的函数体周围建立一个异常处理程序，而不是围绕一个代码块。
函数 try 块的语法有点难以描述，所以我们通过示例来演示：
#include <iostream>

class A
{
private:
	int m_x;
public:
	A(int x) : m_x{x}
	{
		if (x <= 0)
			throw 1; // Exception thrown here
	}
};

class B : public A
{
public:
	B(int x) try : A{x} // note addition of try keyword here
	{
	}
	catch (...) // note this is at same level of indentation as the function itself
	{
                // Exceptions from member initializer list or
                // from constructor body are caught here

                std::cerr << "Exception caught\n";

                throw; // rethrow the existing exception
	}
};

int main()
{
	try
	{
		B b{0};
	}
	catch (int)
	{
		std::cout << "Oops\n";
	}
}
当这个程序运行时，它会产生以下输出：
Exception caught
Oops
让我们更详细地检查这个程序。
首先，注意在成员初始化列表之前添加了
try
关键字。这表明从该点之后（直到函数结束）的所有内容都应被视为在 try 块内部。
其次，请注意关联的 catch 块与整个函数具有相同的缩进级别。在 try 关键字和函数体结束之间抛出的任何异常都可以在这里被捕获。
当上述程序运行时，变量
b
开始构造，这会调用 B 的构造函数（它使用了函数 try）。B 的构造函数调用 A 的构造函数，然后 A 的构造函数抛出异常。由于 A 的构造函数不处理此异常，异常会沿堆栈传播到 B 的构造函数，在那里它被 B 构造函数的函数级 catch 捕获。catch 块打印“Exception caught”，然后将当前异常重新抛出到堆栈中，该异常被
main()
中的 catch 块捕获，后者打印“Oops”。
最佳实践
当您需要构造函数处理成员初始化列表中抛出的异常时，请使用函数 try 块。
函数 catch 块的限制
对于常规 catch 块（在函数内部），我们有三种选择：我们可以抛出一个新异常，重新抛出当前异常，或者解决异常（通过 return 语句，或者让控制流到达 catch 块的末尾）。
构造函数的函数级 catch 块必须抛出新异常或重新抛出现有异常——它们不允许解决异常！也不允许使用 return 语句，并且到达 catch 块的末尾将隐式地重新抛出。
析构函数的函数级 catch 块可以通过 return 语句抛出、重新抛出或解决当前异常。到达 catch 块的末尾将隐式地重新抛出。
其他函数的函数级 catch 块可以通过 return 语句抛出、重新抛出或解决当前异常。到达 catch 块的末尾将隐式地解决非值（void）返回函数的异常，并为值返回函数产生未定义行为！
下表总结了函数级 catch 块的限制和行为
函数类型
可以解决异常
通过 return 语句
catch 块结束时的行为
构造函数
否，必须抛出或重新抛出
隐式重新抛出
析构函数
是
隐式重新抛出
非值返回函数
是
解决异常
值返回函数
是
未定义行为
由于 catch 块结束时的这种行为根据函数类型（包括值返回函数的未定义行为）而变化很大，我们建议永远不要让控制流到达 catch 块的末尾，而总是显式地抛出、重新抛出或返回。
最佳实践
避免让控制流到达函数级 catch 块的末尾。相反，显式地抛出、重新抛出或返回。
在上面的程序中，如果我们没有在构造函数的函数级 catch 块中显式地重新抛出异常，控制流就会到达函数级 catch 的末尾，并且因为这是一个构造函数，所以会发生隐式重新抛出。结果将是相同的。
尽管函数级 try 块也可以与非成员函数一起使用，但它们通常不常用，因为很少有需要这种情况的情况。它们几乎只与构造函数一起使用！
函数 try 块可以捕获基类和当前类的异常
在上面的例子中，如果 A 或 B 的构造函数抛出异常，它将被 B 的构造函数周围的 try 块捕获。
我们可以在下面的例子中看到这一点，我们在类 B 而不是类 A 中抛出异常：
#include <iostream>

class A
{
private:
	int m_x;
public:
	A(int x) : m_x{x}
	{
	}
};

class B : public A
{
public:
	B(int x) try : A{x} // note addition of try keyword here
	{
		if (x <= 0) // moved this from A to B
			throw 1; // and this too
	}
	catch (...)
	{
                std::cerr << "Exception caught\n";

                // If an exception isn't explicitly thrown here,
                // the current exception will be implicitly rethrown
	}
};

int main()
{
	try
	{
		B b{0};
	}
	catch (int)
	{
		std::cout << "Oops\n";
	}
}
我们得到相同的输出：
Exception caught
Oops
不要使用函数 try 来清理资源
当对象的构造失败时，不会调用类的析构函数。因此，您可能会试图使用函数 try 块作为一种方法来清理一个在失败之前部分分配了资源的类。然而，引用失败对象的成员被认为是未定义行为，因为对象在 catch 块执行之前就已经“死亡”。这意味着您不能使用函数 try 来清理类。如果您想清理类，请遵循清理抛出异常的类的标准规则（参见课程
27.5 -- 异常、类和继承
中的“当构造函数失败时”小节）。
函数 try 主要用于在将异常传递到堆栈之前记录失败，或者用于更改抛出的异常类型。
下一课
27.8
异常的危险和缺点
返回目录
上一课
27.6
重新抛出异常