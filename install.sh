#!/bin/bash
# Cortex Knowledge Base - Installation Script
# Automated setup for Cortex KB

set -e  # Exit on error

echo "=========================================="
echo "Cortex Knowledge Base - Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✓ Found pip"
echo ""

# Ask user about virtual environment
echo "Would you like to create a virtual environment? (recommended)"
read -p "Create venv? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "✓ Virtual environment created"
    echo ""
    echo "Activating virtual environment..."
    
    # Activate based on OS
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    PIP_CMD="pip"
    echo "✓ Virtual environment activated"
fi

echo ""
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

echo ""
echo "✓ Dependencies installed successfully!"
echo ""

# Create data directory
if [ ! -d "cortex_data" ]; then
    echo "Creating data directory..."
    mkdir -p cortex_data
    echo "✓ Data directory created"
fi

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Environment file created"
    echo "  You can customize settings in .env"
fi

echo ""
echo "=========================================="
echo "Installation Complete! 🎉"
echo "=========================================="
echo ""
echo "✅ Your installation is PERSISTENT"
echo "   - Virtual environment: ./venv (if created)"
echo "   - Data directory: ./cortex_data"
echo "   - Configuration: ./.env"
echo "   All files remain after reboot!"
echo ""
echo "To get started:"
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "1. Activate the virtual environment:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "   venv\\Scripts\\activate"
    else
        echo "   source venv/bin/activate"
    fi
    echo ""
fi

echo "2. Add your first document:"
echo "   python cortex_cli.py add document.md"
echo ""
echo "3. Try the demo:"
echo "   ./demo.sh"
echo ""
echo "4. View help:"
echo "   python cortex_cli.py --help"
echo ""
echo "📦 Data Persistence:"
echo "   Your knowledge base is saved in: ./cortex_data/"
echo "   This directory persists across sessions and reboots"
echo "   Backup: tar -czf backup.tar.gz cortex_data/"
echo ""
echo "For more information, see:"
echo "  - README.md - Full documentation"
echo "  - QUICKSTART.md - Quick start guide"
echo "  - DEPLOYMENT.md - Deployment options"
echo "  - CLOUD_DEPLOY.md - Easy cloud deployment"
echo ""
echo "Happy knowledge building! 🧠"
