1|# 🍅 小番茄题库浓缩版
2|
3|免费开源的期末复习题库浓缩系统，目前已覆盖两门课程：
4|
5|- 🐍 **Python程序设计** — 13章速记卡，覆盖超星题库1300+题
6|- 💻 **计算机科学概论** — 8章速记卡
7|
8|## 特点
9|
10|每章速记卡包含：
11|- 🍳 **费曼类比** — 用生活例子讲抽象概念
12|- 📊 **知识表格** — 规则速查，拒绝长篇大论
13|- ⚠️ **高频陷阱** — 考试最易错点一网打尽
14|- ✍️ **自测练习** — 15道选择题 + 5道大题 + 解析 + 评分线
15|
16|## 如何使用
17|
18|直接打开 `exam-bank/index.html` 即可浏览，或访问在线版（需要服务器）。
19|
20|每章预计30分钟完成：10分钟知识表格 → 10分钟自测 → 10分钟对答案看解析。
21|
22|## 项目结构
23|
24|```
25|├── exam-bank/          # 构建好的网站（静态HTML）
26|│   ├── index.html      # 科目选择首页
27|│   ├── python/         # Python各章HTML
28|│   └── cs/             # 计算机科学概论各章HTML
29|├── md-source/          # Markdown源文件
30|│   ├── python/         # Python各章.md
31|│   └── cs/             # 计算机科学概论各章.md
32|└── README.md
33|```
34|
35|## 本地运行
36|
37|直接用浏览器打开 `exam-bank/index.html`，无需任何服务器。
38|
39|或者用 Python 快速起一个本地服务器：
40|```bash
41|cd exam-bank
42|python3 -m http.server 8080
43|```
44|然后访问 http://localhost:8080
45|
46|## 贡献
47|
48|欢迎提 Issue 和 PR！发现题目的错误或想新增科目，直接来。
49|
50|
## 自己部署

### 前端（纯静态）
直接用浏览器打开 `exam-bank/index.html`，或放到任意静态服务器上。

### 后端（评论区 + PDF 下载）
后端代码见 `backend/app.py`，基于 FastAPI + weasyprint。

```bash
cd backend
pip install fastapi uvicorn weasyprint
# 修改 app.py 里的 ADMIN_PASS 和路径
uvicorn app:app --host 0.0.0.0 --port 8890
```

配合 Nginx 反向代理（参考 `backend/nginx.conf`）即可完整运行。

## 联系
51|
52|- 微信：OceanOfInfinity
53|- QQ群：949808620
54|
55|---
56|⭐ 如果觉得有用，点个 Star 支持一下！
57|