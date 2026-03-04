# Easy Cloud Deployment Guide

## TL;DR - One Command Cloud Deploy

```bash
# On your cloud server (DigitalOcean, AWS EC2, etc.)
curl -fsSL https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh | bash
```

Or manually:
```bash
wget https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh
chmod +x cloud-deploy.sh
./cloud-deploy.sh
```

## Is Cloud Deployment Easy? YES! ✅

We've simplified cloud deployment to be as easy as local installation. Here are your options:

### Option 1: One-Click Cloud Platforms (Easiest) ⭐

These platforms handle everything for you:

#### Railway.app
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the button above or go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Fork this repository
4. Click "Deploy Now"
5. Done! Railway handles everything automatically

**Persistence**: ✅ Built-in persistent volumes
**Cost**: Free tier available, then ~$5/month
**Difficulty**: ⭐ Very Easy

#### Render.com
1. Go to [Render.com](https://render.com)
2. Create a new "Background Worker"
3. Connect to this repository
4. Render auto-deploys from git
5. Add persistent disk storage

**Persistence**: ✅ Persistent disks available
**Cost**: Free tier available, then ~$7/month
**Difficulty**: ⭐ Very Easy

### Option 2: Simple VPS Deployment (Easy) ⭐⭐

Perfect for DigitalOcean, Linode, Vultr, etc.

#### Quick Setup (5 minutes)

```bash
# 1. SSH to your server
ssh root@your-server-ip

# 2. Run the cloud deployment script
curl -fsSL https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh | bash

# 3. Done! Start using Cortex
cd /opt/cortex-kb
source venv/bin/activate
python cortex_cli.py stats
```

**What the script does:**
- ✅ Installs Python and dependencies
- ✅ Clones the repository
- ✅ Creates virtual environment
- ✅ Sets up persistent data directory
- ✅ Creates systemd service (auto-start on boot)
- ✅ Configures everything automatically

**Persistence**: ✅ Full persistence with `/var/lib/cortex-kb`
**Cost**: $5-10/month for basic VPS
**Difficulty**: ⭐⭐ Easy (just run one command)

### Option 3: Manual Cloud Setup (Most Control) ⭐⭐⭐

If you prefer to do it yourself:

```bash
# 1. SSH to server
ssh user@your-server.com

# 2. Install Python
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# 3. Clone repository
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure persistent storage
mkdir -p /var/lib/cortex-kb
nano .env  # Set DATA_DIR=/var/lib/cortex-kb

# 7. Test it
python cortex_cli.py stats
```

**Persistence**: ✅ You control everything
**Cost**: Varies by provider
**Difficulty**: ⭐⭐⭐ Medium (more steps)

## Data Persistence Explained

### Your Data is ALWAYS Persistent ✅

No matter which deployment method you choose, your knowledge base is persistent:

| What | Where | Persistent? |
|------|-------|-------------|
| Knowledge base data | `cortex_data/` or `/var/lib/cortex-kb` | ✅ Yes - survives reboots |
| Python packages | `venv/` | ✅ Yes - survives reboots |
| Configuration | `.env` | ✅ Yes - survives reboots |
| Application code | Repository clone | ✅ Yes - survives reboots |

**The ONLY thing that's temporary is the Python process itself** - but your data is always saved to disk!

### How to Verify Persistence

```bash
# Add some data
python cortex_cli.py add-text "Test persistence" --name "Test"

# Reboot the server
sudo reboot

# After reboot, SSH back in and check
cd /opt/cortex-kb  # or your installation directory
source venv/bin/activate
python cortex_cli.py list

# Your data is still there! ✅
```

## Recommended Cloud Providers

### For Beginners

1. **Railway.app** - Absolute easiest, one-click deploy
2. **Render.com** - Very simple, good free tier
3. **DigitalOcean** - User-friendly VPS, good documentation

### For Advanced Users

1. **AWS Lightsail** - Cheap VPS, AWS integration
2. **Linode** - Great performance, simple pricing
3. **Vultr** - Fast deployment, many locations

### Cost Comparison

| Provider | Cheapest Option | Persistence | Setup Time |
|----------|-----------------|-------------|------------|
| Railway | Free tier, then $5/mo | ✅ Yes | 2 minutes |
| Render | Free tier, then $7/mo | ✅ Yes | 3 minutes |
| DigitalOcean | $6/mo | ✅ Yes | 5 minutes |
| AWS Lightsail | $3.50/mo | ✅ Yes | 5 minutes |
| Linode | $5/mo | ✅ Yes | 5 minutes |

## Quick Start: DigitalOcean Example

1. **Create Droplet**
   - Go to DigitalOcean.com
   - Create → Droplets
   - Choose: Ubuntu 22.04
   - Size: Basic $6/mo
   - Add SSH key
   - Click "Create Droplet"

2. **Deploy Cortex** (wait 60 seconds for droplet to start)
   ```bash
   ssh root@your-droplet-ip
   curl -fsSL https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh | bash
   ```

3. **Done!** Start using:
   ```bash
   cd /opt/cortex-kb
   source venv/bin/activate
   python cortex_cli.py add document.md
   ```

## Persistence Best Practices

### 1. Regular Backups

Even though data is persistent, always backup:

```bash
# On your cloud server
cd /var/lib/cortex-kb  # or your data directory
tar -czf ~/cortex-backup-$(date +%Y%m%d).tar.gz .

# Download backup to your computer
# On your local machine:
scp user@server:~/cortex-backup-20260304.tar.gz ./
```

### 2. Auto-start on Boot

Using `cloud-deploy.sh` automatically sets this up:

```bash
# Enable auto-start
sudo systemctl enable cortex-kb

# Check if it's enabled
sudo systemctl status cortex-kb
```

### 3. Monitor Disk Space

```bash
# Check available space
df -h /var/lib/cortex-kb

# Clean up old backups if needed
rm ~/cortex-backup-*.tar.gz
```

## Troubleshooting Cloud Deployment

### Issue: "Command not found" after reboot

**Solution**: You need to activate the virtual environment again

```bash
cd /opt/cortex-kb  # or your installation path
source venv/bin/activate
```

### Issue: "Data disappeared"

**Solution**: Check if you're in the right directory

```bash
# Find your data
find / -name "cortex_data" 2>/dev/null
find / -name "nodes.json" 2>/dev/null

# Or check the configured data directory
cat .env | grep DATA_DIR
```

### Issue: "Permission denied"

**Solution**: Fix ownership

```bash
sudo chown -R $USER:$USER /opt/cortex-kb
sudo chown -R $USER:$USER /var/lib/cortex-kb
```

### Issue: "Service won't start"

**Solution**: Check the service logs

```bash
sudo systemctl status cortex-kb
sudo journalctl -u cortex-kb -n 50
```

## Accessing from Multiple Machines

Once deployed to the cloud, you can:

1. **SSH from anywhere**
   ```bash
   ssh user@your-server.com
   cd /opt/cortex-kb && source venv/bin/activate
   python cortex_cli.py search "query"
   ```

2. **Use screen/tmux for persistent sessions**
   ```bash
   # Start a screen session
   screen -S cortex
   cd /opt/cortex-kb && source venv/bin/activate
   
   # Detach: Ctrl+A, then D
   # Reattach later: screen -r cortex
   ```

3. **Add alias for convenience**
   ```bash
   echo 'alias cortex="cd /opt/cortex-kb && source venv/bin/activate && python cortex_cli.py"' >> ~/.bashrc
   source ~/.bashrc
   
   # Now just type:
   cortex stats
   ```

## Summary

### Is Cloud Deployment Easy? **YES!** ✅

- **Easiest**: Use Railway/Render (2-3 minutes, one-click)
- **Easy**: Use `cloud-deploy.sh` on any VPS (5 minutes, one command)
- **Manual**: Traditional setup (10-15 minutes, full control)

### Is Data Persistent? **YES!** ✅

- All data is stored on disk
- Survives reboots and server restarts
- Only the Python process is temporary
- Backup regularly for safety

### Next Steps

1. Choose a cloud provider (Railway for easiest)
2. Run the deployment script or use one-click deploy
3. Start building your knowledge base
4. Set up regular backups

**Need help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for more options or [QUICKSTART.md](QUICKSTART.md) for usage tips.
