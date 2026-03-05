#include <iostream>
#include <string>
#include <string_view>
/**
 * getQuantityPhrase() 应该接受一个表示某物数量的单个 int 参数，并返回以下描述符
    < 0 = “负数”
    0 = “无”
    1 = “一个”
    2 = “几个”
    3 = “一些”
    > 3 = “许多”
    getApplesPluralized() 应该接受一个表示苹果数量的单个 int 参数，并返回以下内容

    1 = “apple”
    否则 = “apples”
 */

// Write the function getQuantityPhrase() here
std::string_view getQuantityPhrase(int quantity)
{
    if (quantity < 0)
    {
        return "negetive";
    }
    else if (!quantity)
    {
        return "none";
    }
    else if (quantity == 1)
    {
        return "a";
    }
    else if (quantity == 2)
    {
        return "some";
    }
    else if (quantity == 3)
    {
        return "a few";
    }
    else
    {
        return "many";
    }
}

// Write the function getApplesPluralized() here
std::string_view getApplesPluralized(int plur)
{
    return (plur - 1) ? "apples" : "apple";
}

int main()
{
    constexpr int maryApples{3};
    std::cout << "Mary has " << getQuantityPhrase(maryApples) << ' ' << getApplesPluralized(maryApples) << ".\n";

    std::cout << "How many apples do you have? ";
    int numApples{};
    std::cin >> numApples;

    std::cout << "You have " << getQuantityPhrase(numApples) << ' ' << getApplesPluralized(numApples) << ".\n";

    return 0;
}
