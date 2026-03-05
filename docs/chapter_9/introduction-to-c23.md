# B.5 — C++23 简介

B.5 — C++23 简介
Alex
2024年1月25日，太平洋标准时间下午1:33
2025年1月17日
什么是 C++23？
2023 年 2 月，ISO（国际标准化组织）批准了新版 C++，名为 C++23。
C++23 中的新改进
为了您的兴趣，这里列出了 C++23 添加的主要更改。请注意，此列表不全面，但旨在突出一些值得关注的关键更改。
Constexpr <cmath> (例如
std::abs()
)，和 <cstdlib> (
6.7 -- 关系运算符和浮点比较
)。
Constexpr
std::unique_ptr
（暂无课程）。
显式
this
参数（暂无课程）。
固定大小浮点类型（通过 <stdfloat>）（暂无课程）。
格式化打印函数
std::print
和
std::println
（暂无课程）
std::size_t
及其对应有符号类型的字面量后缀（
5.2 -- 字面量
）。
多维下标
operator[]
（在课程
17.13 -- 多维 std::array
中提及）。
多维跨度
std::mdspan
（
17.13 -- 多维 std::array
）。
预处理器指令
#elifdef
和
#elifndef
（暂无课程）。
预处理器指令
#warning
（暂无课程）。
堆栈跟踪库（暂无课程）
标准库模块
std
（和
std.compat
）（暂无课程）。
静态
operator()
和
operator[]
（暂无课程）。
std::bitset
现在完全是 constexpr。
std::expected
（暂无课程）
std::ranges
算法
starts_with
、
ends_with
、
contains
（暂无课程）
std::string::contains
和
std::string_view::contains
（暂无课程）
std::to_underlying
用于获取枚举的基础类型（
13.6 -- 作用域枚举（枚举类）
）。
std::unreachable()
（暂无课程）。
在常量表达式中使用未知指针和引用（
17.2 -- std::array 长度和索引
）。
下一课
C.1
结束了吗？
返回目录
上一课
B.4
C++20 简介