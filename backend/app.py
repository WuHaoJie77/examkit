"""
小番茄题库浓缩版 - 后端服务
=============================
功能：
  1. 评论区 API（发布/加载评论）
  2. PDF 生成与下载（weasyprint + pdfunite）
  3. 番茄大王身份验证

部署前需要改的地方（搜索 FIXME）：
  - ADMIN_PASS: 站长密码，用于「番茄大王」身份验证
  - HTML_DIR / HTML_DIR_CS: 静态网站路径
  - PDF_CACHE: PDF 缓存目录

依赖安装（Debian/Ubuntu）：
  apt-get install -y fonts-noto-cjk poppler-utils
  pip install fastapi uvicorn weasyprint

启动：
  uvicorn app:app --host 0.0.0.0 --port 8890
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import sqlite3, os, subprocess, threading
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from weasyprint import HTML

app = FastAPI()
# CORS 中间件已移除 (2026-08-09 安全加固: 同源部署不需要跨域)

# ==== CONFIG: 修改为你的实际路径和密码 ====
DB = '/opt/exam-comments/comments.db'
ADMIN_PASS = os.environ.get('EXAM_ADMIN_PASS', '')  # 从环境变量读取，空则番茄大王验证永远失败
CST = timezone(timedelta(hours=8))
HTML_DIR = '/var/www/exam-bank/python'   # FIXME: Python 章节 HTML 路径
HTML_DIR_CS = '/var/www/exam-bank/cs'    # FIXME: CS 章节 HTML 路径
HTML_DIR_AUDIT = '/var/www/exam-bank/audit'  # 审计学 HTML 路径
PDF_CACHE = '/opt/exam-comments/pdf_cache'  # FIXME: PDF 缓存目录

CHAPTERS = [
    ('一', '第一章'), ('二', '第二章'), ('三', '第三章'), ('四', '第四章'),
    ('五', '第五章'), ('六', '第六章'), ('七', '第七章'), ('八', '第八章'),
    ('九', '第九章'), ('十', '第十章'), ('十一', '第十一章'), ('十二', '第十二章'), ('十三', '第十三章'),
]

CS_CHAPTERS = [
    ('00', '第00章'), ('01', '第01章'), ('02', '第02章'), ('03', '第03章'),
    ('04', '第04章'), ('05', '第05章'), ('06', '第06章'), ('09', '第09章'),
]

AUDIT_CHAPTERS = [
    ('01', '第01章', '审计学_第01章_审计概述_浓缩版.html'),
    ('02', '第02章', '审计学_第02章_职业道德_浓缩版.html'),
    ('03', '第03章', '审计学_第03章_审计证据_浓缩版.html'),
    ('04', '第04章', '审计学_第04章_审计计划_浓缩版.html'),
    ('05', '第05章', '审计学_第05章_审计抽样_浓缩版.html'),
    ('06', '第06章', '审计学_第06章_审计工作底稿_浓缩版.html'),
    ('07', '第07章', '审计学_第07章_风险评估_浓缩版.html'),
    ('08', '第08章', '审计学_第08章_风险应对_浓缩版.html'),
    ('09', '第09章', '审计学_第09章_完成审计工作与审计报告_浓缩版.html'),
    ('10', '第10章', '审计学_第10章_销售与收款循环审计_浓缩版.html'),
]

os.makedirs(PDF_CACHE, exist_ok=True)

NUM_MAP = {'1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七',
           '8':'八','9':'九','10':'十','11':'十一','12':'十二','13':'十三',
           '一':'一','二':'二','三':'三','四':'四','五':'五','六':'六',
           '七':'七','八':'八','九':'九','十':'十','十一':'十一','十二':'十二','十三':'十三'}

# ---- 数据库初始化 ----
with sqlite3.connect(DB) as c:
    c.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT DEFAULT '匿名', content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    try:
        c.execute("ALTER TABLE comments ADD COLUMN name TEXT DEFAULT '匿名'")
    except:
        pass

class CommentReq(BaseModel):
    content: str
    name: str = '匿名'
    password: str = ''

@app.post('/api/comment')
def post_comment(r: CommentReq):
    """发布评论。如果昵称是「番茄大王」需要验证密码。"""
    c = r.content.strip()
    if len(c) < 1:
        raise HTTPException(400, '内容不能为空')
    if len(c) > 500:
        raise HTTPException(400, '不能超过500字')
    if '<' in c or '>' in c:
        raise HTTPException(400, '评论内容不能包含尖括号（HTML标签会被拦截）')
    n = r.name.strip()[:20] if r.name.strip() else '匿名'
    if '<' in n or '>' in n:
        raise HTTPException(400, '昵称不能包含尖括号')
    if n == '番茄大王' and (not ADMIN_PASS or r.password != ADMIN_PASS):
        raise HTTPException(403, '昵称「番茄大王」已被站长保留，如需输入密码请输入')
    now = datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB) as conn:
        conn.execute('INSERT INTO comments(name,content,created_at) VALUES(?,?,?)', (n, r.content, now))
    return {'ok': True}

@app.get('/api/comments')
def get_comments(page: int = 1, size: int = 20):
    """分页加载评论列表。"""
    with sqlite3.connect(DB) as conn:
        rows = conn.execute('SELECT id,name,content,created_at FROM comments ORDER BY id DESC LIMIT ? OFFSET ?', (size, (page-1)*size)).fetchall()
        total = conn.execute('SELECT COUNT(*) FROM comments').fetchone()[0]
    return {'comments': [{'id':r[0],'name':r[1],'content':r[2],'created_at':r[3]} for r in rows], 'total':total, 'page':page, 'size':size}

# ---- PDF 生成（懒加载 + 磁盘缓存） ----
_gen_lock = threading.Lock()

def _get_cached_pdf(chapter_name: str, html_dir: str, file_prefix: str = 'Python') -> bytes:
    """
    获取 PDF 文件，如果缓存中没有则用 weasyprint 从 HTML 生成。
    首次生成需要 10-30 秒，之后从缓存秒出。
    """
    cache_path = os.path.join(PDF_CACHE, f'{chapter_name}.pdf')
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return f.read()
    with _gen_lock:
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return f.read()
        html_path = os.path.join(html_dir, f'{file_prefix}{chapter_name}_浓缩版.html')
        if not os.path.exists(html_path):
            raise HTTPException(404, f'文件不存在: {html_path}')
        with open(html_path, 'r', encoding='utf-8') as f:
            doc = HTML(string=f.read(), base_url=html_dir)
        doc.write_pdf(target=cache_path)
    with open(cache_path, 'rb') as f:
        return f.read()

def _get_cached_pdf_by_file(chapter_label: str, html_dir: str, filename: str) -> bytes:
    """
    按完整文件名生成/获取 PDF（审计学用）。
    与 _get_cached_pdf 逻辑相同，但不拼接前缀，直接用传入的 filename。
    """
    cache_path = os.path.join(PDF_CACHE, f'{chapter_label}.pdf')
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return f.read()
    with _gen_lock:
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return f.read()
        html_path = os.path.join(html_dir, filename)
        if not os.path.exists(html_path):
            raise HTTPException(404, f'文件不存在: {html_path}')
        with open(html_path, 'r', encoding='utf-8') as f:
            doc = HTML(string=f.read(), base_url=html_dir)
        doc.write_pdf(target=cache_path)
    with open(cache_path, 'rb') as f:
        return f.read()

@app.get('/api/pdf/{chapter}')
def download_pdf(chapter: str):
    """下载 Python 单章 PDF，参数为中文数字（一~十三）或阿拉伯数字（1~13）。"""
    cn = NUM_MAP.get(chapter)
    if not cn:
        raise HTTPException(404, f'无效章节: {chapter}')
    name = None
    for n, full in CHAPTERS:
        if n == cn:
            name = full
            break
    if not name:
        raise HTTPException(404, f'章节不存在: {chapter}')
    try:
        pdf_bytes = _get_cached_pdf(name, HTML_DIR)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f'PDF生成失败: {str(e)}')
    safe_name = quote(f'Python第{cn}章_浓缩版.pdf')
    return Response(content=pdf_bytes, media_type='application/pdf',
                    headers={'Content-Disposition': f"attachment; filename*=UTF-8''{safe_name}"})

@app.get('/api/pdf-all')
def download_all_pdf():
    """下载 Python 全部 13 章合并 PDF，使用 pdfunite 拼接缓存文件。"""
    pdf_files = []
    for num, name in CHAPTERS:
        try:
            _get_cached_pdf(name, HTML_DIR)
            pdf_files.append(os.path.join(PDF_CACHE, f'{name}.pdf'))
        except Exception as e:
            raise HTTPException(500, f'生成第{num}章PDF失败: {str(e)}')
    output = os.path.join(PDF_CACHE, 'all_13.pdf')
    if os.path.exists(output):
        os.remove(output)
    result = subprocess.run(['pdfunite'] + pdf_files + [output], capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise HTTPException(500, f'PDF合并失败: {result.stderr}')
    with open(output, 'rb') as f:
        pdf_bytes = f.read()
    safe_name = quote('Python题库浓缩版_全13章.pdf')
    return Response(content=pdf_bytes, media_type='application/pdf',
                    headers={'Content-Disposition': f"attachment; filename*=UTF-8''{safe_name}"})

@app.get('/api/pdf/cs/{chapter}')
def download_pdf_cs(chapter: str):
    """下载计算机科学概论单章 PDF，参数为章节号（00~09）。"""
    valid = [n for n, _ in CS_CHAPTERS]
    if chapter not in valid:
        raise HTTPException(404, f'无效章节: {chapter}，可选: {valid}')
    name = None
    for n, full in CS_CHAPTERS:
        if n == chapter:
            name = full
            break
    try:
        pdf_bytes = _get_cached_pdf(name, HTML_DIR_CS, file_prefix='计算机科学概论_')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f'PDF生成失败: {str(e)}')
    safe_name = quote(f'计算机科学概论_第{chapter}章_浓缩版.pdf')
    return Response(content=pdf_bytes, media_type='application/pdf',
                    headers={'Content-Disposition': f"attachment; filename*=UTF-8''{safe_name}"})

@app.get('/api/pdf-all/cs')
def download_all_pdf_cs():
    """下载计算机科学概论全部 8 章合并 PDF。"""
    pdf_files = []
    for num, name in CS_CHAPTERS:
        try:
            _get_cached_pdf(name, HTML_DIR_CS, file_prefix='计算机科学概论_')
            pdf_files.append(os.path.join(PDF_CACHE, f'{name}.pdf'))
        except Exception as e:
            raise HTTPException(500, f'生成第{num}章PDF失败: {str(e)}')
    output = os.path.join(PDF_CACHE, 'all_cs.pdf')
    if os.path.exists(output):
        os.remove(output)
    result = subprocess.run(['pdfunite'] + pdf_files + [output], capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise HTTPException(500, f'PDF合并失败: {result.stderr}')
    with open(output, 'rb') as f:
        pdf_bytes = f.read()
    safe_name = quote('计算机科学概论_全8章.pdf')
    return Response(content=pdf_bytes, media_type='application/pdf',
                    headers={'Content-Disposition': f"attachment; filename*=UTF-8''{safe_name}"})

@app.get('/api/pdf/audit/{chapter}')
def download_pdf_audit(chapter: str):
    """下载审计学单章 PDF，参数为章节号（01~10）。"""
    valid = [n for n, _, _ in AUDIT_CHAPTERS]
    if chapter not in valid:
        raise HTTPException(404, f'无效章节: {chapter}，可选: {valid}')
    label = None
    filename = None
    for n, lbl, fn in AUDIT_CHAPTERS:
        if n == chapter:
            label = lbl
            filename = fn
            break
    if not label or not filename:
        raise HTTPException(404, f'章节数据异常: {chapter}')
    try:
        pdf_bytes = _get_cached_pdf_by_file(label, HTML_DIR_AUDIT, filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f'PDF生成失败: {str(e)}')
    safe_name = quote(f'审计学_{label}_浓缩版.pdf')
    return Response(content=pdf_bytes, media_type='application/pdf',
                    headers={'Content-Disposition': f"attachment; filename*=UTF-8''{safe_name}"})

@app.get('/api/pdf-all/audit')
def download_all_pdf_audit():
    """下载审计学全部 10 章合并 PDF。"""
    pdf_files = []
    for num, label, filename in AUDIT_CHAPTERS:
        try:
            _get_cached_pdf_by_file(label, HTML_DIR_AUDIT, filename)
            pdf_files.append(os.path.join(PDF_CACHE, f'{label}.pdf'))
        except Exception as e:
            raise HTTPException(500, f'生成{label}PDF失败: {str(e)}')
    output = os.path.join(PDF_CACHE, 'all_audit.pdf')
    if os.path.exists(output):
        os.remove(output)
    result = subprocess.run(['pdfunite'] + pdf_files + [output], capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise HTTPException(500, f'PDF合并失败: {result.stderr}')
    with open(output, 'rb') as f:
        pdf_bytes = f.read()
    safe_name = quote('审计学题库浓缩版_全10章.pdf')
    return Response(content=pdf_bytes, media_type='application/pdf',
                    headers={'Content-Disposition': f"attachment; filename*=UTF-8''{safe_name}"})
