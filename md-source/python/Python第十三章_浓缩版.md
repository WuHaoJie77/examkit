# Python 第十三章 浓缩速记卡（函数定义 · 调用 · 参数）

---

## 一、函数定义与调用

> **🧠 费曼：函数 = 榨汁机。** 你把苹果（实参）从上面扔进去，机器（函数体）在里面一顿榨，最后从出口流出苹果汁（返回值）。`def`就是制造这个机器的图纸——你画好图纸（定义），要用的时候把水果扔进去（调用）。你可以造一台不榨汁只干活的机器（无return→返回None），也可以造一台榨完汁还附带果渣的（return多个值）。关键是：机器必须先造好（定义在前），才能用（调用在后）。

### 1.1 基本语法

```python
def 函数名(形参列表):
    """文档字符串（可选）"""
    函数体
    return 返回值    # 可选
```

```python
def add(a, b):
    return a + b

result = add(3, 5)    # 调用，result=8
```

### 1.2 语法铁律

| 规则 | 正确 | 错误 |
|------|------|------|
| 关键字 | `def` | `define` `del` `function` |
| 函数名后 | 必须有 `()` | 不能省略 |
| 冒号 | 英文 `:` | 中文 `：` ❌ |
| 定义在前调用在后 | ✅ | ❌ 不能先调用后定义 |
| return 可选 | 可以没有 | — |

---

## 二、形参与实参

| 概念 | 在哪出现 | 是什么 |
|------|----------|--------|
| **形参** | 函数**定义**时 | 占位变量名 |
| **实参** | 函数**调用**时 | 实际传递的值 |

```python
def add(a, b):        # a, b 是形参
    return a + b

result = add(3, 5)    # 3, 5 是实参（按位置传递）
```

### 2.1 实参的灵活性

```python
add(3, 5)              # 常量
add(x, y)              # 变量
add(3+2, len("hi"))   # 表达式
add(f(1), g(2))       # 函数返回值
```

**实参不限于常量，可以是任何表达式。**

---

## 三、返回值

### 3.1 return 规则

```python
def f1():
    return 5          # 返回5

def f2():
    pass              # 无return → 返回None

def f3():
    print("hi")       # 无return → 返回None

def f4():
    return            # 返回None
```

| 情况 | 返回值 |
|------|--------|
| `return 表达式` | 表达式的值 |
| `return` 或 无return | **None** |
| 函数体只有 `pass` | None |

### 3.2 函数间调用

```python
def f1(a):
    return a * 2

def f2(b):
    return f1(b) + 3    # 函数内调用另一个函数

print(f2(4))            # f1(4)+3 = 8+3 = 11
```

---

## 四、函数参数个数

```python
def f1():           # 0个参数 ✅
    return 1

def f2(a, b):       # 多个参数 ✅
    return a + b

f1()                # 调用也必须加()
```

**无论定义还是调用，圆括号必不可少。**

---

## 五、常见内置函数调用模式

```python
# 字符串方法
s.upper()              # 转大写
s.startswith("pre")    # 检查前缀 → True/False
s.count("c")           # 统计出现次数

# 列表方法
lst.append(x)          # 追加
lst1 + lst2            # 拼接

# 数学计算
max(a, b)
sum(lst)
len(s)
```

---

## 六、经典函数模板

```python
# 阶乘
def factorial(n):
    if n == 0 or n == 1:
        return 1
    t = 1
    for i in range(1, n+1):
        t *= i
    return t

# 组合数 C(n,m) = n!/(m!(n-m)!)
def fact(x):
    t = 1
    for i in range(1, x+1):
        t *= i
    return t
# 调用: fact(n) / fact(m) / fact(n-m)

# 判断质数
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 三角形面积
def triangle_area(base, height):
    return 0.5 * base * height

# 偶数判断
def is_even(n):
    return n % 2 == 0

# 最大公约数（欧几里得）
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
```

---

## 七、高频易错速查

| 陷阱 | 真相 |
|------|------|
| 定义函数用 `define`？ | ❌ 是 `def` |
| 函数可以先调用后定义？ | ❌ 必须先定义 |
| 函数名后可以省略 `()`？ | ❌ 定义和调用都必须有 |
| 冒号用中文 `：`？ | ❌ 必须英文 `:` |
| 无 return 返回什么？ | **None** |
| 形参是调用时传入的？ | ❌ 形参在定义时，实参在调用时 |
| 实参只能是常量？ | ❌ 可以是任何表达式 |
| 函数内不能调用其他函数？ | ❌ 可以调用 |
| Python 函数最多返回一个值？ | ❌ 可返回多个值（元组） |
| 函数名能以数字开头？ | ❌ 不能 |
| `return` 和 `print` 一样？ | ❌ return 返回值，print 仅显示 |

---

## 八、自测15题（检测学习效果）

> 每题5分，70分及格。重点覆盖 def 语法和 return 行为。

**1.** Python定义函数的关键字是？

A. `define`　　B. `def`　　C. `function`　　D. `del`

**2.** 以下函数定义语法正确的是？

A. `def f(x): return x+1`　　B. `def f(x) return x+1`  
C. `function f(x): return x+1`　　D. `def f(x)：return x+1`

**3.** 函数无return语句时，返回值是？

A. 0　　B. False　　C. None　　D. 报错

**4.** 以下代码输出？

```python
def f():
    pass
print(f())
```

A. None　　B. 0　　C. pass　　D. 报错

**5.** 定义时的参数叫____，调用时传入的叫____？

A. 实参，形参　　B. 形参，实参　　C. 都是形参　　D. 都是实参

**6.** 调用函数时，函数名后面的 `()` 可以省略吗？

A. 可以　　B. 不可以　　C. 无参数时可以　　D. 定义时可以

**7.** 函数可以先调用再定义吗？

A. 可以　　B. 不可以　　C. 内置函数可以　　D. 无参数时可以

**8.** 以下代码输出？

```python
def add(a, b): return a + b
print(add(10, 20))
```

A. 10　　B. 20　　C. 30　　D. None

**9.** 以下哪个**不能**作为函数调用的实参？

A. 常量 `5`　　B. 变量 `x`　　C. 表达式 `3+2`　　D. 以上都可以

**10.** 函数定义中，形参个数可以是？

A. 至少1个　　B. 0个、1个或多个　　C. 最多5个　　D. 只能2个

**11.** `def`语句后面的冒号必须用？

A. 中文`：`　　B. 英文`:`　　C. 都可以　　D. 不需要

**12.** 以下代码输出？

```python
def f1(a): return a * 2
def f2(b): return f1(b) + 3
print(f2(4))
```

A. 8　　B. 11　　C. 7　　D. 报错

**13.** 函数体内可以调用其他自定义函数吗？

A. 可以　　B. 不可以　　C. 只能调用内置函数　　D. 只能调用一个

**14.** 以下函数调用写法正确的是？

A. `add 3, 5`　　B. `add(3, 5)`　　C. `add[3, 5]`　　D. `add{3, 5}`

**15.** 一个函数可以有多个 return 语句吗？

A. 不可以　　B. 可以，但只能执行一个　　C. 可以，全部执行　　D. 最多2个

---

### 答案与解析

| 题号 | 答案 | 解析 |
|------|------|------|
| 1 | **B** | Python用`def`。`define`/`function`是其他语言，`del`是删除。 |
| 2 | **A** | 必须有冒号且缩进。B缺冒号，C关键字错，D用了中文冒号。 |
| 3 | **C** | 无return→隐式返回None。 |
| 4 | **A** | f()只有pass无return→返回None→print输出None。 |
| 5 | **B** | 定义时=形参(占位)，调用时=实参(实际值)。别记反。 |
| 6 | **B** | 定义和调用时圆括号都不可省略。 |
| 7 | **B** | Python是解释型语言，必须先定义再调用。 |
| 8 | **C** | 10+20=30。 |
| 9 | **D** | 实参可以是常量、变量、表达式、函数返回值，全部合法。 |
| 10 | **B** | 0个到多个都可以。 |
| 11 | **B** | 必须英文冒号。if/while/for/def都一样。 |
| 12 | **B** | f1(4)=8, f2(4)=8+3=11。 |
| 13 | **A** | 函数内可以调用任何已定义的函数。 |
| 14 | **B** | 函数调用必须用圆括号。 |
| 15 | **B** | 可以有多个return（如if/else分支中各一个），但实际只执行一个。 |

---

> 错3题以内：函数基础过关　｜　错3-6题：重点回看第一节和第三节　｜　错6题以上：全文重读
