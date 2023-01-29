#include "../../common.h"

// 返回数组a[0:n-1]中value出现的次数
template<class T, class Y>
T count(const T &n, const Y &value)
{
    T index = 0;
    for (T i = 0; i < n; i++)
    {
        if (a[i] == value)
        {
            index++;
        }
    }

    return index;
}

// 给数组a[start:end-1]赋值value
template<class T, class Y>
void fill(const T &start, const T &end, const Y &value)
{
    for (T i = start, i < end; i++)
    {
        a[i] = value;
    }
}