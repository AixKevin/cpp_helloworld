# 13.10 — 传递和返回结构体

13.10 — 传递和返回结构体
Alex
2022年1月18日，太平洋标准时间上午10:24
2024年11月29日
考虑一个由3个松散变量表示的员工
int main()
{
    int id { 1 };
    int age { 24 };
    double wage { 52400.0 };

    return 0;
}
如果我们要将此员工传递给函数，我们必须传递三个变量
#include <iostream>

void printEmployee(int id, int age, double wage)
{
    std::cout << "ID:   " << id << '\n';
    std::cout << "Age:  " << age << '\n';
    std::cout << "Wage: " << wage << '\n';
}

int main()
{
    int id { 1 };
    int age { 24 };
    double wage { 52400.0 };

    printEmployee(id, age, wage);

    return 0;
}
虽然传递3个独立的员工变量还不算太糟，但考虑一个需要传递10或12个员工变量的函数。独立传递每个变量将耗时且容易出错。此外，如果将来我们为员工添加新属性（例如姓名），我们现在必须修改所有函数声明、定义和函数调用以接受新参数和实参！
传递结构体（通过引用）
与独立变量相比，使用结构体的一个巨大优势是我们可以将整个结构体传递给需要处理成员的函数。结构体通常通过引用（通常是const引用）传递，以避免创建副本。
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

void printEmployee(const Employee& employee) // note pass by reference here
{
    std::cout << "ID:   " << employee.id << '\n';
    std::cout << "Age:  " << employee.age << '\n';
    std::cout << "Wage: " << employee.wage << '\n';
}

int main()
{
    Employee joe { 14, 32, 24.15 };
    Employee frank { 15, 28, 18.27 };

    // Print Joe's information
    printEmployee(joe);

    std::cout << '\n';

    // Print Frank's information
    printEmployee(frank);

    return 0;
}
在上面的例子中，我们将整个
Employee
传递给
printEmployee()
（两次，一次用于
joe
，一次用于
frank
）。
上述程序输出
ID:   14
Age:  32
Wage: 24.15

ID:   15
Age:  28
Wage: 18.27
因为我们传递的是整个结构体对象（而不是单个成员），所以无论结构体对象有多少成员，我们都只需要一个参数。而且，将来，如果我们决定向
Employee
结构体添加新成员，我们将无需更改函数声明或函数调用！新成员将自动包含在内。
相关内容
我们将在课程
12.6 -- 通过const左值引用传递
中讨论何时按值或按引用传递结构体。
传递临时结构体
在前面的例子中，我们在将Employee变量
joe
传递给
printEmployee()
函数之前创建了它。这允许我们给Employee变量一个名称，这对于文档目的很有用。但这也需要两条语句（一条用于创建
joe
，一条用于使用
joe
）。
在只使用变量一次的情况下，必须给变量一个名称并将变量的创建和使用分开，这会增加复杂性。在这种情况下，最好使用临时对象。临时对象不是变量，因此它没有标识符。
以下是上面的相同示例，但我们用临时对象替换了变量
joe
和
frank
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

void printEmployee(const Employee& employee) // note pass by reference here
{
    std::cout << "ID:   " << employee.id << '\n';
    std::cout << "Age:  " << employee.age << '\n';
    std::cout << "Wage: " << employee.wage << '\n';
}

int main()
{
    // Print Joe's information
    printEmployee(Employee { 14, 32, 24.15 }); // construct a temporary Employee to pass to function (type explicitly specified) (preferred)

    std::cout << '\n';

    // Print Frank's information
    printEmployee({ 15, 28, 18.27 }); // construct a temporary Employee to pass to function (type deduced from parameter)

    return 0;
}
我们可以通过两种方式创建临时
Employee
。在第一次调用中，我们使用语法
Employee { 14, 32, 24.15 }
。这告诉编译器创建一个
Employee
对象并使用提供的初始化程序对其进行初始化。这是首选语法，因为它清楚地说明了我们正在创建哪种临时对象，并且编译器不可能误解我们的意图。
在第二次调用中，我们使用语法
{ 15, 28, 18.27 }
。编译器足够智能，可以理解提供的参数必须转换为
Employee
，以便函数调用成功。请注意，这种形式被认为是隐式转换，因此在只接受显式转换的情况下它不起作用。
相关内容
我们将在课程
14.13 -- 临时类对象
中讨论更多关于类类型临时对象和转换的内容。
关于临时对象的几点说明：它们在定义时创建并初始化，并在创建它们的完整表达式结束时销毁。临时对象的求值是一个右值表达式，它只能用于接受右值的地方。当临时对象用作函数参数时，它只绑定到接受右值的参数。这包括按值传递和按const引用传递，不包括按非const引用传递和按地址传递。
返回结构体
考虑这样一种情况：我们有一个函数需要返回三维笛卡尔空间中的一个点。这样的点有3个属性：x坐标、y坐标和z坐标。但是函数只能返回一个值。那么我们如何将所有3个坐标返回给用户呢？
一种常见的方法是返回一个结构体
#include <iostream>

struct Point3d
{
    double x { 0.0 };
    double y { 0.0 };
    double z { 0.0 };
};

Point3d getZeroPoint()
{
    // We can create a variable and return the variable (we'll improve this below)
    Point3d temp { 0.0, 0.0, 0.0 };
    return temp;
}

int main()
{
    Point3d zero{ getZeroPoint() };

    if (zero.x == 0.0 && zero.y == 0.0 && zero.z == 0.0)
        std::cout << "The point is zero\n";
    else
        std::cout << "The point is not zero\n";

    return 0;
}
这会打印
The point is zero
函数内部定义的结构体通常按值返回，以免返回悬空引用。
在上面的
getZeroPoint()
函数中，我们创建了一个新的命名对象（
temp
），仅仅是为了返回它
Point3d getZeroPoint()
{
    // We can create a variable and return the variable (we'll improve this below)
    Point3d temp { 0.0, 0.0, 0.0 };
    return temp;
}
这里对象名（
temp
）并没有提供任何文档价值。
我们可以通过返回一个临时（未命名/匿名）对象来稍微改进我们的函数
Point3d getZeroPoint()
{
    return Point3d { 0.0, 0.0, 0.0 }; // return an unnamed Point3d
}
在这种情况下，会构造一个临时`Point3d`，将其复制回调用者，然后在表达式结束时销毁。注意这有多么简洁（一行而不是两行，并且无需理解`temp`是否被多次使用）。
相关内容
我们将在课程
14.13 -- 临时类对象
中更详细地讨论匿名对象。
推导返回类型
在函数具有显式返回类型（例如
Point3d
）的情况下，我们甚至可以在return语句中省略类型
Point3d getZeroPoint()
{
    // We already specified the type at the function declaration
    // so we don't need to do so here again
    return { 0.0, 0.0, 0.0 }; // return an unnamed Point3d
}
这被认为是隐式转换。
还要注意，由于在这种情况下我们返回所有零值，我们可以使用空大括号来返回一个值初始化的 Point3d
Point3d getZeroPoint()
{
    // We can use empty curly braces to value-initialize all members
    return {};
}
结构体是重要的构建块
虽然结构体本身很有用，但类（C++和面向对象编程的核心）直接建立在我们在此处介绍的概念之上。对结构体（尤其是数据成员、成员选择和默认成员初始化）有很好的理解将使您更容易过渡到类。
小测验时间
问题 #1
您正在运营一个网站，并且正在尝试计算您的广告收入。编写一个程序，允许您输入3条数据
观看了多少广告。
点击广告的用户百分比。
每次点击广告的平均收益。
将这3个值存储在一个结构体中。将该结构体传递给另一个函数，该函数打印每个值。打印函数还应该打印您当天赚了多少钱（将3个字段相乘）。
显示提示
提示：如果您将百分比存储为整数，那么在计算您当天赚了多少钱时，您还需要除以100。
显示答案
#include <iostream>

// First we need to define our Advertising struct
struct Advertising
{
    int adsShown {};
    double clickThroughRatePercentage {};
    double averageEarningsPerClick {};
};

Advertising getAdvertising()
{
    Advertising temp {};
    std::cout << "How many ads were shown today? ";
    std::cin >> temp.adsShown;
    std::cout << "What percentage of ads were clicked on by users? ";
    std::cin >> temp.clickThroughRatePercentage;
    std::cout << "What was the average earnings per click? ";
    std::cin >> temp.averageEarningsPerClick;

    return temp;
}

void printAdvertising(const Advertising& ad)
{
    std::cout << "Number of ads shown: " << ad.adsShown << '\n';
    std::cout << "Click through rate: " << ad.clickThroughRatePercentage << '\n';
    std::cout << "Average earnings per click: $" << ad.averageEarningsPerClick << '\n';

    // The following line is split up to reduce the length
    // We need to divide ad.clickThroughRatePercentage by 100 because it's a percent of 100, not a multiplier
    std::cout << "Total Earnings: $"
        << (ad.adsShown * ad.clickThroughRatePercentage / 100 * ad.averageEarningsPerClick) << '\n';
}

int main()
{
    // Declare an Advertising struct variable
    Advertising ad{ getAdvertising() };
    printAdvertising(ad);

    return 0;
}
问题 #2
创建一个结构体来存储一个分数。该结构体应具有一个整数分子成员和一个整数分母成员。
编写一个函数从用户那里读取一个Fraction，并使用它读取两个Fraction对象。编写另一个函数将两个Fraction相乘并以Fraction形式返回结果（您不需要约分）。编写另一个函数打印一个Fraction。
你的程序输出应与以下匹配
Enter a value for the numerator: 1
Enter a value for the denominator: 2

Enter a value for the numerator: 3
Enter a value for the denominator: 4

Your fractions multiplied together: 3/8
将两个分数相乘时，结果的分子是两个分子的乘积，结果的分母是两个分母的乘积。
显示答案
#include <iostream>

struct Fraction
{
    int numerator{ 0 };
    int denominator{ 1 };
};

Fraction getFraction()
{
    Fraction temp{};
    std::cout << "Enter a value for numerator: ";
    std::cin >> temp.numerator;
    std::cout << "Enter a value for denominator: ";
    std::cin >> temp.denominator;
    std::cout << '\n';

    return temp;
}

constexpr Fraction multiply(const Fraction& f1, const Fraction& f2)
{
    return { f1.numerator * f2.numerator, f1.denominator * f2.denominator };
}

void printFraction(const Fraction& f)
{
    std::cout << f.numerator << '/' << f.denominator << '\n';
}

int main()
{
    Fraction f1{ getFraction() };
    Fraction f2{ getFraction() };

    std::cout << "Your fractions multiplied together: ";

    printFraction(multiply(f1, f2));

    return 0;
}
问题 #3
在前面测验问题的解决方案中，为什么
getFraction()
按值返回而不是按引用返回？
显示答案
因为我们的
temp
Fraction是局部变量，它将在函数结束时超出作用域。如果我们以引用形式返回
temp
，我们将向调用者返回一个悬空引用。
下一课
13.11
结构体杂项
返回目录
上一课
13.9
默认成员初始化