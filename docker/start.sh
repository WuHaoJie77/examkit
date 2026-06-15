#!/bin/bash
set -e

# 启动 FastAPI 后端（后台运行）
cd /app
uvicorn app:app --host 127.0.0.1 --port 8890 &
API_PID=$!

# 启动 Nginx（前台运行）
echo "🚀 后端已启动 (PID: $API_PID)"
echo "🌐 前端监听 :8898"
nginx -g "daemon off;"
