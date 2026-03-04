# Cloud Deployment Quickstart 🚀

**Deploy Cortex KB to the cloud in under 5 minutes!**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/cortex-kb)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/popsquatch9/the-cortex-kb)

---

## 🎯 Pick Your Path

### Path 1: Absolute Easiest (2 minutes) ⭐
**Just click a button above** → Railway or Render will handle everything

### Path 2: One Command VPS (5 minutes)
**Copy-paste one command** → Works on DigitalOcean, AWS, Linode, etc.

### Path 3: Platform Comparison
**Not sure which?** → See [CLOUD_COMPARISON.md](CLOUD_COMPARISON.md)

---

## Choose Your Platform

### 🎯 Fastest: One-Click Platforms (2-3 minutes)

#### Railway.app ⭐ Recommended
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/cortex-kb)

**Why Railway?**
- ✅ Fastest deployment (2 minutes)
- ✅ Free $5 credit monthly
- ✅ Automatic HTTPS
- ✅ Built-in persistent storage
- ✅ Auto-deploys from GitHub

**Steps:**
1. Click the "Deploy on Railway" button above
2. Sign in with GitHub
3. Click "Deploy Now"
4. Done! Access your deployment URL

**After Deploy:**
```bash
# Access your Railway deployment
railway shell
source venv/bin/activate
python cortex_cli.py add document.md
```

---

#### Render.com
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/popsquatch9/the-cortex-kb)

**Why Render?**
- ✅ Free tier available
- ✅ Automatic SSL
- ✅ Git-based deployments
- ✅ Persistent disks

**Steps:**
1. Click "Deploy to Render" button above
2. Connect your GitHub account
3. Select the repository
4. Add a persistent disk (1GB is enough)
5. Click "Deploy"

---

### 💻 VPS Deployment (5 minutes)

Perfect for DigitalOcean, Linode, AWS Lightsail, Vultr, etc.

#### DigitalOcean (Most Popular)

**Create Droplet:**
1. Go to [DigitalOcean.com](https://www.digitalocean.com)
2. Create Droplet
3. Choose Ubuntu 22.04
4. Select $6/month plan
5. Add your SSH key
6. Click "Create Droplet"

**Deploy Cortex (one command):**
```bash
ssh root@your-droplet-ip
curl -fsSL https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh | bash
```

**That's it!** The script handles everything:
- ✅ Installs Python
- ✅ Sets up virtual environment
- ✅ Creates persistent storage
- ✅ Configures auto-start

---

#### AWS Lightsail

**Create Instance:**
1. Go to [AWS Lightsail](https://lightsail.aws.amazon.com)
2. Create instance
3. Select Linux/Unix → Ubuntu 22.04
4. Choose $3.50/month plan
5. Launch instance

**Deploy:**
```bash
ssh ubuntu@your-instance-ip
curl -fsSL https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh | bash
```

---

#### Linode

**Create Linode:**
1. Go to [Linode.com](https://www.linode.com)
2. Create Linode
3. Select Ubuntu 22.04
4. Choose Nanode 1GB ($5/month)
5. Deploy

**Deploy:**
```bash
ssh root@your-linode-ip
curl -fsSL https://raw.githubusercontent.com/popsquatch9/the-cortex-kb/main/cloud-deploy.sh | bash
```

---

## Platform Comparison

| Platform | Time | Cost/Month | Free Tier | Difficulty |
|----------|------|------------|-----------|------------|
| **Railway** | 2 min | $5 | $5 credit | ⭐ Easiest |
| **Render** | 3 min | $7 | Yes (limited) | ⭐ Easiest |
| **DigitalOcean** | 5 min | $6 | $200 credit | ⭐⭐ Easy |
| **AWS Lightsail** | 5 min | $3.50 | Free 3 months | ⭐⭐ Easy |
| **Linode** | 5 min | $5 | $100 credit | ⭐⭐ Easy |

## Quick Commands After Deploy

### Add Your First Document
```bash
# SSH to your server
ssh user@your-server

# Activate environment
cd /opt/cortex-kb
source venv/bin/activate

# Add a document
python cortex_cli.py add document.md

# Or add text
python cortex_cli.py add-text "Your knowledge here" --name "Note"
```

### Search Your Knowledge
```bash
python cortex_cli.py search "query"
```

### View Statistics
```bash
python cortex_cli.py stats
```

### Backup Your Data
```bash
# Backup command
tar -czf ~/cortex-backup-$(date +%Y%m%d).tar.gz /var/lib/cortex-kb

# Download backup to local machine
scp user@server:~/cortex-backup-*.tar.gz ./
```

## Troubleshooting

### Issue: Can't connect via SSH
**Solution:** Check your firewall settings and ensure SSH (port 22) is open

### Issue: Script fails
**Solution:** Run with verbose output:
```bash
bash -x cloud-deploy.sh
```

### Issue: Out of disk space
**Solution:** Check and clean:
```bash
df -h
sudo apt autoremove
```

### Issue: Service won't start
**Solution:** Check logs:
```bash
sudo systemctl status cortex-kb
sudo journalctl -u cortex-kb -n 50
```

## Next Steps

1. ✅ Choose a platform above
2. ✅ Deploy (2-5 minutes)
3. ✅ Add your first documents
4. ✅ Set up regular backups
5. ✅ Explore advanced features

## Get Help

- **Full Guide**: See [CLOUD_DEPLOY.md](CLOUD_DEPLOY.md)
- **Deployment FAQ**: See [DEPLOYMENT_FAQ.md](DEPLOYMENT_FAQ.md)
- **General Help**: See [README.md](README.md)

## Video Tutorials

Coming soon! We'll add video tutorials for:
- Railway deployment
- DigitalOcean deployment
- Using Cortex KB after deployment

---

**Ready to deploy?** Pick a platform above and start in under 5 minutes! 🚀
