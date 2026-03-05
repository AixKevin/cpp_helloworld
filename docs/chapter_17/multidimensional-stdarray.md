# 17.13 — 多维 std::array

17.13 — 多维 std::array
Alex
2023年9月11日，太平洋夏令时下午4:18
2024年6月26日
在上一课（
17.12 -- 多维 C 风格数组
）中，我们讨论了 C 风格的多维数组。
// C-style 2d array
    int arr[3][4] { 
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }};
但正如您所知，我们通常希望避免使用 C 风格数组（除非它们用于存储全局数据）。
在本课中，我们将了解多维数组如何与
std::array
一起使用。
没有标准库多维数组类
请注意，
std::array
实现为一维数组。所以您应该问的第一个问题是，“有没有一个标准库类用于多维数组？”答案是……没有。太糟糕了。呜呜呜。
一个二维
std::array
创建
std::array
的二维数组的规范方法是创建一个
std::array
，其中模板类型参数是另一个
std::array
。这会导致类似这样的代码
std::array<std::array<int, 4>, 3> arr {{  // note double braces
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};
关于这一点，有许多“有趣”的事情需要注意
初始化多维
std::array
时，我们需要使用双大括号（我们将在
17.4 -- std::array 的类类型和括号省略
一课中讨论原因）。
语法冗长且难以阅读。
由于模板嵌套的方式，数组维度是颠倒的。我们想要一个包含 3 行 4 列的数组，所以
arr[3][4]
是自然的。
std::array<std::array<int, 4>, 3>
是反向的。
索引二维
std::array
元素就像索引二维 C 风格数组一样
std::cout << arr[1][2]; // print the element in row 1, column 2
我们还可以像传递一维
std::array
一样将二维
std::array
传递给函数
#include <array>
#include <iostream>

template <typename T, std::size_t Row, std::size_t Col>
void printArray(const std::array<std::array<T, Col>, Row> &arr)
{
    for (const auto& arow: arr)   // get each array row
    {
        for (const auto& e: arow) // get each element of the row
            std::cout << e << ' ';

        std::cout << '\n';
    }
}

int main()
{
    std::array<std::array<int, 4>, 3>  arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    printArray(arr);

    return 0;
}
呸。这还是一个二维的
std::array
。三维或更高维度的
std::array
更加冗长！
使用别名模板使二维
std::array
更容易
在
10.7 -- typedefs 和类型别名
一课中，我们介绍了类型别名，并指出类型别名的一种用途是使复杂类型更易于使用。但是，对于普通的类型别名，我们必须显式指定所有模板参数。例如：
using Array2dint34 = std::array<std::array<int, 4>, 3>;
这允许我们在任何需要 3x4 二维
int
类型
std::array
的地方使用
Array2dint34
。但请注意，对于我们想要使用的每种元素类型和维度组合，我们都需要一个这样的别名！
这是一个使用别名模板的绝佳位置，它允许我们将元素类型、行长和列长指定为类型别名的模板参数！
// An alias template for a two-dimensional std::array
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;
然后我们可以使用
Array2d<int, 3, 4>
来表示任何我们想要 3x4 二维
int
类型
std::array
的地方。这好多了！
这是一个完整的例子
#include <array>
#include <iostream>

// An alias template for a two-dimensional std::array
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

// When using Array2d as a function parameter, we need to respecify the template parameters
template <typename T, std::size_t Row, std::size_t Col>
void printArray(const Array2d<T, Row, Col> &arr)
{
    for (const auto& arow: arr)   // get each array row
    {
        for (const auto& e: arow) // get each element of the row
            std::cout << e << ' ';

        std::cout << '\n';
    }
}

int main()
{
    // Define a two-dimensional array of int with 3 rows and 4 columns
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    printArray(arr);

    return 0;
}
注意这有多么简洁和易用！
我们的别名模板的一个优点是我们可以按我们喜欢的任何顺序定义模板参数。由于
std::array
首先指定元素类型，然后指定维度，我们坚持这个约定。但是我们有灵活性来首先定义
Row
或
Col
。由于 C 风格数组的定义是按行优先的，我们以
Row
在
Col
之前的顺序定义别名模板。
这种方法也很好地扩展到更高维度的
std::array
// An alias template for a three-dimensional std::array
template <typename T, std::size_t Row, std::size_t Col, std::size_t Depth>
using Array3d = std::array<std::array<std::array<T, Depth>, Col>, Row>;
获取二维数组的维度长度
对于一维
std::array
，我们可以使用
size()
成员函数（或
std::size()
）获取数组的长度。但是当有二维
std::array
时我们该怎么办呢？在这种情况下，
size()
将只返回第一维的长度。
一种看似有吸引力（但可能危险）的选择是获取所需维度的元素，然后在该元素上调用
size()
#include <array>
#include <iostream>

// An alias template for a two-dimensional std::array
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

int main()
{
    // Define a two-dimensional array of int with 3 rows and 4 columns
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    std::cout << "Rows: " << arr.size() << '\n';    // get length of first dimension (rows)
    std::cout << "Cols: " << arr[0].size() << '\n'; // get length of second dimension (cols), undefined behavior if length of first dimension is zero!

    return 0;
}
为了获取第一维的长度，我们对数组调用
size()
。为了获取第二维的长度，我们首先调用
arr[0]
获取第一个元素，然后对该元素调用
size()
。为了获取三维数组的第三维长度，我们将调用
arr[0][0].size()
。
然而，上面的代码是有缺陷的，因为如果除最后一维之外的任何维度长度为 0，它将产生未定义行为！
一个更好的选择是使用函数模板直接从关联的非类型模板参数返回维度的长度
#include <array>
#include <iostream>

// An alias template for a two-dimensional std::array
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

// Fetch the number of rows from the Row non-type template parameter
template <typename T, std::size_t Row, std::size_t Col>
constexpr int rowLength(const Array2d<T, Row, Col>&) // you can return std::size_t if you prefer
{
    return Row;
}

// Fetch the number of cols from the Col non-type template parameter
template <typename T, std::size_t Row, std::size_t Col>
constexpr int colLength(const Array2d<T, Row, Col>&) // you can return std::size_t if you prefer
{
    return Col;
}

int main()
{
    // Define a two-dimensional array of int with 3 rows and 4 columns
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    std::cout << "Rows: " << rowLength(arr) << '\n'; // get length of first dimension (rows)
    std::cout << "Cols: " << colLength(arr) << '\n'; // get length of second dimension (cols)

    return 0;
}
这避免了当任何维度长度为零时可能出现的未定义行为，因为它只使用数组的类型信息，而不是数组的实际数据。这也允许我们轻松地将长度作为
int
返回（不需要 static_cast，因为从
constexpr std::size_t
转换为
constexpr int
是非窄化转换，因此隐式转换是允许的）。
展平二维数组
具有两个或更多维度的数组存在一些挑战
它们定义和使用起来更冗长。
获取大于第一维的维度长度很尴尬。
它们越来越难以迭代（每个维度都需要多一个循环）。
使多维数组更易于使用的一种方法是展平它们。
展平
数组是减少数组维度（通常降至一维）的过程。
例如，我们可以创建一个具有
Row * Col
个元素的一维数组，而不是创建一个具有
Row
行和
Col
列的二维数组。这以一维形式提供了相同的存储量。
然而，由于我们的一维数组只有一个维度，我们无法将其作为多维数组来使用。为了解决这个问题，我们可以提供一个模仿多维数组的接口。这个接口将接受二维坐标，然后将它们映射到一维数组中的唯一位置。
这是C++11或更高版本中可行的方法示例
#include <array>
#include <iostream>
#include <functional>

// An alias template to allow us to define a one-dimensional std::array using two dimensions
template <typename T, std::size_t Row, std::size_t Col>
using ArrayFlat2d = std::array<T, Row * Col>;

// A modifiable view that allows us to work with an ArrayFlat2d using two dimensions
// This is a view, so the ArrayFlat2d being viewed must stay in scope
template <typename T, std::size_t Row, std::size_t Col>
class ArrayView2d
{
private:
    // You might be tempted to make m_arr a reference to an ArrayFlat2d,
    // but this makes the view non-copy-assignable since references can't be reseated.
    // Using std::reference_wrapper gives us reference semantics and copy assignability.
    std::reference_wrapper<ArrayFlat2d<T, Row, Col>> m_arr {};

public:
    ArrayView2d(ArrayFlat2d<T, Row, Col> &arr)
        : m_arr { arr }
    {}

    // Get element via single subscript (using operator[])
    T& operator[](int i) { return m_arr.get()[static_cast<std::size_t>(i)]; }
    const T& operator[](int i) const { return m_arr.get()[static_cast<std::size_t>(i)]; }

    // Get element via 2d subscript (using operator(), since operator[] doesn't support multiple dimensions prior to C++23)
    T& operator()(int row, int col) { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }
    const T& operator()(int row, int col) const { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }

    // in C++23, you can uncomment these since multidimensional operator[] is supported
//    T& operator[](int row, int col) { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }
//    const T& operator[](int row, int col) const { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }

    int rows() const { return static_cast<int>(Row); }
    int cols() const { return static_cast<int>(Col); }
    int length() const { return static_cast<int>(Row * Col); }
};

int main()
{
    // Define a one-dimensional std::array of int (with 3 rows and 4 columns)
    ArrayFlat2d<int, 3, 4> arr {
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12 };

    // Define a two-dimensional view into our one-dimensional array
    ArrayView2d<int, 3, 4> arrView { arr };

    // print array dimensions
    std::cout << "Rows: " << arrView.rows() << '\n';
    std::cout << "Cols: " << arrView.cols() << '\n';

    // print array using a single dimension
    for (int i=0; i < arrView.length(); ++i)
        std::cout << arrView[i] << ' ';

    std::cout << '\n';

    // print array using two dimensions
    for (int row=0; row < arrView.rows(); ++row)
    {
        for (int col=0; col < arrView.cols(); ++col)
            std::cout << arrView(row, col) << ' ';
        std::cout << '\n';
    }

    std::cout << '\n';

    return 0;
}
这会打印
Rows: 3
Cols: 4
1 2 3 4 5 6 7 8 9 10 11 12
1 2 3 4
5 6 7 8
9 10 11 12
由于在 C++23 之前
operator[]
只能接受一个下标，因此有两种替代方法
改用
operator()
，它可以接受多个下标。这允许您将
[]
用于单索引索引，将
()
用于多维索引。我们上面选择了这种方法。
让
operator[]
返回一个也重载
operator[]
的子视图，以便您可以链式使用
operator[]
。这更复杂，并且不能很好地扩展到更高维度。
在 C++23 中，
operator[]
已扩展为接受多个下标，因此您可以重载它以处理单个和多个下标（而不是使用
operator()
来处理多个下标）。
相关内容
我们将在
17.5 -- 通过 std::reference_wrapper 实现引用数组
一课中介绍
std::reference_wrapper
。
std::mdspan
C++23
std::mdspan
在 C++23 中引入，它是一个可修改的视图，为连续的元素序列提供多维数组接口。通过可修改视图，我们的意思是
std::mdspan
不仅仅是只读视图（如
std::string_view
）——如果底层元素序列不是 const，则这些元素可以被修改。
以下示例打印与前一个示例相同的输出，但使用
std::mdspan
而不是我们自己的自定义视图
#include <array>
#include <iostream>
#include <mdspan>

// An alias template to allow us to define a one-dimensional std::array using two dimensions
template <typename T, std::size_t Row, std::size_t Col>
using ArrayFlat2d = std::array<T, Row * Col>;

int main()
{
    // Define a one-dimensional std::array of int (with 3 rows and 4 columns)
    ArrayFlat2d<int, 3, 4> arr {
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12 };

    // Define a two-dimensional span into our one-dimensional array
    // We must pass std::mdspan a pointer to the sequence of elements
    // which we can do via the data() member function of std::array or std::vector
    std::mdspan mdView { arr.data(), 3, 4 };

    // print array dimensions
    // std::mdspan calls these extents
    std::size_t rows { mdView.extents().extent(0) };
    std::size_t cols { mdView.extents().extent(1) };
    std::cout << "Rows: " << rows << '\n';
    std::cout << "Cols: " << cols << '\n';

    // print array in 1d
    // The data_handle() member gives us a pointer to the sequence of elements
    // which we can then index
    for (std::size_t i=0; i < mdView.size(); ++i)
        std::cout << mdView.data_handle()[i] << ' ';
    std::cout << '\n';

    // print array in 2d
    // We use multidimensional [] to access elements
    for (std::size_t row=0; row < rows; ++row)
    {
        for (std::size_t col=0; col < cols; ++col)
            std::cout << mdView[row, col] << ' ';
        std::cout << '\n';
    }
    std::cout << '\n';

    return 0;
}
这应该相当简单，但有几点值得注意
std::mdspan
允许我们定义任意维度的视图。
std::mdspan
构造函数的第一个参数应该是指向数组数据的指针。这可以是退化的 C 风格数组，或者我们可以使用
std::array
或
std::vector
的
data()
成员函数来获取此数据。
要在一维中索引
std::mdspan
，我们必须获取指向数组数据的指针，这可以通过
data_handle()
成员函数完成。然后我们可以对它进行下标操作。
在 C++23 中，
operator[]
接受多个索引，所以我们使用
[row, col]
作为索引而不是
[row][col]
。
C++26 将包含
std::mdarray
，它本质上将
std::array
和
std::mdspan
组合成一个拥有的多维数组！
下一课
17.x
第17章 总结和测验
返回目录
上一课
17.12
多维 C 风格数组