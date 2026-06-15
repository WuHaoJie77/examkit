# Python 第六章 浓缩速记卡（字符串方法大全）

---

## 一、查找与统计

> **🧠 费曼：find = Ctrl+F 搜索，count = 数数有几个。** 你打开一个Word文档，按Ctrl+F搜"Python"，`find()`告诉你它第一次出现在第几个字。`count()`数全文出现了几次。搜不到的时候`find`返回-1（礼貌地说"没找到"），不像`index`那样直接甩脸报错。判断在不在直接用`in`，跟说人话一样：'"Python"在不在这个句子里？'

| 方法 | 作用 | 示例 | 结果 |
|------|------|------|------|
| `s.find(sub)` | 找子串位置，找不到返-1 | `'Python'.find('th')` | `2` |
| `s.count(sub)` | 计数字串出现次数 | `'ababa'.count('aba')` | `1`（不重叠） |
| `sub in s` | 判断是否包含 | `'Py' in 'Python'` | `True` |
| `s.index(sub)` | 同find，找不到**报错** | `'ab'.index('c')` | ValueError |

```python
'PythonPython'.count('Py')        # 2
'hello Python'.find('Python')     # 6
'Python'.find('z')                # -1 (不存在)
'x' in 'Python'                   # False

# find带起始位置
s = 'abcabcabc'
s.find('ab', 5)                   # 6 (从索引5开始找)
s.count('abc', 2)                 # 2 (从索引2开始数)

# count不重叠计数
'aaaaa'.count('aa')               # 2 (位置0-1, 2-3)
```

---

## 二、拆分与拼接

> **🧠 费曼：split = 拆积木，join = 拼积木。** 你有一串用逗号连起来的单词 `"苹果,香蕉,橘子"`，`split(",")` 就是按逗号拆开，变成三个独立的积木 `["苹果","香蕉","橘子"]`。反过来 `join` 是把积木拼回去：`"-".join(["苹果","香蕉","橘子"])` 用横杠把它们串成 `"苹果-香蕉-橘子"`。拆和拼是反向操作。

| 方法 | 方向 | 示例 | 结果 |
|------|------|------|------|
| `s.split(sep)` | 字符串→列表 | `'a,b,c'.split(',')` | `['a','b','c']` |
| `sep.join(list)` | 列表→字符串 | `'-'.join(['a','b'])` | `'a-b'` |
| `s.split()` | 按空白分割 | `'a b c'.split()` | `['a','b','c']` |

```python
# split + join 经典组合
s = 'a-b-c-d'
'-'.join(s.split('-')[1:3])       # 'b-c'

s = 'a:b:c:d'
''.join(s.split(':')[::2])        # 'ac'

# 实战：去掉逗号再统计
'apple,banana,orange'.replace(',',' ').split()  # ['apple','banana','orange']

# join + upper 链式
'-'.join(['hello','world']).upper()  # 'HELLO-WORLD'
```

---

## 三、大小写转换

| 方法 | 作用 | 示例 |
|------|------|------|
| `s.upper()` | 全大写 | `'Python'.upper()` → `'PYTHON'` |
| `s.lower()` | 全小写 | `'Python'.lower()` → `'python'` |
| `s.capitalize()` | 首字母大写 | 不常考 |
| `s.title()` | 每词首字母大写 | 不常考 |

```python
# 首字母大写 + 其余小写
st = 'python'
st[0].upper() + st[1:]            # 'Python'

# 忽略大小写比较
x.upper() == y.upper()            # 判断相等

# 链式调用
'Hello World'.upper().count('O')  # 2
'PyThOn'.upper().find('THON')     # 2
```

---

## 四、替换与去空白

| 方法 | 作用 | 示例 |
|------|------|------|
| `s.replace(old, new, count)` | 替换，count可选限制次数 | `'aaaa'.replace('a','b',3)` → `'bbba'` |
| `s.strip(chars)` | 去首尾字符 | `'**py**'.strip('*')` → `'py'` |
| `s.lstrip(chars)` | 去左侧字符 | `'##hi##'.lstrip('#')` → `'hi##'` |
| `s.rstrip(chars)` | 去右侧字符 | `'##hi##'.rstrip('#')` → `'##hi'` |

```python
# strip无参 = 去首尾空白
'  hello  '.strip()              # 'hello'

# strip指定字符集
'eeehelloeeeeeee'.strip('eo')    # 'hell' (去掉首尾的e和o)
'abbdebac'.strip('abc')          # 'de'
'aaaaaaabc'.strip('a')           # 'bc'

# replace限制次数
'aaaaa'.replace('a','b',3)       # 'bbbaa'
'aaaaa'.replace('a','b',3).count('a')  # 2

# strip + replace 组合
' abc123abc '.strip().replace('a','x',1)  # 'xbc123abc'
```

---

## 五、对齐填充

| 方法 | 作用 | 示例(s='hi') |
|------|------|------|
| `s.center(w, fill)` | 居中 | `'hi'.center(6,'*')` → `'**hi**'` |
| `s.ljust(w, fill)` | 左对齐 | `'hi'.ljust(6,'-')` → `'hi----'` |
| `s.rjust(w, fill)` | 右对齐 | `'hi'.rjust(6,'0')` → `'0000hi'` |
| `s.zfill(w)` | 右对齐补0 | `'42'.zfill(6)` → `'000042'` |

```python
'123'.center(7, '*')    # '**123**'
'123'.rjust(5, '-')     # '--123'
'123'.zfill(4)          # '0123'
'789'.zfill(5)          # '00789'
```

**注意：** center/rjust/ljust **返回新字符串**，不修改原变量。

---

## 六、判断方法（is 系列）

> **🧠 费曼：is系列 = 安检门。** 你过安检，工作人员看一眼就知道：你是男是女（islower/isupper）、包里有没有液体（isdigit查数字）、是不是空手（isspace查空白）。每个`is`方法就是一个安检门，符合条件→放行（True），不符合→拦下（False）。数字穿字母衣服？`isdigit`直接拦。空手过isspace？也不行，必须手里有空白才算。

### 6.1 快速参考表

| 方法 | 判断内容 | True 示例 | False 示例 |
|------|----------|-----------|------------|
| `s.islower()` | 全小写 | `'abc'` `'123abc'` | `'Abc'` |
| `s.isupper()` | 全大写 | `'ABC'` | `'Abc'` |
| `s.isdigit()` | 全数字 | `'123'` | `'123a'` `'12.3'` |
| `s.isnumeric()` | 全数字（含中文） | `'123'` `'壹贰叁'` | `'123a'` |
| `s.isalpha()` | 全字母（含中文） | `'abc'` `'你好'` | `'a1'` |
| `s.isalnum()` | 全字母或数字 | `'a1'` `'你好123'` | `'a-1'` |
| `s.isspace()` | 全空白 | `' '` `'\t'` `'\n'` | `''` `'a b'` |
| `s.isprintable()` | 可打印 | `'hello'` `'123'` | `'\n'` `'\t'` |
| `s.startswith(pre)` | 以...开头 | `'hi'.startswith('h')` | `'hi'.startswith('x')` |
| `s.endswith(suf)` | 以...结尾 | `'hi'.endswith('i')` | `'hi'.endswith('h')` |

### 6.2 关键细节

```python
# 数字混字母：isdigit=False, isnumeric=False
'123abc'.isdigit()               # False
'123abc'.isnumeric()             # False

# 中文数字：isnumeric=True
'壹贰叁'.isnumeric()             # True

# islower/isupper：忽略非字母字符
'123abc'.islower()               # True (只看字母部分)
'123ABC'.isupper()               # True
'hello WORLD'.islower()          # False (含大写字母)
'hello WORLD'.isupper()          # False (含小写字母)

# 空字符串陷阱
''.isspace()                     # False (空串不是空白)
' '.isspace()                    # True
'\t\n '.isspace()                # True

# 不可打印字符
'\n'.isprintable()               # False
'\t'.isprintable()               # False
'hello'.isprintable()            # True
```

---

## 七、len/ord/chr/str 四个基础函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `len(s)` | 字符数（含空格、转义） | `len('py\n好')` → `5` |
| `ord(c)` | 字符→Unicode | `ord('A')` → `65` |
| `chr(n)` | Unicode→字符 | `chr(97)` → `'a'` |
| `str(x)` | 转字符串 | `str(123)` → `'123'` |

```python
len('Python语言')                # 8 (6+2)
len('I\'m a student')            # 13 (\' 算1个字符)
len('Python 语言')               # 9 (6+1+2)

# ord+chr 经典题
chr(ord('a') + len('123'))       # chr(97+3) = chr(100) = 'd'
chr(len('Hello') + ord('A'))     # chr(5+65) = chr(70) = 'F'
chr(ord('z') - 25) == 'a'        # True

# len不能直接用于数字
len(123)                         # ❌ TypeError
```

---

## 八、综合链式调用

```python
# 统计某字母出现次数（忽略大小写）
'Hello World'.upper().count('O')   # 2

# 替换逗号后统计单词数
len('a,b,c'.replace(',',' ').split())  # 3

# strip后改首字母
'  test  '.strip().replace('t','T')    # 'TesT'

# 切分重组
'-'.join('a:b:c'.split(':')[::2])      # 'a-c'

# 判断是否全是数字词
all(x.isnumeric() for x in '123 456'.split())  # True
```

---

## 九、高频易错速查

| 陷阱 | 正确答案 |
|------|----------|
| `str.len()` 获取长度？ | ❌ 是 `len(str)` |
| `find` 找不到返回什么？ | **-1**，不报错 |
| `index` 找不到返回什么？ | **报错** ValueError |
| `count` 计数是否重叠？ | **不重叠** |
| `upper()` 变小写？ | ❌ upper=大写，lower=小写 |
| `center/rjust` 修改原字符串？ | ❌ 返回新字符串，原串不变 |
| `isnumeric` 和 `isdigit` 区别？ | isnumeric 认中文数字，isdigit不认 |
| 空串 `''.isspace()` ？ | **False** |
| `'123abc'.isalpha()` ？ | **False**（含数字） |
| `'123abc'.islower()` ？ | **True**（只看字母） |
| `strip('eo')` 去什么？ | 首尾出现的 **e或o** 任一字符 |
| `strip()` 无参？ | 去首尾**空白字符** |
| `'upper'` 是字符串方法？ | ✅ `s.upper()` |
| `ord('0')+8 == ord('9')`？ | ❌ 48+8=56 ≠ 57 |
| len 计算转义字符？ | `\n` `\t` `\'` 各算 **1个字符** |

---

## 十、自测15题（检测学习效果）

> 每题5分，70分及格。重点覆盖 is 系列判断和 find/count 陷阱。

**1.** `'Python'.find('z')` 的结果是？

A. 0　　B. -1　　C. 报错　　D. None

**2.** `'aaaaa'.count('aa')` 的结果是？

A. 4　　B. 2　　C. 3　　D. 1

**3.** `'123abc'.isdigit()` 的结果是？

A. True　　B. False　　C. 报错　　D. None

**4.** `''.isspace()` 的结果是？

A. True　　B. False　　C. 报错　　D. None

**5.** `'hello WORLD'.islower()` 的结果是？

A. True　　B. False　　C. 报错　　D. None

**6.** `'python'.upper()` 的结果是？

A. `'python'`　　B. `'PYTHON'`　　C. `'Python'`　　D. 报错

**7.** `'  hi  '.strip()` 的结果是？

A. `'hi'`　　B. `'  hi'`　　C. `'hi  '`　　D. `'  hi  '`

**8.** `'壹贰叁'.isnumeric()` 的结果是？

A. True　　B. False　　C. 报错　　D. None

**9.** `'-'.join(['a','b','c'])` 的结果是？

A. `'abc'`　　B. `'a-b-c'`　　C. `['a-b-c']`　　D. `'-abc-'`

**10.** `'HelloWorld'.endswith('ld')` 的结果是？

A. `'ld'`　　B. True　　C. False　　D. 2

**11.** `'aaaaa'.replace('a','b',3)` 的结果是？

A. `'bbbbb'`　　B. `'bbbaa'`　　C. `'aaabb'`　　D. `'ababa'`

**12.** 获取字符串 s 长度的正确写法是？

A. `s.len()`　　B. `len(s)`　　C. `s.length()`　　D. `length(s)`

**13.** `'\t\n '.isspace()` 的结果是？

A. True　　B. False　　C. `'\t\n '`　　D. 报错

**14.** `'abcabcabc'.find('ab', 5)` 的结果是？

A. 0　　B. 3　　C. 6　　D. -1

**15.** `'\n'.isprintable()` 的结果是？

A. True　　B. False　　C. `'\n'`　　D. 报错

---

### 答案与解析

| 题号 | 答案 | 解析 |
|------|------|------|
| 1 | **B** | find找不到返回 `-1`，不报错。index找不到才报错。 |
| 2 | **B** | count不重叠计数：位置0-1的'aa'和位置2-3的'aa'，第4个a单独→2次。 |
| 3 | **B** | isdigit()要求全部字符是数字，含字母'a'→False。 |
| 4 | **B** | 空串不是空白串。必须至少含一个空白字符才返回True。 |
| 5 | **B** | 含大写字母'W''O''R''L''D'→islower()=False。只看字母字符。 |
| 6 | **B** | upper()全转大写。lower()才是转小写，别记反。 |
| 7 | **A** | strip()无参=去首尾空白。`'  hi  '`→`'hi'`。 |
| 8 | **A** | 中文数字`壹贰叁`被isnumeric()识别为数字。isdigit()不识别。 |
| 9 | **B** | join用分隔符拼接列表元素→`'a-b-c'`。分隔符只插在元素之间。 |
| 10 | **B** | 'HelloWorld'以'ld'结尾→True。endswith返回布尔值。 |
| 11 | **B** | replace第三参数=限制3次→前3个a变b，后2个a不变→`'bbbaa'`。 |
| 12 | **B** | 字符串长度用`len(s)`函数，不是方法。`s.len()`不存在。 |
| 13 | **A** | `\t`(tab)和`\n`(换行)和空格都是空白字符→isspace()=True。 |
| 14 | **C** | 从索引5开始找'ab'，在位置6找到→6。 |
| 15 | **B** | `\n`是不可打印字符→isprintable()=False。 |

---

> 错3题以内：字符串方法基本通关　｜　错3-6题：重点回看第六节(is判断表)　｜　错6题以上：全文重读
