# 🍅 ExamKit — 题库浓缩版

免费开源的期末复习题库浓缩系统，目前已覆盖两门课程：

- 🐍 **Python程序设计** — 13章速记卡，覆盖超星题库1300+题
- 💻 **计算机科学概论** — 8章速记卡

## 特点

每章速记卡包含：
- 🍳 **费曼类比** — 用生活例子讲抽象概念
- 📊 **知识表格** — 规则速查，拒绝长篇大论
- ⚠️ **高频陷阱** — 考试最易错点一网打尽
- ✍️ **自测练习** — 15道选择题 + 5道大题 + 解析 + 评分线

## 如何使用

直接打开 `exam-bank/index.html` 即可浏览，或访问在线版（需要服务器）。

每章预计30分钟完成：10分钟知识表格 → 10分钟自测 → 10分钟对答案看解析。

## 项目结构

```
├── exam-bank/          # 构建好的网站（静态HTML）
│   ├── index.html      # 科目选择首页
│   ├── python/         # Python各章HTML
│   └── cs/             # 计算机科学概论各章HTML
├── md-source/          # Markdown源文件
│   ├── python/         # Python各章.md
│   └── cs/             # 计算机科学概论各章.md
├── backend/            # FastAPI后端（评论+PDF）
│   ├── app.py          # 后端代码（密码已脱敏）
│   └── nginx.conf      # Nginx配置模板
└── README.md
```

## 自己部署

### Docker 一键部署（推荐）

零环境依赖：

```bash
docker compose up -d
```

访问 http://localhost:8898

- 评论数据保存在 `data/comments.db`
- PDF 缓存在 `data/pdf_cache/`
- 开发模式：`docker compose -f docker-compose.dev.yml up`（前端修改即时生效）

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

依赖（Debian/Ubuntu）：
```bash
apt-get install -y fonts-noto-cjk poppler-utils
```

## 本地运行

直接用浏览器打开 `exam-bank/index.html`，无需任何服务器。

或者用 Python 快速起一个本地服务器：
```bash
cd exam-bank
python3 -m http.server 8080
```
然后访问 http://localhost:8080

## 贡献

欢迎提 Issue 和 PR！发现题目的错误或想新增科目，直接来。

## 联系

- 微信：OceanOfInfinity
- QQ群：949808620

---
⭐ 如果觉得有用，点个 Star 支持一下！
