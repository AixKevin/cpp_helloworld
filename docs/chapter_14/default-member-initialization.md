# 13.9 — 默认成员初始化

13.9 — 默认成员初始化
Alex
2022 年 1 月 18 日，上午 10:24 PST
2024 年 9 月 16 日
当我们定义一个结构体（或类）类型时，我们可以为每个成员提供一个默认的初始化值，作为类型定义的一部分。对于未标记为
static
的成员，这个过程有时被称为
非静态成员初始化
。初始化值被称为
默认成员初始化器
。
相关内容
我们在课程
15.6 -- 静态成员变量
中讨论静态成员和静态成员初始化。
这是一个例子
struct Something
{
    int x;       // no initialization value (bad)
    int y {};    // value-initialized by default
    int z { 2 }; // explicit default value
};

int main()
{
    Something s1; // s1.x is uninitialized, s1.y is 0, and s1.z is 2

    return 0;
}
在上面的
Something
定义中，
x
没有默认值，
y
默认进行值初始化，
z
的默认值为
2
。当用户在实例化
Something
类型的对象时没有提供显式初始化值时，将使用这些默认成员初始化值。
我们的
s1
对象没有初始化器，因此
s1
的成员被初始化为它们的默认值。
s1.x
没有默认初始化器，因此它保持未初始化。
s1.y
默认进行值初始化，因此它获得值
0
。而
s1.z
用值
2
初始化。
请注意，尽管我们没有为
s1.z
提供显式初始化器，但由于提供了默认成员初始化器，它被初始化为一个非零值。
关键见解
使用默认成员初始化器（或我们稍后将介绍的其他机制），结构体和类即使在没有提供显式初始化器的情况下也能自初始化！
致进阶读者
CTAD（我们将在课程
13.14 -- 类模板参数推导 (CTAD) 和推导指南
中介绍）不能用于非静态成员初始化。
显式初始化值优先于默认值
列表初始化器中的显式值总是优先于默认成员初始化值。
struct Something
{
    int x;       // no default initialization value (bad)
    int y {};    // value-initialized by default
    int z { 2 }; // explicit default value
};

int main()
{
    Something s2 { 5, 6, 7 }; // use explicit initializers for s2.x, s2.y, and s2.z (no default values are used)
   
    return 0;
}
在上述情况下，
s2
为每个成员都有显式初始化值，因此完全不使用默认成员初始化值。这意味着
s2.x
、
s2.y
和
s2.z
分别初始化为值
5
、
6
和
7
。
存在默认值时初始化列表中缺少初始化器
在上一课 (
13.8 -- 结构体聚合初始化
) 中，我们注意到，如果一个聚合被初始化，但初始化值的数量少于成员的数量，那么所有剩余的成员都将进行值初始化。但是，如果为给定成员提供了默认成员初始化器，则将使用该默认成员初始化器。
struct Something
{
    int x;       // no default initialization value (bad)
    int y {};    // value-initialized by default
    int z { 2 }; // explicit default value
};

int main()
{
    Something s3 {}; // value initialize s3.x, use default values for s3.y and s3.z
   
    return 0;
}
在上述情况下，
s3
用空列表进行列表初始化，因此所有初始化器都缺失。这意味着如果存在默认成员初始化器，则将使用它，否则将进行值初始化。因此，
s3.x
（没有默认成员初始化器）进行值初始化为
0
，
s3.y
默认进行值初始化为
0
，而
s3.z
默认值为
2
。
初始化可能性的总结
如果聚合用初始化列表定义
如果存在显式初始化值，则使用该显式值。
如果初始化器缺失且存在默认成员初始化器，则使用默认值。
如果初始化器缺失且不存在默认成员初始化器，则进行值初始化。
如果聚合没有初始化列表定义
如果存在默认成员初始化器，则使用默认值。
如果不存在默认成员初始化器，则成员保持未初始化。
成员总是按声明顺序初始化。
以下示例总结了所有可能性
struct Something
{
    int x;       // no default initialization value (bad)
    int y {};    // value-initialized by default
    int z { 2 }; // explicit default value
};

int main()
{
    Something s1;             // No initializer list: s1.x is uninitialized, s1.y and s1.z use defaults
    Something s2 { 5, 6, 7 }; // Explicit initializers: s2.x, s2.y, and s2.z use explicit values (no default values are used)
    Something s3 {};          // Missing initializers: s3.x is value initialized, s3.y and s3.z use defaults
   
    return 0;
}
我们需要注意的情况是
s1.x
。因为
s1
没有初始化列表，并且
x
没有默认成员初始化器，所以
s1.x
保持未初始化（这很糟糕，因为我们应该总是初始化我们的变量）。
总是为您的成员提供默认值
为了避免未初始化成员的可能性，只需确保每个成员都有一个默认值（无论是显式默认值还是空大括号对）。这样，无论我们是否提供初始化列表，我们的成员都将以某个值初始化。
考虑以下结构体，其所有成员都已默认化
struct Fraction
{
	int numerator { }; // we should use { 0 } here, but for the sake of example we'll use value initialization instead
	int denominator { 1 };
};

int main()
{
	Fraction f1;          // f1.numerator value initialized to 0, f1.denominator defaulted to 1
	Fraction f2 {};       // f2.numerator value initialized to 0, f2.denominator defaulted to 1
	Fraction f3 { 6 };    // f3.numerator initialized to 6, f3.denominator defaulted to 1
	Fraction f4 { 5, 8 }; // f4.numerator initialized to 5, f4.denominator initialized to 8

	return 0;
}
在所有情况下，我们的成员都用值初始化。
最佳实践
为所有成员提供默认值。这确保了即使变量定义不包含初始化列表，您的成员也将被初始化。
聚合的默认初始化与值初始化
重新审视上述示例中的两行代码
Fraction f1;          // f1.numerator value initialized to 0, f1.denominator defaulted to 1
	Fraction f2 {};       // f2.numerator value initialized to 0, f2.denominator defaulted to 1
您会注意到
f1
是默认初始化的，而
f2
是值初始化的，但结果是相同的（
numerator
初始化为
0
，
denominator
初始化为
1
）。那么我们应该选择哪种呢？
值初始化（
f2
）的情况更安全，因为它将确保任何没有默认值的成员都进行值初始化（尽管我们应该始终为成员提供默认值，但这可以防止遗漏的情况）。
偏好值初始化还有一个好处——它与我们初始化其他类型对象的方式保持一致。一致性有助于防止错误。
最佳实践
对于聚合，首选值初始化（使用空大括号初始化器）而不是默认初始化（不使用大括号）。
尽管如此，程序员使用默认初始化而不是值初始化来初始化类类型并不少见。这部分是出于历史原因（因为值初始化直到 C++11 才引入），部分是因为在特定情况下（对于非聚合），默认初始化可能比值初始化更高效（我们在课程
14.11 -- 默认构造函数和默认参数
中介绍了这种情况）。
因此，在这些教程中，我们不会强制要求对结构体和类使用值初始化，但我们强烈推荐它。
下一课
13.10
传递和返回结构体
返回目录
上一课
13.8
结构体聚合初始化