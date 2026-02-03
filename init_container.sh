#!/bin/bash
echo "🔧 Installing Dev Tools inside postman-lab..."
sudo dnf install -y python3-pip python3-devel git cloudflared jq nano

echo "🐍 Setting up Python Virtual Environment..."
cd "$HOME/funspace/projects/demo"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate and Install basics
source venv/bin/activate
pip install --upgrade pip
# We install FastAPI, Uvicorn (server), PyJWT (Auth), and Pydantic (Validation)
pip install fastapi "uvicorn[standard]" pyjwt pydantic python-multipart requests

echo "✅ Environment Ready. To activate in the future: source venv/bin/activate"
