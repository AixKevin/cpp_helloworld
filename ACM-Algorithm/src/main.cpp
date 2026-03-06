#include <iostream>
#include <cstring>

using namespace std;

class Solution {
public:
    int solve(int a, int b) {
        // 定义一个大小为 10 的静态数组
    int arr[10];

    // 用 memset 函数把数组的值初始化为 0
    memset(arr, 0, sizeof(arr));

    // 使用索引赋值
    arr[0] = 1;
    arr[1] = 2;

    // 使用索引取值
    int a = arr[0];






    }
};

int main() {
    int a, b;
    // 读取到 EOF
    while (cin >> a >> b) {
        int result = Solution().solve(a, b);
        cout << result << endl;
    }
    return 0;
}
