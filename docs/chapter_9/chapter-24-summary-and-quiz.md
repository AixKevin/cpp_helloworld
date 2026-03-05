# 24.x — 第 24 章总结与测验

24.x — 第 24 章总结与测验
Alex
2016 年 10 月 29 日，下午 3:32 PDT
2024 年 1 月 31 日
总结
继承允许我们模拟两个对象之间的“is-a”关系。被继承的对象称为父类、基类或超类。执行继承的对象称为子类、派生类或子类。
当一个派生类从基类继承时，派生类会获得基类的所有成员。
当一个派生类被构造时，类中的基类部分会首先被构造，然后派生类部分才会被构造。更详细地说：
为派生类预留内存（足够基类和派生类两部分使用）。
调用适当的派生类构造函数。
首先使用适当的基类构造函数构造基类对象。如果未指定基类构造函数，则将使用默认构造函数。
派生类的初始化列表初始化派生类的成员。
执行派生类构造函数的主体。
控制权返回给调用者。
销毁按相反的顺序进行，从最派生类到最基类。
C++ 有 3 种访问修饰符：public、private 和 protected。protected 访问修饰符允许成员所属的类、友元和派生类访问受保护成员，但公共部分不能访问。
类可以公开、私有或受保护地继承自另一个类。类几乎总是公开继承。
以下是所有访问修饰符和继承类型组合的表格
基类中的访问修饰符
公开继承时的访问修饰符
私有继承时的访问修饰符
受保护继承时的访问修饰符
公共
公共
私有的
受保护的
私有的
不可访问
不可访问
不可访问
受保护的
受保护的
私有的
受保护的
派生类可以添加新函数，改变基类中存在的函数在派生类中的工作方式，改变继承成员的访问级别，或隐藏功能。
多重继承允许派生类从多个父类继承成员。除非替代方案导致更高的复杂性，否则通常应避免使用多重继承。
小测验时间
问题 #1
对于以下每个程序，确定它们的输出，或者如果它们无法编译，请说明原因。本练习旨在通过检查来完成，因此请勿编译它们（否则答案将是微不足道的）。
a)
#include <iostream>

class Base
{
public:
	Base()
	{
		std::cout << "Base()\n";
	}
	~Base()
	{
		std::cout << "~Base()\n";
	}
};

class Derived: public Base
{
public:
	Derived()
	{
		std::cout << "Derived()\n";
	}
	~Derived()
	{
		std::cout << "~Derived()\n";
	}
};

int main()
{
	Derived d;

	return 0;
}
显示答案
构造按从最父级到最子级的顺序进行。析构按相反的顺序进行。
Base()
Derived()
~Derived()
~Base()
b)
#include <iostream>

class Base
{
public:
	Base()
	{
		std::cout << "Base()\n";
	}
	~Base()
	{
		std::cout << "~Base()\n";
	}
};

class Derived: public Base
{
public:
	Derived()
	{
		std::cout << "Derived()\n";
	}
	~Derived()
	{
		std::cout << "~Derived()\n";
	}
};

int main()
{
	Derived d;
	Base b;

	return 0;
}
提示：局部变量按定义顺序的相反顺序销毁。
显示答案
首先我们构造d，它会打印
Base()
Derived()
然后我们构造b，它会打印
Base()
然后我们析构b，它会打印
~Base()
然后我们析构d，它会打印
~Derived()
~Base()
c)
#include <iostream>

class Base
{
private:
	int m_x {};
public:
	Base(int x): m_x{ x }
	{
		std::cout << "Base()\n";
	}
	~Base()
	{
		std::cout << "~Base()\n";
	}

	void print() const { std::cout << "Base: " << m_x << '\n';  }
};

class Derived: public Base
{
public:
	Derived(int y):  Base{ y }
	{
		std::cout << "Derived()\n";
	}
	~Derived()
	{
		std::cout << "~Derived()\n";
	}

	void print() const { std::cout << "Derived: " << m_x << '\n'; }
};

int main()
{
	Derived d{ 5 };
	d.print();

	return 0;
}
显示答案
无法编译，Derived::print() 无法访问私有成员 m_x
d)
#include <iostream>

class Base
{
protected:
	int m_x {};
public:
	Base(int x): m_x{ x }
	{
		std::cout << "Base()\n";
	}
	~Base()
	{
		std::cout << "~Base()\n";
	}

	void print() const { std::cout << "Base: " << m_x << '\n';  }
};

class Derived: public Base
{
public:
	Derived(int y):  Base{ y }
	{
		std::cout << "Derived()\n";
	}
	~Derived()
	{
		std::cout << "~Derived()\n";
	}

	void print() const { std::cout << "Derived: " << m_x << '\n'; }
};

int main()
{
	Derived d{ 5 };
	d.print();

	return 0;
}
显示答案
Base()
Derived()
Derived: 5
~Derived()
~Base()
e)
#include <iostream>

class Base
{
protected:
	int m_x {};
public:
	Base(int x): m_x{ x }
	{
		std::cout << "Base()\n";
	}
	~Base()
	{
		std::cout << "~Base()\n";
	}

	void print() const { std::cout << "Base: " << m_x << '\n';  }
};

class Derived: public Base
{
public:
	Derived(int y):  Base{ y }
	{
		std::cout << "Derived()\n";
	}
	~Derived()
	{
		std::cout << "~Derived()\n";
	}

	void print() const { std::cout << "Derived: " << m_x << '\n'; }
};

class D2 : public Derived
{
public:
	D2(int z): Derived{ z }
	{
		std::cout << "D2()\n";
	}
	~D2()
	{
		std::cout << "~D2()\n";
	}

        // note: no print() function here
};

int main()
{
	D2 d{ 5 };
	d.print();

	return 0;
}
显示答案
Base()
Derived()
D2()
Derived: 5
~D2()
~Derived()
~Base()
问题 #2
a) 编写一个 Apple 类和一个 Banana 类，它们都派生自一个共同的 Fruit 类。Fruit 应该有两个成员：名称和颜色。
以下程序应该运行
int main()
{
	Apple a{ "red" };
	Banana b{};

	std::cout << "My " << a.getName() << " is " << a.getColor() << ".\n";
	std::cout << "My " << b.getName() << " is " << b.getColor() << ".\n";
	
	return 0;
}
并产生结果
My apple is red.
My banana is yellow.
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Fruit
{
private:
	std::string m_name;
	std::string m_color;

public:
	Fruit(std::string_view name, std::string_view color)
		: m_name{ name }, m_color{ color }
	{
	}

	const std::string& getName() const { return m_name; }
	const std::string& getColor() const { return m_color; }
};

class Apple: public Fruit
{
public:
	Apple(std::string_view color="red")
		: Fruit{ "apple", color }
	{
	}
};

class Banana : public Fruit
{
public:
	Banana()
		: Fruit{ "banana", "yellow" }
	{
	}
};

int main()
{
	Apple a{ "red" };
	Banana b;

	std::cout << "My " << a.getName() << " is " << a.getColor() << ".\n";
	std::cout << "My " << b.getName() << " is " << b.getColor() << ".\n";
	
	return 0;
}
b) 在上一个程序中添加一个新类，名为 GrannySmith，它继承自 Apple。
以下程序应该运行
int main()
{
	Apple a{ "red" };
	Banana b;
	GrannySmith c;

	std::cout << "My " << a.getName() << " is " << a.getColor() << ".\n";
	std::cout << "My " << b.getName() << " is " << b.getColor() << ".\n";
	std::cout << "My " << c.getName() << " is " << c.getColor() << ".\n";
	
	return 0;
}
并产生结果
My apple is red.
My banana is yellow.
My granny smith apple is green.
显示答案
#include <iostream>
#include <string>
#include <string_view>

class Fruit
{
private:
	std::string m_name;
	std::string m_color;

public:
	Fruit(std::string_view name, std::string_view color)
		: m_name{ name }, m_color{ color }
	{
	}

	const std::string& getName() const { return m_name; }
	const std::string& getColor() const { return m_color; }
};

class Apple: public Fruit
{
// The previous constructor we used for Apple had a fixed name ("apple").
// We need a new constructor for GrannySmith to use to set the name of the fruit
protected: // protected so only derived classes can access
	Apple(std::string_view name, std::string_view color)
		: Fruit{ name, color }
	{
	}

public:
	Apple(std::string_view color="red")
		: Fruit{ "apple", color }
	{
	}
};

class Banana : public Fruit
{
public:
	Banana()
		: Fruit{ "banana", "yellow" }
	{
	}
};

class GrannySmith : public Apple
{
public:
	GrannySmith()
		: Apple{ "granny smith apple", "green" }
	{
	}
};

int main()
{
	Apple a{ "red" };
	Banana b;
	GrannySmith c;

	std::cout << "My " << a.getName() << " is " << a.getColor() << ".\n";
	std::cout << "My " << b.getName() << " is " << b.getColor() << ".\n";
	std::cout << "My " << c.getName() << " is " << c.getColor() << ".\n";

	return 0;
}
问题 #3
挑战时间！下面的测验问题更加困难和冗长。我们将编写一个简单的游戏，你将在其中与怪物战斗。游戏的目标是在你死亡或达到 20 级之前收集尽可能多的金币。
我们的程序将由 3 个类组成：一个 Creature 类，一个 Player 类和一个 Monster 类。Player 和 Monster 都继承自 Creature。
a) 首先创建 Creature 类。生物有 5 个属性：名称（std::string）、符号（char）、生命值（int）、每次攻击造成的伤害（int）以及携带的金币数量（int）。将这些实现为类成员。编写一组完整的 getter（每个成员一个 get 函数）。添加另外三个函数：void reduceHealth(int) 将生物的生命值减少一个整数值。bool isDead() 在生物生命值为 0 或更少时返回 true。void addGold(int) 为生物添加金币。
以下程序应该运行
#include <iostream>
#include <string>

int main()
{
	Creature o{ "orc", 'o', 4, 2, 10 };
	o.addGold(5);
	o.reduceHealth(1);
	std::cout << "The " << o.getName() << " has " << o.getHealth() << " health and is carrying " << o.getGold() << " gold.\n";

	return 0;
}
并产生结果
The orc has 3 health and is carrying 15 gold.
显示答案
#include <iostream>
#include <string>
#include <string_view> // Requires C++17

class Creature
{
protected:
	std::string m_name;
	char m_symbol {};
	int m_health {};
	int m_damage {};
	int m_gold {};

public:
	Creature(std::string_view name, char symbol, int health, int damage, int gold)
		: m_name{ name }
		, m_symbol{ symbol }
		, m_health{ health }
		, m_damage{ damage }
		, m_gold{ gold }
	{
	}

	const std::string& getName() const { return m_name; }
	char getSymbol() const { return m_symbol; }
	int getHealth() const { return m_health; }
	int getDamage() const { return m_damage; }
	int getGold() const { return m_gold; }

	void reduceHealth(int health) { m_health -= health; }
	bool isDead() const { return m_health <= 0; }
	void addGold(int gold) { m_gold += gold; }
};

int main()
{
	Creature o{ "orc", 'o', 4, 2, 10 };
	o.addGold(5);
	o.reduceHealth(1);
	std::cout << "The " << o.getName() << " has " << o.getHealth() << " health and is carrying " << o.getGold() << " gold.\n";

	return 0;
}
b) 现在我们来创建 Player 类。Player 类继承自 Creature。Player 还有一个额外成员，玩家的等级，初始为 1。玩家有一个自定义名称（由用户输入），使用符号“@”，初始生命值为 10，初始伤害为 1，没有金币。编写一个名为 levelUp() 的函数，该函数将玩家的等级和伤害增加 1。还为等级成员编写一个 getter。最后，编写一个名为 hasWon() 的函数，如果玩家达到 20 级，则返回 true。
编写一个新的 main() 函数，询问用户姓名并生成以下输出
Enter your name: Alex
Welcome, Alex.
You have 10 health and are carrying 0 gold.
显示答案
#include <iostream>
#include <string>
#include <string_view> // std::string_view requires C++17

class Creature
{
protected:
	std::string m_name;
	char m_symbol {};
	int m_health {};
	int m_damage {};
	int m_gold {};

public:
	Creature(std::string_view name, char symbol, int health, int damage, int gold)
		: m_name{ name }
		, m_symbol{ symbol }
		, m_health{ health }
		, m_damage{ damage }
		, m_gold{ gold }
	{
	}

	const std::string& getName() const { return m_name; }
	char getSymbol() const { return m_symbol; }
	int getHealth() const { return m_health; }
	int getDamage() const { return m_damage; }
	int getGold() const { return m_gold; }

	void reduceHealth(int health) { m_health -= health; }
	bool isDead() const { return m_health <= 0; }
	void addGold(int gold) { m_gold += gold; }
};

class Player : public Creature
{
	int m_level{ 1 };

public:
	Player(std::string_view name)
		: Creature{ name, '@', 10, 1, 0 }
	{
	}

	void levelUp()
	{
		++m_level;
		++m_damage;
	}

	int getLevel() const { return m_level; }
	bool hasWon() const { return m_level >= 20; }
};

int main()
{
	std::cout << "Enter your name: ";
	std::string playerName;
	std::cin >> playerName;

	Player p{ playerName };
	std::cout << "Welcome, " << p.getName() << ".\n";

	std::cout << "You have " << p.getHealth() << " health and are carrying " << p.getGold() << " gold.\n";

	return 0;
}
c) 接下来是 Monster 类。Monster 也继承自 Creature。怪物没有非继承的成员变量。
首先，编写一个从 Creature 继承的空 Monster 类，然后在 Monster 类内部添加一个名为 Type 的枚举，其中包含此游戏中我们将拥有的 3 种怪物的枚举器：`dragon`、`orc` 和 `slime`（你还需要一个 `max_types` 枚举器，因为这稍后会派上用场）。
显示答案
class Monster : public Creature
{
public:
	enum Type
	{
		dragon,
		orc,
		slime,
		max_types
	};
};
d) 每种怪物类型将拥有不同的名称、符号、起始生命值、金币和伤害。以下是每种怪物类型的数据表
类型
名称
符号
生命值
伤害
金币
龙
龙
D
20
4
100
兽人
兽人
o
4
2
25
史莱姆
史莱姆
s
1
1
10
下一步是编写一个 Monster 构造函数，以便我们可以创建怪物。Monster 构造函数应将 Type 枚举作为参数，然后创建一个具有该类型怪物相应统计数据的 Monster。
有多种不同的方法来实现这一点（有些更好，有些更差）。然而在这种情况下，因为我们所有的怪物属性都是预定义的（不是随机或按生物定制的），我们可以使用一个查找表。我们的查找表将是一个 Creature 的 C 风格数组，通过 Type 索引数组将返回该 Type 相应的 Creature。
由于此生物表是怪物特有的，我们可以在 Monster 类中将其定义为 `static inline Creature monsterData[] { }`，并用我们的 Creature 元素进行初始化。
我们的 Monster 构造函数就变得简单了：我们可以调用 Creature 复制构造函数，并传递来自 monsterData 表中相应的 Creature。
以下程序应编译通过
#include <iostream>
#include <string>

int main()
{
	Monster m{ Monster::Type::orc };
	std::cout << "A " << m.getName() << " (" << m.getSymbol() << ") was created.\n";

	return 0;
}
并打印
A orc (o) was created.
显示答案
#include <array>
#include <iostream>
#include <string>
#include <string_view>
 
class Creature
{
protected:
    std::string m_name;
    char m_symbol {};
    int m_health {};
    int m_damage {};
    int m_gold {};
 
public:
     Creature(std::string_view name, char symbol, int health, int damage, int gold)
        : m_name{ name }
        , m_symbol{ symbol }
        , m_health{ health }
        , m_damage{ damage }
        , m_gold{ gold }
    { }
 
    char getSymbol() const { return m_symbol; }
    const std::string& getName() const { return m_name; }
    bool isDead() const { return m_health <= 0; }
    int getGold() const { return m_gold; }
    void addGold(int gold) { m_gold += gold; }
    void reduceHealth(int health) { m_health -= health; }
    int getHealth() const { return m_health; }
    int getDamage() const { return m_damage; }
};
 
class Player : public Creature
{
    int m_level{ 1 };
 
public:
    Player(const std::string& name)
        : Creature{ name, '@', 10, 1, 0 }
    {
    }
 
    void levelUp()
    {
        ++m_level;
        ++m_damage;
    }
 
    int getLevel() const { return m_level; }
    bool hasWon() const { return m_level >= 20; }
};
 
class Monster : public Creature
{
public:
    enum Type
    {
        dragon,
        orc,
        slime,
        max_types
    };
 
private:
    inline static Creature monsterData[] {
        Creature { "dragon", 'D', 20, 4, 100 },
        Creature { "orc", 'o', 4, 2, 25 },
        Creature { "slime", 's', 1, 1, 10 }
        };

    static_assert(std::size(monsterData) == max_types);

public:
    Monster(Type type)
        : Creature{ monsterData[type] }
    {
    }
};
 
int main()
{
    Monster m{ Monster::Type::orc };
    std::cout << "A " << m.getName() << " (" << m.getSymbol() << ") was created.\n";
 
  return 0;
}
e) 最后，向 Monster 添加一个名为 `getRandomMonster()` 的 `static` 函数。此函数应从 `0` 到 `max_types-1` 中选择一个随机数，并返回一个具有该 `Type` 的怪物（通过值）（您需要将 `int` `static_cast` 为 `Type` 才能将其传递给 `Monster` 构造函数）。
第
8.15 课 -- 全局随机数 (Random.h)
包含可用于选择随机数的代码。
以下 main 函数应该运行
#include <iostream>
#include <string>

int main()
{
	for (int i{ 0 }; i < 10; ++i)
	{
		Monster m{ Monster::getRandomMonster() };
		std::cout << "A " << m.getName() << " (" << m.getSymbol() << ") was created.\n";
	}

	return 0;
}
这个程序的结果应该是随机的。
显示答案
#include "Random.h" // https://learncpp.com.cn/cpp-tutorial/global-random-numbers-random-h/
#include <array>
#include <iostream>
#include <string>
#include <string_view>
 
class Creature
{
protected:
    std::string m_name;
    char m_symbol {};
    int m_health {};
    int m_damage {};
    int m_gold {};
 
public:
     Creature(std::string_view name, char symbol, int health, int damage, int gold)
        : m_name{ name }
        , m_symbol{ symbol }
        , m_health{ health }
        , m_damage{ damage }
        , m_gold{ gold }
    { }
 
    char getSymbol() const { return m_symbol; }
    const std::string& getName() const { return m_name; }
    bool isDead() const { return m_health <= 0; }
    int getGold() const { return m_gold; }
    void addGold(int gold) { m_gold += gold; }
    void reduceHealth(int health) { m_health -= health; }
    int getHealth() const { return m_health; }
    int getDamage() const { return m_damage; }
};
 
class Player : public Creature
{
    int m_level{ 1 };
 
public:
    Player(const std::string& name)
        : Creature{ name, '@', 10, 1, 0 }
    {
    }
 
    void levelUp()
    {
        ++m_level;
        ++m_damage;
    }
 
    int getLevel() const { return m_level; }
    bool hasWon() const { return m_level >= 20; }
};
 
class Monster : public Creature
{
public:
    enum Type
    {
        dragon,
        orc,
        slime,
        max_types
    };
 
private:
    inline static Creature monsterData[] {
        Creature { "dragon", 'D', 20, 4, 100 },
        Creature { "orc", 'o', 4, 2, 25 },
        Creature { "slime", 's', 1, 1, 10 }
        };

    static_assert(std::size(monsterData) == max_types);

public:
    Monster(Type type)
        : Creature{ monsterData[type] }
    {
    }
 
    static Monster getRandomMonster()
    {
        int num{ Random::get(0, max_types - 1) };
        return Monster{ static_cast<Type>(num) };
    }
};
 
int main()
{
    for (int i{ 0 }; i < 10; ++i)
    {
        Monster m{ Monster::getRandomMonster() };
        std::cout << "A " << m.getName() << " (" << m.getSymbol() << ") was created.\n";
    }
 
  return 0;
}
f) 我们终于可以编写游戏逻辑了！
以下是游戏规则
玩家一次遭遇一个随机生成的怪物。
对于每个怪物，玩家有两种选择：(R)逃跑或(F)战斗。
如果玩家决定逃跑，他们有 50% 的机会成功逃脱。
如果玩家逃脱，他们将进入下一次遭遇，没有不良影响。
如果玩家没有逃脱，怪物将获得一次免费攻击，然后玩家选择他们的下一个行动。
如果玩家选择战斗，玩家首先攻击。怪物的生命值会因玩家的伤害而减少。
如果怪物死亡，玩家将获得怪物携带的所有金币。玩家还会升级，等级和伤害增加 1。
如果怪物没有死亡，怪物会反击玩家。玩家的生命值会因怪物的伤害而减少。
游戏在玩家死亡（失败）或达到 20 级（胜利）时结束
如果玩家死亡，游戏应该告诉玩家他们当前的等级和拥有的金币数量。
如果玩家获胜，游戏应该告诉玩家他们赢了，以及他们有多少金币
这是一个游戏会话示例
输入你的名字：Alex
欢迎，Alex
你遇到了一只史莱姆 (s)。
(R)逃跑或(F)战斗：f
你攻击史莱姆造成 1 点伤害。
你杀死了史莱姆。
你现在是 2 级了。
你找到了 10 枚金币。
你遇到了一条龙 (D)。
(R)逃跑或(F)战斗：r
你逃跑失败了。
巨龙对你造成了 4 点伤害。
(R)逃跑或(F)战斗：r
你成功逃脱了。
你遇到了一只兽人 (o)。
(R)逃跑或(F)战斗：f
你攻击兽人造成 2 点伤害。
兽人对你造成了 2 点伤害。
(R)逃跑或(F)战斗：f
你攻击兽人造成 2 点伤害。
你杀死了兽人。
你现在是 3 级了。
你找到了 25 枚金币。
你遇到了一条龙 (D)。
(R)逃跑或(F)战斗：r
你逃跑失败了。
巨龙对你造成了 4 点伤害。
你死在了 3 级，拥有 35 枚金币。
可惜你带不走它们！
提示：创建 4 个函数
main() 函数应处理游戏设置（创建 Player）和主游戏循环。
fightMonster() 处理玩家与单个怪物之间的战斗，包括询问玩家想要做什么，处理逃跑或战斗情况。
attackMonster() 处理玩家攻击怪物，包括升级。
attackPlayer() 处理怪物攻击玩家。
显示答案
#include "Random.h" // https://learncpp.com.cn/cpp-tutorial/global-random-numbers-random-h/
#include <array>
#include <iostream>
#include <string>
#include <string_view>
 
class Creature
{
protected:
    std::string m_name;
    char m_symbol {};
    int m_health {};
    int m_damage {};
    int m_gold {};
 
public:
     Creature(std::string_view name, char symbol, int health, int damage, int gold)
        : m_name{ name }
        , m_symbol{ symbol }
        , m_health{ health }
        , m_damage{ damage }
        , m_gold{ gold }
    { }
 
    char getSymbol() const { return m_symbol; }
    const std::string& getName() const { return m_name; }
    bool isDead() const { return m_health <= 0; }
    int getGold() const { return m_gold; }
    void addGold(int gold) { m_gold += gold; }
    void reduceHealth(int health) { m_health -= health; }
    int getHealth() const { return m_health; }
    int getDamage() const { return m_damage; }
};
 
class Player : public Creature
{
    int m_level{ 1 };
 
public:
    Player(const std::string& name)
        : Creature{ name, '@', 10, 1, 0 }
    {
    }
 
    void levelUp()
    {
        ++m_level;
        ++m_damage;
    }
 
    int getLevel() const { return m_level; }
    bool hasWon() const { return m_level >= 20; }
};
 
class Monster : public Creature
{
public:
    enum Type
    {
        dragon,
        orc,
        slime,
        max_types
    };
 
private:
    inline static Creature monsterData[] {
        Creature { "dragon", 'D', 20, 4, 100 },
        Creature { "orc", 'o', 4, 2, 25 },
        Creature { "slime", 's', 1, 1, 10 }
        };

    static_assert(std::size(monsterData) == max_types);

public:
    Monster(Type type)
        : Creature{ monsterData[type] }
    {
    }
 
    static Monster getRandomMonster()
    {
        int num{ Random::get(0, max_types - 1) };
        return Monster{ static_cast<Type>(num) };
    }
};
 
// This function handles the player attacking the monster
void attackMonster(Player& player, Monster& monster)
{
    // If the player is dead, we can't attack the monster
    if (player.isDead())
        return;

    std::cout << "You hit the " << monster.getName() << " for " << player.getDamage() << " damage.\n";

    // Reduce the monster's health by the player's damage
    monster.reduceHealth(player.getDamage());

    // If the monster is now dead, level the player up
    if (monster.isDead())
    {
        std::cout << "You killed the " << monster.getName() << ".\n";
        player.levelUp();
        std::cout << "You are now level " << player.getLevel() << ".\n";
        std::cout << "You found " << monster.getGold() << " gold.\n";
        player.addGold(monster.getGold());
    }
}

// This function handles the monster attacking the player
void attackPlayer(const Monster& monster, Player& player)
{
    // If the monster is dead, it can't attack the player
    if (monster.isDead())
        return;

    // Reduce the player's health by the monster's damage
    player.reduceHealth(monster.getDamage());
    std::cout << "The " << monster.getName() << " hit you for " << monster.getDamage() << " damage.\n";
}

// This function handles the entire fight between a player and a randomly generated monster
void fightMonster(Player& player)
{
    // First randomly generate a monster
    Monster monster{ Monster::getRandomMonster() };
    std::cout << "You have encountered a " << monster.getName() << " (" << monster.getSymbol() << ").\n";

    // While the monster isn't dead and the player isn't dead, the fight continues
    while (!monster.isDead() && !player.isDead())
    {
        std::cout << "(R)un or (F)ight: ";
        char input{};
        std::cin >> input;
        if (input == 'R' || input == 'r')
        {
            // 50% chance of fleeing successfully
            if (Random::get(1, 2) == 1)
            {
                std::cout << "You successfully fled.\n";
                return; // success ends the encounter
            }
            else
            {
                // Failure to flee gives the monster a free attack on the player
                std::cout << "You failed to flee.\n";
                attackPlayer(monster, player);
                continue;
            }
        }

        if (input == 'F' || input == 'f')
        {
            // Player attacks first, monster attacks second
            attackMonster(player, monster);
            attackPlayer(monster, player);
        }
    }
}

int main()
{
    std::cout << "Enter your name: ";
    std::string playerName;
    std::cin >> playerName;

    Player player{ playerName };
    std::cout << "Welcome, " << player.getName() << '\n';

    // If the player isn't dead and hasn't won yet, the game continues
    while (!player.isDead() && !player.hasWon())
        fightMonster(player);

    // At this point, the player is either dead or has won
    if (player.isDead())
    {
        std::cout << "You died at level " << player.getLevel() << " and with " << player.getGold() << " gold.\n";
        std::cout << "Too bad you can't take it with you!\n";
    }
    else
    {
        std::cout << "You won the game with " << player.getGold() << " gold!\n";
    }

  return 0;
}
g) 额外奖励
读者
Tom
没有把剑磨得足够锋利，无法击败强大的巨龙。通过实现以下不同尺寸的药水来帮助他
类型
效果（小型）
效果（中型）
效果（大型）
生命值
+2 生命值
+2 生命值
+5 生命值
力量
+1 伤害
+1 伤害
+1 伤害
毒药
-1 生命值
-1 生命值
-1 生命值
尽情发挥创意，添加更多药水或改变它们的效果！
玩家在每次赢得战斗后有 30% 的机会找到一瓶药水，并可以选择喝或不喝。如果玩家不喝药水，它就会消失。玩家在喝下药水之前不知道药水的类型，喝下后药水的类型和大小会揭示出来，并且效果会生效。
在以下示例中，玩家找到了一瓶毒药并因喝下它而死亡（在此示例中，毒药的伤害性更大）
You have encountered a slime (s).
(R)un or (F)ight: f
You hit the slime for 1 damage.
You killed the slime.
You are now level 2.
You found 10 gold.
You found a mythical potion! Do you want to drink it? [y/n]: y
You drank a Medium potion of Poison
You died at level 2 and with 10 gold.
Too bad you can't take it with you!
显示提示
提示：添加一个 Potion 类，它具有 type 和 size 成员变量，以及一个返回其名称的成员函数和一个创建随机 Potion 的静态成员函数，类似于 getRandomMonster() 函数。
在 Player 类中，添加一个 drinkPotion() 成员函数来应用药水的效果。
显示答案
#include "Random.h" // https://learncpp.com.cn/cpp-tutorial/global-random-numbers-random-h/
#include <array>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>

class Potion
{
public:
    // All possible types of potions
    enum Type
    {
        health,
        strength,
        poison,

        // For random potion generation
        max_type
    };

    enum Size
    {
        small,
        medium,
        large,

        max_size
    };


private:
    Type m_type{};
    Size m_size{};

public:
    Potion(Type type, Size size)
        : m_type{ type },
        m_size{ size }
    {
    }

    Type getType() const { return m_type; }
    Size getSize() const { return m_size; }

    // The names of potions are compile-time literals, we can
    // return a std::string_view.
    static std::string_view getPotionTypeName(Type type)
    {
        static constexpr std::string_view names[] {
          "Health",
          "Strength",
          "Poison"
        };

        return names[type];
    }

    static std::string_view getPotionSizeName(Size size)
    {
        static constexpr std::string_view names[] {
          "Small",
          "Medium",
          "Large"
        };

        return names[size];
    }

    std::string getName() const
    {
        // We use a std::stringstream, but this could also be solved using
        // std::string.
        // We first used std::stringstream in lesson 7.13.
        std::stringstream result{};

        result << getPotionSizeName(getSize()) << " potion of " << getPotionTypeName(getType());

        // We can extract the string from an std::stringstream by using the str()
        // member function.
        return result.str();
    }

    static Potion getRandomPotion()
    {
        return Potion{
          static_cast<Type>(Random::get(0, max_type - 1)),
          static_cast<Size>(Random::get(0, max_size - 1))
        };
    }
};

class Creature
{
protected:
    std::string m_name;
    char m_symbol {};
    int m_health {};
    int m_damage {};
    int m_gold {};
 
public:
     Creature(std::string_view name, char symbol, int health, int damage, int gold)
        : m_name{ name }
        , m_symbol{ symbol }
        , m_health{ health }
        , m_damage{ damage }
        , m_gold{ gold }
    { }
 
    char getSymbol() const { return m_symbol; }
    const std::string& getName() const { return m_name; }
    bool isDead() const { return m_health <= 0; }
    int getGold() const { return m_gold; }
    void addGold(int gold) { m_gold += gold; }
    void reduceHealth(int health) { m_health -= health; }
    int getHealth() const { return m_health; }
    int getDamage() const { return m_damage; }
};
 
class Player : public Creature
{
    int m_level{ 1 };
 
public:
    Player(const std::string& name)
        : Creature{ name, '@', 10, 1, 0 }
    {
    }
 
    void levelUp()
    {
        ++m_level;
        ++m_damage;
    }

    // Applies a potion's effect to the player
    void drinkPotion(const Potion& potion)
    {
        switch (potion.getType())
        {
        case Potion::health:
            // Only a health potion's size affects its power. All other
            // potions are independent of size.
            m_health += ((potion.getSize() == Potion::large) ? 5 : 2);
            break;
        case Potion::strength:
            ++m_damage;
            break;
        case Potion::poison:
            reduceHealth(1);
            break;
            // Handle max_type to silence the compiler warning. Don't use default:
            // because we want the compiler to warn us if we add a new potion but
            // forget to implement its effect.
        case Potion::max_type:
            break;
        }
    }

    int getLevel() const { return m_level; }
    bool hasWon() const { return m_level >= 20; }
};
 
class Monster : public Creature
{
public:
    enum Type
    {
        dragon,
        orc,
        slime,
        max_types
    };
 
private:
    inline static Creature monsterData[] {
        Creature { "dragon", 'D', 20, 4, 100 },
        Creature { "orc", 'o', 4, 2, 25 },
        Creature { "slime", 's', 1, 1, 10 }
        };

    static_assert(std::size(monsterData) == max_types);

public:
    Monster(Type type)
        : Creature{ monsterData[type] }
    {
    }
 
    static Monster getRandomMonster()
    {
        int num{ Random::get(0, max_types - 1) };
        return Monster{ static_cast<Type>(num) };
    }
};

// We moved this out of attackMonster() to keep the function shorter.
void onMonsterKilled(Player& player, const Monster& monster)
{
    std::cout << "You killed the " << monster.getName() << ".\n";
    player.levelUp();
    std::cout << "You are now level " << player.getLevel() << ".\n";
    std::cout << "You found " << monster.getGold() << " gold.\n";
    player.addGold(monster.getGold());

    // 30% chance of finding a potion
    constexpr int potionChance{ 30 };
    if (Random::get(1, 100) <= potionChance)
    {
        // Generate a random potion
        auto potion{ Potion::getRandomPotion() };

        std::cout << "You found a mythical potion! Do you want to drink it? [y/n]: ";
        char choice{};
        std::cin >> choice;

        if (choice == 'Y' || choice == 'y')
        {
            // Apply the effect
            player.drinkPotion(potion);
            // Reveal the potion type and size
            std::cout << "You drank a " << potion.getName() << ".\n";
        }
    }
}

// This function handles the player attacking the monster
void attackMonster(Player& player, Monster& monster)
{
    // If the player is dead, we can't attack the monster
    if (player.isDead())
        return;

    std::cout << "You hit the " << monster.getName() << " for " << player.getDamage() << " damage.\n";

    // Reduce the monster's health by the player's damage
    monster.reduceHealth(player.getDamage());

    // If the monster is now dead, level the player up
    if (monster.isDead())
    {
        // Reward the player
        onMonsterKilled(player, monster);
    }
}

// This function handles the monster attacking the player
void attackPlayer(const Monster& monster, Player& player)
{
    // If the monster is dead, it can't attack the player
    if (monster.isDead())
        return;

    // Reduce the player's health by the monster's damage
    player.reduceHealth(monster.getDamage());
    std::cout << "The " << monster.getName() << " hit you for " << monster.getDamage() << " damage.\n";
}

// This function handles the entire fight between a player and a randomly generated monster
void fightMonster(Player& player)
{
    // First randomly generate a monster
    Monster monster{ Monster::getRandomMonster() };
    std::cout << "You have encountered a " << monster.getName() << " (" << monster.getSymbol() << ").\n";

    // While the monster isn't dead and the player isn't dead, the fight continues
    while (!monster.isDead() && !player.isDead())
    {
        std::cout << "(R)un or (F)ight: ";
        char input{};
        std::cin >> input;
        if (input == 'R' || input == 'r')
        {
            // 50% chance of fleeing successfully
            if (Random::get(1, 2) == 1)
            {
                std::cout << "You successfully fled.\n";
                return; // success ends the encounter
            }
            else
            {
                // Failure to flee gives the monster a free attack on the player
                std::cout << "You failed to flee.\n";
                attackPlayer(monster, player);
                continue;
            }
        }

        if (input == 'F' || input == 'f')
        {
            // Player attacks first, monster attacks second
            attackMonster(player, monster);
            attackPlayer(monster, player);
        }
    }
}

int main()
{
    std::cout << "Enter your name: ";
    std::string playerName;
    std::cin >> playerName;

    Player player{ playerName };
    std::cout << "Welcome, " << player.getName() << '\n';

    // If the player isn't dead and hasn't won yet, the game continues
    while (!player.isDead() && !player.hasWon())
        fightMonster(player);

    // At this point, the player is either dead or has won
    if (player.isDead())
    {
        std::cout << "You died at level " << player.getLevel() << " and with " << player.getGold() << " gold.\n";
        std::cout << "Too bad you can't take it with you!\n";
    }
    else
    {
        std::cout << "You won the game with " << player.getGold() << " gold!\n";
    }

  return 0;
}
下一课
25.1
指向派生对象基类的指针和引用
返回目录
上一课
24.9
多重继承