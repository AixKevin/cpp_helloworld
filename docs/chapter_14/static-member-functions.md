# 15.7 — 静态成员函数

15.7 — 静态成员函数
Alex
2007年9月18日，上午9:08 PDT
2024年10月18日
在上一课
15.6 -- 静态成员变量
中，你了解到静态成员变量是属于类而不是类对象的成员变量。如果静态成员变量是 public 的，它可以使用类名和作用域解析运算符直接访问
#include <iostream>

class Something
{
public:
    static inline int s_value { 1 };
};

int main()
{
    std::cout << Something::s_value; // s_value is public, we can access it directly
}
但是如果静态成员变量是 private 的呢？考虑以下示例
#include <iostream>

class Something
{
private: // now private
    static inline int s_value { 1 };
};

int main()
{
    std::cout << Something::s_value; // error: s_value is private and can't be accessed directly outside the class
}
在这种情况下，我们不能直接从
main()
访问
Something::s_value
，因为它是 private 的。通常我们通过 public 成员函数访问 private 成员。虽然我们可以创建一个普通的 public 成员函数来访问
s_value
，但那样我们就需要实例化一个类类型的对象才能使用该函数！
#include <iostream>

class Something
{
private:
    static inline int s_value { 1 };

public:
    int getValue() { return s_value; }
};

int main()
{
    Something s{};
    std::cout << s.getValue(); // works, but requires us to instantiate an object to call getValue()
}
我们可以做得更好。
静态成员函数
成员变量并不是唯一可以设为静态的成员类型。成员函数也可以设为静态。这是上面带有静态成员函数访问器的示例
#include <iostream>

class Something
{
private:
    static inline int s_value { 1 };

public:
    static int getValue() { return s_value; } // static member function
};

int main()
{
    std::cout << Something::getValue() << '\n';
}
由于静态成员函数不与特定对象关联，因此它们可以直接通过类名和作用域解析运算符调用（例如
Something::getValue()
）。与静态成员变量一样，它们也可以通过类类型的对象调用，尽管不推荐这样做。
静态成员函数没有
this
指针
静态成员函数有两个值得注意的有趣怪癖。首先，因为静态成员函数不依附于对象，所以它们没有
this
指针！仔细想想这很合理——
this
指针总是指向成员函数正在操作的对象。静态成员函数不操作对象，所以不需要
this
指针。
其次，静态成员函数可以直接访问其他静态成员（变量或函数），但不能访问非静态成员。这是因为非静态成员必须属于类对象，而静态成员函数没有类对象可供操作！
在类定义之外定义的静态成员
静态成员函数也可以在类声明之外定义。这与普通成员函数的工作方式相同。
#include <iostream>

class IDGenerator
{
private:
    static inline int s_nextID { 1 };

public:
     static int getNextID(); // Here's the declaration for a static function
};

// Here's the definition of the static function outside of the class.  Note we don't use the static keyword here.
int IDGenerator::getNextID() { return s_nextID++; } 

int main()
{
    for (int count{ 0 }; count < 5; ++count)
        std::cout << "The next ID is: " << IDGenerator::getNextID() << '\n';

    return 0;
}
这个程序打印
The next ID is: 1
The next ID is: 2
The next ID is: 3
The next ID is: 4
The next ID is: 5
请注意，由于此类的所有数据和函数都是静态的，我们不需要实例化类的对象即可使用其功能！此类使用静态成员变量来保存要分配的下一个 ID 的值，并提供一个静态成员函数来返回该 ID 并递增它。
如课程
15.2 -- 类和头文件
中所述，在类定义内部定义的成员函数是隐式内联的。在类定义外部定义的成员函数不是隐式内联的，但可以使用
inline
关键字使其内联。因此，在头文件中定义的静态成员函数应该声明为
inline
，这样当该头文件被包含到多个翻译单元时才不会违反单定义规则 (ODR)。
关于所有成员都是静态的类的警告
在编写所有成员都是静态的类时要小心。尽管这种“纯静态类”（也称为“单态”）可能很有用，但它们也伴随着一些潜在的缺点。
首先，由于所有静态成员只实例化一次，因此无法拥有纯静态类的多个副本（除非克隆类并重命名它）。例如，如果您需要两个独立的
IDGenerator
，这对于纯静态类是不可能的。
其次，在关于全局变量的课程中，您了解到全局变量很危险，因为任何一段代码都可以更改全局变量的值，并最终破坏另一段看似不相关的代码。对于纯静态类也是如此。由于所有成员都属于类（而不是类对象），并且类声明通常具有全局作用域，因此纯静态类本质上等同于在全局可访问的命名空间中声明函数和全局变量，并具有全局变量所带来的所有固有缺点。
与其编写所有成员都是静态的类，不如考虑编写一个普通类并实例化它的一个全局实例（全局变量具有静态持续时间）。这样，在适当的时候可以使用全局实例，但如果需要，仍然可以实例化局部实例。
纯静态类与命名空间
纯静态类与命名空间有很多重叠。它们都允许您在其作用域区域内定义具有静态持续时间的变量和函数。然而，一个显著的区别是类具有访问控制，而命名空间没有。
通常，当您有静态数据成员和/或需要访问控制时，静态类是更可取的。否则，首选命名空间。
C++ 不支持静态构造函数
如果你可以通过构造函数初始化普通成员变量，那么推而广之，你应该能够通过静态构造函数初始化静态成员变量。虽然一些现代语言确实支持静态构造函数以实现此目的，但不幸的是，C++ 不是其中之一。
如果你的静态变量可以直接初始化，则不需要构造函数：你可以在定义时初始化静态成员变量（即使它是私有的）。我们在上面的
IDGenerator
示例中就是这样做的。这是另一个例子
#include <iostream>

struct Chars
{
    char first{};
    char second{};
    char third{};
    char fourth{};
    char fifth{};
};

struct MyClass
{
	static inline Chars s_mychars { 'a', 'e', 'i', 'o', 'u' }; // initialize static variable at point of definition
};

int main()
{
    std::cout << MyClass::s_mychars.third; // print i

    return 0;
}
如果初始化静态成员变量需要执行代码（例如循环），有许多不同且有些晦涩的方法可以做到这一点。一种适用于所有变量（静态或非静态）的方法是使用函数创建对象，用数据填充它，然后将其返回给调用者。这个返回的值可以复制到正在初始化的对象中。
#include <iostream>

struct Chars
{
    char first{};
    char second{};
    char third{};
    char fourth{};
    char fifth{};
};

class MyClass
{
private:
    static Chars generate()
    {
        Chars c{}; // create an object
        c.first = 'a'; // fill it with values however you like
        c.second = 'e';
        c.third = 'i';
        c.fourth = 'o';
        c.fifth = 'u';
        
        return c; // return the object
    }

public:
	static inline Chars s_mychars { generate() }; // copy the returned object into s_mychars
};

int main()
{
    std::cout << MyClass::s_mychars.third; // print i

    return 0;
}
相关内容
Lambda 表达式也可以用于此。
我们在课程
8.15 -- 全局随机数 (Random.h)
中展示了这种方法的实际示例（尽管我们使用命名空间而不是静态类，但其工作方式相同）
小测验时间
问题 #1
将以下示例中的
Random
命名空间转换为具有静态成员的类
#include <chrono>
#include <random>
#include <iostream>

namespace Random
{
	inline std::mt19937 generate()
	{
		std::random_device rd{};

		// Create seed_seq with high-res clock and 7 random numbers from std::random_device
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };

		return std::mt19937{ ss };
	}

	inline std::mt19937 mt{ generate() }; // generates a seeded std::mt19937 and copies it into our global object

	// Generate a random int between [min, max] (inclusive)
	inline int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}
}

int main()
{
	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 10; ++count)
		std::cout << Random::get(1, 6) << '\t';

	std::cout << '\n';

	return 0;
}
显示答案
#include <chrono>
#include <random>
#include <iostream>

class Random
{
private: // could be public if we want these to be accessible
	static std::mt19937 generate()
	{
		std::random_device rd{};

		// Create seed_seq with high-res clock and 7 random numbers from std::random_device
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };

		return std::mt19937{ ss };
	}

	static inline std::mt19937 mt{ generate() }; // generates a seeded std::mt19937 and copies it into our global object

public:
	// Generate a random int between [min, max] (inclusive)
	static int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}
};

int main()
{
	// Print a bunch of random numbers
	for (int count{ 1 }; count <= 10; ++count)
		std::cout << Random::get(1, 6) << '\t';

	std::cout << '\n';

	return 0;
}
在命名空间中声明的任何对象都是全局变量。当我们在命名空间内部声明
inline std::mt19937 mt
时，我们是将
mt
声明为内联全局变量。这允许整个程序使用
std::mt19937
的单个实例（通过全局变量
mt
）。
相比之下，当实例化一个类对象时，该类对象包含每个非静态数据成员的一个副本。我们不希望每个类对象都有自己的
std::mt19937
副本。因此，我们声明
static inline std::mt19937 mt
，这告诉编译器
std::mt19937
的单个实例应该作为
Random
类的一部分存在。将
mt
定义为
static inline
使其成为一个内联变量，允许我们在类定义内部对其进行初始化（我们在课程
15.6 -- 静态成员变量
中介绍了这一点）。
我们还将成员函数设为
static
，以便无需实例化
Random
对象即可访问它们。
下一课
15.8
友元非成员函数
返回目录
上一课
15.6
静态成员变量