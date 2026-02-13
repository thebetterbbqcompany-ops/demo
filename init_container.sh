#!/bin/bash
echo "🔧 Installing Dev Tools inside postman-lab..."
sudo dnf install -y python3-pip python3-devel git cloudflared jq nano

echo "🐍 Setting up Python Virtual Environment..."
cd "$HOME/funspace/projects/demo"

echo "🧹 Wiping old environment..."
rm -rf venv

echo "🌱 Creating fresh venv..."
python3 -m venv venv

source venv/bin/activate
pip install --upgrade pip

echo "📦 Installing Libraries..."
# ADDED: httpx
pip install fastapi "uvicorn[standard]" pyjwt pydantic python-multipart requests httpx sse-starlette
echo "✅ Environment Ready."
