# Python 第八章 浓缩速记卡（分支结构 if/elif/else）

---

## 一、三种分支结构

> **🧠 费曼：if = 岔路口。** 你开车到路口，看红绿灯。绿灯→直行（if True），红灯→右转绕路（else）。`elif`就是多个岔路：先去肯德基？关门了→去麦当劳？也关门了→else：回家吃泡面。电脑就是按照这个逻辑一条路一条路试，找到第一条能走的路就进去，后面不看了。

### 1.1 单分支 if

```python
if 条件:
    语句块          # 条件为True时执行，必须缩进
```

### 1.2 双分支 if-else

```python
if 条件:
    语句块A         # True时执行
else:
    语句块B         # False时执行
```

### 1.3 多分支 if-elif-else

```python
if 条件1:
    语句块1
elif 条件2:
    语句块2
elif 条件3:
    语句块3
else:               # 可选
    语句块4
```

**执行规则：** 从上到下依次判断，**找到第一个True就执行并跳出**，后面不再判断。

### 1.4 紧凑形式（三元表达式）

```python
x = a if 条件 else b      # 条件True→a, False→b
print(a if a>b else b)    # 输出较大值
print(x if x>=0 else -x)  # 输出绝对值
```

---

## 二、语法铁律

| 规则 | 错误写法 | 正确写法 |
|------|----------|----------|
| 条件后必须加冒号 | `if x>0` | `if x>0:` |
| 语句块必须缩进 | 顶格写 | 缩进4空格 |
| else后有冒号 | `else` | `else:` |
| elif不是elseif | `elseif` ❌ | `elif` ✅ |
| if/else同级对齐 | else缩进 | else与if对齐 |
| 比较用==不是= | `if a=5` ❌ | `if a==5:` ✅ |

---

## 三、多分支 vs 多个独立if

```python
# 多分支——只执行第一个True
x = 89
if x >= 60: print('及格')
elif x >= 70: print('中等')
elif x >= 80: print('良好')
# 输出：及格（后面的不再判断）

# 独立if——每个都判断，可能执行多个
x = 78
if x >= 60: print('及格')    # ✓
if x >= 70: print('中等')    # ✓
if x >= 80: print('良好')    # ✗
# 输出：及格 中等
```

**分清楚什么时候用 elif，什么时候用独立 if。**

---

## 四、分支嵌套

### 4.1 核心规则

```python
if 外层条件:
    if 内层条件:       # 内层必须比外层多缩进一级
        语句块
    else:               # 与最近的未配对if配对
        语句块
else:                   # 与外层if对齐
    语句块
```

- **内层else与最近的未配对if配对**（看缩进级别）
- 内层分支必须完全包含在外层分支的代码块中
- 外层条件不满足时，内层不会执行
- 没有嵌套层数上限

### 4.2 经典嵌套示例

```python
# 判断闰年（三层嵌套）
year = 2024
if year % 4 == 0:
    if year % 100 == 0:
        if year % 400 == 0:
            print("闰年")
        else:
            print("平年")
    else:
        print("闰年")
else:
    print("平年")
# 2024 → 闰年

# 判断正负零
num = 0
if num > 0:
    print("正数")
else:
    if num < 0:
        print("负数")
    else:
        print("零")

# 成绩分级嵌套
score = 85
if score >= 90:
    print("优秀")
else:
    if score >= 80:
        print("良好")
    else:
        print("其他")
```

---

## 五、条件表达式编写

### 5.1 常见判断

```python
# 奇偶
if x % 2 == 1:           # 奇数
if x % 2 == 0:           # 偶数

# 整除
if x % 3 == 0:           # 能被3整除

# 区间
if 0 <= x <= 100:        # [0,100]闭区间
if x >= 0 and x <= 50 or x > 100:  # [0,50]∪(100,+∞)

# 字符类型
if 'A' <= c <= 'Z':      # 大写字母
if 'a' <= c <= 'z':      # 小写字母
if '0' <= c <= '9':      # 数字字符
if 'a'<=c<='z' or 'A'<=c<='Z':  # 英文字母（含大小写）

# 字符串包含
if "红" in name:          # 判断是否包含子串
if 学号 in 列表:          # 判断是否在列表中

# 登录验证
if user == "admin" and pwd == "123456":
    print("登录成功")
```

### 5.2 闰年判断

```python
(year % 4 == 0 and year % 100 != 0) or year % 400 == 0
```

### 5.3 三角形判断

```python
# 能否构成
a + b > c and a + c > b and b + c > a

# 等腰
a == b or b == c or a == c

# 等边
a == b == c

# 直角
a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2
```

---

## 六、input() 在分支中的陷阱

```python
x = input("分数: ")       # x是字符串！
if x > 60:                # TypeError! str不能和int比
    print("及格")

# 正确写法
x = eval(input("分数: "))  # 转成数字
if x >= 60:
    print("及格")
```

---

## 七、高频填空模板

```python
# 1. 正数判断
if num > 0:
    print("正数")
elif num < 0:
    print("负数")
else:
    print("零")

# 2. 成绩等级
if score >= 90:    grade = 'A'
elif score >= 80:  grade = 'B'
elif score >= 70:  grade = 'C'
elif score >= 60:  grade = 'D'
else:              grade = 'E'

# 3. 字母判断
if c.isupper():    print("大写字母")
elif c.islower():  print("小写字母")
elif c.isdigit():  print("数字")
else:              print("其他字符")

# 4. 季节
if 3 <= month <= 5:    print("春季")
elif 6 <= month <= 8:  print("夏季")
elif 9 <= month <= 11: print("秋季")
else:                  print("冬季")

# 5. 登录验证
if user == 'admin' and pwd == '123456':
    print("登录成功")
elif user != 'admin':
    print("用户名错误")
else:
    print("密码错误")
```

---

## 八、高频易错速查

| 陷阱 | 正确答案 |
|------|----------|
| Python多分支关键字？ | `if` `elif` `else`，不是 `elseif` |
| `elif` 能单独使用？ | ❌ 必须在 `if` 之后 |
| `else` 必须出现？ | ❌ 可选 |
| 判断相等用什么？ | `==` 不是 `=` |
| 多个 `elif`，执行几个？ | 只执行**第一个**满足条件的 |
| 多个独立 `if`，执行几个？ | 每个独立判断，可能执行多个 |
| 分支结构每句都执行？ | ❌ 只执行匹配的分支 |
| 内层else和谁配对？ | 最近的**同缩进级别**未配对 `if` |
| 分支可以向已执行过的语句跳转？ | ❌ Python没有goto |
| 双分支紧凑形式关键字？ | `if` 和 `else`，不是 `elif` |
| 递归是基本结构？ | ❌ 顺序/分支/循环才是 |
| `input()` 返回的能直接和数字比？ | ❌ 必须先 `eval()` 或 `int()` 转换 |
| `if x>0:` 冒号后面缩进的语句是？ | 条件为True时执行 |

---

## 九、自测15题（检测学习效果）

> 每题5分，70分及格。重点覆盖 elif 执行顺序和嵌套配对。

**1.** Python中多分支的关键字是？

A. `elseif`　　B. `elif`　　C. `else if`　　D. `switch`

**2.** 执行以下代码，输入70后输出？

```python
x = eval(input())
if x >= 90: print('A')
elif x >= 70: print('B')
elif x >= 60: print('C')
```

A. A　　B. B　　C. C　　D. 无输出

**3.** `x = 5 if 3>5 else 10` 后，x的值是？

A. 5　　B. 10　　C. True　　D. False

**4.** 以下哪种写法会导致语法错误？

A. `if x>0:`　　B. `elif x>0:`　　C. `elseif x>0:`　　D. `else:`

**5.** 执行以下代码，x=15时输出？

```python
x = 15
if x > 10:
    if x < 20:
        print("A")
    else:
        print("B")
else:
    print("C")
```

A. A　　B. B　　C. C　　D. 无输出

**6.** 内层else与哪个if配对？

A. 最近的外层if　　B. 最近的同缩进级别未配对if  
C. 最远的外层if　　D. 所有未配对的if

**7.** `if False: print('A'); else: print('B')` 输出？

A. A　　B. B　　C. AB　　D. 无输出

**8.** 判断x是三位整数的正确写法是？

A. `x%100!=0`　　B. `x>=100 and x<=999`  
C. `x//100==0`　　D. `x/100>=1`

**9.** 以下代码输出？

```python
a = 89
if a >= 60: print('及格')
elif a >= 70: print('中等')
elif a >= 80: print('良好')
```

A. 及格　　B. 中等　　C. 良好　　D. 及格中等良好

**10.** 判断c是否为大写字母的正确写法？

A. `c >= 'A' and c <= 'Z'`　　B. `'A' <= c <= 'Z'`  
C. A和B都行　　D. A和B都不行

**11.** 嵌套if中，外层条件为False时，内层代码会执行吗？

A. 会　　B. 不会　　C. 取决于内层条件　　D. 报错

**12.** `if x>0:` 中忘记写冒号会导致什么？

A. 逻辑错误　　B. 语法错误　　C. 程序正常运行　　D. 运行时错误

**13.** 以下哪个不是Python分支结构的关键字？

A. `if`　　B. `else`　　C. `in`　　D. `elif`

**14.** 执行代码，num=3输出？

```python
num = 3
if num % 2 == 0:
    if num % 3 == 0:
        print("A")
    else:
        print("B")
else:
    if num % 3 == 0:
        print("C")
    else:
        print("D")
```

A. A　　B. B　　C. C　　D. D

**15.** `x = input(); if x > 60:` 当输入70时会怎样？

A. 输出True　　B. 输出False　　C. TypeError报错　　D. 正常判断

---

### 答案与解析

| 题号 | 答案 | 解析 |
|------|------|------|
| 1 | **B** | Python用`elif`，没有`elseif`和`switch`。 |
| 2 | **B** | 70>=90? No。70>=70? Yes→执行print('B')并跳出，不再判断后面的elif。 |
| 3 | **B** | 3>5为False→取else的值10。紧凑形式：True取if前值，False取else后值。 |
| 4 | **C** | `elseif`不是Python关键字。D的`else:`是正确的。 |
| 5 | **A** | 15>10 True→进入外层。15<20 True→进入内层→输出A。 |
| 6 | **B** | 内层else与最近的、同缩进级别的未配对if配对。 |
| 7 | **B** | False→执行else分支→输出B。 |
| 8 | **B** | 三位数范围100-999。A不对（如5%100=5≠0但不满足），C/D都不对。 |
| 9 | **A** | 多分支只执行第一个满足的。89>=60→输出'及格'，后面全部跳过。 |
| 10 | **C** | 两种写法等价。`'A'<=c<='Z'`是Python链式比较的语法糖。 |
| 11 | **B** | 外层条件False→整个外层代码块跳过，内层代码根本不执行。 |
| 12 | **B** | 缺少冒号是SyntaxError（语法错误），程序根本跑不起来。 |
| 13 | **C** | `in`是关系运算符，不是分支关键字。 |
| 14 | **C** | 3%2=1≠0→进外层else。内层3%3=0→进if→输出C。 |
| 15 | **C** | input返回str"70"，和int(60)比较→TypeError。必须先eval()转换。 |

---

> 错3题以内：分支结构吃透了　｜　错3-6题：重点回看第三节(多分支vs独立if)和第四节(嵌套)　｜　错6题以上：全文重读
