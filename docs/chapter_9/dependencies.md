# 23.5 — 依赖关系

23.5 — 依赖关系
Alex
2016 年 8 月 23 日，下午 4:36 PDT
2023 年 9 月 11 日
到目前为止，我们已经探讨了 3 种关系类型：组合、聚合和关联。我们把最简单的一种留到了最后：依赖关系。
在日常对话中，我们使用“依赖”一词来表示一个对象为了完成特定任务而依赖于另一个对象。例如，如果你摔断了脚，你需要依赖拐杖来行走（但除此之外不需要）。花朵依赖蜜蜂授粉，以便结果或繁殖（但除此之外不需要）。
当一个对象调用另一个对象的功能以完成某个特定任务时，就发生了
依赖
。这比关联是一种更弱的关系，但即便如此，被依赖对象上的任何更改都可能破坏（依赖）调用者中的功能。依赖关系始终是单向关系。
你已经多次看到的一个很好的依赖关系示例是 std::ostream。我们的类使用 std::ostream 是为了完成向控制台打印某些内容的任务，但除此之外不使用。
例如
#include <iostream>
 
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0): m_x{x}, m_y{y}, m_z{z}
    {
    }
 
    friend std::ostream& operator<< (std::ostream& out, const Point& point); // Point has a dependency on std::ostream here
};
 
std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // Since operator<< is a friend of the Point class, we can access Point's members directly.
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';
 
    return out;
}
 
int main()
{
    Point point1 { 2.0, 3.0, 4.0 };
 
    std::cout << point1; // the program has a dependency on std::cout here
 
    return 0;
}
在上面的代码中，Point 与 std::ostream 没有直接关系，但它依赖于 std::ostream，因为 operator<< 使用 std::ostream 将 Point 打印到控制台。
C++ 中的依赖关系与关联
通常，人们对依赖关系和关联的区别有一些困惑。
在 C++ 中，关联是一种关系，其中一个类将指向关联类的直接或间接“链接”作为成员。例如，Doctor 类将指向其 Patient 的指针数组作为成员。你可以随时询问 Doctor 他的病人是谁。Driver 类将司机对象拥有的汽车的 id 作为整数成员持有。Driver 总是知道与之关联的 Car 是什么。
依赖关系通常不是成员。相反，被依赖的对象通常是按需实例化（例如打开文件以写入数据），或者作为参数传递给函数（例如上面重载的 operator<< 中的 std::ostream）。
幽默休息
依赖关系（感谢我们的朋友
xkcd
）
当然，你我都知道这实际上是一种自反关联！
下一课
23.6
容器类
返回目录
上一课
23.4
关联