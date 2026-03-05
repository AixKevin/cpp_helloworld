# 15.4 — 析构函数介绍

15.4 — 析构函数介绍
Alex
2023 年 9 月 11 日，太平洋夏令时上午 11:55
2024 年 9 月 23 日
清理问题
假设您正在编写一个程序，需要通过网络发送一些数据。但是，建立与服务器的连接成本很高，因此您希望收集大量数据，然后一次性发送。这样的类可能如下所示：
// This example won't compile because it is (intentionally) incomplete
class NetworkData
{
private:
    std::string m_serverName{};
    DataStore m_dataQueue{};

public:
	NetworkData(std::string_view serverName)
		: m_serverName { serverName }
	{
	}

	void addData(std::string_view data)
	{
		m_dataQueue.add(data);
	}

	void sendData()
	{
		// connect to server
		// send all data
		// clear data
	}
};

int main()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    n.sendData();

    return 0;
}
然而，这个
NetworkData
存在一个潜在问题。它依赖于在程序关闭之前显式调用
sendData()
。如果
NetworkData
的用户忘记这样做，数据将不会发送到服务器，并在程序退出时丢失。现在，您可能会说，“嗯，这不难记住！”，在这种特殊情况下，您是对的。但考虑一个稍微复杂一点的例子，比如这个函数：
bool someFunction()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    if (someCondition)
        return false;

    n.sendData();
    return true;
}
在这种情况下，如果
someCondition
为
true
，则函数将提前返回，并且
sendData()
将不会被调用。这是一个更容易犯的错误，因为
sendData()
调用存在，但程序并非在所有情况下都执行到它。
概括来说，使用资源的类（最常见的是内存，但有时是文件、数据库、网络连接等）通常需要在销毁使用它们的类对象之前显式发送或关闭。在其他情况下，我们可能希望在对象销毁之前进行一些记录，例如将信息写入日志文件，或向服务器发送一段遥测数据。“清理”一词通常用于指在类对象被销毁之前，为了使其正常运行，类必须执行的任何任务集。如果我们必须依靠此类用户来确保在对象销毁之前调用执行清理的函数，我们很可能会遇到错误。
但是，我们为什么要要求用户确保这一点呢？如果对象正在被销毁，那么我们知道此时需要执行清理。清理是否应该自动发生？
析构函数登场
在第
14.9 课 -- 构造函数介绍
中，我们介绍了构造函数，它们是当非聚合类类型的对象被创建时调用的特殊成员函数。构造函数用于初始化成员变量，并执行确保类对象可以使用的任何其他设置任务。
类似地，类还有另一种特殊成员函数，当非聚合类类型的对象被销毁时会自动调用。此函数称为
析构函数
。析构函数旨在允许类在类对象被销毁之前执行任何必要的清理工作。
析构函数命名
与构造函数一样，析构函数也有特定的命名规则：
析构函数必须与类名相同，前面带有波浪号（~）。
析构函数不能接受参数。
析构函数没有返回类型。
一个类只能有一个析构函数。
通常不应显式调用析构函数（因为它会在对象销毁时自动调用），因为很少有需要多次清理对象的情况。
析构函数可以安全地调用其他成员函数，因为对象直到析构函数执行完毕后才会被销毁。
析构函数示例
#include <iostream>

class Simple
{
private:
    int m_id {};

public:
    Simple(int id)
        : m_id { id }
    {
        std::cout << "Constructing Simple " << m_id << '\n';
    }

    ~Simple() // here's our destructor
    {
        std::cout << "Destructing Simple " << m_id << '\n';
    }

    int getID() const { return m_id; }
};

int main()
{
    // Allocate a Simple
    Simple simple1{ 1 };
    {
        Simple simple2{ 2 };
    } // simple2 dies here

    return 0;
} // simple1 dies here
此程序产生以下结果：
Constructing Simple 1
Constructing Simple 2
Destructing Simple 2
Destructing Simple 1
请注意，当每个
Simple
对象被销毁时，都会调用析构函数，该函数会打印一条消息。“销毁 Simple 1”在“销毁 Simple 2”之后打印，因为
simple2
在函数结束之前被销毁，而
simple1
直到
main()
结束才被销毁。
请记住，静态变量（包括全局变量和静态局部变量）在程序启动时构造，在程序关闭时销毁。
改进 NetworkData 程序
回到本课开头的例子，我们可以通过让析构函数调用
sendData()
来消除用户显式调用
sendData()
的需要：
class NetworkData
{
private:
    std::string m_serverName{};
    DataStore m_dataQueue{};

public:
	NetworkData(std::string_view serverName)
		: m_serverName { serverName }
	{
	}

	~NetworkData()
	{
		sendData(); // make sure all data is sent before object is destroyed
	}

	void addData(std::string_view data)
	{
		m_dataQueue.add(data);
	}

	void sendData()
	{
		// connect to server
		// send all data
		// clear data
	}
};

int main()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    return 0;
}
有了这样的析构函数，我们的
NetworkData
对象在被销毁之前总是会发送它所拥有的任何数据！清理会自动发生，这意味着更少的错误机会，以及更少需要考虑的事情。
隐式析构函数
如果非聚合类类型对象没有用户声明的析构函数，编译器将生成一个空体的析构函数。这个析构函数称为隐式析构函数，它实际上只是一个占位符。
如果您的类在销毁时不需要执行任何清理工作，那么完全不定义析构函数，让编译器为您的类生成一个隐式析构函数是可以的。
关于
std::exit()
函数的警告
在第
8.12 课 -- 暂停（提前退出程序）
中，我们讨论了
std::exit()
函数，它可以用于立即终止程序。当程序立即终止时，程序只是结束。局部变量不会首先被销毁，因此不会调用任何析构函数。如果您在这种情况下依赖析构函数执行必要的清理工作，请务必小心。
致进阶读者
未处理的异常也会导致程序终止，并且可能在终止之前不会展开堆栈。如果堆栈未展开，析构函数将不会在程序终止之前被调用。
下一课
15.5
带成员函数的类模板
返回目录
上一课
15.3
嵌套类型（成员类型）