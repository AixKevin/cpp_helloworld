# 0.13 — 我的编译器正在使用哪个语言标准？

0.13 — 我的编译器正在使用哪个语言标准？
Alex
2024年4月18日，上午10:29 PDT
2024年12月29日
以下程序旨在打印你的编译器当前使用的语言标准名称。你可以复制/粘贴、编译并运行此程序，以验证你的编译器是否使用了你期望的语言标准。
PrintStandard.cpp
// This program prints the C++ language standard your compiler is currently using
// Freely redistributable, courtesy of learncpp.com (https://learncpp.com.cn/cpp-tutorial/what-language-standard-is-my-compiler-using/)

#include <iostream>

const int numStandards = 7;
// The C++26 stdCode is a placeholder since the exact code won't be determined until the standard is finalized
const long stdCode[numStandards] = { 199711L, 201103L, 201402L, 201703L, 202002L, 202302L, 202612L};
const char* stdName[numStandards] = { "Pre-C++11", "C++11", "C++14", "C++17", "C++20", "C++23", "C++26" };

long getCPPStandard()
{
    // Visual Studio is non-conforming in support for __cplusplus (unless you set a specific compiler flag, which you probably haven't)
    // In Visual Studio 2015 or newer we can use _MSVC_LANG instead
    // See https://devblogs.microsoft.com/cppblog/msvc-now-correctly-reports-__cplusplus/
#if defined (_MSVC_LANG)
    return _MSVC_LANG;
#elif defined (_MSC_VER)
    // If we're using an older version of Visual Studio, bail out
    return -1;
#else
    // __cplusplus is the intended way to query the language standard code (as defined by the language standards)
    return __cplusplus;
#endif
}

int main()
{
    long standard = getCPPStandard();

    if (standard == -1)
    {
        std::cout << "Error: Unable to determine your language standard.  Sorry.\n";
        return 0;
    }
    
    for (int i = 0; i < numStandards; ++i)
    {
        // If the reported version is one of the finalized standard codes
        // then we know exactly what version the compiler is running
        if (standard == stdCode[i])
        {
            std::cout << "Your compiler is using " << stdName[i]
                << " (language standard code " << standard << "L)\n";
            break;
        }

        // If the reported version is between two finalized standard codes,
        // this must be a preview / experimental support for the next upcoming version.
        if (standard < stdCode[i])
        {
            std::cout << "Your compiler is using a preview/pre-release of " << stdName[i]
                << " (language standard code " << standard << "L)\n";
            break;
        }
    }
    
    return 0;
}
构建或运行时问题
如果你在尝试构建此程序时遇到错误，可能是你的项目设置不正确。请参阅
0.8 -- 几个常见的 C++ 问题
以获取常见问题的建议。如果这没有帮助，请回顾从
0.6 -- 安装集成开发环境 (IDE)
开始的课程。
如果程序打印“错误：无法确定您的语言标准”，您的编译器可能不符合规范。如果您使用的是流行的编译器，并且出现这种情况，请在下方留言并提供相关信息（例如编译器的名称和版本）。
如果此程序打印的语言标准与您预期的不同
检查你的 IDE 设置，确保你的编译器配置为使用你期望的语言标准。有关如何为一些主要编译器执行此操作的更多信息，请参阅
0.12 -- 配置你的编译器：选择语言标准
。确保没有拼写错误或格式错误。有些编译器要求为每个项目而不是全局设置语言标准，所以如果你刚刚创建了一个新项目，可能就是这种情况。
您的IDE或编译器甚至可能没有读取您正在编辑的配置文件（我们偶尔会看到读者对VS Code的反馈）。如果情况似乎如此，请查阅您的IDE或编译器的文档。
问：如果我的编译器使用的是预览/预发布版本，我应该回退一个版本吗？
如果你只是在学习这门语言，那没必要。只需注意，即将推出的语言版本中的某些功能可能缺失、不完整、有错误，或者可能会略有变化。
下一课
1.1
语句和程序结构
返回目录
上一课
0.12
配置你的编译器：选择语言标准