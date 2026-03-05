# 23.6 — 容器类

23.6 — 容器类
Alex
2007年12月14日，太平洋标准时间下午4:54
2024年12月30日
在现实生活中，我们一直都在使用容器。你的早餐麦片装在盒子里，你的书页装在封面和装订中，你可能会把许多物品储存在车库的容器里。没有容器，处理这些对象会极其不便。想象一下，如果一本书没有任何装订，或者没有盒子装着麦片，而你也没有用碗，那会是多么混乱。容器的价值主要在于它能够帮助组织和存储放入其中的物品。
同样地，
容器类
是一个旨在容纳和组织另一种类型（可以是另一个类，也可以是基本类型）的多个实例的类。容器类有许多不同种类，每种都有其优点、缺点和使用限制。到目前为止，编程中最常用的容器是数组，你已经见过许多示例。尽管 C++ 内置了数组功能，但程序员通常会使用数组容器类（std::array 或 std::vector）来代替，因为它们提供了额外的优势。与内置数组不同，数组容器类通常提供动态调整大小（当添加或移除元素时）、在传递给函数时记住其大小，并进行边界检查。这不仅使数组容器类比普通数组更方便，也更安全。
容器类通常实现一套相当标准化的最小功能集。大多数定义良好的容器将包含以下函数：
通过构造函数创建一个空容器
向容器中插入一个新对象
从容器中移除一个对象
报告容器中当前对象的数量
清空容器中的所有对象
提供对存储对象的访问
对元素进行排序（可选）
有时某些容器类会省略一些功能。例如，数组容器类通常会省略插入和移除函数，因为它们速度慢，并且类设计者不希望鼓励使用它们。
容器类实现了“成员关系”。例如，数组的元素是数组的“成员”（属于数组）。请注意，我们这里使用的是“成员”的常规意义，而不是 C++ 类成员的意义。
容器的类型
容器类通常有两种不同的变体。
值容器
是
组合
，它们存储所持对象的副本（因此负责创建和销毁这些副本）。
引用容器
是
聚合
，它们存储指向其他对象的指针或引用（因此不负责这些对象的创建或销毁）。
与现实生活中容器可以容纳任何类型的对象不同，在 C++ 中，容器通常只容纳一种数据类型。例如，如果你有一个整数数组，它将只容纳整数。与某些其他语言不同，许多 C++ 容器不允许你任意混合类型。如果你需要容器来容纳整数和双精度浮点数，你通常必须编写两个单独的容器来完成此操作（或者使用模板，这是一个高级 C++ 功能）。尽管有使用限制，但容器非常有用，它们使编程更容易、更安全、更快。
一个数组容器类
在这个例子中，我们将从头开始编写一个整数数组类，它实现容器应该具有的大多数常见功能。这个数组类将是一个值容器，它将存储它所组织元素的副本。顾名思义，该容器将容纳一个整数数组，类似于
std::vector<int>
。
首先，我们创建 IntArray.h 文件
#ifndef INTARRAY_H
#define INTARRAY_H

class IntArray
{
};

#endif
我们的 IntArray 将需要跟踪两个值：数据本身和数组的大小。因为我们希望我们的数组能够改变大小，所以我们必须进行一些动态分配，这意味着我们必须使用指针来存储数据。
#ifndef INTARRAY_H
#define INTARRAY_H

class IntArray
{
private:
    int m_length{};
    int* m_data{};
};

#endif
现在我们需要添加一些构造函数，它们将允许我们创建 IntArrays。我们将添加两个构造函数：一个构造空数组，一个允许我们构造预定大小的数组。
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert> // for assert()
#include <cstddef> // for std::size_t

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[static_cast<std::size_t>(length)]{};
    }
};

#endif
我们还需要一些函数来帮助我们清理 IntArrays。首先，我们将编写一个析构函数，它只释放任何动态分配的数据。其次，我们将编写一个名为 erase() 的函数，它将擦除数组并将长度设置为 0。
~IntArray()
    {
        delete[] m_data;
        // we don't need to set m_data to null or m_length to 0 here, since the object will be destroyed immediately after this function anyway
    }

    void erase()
    {
        delete[] m_data;

        // We need to make sure we set m_data to nullptr here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }
现在让我们重载 [] 运算符，以便我们可以访问数组的元素。我们应该确保索引参数具有有效值，这可以通过使用 assert() 函数来完成。我们还将添加一个访问函数来返回数组的长度。这是目前为止的所有内容：
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert> // for assert()
#include <cstddef> // for std::size_t

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[static_cast<std::size_t>(length)]{};
    }

    ~IntArray()
    {
        delete[] m_data;
        // we don't need to set m_data to null or m_length to 0 here, since the object will be destroyed immediately after this function anyway
    }

    void erase()
    {
        delete[] m_data;
        // We need to make sure we set m_data to nullptr here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
此时，我们已经有了一个可以使用的 IntArray 类。我们可以分配给定大小的 IntArrays，并且可以使用 [] 运算符检索或更改元素的值。
然而，我们的 IntArray 仍然有一些事情做不到。我们仍然不能改变它的大小，仍然不能插入或删除元素，并且我们仍然不能对其进行排序。复制数组也会导致问题，因为它会浅复制数据指针。
首先，让我们编写一些代码，允许我们调整数组的大小。我们将编写两个不同的函数来完成此操作。第一个函数 reallocate() 在调整大小时会销毁数组中任何现有元素，但它会很快。第二个函数 resize() 在调整大小时会保留数组中任何现有元素，但它会很慢。
#include <algorithm> // for std::copy_n

    // reallocate resizes the array.  Any existing elements will be destroyed.  This function operates quickly.
    void reallocate(int newLength)
    {
        // First we delete any existing elements
        erase();

        // If our array is going to be empty now, return here
        if (newLength <= 0)
            return;

        // Then we have to allocate new elements
        m_data = new int[static_cast<std::size_t>(newLength)];
        m_length = newLength;
    }

    // resize resizes the array.  Any existing elements will be kept.  This function operates slowly.
    void resize(int newLength)
    {
        // if the array is already the right length, we're done
        if (newLength == m_length)
            return;

        // If we are resizing to an empty array, do that and return
        if (newLength <= 0)
        {
            erase();
            return;
        }

        // Now we can assume newLength is at least 1 element.  This algorithm
        // works as follows: First we are going to allocate a new array.  Then we
        // are going to copy elements from the existing array to the new array.
        // Once that is done, we can destroy the old array, and make m_data
        // point to the new array.

        // First we have to allocate a new array
        int* data{ new int[static_cast<std::size_t>(newLength)] };

        // Then we have to figure out how many elements to copy from the existing
        // array to the new array.  We want to copy as many elements as there are
        // in the smaller of the two arrays.
        if (m_length > 0)
        {
            int elementsToCopy{ (newLength > m_length) ? m_length : newLength };
            std::copy_n(m_data, elementsToCopy, data); // copy the elements
        }
 
        // Now we can delete the old array because we don't need it any more
        delete[] m_data;

        // And use the new array instead!  Note that this simply makes m_data point
        // to the same address as the new array we dynamically allocated.  Because
        // data was dynamically allocated, it won't be destroyed when it goes out of scope.
        m_data = data;
        m_length = newLength;
    }
呼！这有点棘手！
我们还要添加一个复制构造函数和赋值运算符，以便我们可以复制数组。
IntArray(const IntArray& a): IntArray(a.getLength()) // use normal constructor to set size of array appropriately
    {
        std::copy_n(a.m_data, m_length, m_data); // copy the elements
    }

    IntArray& operator=(const IntArray& a)
    {
        // Self-assignment check
        if (&a == this)
            return *this;

        // Set the size of the new array appropriately
        reallocate(a.getLength());
        std::copy_n(a.m_data, m_length, m_data); // copy the elements

        return *this;
    }
许多数组容器类到此为止。然而，万一您想看看如何实现插入和删除功能，我们也会继续编写这些。这两个算法都与 resize() 非常相似。
void insertBefore(int value, int index)
    {
        // Sanity check our index value
        assert(index >= 0 && index <= m_length);

        // First create a new array one element larger than the old array
        int* data{ new int[static_cast<std::size_t>(m_length+1)] };

        // Copy all of the elements up to the index
        std::copy_n(m_data, index, data); 

        // Insert our new element into the new array
        data[index] = value;

        // Copy all of the values after the inserted element
        std::copy_n(m_data + index, m_length - index, data + index + 1);

        // Finally, delete the old array, and use the new array instead
        delete[] m_data;
        m_data = data;
        ++m_length;
    }

    void remove(int index)
    {
        // Sanity check our index value
        assert(index >= 0 && index < m_length);

        // If this is the last remaining element in the array, set the array to empty and bail out
        if (m_length == 1)
        {
            erase();
            return;
        }

        // First create a new array one element smaller than the old array
        int* data{ new int[static_cast<std::size_t>(m_length-1)] };

        // Copy all of the elements up to the index
        std::copy_n(m_data, index, data); 

        // Copy all of the values after the removed element
        std::copy_n(m_data + index + 1, m_length - index - 1, data + index); 

        // Finally, delete the old array, and use the new array instead
        delete[] m_data;
        m_data = data;
        --m_length;
    }
这是我们完整的 IntArray 容器类。
IntArray.h
#ifndef INTARRAY_H
#define INTARRAY_H

#include <algorithm> // for std::copy_n
#include <cassert> // for assert()
#include <cstddef> // for std::size_t

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[static_cast<std::size_t>(length)]{};
    }

    ~IntArray()
    {
        delete[] m_data;
        // we don't need to set m_data to null or m_length to 0 here, since the object will be destroyed immediately after this function anyway
    }

    IntArray(const IntArray& a): IntArray(a.getLength()) // use normal constructor to set size of array appropriately
    {
        std::copy_n(a.m_data, m_length, m_data); // copy the elements
    }

    IntArray& operator=(const IntArray& a)
    {
        // Self-assignment check
        if (&a == this)
            return *this;

        // Set the size of the new array appropriately
        reallocate(a.getLength());
        std::copy_n(a.m_data, m_length, m_data); // copy the elements

        return *this;
    }

    void erase()
    {
        delete[] m_data;
        // We need to make sure we set m_data to nullptr here, otherwise it will
        // be left pointing at deallocated memory!
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }


    // reallocate resizes the array.  Any existing elements will be destroyed.  This function operates quickly.
    void reallocate(int newLength)
    {
        // First we delete any existing elements
        erase();

        // If our array is going to be empty now, return here
        if (newLength <= 0)
            return;

        // Then we have to allocate new elements
        m_data = new int[static_cast<std::size_t>(newLength)];
        m_length = newLength;
    }

    // resize resizes the array.  Any existing elements will be kept.  This function operates slowly.
    void resize(int newLength)
    {
        // if the array is already the right length, we're done
        if (newLength == m_length)
            return;

        // If we are resizing to an empty array, do that and return
        if (newLength <= 0)
        {
            erase();
            return;
        }

        // Now we can assume newLength is at least 1 element.  This algorithm
        // works as follows: First we are going to allocate a new array.  Then we
        // are going to copy elements from the existing array to the new array.
        // Once that is done, we can destroy the old array, and make m_data
        // point to the new array.

        // First we have to allocate a new array
        int* data{ new int[static_cast<std::size_t>(newLength)] };

        // Then we have to figure out how many elements to copy from the existing
        // array to the new array.  We want to copy as many elements as there are
        // in the smaller of the two arrays.
        if (m_length > 0)
        {
            int elementsToCopy{ (newLength > m_length) ? m_length : newLength };
            std::copy_n(m_data, elementsToCopy, data); // copy the elements
        }
 
        // Now we can delete the old array because we don't need it any more
        delete[] m_data;

        // And use the new array instead!  Note that this simply makes m_data point
        // to the same address as the new array we dynamically allocated.  Because
        // data was dynamically allocated, it won't be destroyed when it goes out of scope.
        m_data = data;
        m_length = newLength;
    }

    void insertBefore(int value, int index)
    {
        // Sanity check our index value
        assert(index >= 0 && index <= m_length);

        // First create a new array one element larger than the old array
        int* data{ new int[static_cast<std::size_t>(m_length+1)] };

        // Copy all of the elements up to the index
        std::copy_n(m_data, index, data); 

        // Insert our new element into the new array
        data[index] = value;

        // Copy all of the values after the inserted element
        std::copy_n(m_data + index, m_length - index, data + index + 1);

        // Finally, delete the old array, and use the new array instead
        delete[] m_data;
        m_data = data;
        ++m_length;
    }

    void remove(int index)
    {
        // Sanity check our index value
        assert(index >= 0 && index < m_length);

        // If this is the last remaining element in the array, set the array to empty and bail out
        if (m_length == 1)
        {
            erase();
            return;
        }

        // First create a new array one element smaller than the old array
        int* data{ new int[static_cast<std::size_t>(m_length-1)] };

        // Copy all of the elements up to the index
        std::copy_n(m_data, index, data); 

        // Copy all of the values after the removed element
        std::copy_n(m_data + index + 1, m_length - index - 1, data + index); 

        // Finally, delete the old array, and use the new array instead
        delete[] m_data;
        m_data = data;
        --m_length;
    }

    // A couple of additional functions just for convenience
    void insertAtBeginning(int value) { insertBefore(value, 0); }
    void insertAtEnd(int value) { insertBefore(value, m_length); }

    int getLength() const { return m_length; }
};

#endif
现在，让我们测试一下，以证明它有效
#include <iostream>
#include "IntArray.h"

int main()
{
    // Declare an array with 10 elements
    IntArray array(10);

    // Fill the array with numbers 1 through 10
    for (int i{ 0 }; i<10; ++i)
        array[i] = i+1;

    // Resize the array to 8 elements
    array.resize(8);

    // Insert the number 20 before element with index 5
    array.insertBefore(20, 5);

    // Remove the element with index 3
    array.remove(3);

    // Add 30 and 40 to the end and beginning
    array.insertAtEnd(30);
    array.insertAtBeginning(40);

    // A few more tests to ensure copy constructing / assigning arrays
    // doesn't break things
    {
        IntArray b{ array };
        b = array;
        b = b;
        array = array;
    }

    // Print out all the numbers
    for (int i{ 0 }; i<array.getLength(); ++i)
        std::cout << array[i] << ' ';

    std::cout << '\n';

    return 0;
}
这会产生结果
40 1 2 3 5 20 6 7 8 30
尽管编写容器类可能相当复杂，但好消息是您只需要编写一次。一旦容器类正常工作，您就可以随意使用和重用它，无需任何额外的编程工作。
一些可以/应该进行的额外改进
我们可以将其制作成模板类，使其适用于任何可复制类型，而不仅仅是 int。
我们应该添加各种成员函数的 const 重载，以正确支持 const IntArrays。
我们应该添加对移动语义的支持（通过添加移动构造函数和移动赋值）。
在执行 resize 或插入操作时，我们可以移动元素而不是复制它们。
致进阶读者
一些与异常处理相关的高级改进
在执行 resize 或插入操作时，仅当其移动构造函数是 noexcept 时才移动元素，否则复制它们 (
27.10 -- std::move_if_noexcept
)。
为 resize 或插入操作提供强异常安全保证 (
27.9 -- 异常规范和 noexcept
)。
还有一件事：如果标准库中的类满足您的需求，请使用它而不是创建自己的。例如，与其使用 IntArray，不如使用
std::vector<int>
。它经过实战考验，高效，并且与标准库中的其他类配合得很好。但有时您需要标准库中不存在的专门容器类，因此了解如何在需要时创建自己的容器类是件好事。
下一课
23.7
std::initializer_list
返回目录
上一课
23.5
依赖关系