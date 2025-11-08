#!/bin/bash
# Quick start script for BIO-RED Validation Portal

echo "🔬 BIO-RED Data Validation Portal"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -q streamlit pandas openpyxl --user
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🚀 Starting validation portal..."
echo "📱 Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start Streamlit
python3 -m streamlit run validation_portal.py
