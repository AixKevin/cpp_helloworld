# 21.10 — 重载圆括号运算符

21.10 — 重载圆括号运算符
Alex
2007 年 10 月 25 日，下午 1:19 PDT
2024 年 11 月 14 日
到目前为止，你所见过的所有重载运算符都允许你定义运算符参数的类型，但不能定义参数的数量（参数数量是根据运算符的类型固定的）。例如，operator== 总是接受两个参数，而 operator! 总是接受一个参数。圆括号运算符 (operator()) 是一个特别有趣的运算符，因为它允许你更改其接受的参数类型和数量。
需要记住两件事：首先，圆括号运算符必须作为成员函数实现。其次，在非面向对象的 C++ 中，() 运算符用于调用函数。对于类，operator() 只是一个普通的运算符，它像任何其他重载运算符一样调用一个函数（名为 operator()）。
一个例子
让我们看一个适合重载此运算符的例子
class Matrix
{
private:
    double data[4][4]{};
};
矩阵是线性代数的关键组成部分，常用于几何建模和 3D 计算机图形工作。在这种情况下，你只需要认识到 Matrix 类是一个 4 乘 4 的二维双精度浮点数数组。
在关于
重载下标运算符
的课程中，你学到我们可以重载 operator[] 来提供对私有一维数组的直接访问。然而，在这种情况下，我们想要访问私有二维数组。在 C++23 之前，operator[] 仅限于单个参数，因此不足以让我们直接索引二维数组。
但是，因为 () 运算符可以接受我们想要的任意数量的参数，我们可以声明一个接受两个整数索引参数的 operator() 版本，并使用它来访问我们的二维数组。这是一个例子
#include <cassert> // for assert()

class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const; // for const objects
};

double& Matrix::operator()(int row, int col)
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

double Matrix::operator()(int row, int col) const
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}
现在我们可以声明一个 Matrix 并像这样访问其元素
#include <iostream>

int main()
{
    Matrix matrix;
    matrix(1, 2) = 4.5;
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
结果是
4.5
现在，让我们再次重载 () 运算符，这次是以不带任何参数的方式
#include <cassert> // for assert()
class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const;
    void operator()();
};

double& Matrix::operator()(int row, int col)
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

double Matrix::operator()(int row, int col) const
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

void Matrix::operator()()
{
    // reset all elements of the matrix to 0.0
    for (int row{ 0 }; row < 4; ++row)
    {
        for (int col{ 0 }; col < 4; ++col)
        {
            m_data[row][col] = 0.0;
        }
    }
}
这是我们的新示例
#include <iostream>

int main()
{
    Matrix matrix{};
    matrix(1, 2) = 4.5;
    matrix(); // erase matrix
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
结果是
0
由于 () 运算符如此灵活，它可能很容易被用于许多不同的目的。然而，强烈不鼓励这样做，因为 () 符号并没有真正说明运算符正在做什么。在上面的例子中，最好将擦除功能写成一个名为 clear() 或 erase() 的函数，因为
matrix.erase()
比
matrix()
（它可以做任何事情！）更容易理解。
注意：从 C++23 开始，你可以使用带有多个索引的
operator[]
。这与上面
operator()
的工作方式类似。
函数对象（Functors）的乐趣
Operator() 也常被重载来实现
函数对象
（或
函数对象
），它们是像函数一样操作的类。函数对象优于普通函数的地方在于，函数对象可以将数据存储在成员变量中（因为它们是类）。
这是一个简单的函数对象
#include <iostream>

class Accumulator
{
private:
    int m_counter{ 0 };

public:
    int operator() (int i) { return (m_counter += i); }

    void reset() { m_counter = 0; } // optional 
};

int main()
{
    Accumulator acc{};
    std::cout << acc(1) << '\n'; // prints 1
    std::cout << acc(3) << '\n'; // prints 4

    Accumulator acc2{};
    std::cout << acc2(10) << '\n'; // prints 10
    std::cout << acc2(20) << '\n'; // prints 30
    
    return 0;
}
请注意，使用我们的 Accumulator 看起来就像进行正常的函数调用，但我们的 Accumulator 对象正在存储一个累积值。
函数对象的好处在于，我们可以根据需要实例化任意数量的独立函数对象，并同时使用它们。函数对象还可以有其他成员函数（例如
reset()
）来执行方便的操作。
总结
Operator() 有时会重载两个参数，用于索引多维数组，或检索一维数组的子集（其中两个参数定义要返回的子集）。其他任何情况最好写成成员函数，并带有更具描述性的名称。
Operator() 也常被重载以创建函数对象。尽管简单的函数对象（如上面的示例）很容易理解，但函数对象通常用于更高级的编程主题，并值得单独一课。
小测验时间
问题 #1
编写一个名为 MyString 的类，它包含一个
std::string
。重载
operator<<
以输出字符串。重载
operator()
以返回从第一个参数索引开始的子字符串（作为
MyString
）。子字符串的长度应由第二个参数定义。
以下代码应该运行
int main()
{
    MyString s { "Hello, world!" };
    std::cout << s(7, 5) << '\n'; // start at index 7 and return 5 characters

    return 0;
}
这应该打印
world
提示：你可以使用
std::string::substr
来获取
std::string
的子字符串。
显示答案
#include <cassert>
#include <iostream>
#include <string>
#include <string_view>

class MyString
{
private:
	std::string m_string{};

public:
	MyString(std::string_view string = {})
		:m_string{ string }
	{
	}

	MyString operator()(int start, int length)
	{
		assert(start >= 0);
		assert(start + length <= static_cast<int>(m_string.length()) && "MyString::operator(int, int): Substring is out of range");

		return MyString { m_string.substr(
			static_cast<std::string::size_type>(start),
			static_cast<std::string::size_type>(length)
			)};
	}

	friend std::ostream& operator<<(std::ostream& out, const MyString& s)
	{
		out << s.m_string;

		return out;
	}
};

int main()
{
	MyString s{ "Hello, world!" };
	std::cout << s(7, 5) << '\n'; // start at index 7 and return 5 characters

	return 0;
}
问题 #2
此测验题为额外加分题。
> 步骤 #1
如果我们不需要修改返回的子字符串，为什么上述方法效率低下？
显示答案
在我们的
operator()
内部，
std::string::substr
返回一个
std::string
，这意味着当我们调用它时，我们正在复制源字符串的一部分。我们重载的
operator()
使用它来构造一个新的
MyString
，其中包含一个
std::string
成员，这又会进行一次复制。然后我们将这个
MyString
返回给调用者，这会进行第三次复制。编译器可能会优化掉一些这些复制，但至少一个
std::string
（包含结果子字符串）必须保留。
我们只有在打算修改子字符串，或者子字符串的生命周期比原始字符串长的情况下才需要复制子字符串。通常情况并非如此，所以我们正在进行昂贵的复制，而这些复制通常是不需要的。
> 步骤 #2
我们还能做什么？
显示答案
std::string_view
能够查看现有字符串的子字符串而无需进行复制。如果我们的
operator()
返回一个
std::string_view
，那么调用者可以在足够的情况下使用
std::string_view
，或者在需要修改或持久化子字符串时将其转换为
std::string
或
MyString
。
> 步骤 #3
更新之前测验解决方案中的
operator()
，使其返回子字符串为
std::string_view
。
提示：
std::string::substr()
返回一个
std::string
。
std::string_view::substr()
返回一个
std::string_view
。务必小心不要返回一个悬空（dangling）的
std::string_view
！
显示提示
提示：不要创建任何
std::string
临时对象，因为它们会在函数结束时被销毁，任何查看这些
std::string
的
std::string_view
都将悬空。
显示提示
提示：创建
std::string_view
临时对象是允许的，只要它们是
m_string
的视图。
显示答案
#include <cassert>
#include <iostream>
#include <string>
#include <string_view>

class MyString
{
private:
	std::string m_string{};

public:
	MyString(std::string_view string = {})
		:m_string{ string }
	{
	}

	std::string_view operator()(int start, int length)
	{
		assert(start >= 0);
		assert(start + length <= static_cast<int>(m_string.length()) && "MyString::operator(int, int): Substring is out of range");

		// Create a std::string_view of m_string, so we can use std::string_view::substr() instead of std::string::substr()
		return std::string_view{ m_string }.substr(
			static_cast<std::string_view::size_type>(start),
			static_cast<std::string_view::size_type>(length)
		);
	}

	friend std::ostream& operator<<(std::ostream& out, const MyString& s)
	{
		out << s.m_string;

		return out;
	}
};

int main()
{
	MyString s{ "Hello, world!" };
	std::cout << s(7, 5) << '\n'; // start at index 7 and return 5 characters

	return 0;
}
让我们进一步探讨
return std::string_view{ m_string }.substr();
。首先，我们正在创建
m_string
的临时
std::string_view
，这开销很小，并允许我们访问
std::string_view
成员函数。接下来，我们在这个临时对象上调用
std::string_view::substr
来获取我们的子字符串（作为
m_string
的非空终止视图）。然后我们将此视图返回给调用者。由于我们返回给调用者的
std::string_view
仍然是
m_string
的视图（它仍在作用域内），所以我们返回的
std::string_view
不会悬空。
最终结果是我们创建了 3 个
std::string_view
而不是 3 个
std::string
，这更高效。
下一课
21.11
重载类型转换运算符
返回目录
上一课
21.9
重载下标运算符