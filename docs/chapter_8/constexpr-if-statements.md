# 8.4 — Constexpr if 语句

8.4 — Constexpr if 语句
Alex
2023 年 5 月 30 日，下午 5:18 PDT
2024 年 3 月 5 日
通常，if 语句的条件是在运行时评估的。
然而，考虑条件是常量表达式的情况，例如以下示例
#include <iostream>

int main()
{
	constexpr double gravity{ 9.8 };

	// reminder: low-precision floating point literals of the same type can be tested for equality
	if (gravity == 9.8) // constant expression, always true
		std::cout << "Gravity is normal.\n";   // will always be executed
	else
		std::cout << "We are not on Earth.\n"; // will never be executed

	return 0;
}
因为
gravity
是 constexpr 且用值
9.8
初始化，所以条件
gravity == 9.8
必须评估为
true
。因此，else 语句永远不会执行。
在运行时评估 constexpr 条件是浪费的（因为结果永远不会改变）。将永远不会执行的代码编译到可执行文件中也是浪费的。
Constexpr if 语句
C++17
C++17 引入了
constexpr if 语句
，它要求条件必须是常量表达式。constexpr-if-语句的条件将在编译时评估。
如果 constexpr 条件评估为
true
，整个 if-else 将被 true-statement 替换。如果 constexpr 条件评估为
false
，整个 if-else 将被 false-statement 替换（如果存在）或什么都不替换（如果没有 else）。
要使用 constexpr-if-语句，我们在
if
之后添加
constexpr
关键字
#include <iostream>

int main()
{
	constexpr double gravity{ 9.8 };

	if constexpr (gravity == 9.8) // now using constexpr if
		std::cout << "Gravity is normal.\n";
	else
		std::cout << "We are not on Earth.\n";

	return 0;
}
当上述代码编译时，编译器将在编译时评估条件，发现它始终为
true
，并只保留单个语句
std::cout << "Gravity is normal.\n";
。
换句话说，它将编译这个
int main()
{
	constexpr double gravity{ 9.8 };

	std::cout << "Gravity is normal.\n";

	return 0;
}
最佳实践
当条件是常量表达式时，优先使用 constexpr if 语句而不是非 constexpr if 语句。
现代编译器和带有 constexpr 条件的 if 语句
C++17
出于优化目的，现代编译器通常会将具有 constexpr 条件的非 constexpr if 语句视为 constexpr-if-语句。但是，它们并非必须这样做。
遇到带有 constexpr 条件的非 constexpr if 语句的编译器可能会发出警告，建议您改用
if constexpr
。这将确保编译时评估会发生（即使禁用了优化）。
下一课
8.5
Switch 语句基础
返回目录
上一课
8.3
常见的 if 语句问题