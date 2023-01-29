// 函数与参数

int abc_1(int a, int b, int c)
{
    return a + b * c;
}

float abc_2(float a, float b, float c)
{
    return a + b * c;
}

// 模板函数
template<class T>
T abc_3(T a, T b, T c)
{
    return a + b * c;
}

// 引用参数
template<class T>
T abc_4(T &a, T &b, T &c)
{
    return a + b * c;
}

// 常量引用 引用参数不可被修改
template<class T>
T abc_5(const T &a, const T &b, const T &c)
{
    return a + b * c;
}

template<class Ta, class Tb, class Tc>
Ta abc_6(const Ta &a, const Tb &b, const Tc &c)
{
    return a + b * c;
}