# 16.12 — std::vector<bool>

16.12 — std::vector<bool>
Alex
2023年9月11日，下午2:54 PDT
2024年1月10日
在课程
O.1 -- 通过 std::bitset 进行位标志和位操作
中，我们讨论了
std::bitset
如何能够将8个布尔值压缩到一个字节中。然后可以通过
std::bitset
的成员函数修改这些位。
std::vector
有一个有趣的技巧。
std::vector<bool>
有一个特殊的实现，它可以通过类似地将8个布尔值压缩到一个字节中，从而在布尔值方面更节省空间。
致进阶读者
当一个模板类对特定的模板类型参数有不同的实现时，这称为
类模板特化
。我们在课程
26.4 -- 类模板特化
中进一步讨论这个主题。
与为位操作设计的
std::bitset
不同，
std::vector<bool>
缺少位操作成员函数。
使用
std::vector<bool>
在大多数情况下，
std::vector<bool>
的工作方式与普通的
std::vector
相同
#include <iostream>
#include <vector>

int main()
{
    std::vector<bool> v { true, false, false, true, true };
    
    for (int i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // Change the Boolean value with index 4 to false
    v[4] = false;

    for (int i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
在作者的64位机器上，这会打印
1 0 0 1 1
1 0 0 1 0
std::vector<bool>
的权衡
然而，
std::vector<bool>
存在一些用户应该注意的权衡。
首先，
std::vector<bool>
的开销相当高（在作者的机器上，
sizeof(std::vector<bool>)
是40字节），所以除非您分配的布尔值数量超过您的架构的开销，否则您不会节省内存。
其次，
std::vector<bool>
的性能高度依赖于实现（因为实现甚至不需要进行优化，更不用说做得好）。根据
这篇文章
，高度优化的实现可以比替代方案快得多。然而，优化不佳的实现会更慢。
第三，也是最重要的一点，
std::vector<bool>
不是一个向量（它不要求在内存中是连续的），它也不持有
bool
值（它持有一组位），它也不符合 C++ 对容器的定义。
尽管
std::vector<bool>
在大多数情况下表现得像一个向量，但它与标准库的其余部分并不完全兼容。适用于其他元素类型的代码可能不适用于
std::vector<bool>
。
例如，当
T
是除
bool
之外的任何类型时，以下代码有效
template<typename T>
void foo( std::vector<T>& v )
{
    T& first = v[0]; // get a reference to the first element
    // Do something with first
}
避免使用
std::vector<bool>
现代的共识是，通常应避免使用
std::vector<bool>
，因为其性能提升不太可能抵消由于它不是一个合适的容器而导致的兼容性问题。
不幸的是，
std::vector<bool>
的这个优化版本默认启用，并且无法禁用它以支持实际上是容器的非优化版本。有人呼吁弃用
std::vector<bool>
，并且正在进行工作以确定压缩的
bool
向量的替代方案可能是什么样子（也许是未来的
std::dynamic_bitset
）。
我们的建议如下
当您需要的位数在编译时已知，您不需要存储超过适中数量的布尔值（例如，低于64k），并且有限的运算符和成员函数集（例如，缺乏迭代器支持）满足您的要求时，使用 (constexpr)
std::bitset
。
当您需要一个可调整大小的布尔值容器并且空间节省不是必需时，首选
std::vector<char>
。这种类型表现得像一个普通容器。
当您需要一个动态位集进行位操作时，优先选择第三方动态位集实现（例如
boost::dynamic_bitset
）。这些类型不会假装是标准库容器，尽管它们不是。
最佳实践
优先选择
constexpr std::bitset
、
std::vector<char>
或第三方动态位集，而不是
std::vector<bool>
。
下一课
16.x
第16章 总结与测试
返回目录
上一课
16.11
std::vector 和栈行为