# 21.9 — 重载下标运算符

21.9 — 重载下标运算符
Alex
2007 年 10 月 19 日，太平洋夏令时上午 9:50
2025 年 2 月 2 日
在使用数组时，我们通常使用下标运算符（[]）来索引数组的特定元素
myArray[0] = 7; // put the value 7 in the first element of the array
然而，考虑以下 `IntList` 类，它有一个成员变量是一个数组
class IntList
{
private:
    int m_list[10]{};
};

int main()
{
    IntList list{};
    // how do we access elements from m_list?
    return 0;
}
由于 `m_list` 成员变量是私有的，我们无法直接从 `list` 变量访问它。这意味着我们无法直接获取或设置 `m_list` 数组中的值。那么我们如何将元素放入或取出我们的列表呢？
如果不进行运算符重载，典型的方法是创建访问函数
class IntList
{
private:
    int m_list[10]{};

public:
    void setItem(int index, int value) { m_list[index] = value; }
    int getItem(int index) const { return m_list[index]; }
};
虽然这行得通，但它不是特别用户友好。考虑以下示例
int main()
{
    IntList list{};
    list.setItem(2, 3);

    return 0;
}
我们是将元素 2 设置为值 3，还是将元素 3 设置为值 2？如果没有看到 `setItem()` 的定义，这根本不清楚。
您也可以直接返回整个列表并使用 `operator[]` 访问元素
class IntList
{
private:
    int m_list[10]{};

public:
    int* getList() { return m_list; }
};
虽然这也能工作，但语法上有些奇怪
int main()
{
    IntList list{};
    list.getList()[2] = 3;

    return 0;
}
重载 `operator[]`
然而，在这种情况下，更好的解决方案是重载下标运算符（[]）以允许访问 `m_list` 的元素。下标运算符是必须作为成员函数重载的运算符之一。重载的 `operator[]` 函数总是接受一个参数：用户放在方括号之间的下标。在我们的 `IntList` 案例中，我们期望用户传入一个整数索引，我们将返回一个整数值作为结果。
#include <iostream>

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        return m_list[index];
    }
};

/*
// Can also be implemented outside the class definition
int& IntList::operator[] (int index)
{
    return m_list[index];
}
*/

int main()
{
    IntList list{};
    list[2] = 3; // set a value
    std::cout << list[2] << '\n'; // get a value

    return 0;
}
现在，每当我们在类的对象上使用下标运算符（[]）时，编译器将从 `m_list` 成员变量返回相应的元素！这允许我们直接获取和设置 `m_list` 的值。
这在语法上和理解上都很容易。当 `list[2]` 求值时，编译器首先检查是否存在重载的 `operator[]` 函数。如果存在，它会将方括号内的值（在本例中为 2）作为参数传递给该函数。
请注意，尽管您可以为函数参数提供默认值，但实际上不带下标使用 `operator[]` 不被认为是有效的语法，所以这样做没有意义。
提示
C++23 增加了对重载带多个下标的 `operator[]` 的支持。
为什么 `operator[]` 返回引用
让我们仔细看看 `list[2] = 3` 是如何求值的。因为下标运算符的优先级高于赋值运算符，所以 `list[2]` 首先求值。`list[2]` 调用 `operator[]`，我们已将其定义为返回 `list.m_list[2]` 的引用。由于 `operator[]` 返回引用，它返回实际的 `list.m_list[2]` 数组元素。我们部分求值的表达式变为 `list.m_list[2] = 3`，这是一个简单的整数赋值。
在第
12.2 课 -- 值类别（左值和右值）
中，您了解到赋值语句左侧的任何值都必须是左值（即具有实际内存地址的变量）。由于 `operator[]` 的结果可以在赋值的左侧使用（例如 `list[2] = 3`），因此 `operator[]` 的返回值必须是左值。事实证明，引用总是左值，因为您只能引用具有内存地址的变量。因此，通过返回引用，编译器认为我们正在返回一个左值。
考虑如果 `operator[]` 返回一个整数值而不是引用会发生什么。`list[2]` 会调用 `operator[]`，它会返回 `list.m_list[2]` 的
值
。例如，如果 `m_list[2]` 的值为 6，`operator[]` 将返回值 6。`list[2] = 3` 将部分求值为 `6 = 3`，这毫无意义！如果您尝试这样做，C++ 编译器会报错
C:VCProjectsTest.cpp(386) : error C2106: '=' : left operand must be l-value
用于 const 对象的重载 `operator[]`
在上面的 `IntList` 示例中，`operator[]` 是非 const 的，我们可以将其用作左值来改变非 const 对象的 상태。但是，如果我们的 `IntList` 对象是 const 的怎么办？在这种情况下，我们将无法调用 `operator[]` 的非 const 版本，因为那会允许我们潜在地改变 const 对象的 상태。
好消息是我们可以分别定义 `operator[]` 的非 const 和 const 版本。非 const 版本将用于非 const 对象，而 const 版本将用于 const 对象。
#include <iostream>

class IntList
{
private:
    int m_list[10]{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }; // give this class some initial state for this example

public:
    // For non-const objects: can be used for assignment
    int& operator[] (int index)
    {
        return m_list[index];
    }

    // For const objects: can only be used for access
    // This function could also return by value if the type is cheap to copy
    const int& operator[] (int index) const
    {
        return m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // okay: calls non-const version of operator[]
    std::cout << list[2] << '\n';

    const IntList clist{};
    // clist[2] = 3; // compile error: clist[2] returns const reference, which we can't assign to
    std::cout << clist[2] << '\n';

    return 0;
}
删除 const 和非 const 重载之间的重复代码
在上面的示例中，请注意 `int& IntList::operator[](int)` 和 `const int& IntList::operator[](int) const` 的实现是相同的。唯一的区别是函数的返回类型。
在实现微不足道（例如，一行）的情况下，两个函数使用相同的实现是可以的（并且是首选）。这种引入的少量冗余不值得删除。
但是，如果这些运算符的实现很复杂，需要许多语句怎么办？例如，也许验证索引是否有效很重要，这需要向每个函数添加许多冗余代码行。
在这种情况下，由于许多重复语句而引入的冗余更成问题，并且希望有一个可以用于两个重载的单一实现。但如何实现呢？通常我们只会用一个函数来实现在另一个函数的基础上（例如，让一个函数调用另一个函数）。但在这种情况下有点棘手。函数的 const 版本不能调用函数的非 const 版本，因为那将需要丢弃 const 对象的 const。虽然函数的非 const 版本可以调用函数的 const 版本，但函数的 const 版本返回一个 const 引用，而我们需要返回一个非 const 引用。幸运的是，有一种方法可以解决这个问题。
首选的解决方案如下
实现函数的 const 版本的逻辑。
让非 const 函数调用 const 函数，并使用 `const_cast` 删除 const。
最终的解决方案看起来像这样
#include <iostream>
#include <utility> // for std::as_const

class IntList
{
private:
    int m_list[10]{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }; // give this class some initial state for this example

public:
    int& operator[] (int index)
    {
        // use std::as_const to get a const version of `this` (as a reference) 
        // so we can call the const version of operator[]
        // then const_cast to discard the const on the returned reference
        return const_cast<int&>(std::as_const(*this)[index]);
    }

    const int& operator[] (int index) const
    {
        return m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // okay: calls non-const version of operator[]
    std::cout << list[2] << '\n';

    const IntList clist{};
    // clist[2] = 3; // compile error: clist[2] returns const reference, which we can't assign to
    std::cout << clist[2] << '\n';

    return 0;
}
通常使用 `const_cast` 删除 const 是我们希望避免的事情，但在这种情况下是可以接受的。如果调用了非 const 重载，那么我们知道我们正在处理一个非 const 对象。删除指向非 const 对象的 const 引用上的 const 是可以的。
致进阶读者
在 C++23 中，我们可以通过利用本教程系列中尚未介绍的几个特性做得更好
#include <iostream>

class IntList
{
private:
    int m_list[10]{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }; // give this class some initial state for this example

public:
    // Use an explicit object parameter (self) and auto&& to differentiate const vs non-const
    auto&& operator[](this auto&& self, int index)
    {
        // Complex code goes here
        return self.m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // okay: calls non-const version of operator[]
    std::cout << list[2] << '\n';

    const IntList clist{};
    // clist[2] = 3; // compile error: clist[2] returns const reference, which we can't assign to
    std::cout << clist[2] << '\n';

    return 0;
}
检测索引有效性
重载下标运算符的另一个优点是我们可以使其比直接访问数组更安全。通常，当访问数组时，下标运算符不检查索引是否有效。例如，编译器不会抱怨以下代码
int list[5]{};
list[7] = 3; // index 7 is out of bounds!
但是，如果我们知道数组的大小，我们可以让我们的重载下标运算符检查以确保索引在边界内
#include <cassert> // for assert()
#include <iterator> // for std::size()

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        assert(index >= 0 && static_cast<std::size_t>(index) < std::size(m_list));

        return m_list[index];
    }
};
在上面的示例中，我们使用了 `assert()` 函数（包含在 `cassert` 头文件中）来确保我们的索引是有效的。如果 `assert` 内部的表达式评估为 false（这意味着用户传入了无效索引），程序将以错误消息终止，这比替代方案（损坏内存）要好得多。这可能是进行此类错误检查最常用的方法。
如果您不想使用断言（它将在非调试版本中被编译掉），您可以改用 if 语句和您喜欢的错误处理方法（例如，抛出异常、调用 `std::exit` 等）
#include <iterator> // for std::size()

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        if (!(index >= 0 && static_cast<std::size_t>(index) < std::size(m_list))
        {
            // handle invalid index here
        }

        return m_list[index];
    }
};
指向对象的指针和重载的 `operator[]` 不兼容
如果您尝试在指向对象的指针上调用 `operator[]`，C++ 会假定您正在尝试索引该类型对象的数组。
考虑以下示例
#include <cassert> // for assert()
#include <iterator> // for std::size()

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        return m_list[index];
    }
};

int main()
{
    IntList* list{ new IntList{} };
    list [2] = 3; // error: this will assume we're accessing index 2 of an array of IntLists
    delete list;

    return 0;
}
因为我们不能将整数赋值给 `IntList`，所以这不会编译。但是，如果赋值整数是有效的，这将编译并运行，但结果未定义。
规则
确保您没有尝试在指向对象的指针上调用重载的 `operator[]`。
正确的语法是首先解引用指针（确保使用括号，因为 `operator[]` 的优先级高于 `operator*`），然后调用 `operator[]`
int main()
{
    IntList* list{ new IntList{} };
    (*list)[2] = 3; // get our IntList object, then call overloaded operator[]
    delete list;

    return 0;
}
这既丑陋又容易出错。更好的是，如果没有必要，就不要设置指向您对象的指针。
函数参数不必是整数类型
如上所述，C++ 将用户在方括号之间输入的内容作为参数传递给重载函数。在大多数情况下，这将是一个整数值。然而，这不是必需的——事实上，您可以定义您的重载 `operator[]` 接受您想要的任何类型的值。您可以定义您的重载 `operator[]` 接受双精度浮点数、`std::string` 或其他任何您喜欢的值。
作为一个荒谬的例子，只是为了让您看到它的作用
#include <iostream>
#include <string_view> // C++17

class Stupid
{
private:

public:
	void operator[] (std::string_view index);
};

// It doesn't make sense to overload operator[] to print something
// but it is the easiest way to show that the function parameter can be a non-integer
void Stupid::operator[] (std::string_view index)
{
	std::cout << index;
}

int main()
{
	Stupid stupid{};
	stupid["Hello, world!"];

	return 0;
}
正如您所期望的，这将打印
Hello, world!
在编写某些类型的类时，重载 `operator[]` 以接受 `std::string` 参数可能很有用，例如那些使用单词作为索引的类。
小测验时间
问题 #1
映射是一种将元素存储为键值对的类。键必须是唯一的，并用于访问关联的对。在这个测验中，我们将编写一个应用程序，允许我们使用一个简单的映射类按名称给学生分配成绩。学生姓名将是键，成绩（作为 char）将是值。
a) 首先，编写一个名为 `StudentGrade` 的结构体，其中包含学生的姓名（作为 `std::string`）和成绩（作为 `char`）。
显示答案
#include <string>

struct StudentGrade
{
    std::string name{};
    char grade{};
};
b) 添加一个名为 `GradeMap` 的类，其中包含一个名为 `m_map` 的 `StudentGrade` 类型的 `std::vector`。
显示答案
#include <string>
#include <vector>

struct StudentGrade
{
	std::string name{};
	char grade{};
};

class GradeMap
{
private:
	std::vector<StudentGrade> m_map{};
};
c) 为此类别编写一个重载的 `operator[]`。此函数应接受一个 `std::string` 参数，并返回一个 `char` 的引用。在函数体中，首先查看学生姓名是否已存在（您可以使用 `
` 中的 `std::find_if`）。如果学生存在，则返回成绩的引用，您就完成了。否则，使用 `std::vector::emplace_back()` 或 `std::vector::push_back()` 函数为此新学生添加一个 `StudentGrade`。当您这样做时，`std::vector` 会将 `StudentGrade` 的副本添加到自身（如果需要会调整大小，使所有先前返回的引用无效）。最后，我们需要返回我们刚刚添加到 `std::vector` 中的学生的成绩的引用。我们可以使用 `std::vector::back()` 函数访问我们刚刚添加的学生。
以下程序应该运行
#include <iostream>

// ...

int main()
{
	GradeMap grades{};

	grades["Joe"] = 'A';
	grades["Frank"] = 'B';

	std::cout << "Joe has a grade of " << grades["Joe"] << '\n';
	std::cout << "Frank has a grade of " << grades["Frank"] << '\n';

	return 0;
}
显示答案
#include <algorithm>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

struct StudentGrade
{
	std::string name{};
	char grade{};
};

class GradeMap
{
private:
	std::vector<StudentGrade> m_map{};

public:
	char& operator[](std::string_view name);
};

char& GradeMap::operator[](std::string_view name)
{
	auto found{ std::find_if(m_map.begin(), m_map.end(),
				[name](const auto& student) { // this is a lambda that captures name from the surrounding scope
					return (student.name == name); // so we can use name here
				}) };

	if (found != m_map.end())
	{
		return found->grade;
	}

	// otherwise create a new StudentGrade for this student and add
	// it to the end of our vector.  Then return the grade.

	// emplace_back version (C++20 onward)
	// StudentGrade is an aggregate and emplace_back only works with aggregates as of C++20
	return m_map.emplace_back(std::string{name}).grade;

	// push_back version (C++17 or older)
	// m_map.push_back(StudentGrade{std::string{name}});
	// return m_map.back().grade;
}

int main()
{
	GradeMap grades{};

	grades["Joe"] = 'A';
	grades["Frank"] = 'B';

	std::cout << "Joe has a grade of " << grades["Joe"] << '\n';
	std::cout << "Frank has a grade of " << grades["Frank"] << '\n';

	return 0;
}
提醒
有关 lambda 表达式的更多信息，请参阅
20.6 -- lambda 表达式（匿名函数）简介
。
提示
由于映射很常见，标准库提供了
`std::map`
，目前 learncpp 尚未涵盖。使用 `std::map`，我们可以将代码简化为
#include <iostream>
#include <map> // std::map
#include <string>

int main()
{
	// std::map can be initialized
	std::map<std::string, char> grades{
		{ "Joe", 'A' },
		{ "Frank", 'B' }
	};

	// and assigned
	grades["Susan"] = 'C';
	grades["Tom"] = 'D';

	std::cout << "Joe has a grade of " << grades["Joe"] << '\n';
	std::cout << "Frank has a grade of " << grades["Frank"] << '\n';

	return 0;
}
优先使用 `std::map` 而不是自己实现。
问题 #2
额外加分 #1: 我们编写的 `GradeMap` 类和示例程序由于多种原因效率低下。描述一种可以改进 `GradeMap` 类的方法。
显示答案
`std::vector` 本质上是未排序的。这意味着每次我们调用 `operator[]` 时，我们都可能遍历整个 `std::vector` 来查找我们的元素。对于少量元素来说，这不是问题，但是随着我们不断添加名称，这将变得越来越慢。我们可以通过保持 `m_map` 有序并使用二分查找来优化这一点，从而最大限度地减少我们需要查找的元素数量，以找到我们感兴趣的元素。
问题 #3
额外加分 #2：为什么这个程序可能无法按预期工作？
#include <iostream>

int main()
{
	GradeMap grades{};

	char& gradeJoe{ grades["Joe"] }; // does an emplace_back
	gradeJoe = 'A';

	char& gradeFrank{ grades["Frank"] }; // does a emplace_back
	gradeFrank = 'B';

	std::cout << "Joe has a grade of " << gradeJoe << '\n';
	std::cout << "Frank has a grade of " << gradeFrank << '\n';

	return 0;
}
显示答案
当添加 Frank 时，`std::vector` 可能需要增长以容纳它。这需要动态分配一个新的内存块，将数组中的元素复制到该新块，并删除旧块。当这种情况发生时，任何指向 `std::vector` 中现有元素的引用都会失效（这意味着它们作为悬空引用指向已删除的内存）。
换句话说，在我们 `emplace_back("Frank")` 之后，如果 `std::vector` 必须增长以容纳 Frank，那么 `gradeJoe` 引用将失效。然后访问 `gradeJoe` 打印 Joe 的成绩将导致未定义的结果。
`std::vector` 如何增长是编译器特定的细节，因此我们可以预期上面的程序在某些编译器下可以正常工作，而在其他编译器下则不能。
下一课
21.10
重载圆括号运算符
返回目录
上一课
21.8
重载递增和递减运算符