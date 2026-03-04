#!/bin/bash
# Cortex Knowledge Base - Cloud Deployment Script
# Easy deployment to cloud VPS or server

set -e  # Exit on error

echo "=========================================="
echo "Cortex KB - Cloud Deployment"
echo "=========================================="
echo ""

# Check if running on a server
if [[ ! -t 0 ]]; then
    echo "Running in non-interactive mode (cloud/server deployment)"
    INTERACTIVE=false
else
    echo "Running in interactive mode"
    INTERACTIVE=true
fi

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Installing Python 3..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Install system dependencies
echo ""
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y git build-essential

echo "✓ System dependencies installed"
echo ""

# Create application directory
APP_DIR="/opt/cortex-kb"
if [ "$INTERACTIVE" = true ]; then
    read -p "Installation directory [/opt/cortex-kb]: " USER_DIR
    if [ ! -z "$USER_DIR" ]; then
        APP_DIR="$USER_DIR"
    fi
fi

echo "Installing to: $APP_DIR"

# Clone or update repository
if [ -d "$APP_DIR" ]; then
    echo "Directory exists. Updating..."
    cd "$APP_DIR"
    git pull
else
    echo "Cloning repository..."
    sudo mkdir -p "$APP_DIR"
    sudo chown $USER:$USER "$APP_DIR"
    git clone https://github.com/popsquatch9/the-cortex-kb.git "$APP_DIR"
    cd "$APP_DIR"
fi

echo "✓ Repository ready"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate and install dependencies
echo ""
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Create data directory with proper permissions
DATA_DIR="/var/lib/cortex-kb"
if [ "$INTERACTIVE" = true ]; then
    read -p "Data directory [/var/lib/cortex-kb]: " USER_DATA_DIR
    if [ ! -z "$USER_DATA_DIR" ]; then
        DATA_DIR="$USER_DATA_DIR"
    fi
fi

echo "Creating data directory: $DATA_DIR"
sudo mkdir -p "$DATA_DIR"
sudo chown $USER:$USER "$DATA_DIR"
echo "✓ Data directory created"

# Setup environment file
if [ ! -f "$APP_DIR/.env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    sed -i "s|DATA_DIR=./cortex_data|DATA_DIR=$DATA_DIR|g" .env
    echo "✓ Environment file created"
fi

# Create systemd service file
echo ""
echo "Creating systemd service..."
sudo tee /etc/systemd/system/cortex-kb.service > /dev/null <<EOF
[Unit]
Description=Cortex Knowledge Base
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/cortex_cli.py stats
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Systemd service created"
echo ""

# Reload systemd
sudo systemctl daemon-reload

echo "=========================================="
echo "Cloud Deployment Complete! 🎉"
echo "=========================================="
echo ""
echo "Your Cortex KB is installed at: $APP_DIR"
echo "Data will be stored in: $DATA_DIR"
echo ""
echo "Quick commands:"
echo ""
echo "  # Activate environment"
echo "  cd $APP_DIR && source venv/bin/activate"
echo ""
echo "  # Add a document"
echo "  python cortex_cli.py add document.md"
echo ""
echo "  # Search"
echo "  python cortex_cli.py search 'query'"
echo ""
echo "  # View stats"
echo "  python cortex_cli.py stats"
echo ""
echo "Service management:"
echo "  sudo systemctl start cortex-kb    # Start service"
echo "  sudo systemctl stop cortex-kb     # Stop service"
echo "  sudo systemctl status cortex-kb   # Check status"
echo "  sudo systemctl enable cortex-kb   # Start on boot"
echo ""
echo "Data persistence:"
echo "  Your data is stored in: $DATA_DIR"
echo "  This directory persists across reboots"
echo "  Backup: tar -czf backup.tar.gz $DATA_DIR"
echo ""
echo "To backup your knowledge base:"
echo "  tar -czf cortex-backup-\$(date +%Y%m%d).tar.gz $DATA_DIR"
echo ""
echo "Happy knowledge building! 🧠"
