# 16.6 — 数组与循环

16.6 — 数组与循环
Alex
2007 年 7 月 2 日 下午 2:03（太平洋夏令时）
2024 年 12 月 14 日
在本章的介绍性课程（
16.1 -- 容器和数组简介
）中，我们介绍了当有许多相关的独立变量时出现的可伸缩性挑战。在本课程中，我们将重新介绍这个问题，然后讨论数组如何帮助我们优雅地解决这些问题。
变量可伸缩性挑战，再探
考虑我们要计算一个班级学生的平均考试分数的情况。为了使这些示例简洁，我们假设班级只有 5 名学生。
下面是我们如何使用独立变量来解决这个问题
#include <iostream>

int main()
{
    // allocate 5 integer variables (each with a different name)
    int testScore1{ 84 };
    int testScore2{ 92 };
    int testScore3{ 76 };
    int testScore4{ 81 };
    int testScore5{ 56 };

    int average { (testScore1 + testScore2 + testScore3 + testScore4 + testScore5) / 5 };

    std::cout << "The class average is: " << average << '\n';

    return 0;
}
这需要大量的变量和大量的输入。想象一下，如果我们要处理 30 名学生或 600 名学生，那将需要多少工作量。此外，如果添加新的考试分数，则必须声明、初始化新变量，并将其添加到平均值计算中。你还记得更新除数吗？如果你忘记了，你现在就有了一个语义错误。任何时候你不得不修改现有代码，你都会面临引入错误的风险。
到目前为止，你已经知道当我们有一堆相关变量时，我们应该使用数组。所以让我们用
std::vector
替换我们的独立变量
#include <iostream>
#include <vector>

int main()
{
    std::vector testScore { 84, 92, 76, 81, 56 };
    std::size_t length { testScore.size() };
    
    int average { (testScore[0] + testScore[1] + testScore[2] + testScore[3] + testScore[4])
        / static_cast<int>(length) };

    std::cout << "The class average is: " << average << '\n';

    return 0;
}
这更好——我们显著减少了定义的变量数量，并且平均值计算的除数现在直接由数组的长度决定。
但是平均值计算仍然是一个问题，因为我们必须手动单独列出每个元素。而且由于我们必须显式列出每个元素，我们的平均值计算只适用于元素数量与我们列出的元素数量完全相同的数组。如果我们也想对其他长度的数组进行平均，我们将需要为每个不同的数组长度编写新的平均值计算。
我们真正需要的是一种无需显式列出每个元素即可访问每个数组元素的方法。
数组与循环
在之前的课程中，我们注意到数组下标不需要是常量表达式——它们可以是运行时表达式。这意味着我们可以使用变量的值作为索引。
另请注意，上一个示例的平均值计算中使用的数组索引是升序序列：0、1、2、3、4。因此，如果我们有办法将变量按顺序设置为值 0、1、2、3 和 4，那么我们就可以直接使用该变量作为我们的数组索引，而不是字面值。我们已经知道如何做到这一点——使用 for 循环。
相关内容
我们在课程
8.10 -- For 语句
中介绍了 for 循环。
让我们使用 for 循环重写上面的示例，其中循环变量用作数组索引
#include <iostream>
#include <vector>

int main()
{
    std::vector testScore { 84, 92, 76, 81, 56 };
    std::size_t length { testScore.size() };

    int average { 0 };
    for (std::size_t index{ 0 }; index < length; ++index) // index from 0 to length-1
        average += testScore[index];                      // add the value of element with index `index`
    average /= static_cast<int>(length);                  // calculate the average

    std::cout << "The class average is: " << average << '\n';

    return 0;
}
这应该很简单。
index
从
0
开始，
testScore[0]
加到
average
，
index
递增到
1
。
testScore[1]
加到
average
，
index
递增到
2
。最终，当
index
递增到
5
时，
index < length
为假，循环终止。
此时，循环已将
testScore[0]
、
testScore[1]
、
testScore[2]
、
testScore[3]
和
testScore[4]
的值加到
average
中。
最后，我们通过将累积值除以数组长度来计算平均值。
这个解决方案在可维护性方面是理想的。循环迭代的次数由数组的长度决定，循环变量用于所有数组索引。我们不再需要手动列出每个数组元素。
如果我们要添加或删除考试分数，我们只需修改数组初始化器的数量，其余代码将无需进一步更改即可工作！
以某种顺序访问容器的每个元素称为
遍历
或
遍历
容器。遍历通常称为
迭代
或
迭代遍历
或
迭代通过
容器。
作者注
由于容器类使用类型
size_t
表示长度和索引，因此在本课程中，我们将遵循相同做法。我们将在即将到来的课程
16.7 -- 数组、循环和符号挑战解决方案
中讨论使用有符号长度和索引。
模板、数组和循环解锁可伸缩性
数组提供了一种存储多个对象而无需命名每个元素的方法。
循环提供了一种遍历数组而无需显式列出每个元素的方法。
模板提供了一种参数化元素类型的方法。
模板、数组和循环共同使我们能够编写可以对元素容器进行操作的代码，无论元素类型或容器中的元素数量如何！
为了进一步说明这一点，让我们重写上面的示例，将平均值计算重构为函数模板
#include <iostream>
#include <vector>

// Function template to calculate the average of the values in a std::vector
template <typename T>
T calculateAverage(const std::vector<T>& arr)
{
    std::size_t length { arr.size() };
    
    T average { 0 };                                      // if our array has elements of type T, our average should have type T too
    for (std::size_t index{ 0 }; index < length; ++index) // iterate through all the elements
        average += arr[index];                            // sum up all the elements
    average /= static_cast<int>(length);                  // divide by count of items (integral in nature)
    
    return average;
}

int main()
{
    std::vector class1 { 84, 92, 76, 81, 56 };
    std::cout << "The class 1 average is: " << calculateAverage(class1) << '\n'; // calc average of 5 ints

    std::vector class2 { 93.2, 88.6, 64.2, 81.0 };
    std::cout << "The class 2 average is: " << calculateAverage(class2) << '\n'; // calc average of 4 doubles
    
    return 0;
}
这会打印
The class 1 average is: 77
The class 2 average is: 81.75
在上面的示例中，我们创建了函数模板
calculateAverage()
，它接受任何元素类型和任何长度的
std::vector
，并返回平均值。在
main()
中，我们演示了此函数在调用包含 5 个
int
元素的数组或 4 个
double
元素的数组时同样有效！
calculateAverage()
将适用于支持函数内部使用的运算符 (
operator+=(T)
,
operator/=(int)
) 的任何类型
T
。如果你尝试使用不支持这些运算符的
T
，编译器将在尝试编译实例化函数模板时出错。
你可能想知道为什么我们将
length
转换为
int
而不是
T
。当我们计算平均值时，我们将总和除以项目计数。项目计数是整数值。因此，从语义上讲，除以
int
更合理。
我们可以用数组和循环做什么
现在我们知道如何使用循环遍历元素容器，让我们看看我们可以将容器遍历用于的最常见的事情。我们通常遍历容器以执行四种操作之一
根据现有元素的值计算新值（例如平均值、值的总和）。
搜索现有元素（例如精确匹配、匹配计数、查找最大值）。
对每个元素进行操作（例如输出每个元素、将所有元素乘以 2）。
重新排序元素（例如按升序对元素进行排序）。
前三项相当简单。我们可以使用单个循环遍历数组，并酌情检查或修改每个元素。
重新排序容器的元素要复杂得多，因为这样做通常涉及在一个循环中使用另一个循环。虽然我们可以手动完成，但通常最好使用标准库中的现有算法来完成。我们将在未来的章节中详细介绍这一点，届时我们将讨论算法。
数组和差一错误
当使用索引遍历容器时，你必须注意确保循环执行适当的次数。差一错误（循环体执行次数过多或过少）很容易发生。
通常，当使用索引遍历容器时，我们将索引从
0
开始，并循环直到
index < length
。
新程序员有时会不小心使用
index <= length
作为循环条件。这将导致循环在
index == length
时执行，从而导致下标越界和未定义行为。
小测验时间
问题 #1
编写一个短程序，使用循环将以下向量的元素打印到屏幕上
#include <iostream>
#include <vector>

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    // Add your code here

    return 0;
}
输出应如下所示
4 6 7 3 8 2 1 9
显示答案
#include <iostream>
#include <vector>

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    for (std::size_t index{ 0 }; index < arr.size(); ++index)
    {
        std::cout << arr[index] << ' ';
    }

    if (arr.size() > 0)
        std::cout << '\n';

    return 0;
}
问题 #2
更新你之前测验解决方案的代码，以便以下程序能够编译并具有相同的输出
#include <iostream>
#include <vector>

// Implement printArray() here

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printArray(arr); // use function template to print array

    return 0;
}
显示答案
#include <iostream>
#include <vector>

template <typename T>
void printArray(const std::vector<T>& arr)
{
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
    {
        std::cout << arr[index] << ' ';
    }

    if (arr.size() > 0)
        std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printArray(arr);

    return 0;
}
问题 #3
给定测验 2 的解决方案，执行以下操作
向用户询问一个介于 1 到 9 之间的值。如果用户未输入 1 到 9 之间的值，则重复询问整数值，直到他们输入。如果用户输入数字后有多余的输入，则忽略多余的输入。
打印数组。
编写一个函数模板来搜索数组中用户输入的值。如果该值在数组中，则返回该元素的索引。如果该值不在数组中，则返回适当的值。
如果找到该值，则打印值和索引。如果未找到该值，则打印值并指示未找到。
我们在课程
9.5 -- std::cin 和处理无效输入
中介绍了如何处理无效输入。
以下是该程序的两次示例运行
Enter a number between 1 and 9: d
Enter a number between 1 and 9: 6
4 6 7 3 8 2 1 9
The number 6 has index 1
Enter a number between 1 and 9: 5
4 6 7 3 8 2 1 9
The number 5 was not found
显示答案
#include <iostream>
#include <limits>
#include <vector>

template <typename T>
void printArray(const std::vector<T>& arr)
{
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
    {
        std::cout << arr[index] << ' ';
    }
   
    if (arr.size() > 0)
        std::cout << '\n';
}

template <typename T>
int findIndex(const std::vector<T>& arr, T val)
{
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
    {
        if (arr[index] == val)
            return static_cast<int>(index);
    }    

    return -1; // -1 is not a valid index, so we can use it as an error return value
}


int getValidNumber()
{
    // First, read in valid input from user
    int num {};
    do
    {
        std::cout << "Enter a number between 1 and 9: ";
        std::cin >> num;

        // if the user entered an invalid character
        if (!std::cin)
            std::cin.clear(); // reset any error flags

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // ignore any extra characters in the input buffer (regardless of whether we had an error or not)

    } while (num < 1 || num > 9);

    return num;
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    int num { getValidNumber() };
    
    printArray(arr);

    int index { findIndex(arr, num) };

    if (index != -1)
        std::cout << "The number " << num << " has index " << index << '\n';
    else
        std::cout << "The number " << num << " was not found\n";

    return 0;
}
问题 #4
额外加分：修改前面的程序，使其能够处理包含非整数数值的
std::vector
，例如
std::vector arr{ 4.4, 6.6, 7.7, 3.3, 8.8, 2.2, 1.1, 9.9 };
。
显示答案
#include <iostream>
#include <limits>
#include <vector>

template <typename T>
void printArray(const std::vector<T>& arr)
{
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
    {
        std::cout << arr[index] << ' ';
    }

    if (arr.size() > 0)
        std::cout << '\n';
}

template <typename T>
int findIndex(const std::vector<T>& arr, T val)
{
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
    {
        if (arr[index] == val)
            return static_cast<int>(index);
    }

    return -1; // -1 is not a valid index, so we can use it as an error return value
}

// Passing in low and high allows the compiler to infer the type of the input we want
template <typename T>
T getValidNumber(std::string_view prompt, T low, T high)
{
    // First, read in valid input from user
    T val {};
    do
    {
        std::cout << prompt;
        std::cin >> val;

        // if the user entered an invalid character
        if (!std::cin)
            std::cin.clear(); // reset any error flags

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // ignore any extra characters in the input buffer (regardless of whether we had an error or not)

    } while (val < low || val > high);

    return val;
}

int main()
{
    std::vector arr{ 4.4, 6.6, 7.7, 3.3, 8.8, 2.2, 1.1, 9.9 };
    
    auto num { getValidNumber("Enter a number between 1 and 9: ", 1.0, 9.0) };

    printArray(arr);

    int index { findIndex(arr, num) };

    if (index != -1)
        std::cout << "The number " << num << " has index " << index << '\n';
    else
        std::cout << "The number " << num << " was not found\n";

    return 0;
}
问题 #5
编写一个函数模板以在
std::vector
中查找最大值。如果向量为空，则返回元素类型的默认值。
以下代码应该执行
int main()
{
    std::vector data1 { 84, 92, 76, 81, 56 };
    std::cout << findMax(data1) << '\n';

    std::vector data2 { -13.0, -26.7, -105.5, -14.8 };
    std::cout << findMax(data2) << '\n';

    std::vector<int> data3 { };
    std::cout << findMax(data3) << '\n';
    
    return 0;
}
并打印以下结果
92
-13
0
显示提示
提示：使用非循环变量来跟踪你目前看到的最高值。
显示答案
#include <iostream>
#include <vector>

template <typename T>
T findMax(const std::vector<T>& arr)
{
    std::size_t length { arr.size() };

    if (length==0)
        return T{};    

    T max { arr[0] }; // Set the max seen to the first element

    // Iterate through any remaining elements looking for a larger value
    for (std::size_t index{ 1 }; index < length; ++index)
    {
        if (arr[index] > max)
            max = arr[index];
    }

    return max;
}

int main()
{
    std::vector data1 { 84, 92, 76, 81, 56 };
    std::cout << findMax(data1) << '\n';

    std::vector data2 { -13.0, -26.7, -105.5, -14.8 };
    std::cout << findMax(data2) << '\n';

    std::vector<int> data3 { };
    std::cout << findMax(data3) << '\n';
    
    return 0;
}
在这个示例中，我们使用一个名为
max
的非循环变量来跟踪我们见过的最高分数。我们用第一个元素的值初始化
max
，使其以合法值开始。值初始化可能很诱人，但如果数组只包含负值，则会导致函数返回错误的值。
然后我们遍历数组的每个元素，如果找到比我们之前见过的任何分数都高的分数，我们就将
max
设置为该值。因此，
max
始终代表我们迄今为止搜索过的所有元素中的最高分数。当我们到达数组末尾时，
max
保存着整个数组中的最高分数，然后我们可以将其返回给调用者。
问题 #6
在课程
8.10 -- For 语句
的测验中，我们为数字三、五和七实现了一个名为 FizzBuzz 的游戏。
在此测验中，按以下方式实现游戏
只能被 3 整除的数字应打印“fizz”。
只能被 5 整除的数字应打印“buzz”。
只能被 7 整除的数字应打印“pop”。
只能被 11 整除的数字应打印“bang”。
只能被 13 整除的数字应打印“jazz”。
只能被 17 整除的数字应打印“pow”。
只能被 19 整除的数字应打印“boom”。
能被上述多个数字整除的数字应打印与其除数相关的每个单词。
不能被上述任何数字整除的数字应只打印数字。
使用
std::vector
来保存除数，另一个
std::vector
来保存单词（作为
std::string_view
类型）。如果数组长度不同，程序应断言。为 150 个数字生成输出。
显示提示
提示：使用
sv
字面量后缀使单词类型为
std::string_view
，这样你就可以使用 CTAD 来推断数组的类型。
显示提示
提示：使用嵌套的 for 循环来检查数字与除数。我们在课程
8.10 -- For 语句
中讨论嵌套的 for 循环。
这是前 21 次迭代的预期输出
1
2
fizz
4
buzz
fizz
pop
8
fizz
buzz
bang
fizz
jazz
pop
fizzbuzz
16
pow
fizz
boom
buzz
fizzpop
显示答案
// h/t to reader Waldo for suggesting this quiz
#include <cassert>
#include <iostream>
#include <string_view>
#include <vector>

void fizzbuzz(int count)
{
	// We'll make these static so we only have to do initialization once
	static const std::vector divisors                { 3, 5, 7, 11, 13, 17, 19 };
	static const std::vector<std::string_view> words { "fizz", "buzz", "pop", "bang", "jazz", "pow", "boom" };
	assert(std::size(divisors) == std::size(words) && "fizzbuzz: array sizes don't match");

	// Loop through each number between 1 and count (inclusive)
	for (int i{ 1 }; i <= count; ++i)
	{
		bool printed{ false };

		// Check the current number against each possible divisor
		for (std::size_t j{ 0 }; j < divisors.size(); ++j)
		{
			if (i % divisors[j] == 0)
			{
				std::cout << words[j];
				printed = true;
			}
		}

		// If there were no divisors
		if (!printed)
			std::cout << i;

		std::cout << '\n';
	}
}

int main()
{
	fizzbuzz(150);

	return 0;
}
提示
因为
divisors
和
words
是常量数组，所以最好将它们设置为
constexpr
——但我们不能对
std::vector
这样做。在这里最好使用
constexpr std::array
。我们在课程
17.1 -- std::array 简介
中介绍了
std::array
。
下一课
16.7
数组、循环和符号挑战解决方案
返回目录
上一课
16.5
返回 std::vector，以及移动语义简介