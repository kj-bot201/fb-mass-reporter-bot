#!/bin/bash

# Facebook Mass Reporter Bot - Setup Script

echo "🚀 Facebook Mass Reporter Bot - Setup"
echo "====================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed"

# Check if config files exist
echo ""
echo "Checking configuration files..."

if [ ! -f "config.json" ]; then
    echo "⚠️  config.json not found. Creating template..."
    cp config.json.template config.json 2>/dev/null || echo "Please create config.json manually"
fi

if [ ! -f "accounts.json" ]; then
    echo "⚠️  accounts.json not found. Creating template..."
    cp accounts.json.template accounts.json 2>/dev/null || echo "Please create accounts.json manually"
fi

echo ""
echo "====================================="
echo "✅ Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit config.json with your Facebook credentials"
echo "2. Edit accounts.json with scam account URLs"
echo "3. Run: python main.py"
echo ""
echo "⚠️  Warning: This may get your account banned!"
echo ""
