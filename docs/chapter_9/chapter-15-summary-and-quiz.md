# 15.x — 第 15 章总结和测验

15.x — 第 15 章总结和测验
Alex
2023 年 9 月 11 日下午 1:08（太平洋夏令时）
2024 年 5 月 3 日
章节回顾
在每个（非静态）成员函数内部，关键字
this
是一个 const 指针，它保存当前隐式对象的地址。我们可以让函数通过引用返回
*this
，以启用
方法链
，其中可以在一个表达式中对同一个对象调用多个成员函数。
最好将类定义放在与类同名的头文件中。简单成员函数（例如访问函数、空函数体的构造函数等）可以在类定义内部定义。
最好将非简单成员函数定义在与类同名的源文件中。
在类类型内部定义的类型称为
嵌套类型
（或
成员类型
）。类型别名也可以嵌套。
在类模板定义内部定义的成员函数可以使用类模板本身的模板参数。在类模板定义外部定义的成员函数必须重新提供模板参数声明，并且应该在（同一文件中）类模板定义下方定义。
静态成员变量
是静态持续时间成员，由类的所有对象共享。即使没有实例化类的对象，静态成员也存在。最好使用类名、作用域解析运算符和成员名称来访问它们。
使静态成员
inline
允许它们在类定义内部初始化。
静态成员函数
是可以不带对象调用的成员函数。它们没有
*this
指针，也无法访问非静态数据成员。
在类的主体内部，可以使用
友元声明
（使用
friend
关键字）来告诉编译器某些其他类或函数现在是友元。
友元
是一个类或函数（成员或非成员），被授予对另一个类的私有和保护成员的完全访问权限。
友元函数
是一个函数（成员或非成员），可以像类的成员一样访问类的私有和保护成员。
友元类
是一个可以访问另一个类的私有和保护成员的类。
小测验时间
问题 #1
让我们创建一个随机怪物生成器。这应该很有趣。
a) 首先，让我们创建一个名为
MonsterType
的怪物类型作用域枚举。包括以下怪物类型：龙、哥布林、食人魔、兽人、骷髅、巨魔、吸血鬼和僵尸。添加一个额外的 maxMonsterTypes 枚举器，这样我们就可以计算有多少个枚举器。
显示答案
enum class MonsterType
{
	dragon,
	goblin,
	ogre,
	orc,
	skeleton,
	troll,
	vampire,
	zombie,
	maxMonsterTypes,
};
b) 现在，让我们创建我们的
Monster
类。我们的
Monster
将有 4 个属性（成员变量）：一个类型 (
MonsterType
)、一个名称 (
std::string
)、一个吼叫 (
std::string
) 和生命值 (
int
)。
显示答案
#include <string>

enum class MonsterType
{
	dragon,
	goblin,
	ogre,
	orc,
	skeleton,
	troll,
	vampire,
	zombie,
	maxMonsterTypes,
};

class Monster
{
private:
	MonsterType m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};
};
c)
enum class MonsterType
是
Monster
特有的，所以将
MonsterType
设为
Monster
内部的嵌套无作用域枚举，并将其重命名为
Type
。
显示答案
#include <string>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:

	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};
};
d) 创建一个构造函数，允许您初始化所有成员变量。
以下程序应编译通过
int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };

	return 0;
}
显示答案
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:

	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{
	}
};

int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };

	return 0;
}
e) 现在我们希望能够打印我们的怪物，以便验证它是否正确。编写两个函数：一个名为
getTypeString()
，返回怪物类型作为字符串；另一个名为
print()
，与下面示例程序的输出匹配。
以下程序应编译通过
int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };
	skeleton.print();

	Monster vampire{ Monster::vampire, "Nibblez", "*hiss*", 0 };
	vampire.print();

	return 0;
}
并打印
Bones the skeleton has 4 hit points and says *rattle*.
Nibblez the vampire is dead.
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:

	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{

	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case dragon:   return "dragon";
		case goblin:   return "goblin";
		case ogre:     return "ogre";
		case orc:      return "orc";
		case skeleton: return "skeleton";
		case troll:    return "troll";
		case vampire:  return "vampire";
		case zombie:   return "zombie";
		default:       return "???";
		}
	}

	void print() const
	{
		std::cout << m_name << " the " << getTypeString();

		if (m_hitPoints <= 0)
			std::cout << " is dead.\n";
		else
			std::cout << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };
	skeleton.print();

	Monster vampire{ Monster::vampire, "Nibblez", "*hiss*", 0 };
	vampire.print();

	return 0;
}
f) 现在我们可以创建一个随机怪物生成器。让我们考虑一下我们的
MonsterGenerator
将如何工作。理想情况下，我们会要求它给我们一个
Monster
，它会为我们创建一个随机怪物。因为
MonsterGenerator
没有状态，所以这是一个适合命名空间的候选对象。
创建
MonsterGenerator
命名空间。在其中创建名为
generate()
的函数。它应该返回一个
Monster
。目前，让它返回
Monster{ Monster::skeleton, "Bones", "*rattle*", 4}
；
以下程序应编译通过
int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();

	return 0;
}
并打印
Bones the skeleton has 4 hit points and says *rattle*
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:

	Type m_type{};
	std::string m_name{};
	std::string m_roar{};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, const std::string& roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{

	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case Type::dragon: return "dragon";
		case Type::goblin: return "goblin";
		case Type::ogre: return "ogre";
		case Type::orc: return "orc";
		case Type::skeleton: return "skeleton";
		case Type::troll: return "troll";
		case Type::vampire: return "vampire";
		case Type::zombie: return "zombie";
		default: return "???";
		}
	}

	void print() const
	{
		if (m_hitPoints <= 0)
			std::cout << m_name << " is dead.\n";
		else
			std::cout << m_name << " the " << getTypeString() << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

namespace MonsterGenerator
{
	Monster generate()
	{
		return Monster{ Monster::skeleton, "Bones", "*rattle*", 4 };
	}
};

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();

	return 0;
}
g) 在
MonsterGenerator
命名空间中再添加两个函数。
getName(int)
将接受一个介于 0 到 5 之间（包含）的数字，并返回您选择的名称。
getRoar(int)
也将接受一个介于 0 到 5 之间（包含）的数字，并返回您选择的吼叫。此外，更新您的
generate()
函数以调用
getName(0)
和
getRoar(0)
。
以下程序应编译通过
int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();

	return 0;
}
并打印
Blarg the skeleton has 4 hit points and says *ROAR*
您的名称和声音将根据您的选择而变化。
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:

	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{

	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case dragon:   return "dragon";
		case goblin:   return "goblin";
		case ogre:     return "ogre";
		case orc:      return "orc";
		case skeleton: return "skeleton";
		case troll:    return "troll";
		case vampire:  return "vampire";
		case zombie:   return "zombie";
		default: return "???";
		}
	}

	void print() const
	{
		std::cout << m_name << " the " << getTypeString();

		if (m_hitPoints <= 0)
			std::cout << " is dead.\n";
		else
			std::cout << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

namespace MonsterGenerator
{
    std::string_view getName(int n)
	{
        switch (n)
        {
            case 0:  return "Blarg";
            case 1:  return "Moog";
            case 2:  return "Pksh";
            case 3:  return "Tyrn";
            case 4:  return "Mort";
            case 5:  return "Hans";
            default: return "???";
        }
    }

    std::string_view getRoar(int n)
	{
        switch (n)
        {
            case 0:  return "*ROAR*";
            case 1:  return "*peep*";
            case 2:  return "*squeal*";
            case 3:  return "*whine*";
            case 4:  return "*growl*";
            case 5:  return "*burp*";
            default: return "???";
        }
    }

	Monster generate()
	{
		return Monster{ Monster::skeleton, getName(0), getRoar(0), 4 };
	}

};

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();

	return 0;
}
h) 现在我们将使生成的怪物随机化。从
8.15 -- 全局随机数 (Random.h)
获取“Random.h”代码并将其另存为 Random.h。然后使用
Random::get()
生成一个随机怪物类型、随机名称、随机吼叫和随机生命值（介于 1 到 100 之间）。
以下程序应编译通过
#include "Random.h"

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();

	return 0;
}
并打印类似以下内容：
Mort the zombie has 61 hit points and says *growl*
显示答案
#include "Random.h"
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:

	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{

	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case dragon:   return "dragon";
		case goblin:   return "goblin";
		case ogre:     return "ogre";
		case orc:      return "orc";
		case skeleton: return "skeleton";
		case troll:    return "troll";
		case vampire:  return "vampire";
		case zombie:   return "zombie";
		default: return "???";
		}
	}

	void print() const
	{
		std::cout << m_name << " the " << getTypeString();

		if (m_hitPoints <= 0)
			std::cout << " is dead.\n";
		else
			std::cout << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

namespace MonsterGenerator
{
    std::string_view getName(int n)
	{
        switch (n)
        {
            case 0:  return "Blarg";
            case 1:  return "Moog";
            case 2:  return "Pksh";
            case 3:  return "Tyrn";
            case 4:  return "Mort";
            case 5:  return "Hans";
            default: return "???";
        }
    }

    std::string_view getRoar(int n)
	{
        switch (n)
        {
            case 0:  return "*ROAR*";
            case 1:  return "*peep*";
            case 2:  return "*squeal*";
            case 3:  return "*whine*";
            case 4:  return "*growl*";
            case 5:  return "*burp*";
            default: return "???";
        }
    }

    Monster generate()
    {
        return Monster{
            static_cast<Monster::Type>(Random::get(0, Monster::maxMonsterTypes-1)),
            getName(Random::get(0,5)),
            getRoar(Random::get(0,5)),
            Random::get(1, 100)
            };
	}

};

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();

	return 0;
}
下一课
16.1
容器和数组简介
返回目录
上一课
15.10
引用限定符