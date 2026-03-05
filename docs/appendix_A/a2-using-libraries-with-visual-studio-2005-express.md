# A.2 — 在 Visual Studio 中使用库

A.2 — 在 Visual Studio 中使用库
Alex
2007 年 6 月 30 日，太平洋夏令时上午 10:01
2024 年 8 月 22 日
回顾使用库所需的过程
每个库一次
获取库。从网站或通过包管理器下载。
安装库。将其解压到目录或通过包管理器安装。
每个项目一次
告诉编译器去哪里查找库的头文件。
告诉链接器去哪里查找库的预编译库文件（如果有）。
告诉链接器链接哪些静态或导入的预编译库文件（如果有）。
在你的程序中 #include 库的头文件。
确保程序知道在哪里找到正在使用的任何动态库。
步骤 1 和 2 -- 获取和安装库
下载并将库安装到硬盘。有关此步骤的更多信息，请参阅关于
静态库和动态库
的教程。
步骤 3 和 4 -- 告诉编译器在哪里查找头文件和库文件
A) 转到项目菜单并选择 Project -> Properties（它应该在底部）
B) 在“Configuration”下拉菜单下，确保选中“All configurations”。
C) 在左侧窗口窗格中，选择“Configuration Properties”->“VC++ Directories”。
D) 在“Include Directories”行，添加库的 .h 文件的路径（确保与之前的条目用分号分隔）。
E) 在“Library Directories”行，添加库的库 (.lib) 文件的路径（如果有）。
F) 单击“OK”。
步骤 5 -- 告诉链接器你的程序正在使用哪些库
对于步骤 5，我们需要将库的 (.lib) 文件添加到我们的项目（如果有的话——如果没有，可以跳过此步骤）。我们按单个项目执行此操作。
A) 转到项目菜单并选择 Project -> Properties（它应该在底部）
B) 在“Configuration”下拉菜单下，确保选中“All configurations”。
C) 在左侧窗口窗格中，选择“Configuration Properties”->“Linker”->“Input”。
D) 将你的 .lib 文件名添加到“Additional Dependencies”列表（与之前的条目用分号分隔）
E) 单击“OK”。
步骤 6 和 7 -- #include 头文件并确保项目可以找到 DLL
像往常一样，只需在项目中 #include 库的头文件。
有关步骤 7 的更多信息，请参阅教程
A1 -- 静态库和动态库
。
vcpkg 包管理器
vcpkg 是微软开发的包管理器，它使 C++ 库的下载、安装、管理和使用更加容易。它与 Visual Studio 集成。有关如何安装和使用 vcpkg 的更多信息，请参阅
此页面
。
下一课
A.3
在 Code::Blocks 中使用库
返回目录
上一课
A.1
静态库和动态库