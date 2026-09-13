# Python 基础笔记

> 阶段：2026-09 | 标签：#Python #基础

从 C++ 基础出发学习 Python，重点掌握写安全脚本所需的部分，不追求语言细节全覆盖。

## 学习内容

| 课次 | 主题 | 核心要点 |
|---|---|---|
| 第 1 课 | 变量、输入输出、条件判断 | 变量无需声明类型；input 返回文字；int/float 转换；if/elif/else 与缩进 |
| 第 2 课 | 循环 | for + range；while + break；死循环风险 |
| 第 3 课 | 函数 | def；参数；return；函数复用 |
| 第 4 课 | 列表与字典 | 下标访问、append；键值对、in、items |
| 第 5 课 | 字符串与文件 | f-string；open 的 w/a/r；encoding="utf-8"；with 自动关闭 |
| 第 6 课 | requests 与 HTTP | GET 请求；status_code；headers；保存网页内容 |

## 关键认知

- Python 变量无需声明类型，类型跟随赋值的值变化
- `input()` 返回的是**字符串**，做数学运算前必须用 `int()` 或 `float()` 转换
- 代码块用**缩进**表示，行尾需要**冒号**
- 字符串方法不需要背诵，记住"有这些工具"、用时查文档即可

## 常用代码片段

### 读取用户输入并判断

```python
x = int(input("请输入一个整数: "))
if x % 2 == 0:
    print("这是偶数")
else:
    print("这是奇数")
```

### 循环累加

```python
total = 0
for i in range(1, 101):
    total = total + i
print(total)   # 5050
```
### 打擂台+计数器
```
nums=[23,88,45,92,30,67]
 #打擂台：找最大值
m = nums[0]
for x in nums:
    if x>m:
        m=x
print("最大:",m)
 #计数器:统计大于50的个数
count = 0
for x in nums:
    if x > 50:
        count = count + 1
print("大于 50 的个数:", count)
```
### 函数与复用

```python
def max_of_two(a, b):
    if a > b:
        return a
    else:
        return b

def max_of_three(a, b, c):
    return max_of_two(max_of_two(a, b), c)
```

### 列表收集与字典存取

```python
big = []
for x in nums:
    if x > 50:
        big.append(x)

scores = {"小明": 88}
scores["小刚"] = 76
```

### 文件读写（防止中文乱码）

```python
with open("result.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")

with open("result.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 发送 HTTP 请求

```python
import requests
resp = requests.get("https://www.baidu.com", headers={"User-Agent": "Mozilla/5.0"})
resp.encoding = "utf-8"
print(resp.status_code)
```
