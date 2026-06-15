# 小番茄题库浓缩版 - Docker 镜像
# 一条命令部署：docker compose up -d

FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nginx \
    fonts-noto-cjk \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir fastapi uvicorn weasyprint

# 创建目录
RUN mkdir -p /app /var/www/exam-bank /opt/exam-comments/pdf_cache

# 复制静态网站
COPY exam-bank/ /var/www/exam-bank/

# 复制后端代码
COPY backend/app.py /app/app.py

# 复制 Nginx 配置
COPY docker/nginx.conf /etc/nginx/sites-available/default

# 复制启动脚本
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# 暴露端口
EXPOSE 8898

# 启动
CMD ["/start.sh"]
