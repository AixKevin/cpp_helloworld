# 28.7 — 随机文件 I/O

28.7 — 随机文件 I/O
Alex
2008年4月4日，太平洋夏令时晚上10:04
2024年4月16日
文件指针
每个文件流类都包含一个文件指针，用于跟踪文件中当前的读/写位置。当从文件中读取或写入内容时，读/写操作会在文件指针的当前位置进行。默认情况下，当以读或写模式打开文件时，文件指针会设置在文件开头。但是，如果文件以追加模式打开，文件指针会移动到文件末尾，这样写入操作就不会覆盖文件的当前内容。
使用 seekg() 和 seekp() 进行随机文件访问
到目前为止，我们进行的所有文件访问都是顺序的——也就是说，我们按顺序读写文件内容。然而，也可以进行随机文件访问——即，跳到文件中的各个位置来读取其内容。当您的文件包含大量记录，并且您希望检索特定记录时，这会非常有用。您可以直接跳到您希望检索的记录，而不是读取所有记录直到找到您想要的记录。
随机文件访问通过使用 seekg() 函数（用于输入）和 seekp() 函数（用于输出）来操作文件指针。如果您想知道，g 代表“get”，p 代表“put”。对于某些类型的流，seekg()（改变读取位置）和 seekp()（改变写入位置）是独立操作的——但是，对于文件流，读取和写入位置始终相同，因此 seekg 和 seekp 可以互换使用。
seekg() 和 seekp() 函数接受两个参数。第一个参数是偏移量，用于确定文件指针移动的字节数。第二个参数是一个 ios 标志，指定偏移量参数应从何处偏移。
Ios 查找标志
含义
beg
偏移量相对于文件开头（默认）
cur
偏移量相对于文件指针的当前位置
end
偏移量相对于文件末尾
正偏移量表示将文件指针向文件末尾移动，而负偏移量表示将文件指针向文件开头移动。
以下是一些示例
inf.seekg(14, std::ios::cur); // move forward 14 bytes
inf.seekg(-18, std::ios::cur); // move backwards 18 bytes
inf.seekg(22, std::ios::beg); // move to 22nd byte in file
inf.seekg(24); // move to 24th byte in file
inf.seekg(-28, std::ios::end); // move to the 28th byte before end of the file
移动到文件开头或末尾很容易
inf.seekg(0, std::ios::beg); // move to beginning of file
inf.seekg(0, std::ios::end); // move to end of file
警告
在文本文件中，定位到文件开头以外的位置可能会导致意外行为。
在编程中，换行符（‘\n’）实际上是一个抽象。
在 Windows 上，换行符表示为顺序的 CR（回车）和 LF（换行）字符（因此占用 2 个字节的存储空间）。
在 Unix 上，换行符表示为 LF（换行）字符（因此占用 1 个字节的存储空间）。
在任何一个方向上跳过换行符都会占用可变数量的字节，具体取决于文件的编码方式，这意味着结果会因所使用的编码而异。
此外，在某些操作系统上，文件可能会用尾随零字节（值为 0 的字节）填充。定位到文件末尾（或从文件末尾偏移）在这些文件上会产生不同的结果。
为了让您了解它们的工作原理，我们来使用 seekg() 和我们在上一课中创建的输入文件做一个示例。那个输入文件看起来像这样
This is line 1
This is line 2
This is line 3
This is line 4
这是示例
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    std::ifstream inf{ "Sample.txt" };

    // If we couldn't open the input file stream for reading
    if (!inf)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    std::string strData;

    inf.seekg(5); // move to 5th character
    // Get the rest of the line and print it, moving to line 2
    std::getline(inf, strData);
    std::cout << strData << '\n';

    inf.seekg(8, std::ios::cur); // move 8 more bytes into file
    // Get rest of the line and print it
    std::getline(inf, strData);
    std::cout << strData << '\n';

    inf.seekg(-14, std::ios::end); // move 14 bytes before end of file
    // Get rest of the line and print it
    std::getline(inf, strData); // undefined behavior
    std::cout << strData << '\n';

    return 0;
}
这会产生结果
is line 1
line 2
This is line 4
第三行您可能会得到不同的结果，具体取决于您的文件编码方式。
seekg() 和 seekp() 更适合用于二进制文件。您可以通过以下方式以二进制模式打开上述文件：
std::ifstream inf {"Sample.txt", std::ifstream::binary};
另外两个有用的函数是 tellg() 和 tellp()，它们返回文件指针的绝对位置。这可以用来确定文件的大小。
std::ifstream inf {"Sample.txt"};
inf.seekg(0, std::ios::end); // move to end of file
std::cout << inf.tellg();
在作者的机器上，这会打印出
64
这是 sample.txt 的字节长度（假设最后一行后面有换行符）。
作者注
上例中
64
的结果出现在 Windows 上。如果您在 Unix 上运行该示例，您将得到
60
，这是由于较小的换行符表示。如果您的文件用尾随零字节填充，您可能会得到其他结果。
同时读写文件使用 fstream
fstream 类能够同时读写文件——几乎！这里最大的注意事项是，无法任意在读写之间切换。一旦发生读写操作，切换的唯一方法是执行修改文件位置的操作（例如 seek）。如果您实际上不想移动文件指针（因为它已经位于您想要的位置），您可以随时定位到当前位置。
// assume iofile is an object of type fstream
iofile.seekg(iofile.tellg(), std::ios::beg); // seek to current file position
如果您不这样做，可能会发生各种奇怪的事情。
（注意：尽管看起来
iofile.seekg(0, std::ios::cur)
也会起作用，但某些编译器似乎会将其优化掉）。
另一个棘手之处：与 ifstream 不同，我们可以通过
while (inf)
来判断是否还有更多内容可读，这在 fstream 中行不通。
让我们使用 fstream 来做一个文件 I/O 示例。我们将编写一个程序，它打开一个文件，读取其内容，并将找到的任何元音字母更改为“#”符号。
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // Note we have to specify both in and out because we're using fstream
    std::fstream iofile{ "Sample.txt", std::ios::in | std::ios::out };

    // If we couldn't open iofile, print an error
    if (!iofile)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened!\n";
        return 1;
    }

    char chChar{}; // we're going to do this character by character

    // While there's still data to process
    while (iofile.get(chChar))
    {
        switch (chChar)
        {
            // If we find a vowel
            case 'a':
            case 'e':
            case 'i':
            case 'o':
            case 'u':
            case 'A':
            case 'E':
            case 'I':
            case 'O':
            case 'U':

                // Back up one character
                iofile.seekg(-1, std::ios::cur);

                // Because we did a seek, we can now safely do a write, so
                // let's write a # over the vowel
                iofile << '#';

                // Now we want to go back to read mode so the next call
                // to get() will perform correctly.  We'll seekg() to the current
                // location because we don't want to move the file pointer.
                iofile.seekg(iofile.tellg(), std::ios::beg);

                break;
        }
    }

    return 0;
}
运行上述程序后，我们的 Sample.txt 文件将如下所示
Th#s #s l#n# 1
Th#s #s l#n# 2
Th#s #s l#n# 3
Th#s #s l#n# 4
其他有用的文件函数
要删除文件，只需使用 remove() 函数。
此外，is_open() 函数会返回 true 如果流当前是打开的，否则返回 false。
关于将指针写入磁盘的警告
尽管将变量流式传输到文件非常容易，但当您处理指针时，事情会变得更加复杂。请记住，指针只保存其指向变量的地址。尽管可以将地址读写到磁盘，但这样做极其危险。这是因为变量的地址可能在每次执行时都不同。因此，尽管当您将变量地址写入磁盘时，它可能位于地址 0x0012FF7C，但当您将该地址读回时，它可能不再位于那里了！
例如，假设您有一个名为 nValue 的整数，它位于地址 0x0012FF7C。您将 nValue 赋值为 5。您还声明了一个名为 *pnValue 的指针，它指向 nValue。pnValue 保存着 nValue 的地址 0x0012FF7C。您想保存这些以备后用，因此您将值 5 和地址 0x0012FF7C 写入磁盘。
几周后，您再次运行程序，并从磁盘读回这些值。您将值 5 读入另一个名为 nValue 的变量，该变量位于 0x0012FF78。您将地址 0x0012FF7C 读入一个名为 *pnValue 的新指针。因为 pnValue 现在指向 0x0012FF7C，而 nValue 位于 0x0012FF78，所以 pnValue 不再指向 nValue，并且尝试访问 pnValue 将导致麻烦。
警告
不要将内存地址写入文件。当您从磁盘读回它们的值时，原来位于这些地址的变量可能位于不同的地址，并且这些地址将无效。
下一课
A.1
静态库和动态库
返回目录
上一课
28.6
基本文件 I/O