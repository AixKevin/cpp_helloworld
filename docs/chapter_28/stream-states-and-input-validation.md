# 28.5 — 流状态和输入验证

28.5 — 流状态和输入验证
Alex
2008 年 3 月 25 日，下午 3:21 (PDT)
2024 年 9 月 9 日
流状态
ios_base 类包含几个状态标志，用于指示在使用流时可能发生的各种情况
标志
含义
goodbit
一切正常
badbit
发生了一些致命错误（例如程序试图读取超出文件末尾的内容）
eofbit
流已到达文件末尾
failbit
发生了非致命错误（例如用户输入了字母，而程序期望的是整数）
尽管这些标志存在于 ios_base 中，但由于 ios 派生自 ios_base，并且 ios 比 ios_base 更少输入，因此它们通常通过 ios 访问（例如，作为 std::ios::failbit）。
ios 还提供了许多成员函数，以便方便地访问这些状态
成员函数
含义
good()
如果 goodbit 已设置，则返回 true（流正常）
bad()
如果 badbit 已设置，则返回 true（发生了致命错误）
eof()
如果 eofbit 已设置，则返回 true（流已到达文件末尾）
fail()
如果 failbit 已设置，则返回 true（发生了非致命错误）
clear()
清除所有标志并将流恢复到 goodbit 状态
clear(state)
清除所有标志并设置传入的状态标志
rdstate()
返回当前设置的标志
setstate(state)
设置传入的状态标志
最常处理的位是 failbit，当用户输入无效输入时会设置此位。例如，考虑以下程序
std::cout << "Enter your age: ";
int age {};
std::cin >> age;
请注意，此程序期望用户输入一个整数。但是，如果用户输入非数字数据，例如“Alex”，cin 将无法将任何内容提取到 age，并且 failbit 将被设置。
如果发生错误并且流设置为 goodbit 以外的任何内容，则将忽略该流上的进一步流操作。可以通过调用 clear() 函数清除此条件。
输入验证
输入验证
是检查用户输入是否满足某些标准集的过程。输入验证通常可以分为两种类型：字符串和数字。
对于字符串验证，我们接受所有用户输入作为字符串，然后根据其格式是否合适来接受或拒绝该字符串。例如，如果要求用户输入电话号码，我们可能希望确保他们输入的数据有十位数字。在大多数语言（尤其是 Perl 和 PHP 等脚本语言）中，这是通过正则表达式完成的。C++ 标准库也有一个
正则表达式库
。由于正则表达式与手动字符串验证相比速度较慢，因此只有在不关心性能（编译时和运行时）或手动验证过于繁琐时才应使用它们。
对于数字验证，我们通常关心的是确保用户输入的数字在特定范围内（例如 0 到 20 之间）。但是，与字符串验证不同，用户可能会输入根本不是数字的东西——我们也需要处理这些情况。
为了帮助我们，C++ 提供了许多有用的函数，我们可以使用它们来确定特定字符是数字还是字母。以下函数位于 cctype 头文件中
函数
含义
std::isalnum(int)
如果参数是字母或数字，则返回非零值
std::isalpha(int)
如果参数是字母，则返回非零值
std::iscntrl(int)
如果参数是控制字符，则返回非零值
std::isdigit(int)
如果参数是数字，则返回非零值
std::isgraph(int)
如果参数是可打印字符且不是空格，则返回非零值
std::isprint(int)
如果参数是可打印字符（包括空格），则返回非零值
std::ispunct(int)
如果参数既不是字母数字也不是空格，则返回非零值
std::isspace(int)
如果参数是空格，则返回非零值
std::isxdigit(int)
如果参数是十六进制数字（0-9，a-f，A-F），则返回非零值
字符串验证
让我们通过要求用户输入姓名来做一个简单的字符串验证示例。我们的验证标准是用户只能输入字母字符或空格。如果遇到其他任何字符，输入将被拒绝。
当涉及到可变长度输入时，验证字符串的最佳方法（除了使用正则表达式库）是遍历字符串的每个字符并确保其符合验证标准。这正是我们要在这里做的，或者更好的是，这就是
std::all_of
为我们所做的。
#include <algorithm> // std::all_of
#include <cctype> // std::isalpha, std::isspace
#include <iostream>
#include <ranges>
#include <string>
#include <string_view>

bool isValidName(std::string_view name)
{
  return std::ranges::all_of(name, [](char ch) {
    return std::isalpha(ch) || std::isspace(ch);
  });

  // Before C++20, without ranges
  // return std::all_of(name.begin(), name.end(), [](char ch) {
  //    return std::isalpha(ch) || std::isspace(ch);
  // });
}

int main()
{
  std::string name{};

  do
  {
    std::cout << "Enter your name: ";
    std::getline(std::cin, name); // get the entire line, including spaces
  } while (!isValidName(name));

  std::cout << "Hello " << name << "!\n";
}
请注意，此代码并不完美：用户可能会说他们的名字是“asf w jweo s di we ao”或其他一些胡言乱语，或者更糟糕的是，只是一堆空格。我们可以通过细化验证标准来解决这个问题，只接受包含至少一个字符且最多一个空格的字符串。
作者注
读者“Waldo”提供了一个 C++20 解决方案（使用 std::ranges）来解决这些缺点，请参见
此处
现在让我们看另一个示例，我们将要求用户输入他们的电话号码。与用户的姓名不同，电话号码是固定长度的，但验证标准根据字符位置而异。因此，我们将采用不同的方法来验证我们的电话号码输入。在这种情况下，我们将编写一个函数，将用户的输入与预定义的模板进行检查，以查看它是否匹配。该模板的工作方式如下
# 将匹配用户输入中的任何数字。
@ 将匹配用户输入中的任何字母字符。
_ 将匹配任何空格。
? 将匹配任何内容。
否则，用户输入和模板中的字符必须完全匹配。
因此，如果要求函数匹配模板“(###) ###-####”，这意味着我们期望用户输入一个‘(’字符、三个数字、一个‘)’字符、一个空格、三个数字、一个破折号和另外四个数字。如果其中任何一个不匹配，输入将被拒绝。
这是代码
#include <algorithm> // std::equal
#include <cctype> // std::isdigit, std::isspace, std::isalpha
#include <iostream>
#include <map>
#include <ranges>
#include <string>
#include <string_view>

bool inputMatches(std::string_view input, std::string_view pattern)
{
    if (input.length() != pattern.length())
    {
        return false;
    }

    // This table defines all special symbols that can match a range of user input
    // Each symbol is mapped to a function that determines whether the input is valid for that symbol
    static const std::map<char, int (*)(int)> validators{
      { '#', &std::isdigit },
      { '_', &std::isspace },
      { '@', &std::isalpha },
      { '?', [](int) { return 1; } }
    };

    // Before C++20, use
    // return std::equal(input.begin(), input.end(), pattern.begin(), [](char ch, char mask) -> bool {
    // ...

    return std::ranges::equal(input, pattern, [](char ch, char mask) -> bool {
        auto found{ validators.find(mask) };
        
        if (found != validators.end())
        {
            // The pattern's current element was found in the validators. Call the
            // corresponding function.
            return (*found->second)(ch);
        }

        // The pattern's current element was not found in the validators. The
        // characters have to be an exact match.
        return ch == mask;
        }); // end of lambda
}

int main()
{
    std::string phoneNumber{};

    do
    {
        std::cout << "Enter a phone number (###) ###-####: ";
        std::getline(std::cin, phoneNumber);
    } while (!inputMatches(phoneNumber, "(###) ###-####"));

    std::cout << "You entered: " << phoneNumber << '\n';
}
使用此函数，我们可以强制用户完全匹配我们指定的格式。但是，此函数仍然受到几个限制：如果 #、@、_ 和 ? 是用户输入中的有效字符，此函数将不起作用，因为这些符号已被赋予特殊含义。此外，与正则表达式不同，没有模板符号表示“可以输入可变数量的字符”。因此，此类模板不能用于确保用户输入由空格分隔的两个单词，因为它无法处理单词长度可变的事实。对于此类问题，非模板方法通常更合适。
数字验证
在处理数字输入时，显而易见的方法是使用提取运算符将输入提取到数字类型。通过检查 failbit，我们可以判断用户是否输入了数字。
让我们尝试这种方法
#include <iostream>
#include <limits>

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) // no extraction took place
        {
            std::cin.clear(); // reset the state bits back to goodbit so we can use ignore()
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // clear out the bad input from the stream
            continue; // try again
        }

        if (age <= 0) // make sure age is positive
            continue;

        break;
    }

    std::cout << "You entered: " << age << '\n';
}
如果用户输入整数，则提取将成功。std::cin.fail() 将评估为 false，跳过条件，并且（假设用户输入了正数），我们将遇到 break 语句，退出循环。
如果用户改为输入以字母开头的输入，则提取将失败。std::cin.fail() 将评估为 true，我们将进入条件。在条件块的末尾，我们将遇到 continue 语句，它将跳回 while 循环的顶部，并将再次要求用户输入。
但是，我们还没有测试另一种情况，那就是当用户输入一个以数字开头但随后包含字母的字符串时（例如“34abcd56”）。在这种情况下，开头的数字（34）将被提取到 age 中，字符串的其余部分（“abcd56”）将留在输入流中，并且 failbit 不会被设置。这会导致两个潜在问题
如果你希望这是有效输入，那么你的流中现在有垃圾。
如果你不希望这是有效输入，它不会被拒绝（并且你的流中有垃圾）。
让我们解决第一个问题。这很容易
#include <iostream>
#include <limits>

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) // no extraction took place
        {
            std::cin.clear(); // reset the state bits back to goodbit so we can use ignore()
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // clear out the bad input from the stream
            continue; // try again
        }

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // clear out any additional input from the stream

        if (age <= 0) // make sure age is positive
            continue;

      break;
    }

    std::cout << "You entered: " << age << '\n';
}
如果你不希望此类输入有效，我们将需要做一些额外的工作。幸运的是，之前的解决方案已经完成了一半。我们可以使用 gcount() 函数来确定忽略了多少个字符。如果我们的输入有效，gcount() 应该返回 1（被丢弃的换行符）。如果它返回大于 1，则用户输入了未正确提取的内容，我们应该要求他们重新输入。这是一个示例
#include <iostream>
#include <limits>

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) // no extraction took place
        {
            std::cin.clear(); // reset the state bits back to goodbit so we can use ignore()
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // clear out the bad input from the stream
            continue; // try again
        }

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // clear out any additional input from the stream
        if (std::cin.gcount() > 1) // if we cleared out more than one additional character
        {
            continue; // we'll consider this input to be invalid
        }

        if (age <= 0) // make sure age is positive
        {
            continue;
        }

        break;
    }

    std::cout << "You entered: " << age << '\n';
}
将数字验证作为字符串
上面的示例只是为了获得一个简单值就做了很多工作！处理数字输入的另一种方法是将其作为字符串读取，然后尝试将其转换为数字类型。以下程序使用了这种方法
#include <charconv> // std::from_chars
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <string_view>

// std::optional<int> returns either an int or nothing
std::optional<int> extractAge(std::string_view age)
{
    int result{};
    const auto end{ age.data() + age.length() }; // get end iterator of underlying C-style string

    // Try to parse an int from age
    // If we got an error of some kind...
    if (std::from_chars(age.data(), end, result).ec != std::errc{})
    {
        return {}; // return nothing
    }

    if (result <= 0) // make sure age is positive
    {
        return {}; // return nothing
    }

    return result; // return an int value
}

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::string strAge{};

        // Try to get a line of input
        if (!std::getline(std::cin >> std::ws, strAge))
        {
            // If we failed, clean up and try again
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');    
            continue;
        }

        // Try to extract the age
        auto extracted{ extractAge(strAge) };

        // If we failed, try again
        if (!extracted)
            continue;

        age = *extracted; // get the value
        break;
    }

  std::cout << "You entered: " << age << '\n';
}
这种方法是否比直接的数字提取更省力取决于你的验证参数和限制。
如你所见，在 C++ 中进行输入验证需要大量工作。幸运的是，许多此类任务（例如将数字验证作为字符串）可以轻松转换为函数，这些函数可以在各种情况下重复使用。
下一课
28.6
基本文件 I/O
返回目录
上一课
28.4
字符串流类