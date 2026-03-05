# 8.15 — 全局随机数 (Random.h)

8.15 — 全局随机数 (Random.h)
Alex
2023 年 12 月 28 日，太平洋标准时间下午 4:46
2025 年 1 月 29 日
如果我们想在多个函数或文件中使用随机数生成器，该怎么办？一种方法是在
main()
函数中创建（并播种）我们的 PRNG，然后将其传递到所有需要它的地方。但是对于我们可能只是偶尔在许多不同地方使用的东西来说，这样传递会增加很多麻烦。在代码中传递这样的对象会增加很多混乱。
或者，您可以在每个需要它的函数中创建一个静态局部
std::mt19937
变量（静态的，因此它只播种一次）。然而，让每个使用随机数生成器的函数都定义和播种自己的局部生成器是过度的，并且对每个生成器的低调用量可能导致较低质量的结果。
我们真正想要的是一个可以共享和访问的单个 PRNG 对象，它可以在我们所有的函数和文件中使用。这里最好的选择是创建一个全局随机数生成器对象（在命名空间内！）。还记得我们告诉您要避免非 const 全局变量吗？这是一个例外。
这是一个简单的、仅头文件的解决方案，您可以将其 #include 到任何需要访问随机的、自播种的
std::mt19937
的代码文件中。
Random.h
#ifndef RANDOM_MT_H
#define RANDOM_MT_H

#include <chrono>
#include <random>

// This header-only Random namespace implements a self-seeding Mersenne Twister.
// Requires C++17 or newer.
// It can be #included into as many code files as needed (The inline keyword avoids ODR violations)
// Freely redistributable, courtesy of learncpp.com (https://learncpp.com.cn/cpp-tutorial/global-random-numbers-random-h/)
namespace Random
{
	// Returns a seeded Mersenne Twister
	// Note: we'd prefer to return a std::seed_seq (to initialize a std::mt19937), but std::seed can't be copied, so it can't be returned by value.
	// Instead, we'll create a std::mt19937, seed it, and then return the std::mt19937 (which can be copied).
	inline std::mt19937 generate()
	{
		std::random_device rd{};

		// Create seed_seq with clock and 7 random numbers from std::random_device
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };

		return std::mt19937{ ss };
	}

	// Here's our global std::mt19937 object.
	// The inline keyword means we only have one global instance for our whole program.
	inline std::mt19937 mt{ generate() }; // generates a seeded std::mt19937 and copies it into our global object

	// Generate a random int between [min, max] (inclusive)
        // * also handles cases where the two arguments have different types but can be converted to int
	inline int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}

	// The following function templates can be used to generate random numbers in other cases

	// See https://learncpp.com.cn/cpp-tutorial/function-template-instantiation/
	// You can ignore these if you don't understand them

	// Generate a random value between [min, max] (inclusive)
	// * min and max must have the same type
	// * return value has same type as min and max
	// * Supported types:
	// *    short, int, long, long long
	// *    unsigned short, unsigned int, unsigned long, or unsigned long long
	// Sample call: Random::get(1L, 6L);             // returns long
	// Sample call: Random::get(1u, 6u);             // returns unsigned int
	template <typename T>
	T get(T min, T max)
	{
		return std::uniform_int_distribution<T>{min, max}(mt);
	}

	// Generate a random value between [min, max] (inclusive)
	// * min and max can have different types
        // * return type must be explicitly specified as a template argument
	// * min and max will be converted to the return type
	// Sample call: Random::get<std::size_t>(0, 6);  // returns std::size_t
	// Sample call: Random::get<std::size_t>(0, 6u); // returns std::size_t
	// Sample call: Random::get<std::int>(0, 6u);    // returns int
	template <typename R, typename S, typename T>
	R get(S min, T max)
	{
		return get<R>(static_cast<R>(min), static_cast<R>(max));
	}
}

#endif
使用 Random.h
使用上述方法生成随机数就像遵循以下三个步骤一样简单：
将上述代码复制/粘贴到项目目录中名为
Random.h
的文件中并保存。可选地将 Random.h 添加到您的项目中。
在项目中任何需要生成随机数的 .cpp 文件中
#include "Random.h"
。
调用
Random::get(min, max)
来生成一个介于
min
和
max
之间的随机数（包含两端）。无需初始化或设置。
这是一个演示 Random.h 不同用法的示例程序：
main.cpp
#include "Random.h" // defines Random::mt, Random::get(), and Random::generate()
#include <cstddef> // for std::size_t
#include <iostream>

int main()
{
	// We can call Random::get() to generate random integral values
	// If the two arguments have the same type, the returned value will have that same type.
	std::cout << Random::get(1, 6) << '\n';   // returns int between 1 and 6
	std::cout << Random::get(1u, 6u) << '\n'; // returns unsigned int between 1 and 6

        // In cases where we have two arguments with different types
        // and/or if we want the return type to be different than the argument types
        // We must specify the return type using a template type argument (between the angled brackets)
	// See https://learncpp.com.cn/cpp-tutorial/function-template-instantiation/
	std::cout << Random::get<std::size_t>(1, 6u) << '\n'; // returns std::size_t between 1 and 6

	// If we have our own distribution, we can access Random::mt directly

	// Let's create a reusable random number generator that generates uniform numbers between 1 and 6
	std::uniform_int_distribution die6{ 1, 6 }; // for C++14, use std::uniform_int_distribution<> die6{ 1, 6 };
	for (int count{ 1 }; count <= 10; ++count)
	{
		std::cout << die6(Random::mt) << '\t'; // generate a roll of the die here
	}

	std::cout << '\n';

	return 0;
}
关于 Random.h 实现的几点说明
可选
通常，在头文件中定义变量和函数会导致当该头文件包含到多个源文件时违反一次定义规则 (ODR)。但是，我们已经使我们的
mt
变量和支持函数
inline
，这允许我们拥有重复的定义而不会违反 ODR，只要这些定义都相同。因为我们是从头文件 #包含这些定义（而不是手动输入或复制/粘贴它们），我们可以确保它们是相同的。内联函数和变量被添加到语言中，主要是为了使这种仅头文件功能成为可能。
相关内容
我们在课程
7.9 -- 内联函数和变量
中介绍了内联函数和变量。
我们必须克服的另一个挑战是我们如何初始化全局
Random::mt
对象，因为我们希望它是自播种的，这样我们就不必记住显式调用初始化函数才能使其正常工作。我们的初始化器必须是一个表达式。但是为了初始化
std::mt19937
，我们需要几个辅助对象（一个
std::random_device
和一个
std::seed_seq
），它们必须定义为语句。这就是辅助函数派上用场的地方。函数调用是一个表达式，因此我们可以使用函数的返回值作为初始化器。在函数内部，我们可以拥有我们需要的任何语句组合。因此，我们的
generate()
函数创建并返回一个完全播种的
std::mt19937
对象（使用系统时钟和
std::random_device
进行播种），我们将其用作全局
Random::mt
对象的初始化器。
下一课
8.x
第 8 章总结和测验
返回目录
上一课
8.14
使用 Mersenne Twister 生成随机数