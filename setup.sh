#!/bin/bash

# Quick Setup Script for Stealth Job Discovery Bot
# Makes installation super easy!

echo "======================================"
echo "🤖 Stealth Job Discovery Bot Setup"
echo "======================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

echo ""
echo "⚡ Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

echo ""
echo "🔑 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - SERPAPI_KEY (get from https://serpapi.com/)"
    echo "   - GEMINI_API_KEY (get from https://aistudio.google.com/app/apikey)"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "📝 Next Steps:"
echo "1. Edit .env and add your API keys"
echo "2. Activate environment: source venv/bin/activate"
echo "3. Run the UI: python ui_app.py"
echo "4. Open browser: http://localhost:7860"
echo ""
echo "🎉 Happy Job Hunting!"
echo ""
