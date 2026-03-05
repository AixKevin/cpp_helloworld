# 25.x — 第 25 章总结与测验

25.x — 第 25 章总结与测验
Alex
2016 年 11 月 23 日，下午 2:59 PST
2025 年 2 月 19 日
至此，我们对 C++ 继承和虚函数的学习之旅告一段落。读者们，请不要担心，随着我们的继续深入，C++ 还有很多其他领域等待我们探索。
章节总结
C++ 允许您将基类指针和引用设置为派生对象。当我们想要编写一个可以处理从基类派生的任何类型对象的函数或数组时，这非常有用。
如果没有虚函数，基类指针和对派生类的引用将只能访问基类成员变量和函数版本。
虚函数是一种特殊类型的函数，它解析为基类和派生类之间存在的函数的最派生版本（称为重写）。要被视为重写，派生类函数必须与虚基类函数具有相同的签名和返回类型。唯一的例外是协变返回类型，如果基类函数返回指向基类的指针或引用，协变返回类型允许重写返回指向派生类的指针或引用。
旨在作为重写的函数应使用 override 说明符，以确保它确实是重写。
final 说明符可用于阻止函数的重写或类的继承。
如果您打算使用继承，您应该将析构函数设置为虚函数，以便在删除基类指针时调用正确的析构函数。
您可以通过使用作用域解析运算符直接指定您想要的类的函数版本来忽略虚函数解析：例如
base.Base::getName()
。
当编译器遇到直接函数调用时，会发生早期绑定。编译器或链接器可以直接解析这些函数调用。当调用函数指针时，会发生后期绑定。在这种情况下，直到运行时才能解析将调用哪个函数。虚函数使用后期绑定和虚表来确定调用哪个版本的函数。
使用虚函数是有代价的：虚函数调用时间更长，并且虚表的必要性使每个包含虚函数的对象的大小增加了一个指针。
通过在虚函数原型末尾添加“= 0”，可以将虚函数设置为纯虚函数/抽象函数。包含纯虚函数的类称为抽象类，不能实例化。继承纯虚函数的类必须具体定义它们，否则它也将被视为抽象类。纯虚函数可以有函数体，但它们仍然被认为是抽象的。
接口类是没有成员变量且所有函数都是纯虚函数的类。这些类的名称通常以大写字母 I 开头。
虚基类是一个只包含一次的基类，无论它被对象继承多少次。
当派生类分配给基类对象时，基类只接收派生类基类部分的副本。这称为对象切片。
动态转换可用于将指向基类对象的指针转换为指向派生类对象的指针。这称为向下转换。失败的转换将返回空指针。
重载继承类的 operator<< 最简单的方法是为最基类编写一个重载的 operator<<，然后调用一个虚成员函数来完成打印。
小测验时间
以下每个程序都有某种缺陷。检查每个程序（目视检查，不要编译）并确定程序有什么问题。每个程序的输出都应该是“Derived”。
1a)
#include <iostream>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	const char* getName() const { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	const char* getName() const { return "Derived"; }
};

int main()
{
	Derived d{ 5 };
	Base& b{ d };
	std::cout << b.getName() << '\n';

	return 0;
}
显示答案
Base::getName() 未设置为虚函数，因此 b.getName() 未解析为 Derived::getName()。
1b)
#include <iostream>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	virtual const char* getName() { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	virtual const char* getName() const { return "Derived"; }
};

int main()
{
	Derived d{ 5 };
	Base& b{ d };
	std::cout << b.getName() << '\n';

	return 0;
}
显示答案
Base::getName() 是非 const 的，而 Derived::getName() 是 const 的，因此 Derived::getName() 不被视为重写。
1c)
#include <iostream>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	virtual const char* getName() { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	const char* getName() override { return "Derived"; }
};

int main()
{
	Derived d{ 5 };
	Base b{ d };
	std::cout << b.getName() << '\n';

	return 0;
}
显示答案
d 通过值赋给 b，导致 d 被切片。
1d)
#include <iostream>

class Base final
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	virtual const char* getName() { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	const char* getName() override { return "Derived"; }
};

int main()
{
	Derived d{ 5 };
	Base& b{ d };
	std::cout << b.getName() << '\n';

	return 0;
}
显示答案
Base 被声明为 final，因此 Derived 不能从它派生。这将导致编译错误。
1e)
#include <iostream>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	virtual const char* getName() { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	virtual const char* getName() = 0;
};

const char* Derived::getName()
{
	return "Derived";
}

int main()
{
	Derived d{ 5 };
	Base& b{ d };
	std::cout << b.getName() << '\n';

	return 0;
}
显示答案
Derived::getName() 是一个纯虚函数（带有函数体），因此 Derived 是一个不能实例化的抽象类。
1f)
#include <iostream>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	virtual const char* getName() { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	virtual const char* getName() { return "Derived"; }
};

int main()
{
	auto* d{ new Derived(5) };
	Base* b{ d };
	std::cout << b->getName() << '\n';
	delete b;

	return 0;
}
显示答案
这个程序实际上产生了正确的输出，但有另一个问题。我们正在删除 b，它是一个 Base 指针，但我们从未向 Base 类添加虚析构函数。因此，程序只删除了 Derived 对象的 Base 部分，而 Derived 部分则作为内存泄漏留下。
2a) 创建一个名为 Shape 的抽象类。这个类应该有三个函数：一个纯虚打印函数，它接受并返回一个 std::ostream&，一个重载的 operator<< 和一个空的虚析构函数。
显示答案
class Shape
{
public:
	virtual std::ostream& print(std::ostream& out) const = 0;

	friend std::ostream& operator<<(std::ostream& out, const Shape& p)
	{
		return p.print(out);
	}
	virtual ~Shape() = default;
};
2b) 从 Shape 派生两个类：Triangle 和 Circle。Triangle 应该有 3 个 Point 作为成员。Circle 应该有一个中心 Point 和一个整数半径。重写 print() 函数，以便以下程序运行
int main()
{
    Circle c{ Point{ 1, 2 }, 7 };
    std::cout << c << '\n';

    Triangle t{Point{ 1, 2 }, Point{ 3, 4 }, Point{ 5, 6 }};
    std::cout << t << '\n';

    return 0;
}
这应该打印
Circle(Point(1, 2), radius 7)
Triangle(Point(1, 2), Point(3, 4), Point(5, 6))
这是一个你可以使用的 Point 类
class Point
{
private:
	int m_x{};
	int m_y{};

public:
	Point(int x, int y)
		: m_x{ x }, m_y{ y }
	{

	}

	friend std::ostream& operator<<(std::ostream& out, const Point& p)
	{
		return out << "Point(" << p.m_x << ", " << p.m_y << ')';
	}
};
显示答案
#include <iostream>

class Point
{
private:
	int m_x{};
	int m_y{};

public:
	Point(int x, int y)
		: m_x{ x }, m_y{ y }
	{

	}

	friend std::ostream& operator<<(std::ostream& out, const Point& p)
	{
		return out << "Point(" << p.m_x << ", " << p.m_y << ')';
	}
};

class Shape
{
public:
	virtual std::ostream& print(std::ostream& out) const = 0;

	friend std::ostream& operator<<(std::ostream& out, const Shape& p)
	{
		return p.print(out);
	}
	virtual ~Shape() = default;
};

class Triangle : public Shape
{
private:
	Point m_p1;
	Point m_p2;
	Point m_p3;

public:
	Triangle(const Point& p1, const Point& p2, const Point& p3)
		: m_p1{ p1 }, m_p2{ p2 }, m_p3{ p3 }
	{
	}

	std::ostream& print(std::ostream& out) const override
	{
		return out << "Triangle(" << m_p1 << ", " << m_p2 << ", " << m_p3 << ')';
	}
};

class Circle : public Shape
{
private:
	Point m_center;
	int m_radius;

public:
	Circle(const Point& center, int radius)
		: m_center{ center }, m_radius{ radius }
	{
	}

	std::ostream& print(std::ostream& out) const override
	{
		return out << "Circle(" << m_center << ", radius " << m_radius << ')';
	}
};

int main()
{
	Circle c{ Point{ 1, 2 }, 7 };
	std::cout << c << '\n';

	Triangle t{ Point{ 1, 2 }, Point{ 3, 4 }, Point{ 5, 6 } };
	std::cout << t << '\n';

	return 0;
}
2c) 给出上述类（Point、Shape、Circle 和 Triangle），完成以下程序
#include <vector>
#include <iostream>

int main()
{
	std::vector<Shape*> v{
	  new Circle{Point{ 1, 2 }, 7},
	  new Triangle{Point{ 1, 2 }, Point{ 3, 4 }, Point{ 5, 6 }},
	  new Circle{Point{ 7, 8 }, 3}
	};

	// print each shape in vector v on its own line here

	std::cout << "The largest radius is: " << getLargestRadius(v) << '\n'; // write this function

	// delete each element in the vector here

	return 0;
}
程序应该打印以下内容
Circle(Point(1, 2), radius 7)
Triangle(Point(1, 2), Point(3, 4), Point(5, 6))
Circle(Point(7, 8), radius 3)
The largest radius is: 7
提示：您需要向 Circle 添加一个 getRadius() 函数，并将 Shape* 向下转换为 Circle* 才能访问它。
显示答案
#include <vector>
#include <iostream>
#include <algorithm> // for std::max

class Point
{
private:
	int m_x{};
	int m_y{};

public:
	Point(int x, int y)
		: m_x{ x }, m_y{ y }
	{

	}

	friend std::ostream& operator<<(std::ostream& out, const Point& p)
	{
		return out << "Point(" << p.m_x << ", " << p.m_y << ')';
	}
};

class Shape
{
public:
	virtual std::ostream& print(std::ostream& out) const = 0;

	friend std::ostream& operator<<(std::ostream& out, const Shape& p)
	{
		return p.print(out);
	}
	virtual ~Shape() = default;
};

class Triangle : public Shape
{
private:
	Point m_p1;
	Point m_p2;
	Point m_p3;

public:
	Triangle(const Point& p1, const Point& p2, const Point& p3)
		: m_p1{ p1 }, m_p2{ p2 }, m_p3{ p3 }
	{
	}

	std::ostream& print(std::ostream& out) const override
	{
		return out << "Triangle(" << m_p1 << ", " << m_p2 << ", " << m_p3 << ')';
	}
};


class Circle : public Shape
{
private:
	Point m_center;
	int m_radius{};

public:
	Circle(const Point& center, int radius)
		: m_center{ center }, m_radius{ radius }
	{
	}

	std::ostream& print(std::ostream& out) const override
	{
		out << "Circle(" << m_center << ", radius " << m_radius << ')';
		return out;
	}

	int getRadius() const { return m_radius; }
};

// h/t to reader Olivier for this updated solution
// assumes radiuses are >= 0
int getLargestRadius(const std::vector<Shape*>& v)
{
	int largestRadius{ 0 };

	// Loop through all the shapes in the vector
	for (const auto* element : v)
	{
		// // Ensure the dynamic cast succeeds by checking for a null pointer result
		if (auto* c { dynamic_cast<const Circle*>(element) })
		{
			largestRadius = std::max(largestRadius, c->getRadius());
		}
	}

	return largestRadius;
}
int main()
{
	std::vector<Shape*> v{
		  new Circle{Point{ 1, 2 }, 7},
		  new Triangle{Point{ 1, 2 }, Point{ 3, 4 }, Point{ 5, 6 }},
		  new Circle{Point{ 7, 8 }, 3}
	};

	for (const auto* element : v) // element will be a Shape*
		std::cout << *element << '\n';

	std::cout << "The largest radius is: " << getLargestRadius(v) << '\n';

	for (const auto* element : v)
		delete element;

	return 0;
}
2d) 额外加分：更新之前的解决方案以使用
std::vector<std::unique_ptr<Shape>>
。请记住
std::unique_ptr
是不可复制的。
此想法感谢读者 surrealcereal。
显示提示
提示：您不能使用 std::initializer_list 初始化向量，因为这需要复制元素。
显示提示
提示：std::unique_ptr::get() 返回指向所管理元素的指针。
显示答案
#include <vector>
#include <iostream>
#include <algorithm> // for std::max
#include <memory>

class Point
{
private:
	int m_x{};
	int m_y{};

public:
	Point(int x, int y)
		: m_x{ x }, m_y{ y }
	{

	}

	friend std::ostream& operator<<(std::ostream& out, const Point& p)
	{
		return out << "Point(" << p.m_x << ", " << p.m_y << ')';
	}
};

class Shape
{
public:
	virtual std::ostream& print(std::ostream& out) const = 0;

	friend std::ostream& operator<<(std::ostream& out, const Shape& p)
	{
		return p.print(out);
	}
	virtual ~Shape() = default;
};

class Triangle : public Shape
{
private:
	Point m_p1;
	Point m_p2;
	Point m_p3;

public:
	Triangle(const Point& p1, const Point& p2, const Point& p3)
		: m_p1{ p1 }, m_p2{ p2 }, m_p3{ p3 }
	{
	}

	std::ostream& print(std::ostream& out) const override
	{
		return out << "Triangle(" << m_p1 << ", " << m_p2 << ", " << m_p3 << ')';
	}
};


class Circle : public Shape
{
private:
	Point m_center;
	int m_radius{};

public:
	Circle(const Point& center, int radius)
		: m_center{ center }, m_radius{ radius }
	{
	}

	std::ostream& print(std::ostream& out) const override
	{
		out << "Circle(" << m_center << ", radius " << m_radius << ')';
		return out;
	}

	int getRadius() const { return m_radius; }
};

int getLargestRadius(const std::vector<std::unique_ptr<Shape>>& v)
{
	int largestRadius{ 0 };

	// Loop through all the shapes in the vector
	for (const auto& element : v)
	{
		// // Ensure the dynamic cast succeeds by checking for a null pointer result
		if (auto *c { dynamic_cast<const Circle*>(element.get()) })
		{
			largestRadius = std::max(largestRadius, c->getRadius());
		}
	}

	return largestRadius;
}
int main()
{
	std::vector<std::unique_ptr<Shape>> v;
	v.reserve(3);
	v.push_back(std::make_unique<Circle>(Point{1, 2}, 7));
	v.push_back(std::make_unique<Triangle>(Point{1, 2}, Point{3, 4}, Point{5, 6}));
	v.push_back(std::make_unique<Circle>(Point{7, 8}, 3));

	for (const auto& element : v) std::cout << *element << '\n';
    
	std::cout << "The largest radius is: " << getLargestRadius(v) << '\n';
}
下一课
26.1
模板类
返回目录
上一课
25.11
使用 operator<< 打印继承类