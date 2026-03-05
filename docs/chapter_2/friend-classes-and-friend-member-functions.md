# 15.9 — 友元类和友元成员函数

15.9 — 友元类和友元成员函数
Alex
2023 年 9 月 11 日下午 1:05 PDT
2024 年 4 月 30 日
友元类
友元类
是可以访问另一个类的私有和受保护成员的类。
这是一个示例
#include <iostream>

class Storage
{
private:
    int m_nValue {};
    double m_dValue {};
public:
    Storage(int nValue, double dValue)
       : m_nValue { nValue }, m_dValue { dValue }
    { }

    // Make the Display class a friend of Storage
    friend class Display;
};

class Display
{
private:
    bool m_displayIntFirst {};

public:
    Display(bool displayIntFirst)
         : m_displayIntFirst { displayIntFirst }
    {
    }

    // Because Display is a friend of Storage, Display members can access the private members of Storage
    void displayStorage(const Storage& storage)
    {
        if (m_displayIntFirst)
            std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
        else // display double first
            std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
    }

    void setDisplayIntFirst(bool b)
    {
         m_displayIntFirst = b;
    }
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };

    display.displayStorage(storage);

    display.setDisplayIntFirst(true);
    display.displayStorage(storage);

    return 0;
}
由于 `Display` 类是 `Storage` 的友元，`Display` 的成员可以访问它们有权访问的任何 `Storage` 对象的私有成员。
此程序产生以下结果：
6.7 5
5 6.7
关于友元类的一些额外说明。
首先，即使 `Display` 是 `Storage` 的友元，`Display` 也无法访问 `Storage` 对象的 `*this` 指针（因为 `*this` 实际上是一个函数参数）。
其次，友元关系不是相互的。仅仅因为 `Display` 是 `Storage` 的友元，并不意味着 `Storage` 也是 `Display` 的友元。如果你希望两个类互为友元，则两者都必须声明对方为友元。
作者注
如果这个有点触及痛处，抱歉！
类友元关系也不是传递的。如果类 A 是 B 的友元，B 是 C 的友元，这并不意味着 A 是 C 的友元。
致进阶读者
友元关系也不会被继承。如果类 A 将 B 设为友元，则从 B 派生的类不是 A 的友元。
友元类声明充当被友元类的前向声明。这意味着我们不需要在友元化之前前向声明被友元的类。在上面的示例中，`friend class Display` 既充当 `Display` 的前向声明，又充当友元声明。
友元成员函数
除了将整个类设为友元之外，你还可以将单个成员函数设为友元。这与将非成员函数设为友元类似，只是使用了成员函数的名称。
然而，实际上，这可能比预期的要棘手一些。让我们将前面的示例转换为将 `Display::displayStorage` 设为友元成员函数。你可能会尝试这样做
#include <iostream>

class Display; // forward declaration for class Display

class Storage
{
private:
	int m_nValue {};
	double m_dValue {};
public:
	Storage(int nValue, double dValue)
		: m_nValue { nValue }, m_dValue { dValue }
	{
	}

	// Make the Display::displayStorage member function a friend of the Storage class
	friend void Display::displayStorage(const Storage& storage); // error: Storage hasn't seen the full definition of class Display
};

class Display
{
private:
	bool m_displayIntFirst {};

public:
	Display(bool displayIntFirst)
		: m_displayIntFirst { displayIntFirst }
	{
	}

	void displayStorage(const Storage& storage)
	{
		if (m_displayIntFirst)
			std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
		else // display double first
			std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
	}
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };
    display.displayStorage(storage);

    return 0;
}
然而，事实证明这行不通。为了将单个成员函数设为友元，编译器必须已经看到了友元成员函数所属类的完整定义（而不仅仅是前向声明）。由于类 `Storage` 尚未看到类 `Display` 的完整定义，因此在尝试将成员函数设为友元时，编译器会报错。
幸运的是，这很容易解决，只需将 `Display` 类的定义移动到 `Storage` 类的定义之前（可以在同一个文件中，也可以通过将 `Display` 的定义移动到头文件并在定义 `Storage` 之前 `#include` 它）。
#include <iostream>

class Display
{
private:
	bool m_displayIntFirst {};

public:
	Display(bool displayIntFirst)
		: m_displayIntFirst { displayIntFirst }
	{
	}

	void displayStorage(const Storage& storage) // compile error: compiler doesn't know what a Storage is
	{
		if (m_displayIntFirst)
			std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
		else // display double first
			std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
	}
};

class Storage
{
private:
	int m_nValue {};
	double m_dValue {};
public:
	Storage(int nValue, double dValue)
		: m_nValue { nValue }, m_dValue { dValue }
	{
	}

	// Make the Display::displayStorage member function a friend of the Storage class
	friend void Display::displayStorage(const Storage& storage); // okay now
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };
    display.displayStorage(storage);

    return 0;
}
然而，我们现在遇到了另一个问题。由于成员函数 `Display::displayStorage()` 使用 `Storage` 作为引用参数，并且我们刚刚将 `Storage` 的定义移动到 `Display` 的定义之下，编译器会抱怨它不知道 `Storage` 是什么。我们无法通过重新排列定义顺序来解决这个问题，因为那样会撤销我们之前的修复。
幸运的是，这也可以通过几个简单的步骤解决。首先，我们可以添加 `class Storage` 作为前向声明，这样编译器在看到类的完整定义之前，对 `Storage` 的引用就没问题了。
其次，我们可以将 `Display::displayStorage()` 的定义移出类，放在 `Storage` 类的完整定义之后。
这看起来像这样
#include <iostream>

class Storage; // forward declaration for class Storage

class Display
{
private:
	bool m_displayIntFirst {};

public:
	Display(bool displayIntFirst)
		: m_displayIntFirst { displayIntFirst }
	{
	}

	void displayStorage(const Storage& storage); // forward declaration for Storage needed for reference here
};

class Storage // full definition of Storage class
{
private:
	int m_nValue {};
	double m_dValue {};
public:
	Storage(int nValue, double dValue)
		: m_nValue { nValue }, m_dValue { dValue }
	{
	}

	// Make the Display::displayStorage member function a friend of the Storage class
	// Requires seeing the full definition of class Display (as displayStorage is a member)
	friend void Display::displayStorage(const Storage& storage);
};

// Now we can define Display::displayStorage
// Requires seeing the full definition of class Storage (as we access Storage members)
void Display::displayStorage(const Storage& storage)
{
	if (m_displayIntFirst)
		std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
	else // display double first
		std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
}

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };
    display.displayStorage(storage);

    return 0;
}
现在一切都将正确编译：`class Storage` 的前向声明足以满足 `Display` 类中 `Display::displayStorage()` 的声明。`Display` 的完整定义满足将 `Display::displayStorage()` 声明为 `Storage` 的友元。`Storage` 类的完整定义足以满足成员函数 `Display::displayStorage()` 的定义。
如果这有点令人困惑，请参见上面程序中的注释。关键点是类的前向声明满足对类的引用。但是，访问类的成员需要编译器已经看到了完整的类定义。
如果这看起来很麻烦——确实如此。幸运的是，这种“舞蹈”只在我们将所有内容都放在一个文件中时才需要。更好的解决方案是将每个类定义放在单独的头文件中，并将成员函数定义放在相应的 .cpp 文件中。这样，所有类定义都将在 .cpp 文件中可用，并且不需要重新排列类或函数！
小测验时间
问题 #1
在几何学中，点是空间中的一个位置。我们可以将 3D 空间中的点定义为坐标 x、y 和 z 的集合。例如，`Point { 2.0, 1.0, 0.0 }` 将是坐标空间中 x=2.0、y=1.0 和 z=0.0 的点。
在物理学中，矢量是一个具有大小（长度）和方向（但没有位置）的量。我们可以将 3D 空间中的矢量定义为表示矢量沿 x、y 和 z 轴方向的 x、y 和 z 值（长度可以从这些值推导出来）。例如，`Vector { 2.0, 0.0, 0.0 }` 将是表示沿正 x 轴（仅）方向的矢量，长度为 2.0。
可以将 `Vector` 应用于 `Point` 以将 `Point` 移动到新位置。这是通过将矢量的方向添加到点的位置以产生新位置来完成的。例如，`Point { 2.0, 1.0, 0.0 }` + `Vector { 2.0, 0.0, 0.0 }` 将产生 `Point { 4.0, 1.0, 0.0 }`。
这样的点和矢量通常用于计算机图形学中（点表示形状的顶点，矢量表示形状的移动）。
给定以下程序：
#include <iostream>

class Vector3d
{
private:
	double m_x{};
	double m_y{};
	double m_z{};

public:
	Vector3d(double x, double y, double z)
		: m_x{x}, m_y{y}, m_z{z}
	{
	}

	void print() const
	{
		std::cout << "Vector(" << m_x << ", " << m_y << ", " << m_z << ")\n";
	}
};

class Point3d
{
private:
	double m_x{};
	double m_y{};
	double m_z{};

public:
	Point3d(double x, double y, double z)
		: m_x{x}, m_y{y}, m_z{z}
	{ }

	void print() const
	{
		std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ")\n";
	}

	void moveByVector(const Vector3d& v)
	{
		// implement this function as a friend of class Vector3d
	}
};

int main()
{
	Point3d p { 1.0, 2.0, 3.0 };
	Vector3d v { 2.0, 2.0, -3.0 };

	p.print();
	p.moveByVector(v);
	p.print();

	return 0;
}
> 步骤 #1
使 `Point3d` 成为 `Vector3d` 的友元类，并实现函数 `Point3d::moveByVector()`。
显示答案
#include <iostream>

class Vector3d
{
private:
	double m_x{};
	double m_y{};
	double m_z{};

public:
	Vector3d(double x, double y, double z)
		: m_x{x}, m_y{y}, m_z{z}
	{

	}

	void print() const
	{
		std::cout << "Vector(" << m_x << ", " << m_y << ", " << m_z << ")\n";
	}

	friend class Point3d; // Point3d is now a friend of class Vector3d
};


class Point3d
{
private:
	double m_x{};
	double m_y{};
	double m_z{};

public:
	Point3d(double x, double y, double z)
		: m_x{x}, m_y{y}, m_z{z}
	{

	}

	void print() const
	{
		std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ")\n";
	}


	void moveByVector(const Vector3d& v)
	{
		m_x += v.m_x;
		m_y += v.m_y;
		m_z += v.m_z;
	}
};


int main()
{
	Point3d p { 1.0, 2.0, 3.0 };
	Vector3d v { 2.0, 2.0, -3.0 };

	p.print();
	p.moveByVector(v);
	p.print();

	return 0;
}
> 步骤 #2
不是将类 `Point3d` 设为类 `Vector3d` 的友元，而是将成员函数 `Point3d::moveByVector` 设为类 `Vector3d` 的友元。
显示答案
#include <iostream>

class Vector3d; // first, we need to tell the compiler that a class named Vector3d exists

class Point3d
{
private:
	double m_x{};
	double m_y{};
	double m_z{};

public:
	Point3d(double x, double y, double z)
		: m_x{x}, m_y{y}, m_z{z}
	{

	}

	void print() const
	{
		std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ")\n";
	}

	void moveByVector(const Vector3d& v); // so we can use Vector3d here
       // note: we can't define this function here, because Vector3d hasn't been defined yet (just forward declared)
};

class Vector3d
{
private:
	double m_x{};
	double m_y{};
	double m_z{};

public:
	Vector3d(double x, double y, double z)
		: m_x{x}, m_y{y}, m_z{z}
	{

	}

	void print() const
	{
		std::cout << "Vector(" << m_x << ", " << m_y << ", " << m_z << ")\n";
	}

	friend void Point3d::moveByVector(const Vector3d& v); // Point3d::moveByVector() is now a friend of class Vector3d
};

// Now that Vector3d has been defined, we can define the function Point3d::moveByVector()
void Point3d::moveByVector(const Vector3d& v)
{
	m_x += v.m_x;
	m_y += v.m_y;
	m_z += v.m_z;
}

int main()
{
	Point3d p { 1.0, 2.0, 3.0 };
	Vector3d v { 2.0, 2.0, -3.0 };

	p.print();
	p.moveByVector(v);
	p.print();

	return 0;
}
> 步骤 #3
使用 5 个单独的文件重新实现前一步的解决方案：Point3d.h、Point3d.cpp、Vector3d.h、Vector3d.cpp 和 main.cpp。
感谢读者 Shiva 的建议和解决方案。
显示答案
Point3d.h
// Header file that defines the Point3d class

#ifndef POINT3D_H
#define POINT3D_H

class Vector3d; // forward declaration for class Vector3d for function moveByVector()

class Point3d
{
    private:
        double m_x{};
        double m_y{};
        double m_z{};

    public:
        Point3d(double x, double y, double z);

        void print() const;
        void moveByVector(const Vector3d& v); // forward declaration above needed for this line
};

#endif
Point3d.cpp
// Member functions of the Point3d class defined here

#include "Point3d.h" // Point3d class defined here
#include "Vector3d.h" // for the parameter of the function moveByVector()

#include <iostream>

Point3d::Point3d(double x, double y, double z)
  : m_x{x}, m_y{y}, m_z{z}
{}

void Point3d::moveByVector(const Vector3d& v)
{
    // Add the vector components to the corresponding point coordinates
    m_x += v.m_x;
    m_y += v.m_y;
    m_z += v.m_z;
}

void Point3d::print() const
{
    std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ")\n";
}
Vector3d.h
// Header file that defines the Vector3d class

#ifndef VECTOR3D_H
#define VECTOR3D_H

#include "Point3d.h" // for declaring Point3d::moveByVector() as a friend

class Vector3d
{
    private:
        double m_x{};
        double m_y{};
        double m_z{};

    public:
        Vector3d(double x, double y, double z);

        void print() const;
        friend void Point3d::moveByVector(const Vector3d& v);
};

#endif
Vector3d.cpp
// Member functions of the Vector3d class defined here

#include "Vector3d.h" // Vector3d class defined in this file

#include <iostream>

Vector3d::Vector3d(double x, double y, double z)
  : m_x{x}, m_y{y}, m_z{z}
{}

void Vector3d::print() const
{
    std::cout << "Vector(" << m_x << " , " << m_y << " , " << m_z << ")\n";
}
main.cpp
#include "Vector3d.h"
#include "Point3d.h"

int main()
{
    Point3d p { 1.0, 2.0, 3.0 };
    Vector3d v { 2.0, 2.0, -3.0 };

    p.print();
    p.moveByVector(v);
    p.print();

    return 0;
}
下一课
15.10
引用限定符
返回目录
上一课
15.8
友元非成员函数