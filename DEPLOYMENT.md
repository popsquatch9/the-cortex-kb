# Deployment Guide for Cortex Knowledge Base

## Understanding the Application

**Cortex Knowledge Base is a Python CLI application**, not a web application. Therefore:
- ❌ **GitHub Pages is NOT suitable** - GitHub Pages hosts static HTML/CSS/JS websites
- ✅ **Use local installation or containerization** - This is a command-line tool that runs on your machine

## Deployment Options

### Option 1: Local Installation (Recommended for Personal Use)

This is the simplest way to use Cortex on your personal computer.

#### Quick Install

```bash
# Clone the repository
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb

# Install dependencies
pip install -r requirements.txt

# Start using it!
python cortex_cli.py --help
```

#### System-wide Installation (Optional)

Make Cortex available from anywhere on your system:

```bash
# Install as a Python package
pip install -e .

# Now you can use it from anywhere
cortex --help
```

### Option 2: Docker Container (Recommended for Consistency)

Use Docker for a consistent, isolated environment.

```bash
# Build the Docker image
docker build -t cortex-kb .

# Run with mounted data directory
docker run -it -v $(pwd)/cortex_data:/app/cortex_data cortex-kb

# Or run interactively
docker run -it cortex-kb bash
```

### Option 3: Virtual Environment (Best Practice)

Isolate dependencies using a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Use the application
python cortex_cli.py add document.md
```

### Option 4: Cloud Deployment (Advanced)

For running Cortex on a server or cloud instance:

#### Option 4a: Linux Server/VPS

```bash
# SSH into your server
ssh user@your-server.com

# Install Python 3.8+
sudo apt update
sudo apt install python3 python3-pip

# Clone and setup
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb
pip3 install -r requirements.txt

# Run as needed
python3 cortex_cli.py stats
```

#### Option 4b: GitHub Codespaces

1. Go to the repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for environment to load
4. Run: `pip install -r requirements.txt`
5. Start using: `python cortex_cli.py --help`

### Option 5: PyPI Package (Future Enhancement)

Once published to PyPI, you'll be able to:

```bash
pip install cortex-kb
cortex --help
```

## Automated Installation Script

Use the provided install script for one-command setup:

```bash
./install.sh
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` to customize:
- `DATA_DIR`: Where to store your knowledge base
- `RELEVANCE_THRESHOLD`: Minimum similarity for relationships
- `ENABLE_WEB_SEARCH`: Enable/disable external source discovery

### Data Persistence

Your knowledge base is stored in JSON files in the data directory (default: `./cortex_data`).

**Important**: Back up this directory regularly!

```bash
# Backup your knowledge base
tar -czf cortex_backup_$(date +%Y%m%d).tar.gz cortex_data/

# Restore from backup
tar -xzf cortex_backup_20260304.tar.gz
```

## Running Cortex

### Basic Usage

```bash
# Add a document
python cortex_cli.py add document.md

# Search your knowledge
python cortex_cli.py search "machine learning"

# View statistics
python cortex_cli.py stats
```

### As a Service (Linux)

To run Cortex as a background service on Linux:

```bash
# See the systemd service file
cat cortex-kb.service

# Install the service
sudo cp cortex-kb.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cortex-kb
sudo systemctl start cortex-kb
```

## Web Interface (Future Enhancement)

Currently, Cortex is a CLI application. To make it web-accessible:

### Option A: Add Flask/FastAPI Web UI

A web interface could be added in the future with:
- Flask or FastAPI backend
- Simple HTML/CSS/JS frontend
- Deploy to Heroku, Render, or Railway

### Option B: Static Documentation Site on GitHub Pages

While the app can't run on GitHub Pages, you can host **documentation**:

1. Create a `docs/` folder with HTML documentation
2. Enable GitHub Pages in repository settings
3. Point to `docs/` folder
4. Access at: `https://popsquatch9.github.io/the-cortex-kb/`

## Sharing Your Knowledge Base

### Option 1: Export to Static HTML

```bash
# Export your knowledge base to HTML (feature to be added)
python cortex_cli.py export --format html --output ./export/
```

Then host the `export/` folder on GitHub Pages!

### Option 2: Share the Data Files

```bash
# Share your cortex_data folder
zip -r my_knowledge_base.zip cortex_data/
```

Others can extract and use it with their own Cortex installation.

### Option 3: Collaborate via Git

```bash
# Version control your knowledge base
cd cortex_data
git init
git add .
git commit -m "Initial knowledge base"
git remote add origin https://github.com/you/my-knowledge.git
git push -u origin main
```

## Troubleshooting

### Issue: ModuleNotFoundError

```bash
# Ensure dependencies are installed
pip install -r requirements.txt
```

### Issue: Permission Denied

```bash
# Make scripts executable
chmod +x cortex_cli.py
chmod +x install.sh
chmod +x demo.sh
```

### Issue: Can't Find Python

```bash
# Use python3 explicitly
python3 cortex_cli.py --help
```

## Performance Tips

1. **Use SSD Storage**: Store `cortex_data` on SSD for faster access
2. **Limit Document Size**: Very large documents may slow down embedding
3. **Batch Operations**: Add multiple documents at once for efficiency
4. **Regular Cleanup**: Remove unused documents to keep the graph lean

## Security Considerations

1. **Backup Regularly**: Your knowledge base is valuable data
2. **Secure API Keys**: If using external APIs, use environment variables
3. **Access Control**: If running on a server, use proper authentication
4. **Data Privacy**: Knowledge base contains your personal information

## Next Steps

1. Choose your deployment method (Local, Docker, or Cloud)
2. Follow the installation steps
3. Configure your environment
4. Start building your knowledge base!

## Getting Help

- Read the [README.md](README.md) for usage instructions
- Check [QUICKSTART.md](QUICKSTART.md) for quick setup
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- Run `python cortex_cli.py --help` for command reference

## Future Roadmap

- [ ] Package for PyPI distribution (`pip install cortex-kb`)
- [ ] Add web UI with Flask/FastAPI
- [ ] Create browser extension for quick capture
- [ ] Mobile app for on-the-go access
- [ ] Cloud sync support
- [ ] Multi-user collaboration features
