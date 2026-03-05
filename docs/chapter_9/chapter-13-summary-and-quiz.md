# 13.x — 第 13 章总结和测验

13.x — 第 13 章总结和测验
Alex
2020 年 1 月 3 日，太平洋标准时间下午 1:20
2024 年 11 月 4 日
恭喜！你又完成了一章。你所获得的关于结构体的知识将在我们学习 C++ 最重要的主题——类时非常有用！
快速回顾
程序定义类型
（也称为
用户定义类型
）是一种我们可以创建的自定义类型，用于我们自己的程序中。枚举类型和类类型（包括结构体、类和联合体）允许创建程序定义类型。程序定义类型必须在使用前定义。程序定义类型的定义称为
类型定义
。类型定义不受“单一定义规则”的约束。
枚举
（也称为
枚举类型
或
enum
）是一种复合数据类型，其中每个可能的值都定义为符号常量（称为
枚举器
）。枚举是
不同的类型
，这意味着编译器可以区分它们与其他类型（与类型别名不同）。
无作用域枚举
之所以这样命名，是因为它们将其枚举器名称放入与枚举定义本身相同的范围（而不是像命名空间那样创建新的作用域区域）。无作用域枚举也为其枚举器提供了一个命名作用域区域。无作用域枚举将隐式转换为整数值。
有作用域枚举
的工作方式与无作用域枚举类似，但不会隐式转换为整数，并且枚举器
仅
放置在枚举的作用域区域中（而不是放置在定义枚举的作用域区域中）。
结构体
（
structure
的简称）是一种程序定义数据类型，它允许我们将多个变量捆绑到一个单一类型中。结构体（或类）的一部分的变量称为
数据成员
（或
成员变量
）。要访问特定的成员变量，我们使用
成员选择运算符
（
operator.
）在结构体变量名和成员名之间（对于普通结构体和结构体引用），或者使用
来自指针的成员选择运算符
（
operator->
）（对于结构体指针）。
在通用编程中，
聚合数据类型
（也称为
聚合
）是任何可以包含多个数据成员的类型。在 C++ 中，仅包含数据成员的数组和结构体是
聚合
。
聚合使用一种称为
聚合初始化
的初始化形式，它允许我们直接初始化聚合的成员。为此，我们提供一个
初始化列表
作为初始化器，它只是一个逗号分隔值的列表。聚合初始化执行
成员初始化
，这意味着结构体中的每个成员都按照声明的顺序进行初始化。
在 C++20 中，
指定初始化器
允许你明确定义哪些初始化值映射到哪些成员。成员必须按照它们在结构体中声明的顺序进行初始化，否则会出错。
当我们定义一个结构体（或类）类型时，我们可以为每个成员提供一个默认初始化值作为类型定义的一部分。这个过程称为
非静态成员初始化
，初始化值称为
默认成员初始化器
。
出于性能原因，编译器有时会在结构体中添加间隙（这称为
填充
），因此结构体的大小可能大于其成员大小的总和。
类模板
是用于实例化类类型（结构体、类或联合体）的模板定义。
类模板参数推导 (CTAD)
是 C++17 的一个特性，它允许编译器从初始化器中推导出模板类型参数。
小测验时间
耶！
问题 #1
在设计游戏时，我们决定要有怪物，因为每个人都喜欢打怪。声明一个表示你的怪物的结构体。怪物应该有一个类型，可以是以下之一：食人魔、龙、兽人、巨型蜘蛛或史莱姆。
每个独立的怪物还应该有一个名字（使用
std::string
），以及一个生命值，表示它们在死亡前可以承受多少伤害。编写一个名为
printMonster()
的函数，它打印出结构体的所有成员。实例化一个食人魔和一个史莱姆，使用初始化列表初始化它们，并将它们传递给
printMonster()
。
你的程序应该产生以下输出：
This Ogre is named Torg and has 145 health.
This Slime is named Blurp and has 23 health.
显示答案
#include <iostream>
#include <string>
#include <string_view> // C++17

// Our monster struct represents a single monster

struct Monster
{
	// Define our different monster types as an enum
	enum Type
	{
		ogre,
		dragon,
		orc,
		giant_spider,
		slime,
	};

	Type type{};
	std::string name{}; // the Monster should be an owner of its name
	int health{};
};

// Return the name of the monster's type as a string
// Since this could be used elsewhere, it's better to make this its own function
constexpr std::string_view getMonsterTypeString(Monster::Type type)
{
	switch (type)
	{
	case Monster::ogre:          return "Ogre";
	case Monster::dragon:        return "Dragon";
	case Monster::orc:           return "Orc";
	case Monster::giant_spider:  return "Giant Spider";
	case Monster::slime:         return "Slime";
	}

	return "Unknown";
}

// Print our monster's stats
void printMonster(const Monster& monster)
{
	std::cout << "This " << getMonsterTypeString(monster.type) <<
		" is named " << monster.name <<
		" and has " << monster.health << " health.\n";
}

int main()
{
	Monster ogre{ Monster::ogre, "Torg", 145 };
	Monster slime{ Monster::slime, "Blurp", 23 };

	printMonster(ogre);
	printMonster(slime);

	return 0;
}
问题 #2
指定以下给定类型的对象应该通过值、常量地址还是常量引用传递。你可以假设将这些类型作为参数的函数不会修改它们。
a)
char
显示答案
char
是基本类型，所以应该按值传递。
b)
std::string
显示答案
std::string
在复制时必须创建字符串的副本。按常量引用传递。
c)
unsigned long
显示答案
unsigned long
是基本类型，所以应该按值传递。
d)
bool
显示答案
bool
是基本类型，所以应该按值传递。
e) 枚举类型
显示答案
枚举类型持有整数值（通常是 int）。由于整数值按值传递，枚举类型也应该按值传递。
f)
struct Position
{
  double x{};
  double y{};
  double z{};
};
显示答案
Position
是一个结构体类型，应该按常量引用传递。
g)
struct Player
{
  int health{};
  // The Player struct is still under development.  More members will be added.
};
显示答案
尽管
Player
当前只包含一个
int
，这使得按值传递很快，但将来会添加更多成员。我们不希望在发生这种情况时更新每次使用
Player
的地方，所以我们按常量引用传递它。
h)
int
(当 null 是有效参数时)
显示答案
通常我们会按值传递
int
，但如果我们也希望能够传递一个 null 值，那么按地址传递是一个不错的选择，因为我们可以传递
int
的地址或
nullptr
。
i)
std::string_view
显示答案
std::string_view
不会创建被查看字符串的副本，并且复制成本很低。按值传递。
问题 #3
创建一个名为
Triad
的类模板，它有 3 个相同模板类型的成员。再创建一个名为
print
的函数模板，可以打印一个 Triad。以下程序应该可以编译：
int main()
{
	Triad t1{ 1, 2, 3 }; // note: uses CTAD to deduce template arguments
	print(t1);

	Triad t2{ 1.2, 3.4, 5.6 }; // note: uses CTAD to deduce template arguments
	print(t2);

	return 0;
}
并产生以下结果：
[1, 2, 3][1.2, 3.4, 5.6]
如果你使用 C++17，你需要提供一个推导指南才能使 CTAD 工作（有关信息，请参阅
13.14 -- 类模板参数推导 (CTAD) 和推导指南
）。
显示答案
#include <iostream>

template <typename T>
struct Triad
{
	T first {};
	T second {};
	T third {};
};

// If using C++17, we need to provide a deduction guide (not required in C++20)
// A Triad with three arguments of the same type should deduce to a Triad<T>
template <typename T>
Triad(T, T, T) -> Triad<T>;

template <typename T>
void print(const Triad<T>& t)
{
	std::cout << '[' << t.first << ", " << t.second << ", " << t.third << ']';
}

int main()
{
	Triad t1{ 1, 2, 3 };
	print(t1);

	Triad t2{ 1.2, 3.4, 5.6 };
	print(t2);

	return 0;
}
下一课
13.y
使用语言参考
返回目录
上一课
13.15
别名模板