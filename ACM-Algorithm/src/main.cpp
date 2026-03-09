#include <iostream>
using namespace std;

class Solution
{
public:
    int add(int a, int b)
    {
        return a + b;
    }
};

int main()
{
    int a, b;
    while (cin >> a >> b)
    {
        Solution solution;
        cout << solution.add(a, b) << '\n';
    }
    return 0;
}
