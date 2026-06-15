# Python 第十章 浓缩速记卡（while循环 · 嵌套混用）

---

## 一、while 循环基础

> **🧠 费曼：while = 哨兵站岗。** 一个士兵在门口站岗，每隔一段时间问自己："时间到了吗？"没到→继续站（循环），到了→换岗（退出）。`while True`就是永不换岗的哨兵，必须有人发"break"命令才能把他拉下来。如果忘了发命令（忘写break），这个兵就站到天荒地老——死循环。

### 1.1 语法

```python
while 条件:
    循环体         # 条件为True时反复执行
else:             # 可选：正常结束（未break）时执行
    语句
```

### 1.2 while vs for 对比

| | for | while |
|------|-----|-------|
| 适用场景 | 已知循环次数 | 未知循环次数 |
| 遍历对象 | 可迭代对象（列表/字符串/range） | 条件表达式 |
| 典型写法 | `for i in range(n):` | `while x < n:` |
| 可互转？ | while 能替代所有 for ✅ | for 不能替代所有 while ❌ |

```python
# for → while（总是可以）
for i in range(5):
    print(i)

i = 0
while i < 5:
    print(i)
    i += 1

# while True → for（不行！次数不确定）
```

### 1.3 条件表达式可用任意类型

```python
while 1:        # 非0→True
while "hello":  # 非空字符串→True
while [1,2]:    # 非空列表→True
while 0:        # 0→False，不执行
while "":       # 空字符串→False，不执行
while []:       # 空列表→False，不执行
```

---

## 二、while True + break 模式

```python
# 标准写法：无限循环 + 条件跳出
while True:
    操作
    if 退出条件:
        break         # ← 没有break就是死循环！

# 经典场景：输入验证
while True:
    a = eval(input("输入[0,100]范围的分数："))
    if a < 0 or a > 100:
        break
    s += a
```

| 说法 | 对错 |
|------|:--:|
| while True 一定是死循环 | ❌ 加break可退出 |
| while True 必须有break | ✅ 否则死循环 |
| while True 语法不通过 | ❌ 完全合法 |

---

## 三、while-else 结构

```python
while 条件:
    if 某条件:
        break        # break → else 不执行
    语句
else:
    语句             # 正常结束（条件变False）→ else 执行
```

**规则和 for-else 完全一样：break 跳过 else，正常结束触发 else。**

---

## 四、break / continue 在 while 中

```python
# break：终止整个循环
while True:
    s += 1
    if s > 100:
        break         # 跳出，执行循环后面的代码

# continue：跳过本次，回到条件判断
while x < 10:
    x += 1
    if x % 2 == 0:
        continue      # 跳过print
    print(x)          # 只输出奇数
```

| 说法 | 对错 |
|------|:--:|
| break 跳出所有嵌套层 | ❌ 只跳出最内层 |
| continue 跳出当前循环 | ❌ 只跳过本次迭代 |

---

## 五、while + for 嵌套混用

### 5.1 基本规则

```python
while 外层条件:
    for 变量 in 序列:    # 内层是for
        语句
    更新外层变量
```

**外层执行1次，内层for完整跑一轮。**

### 5.2 典型用例

```python
# 打印九九乘法表前5行
row = 1
while row <= 5:
    for col in range(1, row + 1):
        print(f"{col}×{row}={col*row}", end='\t')
    print()
    row += 1

# while + for 混合计数
count = 0
x = 1
while x <= 2:
    for y in range(3):
        count += 1
    x += 1
# count = 6（2轮×3次）

# while嵌套while
i = 1
while i <= 2:
    j = 1
    while j <= 3:
        print(j, end='')
        j += 1
    i += 1
# 输出: 123123（外层2次×内层3次）
```

### 5.3 break 在嵌套中

```python
while x < 10:
    for y in range(5):
        if 条件:
            break       # 只跳出内层for！外层while继续
```

---

## 六、经典陷阱

### 6.1 忘记更新循环变量 → 死循环

```python
i = 0
while i < 5:
    print(i)
    # 忘了 i += 1  → 死循环输出 0 0 0 ...
```

### 6.2 continue 前忘记更新变量

```python
i = 0
while i < 5:
    if i == 2:
        continue      # 跳过 i+=1 → 死循环！
    print(i)
    i += 1
```

### 6.3 累加位置不同结果不同

```python
# 先加后判断 → 超出范围的值被计入
s = 0
while True:
    a = eval(input())
    s += a            # 先加
    if a < 0 or a > 100:
        break         # 后判断 → 非法值已计入！

# 先判断后加 → 超出范围的值不计入
while True:
    a = eval(input())
    if a < 0 or a > 100:
        break         # 先判断
    s += a            # 合法才加
```

---

## 七、经典程序模板

```python
# 输入-循环累加（遇非法值退出）
s = 0
while True:
    a = eval(input("输入："))
    if a < 0 or a > 100:
        break
    s += a

# 找最小满足条件的数
a = 11
while a < 100:
    if a % (a//10 + a%10) == 0:
        print(a)
        break
    a += 1
else:
    print('不存在')

# 斐波那契数列
a, b = 1, 1
count = 1
while count <= 10:
    print(a)
    a, b = b, a + b
    count += 1

# 猜数字
target = 67
guess = int(input("猜："))
while guess != target:
    if guess < target: print("太小")
    else: print("太大")
    guess = int(input("再猜："))
print("猜对了")
```

---

## 八、循环关键字集合

| 属于循环结构 | 不属于 |
|-------------|--------|
| `for` `while` | `if` `elif` `else` `def` |
| `break` `continue` | `import` `except` `try` |
| `else`(可搭配for/while) | `in`(运算符) |

---

## 九、高频易错速查

| 陷阱 | 真相 |
|------|------|
| while True 必死循环？ | ❌ break可退出 |
| while 条件必须布尔？ | ❌ 任何类型都行(truthiness) |
| while 0 会执行吗？ | ❌ 0是False，不执行 |
| for 能替代所有while？ | ❌ 不确定次数的while不行 |
| break 跳出所有层？ | ❌ 只跳出最内层 |
| for 循环次数不确定？ | ❌ 由遍历结构确定 |
| while 必须提供循环次数？ | ❌ 不需要 |
| else 只和if搭配？ | ❌ 也可搭配for/while |
| while 条件为空列表？ | 不执行(空列表=False) |
| break后的代码会执行？ | ❌ 不会 |

---

## 十、自测15题（检测学习效果）

> 每题5分，70分及格。重点覆盖 while True+break 和 while/for 嵌套。

**1.** `while 0:` 的循环体会执行吗？

A. 执行1次　　B. 死循环　　C. 不执行　　D. 报错

**2.** while True 循环中防止死循环的关键字是？

A. continue　　B. break　　C. else　　D. pass

**3.** 执行后输出？

```python
i = 0
while i < 5:
    i += 2
print(i)
```

A. 4　　B. 5　　C. 6　　D. 0

**4.** while 循环的 else 什么时候执行？

A. 每次循环后　　B. break后　　C. 正常结束(条件变False)后　　D. 永远不执行

**5.** `while "":` 循环体会执行吗？

A. 执行　　B. 不执行　　C. 报错　　D. 死循环

**6.** 嵌套循环中内层 break 会？

A. 跳出所有层　　B. 只跳出内层　　C. 跳到外层else　　D. 终止程序

**7.** 执行后 count 的值？

```python
count = 0
x = 1
while x <= 2:
    for y in range(3):
        count += 1
    x += 1
```

A. 3　　B. 6　　C. 2　　D. 5

**8.** 以下哪个不能和 else 搭配？

A. if　　B. for　　C. while　　D. import

**9.** 所有 for 循环都能用 while 重写吗？

A. 能　　B. 不能　　C. 部分能　　D. 反过来才行

**10.** while 循环的条件表达式必须是什么类型？

A. bool　　B. int　　C. 任何类型都可以(truthiness)　　D. str

**11.** 执行后 s 的值？

```python
s = 0
i = 0
while i < 5:
    s += i
    i += 2
print(s)
```

A. 6　　B. 10　　C. 15　　D. 5

**12.** 以下关于 for 和 while 说法**错误**的是？

A. for遍历循环次数由遍历结构决定　　B. while适合不确定次数的循环  
C. for循环次数不确定　　D. while可用break跳出

**13.** 执行后输出？

```python
k = 5
while k < 50:
    if k % 7 == 0: break
    k += 5
    print(k, end=';')
```

A. `10;15;20;25;30;35;`　　B. `10;15;20;25;30;`  
C. `10;`　　D. `10;15;20;25;30;35;40;45;`

**14.** while 循环中 continue 的作用是？

A. 跳出循环　　B. 跳过本次剩余代码，回到条件判断  
C. 和 break 相同　　D. 终止程序

**15.** 执行后输出？

```python
a = 5
while a < 50:
    if a % 11 == 0: break
    a += 5
    print(a, end=';')
else:
    print('没找到')
```

A. `10;15;...45;50;没找到`　　B. `10;15;...45;50;`  
C. `10;15;...50;没找到`　　D. `没找到`

---

### 答案与解析

| 题号 | 答案 | 解析 |
|------|------|------|
| 1 | **C** | 0是False→循环体一次都不执行。任何falsy值(0/""/[])都不执行。 |
| 2 | **B** | break是while True中唯一的合法出口。continue跳不过条件判断。 |
| 3 | **C** | i:0→2→4→6(循环条件i<5为False)。最后i=6。 |
| 4 | **C** | while-else只在条件变为False正常结束时执行。break跳过else。 |
| 5 | **B** | 空字符串是falsy→循环体不执行。 |
| 6 | **B** | break只跳出最内层循环，外层不受影响。 |
| 7 | **B** | 外层2次×内层3次=6。x=1时3次，x=2时3次，然后x=3退出。 |
| 8 | **D** | else可搭配if、for、while。import不行。 |
| 9 | **A** | 所有for都能改写为while（用变量模拟遍历）。反过来while True无法直接写成for。 |
| 10 | **C** | Python用truthiness：0/空串/空列表=False，其他=True。不限定bool。 |
| 11 | **A** | i:0→s=0,i=2→s=2,i=4→s=6,i=6(退出)。s=6。 |
| 12 | **C** | for循环次数由遍历结构元素个数确定，是**确定的**。说"不确定"是错的。 |
| 13 | **A** | a:5→10→15→20→25→30→35(35%7=0)→break。输出到35。 |
| 14 | **B** | continue=跳过本轮剩余代码，回到while条件判断。不是跳出循环。 |
| 15 | **C** | a从5递增到50(55%11=0? No→55≥50退出)，没有数%11=0→未break→else执行。输出包含50和"没找到"。 |

---

> 错3题以内：while循环过关　｜　错3-6题：重点回看第二节(while True+break)和第三节(while-else)　｜　错6题以上：全文重读
