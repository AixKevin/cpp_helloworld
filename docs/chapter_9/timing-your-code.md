# 18.4 — 代码计时

18.4 — 代码计时
Alex
2018年1月4日，太平洋标准时间下午3:10
2023年10月31日
在编写代码时，有时您会遇到不确定哪种方法性能更好的情况。那么如何判断呢？
一个简单的方法是计时您的代码，看看它运行了多长时间。C++11 在 chrono 库中提供了一些功能来做到这一点。然而，使用 chrono 库有点神秘。好消息是我们可以轻松地将所需的所有计时功能封装到一个类中，然后我们可以在自己的程序中使用它。
这就是这个类
#include <chrono> // for std::chrono functions

class Timer
{
private:
	// Type aliases to make accessing nested type easier
	using Clock = std::chrono::steady_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;
	
	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}
	
	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};
就是这样！要使用它，我们在 main 函数的顶部（或我们想开始计时的地方）实例化一个 Timer 对象，然后当我们想知道程序运行到该点需要多长时间时，调用 elapsed() 成员函数。
#include <iostream>

int main()
{
    Timer t;

    // Code to time goes here

    std::cout << "Time elapsed: " << t.elapsed() << " seconds\n";

    return 0;
}
现在，让我们在一个实际的例子中使用它，我们对一个包含 10000 个元素的数组进行排序。首先，让我们使用我们在前一章中开发的插入排序算法
#include <array>
#include <chrono> // for std::chrono functions
#include <cstddef> // for std::size_t
#include <iostream>
#include <numeric> // for std::iota

const int g_arrayElements { 10000 };

class Timer
{
private:
    // Type aliases to make accessing nested type easier
    using Clock = std::chrono::steady_clock;
    using Second = std::chrono::duration<double, std::ratio<1> >;

    std::chrono::time_point<Clock> m_beg{ Clock::now() };

public:

    void reset()
    {
        m_beg = Clock::now();
    }

    double elapsed() const
    {
        return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
    }
};

void sortArray(std::array<int, g_arrayElements>& array)
{

    // Step through each element of the array
    // (except the last one, which will already be sorted by the time we get there)
    for (std::size_t startIndex{ 0 }; startIndex < (g_arrayElements - 1); ++startIndex)
    {
        // smallestIndex is the index of the smallest element we’ve encountered this iteration
        // Start by assuming the smallest element is the first element of this iteration
        std::size_t smallestIndex{ startIndex };

        // Then look for a smaller element in the rest of the array
        for (std::size_t currentIndex{ startIndex + 1 }; currentIndex < g_arrayElements; ++currentIndex)
        {
            // If we've found an element that is smaller than our previously found smallest
            if (array[currentIndex] < array[smallestIndex])
            {
                // then keep track of it
                smallestIndex = currentIndex;
            }
        }

        // smallestIndex is now the smallest element in the remaining array
        // swap our start element with our smallest element (this sorts it into the correct place)
        std::swap(array[startIndex], array[smallestIndex]);
    }
}

int main()
{
    std::array<int, g_arrayElements> array;
    std::iota(array.rbegin(), array.rend(), 1); // fill the array with values 10000 to 1

    Timer t;

    sortArray(array);

    std::cout << "Time taken: " << t.elapsed() << " seconds\n";

    return 0;
}
在作者的机器上，三次运行产生的时间分别为 0.0507、0.0506 和 0.0498。所以我们可以说大约是 0.05 秒。
现在，让我们使用标准库中的 std::sort 进行相同的测试。
#include <algorithm> // for std::sort
#include <array>
#include <chrono> // for std::chrono functions
#include <cstddef> // for std::size_t
#include <iostream>
#include <numeric> // for std::iota

const int g_arrayElements { 10000 };

class Timer
{
private:
    // Type aliases to make accessing nested type easier
    using Clock = std::chrono::steady_clock;
    using Second = std::chrono::duration<double, std::ratio<1> >;

    std::chrono::time_point<Clock> m_beg{ Clock::now() };

public:

    void reset()
    {
        m_beg = Clock::now();
    }

    double elapsed() const
    {
        return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
    }
};

int main()
{
    std::array<int, g_arrayElements> array;
    std::iota(array.rbegin(), array.rend(), 1); // fill the array with values 10000 to 1

    Timer t;

    std::ranges::sort(array); // Since C++20
    // If your compiler isn't C++20-capable
    // std::sort(array.begin(), array.end());

    std::cout << "Time taken: " << t.elapsed() << " seconds\n";

    return 0;
}
在作者的机器上，这产生了以下结果：0.000693、0.000692 和 0.000699。所以基本上就在 0.0007 左右。
换句话说，在这种情况下，std::sort 比我们自己编写的插入排序快 100 倍！
可能影响程序性能的因素
对程序的运行进行计时相当简单，但您的结果可能会受到许多因素的显著影响，了解如何正确测量以及哪些因素会影响计时非常重要。
首先，请确保您使用的是发布构建目标，而不是调试构建目标。调试构建目标通常会关闭优化，而优化会对结果产生显著影响。例如，使用调试构建目标，在作者的机器上运行上述 std::sort 示例需要 0.0235 秒——时间长了 33 倍！
其次，您的计时结果可能会受到系统在后台执行的其他任务的影响。确保您的系统没有执行任何 CPU、内存或硬盘密集型任务（例如玩游戏、搜索文件、运行防病毒扫描或在后台安装更新）。看似无害的事情，例如空闲的 Web 浏览器，当活动选项卡轮换出新的广告横幅并需要解析大量 javascript 时，可能会暂时使您的 CPU 占用率飙升至 100%。在测量之前关闭的应用程序越多，您的结果的方差就越小。
第三，如果您的程序使用随机数生成器，生成的随机数的特定序列可能会影响计时。例如，如果您正在对一个填充了随机数的数组进行排序，结果可能会因每次运行而异，因为排序数组所需的交换次数会因每次运行而异。为了在程序的多次运行中获得更一致的结果，您可以暂时使用文字值（而不是 std::random_device 或系统时钟）为您的随机数生成器播种，以便它在每次运行中生成相同的数字序列。但是，如果您的程序的性能高度依赖于生成的特定随机序列，这也可能导致总体结果产生误导。
第四，确保您没有将等待用户输入的时间计入，因为用户输入需要多长时间不应成为您的计时考虑因素的一部分。如果需要用户输入，请考虑添加一些不依赖用户等待的方式来提供该输入（例如命令行、来自文件、具有绕过输入的代码路径）。
测量性能
在测量程序性能时，至少收集 3 个结果。如果结果都相似，则这些结果很可能代表您的程序在该机器上的实际性能。否则，继续进行测量，直到您获得一组相似的结果（并了解其他哪些结果是异常值）。由于您的系统在某些运行期间在后台执行某些操作，因此出现一个或多个异常值并不少见。
如果您的结果差异很大（并且没有很好地聚类），您的程序很可能受到系统中发生的其他事情或应用程序内随机化效应的显著影响。
由于性能测量受许多因素的影响（特别是硬件速度，还有操作系统、正在运行的应用程序等），因此绝对性能测量（例如“程序在 10 秒内运行”）通常在了解程序在您关心的特定机器上运行情况之外并没有太大用处。在不同的机器上，同一个程序可能在 1 秒、10 秒或 1 分钟内运行。不实际测量一系列不同的硬件很难知道。
然而，在单台机器上，相对性能测量可能很有用。我们可以从程序的几个不同变体中收集性能结果，以确定哪个变体性能最好。例如，如果变体 1 在 10 秒内运行，变体 2 在 8 秒内运行，那么无论该机器的绝对速度如何，变体 2 可能在所有类似机器上都会更快。
测量第二个变体后，一个很好的健全性检查是再次测量第一个变体。如果第一个变体的结果与您对该变体的初始测量结果一致，则两个变体的结果都应该具有合理的比较性。例如，如果变体 1 运行 10 秒，变体 2 运行 8 秒，然后我们再次测量变体 1 并得到 10 秒，那么我们可以合理地得出结论，两个变体的测量都相当准确，并且变体 2 更快。
但是，如果第一个变体的结果与您对该变体的初始测量不再一致，则机器上发生了影响性能的事情，并且将很难判断测量差异是由于变体还是由于机器本身。在这种情况下，最好丢弃现有结果并重新测量。
下一课
19.1
使用 new 和 delete 进行动态内存分配
返回目录
上一课
18.3
标准库算法介绍