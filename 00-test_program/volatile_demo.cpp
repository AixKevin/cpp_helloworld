// volatile 关键字示例演示

#include <iostream>

// ====== 什么是 volatile？ ======
// volatile 告诉编译器："这个变量可能被意外改变"
// 编译器不应该优化（缓存）这个变量的值，每次访问都要从内存读取

// ====== 典型使用场景 ======

// 场景1: 硬件寄存器
// 硬件可能在外设寄存器中存储值，程序需要每次都读取最新值
struct HardwareRegister {
    volatile uint32_t STATUS;    // 硬件状态寄存器，可能被硬件随时修改
    volatile uint32_t CONTROL;   // 控制寄存器
};

// 场景2: 多线程共享变量
// 多个线程可能访问同一个变量
struct SharedData {
    volatile bool flag;          // 共享标志位
    volatile int counter;        // 共享计数器
};

// 场景3: 信号处理程序中的变量
// 信号处理函数可能修改在主程序中检查的变量
volatile bool g_interruptReceived = false;

// ====== volatile 的限制 ======
// volatile 不保证原子性！
// volatile int count = 0;
// count++;  // 这不是原子操作，仍然有竞态条件问题

// ====== volatile vs const ======
void demonstrate_volatile_const() {
    // const volatile: 常量但可能被意外修改
    // 通常用于硬件只读寄存器
    const volatile int* hw_register = (const volatile int*)0x40001000;
    // *hw_register 只能读取，不能写入，且每次都要从硬件读取
}

int main() {
    std::cout << "===== volatile 示例 =====" << std::endl;
    
    // 演示 volatile 变量
    volatile int value = 10;
    std::cout << "volatile int value = " << value << std::endl;
    
    value = 20;
    std::cout << "After value = 20: " << value << std::endl;
    
    // volatile 指针
    int normal_var = 100;
    volatile int* ptr = &normal_var;
    
    std::cout << "===== 总结 =====" << std::endl;
    std::cout << "volatile 的作用：" << std::endl;
    std::cout << "1. 告诉编译器每次都要从内存读取" << std::endl;
    std::cout << "2. 防止编译器优化掉变量的读取/写入" << std::endl;
    std::cout << "3. 用于硬件寄存器、多线程共享等场景" << std::endl;
    
    return 0;
}
