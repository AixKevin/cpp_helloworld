# 19.4 — 指向指针的指针和动态多维数组

19.4 — 指向指针的指针和动态多维数组
Alex
2015 年 9 月 14 日，下午 3:44 PDT
2024 年 9 月 9 日
本课程为可选内容，适用于希望深入学习 C++ 的高级读者。未来的课程不以此课程为基础。
指向指针的指针正如你所料：一个指针，它存储着另一个指针的地址。
指向指针的指针
一个指向 int 的普通指针使用单个星号声明
int* ptr; // pointer to an int, one asterisk
一个指向 int 指针的指针使用两个星号声明
int** ptrptr; // pointer to a pointer to an int, two asterisks
指向指针的指针就像普通指针一样工作——你可以通过解引用它来检索所指向的值。因为该值本身也是一个指针，所以你可以再次解引用它以获取底层值。这些解引用可以连续进行
int value { 5 };

int* ptr { &value };
std::cout << *ptr << '\n'; // Dereference pointer to int to get int value

int** ptrptr { &ptr };
std::cout << **ptrptr << '\n'; // dereference to get pointer to int, dereference again to get int value
上面的程序打印
5
5
请注意，你不能直接将指向指针的指针设置为值
int value { 5 };
int** ptrptr { &&value }; // not valid
这是因为取地址运算符 (operator&) 需要一个左值，但 &value 是一个右值。
然而，指向指针的指针可以设置为 null
int** ptrptr { nullptr };
指针数组
指向指针的指针有几种用途。最常见的用途是动态分配一个指针数组
int** array { new int*[10] }; // allocate an array of 10 int pointers
这与标准动态分配数组的工作方式相同，只是数组元素类型是“指向整数的指针”而不是整数。
动态分配的二维数组
指向指针的另一个常见用途是方便动态分配多维数组（有关多维数组的复习，请参阅
17.12 -- C 风格多维数组
）。
与可以轻松声明的二维固定数组不同，如下所示
int array[10][5];
动态分配二维数组要复杂一些。你可能会尝试这样做
int** array { new int[10][5] }; // won’t work!
但这行不通。
这里有两种可能的解决方案。如果最右边的数组维度是 constexpr，你可以这样做
int x { 7 }; // non-constant
int (*array)[5] { new int[x][5] }; // rightmost dimension must be constexpr
括号是必需的，以便编译器知道我们希望 `array` 是一个指向 5 个 `int` 数组的指针（在这种情况下是 7 行多维数组的第一行）。如果没有括号，编译器会将其解释为 `int* array[5]`，这是一个包含 5 个 `int*` 的数组。
这里是使用自动类型推导的好地方
int x { 7 }; // non-constant
auto array { new int[x][5] }; // so much simpler!
不幸的是，如果最右边的数组维度不是编译时常量，这种相对简单的解决方案就无效了。在这种情况下，我们必须稍微复杂一些。首先，我们分配一个指针数组（如上所述）。然后，我们遍历指针数组并为每个数组元素分配一个动态数组。我们的动态二维数组是动态的一维数组的动态一维数组！
int** array { new int*[10] }; // allocate an array of 10 int pointers — these are our rows
for (int count { 0 }; count < 10; ++count)
    array[count] = new int[5]; // these are our columns
然后我们可以像往常一样访问我们的数组
array[9][4] = 3; // This is the same as (array[9])[4] = 3;
使用这种方法，由于每个数组列都是独立动态分配的，因此可以创建非矩形的动态分配二维数组。例如，我们可以创建一个三角形数组
int** array { new int*[10] }; // allocate an array of 10 int pointers — these are our rows
for (int count { 0 }; count < 10; ++count)
    array[count] = new int[count+1]; // these are our columns
在上面的例子中，请注意 array[0] 是长度为 1 的数组，array[1] 是长度为 2 的数组，依此类推……
使用此方法解除分配动态分配的二维数组也需要一个循环
for (int count { 0 }; count < 10; ++count)
    delete[] array[count];
delete[] array; // this needs to be done last
请注意，我们按照创建数组的相反顺序删除数组（先删除元素，然后删除数组本身）。如果我们先删除数组，然后删除数组列，那么我们就必须访问已解除分配的内存来删除数组列。这将导致未定义行为。
因为分配和解除分配二维数组既复杂又容易出错，所以通常更容易将二维数组（大小为 x 乘 y）“展平”为大小为 x * y 的一维数组
// Instead of this:
int** array { new int*[10] }; // allocate an array of 10 int pointers — these are our rows
for (int count { 0 }; count < 10; ++count)
    array[count] = new int[5]; // these are our columns

// Do this
int *array { new int[50] }; // a 10x5 array flattened into a single array
然后可以使用简单的数学方法将矩形二维数组的行和列索引转换为一维数组的单个索引
int getSingleIndex(int row, int col, int numberOfColumnsInArray)
{
     return (row * numberOfColumnsInArray) + col;
}

// set array[9,4] to 3 using our flattened array
array[getSingleIndex(9, 4, 5)] = 3;
通过地址传递指针
就像我们可以使用指针参数来改变传入的底层实参的实际值一样，我们可以将指向指针的指针传递给函数，并使用该指针来改变它所指向的指针的值（你是否感到困惑？）。
然而，如果我们想让函数能够修改指针参数所指向的内容，通常更好的做法是使用对指针的引用。这在第
12.11 — 按地址传递（第二部分）
课中有所介绍。
指向指针的指针的指针…
也可以声明指向指针的指针的指针
int*** ptrx3;
这可以用来动态分配一个三维数组。然而，这样做需要循环嵌套，并且要正确实现极其复杂。
你甚至可以声明指向指针的指针的指针的指针
int**** ptrx4;
或者更高，如果你愿意。
然而，实际上这些用处不大，因为你很少需要这么多层间接。
总结
我们建议避免使用指向指针的指针，除非没有其他选择，因为它们使用起来复杂且具有潜在危险。用普通指针解引用空指针或悬空指针已经足够容易出错——用指向指针的指针则更容易出错，因为你需要双重解引用才能获得底层值！
下一课
19.5
空指针
返回目录
上一课
19.3
析构函数