cmake_minimum_required(VERSION 3.10)

# 1. 项目名称（以后每次新建项目，只改这一行即可！）
project(function_template VERSION 1.0)

# 2. 设置 C++ 标准 (推荐 C++17 或 20)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 3. 自动扫描 src 目录下的所有 .cpp 文件
# (注意：这是为了方便个人开发，工业级大项目通常建议手动列出)
file(GLOB_RECURSE SOURCES "src/sub.cpp")

# 4. 自动将 include 目录加入头文件搜索路径
include_directories(include)

# 5. 生成可执行文件
add_executable(${PROJECT_NAME} ${SOURCES})

# 6. (可选) 设置输出目录，让生成的 .exe 都跑去 bin 文件夹，不污染代码
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    # 判断编译器类型（因为 MSVC 和 GCC 的参数不一样）
    if(MSVC)
        # Visual Studio 的编译器选项
        add_compile_options(/W4)
    else()
        # GCC / Clang 的编译器选项 (MinGW 用这个)
        # -Wall: 开启大部分警告
        # -Wextra: 开启额外警告
        # -O2: 注意！这里仅作演示，通常建议交给 Release 模式控制，不要在这里写
        add_compile_options(-Wall -Wextra) 
    endif()
endif()

# -s 参数告诉 GCC/MinGW：剥离所有符号表 (Strip symbols)
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_link_options(${PROJECT_NAME} PRIVATE -s)
endif()
