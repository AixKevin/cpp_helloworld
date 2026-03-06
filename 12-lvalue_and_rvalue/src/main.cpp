#include <iostream>
#include <algorithm>
// 编写一个名为 sort2 的函数，允许调用者传递 2 个 int 变量作为参数。函数返回时，第一个参数应保存两个值中较小的一个，第二个参数应保存两个值中较大的一个。

// 提示：std::swap() 函数（位于 <algorithm> 头文件中）可用于交换两个变量的值。例如：std::swap(x, y) 交换变量 x 和 y 的值。

// 以下代码应运行并打印注释中指出的值

void sort2(int& x, int& y){
    if(x > y){
        std::swap(x, y);
    }
}

int main()
{
    int x { 7 };
    int y { 5 };

    std::cout << x << ' ' << y << '\n'; // should print 7 5

    sort2(x, y); // make sure sort works when values need to be swapped
    std::cout << x << ' ' << y << '\n'; // should print 5 7

    sort2(x, y); // make sure sort works when values don't need to be swapped
    std::cout << x << ' ' << y << '\n'; // should print 5 7

    return 0;
}
