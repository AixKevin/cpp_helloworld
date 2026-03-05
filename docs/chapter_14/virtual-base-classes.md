# 25.8 — 虚基类

25.8 — 虚基类
Alex
2008 年 1 月 28 日，太平洋标准时间上午 8:39
2023 年 9 月 11 日
上一章，在课程
24.9 -- 多重继承
中，我们谈到了“菱形问题”。在本节中，我们将继续讨论。
注意：本节是一个高级主题，如果需要可以跳过或略读。
菱形问题
这是我们上一课中说明菱形问题的示例（带一些构造函数）
#include <iostream>

class PoweredDevice
{
public:
    PoweredDevice(int power)
    {
		std::cout << "PoweredDevice: " << power << '\n';
    }
};

class Scanner: public PoweredDevice
{
public:
    Scanner(int scanner, int power)
        : PoweredDevice{ power }
    {
		std::cout << "Scanner: " << scanner << '\n';
    }
};

class Printer: public PoweredDevice
{
public:
    Printer(int printer, int power)
        : PoweredDevice{ power }
    {
		std::cout << "Printer: " << printer << '\n';
    }
};

class Copier: public Scanner, public Printer
{
public:
    Copier(int scanner, int printer, int power)
        : Scanner{ scanner, power }, Printer{ printer, power }
    {
    }
};
尽管您可能期望得到一个看起来像这样的继承图
如果您要创建一个 Copier 类对象，默认情况下您最终会得到两个 PoweredDevice 类的副本——一个来自 Printer，一个来自 Scanner。其结构如下
我们可以创建一个简短的示例来展示它的作用
int main()
{
    Copier copier{ 1, 2, 3 };

    return 0;
}
这会产生结果
PoweredDevice: 3
Scanner: 1
PoweredDevice: 3
Printer: 2
如您所见，PoweredDevice 被构造了两次。
虽然这通常是期望的，但有时您可能希望 PoweredDevice 的一个副本由 Scanner 和 Printer 共享。
虚基类
要共享基类，只需在派生类的继承列表中插入“virtual”关键字。这创建了一个称为
虚基类
的东西，这意味着只有一个基对象。基对象在继承树中的所有对象之间共享，并且它只构造一次。这是一个示例（为简单起见不带构造函数），展示了如何使用 virtual 关键字来创建共享基类
class PoweredDevice
{
};

class Scanner: virtual public PoweredDevice
{
};

class Printer: virtual public PoweredDevice
{
};

class Copier: public Scanner, public Printer
{
};
现在，当您创建一个 Copier 类对象时，每个 Copier 只会得到一个 PoweredDevice 副本，该副本将由 Scanner 和 Printer 共享。
然而，这导致了另一个问题：如果 Scanner 和 Printer 共享一个 PoweredDevice 基类，谁负责创建它？事实证明，答案是 Copier。Copier 构造函数负责创建 PoweredDevice。因此，这是 Copier 允许直接调用非直接父构造函数的一次
#include <iostream>

class PoweredDevice
{
public:
    PoweredDevice(int power)
    {
		std::cout << "PoweredDevice: " << power << '\n';
    }
};

class Scanner: virtual public PoweredDevice // note: PoweredDevice is now a virtual base class
{
public:
    Scanner(int scanner, int power)
        : PoweredDevice{ power } // this line is required to create Scanner objects, but ignored in this case
    {
		std::cout << "Scanner: " << scanner << '\n';
    }
};

class Printer: virtual public PoweredDevice // note: PoweredDevice is now a virtual base class
{
public:
    Printer(int printer, int power)
        : PoweredDevice{ power } // this line is required to create Printer objects, but ignored in this case
    {
		std::cout << "Printer: " << printer << '\n';
    }
};

class Copier: public Scanner, public Printer
{
public:
    Copier(int scanner, int printer, int power)
        : PoweredDevice{ power }, // PoweredDevice is constructed here
        Scanner{ scanner, power }, Printer{ printer, power }
    {
    }
};
这一次，我们之前的例子
int main()
{
    Copier copier{ 1, 2, 3 };

    return 0;
}
产生结果
PoweredDevice: 3
Scanner: 1
Printer: 2
如您所见，PoweredDevice 只被构造了一次。
我们有一些细节，如果不提及就太失职了。
首先，对于最派生类的构造函数，虚基类总是先于非虚基类创建，这确保了所有基类都在其派生类之前创建。
其次，请注意 Scanner 和 Printer 构造函数仍然调用 PoweredDevice 构造函数。创建 Copier 实例时，这些构造函数调用被简单地忽略，因为 Copier 负责创建 PoweredDevice，而不是 Scanner 或 Printer。但是，如果我们要创建 Scanner 或 Printer 的实例，这些构造函数调用将被使用，并且应用正常的继承规则。
第三，如果一个类继承了一个或多个具有虚父类的类，则
最
派生类负责构造虚基类。在这种情况下，Copier 继承了 Printer 和 Scanner，它们都具有 PoweredDevice 虚基类。Copier，作为最派生类，负责 PoweredDevice 的创建。请注意，即使在单继承情况下也是如此：如果 Copier 单独继承自 Printer，并且 Printer 是从 PoweredDevice 虚继承的，Copier 仍然负责创建 PoweredDevice。
第四，所有继承虚基类的类都将拥有一个虚表，即使它们通常不会有，因此类的实例将比指针大。
因为 Scanner 和 Printer 虚拟地派生自 PoweredDevice，Copier 将只有一个 PoweredDevice 子对象。Scanner 和 Printer 都需要知道如何找到那个单一的 PoweredDevice 子对象，这样它们就可以访问它的成员（因为毕竟它们是从它派生出来的）。这通常通过一些虚表魔术来完成（它本质上存储了从每个子类到 PoweredDevice 子对象的偏移量）。
下一课
25.9
对象切片
返回目录
上一课
25.7
纯虚函数、抽象基类和接口类