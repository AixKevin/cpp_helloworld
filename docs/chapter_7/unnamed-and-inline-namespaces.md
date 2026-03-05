# 7.14 — 匿名命名空间和内联命名空间

7.14 — 匿名命名空间和内联命名空间
Alex
2020 年 1 月 3 日，太平洋标准时间下午 1:12
2024 年 11 月 26 日
C++ 支持两种值得了解的命名空间变体。我们不会在此基础上进行构建，因此暂时可以将本课视为可选。
匿名（无名）命名空间
匿名命名空间
（也称为
无名命名空间
）是没有名称的命名空间，如下所示
#include <iostream>

namespace // unnamed namespace
{
    void doSomething() // can only be accessed in this file
    {
        std::cout << "v1\n";
    }
}

int main()
{
    doSomething(); // we can call doSomething() without a namespace prefix

    return 0;
}
这会打印
v1
在匿名命名空间中声明的所有内容都被视为父命名空间的一部分。因此，即使函数
doSomething()
定义在匿名命名空间中，函数本身也可以从父命名空间（在本例中是全局命名空间）访问，这就是为什么我们可以在
main()
中调用
doSomething()
而无需任何限定符。
这可能让匿名命名空间看起来毫无用处。但匿名命名空间的另一个作用是，匿名命名空间内的所有标识符都被视为具有内部链接，这意味着匿名命名空间的内容不能在其定义的文件之外可见。
对于函数，这实际上与将匿名命名空间中的所有函数定义为静态函数相同。以下程序实际上与上面的程序相同
#include <iostream>

static void doSomething() // can only be accessed in this file
{
    std::cout << "v1\n";
}

int main()
{
    doSomething(); // we can call doSomething() without a namespace prefix

    return 0;
}
匿名命名空间通常用于当您有大量内容需要确保保留在给定翻译单元本地时，因为将这些内容聚集在一个匿名命名空间中比单独将所有声明标记为
static
更容易。匿名命名空间还将使程序定义的类型（我们将在后面的课程中讨论）本地化到翻译单元，这是没有替代等效机制可以做到的。
提示
如果您是骨灰级玩家，您可以采取相反的方法——将所有非明确旨在导出/外部的内容放入匿名命名空间。
匿名命名空间通常不应在头文件中使用。
SEI CERT (规则 DCL59-CPP)
有一些很好的示例说明了原因。
最佳实践
当您有要保留在翻译单元本地的内容时，首选匿名命名空间。
避免在头文件中使用匿名命名空间。
内联命名空间
现在考虑以下程序
#include <iostream>

void doSomething()
{
    std::cout << "v1\n";
}

int main()
{
    doSomething();

    return 0;
}
这会打印
v1
很简单，对吧？
但是，假设您对
doSomething()
不满意，并且您想以某种方式改进它，从而改变其行为。但是，如果您这样做，您可能会破坏使用旧版本程序的现有程序。您如何处理这种情况？
一种方法是创建具有不同名称的函数的新版本。但是，在许多更改的过程中，您最终可能会得到一组名称几乎相同的函数（
doSomething
、
doSomething_v2
、
doSomething_v3
等）。
另一种方法是使用内联命名空间。
内联命名空间
通常用于版本化内容。与匿名命名空间非常相似，内联命名空间中声明的任何内容都被视为父命名空间的一部分。但是，与匿名命名空间不同，内联命名空间不影响链接。
要定义内联命名空间，我们使用
inline
关键字
#include <iostream>

inline namespace V1 // declare an inline namespace named V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

namespace V2 // declare a normal namespace named V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // calls the V1 version of doSomething()
    V2::doSomething(); // calls the V2 version of doSomething()

    doSomething(); // calls the inline version of doSomething() (which is V1)
 
    return 0;
}
这会打印
V1
V2
V1
在上面的示例中，
doSomething()
的调用者将获得
doSomething()
的 V1 版本（内联版本）。想要使用较新版本的调用者可以显式调用
V2::doSomething()
。这保留了现有程序的功能，同时允许较新的程序利用较新/更好的变体。
或者，如果您想推送较新版本
#include <iostream>

namespace V1 // declare a normal namespace named V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace V2 // declare an inline namespace named V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // calls the V1 version of doSomething()
    V2::doSomething(); // calls the V2 version of doSomething()

    doSomething(); // calls the inline version of doSomething() (which is V2)
 
    return 0;
}
这会打印
V1
V2
V2
在此示例中，
doSomething()
的所有调用者将默认获得 v2 版本（较新和更好的版本）。仍然想要旧版本
doSomething()
的用户可以显式调用
V1::doSomething()
来访问旧行为。这意味着想要 V1 版本的现有程序需要全局替换
doSomething
为
V1::doSomething
，但如果函数命名良好，这通常不会有问题。
混合使用内联和匿名命名空间
可选
命名空间可以是内联的，也可以是匿名的
#include <iostream>

namespace V1 // declare a normal namespace named V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace // declare an inline unnamed namespace
{
    void doSomething() // has internal linkage
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // calls the V1 version of doSomething()
    // there is no V2 in this example, so we can't use V2:: as a namespace prefix

    doSomething(); // calls the inline version of doSomething() (which is the anonymous one)

    return 0;
}
但是，在这种情况下，最好将匿名命名空间嵌套在内联命名空间中。这具有相同的效果（匿名命名空间中的所有函数默认具有内部链接），但仍然为您提供一个可以使用的显式命名空间名称
#include <iostream>

namespace V1 // declare a normal namespace named V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace V2 // declare an inline namespace named V2
{
    namespace // unnamed namespace
    {
        void doSomething() // has internal linkage
        {
            std::cout << "V2\n";
        }

    }
}

int main()
{
    V1::doSomething(); // calls the V1 version of doSomething()
    V2::doSomething(); // calls the V2 version of doSomething()

    doSomething(); // calls the inline version of doSomething() (which is V2)

    return 0;
}
下一课
7.x
第 7 章总结和测验
返回目录
上一课
7.13
Using declarations 和 using directives