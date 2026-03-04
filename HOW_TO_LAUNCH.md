# How to Launch Cortex Knowledge Base

## Quick Answer

**GitHub Pages is NOT suitable for Cortex KB** because it's a Python CLI application, not a static website. GitHub Pages only hosts HTML/CSS/JavaScript files.

## Recommended Launch Methods

### 🚀 Method 1: Local Installation (Easiest)

**Best for**: Personal use on your computer

```bash
# One-command install
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb
./install.sh

# Then use it!
python cortex_cli.py add document.md
python cortex_cli.py search "your query"
```

### 🐳 Method 2: Docker (Most Consistent)

**Best for**: Clean, isolated environment

```bash
# Using Docker Compose (recommended)
docker-compose up -d
docker-compose exec cortex-kb python cortex_cli.py stats

# Or build and run directly
docker build -t cortex-kb .
docker run -it -v $(pwd)/cortex_data:/app/cortex_data cortex-kb
```

### 📦 Method 3: System-wide Install

**Best for**: Convenience across your system

```bash
# Install as a package
pip install -e .

# Now use from anywhere
cortex add document.md
cortex search "query"
```

### ☁️ Method 4: Cloud Server

**Best for**: Remote access, always-on service

```bash
# SSH to your VPS/EC2/Digital Ocean instance
ssh user@your-server.com

# Install and run
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb
pip3 install -r requirements.txt
python3 cortex_cli.py stats
```

### 💻 Method 5: GitHub Codespaces

**Best for**: Try without installing locally

1. Go to https://github.com/popsquatch9/the-cortex-kb
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment to load
4. Run: `pip install -r requirements.txt`
5. Use: `python cortex_cli.py --help`

## What About GitHub Pages?

### ❌ Why NOT GitHub Pages?

GitHub Pages is for **static websites** (HTML/CSS/JS). Cortex is a **Python application** that needs:
- Python runtime environment
- File system access for data storage
- Package dependencies (sentence-transformers, etc.)
- Command-line execution

None of these work with GitHub Pages.

### ✅ What CAN Go on GitHub Pages?

You could create:

1. **Documentation website**
   - Host user guides, tutorials
   - API documentation
   - Example usage

2. **Static export** (future feature)
   - Export your knowledge base to HTML
   - Create a read-only website version
   - Share knowledge publicly

Example future workflow:
```bash
# Export to static HTML (not implemented yet)
python cortex_cli.py export --format html --output docs/

# Then enable GitHub Pages for docs/ folder
# Access at: https://username.github.io/the-cortex-kb/
```

## Comparison Table

| Method | Difficulty | Use Case | Persistent Data |
|--------|-----------|----------|-----------------|
| Local Install | ⭐ Easy | Personal use | ✅ Yes |
| Docker | ⭐⭐ Medium | Isolation, consistency | ✅ Yes (volumes) |
| pip Install | ⭐ Easy | System-wide access | ✅ Yes |
| Cloud Server | ⭐⭐⭐ Advanced | Remote access | ✅ Yes |
| GitHub Codespaces | ⭐ Easy | Try before install | ⚠️ Temporary |
| GitHub Pages | ❌ Not Possible | N/A | ❌ No |

## Quick Start Commands

```bash
# Clone
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb

# Install (choose one)
./install.sh                    # Automated
pip install -r requirements.txt # Manual
docker-compose up -d            # Docker
pip install -e .                # Package

# Verify
python cortex_cli.py --help

# Use
python cortex_cli.py add examples/machine_learning.md
python cortex_cli.py search "AI"
python cortex_cli.py stats
```

## Next Steps

1. Choose your launch method above
2. Follow the installation steps
3. Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed options
4. Check [QUICKSTART.md](QUICKSTART.md) for usage guide
5. Start building your knowledge base!

## Common Questions

**Q: Can I access Cortex from a web browser?**
A: Not currently. It's a CLI tool. A web UI could be added in the future.

**Q: Can I run it on Windows?**
A: Yes! Use the install.sh script in Git Bash or WSL, or install manually with pip.

**Q: Can I share my knowledge base?**
A: Yes! You can:
- Share the cortex_data/ folder
- Version control it with Git
- Export to HTML (future feature)

**Q: How do I backup my data?**
A: Your data is in cortex_data/. Just copy/zip that folder:
```bash
tar -czf backup.tar.gz cortex_data/
```

**Q: Can multiple people use it?**
A: Currently single-user. Multi-user features are on the roadmap.

## Getting Help

- **Installation Issues**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Usage Help**: See [QUICKSTART.md](QUICKSTART.md)
- **Technical Details**: See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Command Help**: Run `python cortex_cli.py --help`

---

**Summary**: Use local installation or Docker to launch Cortex. GitHub Pages is only for static websites and cannot run Python applications.
