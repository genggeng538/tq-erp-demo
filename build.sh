#!/usr/bin/env bash
set -e

echo "📦 安装依赖"
pip install -r requirements.txt

echo "📂 收集静态文件"
python manage.py collectstatic --noinput

echo "🧱 执行数据库迁移"
python manage.py migrate --noinput

echo "👤 确保管理员存在"
python manage.py ensure_admin

echo "🚀 启动完成"
