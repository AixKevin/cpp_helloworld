# 28.6 — 基本文件 I/O

28.6 — 基本文件 I/O
Alex
2008 年 3 月 31 日，太平洋夏令时晚上 11:05
2024 年 2 月 27 日
C++ 中的文件 I/O 工作方式与普通 I/O 非常相似（只增加了一些微小的复杂性）。C++ 中有 3 个基本的文件 I/O 类：ifstream（派生自 istream）、ofstream（派生自 ostream）和 fstream（派生自 iostream）。这些类分别进行文件输入、输出和输入/输出。要使用文件 I/O 类，你需要包含 fstream 头文件。
与 cout、cin、cerr 和 clog 流不同，文件流必须由程序员显式设置才能使用。然而，这非常简单：要打开文件进行读写，只需实例化一个相应文件 I/O 类的对象，并将文件名作为参数。然后使用插入 (<<) 或提取 (>>) 运算符向文件写入或从文件读取数据。完成后，有几种方法可以关闭文件：显式调用 close() 函数，或者让文件 I/O 变量超出范围（文件 I/O 类析构函数将为你关闭文件）。
文件输出
在以下示例中，我们将使用 ofstream 类进行文件输出。这非常简单。
#include <fstream>
#include <iostream>
 
int main()
{
    // ofstream is used for writing files
    // We'll make a file called Sample.txt
    std::ofstream outf{ "Sample.txt" };

    // If we couldn't open the output file stream for writing
    if (!outf)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened for writing!\n";
        return 1;
    }

    // We'll write two lines into this file
    outf << "This is line 1\n";
    outf << "This is line 2\n";

    return 0;
	
    // When outf goes out of scope, the ofstream
    // destructor will close the file
}
如果你查看项目目录，应该会看到一个名为 Sample.txt 的文件。如果你用文本编辑器打开它，你会发现它确实包含我们写入文件的两行内容。
请注意，也可以使用 put() 函数向文件写入单个字符。
文件输入
现在，我们将读取上一个示例中写入的文件。请注意，如果达到文件末尾 (EOF)，ifstream 将返回 0。我们将利用此事实来确定要读取多少内容。
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // ifstream is used for reading files
    // We'll read from a file called Sample.txt
    std::ifstream inf{ "Sample.txt" };

    // If we couldn't open the output file stream for reading
    if (!inf)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    // While there's still stuff left to read
    std::string strInput{};
    while (inf >> strInput)
        std::cout << strInput << '\n';
    
    return 0;
	
    // When inf goes out of scope, the ifstream
    // destructor will close the file
}
这会产生结果
This
is
line
1
This
is
line
2
嗯，这与我们想要的有些不同。请记住，提取运算符在空白处中断。为了读取整个行，我们必须使用 getline() 函数。
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // ifstream is used for reading files
    // We'll read from a file called Sample.txt
    std::ifstream inf{ "Sample.txt" };

    // If we couldn't open the input file stream for reading
    if (!inf)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    // While there's still stuff left to read
    std::string strInput{};
    while (std::getline(inf, strInput))
	std::cout << strInput << '\n';
    
    return 0;
	
    // When inf goes out of scope, the ifstream
    // destructor will close the file
}
这会产生结果
This is line 1
This is line 2
缓冲输出
C++ 中的输出可能被缓冲。这意味着输出到文件流的任何内容可能不会立即写入磁盘。相反，多个输出操作可能会被批处理并一起处理。这主要是出于性能原因。当缓冲区写入磁盘时，这称为**刷新**缓冲区。导致缓冲区刷新的方法之一是关闭文件——缓冲区的内容将刷新到磁盘，然后文件将被关闭。
缓冲通常不是问题，但在某些情况下可能会给不熟悉的用户带来复杂性。主要问题是当缓冲区中有数据，然后程序立即终止（无论是崩溃还是调用 exit()）时。在这些情况下，文件流类的析构函数不会执行，这意味着文件永远不会关闭，这意味着缓冲区永远不会刷新。在这种情况下，缓冲区中的数据不会写入磁盘，并且会永远丢失。这就是为什么在调用 exit() 之前始终显式关闭所有打开的文件是个好主意。
可以使用 ostream::flush() 函数或向输出流发送 std::flush 手动刷新缓冲区。这两种方法都可用于确保缓冲区的内容立即写入磁盘，以防程序崩溃。
一个有趣的注意事项是 std::endl; 也会刷新输出流。因此，过度使用 std::endl（导致不必要的缓冲区刷新）在进行缓冲 I/O 且刷新成本很高（例如写入文件）时可能会影响性能。出于这个原因，注重性能的程序员通常会使用 ‘\n’ 而不是 std::endl 在输出流中插入换行符，以避免不必要的缓冲区刷新。
文件模式
如果我们尝试写入一个已经存在的文件会发生什么？再次运行输出示例表明，每次程序运行时，原始文件都会被完全覆盖。如果我们想在文件末尾附加更多数据呢？事实证明，文件流构造函数接受一个可选的第二个参数，允许你指定文件应该如何打开的信息。此参数称为模式，它接受的有效标志位于 ios 类中。
Ios 文件模式
含义
app
以追加模式打开文件
ate
在读/写之前查找文件末尾
binary
以二进制模式打开文件（而不是文本模式）
in
以读取模式打开文件（ifstream 的默认设置）
out
以写入模式打开文件（ofstream 的默认设置）
trunc
如果文件已存在，则擦除文件
可以通过按位或运算符（使用 | 运算符）组合多个标志。ifstream 默认为 std::ios::in 文件模式。ofstream 默认为 std::ios::out 文件模式。而 fstream 默认为 std::ios::in | std::ios::out 文件模式，这意味着默认情况下你可以同时读写。
提示
由于 fstream 的设计方式，如果使用 std::ios::in 且要打开的文件不存在，它可能会失败。如果需要使用 fstream 创建新文件，请仅使用 std::ios::out 模式。
让我们编写一个程序，向我们之前创建的 Sample.txt 文件追加两行内容。
#include <iostream>
#include <fstream>

int main()
{
    // We'll pass the ios:app flag to tell the ofstream to append
    // rather than rewrite the file. We do not need to pass in std::ios::out
    // because ofstream defaults to std::ios::out
    std::ofstream outf{ "Sample.txt", std::ios::app };

    // If we couldn't open the output file stream for writing
    if (!outf)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened for writing!\n";
        return 1;
    }

    outf << "This is line 3\n";
    outf << "This is line 4\n";
    
    return 0;
	
    // When outf goes out of scope, the ofstream
    // destructor will close the file
}
现在，如果我们查看 Sample.txt（使用上述打印其内容的示例程序之一，或在文本编辑器中加载它），我们将看到以下内容
This is line 1
This is line 2
This is line 3
This is line 4
使用 open() 显式打开文件
就像可以使用 close() 显式关闭文件流一样，也可以使用 open() 显式打开文件流。open() 的工作方式与文件流构造函数相同——它接受一个文件名和一个可选的文件模式。
例如
std::ofstream outf{ "Sample.txt" };
outf << "This is line 1\n";
outf << "This is line 2\n";
outf.close(); // explicitly close the file

// Oops, we forgot something
outf.open("Sample.txt", std::ios::app);
outf << "This is line 3\n";
outf.close();
你可以在
此处
找到有关 open() 函数的更多信息。
下一课
28.7
随机文件 I/O
返回目录
上一课
28.5
流状态和输入验证