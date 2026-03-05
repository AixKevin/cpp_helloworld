// AS-IF 规则示例演示

#include <iostream>

// 示例1: 常量折叠
void example1() {
    int a = 2 * 3;      // 编译时计算为 6
    int b = 10 - 4;     // 编译时计算为 6
    int c = a + b;      // 6 + 6 = 12
    std::cout << "Example1: " << c << std::endl;
}

// 示例2: 常量传播
void example2() {
    const int x = 100;  // const 让编译器更确定
    const int y = 200;
    int result = x + y; // 传播为 100 + 200 = 300
    std::cout << "Example2: " << result << std::endl;
}

// 示例3: 死代码消除
void example3() {
    int unused = 999;   // 从未使用
    std::cout << "Example3: Hello" << std::endl;
    // unused 会被完全删除
}

// 示例4: 条件优化
void example4() {
    if (true) {  // 编译时已知条件
        std::cout << "Example4: Always runs" << std::endl;
    }
    // 整个 if 分支可能被消除
}

// 示例5: 循环优化
void example5() {
    // 循环次数编译时已知
    int sum = 0;
    for (int i = 0; i < 3; ++i) {
        sum += i;  // 0+1+2 = 3
    }
    std::cout << "Example5: " << sum << std::endl;
    // 整个循环可能被优化为 sum = 3
}

int main() {
    example1();
    example2();
    example3();
    example4();
    example5();
    return 0;
}
