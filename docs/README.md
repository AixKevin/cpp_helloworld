# LearnCpp C++ 教程文档

本文件夹包含从 LearnCpp.com.cn 网站下载的 C++ 教程文档。

## 文件夹结构

```
docs/
├── LEARNING_PLAN.md          # 学习计划指南
├── fetch_learncpp.py         # 自动抓取脚本
├── chapter_0/                # 第0章：简介/入门
├── chapter_1/                # 第1章：C++基础
├── chapter_2/                # 第2章：函数和文件
├── chapter_3/                # 第3章：调试
├── chapter_4/                # 第4章：基本数据类型
├── chapter_5/                # 第5章：常量和字符串
├── chapter_6/                # 第6章：运算符
├── chapter_7/                # 第7章：作用域
├── chapter_8/                # 第8章：控制流
├── chapter_9/                # 第9章：错误处理
├── chapter_10/               # 第10章：类型系统
├── chapter_11/               # 第11章：函数模板
├── chapter_12/               # 第12章：引用和指针
├── chapter_13/               # 第13章：枚举和结构体
├── chapter_14/               # 第14章：类简介
├── chapter_15/               # 第15章：更多关于类
├── chapter_16/               # 第16章：std::vector
├── chapter_17/               # 第17章：std::array
├── chapter_18/               # 第18章：迭代器和算法
├── chapter_19/               # 第19章：动态内存
├── chapter_20/               # 第20章：函数
├── chapter_21/               # 第21章：运算符重载
├── chapter_22/               # 第22章：移动语义
├── chapter_23/               # 第23章：对象关系
├── chapter_24/               # 第24章：继承
├── chapter_25/               # 第25章：虚函数
├── chapter_26/               # 第26章：模板
├── chapter_27/               # 第27章：异常
├── chapter_28/               # 第28章：I/O
├── chapter_O/                # 位操作
├── chapter_F/               # Constexpr函数
└── appendix_*/               # 附录
```

## 如何使用

1. **学习计划**: 先阅读 `LEARNING_PLAN.md` 了解完整学习路径
2. **按顺序学习**: 按照章节顺序逐步学习
3. **动手实践**: 每个示例都亲手编写和运行

## 在线资源

- 官方网站: https://learncpp.com.cn/
- 网站索引: https://learncpp.com.cn/learn-cpp-site-index/

## 抓取更新

如需获取最新内容，可以运行:

```bash
pip install requests beautifulsoup4
python docs/fetch_learncpp.py
```

## 许可证

本教程内容版权归 LearnCpp.com.cn 所有，仅供个人学习使用。
